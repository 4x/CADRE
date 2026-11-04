"""Operator revision of saved runs: change inputs or model revisions, rerun, keep history."""

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from typing import Any

from .contracts import ModelError, finite
from .registry import Registry
from .reports import diff_runs, read_run
from .runtime import execute, save_run
from .serialization import composition_from_dict, model_from_dict

RUNS_PATH = Path(".runs")


def parse_set(spec: str) -> tuple[str, str, float]:
    """Split a node.input=amount revision; the amount uses the declared port unit."""
    target, equals, raw = spec.partition("=")
    node_id, dot, name = target.strip().rpartition(".")
    if not equals or not dot or not node_id.strip() or not name.strip():
        raise ModelError(
            f"Invalid --set {spec!r}; use node.input=amount, e.g. upgrade-energy.performance=2."
        )
    try:
        amount = float(raw.strip())
    except ValueError:
        raise ModelError(
            f"Invalid --set {spec!r}; the amount must be a finite number."
        ) from None
    return node_id.strip(), name.strip(), finite(amount, "Revised input")


def parse_model(spec: str) -> tuple[str, str]:
    """Split a node=model@version substitution request."""
    node_id, equals, key = spec.partition("=")
    if not equals or not node_id.strip() or not key.strip():
        raise ModelError(
            f"Invalid --model {spec!r}; use node=model@version, e.g. upgrade-energy=heat-to-electricity@2."
        )
    return node_id.strip(), key.strip()


def revise_run(
    parent_id: str,
    sets: list[str],
    models: list[str],
    registry: Registry | None = None,
    directory: Path = RUNS_PATH,
) -> dict[str, Any]:
    """Rerun a saved graph with revised inputs and/or model revisions; preserve the parent run.

    Scenario runs re-execute against the registry's current eligible snapshot, so
    --model selects among reviewed revisions. Fixture runs reuse the models pinned
    in the parent manifest. Unchanged bindings keep their original provenance; each
    --set value is recorded as an explicit operator scenario revision.
    """
    if not sets and not models:
        raise ModelError(
            "Nothing to revise; provide --set node.input=amount and/or --model node=model@version."
        )
    parent = read_run(parent_id, directory)
    composition_data = parent.get("composition")
    if not isinstance(composition_data, dict) or not composition_data.get("nodes"):
        raise ModelError(
            "That run has no executable graph (it may need clarification); ask a new question instead of revising it."
        )
    purpose = composition_data.get("purpose")
    if purpose == "scenario":
        if registry is None:
            raise ModelError("Scenario revision needs the model registry.")
        catalog, admissions = registry.snapshot()
    elif purpose == "fixture":
        catalog = {
            key: replace(model_from_dict(data), status="fixture")
            for key, data in parent.get("models", {}).items()
        }
        admissions = {}
    else:
        raise ModelError(
            "That run predates supported revision; rerun it from its question instead."
        )
    pristine = {node["id"]: node for node in composition_data["nodes"]}
    data = deepcopy(composition_data)
    nodes = {node["id"]: node for node in data["nodes"]}
    applied_models: dict[str, dict[str, str]] = {}
    for spec in models:
        node_id, key = parse_model(spec)
        if node_id not in nodes:
            raise ModelError(
                f"Unknown node {node_id!r}; this run has: {', '.join(sorted(nodes))}."
            )
        if key not in catalog:
            raise ModelError(
                f"Unknown model revision {key!r}; available: {', '.join(sorted(catalog)) or 'none'}."
            )
        applied_models[node_id] = {"old": pristine[node_id]["model"], "new": key}
        nodes[node_id]["model"] = key
    applied_sets: dict[str, dict[str, Any]] = {}
    for spec in sets:
        node_id, name, amount = parse_set(spec)
        if node_id not in nodes:
            raise ModelError(
                f"Unknown node {node_id!r}; this run has: {', '.join(sorted(nodes))}."
            )
        model = catalog.get(nodes[node_id]["model"])
        if model is None:
            raise ModelError(
                f"{node_id} uses {nodes[node_id]['model']}, which is no longer available; "
                f"select a current revision with --model {node_id}=model@version."
            )
        if name not in model.inputs:
            raise ModelError(
                f"{node_id} has no input {name!r}; {model.key} declares: {', '.join(sorted(model.inputs))}."
            )
        binding = nodes[node_id]["bindings"].get(name)
        if binding is None:
            raise ModelError(
                f"{node_id}.{name} has no binding in this run; only recorded inputs can be revised."
            )
        if "amount" not in binding:
            raise ModelError(
                f"{node_id}.{name} is calculated from {binding.get('node')}; only direct inputs can be revised."
            )
        port = model.inputs[name]
        nodes[node_id]["bindings"][name] = {
            "amount": amount,
            "port": {
                "meaning": port.meaning,
                "unit": port.unit,
                "context": port.context,
            },
            "origin": "user-scenario",
            "evidence": f"Operator revision of run {parent['run_id']}: set {node_id}.{name}",
        }
        applied_sets[f"{node_id}.{name}"] = {"amount": amount, "unit": port.unit}
    graph = composition_from_dict(data)
    if purpose == "fixture":
        graph = replace(graph, purpose="fixture")
    manifest = execute(graph, catalog, admissions)
    manifest["revised_from"] = parent["run_id"]
    manifest["revision"] = {"sets": applied_sets, "models": applied_models}
    if parent.get("question"):
        manifest["question"] = parent["question"]
    path = save_run(manifest, directory)
    manifest["diff"] = diff_runs(parent, manifest)
    return {**manifest, "saved_path": str(path)}


