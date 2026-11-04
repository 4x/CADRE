"""Compile explicit dependencies, evaluate once per node, and preserve run evidence."""

import ast
import hashlib
import json
import logging
import math
import platform
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from graphlib import CycleError, TopologicalSorter
from pathlib import Path
from typing import Any
from uuid import uuid4

from . import __version__
from .contracts import (
    DIMENSION_AXES,
    MEANINGS,
    NUMERICAL_BASIS,
    UNITS,
    VOCABULARY_PROFILE,
    Composition,
    Family,
    LLMStep,
    Model,
    ModelError,
    Node,
    Port,
    Reference,
    Value,
    encode_dimensions,
    finite,
    unit_json,
)
from .expressions import check_guard, dimensions, evaluate, guard_dimensions, parse
from .serialization import model_digest
from .solving import SolveError, node_ports, solve, solve_all

MAX_GRAPH_NODES = 64
MAX_MODEL_INPUTS = 16
MAX_LLM_STEPS = 3
LOGGER = logging.getLogger(__name__)

StepCompute = Callable[[LLMStep, dict[str, Value]], tuple[float, str]]
# Step adapter: compute one bounded step from resolved input values, returning
# the computed amount with a short working note. Execution validates
# finiteness and port compatibility around every call.


@dataclass(frozen=True)
class CompiledNode:
    """A validated instance with its parsed model payload."""

    node: Node
    model: Model
    expression: ast.AST
    guards: tuple[ast.Compare, ...]
    inputs: dict[str, Port]
    output: Port
    families: dict[str, Family]


@dataclass(frozen=True)
class CompiledStep:
    """A validated in-context calculation with declared input ports."""

    step: LLMStep


def validate_model(model: Model) -> tuple[ast.AST, tuple[ast.Compare, ...]]:
    """Check a complete model's executable interface without granting admission."""
    if (
        not model.source
        or not model.assumptions
        or len(model.inputs) + len(model.families) > MAX_MODEL_INPUTS
    ):
        raise ModelError(
            "Model needs source, assumptions and a bounded input interface."
        )
    for port in (*model.inputs.values(), model.output):
        port.validate()
    for family in model.families.values():
        family.validate()
    if set(model.inputs) & set(model.families):
        raise ModelError("Scalar inputs and families must not share a name.")
    names = {name: UNITS[port.unit].dimensions for name, port in model.inputs.items()}
    family_dims = {
        name: UNITS[family.unit].dimensions for name, family in model.families.items()
    }
    expression = parse(model.expression)
    if (
        dimensions(expression, names, family_dims)
        != UNITS[model.output.unit].dimensions
    ):
        raise ModelError("Expression/output dimensions differ.")
    guards = tuple(
        guard_dimensions(parse(guard), names, family_dims) for guard in model.guards
    )
    return expression, guards


