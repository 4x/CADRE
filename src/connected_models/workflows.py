"""Offline extraction and query-time composition consume separate persisted artifacts."""

import json
import os
import time
from dataclasses import asdict, replace
from datetime import UTC, datetime
from importlib.resources import files
from pathlib import Path
from typing import Any
from uuid import uuid4

from .compatibility import audit_pairs
from .contracts import Composition, Model, ModelError, Node, Value
from .demo import catalog
from .inference import BudgetLedger, InferenceSettings, load_prompt, structured_request
from .query_inputs import MAX_QUERY_CHARS, MAX_QUERY_FACTS, bind_fact, validate_fact
from .registry import Registry
from .retrieval import FALLBACK_CAP, FALLBACK_K, RETRIEVAL_CAP, RETRIEVAL_VERSION, SEED_K, build_index, neighbors_from_audit, retrieve
from .runtime import execute, save_run
from .serialization import (
    MAX_RECORD_BYTES,
    composition_from_dict,
    model_from_dict,
    object_fields,
    text,
)
from .solving import OUTPUT_BINDING, PROFILE, node_ports

REGISTRY_PATH = Path(".registry/models.sqlite3")
RUNS_PATH = Path(".runs")
PACKET_FILENAME = "nist-uniform-present-value.json"
REFERENCE_TOLERANCE = 0.005
FILL_IN_ENV_VAR = "FILL_IN_ASSUMPTIONS"
FILL_IN_TRUTHY = {"1", "true", "yes", "on"}
BASE_PROMPT_FILE = "answer-question.md"
FILL_IN_PROMPT_FILE = "answer-fill-in-assumptions.md"
REPAIR_PROMPT_FILE = "answer-repair.md"
MAX_COMPOSE_ATTEMPTS = 3


def fill_in_assumptions_enabled(
    cli_flag: bool, environ: dict[str, str] | None = None
) -> bool:
    """Resolve the assumption-filling opt-in from the CLI flag or the environment toggle."""
    if cli_flag:
        return True
    values = environ if environ is not None else os.environ
    return str(values.get(FILL_IN_ENV_VAR, "")).strip().lower() in FILL_IN_TRUTHY


def compose_system_prompt(fill_in_assumptions: bool) -> str:
    """Build the composer system prompt, appending the fill-in section only when enabled."""
    prompt = load_prompt(BASE_PROMPT_FILE)
    if fill_in_assumptions:
        prompt += "\n\n" + load_prompt(FILL_IN_PROMPT_FILE)
    return prompt


def live_request(
    messages: list[dict[str, str]],
    schema: dict[str, Any],
    name: str,
    inference_model: str | None = None,
) -> dict[str, Any]:
    """Use the same priced adapter and ledger across curator and composer roles."""
    settings = InferenceSettings.load(Path("inference.toml"), inference_model)
    return structured_request(
        settings,
        BudgetLedger(Path(".usage/meta.sqlite3"), settings),
        messages,
        schema,
        name,
    )


def load_packet() -> dict[str, Any]:
    """Load the bundled public source packet; no other file is loadable."""
    resource = files("connected_models").joinpath("data").joinpath(PACKET_FILENAME)
    try:
        raw = resource.read_bytes()
    except OSError as exc:
        raise ModelError("Bundled source packet is not readable.") from exc
    if len(raw) > MAX_RECORD_BYTES:
        raise ModelError("Source packet exceeds the supported size.")
    packet: dict[str, Any] = json.loads(raw)
    object_fields(packet, {"source", "location", "text", "profile", "reference"})
    return packet


def reference_check(
    model_data: dict[str, Any], reference: dict[str, Any]
) -> dict[str, Any]:
    """Compare extracted algebra with independent source/reference evidence before admission."""
    model = replace(model_from_dict(model_data), status="fixture")
    if set(reference["inputs"]) != set(model.inputs):
        raise ModelError("Reference inputs do not match the extracted interface.")
    node = Node(
        "reference",
        model.key,
        {
            name: Value(
                amount,
                model.inputs[name],
                "fixture",
                "Independent published or arithmetic reference",
            )
            for name, amount in reference["inputs"].items()
        },
    )
    result = execute(
        Composition("candidate-reference", (node,), (node.id,)), {model.key: model}
    )
    actual = result["outputs"].get(node.id, {}).get("amount")
    return {
        "reference": reference,
        "actual": actual,
        "passed": result["status"] == "completed"
        and abs(actual - reference["expected"])
        <= reference.get("tolerance", REFERENCE_TOLERANCE),
        "error": result.get("error"),
    }


