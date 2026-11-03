"""Offline extraction and query-time composition consume separate persisted artifacts."""

from dataclasses import asdict, replace
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from .contracts import Composition, Model, ModelError, Node, Value
from .demo import catalog
from .inference import BudgetLedger, InferenceSettings, load_prompt, structured_request
from .registry import Registry
from .runtime import execute, save_run
from .query_inputs import MAX_QUERY_CHARS, MAX_QUERY_FACTS, bind_fact, validate_fact
from .solving import OUTPUT_BINDING, PROFILE, node_ports
from .serialization import MAX_RECORD_BYTES, composition_from_dict, model_from_dict, object_fields, text

REGISTRY_PATH = Path(".registry/models.sqlite3")
RUNS_PATH = Path(".runs")
PACKET_PATH = Path("data/nist-uniform-present-value.json")
REFERENCE_TOLERANCE = 0.005


def live_request(messages: list[dict[str, str]], schema: dict[str, Any], name: str) -> dict[str, Any]:
    """Use the same priced adapter and ledger across curator and composer roles."""
    settings = InferenceSettings.load(Path("inference.toml"))
    return structured_request(settings, BudgetLedger(Path(".usage/meta.sqlite3"), settings), messages, schema, name)


def load_packet(path: Path) -> dict[str, Any]:
    """Load an explicit public source packet; never discover credential files."""
    # Only the fixed first-source packet is enabled in the initial curator command.
    if path.resolve() != PACKET_PATH.resolve():
        raise ModelError("Only the bundled public NIST source packet is enabled for this milestone.")
    raw = path.read_bytes()
    if len(raw) > MAX_RECORD_BYTES:
        raise ModelError("Source packet exceeds the supported size.")
    packet = json.loads(raw)
    object_fields(packet, {"source", "location", "text", "profile", "reference"})
    return packet