def compile_graph(
    composition: Composition,
    catalog: dict[str, Model],
    admissions: dict[str, dict[str, Any]] | None = None,
) -> tuple[CompiledNode | CompiledStep, ...]:
    """Validate the complete graph before executing it in dependency order."""
    if composition.purpose not in {"fixture", "scenario"}:
        raise ModelError(
            "Only fixture evaluation and conditional scenarios are supported."
        )
    if not 0 < len(composition.nodes) <= MAX_GRAPH_NODES:
        raise ModelError(f"Graph must have 1–{MAX_GRAPH_NODES} nodes.")
    nodes = {node.id: node for node in composition.nodes}
    if len(nodes) != len(composition.nodes) or any(not name for name in nodes):
        raise ModelError("Node instance IDs must be nonempty and unique.")
    steps = {step.id: step for step in composition.llm_steps}
    if len(steps) != len(composition.llm_steps) or any(not name for name in steps):
        raise ModelError("LLM-computed step IDs must be nonempty and unique.")
    if set(nodes) & set(steps):
        raise ModelError("Node and step IDs must be unique across the graph.")
    if len(steps) > MAX_LLM_STEPS:
        raise ModelError(f"Graphs take at most {MAX_LLM_STEPS} LLM-computed steps.")
    if len(nodes) + len(steps) > MAX_GRAPH_NODES:
        raise ModelError(f"Graph must have 1–{MAX_GRAPH_NODES} nodes and steps.")
    entries = {**nodes, **steps}
    if not composition.outputs or any(
        name not in entries for name in composition.outputs
    ):
        raise ModelError("Requested outputs must refer to existing node instances.")
    compiled: dict[str, CompiledNode | CompiledStep] = {}
    dependencies: dict[str, set[str]] = {}
    for node in composition.nodes:
        if node.model not in catalog:
            raise ModelError(f"{node.id}: model revision {node.model} is missing.")
        model = catalog[node.model]
        if node.model != model.key or not model.source or not model.assumptions:
            raise ModelError(
                f"{node.id}: model identity/source/assumptions are incomplete."
            )
        if composition.purpose == "scenario":
            admission = (admissions or {}).get(model.key, {})
            if model.status != "eligible" or admission.get("digest") != model_digest(
                model
            ):
                raise ModelError(
                    f"{node.id}: model lacks a matching reviewed registry admission."
                )
        elif model.status != "fixture":
            raise ModelError("Fixture runs require fixture definitions.")
        inputs, output = node_ports(node, model)
        if len(inputs) + len(model.families) > MAX_MODEL_INPUTS + 1 or set(
            node.bindings
        ) != set(inputs) | set(model.families):
            raise ModelError(f"{node.id}: missing/extra inputs or too many inputs.")
        expression, guards = validate_model(model)
        dependencies[node.id] = set()

        def check_element(element: Value | Reference, target: Port, label: str) -> None:
            """Apply the scalar upstream/origin/compatibility checks to one element."""
            if isinstance(element, Reference):
                if element.node not in entries:
                    raise ModelError(f"{label}: unknown upstream node {element.node}.")
                source = nodes.get(element.node)
                if source is None:
                    upstream_output = steps[element.node].output
                else:
                    if source.branch == "all":
                        raise ModelError(
                            f"{label}: branch 'all' outputs are terminal and cannot feed another node."
                        )
                    upstream = catalog.get(source.model)
                    if upstream is None:
                        raise ModelError(f"Missing upstream model for {element.node}.")
                    _, upstream_output = node_ports(source, upstream)
                upstream_output.require_compatible(target)
                dependencies[node.id].add(element.node)
            elif isinstance(element, Value):
                if composition.purpose == "scenario" and element.origin in {
                    "fixture",
                    "generated",
                    "derived",
                }:
                    raise ModelError(
                        "Scenario inputs must be sourced observations or explicit user scenarios; generated estimates need owner consent."
                    )
                element.bind(target)
            else:
                raise ModelError(f"{label}: unsupported binding type.")

        for name, binding in node.bindings.items():
            if isinstance(binding, tuple):
                family = model.families.get(name)
                if family is None:
                    raise ModelError(
                        f"{node.id}.{name}: only a declared family takes a tuple binding."
                    )
                if not 1 <= len(binding) <= family.max_size:
                    raise ModelError(
                        f"{node.id}.{name}: family needs 1 to {family.max_size} elements."
                    )
                for index, element in enumerate(binding):
                    check_element(element, family.port, f"{node.id}.{name}[{index}]")
            elif name in model.families:
                raise ModelError(
                    f"{node.id}.{name}: a family needs a tuple binding, not one value."
                )
            else:
                check_element(binding, inputs[name], f"{node.id}.{name}")
        compiled[node.id] = CompiledNode(
            node, model, expression, guards, inputs, output, model.families
        )
    for step in composition.llm_steps:
        step.validate()
        dependencies[step.id] = set()
        for name, binding in step.bindings.items():
            target = step.inputs[name]
            label = f"{step.id}.{name}"
            if isinstance(binding, Reference):
                if binding.node not in entries:
                    raise ModelError(f"{label}: unknown upstream node {binding.node}.")
                source = nodes.get(binding.node)
                if source is None:
                    upstream_output = steps[binding.node].output
                else:
                    if source.branch == "all":
                        raise ModelError(
                            f"{label}: branch 'all' outputs are terminal and cannot feed another node."
                        )
                    upstream = catalog.get(source.model)
                    if upstream is None:
                        raise ModelError(f"Missing upstream model for {binding.node}.")
                    _, upstream_output = node_ports(source, upstream)
                upstream_output.require_compatible(target)
                dependencies[step.id].add(binding.node)
            elif isinstance(binding, Value):
                if composition.purpose == "scenario" and binding.origin in {
                    "fixture",
                    "generated",
                    "derived",
                }:
                    raise ModelError(
                        "Scenario inputs must be sourced observations or explicit user scenarios; generated estimates need owner consent."
                    )
                binding.bind(target)
            else:
                raise ModelError(f"{label}: unsupported binding type.")
        compiled[step.id] = CompiledStep(step)
    try:
        order = tuple(TopologicalSorter(dependencies).static_order())
    except CycleError as exc:
        raise ModelError(
            "Dependency cycle detected; feedback solvers are not supported."
        ) from exc
    return tuple(compiled[name] for name in order)