def replay_run(run_id: str, directory: Path = RUNS_PATH) -> dict[str, Any]:
    """Re-execute a saved graph against its pinned models and compare; saves nothing.

    Unlike revision, replay uses the models and admissions recorded in the run
    manifest rather than the registry's current snapshot, so it verifies exact
    deterministic reproduction of that run's own evidence.
    """
    parent = read_run(run_id, directory)
    composition_data = parent.get("composition")
    if not isinstance(composition_data, dict) or not composition_data.get("nodes"):
        raise ModelError("That run has no executable graph to replay.")
    purpose = composition_data.get("purpose")
    if purpose == "scenario":
        catalog = {
            key: replace(model_from_dict(data), status="eligible")
            for key, data in parent.get("models", {}).items()
        }
        admissions = parent.get("admissions", {})
    elif purpose == "fixture":
        catalog = {
            key: replace(model_from_dict(data), status="fixture")
            for key, data in parent.get("models", {}).items()
        }
        admissions = {}
    else:
        raise ModelError("That run predates supported replay.")
    graph = composition_from_dict(composition_data)
    if purpose == "fixture":
        graph = replace(graph, purpose="fixture")
    repeated = execute(graph, catalog, admissions)
    old_outputs, new_outputs = (
        parent.get("outputs", {}) or {},
        repeated.get("outputs", {}) or {},
    )
    mismatches = sorted(set(old_outputs) ^ set(new_outputs))
    for name in set(old_outputs) & set(new_outputs):
        before, after = old_outputs[name], new_outputs[name]
        if before.get("amount") != after.get("amount") or before.get(
            "port"
        ) != after.get("port"):
            mismatches.append(name)
    status_match = parent.get("status") == repeated.get("status")
    error_match = parent.get("error") == repeated.get("error")
    matched = status_match and error_match and not mismatches
    return {
        "run_id": parent["run_id"],
        "replayed": True,
        "matched": matched,
        "status": {
            "recorded": parent.get("status"),
            "repeated": repeated.get("status"),
        },
        "error_match": error_match,
        "output_mismatches": sorted(mismatches),
        "outputs": repeated.get("outputs", {}),
    }