def reference_check(model_data: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    """Compare extracted algebra with independent source/reference evidence before admission."""
    model = replace(model_from_dict(model_data), status="fixture")
    if set(reference["inputs"]) != set(model.inputs):
        raise ModelError("Reference inputs do not match the extracted interface.")
    node = Node("reference", model.key, {name: Value(amount, model.inputs[name], "fixture", "Independent published or arithmetic reference")
                                        for name, amount in reference["inputs"].items()})
    result = execute(Composition("candidate-reference", (node,), (node.id,)), {model.key: model})
    actual = result["outputs"].get(node.id, {}).get("amount")
    return {"reference": reference, "actual": actual, "passed": result["status"] == "completed" and
            abs(actual - reference["expected"]) <= reference.get("tolerance", REFERENCE_TOLERANCE),
            "error": result.get("error")}


def curate(registry: Registry) -> str:
    """Extract one source relationship offline and retain it as an unapproved candidate."""
    packet = load_packet(PACKET_PATH)
    schema = {"type": "object", "properties": {
        "expression": {"type": "string"}, "guards": {"type": "array", "items": {"type": "string"}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "source_map": {"type": "array", "items": {"type": "object", "properties": {
            "symbol": {"type": "string"}, "source_symbol": {"type": "string"}, "location": {"type": "string"}},
            "required": ["symbol", "source_symbol", "location"], "additionalProperties": False}},
        "unresolved": {"type": "array", "items": {"type": "string"}},
        "limitations": {"type": "array", "items": {"type": "string"}}},
        "required": ["expression", "guards", "assumptions", "source_map", "unresolved", "limitations"], "additionalProperties": False}
    response = live_request([
        {"role": "system", "content": load_prompt("offline-model-extraction.md")},
        {"role": "user", "content": json.dumps({key: packet[key] for key in ("source", "location", "text", "profile")})}], schema, "OfflineModelExtraction")
    extracted = response["content"]
    evidence = {"packet": packet, "extraction": extracted, "inference": response["audit"]}
    model = {**packet["profile"], "source": packet["source"],
             "expression": extracted.get("expression"), "guards": extracted.get("guards"),
             "assumptions": extracted.get("assumptions")}
    checks: list[dict[str, Any]] = []
    try:
        object_fields(extracted, {"expression", "guards", "assumptions", "source_map", "unresolved", "limitations"})
        if not isinstance(extracted["limitations"], list) or not isinstance(extracted["assumptions"], list):
            raise ModelError("Assumptions and limitations must be arrays.")
        model["assumptions"] = [*extracted["assumptions"], *(f"Limitation: {text(item)}" for item in extracted["limitations"])]
        if extracted["unresolved"]:
            raise ModelError("Extraction has unresolved ambiguities; retained for review, not execution.")
        expected_symbols = set(packet["profile"]["inputs"]) | {"output"}
        mappings = extracted["source_map"]
        if not isinstance(mappings, list) or {item["symbol"] for item in mappings} != expected_symbols:
            raise ModelError("Source map must cover every input and the output.")
        for item in mappings:
            object_fields(item, {"symbol", "source_symbol", "location"})
            text(item["source_symbol"])
            if item["location"] != packet["location"]:
                raise ModelError("Extraction source-map location differs from the supplied source.")
        checks.append(reference_check(model, packet["reference"]))
    except (ModelError, KeyError, TypeError, ValueError) as exc:
        checks.append({"passed": False, "error": f"Candidate check failed: {type(exc).__name__}: {exc}"})
    return registry.propose({"model": model, "evidence": evidence, "checks": checks})


def seed_candidates(registry: Registry) -> list[str]:
    """Stage project-derived supporting definitions; never claim agent extraction for them."""
    references = {
        "heat-to-electricity": {"inputs": {"heat": 120, "performance": 3}, "expected": 40},
        "electricity-cost": {"inputs": {"energy": 20, "tariff": 0.25}, "expected": 5},
        "annual-saving": {"inputs": {"baseline": 20, "alternative": 5}, "expected": 15},
        "net-present-value": {"inputs": {"benefit": 20, "investment": 5}, "expected": 15},
    }
    candidate_ids = []
    for model in catalog().values():
        if model.id not in references:
            continue  # The present-value relationship must come from offline source extraction.
        data = json.loads(json.dumps(asdict(model)))
        candidate_ids.append(registry.propose({"model": data, "evidence": {
            "kind": "manual-project-derivation", "source": model.source,
            "notes": "Review the stated assumptions and declared heating use. This is not an agent-curated model."},
            "checks": [reference_check(data, references[model.id])]}))
    return candidate_ids


def catalog_card(model: Model) -> dict[str, Any]:
    """Project one eligible model to its composition signal: ports, guards, assumptions.

    Identity, version, status, source, and expression stay in the database:
    the key already pins the sole eligible revision, sources are never looked
    up at query time, and the expression is the engine's to execute, not the
    composer's to read. Guards and families ride only when non-empty."""
    data = asdict(model)
    card: dict[str, Any] = {"inputs": data["inputs"], "output": data["output"], "assumptions": data["assumptions"]}
    if data["guards"]:
        card["guards"] = data["guards"]
    if data.get("families"):
        card["families"] = data["families"]
    return card


def answer(registry: Registry, question: str) -> dict[str, Any]:
    """Answer a self-contained question with one parse-and-compose call, then execute."""
    record: dict[str, Any] = {"run_id": str(uuid4()), "created": datetime.now(timezone.utc).isoformat(),
        "question": question, "status": "blocked", "outputs": {}, "clarifications": []}
    try:
        text(question)
        if len(question) > MAX_QUERY_CHARS:
            raise ModelError("Question exceeds the supported length.")
        models, admissions = registry.snapshot()
        if not models:
            raise ModelError("No eligible models in the registry match an executable request yet.")
        fact_properties = {name: {"type": "string"} for name in ("id", "name", "value", "unit", "quote")}
        fact_properties["value_type"] = {"type": "string", "enum": ["number", "date", "text"]}
        graph_schema = {"type": "object", "properties": {
            "id": {"type": "string"}, "outputs": {"type": "array", "items": {"type": "string"}},
            "nodes": {"type": "array", "items": {"type": "object", "properties": {
                "id": {"type": "string"}, "model": {"type": "string"},
                "solve_for": {"type": "string"}, "relation": {"type": "string", "enum": ["equal", "at_least"]},
                "bindings": {"type": "array", "items": {"type": "object", "properties": {
                    "input": {"type": "string"}, "source": {"type": "string", "enum": ["node", "fact"]},
                    "ref": {"type": "string"}}, "required": ["input", "source", "ref"], "additionalProperties": False}}},
                "required": ["id", "model", "bindings"], "additionalProperties": False}}},
            "required": ["id", "nodes", "outputs"], "additionalProperties": False}
        schema = {"type": "object", "properties": {
            "facts": {"type": "array", "items": {"type": "object", "properties": fact_properties,
                        "required": list(fact_properties), "additionalProperties": False}},
            "issues": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string", "enum": ["proposed", "needs-input", "unresolved"]},
            "graph": graph_schema, "reason": {"type": "string"},
            "clarifications": {"type": "array", "items": {"type": "string"}}},
            "required": ["facts", "issues", "status", "graph", "reason", "clarifications"], "additionalProperties": False}
        response = live_request([
            {"role": "system", "content": load_prompt("answer-question.md")},
            {"role": "user", "content": json.dumps({"question": question, "solver_profile": PROFILE,
                "models": {key: catalog_card(model) for key, model in models.items()}})}],
            schema, "AnswerQuestionGrounded")
        proposal = response["content"]
        record["proposal"], record["inference"] = proposal, response["audit"]
        object_fields(proposal, {"facts", "issues", "status", "graph", "reason", "clarifications"})
        if not isinstance(proposal["facts"], list) or len(proposal["facts"]) > MAX_QUERY_FACTS or not isinstance(proposal["issues"], list):
            raise ModelError("Answer returned invalid facts or issues.")
        facts = [validate_fact(raw, question) for raw in proposal["facts"]]
        if len({fact["id"] for fact in facts}) != len(facts):
            raise ModelError("Parsed fact identifiers must be unique.")
        record["query_inputs"] = {"facts": facts, "issues": [text(issue) for issue in proposal["issues"]], "inference": response["audit"]}
        if record["query_inputs"]["issues"]:
            record["status"] = "needs-input"
            record["clarifications"] = record["query_inputs"]["issues"]
            raise ModelError("Please clarify the conflicting or ambiguous statements in the question.")
        if not isinstance(proposal["clarifications"], list):
            raise ModelError("Clarifications must be an array.")
        record["clarifications"] = [text(item) for item in proposal["clarifications"]]
        if proposal["status"] != "proposed":
            record["status"] = "needs-input" if proposal["status"] == "needs-input" else "blocked"
            raise ModelError(text(proposal["reason"]))
        if record["clarifications"]:
            record["status"] = "needs-input"
            raise ModelError("The proposed graph still has unresolved input questions.")
        raw_graph = json.dumps(proposal["graph"])
        if len(raw_graph.encode()) > MAX_RECORD_BYTES:
            raise ModelError("Proposed graph exceeds size limit.")
        graph_data = json.loads(raw_graph)
        object_fields(graph_data, {"id", "nodes", "outputs"})
        if not isinstance(graph_data["nodes"], list):
            raise ModelError("Proposed graph nodes must be an array.")
        facts = {fact["id"]: fact for fact in record["query_inputs"]["facts"]}
        grounded = []
        for node in graph_data["nodes"]:
            object_fields(node, {"id", "model", "bindings"}, {"solve_for", "relation"})
            if node["model"] not in models or not isinstance(node["bindings"], list):
                raise ModelError("Proposed node requires an eligible model revision and explicit bindings.")
            model = models[node["model"]]
            target = node.get("solve_for") or None
            node["solve_for"] = target
            direction = Node(node["id"], model.key, {}, target, node.get("relation", "equal"))
            inputs, _ = node_ports(direction, model)
            bindings = {}
            for binding in node["bindings"]:
                object_fields(binding, {"input", "source", "ref"})
                name = text(binding["input"])
                ref = text(binding["ref"])
                if name in bindings:
                    raise ModelError("Composer repeated a binding for the same input.")
                if name not in inputs:
                    raise ModelError("Proposed binding targets an undeclared input.")
                if binding["source"] == "node":
                    bindings[name] = {"node": ref}
                    continue
                if binding["source"] != "fact":
                    raise ModelError("Composer must bind a query fact or an upstream node, not a literal.")
                fact_id = ref
                if fact_id not in facts:
                    raise ModelError("Composer referenced an unknown query fact; defaults and invented inputs are forbidden.")
                value = bind_fact(facts[fact_id], inputs[name])
                bindings[name] = asdict(value)
                grounded.append({"node": node["id"], "input": name, "fact": fact_id,
                                 "assigned_port": asdict(inputs[name]), "value": asdict(value),
                                 "role": "requested-output-target" if name == OUTPUT_BINDING else "known-input"})
            node["bindings"] = bindings
        record["input_bindings"] = grounded
        graph = composition_from_dict(graph_data)
        record.update(execute(graph, models, admissions))
    except (ModelError, ValueError, TypeError, KeyError) as exc:
        record["error"] = str(exc)
    path = save_run(record, RUNS_PATH)
    return {**record, "saved_path": str(path)}

def review_bundle(registry: Registry) -> Path:
    """Create a human-readable derivative of stored candidates without approving any."""
    lines = ["# Candidate review bundle", "", "No candidate is approved by creating this report.", ""]
    for candidate in registry.candidates():
        model = candidate.get("model") or {}
        evidence = candidate.get("evidence")
        if not model and isinstance(evidence, dict) and isinstance(evidence.get("record"), dict):
            research = evidence["record"]
            model = {"id": research.get("id"), "version": research.get("revision"),
                     "expression": research.get("relationship", {}).get("expression"),
                     "source": "Research-only curation record; see source evidence below",
                     "assumptions": research.get("assumptions", [])}
        lines.extend([f"## {model.get('id', 'partial')} @ {model.get('version', 'unresolved')}", "",
            f"Candidate: {candidate['id']}", "", f"Expression: `{model.get('expression', 'unresolved')}`", "",
            f"Source: {model.get('source', 'unresolved')}", "", "### Assumptions", ""])
        lines.extend(f"- {item}" for item in model.get("assumptions", []))
        lines.extend(["", "### Checks and diagnostics", "", "```json", json.dumps({
            "checks": candidate.get("checks"), "diagnostics": candidate["diagnostics"]}, indent=2), "```", "",
            "### Source and extraction evidence", "", "```json", json.dumps(candidate.get("evidence"), indent=2), "```", "",
            "Inspect full ports with the candidate command.", ""])
        if candidate["diagnostics"]:
            lines.extend(["This candidate has blockers. Resolve them in a new candidate revision before admission.", ""])
        else:
            lines.extend(["After checking source fidelity, applicability and semantics, record an attributed review:", "",
                "```powershell", f"uv --cache-dir .uv-cache run --no-env-file -m connected_models review {candidate['id']} --decision accepted --reviewer owner --notes 'Describe the checked scope and evidence here'", "```", ""])
    RUNS_PATH.mkdir(parents=True, exist_ok=True)
    path = RUNS_PATH / f"review-{uuid4()}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