def curate(registry: Registry) -> str:
    """Extract one source relationship offline and retain it as an unapproved candidate."""
    packet = load_packet()
    schema = {
        "type": "object",
        "properties": {
            "expression": {"type": "string"},
            "guards": {"type": "array", "items": {"type": "string"}},
            "assumptions": {"type": "array", "items": {"type": "string"}},
            "source_map": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string"},
                        "source_symbol": {"type": "string"},
                        "location": {"type": "string"},
                    },
                    "required": ["symbol", "source_symbol", "location"],
                    "additionalProperties": False,
                },
            },
            "unresolved": {"type": "array", "items": {"type": "string"}},
            "limitations": {"type": "array", "items": {"type": "string"}},
        },
        "required": [
            "expression",
            "guards",
            "assumptions",
            "source_map",
            "unresolved",
            "limitations",
        ],
        "additionalProperties": False,
    }
    response = live_request(
        [
            {"role": "system", "content": load_prompt("offline-model-extraction.md")},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        key: packet[key]
                        for key in ("source", "location", "text", "profile")
                    }
                ),
            },
        ],
        schema,
        "OfflineModelExtraction",
    )
    extracted = response["content"]
    evidence = {
        "packet": packet,
        "extraction": extracted,
        "inference": response["audit"],
    }
    model = {
        **packet["profile"],
        "source": packet["source"],
        "expression": extracted.get("expression"),
        "guards": extracted.get("guards"),
        "assumptions": extracted.get("assumptions"),
    }
    checks: list[dict[str, Any]] = []
    try:
        object_fields(
            extracted,
            {
                "expression",
                "guards",
                "assumptions",
                "source_map",
                "unresolved",
                "limitations",
            },
        )
        if not isinstance(extracted["limitations"], list) or not isinstance(
            extracted["assumptions"], list
        ):
            raise ModelError("Assumptions and limitations must be arrays.")
        model["assumptions"] = [
            *extracted["assumptions"],
            *(f"Limitation: {text(item)}" for item in extracted["limitations"]),
        ]
        if extracted["unresolved"]:
            raise ModelError(
                "Extraction has unresolved ambiguities; retained for review, not execution."
            )
        expected_symbols = set(packet["profile"]["inputs"]) | {"output"}
        mappings = extracted["source_map"]
        if (
            not isinstance(mappings, list)
            or {item["symbol"] for item in mappings} != expected_symbols
        ):
            raise ModelError("Source map must cover every input and the output.")
        for item in mappings:
            object_fields(item, {"symbol", "source_symbol", "location"})
            text(item["source_symbol"])
            if item["location"] != packet["location"]:
                raise ModelError(
                    "Extraction source-map location differs from the supplied source."
                )
        checks.append(reference_check(model, packet["reference"]))
    except (ModelError, KeyError, TypeError, ValueError) as exc:
        checks.append(
            {
                "passed": False,
                "error": f"Candidate check failed: {type(exc).__name__}: {exc}",
            }
        )
    return registry.propose({"model": model, "evidence": evidence, "checks": checks})


def seed_candidates(registry: Registry) -> list[str]:
    """Stage project-derived supporting definitions; never claim agent extraction for them."""
    references = {
        "heat-to-electricity": {
            "inputs": {"heat": 120, "performance": 3},
            "expected": 40,
        },
        "electricity-cost": {"inputs": {"energy": 20, "tariff": 0.25}, "expected": 5},
        "annual-saving": {"inputs": {"baseline": 20, "alternative": 5}, "expected": 15},
        "net-present-value": {
            "inputs": {"benefit": 20, "investment": 5},
            "expected": 15,
        },
    }
    candidate_ids = []
    for model in catalog().values():
        if model.id not in references:
            continue  # The present-value relationship must come from offline source extraction.
        data = json.loads(json.dumps(asdict(model)))
        candidate_ids.append(
            registry.propose(
                {
                    "model": data,
                    "evidence": {
                        "kind": "manual-project-derivation",
                        "source": model.source,
                        "notes": "Review the stated assumptions and declared heating use. This is not an agent-curated model.",
                    },
                    "checks": [reference_check(data, references[model.id])],
                }
            )
        )
    return candidate_ids


