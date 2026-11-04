"""Compile explicit dependencies, evaluate once per node, and preserve run evidence."""

import ast
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from graphlib import CycleError, TopologicalSorter
import hashlib
import json
import logging
import math
from pathlib import Path
import platform
from typing import Any
from uuid import uuid4

from . import __version__
from .contracts import (Composition, DIMENSION_AXES, Family, MEANINGS, NUMERICAL_BASIS, Model, ModelError,
                        Node, Port, Reference, UNITS, VOCABULARY_PROFILE, Value, encode_dimensions, finite, unit_json)
from .expressions import check_guard, dimensions, evaluate, guard_dimensions, parse
from .serialization import model_digest
from .solving import SolveError, node_ports, solve, solve_all

MAX_GRAPH_NODES = 64
MAX_MODEL_INPUTS = 16
LOGGER = logging.getLogger(__name__)


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


def validate_model(model: Model) -> tuple[ast.AST, tuple[ast.Compare, ...]]:
    """Check a complete model's executable interface without granting admission."""
    if not model.source or not model.assumptions or len(model.inputs) + len(model.families) > MAX_MODEL_INPUTS:
        raise ModelError("Model needs source, assumptions and a bounded input interface.")
    for port in (*model.inputs.values(), model.output):
        port.validate()
    for family in model.families.values():
        family.validate()
    if set(model.inputs) & set(model.families):
        raise ModelError("Scalar inputs and families must not share a name.")
    names = {name: UNITS[port.unit].dimensions for name, port in model.inputs.items()}
    family_dims = {name: UNITS[family.unit].dimensions for name, family in model.families.items()}
    expression = parse(model.expression)
    if dimensions(expression, names, family_dims) != UNITS[model.output.unit].dimensions:
        raise ModelError("Expression/output dimensions differ.")
    guards = tuple(parse(guard) for guard in model.guards)
    for guard in guards:
        guard_dimensions(guard, names, family_dims)
    return expression, guards


def compile_graph(composition: Composition, catalog: dict[str, Model],
                  admissions: dict[str, dict[str, Any]] | None = None) -> tuple[CompiledNode, ...]:
    """Validate the complete graph before executing it in dependency order."""
    if composition.purpose not in {"fixture", "scenario"}:
        raise ModelError("Only fixture evaluation and conditional scenarios are supported.")
    if not 0 < len(composition.nodes) <= MAX_GRAPH_NODES:
        raise ModelError(f"Graph must have 1–{MAX_GRAPH_NODES} nodes.")
    nodes = {node.id: node for node in composition.nodes}
    if len(nodes) != len(composition.nodes) or any(not name for name in nodes):
        raise ModelError("Node instance IDs must be nonempty and unique.")
    if not composition.outputs or any(name not in nodes for name in composition.outputs):
        raise ModelError("Requested outputs must refer to existing node instances.")
    compiled: dict[str, CompiledNode] = {}
    dependencies: dict[str, set[str]] = {}
    for node in composition.nodes:
        if node.model not in catalog:
            raise ModelError(f"{node.id}: model revision {node.model} is missing.")
        model = catalog[node.model]
        if node.model != model.key or not model.source or not model.assumptions:
            raise ModelError(f"{node.id}: model identity/source/assumptions are incomplete.")
        if composition.purpose == "scenario":
            admission = (admissions or {}).get(model.key, {})
            if model.status != "eligible" or admission.get("digest") != model_digest(model):
                raise ModelError(f"{node.id}: model lacks a matching reviewed registry admission.")
        elif model.status != "fixture":
            raise ModelError("Fixture runs require fixture definitions.")
        inputs, output = node_ports(node, model)
        if len(inputs) + len(model.families) > MAX_MODEL_INPUTS + 1 or set(node.bindings) != set(inputs) | set(model.families):
            raise ModelError(f"{node.id}: missing/extra inputs or too many inputs.")
        expression, guards = validate_model(model)
        dependencies[node.id] = set()

        def check_element(element: Value | Reference, target: Port, label: str) -> None:
            """Apply the scalar upstream/origin/compatibility checks to one element."""
            if isinstance(element, Reference):
                if element.node not in nodes:
                    raise ModelError(f"{label}: unknown upstream node {element.node}.")
                if nodes[element.node].branch == "all":
                    raise ModelError(f"{label}: branch 'all' outputs are terminal and cannot feed another node.")
                upstream = catalog.get(nodes[element.node].model)
                if upstream is None:
                    raise ModelError(f"Missing upstream model for {element.node}.")
                _, upstream_output = node_ports(nodes[element.node], upstream)
                upstream_output.require_compatible(target)
                dependencies[node.id].add(element.node)
            elif isinstance(element, Value):
                if composition.purpose == "scenario" and element.origin in {"fixture", "generated", "derived"}:
                    raise ModelError("Scenario inputs must be sourced observations or explicit user scenarios; generated estimates need owner consent.")
                element.bind(target)
            else:
                raise ModelError(f"{label}: unsupported binding type.")

        for name, binding in node.bindings.items():
            if isinstance(binding, tuple):
                family = model.families.get(name)
                if family is None:
                    raise ModelError(f"{node.id}.{name}: only a declared family takes a tuple binding.")
                if not 1 <= len(binding) <= family.max_size:
                    raise ModelError(f"{node.id}.{name}: family needs 1 to {family.max_size} elements.")
                for index, element in enumerate(binding):
                    check_element(element, family.port, f"{node.id}.{name}[{index}]")
            elif name in model.families:
                raise ModelError(f"{node.id}.{name}: a family needs a tuple binding, not one value.")
            else:
                check_element(binding, inputs[name], f"{node.id}.{name}")
        compiled[node.id] = CompiledNode(node, model, expression, guards, inputs, output, model.families)
    try:
        order = tuple(TopologicalSorter(dependencies).static_order())
    except CycleError as exc:
        raise ModelError("Dependency cycle detected; feedback solvers are not supported.") from exc
    return tuple(compiled[name] for name in order)


