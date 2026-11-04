"""Strict bounded JSON decoding shared by stored records and agent proposals."""

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .contracts import (
    MAX_LLM_INSTRUCTION_CHARS,
    Composition,
    Family,
    LLMStep,
    Model,
    ModelError,
    Node,
    Port,
    Reference,
    Value,
)

MAX_RECORD_BYTES = 131_072


def object_fields(
    data: Any, required: set[str], optional: set[str] | frozenset[str] = frozenset()
) -> None:
    """Reject unknown, missing and non-object payloads at contract boundaries."""
    if (
        not isinstance(data, dict)
        or not required <= data.keys()
        or data.keys() - required - optional
    ):
        raise ModelError(
            f"Invalid object fields; required: {', '.join(sorted(required))}."
        )


def text(value: Any) -> str:
    """Require a bounded nonempty string without coercing unknown semantics."""
    if not isinstance(value, str) or not value.strip() or len(value) > MAX_RECORD_BYTES:
        raise ModelError("Expected a bounded, nonempty string.")
    return value


def port_from_dict(data: Any) -> Port:
    """Decode and validate one explicit semantic interface."""
    object_fields(data, {"meaning", "unit", "context"})
    port = Port(**{key: text(value) for key, value in data.items()})
    port.validate()
    return port


def family_from_dict(data: Any) -> Family:
    """Decode and validate one index-family declaration."""
    object_fields(data, {"meaning", "unit", "context", "max_size"})
    if type(data["max_size"]) is not int:
        raise ModelError("Family size bound must be an integer.")
    family = Family(
        text(data["meaning"]),
        text(data["unit"]),
        text(data["context"]),
        data["max_size"],
    )
    family.validate()
    return family


def model_from_dict(data: Any) -> Model:
    """Decode a complete candidate; partial raw candidates remain stored separately."""
    object_fields(
        data,
        {
            "id",
            "version",
            "inputs",
            "output",
            "expression",
            "guards",
            "source",
            "assumptions",
        },
        {"status", "families"},
    )
    if (
        not isinstance(data["inputs"], dict)
        or not isinstance(data["guards"], list)
        or not isinstance(data["assumptions"], list)
    ):
        raise ModelError(
            "Inputs must be an object; guards and assumptions must be arrays."
        )
    for name in data["inputs"]:
        if not name.isidentifier():
            raise ModelError("Input symbols must be valid identifiers.")
    families = data.get("families", {})
    if not isinstance(families, dict):
        raise ModelError("Families must be an object.")
    for name in families:
        if not name.isidentifier():
            raise ModelError("Family symbols must be valid identifiers.")
    return Model(
        text(data["id"]),
        text(data["version"]),
        {name: port_from_dict(value) for name, value in data["inputs"].items()},
        port_from_dict(data["output"]),
        text(data["expression"]),
        tuple(text(item) for item in data["guards"]),
        text(data["source"]),
        tuple(text(item) for item in data["assumptions"]),
        "candidate",
        {name: family_from_dict(value) for name, value in families.items()},
    )


def decode_element(binding: Any) -> Value | Reference:
    """Decode one scalar binding element; nested lists are rejected."""
    if isinstance(binding, dict) and set(binding) == {"node"}:
        return Reference(text(binding["node"]))
    object_fields(binding, {"amount", "port", "origin", "evidence"})
    return Value(
        binding["amount"],
        port_from_dict(binding["port"]),
        text(binding["origin"]),
        text(binding["evidence"]),
    )


def step_from_dict(data: Any) -> LLMStep:
    """Decode one bounded in-context calculation; never executable code."""
    object_fields(data, {"id", "inputs", "bindings", "output", "instruction"})
    if not isinstance(data["inputs"], dict) or not isinstance(data["bindings"], dict):
        raise ModelError("Step inputs and bindings must be objects.")
    inputs: dict[str, Port] = {}
    for name, port in data["inputs"].items():
        if not name.isidentifier():
            raise ModelError("Step input symbols must be valid identifiers.")
        inputs[name] = port_from_dict(port)
    bindings: dict[str, Value | Reference] = {}
    for name, binding in data["bindings"].items():
        if isinstance(binding, list):
            raise ModelError("LLM-computed steps take scalar bindings only.")
        bindings[name] = decode_element(binding)
    instruction = text(data["instruction"])
    if len(instruction) > MAX_LLM_INSTRUCTION_CHARS:
        raise ModelError("Computation instruction exceeds the size limit.")
    step = LLMStep(
        text(data["id"]),
        inputs,
        bindings,
        port_from_dict(data["output"]),
        instruction,
    )
    step.validate()
    return step


def composition_from_dict(data: Any) -> Composition:
    """Decode explicit graph bindings; never accept arbitrary agent executable code."""
    object_fields(data, {"id", "nodes", "outputs"}, {"purpose", "llm_steps"})
    if not isinstance(data["nodes"], list) or not isinstance(data["outputs"], list):
        raise ModelError("Nodes and outputs must be arrays.")
    nodes = []
    for raw in data["nodes"]:
        object_fields(
            raw, {"id", "model", "bindings"}, {"solve_for", "relation", "branch"}
        )
        if not isinstance(raw["bindings"], dict):
            raise ModelError("Bindings must be an object.")
        bindings: dict[str, Value | Reference | tuple[Value | Reference, ...]] = {}
        for name, binding in raw["bindings"].items():
            if isinstance(binding, list):
                bindings[name] = tuple(decode_element(element) for element in binding)
            else:
                bindings[name] = decode_element(binding)
        target = raw.get("solve_for")
        if target is not None:
            target = text(target)
        branch = raw.get("branch")
        if branch is not None:
            branch = text(branch)
        nodes.append(
            Node(
                text(raw["id"]),
                text(raw["model"]),
                bindings,
                target,
                text(raw.get("relation", "equal")),
                branch,
            )
        )
    raw_steps = data.get("llm_steps", [])
    if not isinstance(raw_steps, list):
        raise ModelError("LLM-computed steps must be an array.")
    steps = [step_from_dict(raw) for raw in raw_steps]
    return Composition(
        text(data["id"]),
        tuple(nodes),
        tuple(text(item) for item in data["outputs"]),
        "scenario",
        tuple(steps),
    )


def model_digest(model: Model) -> str:
    """Hash immutable model content independently of derived admission status."""
    data = asdict(model)
    data.pop("status")
    if not data.get("families"):
        # Models without families hash exactly as before the families field existed,
        # preserving stored digests; family declarations join the digest when present.
        data.pop("families", None)
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, allow_nan=False).encode()
    ).hexdigest()
