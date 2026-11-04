"""Natural-language what-if exploration over a saved run.

Meta proposes named scenarios as input revisions; the deterministic engine
validates and executes each one. Proposed figures are never trusted: every
scenario runs through revise_run, so accepted scenarios carry executed
engine outputs and rejected ones carry the exact machine error.
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from .contracts import ModelError
from .inference import load_prompt
from .registry import Registry
from .reports import read_run, value_bindings
from .revisions import revise_run
from .runtime import save_run
from .serialization import object_fields, text
from .workflows import live_request

RUNS_PATH = Path(".runs")
SCENARIO_PROMPT_FILE = "answer-scenarios.md"
MAX_REQUEST_CHARS = 2000
MAX_SCENARIOS = 5
MAX_SETS_PER_SCENARIO = 8
MAX_NAME_CHARS = 80
MAX_RATIONALE_CHARS = 500
MAX_SET_CHARS = 120


def describe_revisable_inputs(parent: dict[str, Any]) -> list[dict[str, Any]]:
    """Project a saved run to the direct inputs a scenario may revise."""
    entries = []
    for (node_id, name), binding in sorted(value_bindings(parent).items()):
        port = binding.get("port", {})
        if not isinstance(port, dict):
            port = {}
        entries.append(
            {
                "node": node_id,
                "input": name,
                "unit": port.get("unit", "?"),
                "meaning": port.get("meaning", "?"),
                "current_amount": binding.get("amount"),
            }
        )
    return entries


def _scenario_schema(max_scenarios: int) -> dict[str, Any]:
    """Build the strict proposal schema, capped at the requested count."""
    return {
        "type": "object",
        "properties": {
            "scenarios": {
                "type": "array",
                "minItems": 1,
                "maxItems": max_scenarios,
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "rationale": {"type": "string"},
                        "sets": {
                            "type": "array",
                            "maxItems": MAX_SETS_PER_SCENARIO,
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["name", "rationale", "sets"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["scenarios"],
        "additionalProperties": False,
    }


def _validate_proposal(proposal: Any, max_scenarios: int) -> list[dict[str, Any]]:
    """Require a bounded list of named scenarios with bounded set strings."""
    if not isinstance(proposal, dict):
        raise ModelError("Scenario proposal must be an object.")
    object_fields(proposal, {"scenarios"})
    scenarios = proposal["scenarios"]
    if (
        not isinstance(scenarios, list)
        or not scenarios
        or len(scenarios) > max_scenarios
    ):
        raise ModelError(f"Scenario proposal must list 1 to {max_scenarios} scenarios.")
    validated = []
    for raw in scenarios:
        object_fields(raw, {"name", "rationale", "sets"})
        name = text(raw["name"])
        rationale = text(raw["rationale"])
        sets = raw["sets"]
        if len(name) > MAX_NAME_CHARS:
            raise ModelError("Scenario name exceeds the supported length.")
        if len(rationale) > MAX_RATIONALE_CHARS:
            raise ModelError("Scenario rationale exceeds the supported length.")
        if not isinstance(sets, list) or len(sets) > MAX_SETS_PER_SCENARIO:
            raise ModelError(
                f"Each scenario may revise at most {MAX_SETS_PER_SCENARIO} inputs."
            )
        cleaned_sets = []
        for item in sets:
            cleaned = text(item)
            if len(cleaned) > MAX_SET_CHARS:
                raise ModelError("Scenario revision exceeds the supported length.")
            cleaned_sets.append(cleaned)
        validated.append({"name": name, "rationale": rationale, "sets": cleaned_sets})
    return validated


def _output_summary(outputs: Any) -> dict[str, dict[str, Any]]:
    """Project executed outputs to amounts and units for the diff table."""
    summary: dict[str, dict[str, Any]] = {}
    if not isinstance(outputs, dict):
        return summary
    for node_id, value in outputs.items():
        if not isinstance(value, dict):
            continue
        port = value.get("port", {})
        if not isinstance(port, dict):
            port = {}
        summary[str(node_id)] = {
            "amount": value.get("amount"),
            "unit": port.get("unit", "?"),
        }
    return summary


def explore(
    registry: Registry,
    run_id: str,
    request: str,
    inference_model: str | None = None,
    max_scenarios: int = 3,
    directory: Path = RUNS_PATH,
) -> dict[str, Any]:
    """Propose named what-if scenarios via Meta and execute each deterministically.

    The model sees only the request plus the parent run's revisable inputs
    and executed outputs; it never computes results. Each proposal runs
    through revise_run, so machine validation (unknown nodes, undeclared
    inputs, calculated bindings, guard failures) decides accepted versus
    rejected per scenario. The exploration record preserves the parent id,
    the request, the validated proposal, the inference audit, and every
    per-scenario outcome with its own saved run.
    """
    if type(max_scenarios) is not int or not 1 <= max_scenarios <= MAX_SCENARIOS:
        raise ModelError(f"Scenario count must be between 1 and {MAX_SCENARIOS}.")
    cleaned = text(request).strip()
    if not cleaned:
        raise ModelError("A scenario request must name what to vary.")
    if len(cleaned) > MAX_REQUEST_CHARS:
        raise ModelError("Scenario request exceeds the supported length.")
    parent = read_run(run_id, directory)
    if parent.get("status") != "completed":
        raise ModelError("Scenarios need a completed run; clarify or rerun it first.")
    nodes = (parent.get("composition") or {}).get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ModelError("That run has no executable graph to vary.")
    revisable = describe_revisable_inputs(parent)
    if not revisable:
        raise ModelError("That run has no direct inputs to vary.")
    response = live_request(
        [
            {"role": "system", "content": load_prompt(SCENARIO_PROMPT_FILE)},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "request": cleaned,
                        "max_scenarios": max_scenarios,
                        "run": {
                            "run_id": parent.get("run_id"),
                            "question": parent.get("question", ""),
                            "revisable_inputs": revisable,
                            "outputs": _output_summary(parent.get("outputs")),
                        },
                    }
                ),
            },
        ],
        _scenario_schema(max_scenarios),
        "ProposeScenarios",
        inference_model,
    )
    proposals = _validate_proposal(response["content"], max_scenarios)
    results = []
    for proposal in proposals:
        sets = [item for item in proposal["sets"] if item.strip()]
        if not sets:
            results.append(
                {
                    "name": proposal["name"],
                    "rationale": proposal["rationale"],
                    "sets": [],
                    "verdict": "rejected",
                    "error": f"Proposed no input changes: {proposal['rationale']}",
                }
            )
            continue
        try:
            revised = revise_run(run_id, sets, [], registry, directory)
        except (ModelError, ValueError, TypeError, KeyError, OSError) as exc:
            results.append(
                {
                    "name": proposal["name"],
                    "rationale": proposal["rationale"],
                    "sets": sets,
                    "verdict": "rejected",
                    "error": str(exc),
                }
            )
            continue
        results.append(
            {
                "name": proposal["name"],
                "rationale": proposal["rationale"],
                "sets": sets,
                "verdict": "accepted",
                "run_id": revised.get("run_id"),
                "saved_path": str(revised.get("saved_path") or ""),
                "outputs": _output_summary(revised.get("outputs")),
                "error": None,
            }
        )
    accepted = sum(1 for item in results if item["verdict"] == "accepted")
    record: dict[str, Any] = {
        "run_id": str(uuid4()),
        "created": datetime.now(UTC).isoformat(),
        "parent_run_id": parent.get("run_id"),
        "request": cleaned,
        "max_scenarios": max_scenarios,
        "proposal": proposals,
        "inference": response["audit"],
        "results": results,
        "accepted": accepted,
        "rejected": len(results) - accepted,
    }
    path = save_run(record, directory)
    return {**record, "saved_path": str(path)}