def execute(composition: Composition, catalog: dict[str, Model],
            admissions: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Return a self-contained successful or rejected run, without mutating definitions."""
    definitions = {key: asdict(catalog[key]) for key in sorted({node.model for node in composition.nodes}) if key in catalog}
    snapshot = json.dumps(definitions, sort_keys=True, allow_nan=False)
    manifest: dict[str, Any] = {
        "run_id": str(uuid4()), "created": datetime.now(timezone.utc).isoformat(),
        "engine": f"connected-models/{__version__}", "python": platform.python_version(),
        "composition": asdict(composition), "models": definitions,
        "model_snapshot_sha256": hashlib.sha256(snapshot.encode()).hexdigest(),
        "admissions": admissions or {},
        "vocabulary": {"profile": VOCABULARY_PROFILE, "dimension_axes": DIMENSION_AXES,
                       "numerical_basis": NUMERICAL_BASIS,
                       "units": {name: unit_json(unit) for name, unit in UNITS.items()},
                       "meanings": {name: encode_dimensions(dims) for name, dims in MEANINGS.items()}},
        "status": "rejected", "steps": [], "outputs": {},
        "limitations": ["Fixture execution." if composition.purpose == "fixture" else "Conditional scenario; no empirical validation of the supplied case.",
                        "Input uncertainty is not propagated; scenario assumptions are conditional."],
    }
    try:
        plan = compile_graph(composition, catalog, admissions)
        values: dict[str, Value] = {}
        reliance: dict[str, list[dict[str, Any]]] = {}
        envelopes: dict[str, dict[str, Any]] = {}
        for compiled in plan:
            node, model = compiled.node, compiled.model
            numbers: dict[str, float] = {}
            family_numbers: dict[str, tuple[float, ...]] = {}
            origins: list[dict[str, Any]] = []
            for name, binding in node.bindings.items():
                if isinstance(binding, tuple):
                    elements = []
                    for index, element in enumerate(binding):
                        value = values[element.node] if isinstance(element, Reference) else element
                        port = compiled.families[name].port
                        elements.append(finite(value.bind(port) * UNITS[port.unit].scale, "Normalized family element"))
                        origins.extend(reliance[element.node] if isinstance(element, Reference)
                                       else [{"node": node.id, "input": name, "element": index, **asdict(value)}])
                    family_numbers[name] = tuple(elements)
                    continue
                value = values[binding.node] if isinstance(binding, Reference) else binding
                numbers[name] = finite(value.bind(compiled.inputs[name]) * UNITS[compiled.inputs[name].unit].scale, "Normalized input")
                origins.extend(reliance[binding.node] if isinstance(binding, Reference) else [{"node": node.id, "input": name, **asdict(value)}])
            solve_evidence = None
            if node.solve_for is not None and node.branch == "all":
                roots, solve_evidence = solve_all(model, compiled.expression, compiled.guards, node.solve_for, numbers, node.relation)
                scale = UNITS[compiled.output.unit].scale
                envelope = {"amounts": [finite(amount / scale, "Output") for amount in roots["amounts"]],
                            "excluded": [finite(amount / scale, "Output") for amount in roots["excluded"]],
                            "port": asdict(compiled.output), "origin": "derived",
                            "source": f"{manifest['run_id']}/{node.id}", "branch": "all"}
                envelopes[node.id], reliance[node.id] = envelope, origins
                manifest["steps"].append({"node": node.id, "model": model.key, "normalized_inputs": numbers,
                                          "normalized_family_inputs": {name: list(values) for name, values in family_numbers.items()},
                                          "result": envelope, "relies_on": origins, "solve": solve_evidence})
                continue
            if node.solve_for is not None:
                canonical_result, solve_evidence = solve(model, compiled.expression, compiled.guards, node.solve_for, numbers, node.relation)
            else:
                for guard_text, guard in zip(model.guards, compiled.guards, strict=True):
                    if not check_guard(guard, numbers, family_numbers):
                        raise ModelError(f"{node.id}: domain condition failed: {guard_text}.")
                canonical_result = evaluate(compiled.expression, numbers, family_numbers)
            result = finite(canonical_result / UNITS[compiled.output.unit].scale, "Output")
            value = Value(result, compiled.output, "derived", f"{manifest['run_id']}/{node.id}")
            value.bind(compiled.output)
            values[node.id], reliance[node.id] = value, origins
            manifest["steps"].append({"node": node.id, "model": model.key, "normalized_inputs": numbers,
                                      "normalized_family_inputs": {name: list(values) for name, values in family_numbers.items()},
                                      "result": asdict(value), "relies_on": origins, "solve": solve_evidence})
        manifest["outputs"] = {name: envelopes[name] if name in envelopes else asdict(values[name])
                                for name in composition.outputs}
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
