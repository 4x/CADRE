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
from .contracts import Composition, MEANINGS, Model, ModelError, Node, Port, Reference, UNITS, Value, finite
from .expressions import check_guard, dimensions, evaluate, guard_dimensions, parse
from .serialization import model_digest
from .solving import SolveError, node_ports, solve

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


def validate_model(model: Model) -> tuple[ast.AST, tuple[ast.Compare, ...]]:
    """Check a complete model's executable interface without granting admission."""
    if not model.source or not model.assumptions or len(model.inputs) > MAX_MODEL_INPUTS:
        raise ModelError("Model needs source, assumptions and a bounded input interface.")
    for port in (*model.inputs.values(), model.output):
        port.validate()
    names = {name: UNITS[port.unit].dimensions for name, port in model.inputs.items()}
    expression = parse(model.expression)
    if dimensions(expression, names) != UNITS[model.output.unit].dimensions:
        raise ModelError("Expression/output dimensions differ.")
    guards = tuple(parse(guard) for guard in model.guards)
    for guard in guards:
        guard_dimensions(guard, names)
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
        if len(inputs) > MAX_MODEL_INPUTS + 1 or set(node.bindings) != set(inputs):
            raise ModelError(f"{node.id}: missing/extra inputs or too many inputs.")
        expression, guards = validate_model(model)
        dependencies[node.id] = set()
        for name, binding in node.bindings.items():
            if isinstance(binding, Reference):
                if binding.node not in nodes:
                    raise ModelError(f"{node.id}.{name}: unknown upstream node {binding.node}.")
                upstream = catalog.get(nodes[binding.node].model)
                if upstream is None:
                    raise ModelError(f"Missing upstream model for {binding.node}.")
                _, upstream_output = node_ports(nodes[binding.node], upstream)
                upstream_output.require_compatible(inputs[name])
                dependencies[node.id].add(binding.node)
            elif isinstance(binding, Value):
                if composition.purpose == "scenario" and binding.origin in {"fixture", "generated", "derived"}:
                    raise ModelError("Scenario inputs must be sourced observations or explicit user scenarios; generated estimates need owner consent.")
                binding.bind(inputs[name])
            else:
                raise ModelError(f"{node.id}.{name}: unsupported binding type.")
        compiled[node.id] = CompiledNode(node, model, expression, guards, inputs, output)
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
        "vocabulary": {"units": {name: asdict(unit) for name, unit in UNITS.items()}, "meanings": MEANINGS},
        "status": "rejected", "steps": [], "outputs": {},
        "limitations": ["Fixture execution." if composition.purpose == "fixture" else "Conditional scenario; no empirical household validation.",
                        "Input uncertainty is not propagated; scenario assumptions are conditional."],
    }
    try:
        plan = compile_graph(composition, catalog, admissions)
        values: dict[str, Value] = {}
        reliance: dict[str, list[dict[str, Any]]] = {}
        for compiled in plan:
            node, model = compiled.node, compiled.model
            numbers: dict[str, float] = {}
            origins: list[dict[str, Any]] = []
            for name, binding in node.bindings.items():
                value = values[binding.node] if isinstance(binding, Reference) else binding
                numbers[name] = finite(value.bind(compiled.inputs[name]) * UNITS[compiled.inputs[name].unit].scale, "Normalized input")
                origins.extend(reliance[binding.node] if isinstance(binding, Reference) else [{"node": node.id, "input": name, **asdict(value)}])
            solve_evidence = None
            if node.solve_for is not None:
                canonical_result, solve_evidence = solve(model, compiled.expression, compiled.guards, node.solve_for, numbers, node.relation)
            else:
                for guard_text, guard in zip(model.guards, compiled.guards, strict=True):
                    if not check_guard(guard, numbers):
                        raise ModelError(f"{node.id}: domain condition failed: {guard_text}.")
                canonical_result = evaluate(compiled.expression, numbers)
            result = finite(canonical_result / UNITS[compiled.output.unit].scale, "Output")
            value = Value(result, compiled.output, "derived", f"{manifest['run_id']}/{node.id}")
            value.bind(compiled.output)
            values[node.id], reliance[node.id] = value, origins
            manifest["steps"].append({"node": node.id, "model": model.key, "normalized_inputs": numbers,
                                      "result": asdict(value), "relies_on": origins, "solve": solve_evidence})
        manifest["outputs"] = {name: asdict(values[name]) for name in composition.outputs}
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
