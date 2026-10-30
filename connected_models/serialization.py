"""Strict bounded JSON decoding shared by stored records and agent proposals."""

from dataclasses import asdict
import hashlib
import json
from typing import Any

from .contracts import Composition, Model, ModelError, Node, Port, Reference, Value

MAX_RECORD_BYTES = 131_072


def object_fields(data: Any, required: set[str], optional: set[str] = frozenset()) -> None:
    """Reject unknown, missing and non-object payloads at contract boundaries."""
    if not isinstance(data, dict) or not required <= data.keys() or data.keys() - required - optional:
        raise ModelError(f"Invalid object fields; required: {', '.join(sorted(required))}.")


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


def model_from_dict(data: Any) -> Model:
    """Decode a complete candidate; partial raw candidates remain stored separately."""
    object_fields(data, {"id", "version", "inputs", "output", "expression", "guards", "source", "assumptions"}, {"status"})
    if not isinstance(data["inputs"], dict) or not isinstance(data["guards"], list) or not isinstance(data["assumptions"], list):
        raise ModelError("Inputs must be an object; guards and assumptions must be arrays.")
    for name in data["inputs"]:
        if not name.isidentifier():
            raise ModelError("Input symbols must be valid identifiers.")
    return Model(text(data["id"]), text(data["version"]),
        {name: port_from_dict(value) for name, value in data["inputs"].items()},
        port_from_dict(data["output"]), text(data["expression"]), tuple(text(item) for item in data["guards"]),
        text(data["source"]), tuple(text(item) for item in data["assumptions"]), "candidate")


def composition_from_dict(data: Any) -> Composition:
    """Decode explicit graph bindings; never accept arbitrary agent executable code."""
    object_fields(data, {"id", "nodes", "outputs"}, {"purpose"})
    if not isinstance(data["nodes"], list) or not isinstance(data["outputs"], list):
        raise ModelError("Nodes and outputs must be arrays.")
    nodes = []
    for raw in data["nodes"]:
        object_fields(raw, {"id", "model", "bindings"})
        if not isinstance(raw["bindings"], dict):
            raise ModelError("Bindings must be an object.")
        bindings: dict[str, Value | Reference] = {}
        for name, binding in raw["bindings"].items():
            if isinstance(binding, dict) and set(binding) == {"node"}:
                bindings[name] = Reference(text(binding["node"]))
            else:
                object_fields(binding, {"amount", "port", "origin", "evidence"})
                bindings[name] = Value(binding["amount"], port_from_dict(binding["port"]), text(binding["origin"]), text(binding["evidence"]))
        nodes.append(Node(text(raw["id"]), text(raw["model"]), bindings))
    return Composition(text(data["id"]), tuple(nodes), tuple(text(item) for item in data["outputs"]), "scenario")


def model_digest(model: Model) -> str:
    """Hash immutable model content independently of derived admission status."""
    data = asdict(model)
    data.pop("status")
    return hashlib.sha256(json.dumps(data, sort_keys=True, allow_nan=False).encode()).hexdigest()