def catalog_card(model: Model) -> dict[str, Any]:
    """Project one eligible model to its composition signal: ports, guards, assumptions.

    Identity, version, status, source, and expression stay in the database:
    the key already pins the sole eligible revision, sources are never looked
    up at query time, and the expression is the engine's to execute, not the
    composer's to read. Guards and families ride only when non-empty."""
    data = asdict(model)
    card: dict[str, Any] = {
        "inputs": data["inputs"],
        "output": data["output"],
        "assumptions": data["assumptions"],
    }
    if data["guards"]:
        card["guards"] = data["guards"]
    if data.get("families"):
        card["families"] = data["families"]
    return card


class _TerminalAnswer(ModelError):
    """A decline needing a human; never repaired by another attempt."""


def _reset_attempt(record: dict[str, Any]) -> None:
    """Clear per-attempt state so a repair round starts from the question."""
    record.update(
        {"status": "blocked", "outputs": {}, "clarifications": [], "assumptions": []}
    )
    for key in ("error", "query_inputs", "input_bindings", "proposal", "inference"):
        record.pop(key, None)


def answer(
    registry: Registry,
    question: str,
    fill_in_assumptions: bool = False,
    inference_model: str | None = None,
    retrieval: str = "subset",
    retrieval_k: int = SEED_K,
    retrieval_cap: int = RETRIEVAL_CAP,
) -> dict[str, Any]:
    """Answer a self-contained question, repairing machine-rejected proposals.

    The composer gets up to MAX_COMPOSE_ATTEMPTS calls: the first attempt
    sees the base prompt, and each retry sees the repair prompt plus the
    prior proposal and its exact machine error. Declines that need a human
    (ambiguity, needs-input, unresolved) stop the loop immediately.
    Execution stays deterministic; only the proposal is revised."""
    record: dict[str, Any] = {
        "run_id": str(uuid4()),
        "created": datetime.now(UTC).isoformat(),
        "question": question,
        "status": "blocked",
        "outputs": {},
        "clarifications": [],
        "fill_in_assumptions": bool(fill_in_assumptions),
        "assumptions": [],
        "attempts": [],
    }
    try:
        text(question)
        if len(question) > MAX_QUERY_CHARS:
            raise ModelError("Question exceeds the supported length.")
        models, admissions = registry.snapshot()
        if not models:
            raise ModelError(
                "No eligible models in the registry match an executable request yet."
            )
        fact_properties: dict[str, dict[str, Any]] = {
            name: {"type": "string"}
            for name in ("id", "name", "value", "unit", "quote")
        }
        fact_properties["value_type"] = {
            "type": "string",
            "enum": ["number", "date", "text"],
        }
        fact_properties["assumption"] = {"type": "string"}
        graph_schema = {"type": "object", "properties": {
            "id": {"type": "string"}, "outputs": {"type": "array", "items": {"type": "string"}},
            "nodes": {"type": "array", "items": {"type": "object", "properties": {
                "id": {"type": "string"}, "model": {"type": "string"},
                "solve_for": {"type": "string"}, "relation": {"type": "string", "enum": ["equal", "at_least"]},
                "branch": {"type": "string", "enum": ["all"]},
                "bindings": {"type": "array", "items": {"type": "object", "properties": {
                    "input": {"type": "string"}, "source": {"type": "string", "enum": ["node", "fact"]},
                    "ref": {"type": "string"}}, "required": ["input", "source", "ref"], "additionalProperties": False}}},
                "required": ["id", "model", "bindings"], "additionalProperties": False}}},
            "required": ["id", "nodes", "outputs"], "additionalProperties": False}
        schema = {"type": "object", "properties": {
            "facts": {"type": "array", "items": {"type": "object", "properties": fact_properties,
                        "required": [name for name in fact_properties if name != "assumption"],
                        "additionalProperties": False}},
            "issues": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string", "enum": ["proposed", "needs-input", "unresolved"]},
            "graph": graph_schema, "reason": {"type": "string"},
            "clarifications": {"type": "array", "items": {"type": "string"}}},
            "required": ["facts", "issues", "status", "graph", "reason", "clarifications"], "additionalProperties": False}
        retrieval_log: dict[str, Any] = {"mode": retrieval, "version": RETRIEVAL_VERSION}
        subset = dict(models)
        retrieval_index = None
        retrieval_neighbors = None
        if retrieval == "subset":
            retrieval_started = time.perf_counter()
            retrieval_index = build_index(models)
            retrieval_neighbors = neighbors_from_audit(audit_pairs(models))
            shortlist = retrieve(question, retrieval_index, retrieval_neighbors,
                                 k=retrieval_k, cap=retrieval_cap)
            subset = {key: models[key] for key in shortlist.keys}
            retrieval_log.update({"k": retrieval_k, "cap": retrieval_cap, "retrieved": len(subset),
                                  "build_ms": round((time.perf_counter() - retrieval_started) * 1000.0, 1),
                                  "seeds": list(shortlist.seeds), "expanded": list(shortlist.expanded),
                                  "dropped": list(shortlist.dropped)})
        elif retrieval != "full":
            raise ModelError("Retrieval mode must be 'full' or 'subset'.")
        record["retrieval"] = retrieval_log
        base_user_content = {"question": question, "solver_profile": PROFILE,
                             "models": {key: catalog_card(model) for key, model in subset.items()}}
        base_system = compose_system_prompt(fill_in_assumptions)
        prior: tuple[Any, str] | None = None
        for attempt in range(1, MAX_COMPOSE_ATTEMPTS + 1):
            _reset_attempt(record)
            if prior is None:
                messages = [
                    {"role": "system", "content": base_system},
                    {"role": "user", "content": json.dumps(base_user_content)},
                ]
            else:
                try:
                    repair_system = (
                        base_system + "\n\n" + load_prompt(REPAIR_PROMPT_FILE)
                    )
                except ModelError:
                    break  # Keep the last attempt's error; repair is unavailable.
                repair_models = base_user_content["models"]
                if retrieval == "subset" and retrieval_index is not None and retrieval_neighbors is not None:
                    wide = retrieve(question, retrieval_index, retrieval_neighbors,
                                    k=FALLBACK_K, cap=FALLBACK_CAP)
                    repair_models = {key: catalog_card(models[key]) for key in wide.keys}
                    retrieval_log["repair"] = {"k": FALLBACK_K, "cap": FALLBACK_CAP,
                                               "retrieved": len(repair_models)}
                repair_user = {"question": question, "solver_profile": PROFILE, "models": repair_models,
                               "prior_proposal": prior[0], "machine_error": prior[1]}
                messages = [{"role": "system", "content": repair_system},
                            {"role": "user", "content": json.dumps(repair_user)}]
            try:
                response = live_request(
                    messages, schema, "AnswerQuestionGrounded", inference_model
                )
                proposal = response["content"]
                record["proposal"], record["inference"] = proposal, response["audit"]
                object_fields(
                    proposal,
                    {"facts", "issues", "status", "graph", "reason", "clarifications"},
                )
                if (
                    not isinstance(proposal["facts"], list)
                    or len(proposal["facts"]) > MAX_QUERY_FACTS
                    or not isinstance(proposal["issues"], list)
                ):
                    raise ModelError("Answer returned invalid facts or issues.")
                facts = [
                    validate_fact(raw, question, fill_in_assumptions)
                    for raw in proposal["facts"]
                ]
                if len({fact["id"] for fact in facts}) != len(facts):
                    raise ModelError("Parsed fact identifiers must be unique.")
                record["query_inputs"] = {
                    "facts": facts,
                    "issues": [text(issue) for issue in proposal["issues"]],
                    "inference": response["audit"],
                }
                if record["query_inputs"]["issues"]:
                    record["status"] = "needs-input"
                    record["clarifications"] = record["query_inputs"]["issues"]
                    raise _TerminalAnswer(
                        "Please clarify the conflicting or ambiguous statements in the question."
                    )
                if not isinstance(proposal["clarifications"], list):
                    raise ModelError("Clarifications must be an array.")
                record["clarifications"] = [
                    text(item) for item in proposal["clarifications"]
                ]
                if proposal["status"] != "proposed":
                    record["status"] = (
                        "needs-input"
                        if proposal["status"] == "needs-input"
                        else "blocked"
                    )
                    raise _TerminalAnswer(text(proposal["reason"]))
                if record["clarifications"]:
                    record["status"] = "needs-input"
                    raise _TerminalAnswer(
                        "The proposed graph still has unresolved input questions."
                    )
                raw_graph = json.dumps(proposal["graph"])
                if len(raw_graph.encode()) > MAX_RECORD_BYTES:
                    raise ModelError("Proposed graph exceeds size limit.")
                graph_data = json.loads(raw_graph)
                object_fields(graph_data, {"id", "nodes", "outputs"})
                if not isinstance(graph_data["nodes"], list):
                    raise ModelError("Proposed graph nodes must be an array.")
                facts_by_id = {
                    fact["id"]: fact for fact in record["query_inputs"]["facts"]
                }
                grounded = []
                for node in graph_data["nodes"]:
                    object_fields(
                        node, {"id", "model", "bindings"}, {"solve_for", "relation", "branch"}
                    )
                    if node["model"] not in models or not isinstance(
                        node["bindings"], list
                    ):
                        raise ModelError(
                            "Proposed node requires an eligible model revision and explicit bindings."
                        )
                    model = models[node["model"]]
                    target = node.get("solve_for") or None
                    node["solve_for"] = target
                    direction = Node(
                        node["id"], model.key, {}, target, node.get("relation", "equal")
                    )
                    inputs, _ = node_ports(direction, model)
                    bindings = {}
                    for binding in node["bindings"]:
                        object_fields(binding, {"input", "source", "ref"})
                        name = text(binding["input"])
                        ref = text(binding["ref"])
                        if name in bindings:
                            raise ModelError(
                                "Composer repeated a binding for the same input."
                            )
                        if name not in inputs:
                            raise ModelError(
                                "Proposed binding targets an undeclared input."
                            )
                        if binding["source"] == "node":
                            bindings[name] = {"node": ref}
                            continue
                        if binding["source"] != "fact":
                            raise ModelError(
                                "Composer must bind a query fact or an upstream node, not a literal."
                            )
                        fact_id = ref
                        if fact_id not in facts_by_id:
                            raise ModelError(
                                "Composer referenced an unknown query fact; defaults and invented inputs are forbidden."
                            )
                        value = bind_fact(facts_by_id[fact_id], inputs[name])
                        bindings[name] = asdict(value)
                        grounded.append(
                            {
                                "node": node["id"],
                                "input": name,
                                "fact": fact_id,
                                "assigned_port": asdict(inputs[name]),
                                "value": asdict(value),
                                "role": "requested-output-target"
                                if name == OUTPUT_BINDING
                                else "known-input",
                            }
                        )
                        if facts_by_id[fact_id].get("assumed"):
                            record["assumptions"].append(
                                {
                                    "node": node["id"],
                                    "input": name,
                                    "fact": fact_id,
                                    "value": facts_by_id[fact_id]["value"],
                                    "unit": facts_by_id[fact_id]["unit"],
                                    "quote": facts_by_id[fact_id]["quote"],
                                    "assumption": facts_by_id[fact_id]["assumption"],
                                }
                            )
                    node["bindings"] = bindings
                record["input_bindings"] = grounded
                graph = composition_from_dict(graph_data)
                outcome = execute(graph, models, admissions)
            except _TerminalAnswer as exc:
                record["error"] = str(exc)
                record["attempts"].append(
                    {
                        "attempt": attempt,
                        "proposal": record.get("proposal"),
                        "error": str(exc),
                        "inference": record.get("inference"),
                    }
                )
                if attempt == 1 or attempt >= MAX_COMPOSE_ATTEMPTS:
                    break
                # The question is unchanged since the last proposal, so a
                # late ambiguity claim is composer confusion until it repeats.
                prior = (record.get("proposal"), str(exc))
                continue
            except (ModelError, ValueError, TypeError, KeyError) as exc:
                record["error"] = str(exc)
                record["attempts"].append(
                    {
                        "attempt": attempt,
                        "proposal": record.get("proposal"),
                        "error": str(exc),
                        "inference": record.get("inference"),
                    }
                )
                if attempt >= MAX_COMPOSE_ATTEMPTS:
                    break
                prior = (record.get("proposal"), str(exc))
                continue
            if outcome["status"] == "completed":
                record.update(outcome)
                record["attempts"].append(
                    {
                        "attempt": attempt,
                        "proposal": record.get("proposal"),
                        "error": None,
                        "inference": record.get("inference"),
                    }
                )
                break
            error = outcome.get("error") or "Execution rejected the proposed graph."
            record["attempts"].append(
                {
                    "attempt": attempt,
                    "proposal": record.get("proposal"),
                    "error": error,
                    "inference": record.get("inference"),
                }
            )
            if attempt >= MAX_COMPOSE_ATTEMPTS:
                record.update(outcome)
                break
            record["error"] = error
            prior = (record.get("proposal"), error)
    except (ModelError, ValueError, TypeError, KeyError) as exc:
        record["error"] = str(exc)
    used = [
        (attempt.get("inference") or {}).get("model") for attempt in record["attempts"]
    ]
    record["model"] = next((name for name in reversed(used) if name), None)
    path = save_run(record, RUNS_PATH)
    return {**record, "saved_path": str(path)}