def execute(
    composition: Composition,
    catalog: dict[str, Model],
    admissions: dict[str, dict[str, Any]] | None = None,
    llm: StepCompute | None = None,
    llm_values: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Return a self-contained successful or rejected run, without mutating definitions.

    The llm adapter computes bounded steps the catalog cannot cover; pass
    recorded amounts in llm_values to replay them without re-querying. A
    graph with steps but neither adapter nor recorded values is rejected.
    """
    definitions = {
        key: asdict(catalog[key])
        for key in sorted({node.model for node in composition.nodes})
        if key in catalog
    }
    snapshot = json.dumps(definitions, sort_keys=True, allow_nan=False)
    manifest: dict[str, Any] = {
        "run_id": str(uuid4()),
        "created": datetime.now(UTC).isoformat(),
        "engine": f"connected-models/{__version__}",
        "python": platform.python_version(),
        "composition": asdict(composition),
        "models": definitions,
        "model_snapshot_sha256": hashlib.sha256(snapshot.encode()).hexdigest(),
        "admissions": admissions or {},
        "vocabulary": {
            "profile": VOCABULARY_PROFILE,
            "dimension_axes": DIMENSION_AXES,
            "numerical_basis": NUMERICAL_BASIS,
            "units": {name: unit_json(unit) for name, unit in UNITS.items()},
            "meanings": {
                name: encode_dimensions(dims) for name, dims in MEANINGS.items()
            },
        },
        "status": "rejected",
        "steps": [],
        "outputs": {},
        "grounding": "full",
        "llm_steps": [],
        "limitations": [
            "Fixture execution."
            if composition.purpose == "fixture"
            else "Conditional scenario; no empirical validation of the supplied case.",
            "Input uncertainty is not propagated; scenario assumptions are conditional.",
        ],
    }
    try:
        plan = compile_graph(composition, catalog, admissions)
        values: dict[str, Value] = {}
        reliance: dict[str, list[dict[str, Any]]] = {}
        envelopes: dict[str, dict[str, Any]] = {}
        for compiled in plan:
            if isinstance(compiled, CompiledStep):
                step = compiled.step
                step_numbers: dict[str, float] = {}
                step_origins: list[dict[str, Any]] = []
                input_values: dict[str, Value] = {}
                for input_name, step_binding in step.bindings.items():
                    target = step.inputs[input_name]
                    step_value = (
                        values[step_binding.node]
                        if isinstance(step_binding, Reference)
                        else step_binding
                    )
                    input_values[input_name] = step_value
                    step_numbers[input_name] = finite(
                        step_value.bind(target) * UNITS[target.unit].scale,
                        "Normalized input",
                    )
                    if isinstance(step_binding, Reference):
                        step_origins.extend(reliance[step_binding.node])
                        if values[step_binding.node].origin == "llm-computed":
                            step_origins.append(
                                {
                                    "node": step_binding.node,
                                    "input": input_name,
                                    **asdict(values[step_binding.node]),
                                }
                            )
                    else:
                        step_origins.append(
                            {
                                "node": step.id,
                                "input": input_name,
                                **asdict(step_value),
                            }
                        )
                carried = llm_values or {}
                if step.id in carried:
                    amount = finite(carried[step.id], f"Carried LLM-computed {step.id}")
                    working, from_cache = "", True
                    evidence = (
                        f"Carried recorded LLM-computed value for {step.id}; "
                        "not re-queried."
                    )
                else:
                    if llm is None:
                        total = len(composition.llm_steps)
                        raise ModelError(
                            f"{step.id}: composition needs {total} LLM-computed "
                            "step(s); set CADRE_ALLOW_LLM_STEPS=1 to allow them."
                        )
                    raw_amount, working = llm(step, input_values)
                    amount = finite(raw_amount, f"LLM-computed {step.id}")
                    working = str(working or "")[:4000]
                    from_cache = False
                    evidence = f"LLM-computed {step.id}: {working}"
                step_value = Value(amount, step.output, "llm-computed", evidence)
                step_value.bind(step.output)
                values[step.id], reliance[step.id] = step_value, step_origins
                manifest["steps"].append(
                    {
                        "node": step.id,
                        "model": "llm-computed",
                        "llm_step": True,
                        "instruction": step.instruction,
                        "normalized_inputs": step_numbers,
                        "result": asdict(step_value),
                        "relies_on": step_origins,
                        "llm": {"working": working, "carried": from_cache},
                    }
                )
                manifest["llm_steps"].append(
                    {
                        "id": step.id,
                        "instruction": step.instruction,
                        "carried": from_cache,
                    }
                )
                continue
            node, model = compiled.node, compiled.model
            numbers: dict[str, float] = {}
            family_numbers: dict[str, tuple[float, ...]] = {}
            origins: list[dict[str, Any]] = []
            for name, binding in node.bindings.items():
                if isinstance(binding, tuple):
                    elements = []
                    for index, element in enumerate(binding):
                        value = (
                            values[element.node]
                            if isinstance(element, Reference)
                            else element
                        )
                        port = compiled.families[name].port
                        elements.append(
                            finite(
                                value.bind(port) * UNITS[port.unit].scale,
                                "Normalized family element",
                            )
                        )
                        if isinstance(element, Reference):
                            origins.extend(reliance[element.node])
                            if values[element.node].origin == "llm-computed":
                                origins.append(
                                    {
                                        "node": element.node,
                                        "input": name,
                                        "element": index,
                                        **asdict(values[element.node]),
                                    }
                                )
                        else:
                            origins.append(
                                {
                                    "node": node.id,
                                    "input": name,
                                    "element": index,
                                    **asdict(value),
                                }
                            )
                    family_numbers[name] = tuple(elements)
                    continue
                value = (
                    values[binding.node] if isinstance(binding, Reference) else binding
                )
                numbers[name] = finite(
                    value.bind(compiled.inputs[name])
                    * UNITS[compiled.inputs[name].unit].scale,
                    "Normalized input",
                )
                if isinstance(binding, Reference):
                    origins.extend(reliance[binding.node])
                    if values[binding.node].origin == "llm-computed":
                        origins.append(
                            {
                                "node": binding.node,
                                "input": name,
                                **asdict(values[binding.node]),
                            }
                        )
                else:
                    origins.append({"node": node.id, "input": name, **asdict(value)})
            solve_evidence = None
            if node.solve_for is not None and node.branch == "all":
                roots, solve_evidence = solve_all(
                    model,
                    compiled.expression,
                    compiled.guards,
                    node.solve_for,
                    numbers,
                    node.relation,
                )
                scale = UNITS[compiled.output.unit].scale
                envelope = {
                    "amounts": [
                        finite(amount / scale, "Output") for amount in roots["amounts"]
                    ],
                    "excluded": [
                        finite(amount / scale, "Output") for amount in roots["excluded"]
                    ],
                    "port": asdict(compiled.output),
                    "origin": "derived",
                    "source": f"{manifest['run_id']}/{node.id}",
                    "branch": "all",
                }
                envelopes[node.id], reliance[node.id] = envelope, origins
                manifest["steps"].append(
                    {
                        "node": node.id,
                        "model": model.key,
                        "normalized_inputs": numbers,
                        "normalized_family_inputs": {
                            name: list(values)
                            for name, values in family_numbers.items()
                        },
                        "result": envelope,
                        "relies_on": origins,
                        "solve": solve_evidence,
                    }
                )
                continue
            if node.solve_for is not None:
                canonical_result, solve_evidence = solve(
                    model,
                    compiled.expression,
                    compiled.guards,
                    node.solve_for,
                    numbers,
                    node.relation,
                )
            else:
                for guard_text, guard in zip(
                    model.guards, compiled.guards, strict=True
                ):
                    if not check_guard(guard, numbers, family_numbers):
                        raise ModelError(
                            f"{node.id}: domain condition failed: {guard_text}."
                        )
                canonical_result = evaluate(
                    compiled.expression, numbers, family_numbers
                )
            result = finite(
                canonical_result / UNITS[compiled.output.unit].scale, "Output"
            )
            value = Value(
                result, compiled.output, "derived", f"{manifest['run_id']}/{node.id}"
            )
            value.bind(compiled.output)
            values[node.id], reliance[node.id] = value, origins
            manifest["steps"].append(
                {
                    "node": node.id,
                    "model": model.key,
                    "normalized_inputs": numbers,
                    "normalized_family_inputs": {
                        name: list(values) for name, values in family_numbers.items()
                    },
                    "result": asdict(value),
                    "relies_on": origins,
                    "solve": solve_evidence,
                }
            )
        manifest["outputs"] = {
            name: envelopes[name] if name in envelopes else asdict(values[name])
            for name in composition.outputs
        }
        for name in composition.outputs:
            if name in values and values[name].origin == "llm-computed":
                manifest["grounding"] = "partial"
                break
            if any(
                entry.get("origin") == "llm-computed"
                for entry in reliance.get(name, ())
            ):
                manifest["grounding"] = "partial"
                break
        manifest["status"] = "completed"
        LOGGER.info(f"Completed run {manifest['run_id']} with {len(plan)} nodes")
    except ModelError as exc:
        manifest["error"] = str(exc)
        if isinstance(exc, SolveError):
            manifest["solve_diagnostic"] = exc.diagnostic
        LOGGER.warning(f"Rejected run {manifest['run_id']}: {exc}")
    return manifest


def save_run(manifest: dict[str, Any], directory: Path) -> Path:
    """Write a new run manifest exclusively, preserving old run files."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{manifest['run_id']}.json"

    # Invalid numeric inputs must remain inspectable as strings in rejection evidence.
    def safe(value: Any) -> Any:
        """Make rejection evidence valid JSON without hiding invalid numbers."""
        if isinstance(value, float) and not math.isfinite(value):
            return repr(value)
        if isinstance(value, dict):
            return {key: safe(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [safe(item) for item in value]
        return value

    serialized = json.dumps(safe(manifest), indent=2, allow_nan=False)
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(serialized + "\n")
    except OSError:
        LOGGER.exception(f"Could not save run {manifest['run_id']} in {directory}")
        raise
    return path