def review_bundle(registry: Registry) -> Path:
    """Create a human-readable derivative of stored candidates without approving any."""
    lines = [
        "# Candidate review bundle",
        "",
        "No candidate is approved by creating this report.",
        "",
    ]
    for candidate in registry.candidates():
        model = candidate.get("model") or {}
        evidence = candidate.get("evidence")
        if (
            not model
            and isinstance(evidence, dict)
            and isinstance(evidence.get("record"), dict)
        ):
            research = evidence["record"]
            model = {
                "id": research.get("id"),
                "version": research.get("revision"),
                "expression": research.get("relationship", {}).get("expression"),
                "source": "Research-only curation record; see source evidence below",
                "assumptions": research.get("assumptions", []),
            }
        lines.extend(
            [
                f"## {model.get('id', 'partial')} @ {model.get('version', 'unresolved')}",
                "",
                f"Candidate: {candidate['id']}",
                "",
                f"Expression: `{model.get('expression', 'unresolved')}`",
                "",
                f"Source: {model.get('source', 'unresolved')}",
                "",
                "### Assumptions",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in model.get("assumptions", []))
        lines.extend(
            [
                "",
                "### Checks and diagnostics",
                "",
                "```json",
                json.dumps(
                    {
                        "checks": candidate.get("checks"),
                        "diagnostics": candidate["diagnostics"],
                    },
                    indent=2,
                ),
                "```",
                "",
                "### Source and extraction evidence",
                "",
                "```json",
                json.dumps(candidate.get("evidence"), indent=2),
                "```",
                "",
                "Inspect full ports with the candidate command.",
                "",
            ]
        )
        if candidate["diagnostics"]:
            lines.extend(
                [
                    "This candidate has blockers. Resolve them in a new candidate revision before admission.",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    "After checking source fidelity, applicability and semantics, record an attributed review:",
                    "",
                    "```powershell",
                    f"uv run --no-env-file connected-models review {candidate['id']} --decision accepted --reviewer owner --notes 'Describe the checked scope and evidence here'",
                    "```",
                    "",
                ]
            )
    RUNS_PATH.mkdir(parents=True, exist_ok=True)
    path = RUNS_PATH / f"review-{uuid4()}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
