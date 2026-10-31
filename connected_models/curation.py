"""Portable offline curation kit, bounded data validation, and candidate-only intake."""

import argparse
import ast
from datetime import date
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any
from urllib.parse import urlsplit
import zipfile

from .contracts import DIMENSIONLESS, DIMENSION_AXES, MEANINGS, NUMERICAL_BASIS, UNITS, VOCABULARY_PROFILE, ModelError, NumericalError
from .curation_schema import DOMAINS, KIT_VERSION, MAX_BATCH_BYTES, SCHEMA, SCHEMA_VERSION, SUPPORTED_KIT_VERSIONS, validate_schema
from .expressions import check_guard, dimensions, evaluate, guard_dimensions, parse
from .registry import Registry
from .runtime import validate_model
from .serialization import MAX_RECORD_BYTES, model_from_dict

ASSETS = Path(__file__).resolve().parent.parent / "data" / "curation"
ROOT = ASSETS.parent.parent
AGENT_GUIDE = Path("knowledge/notes/offline-curator-instructions.md")
REGISTRY = Path(".registry/models.sqlite3")
ARCHIVE_MEMBERS = {"bundle.json", "manifest.json"}
MAX_MANIFEST_BYTES = 4096


def encoded(value: Any) -> bytes:
    """Return stable UTF-8 JSON for checksums and idempotent proposal storage."""
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def digest(raw: bytes) -> str:
    """Compute a transfer-integrity checksum, not an authenticity signature."""
    return hashlib.sha256(raw).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys rather than accepting an overwritten declaration."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ModelError(f"Duplicate JSON key: {key}.")
        result[key] = value
    return result


def decode(raw: bytes) -> Any:
    """Read bounded data with duplicate-key and nonstandard-number rejection."""
    if len(raw) > MAX_BATCH_BYTES:
        raise ModelError("Curation data exceeds the one MiB limit.")
    try:
        value = json.loads(raw, object_pairs_hook=unique_object)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ModelError(f"Invalid curation JSON: {exc}") from exc
    return value


def public_path(path: Path, suffixes: set[str]) -> Path:
    """Restrict explicit artifact paths without accessing secret files or links."""
    if path.suffix.lower() not in suffixes or any(part.lower().startswith(".env") for part in path.parts):
        raise ModelError("Use an explicit public JSON/ZIP artifact path.")
    resolved = path.resolve()
    if any(part.lower().startswith(".env") for part in resolved.parts) or path.is_symlink():
        raise ModelError("Secret paths and artifact symlinks are not supported.")
    return path


def load_bundle(path: Path) -> dict[str, Any]:
    """Read JSON or a strictly data-only return archive without extracting files."""
    public_path(path, {".json", ".zip"})
    if path.suffix.lower() == ".json":
        with path.open("rb") as stream:
            return decode(stream.read(MAX_BATCH_BYTES + 1))
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        if len(members) != len(ARCHIVE_MEMBERS) or {item.filename for item in members} != ARCHIVE_MEMBERS:
            raise ModelError("Return ZIP must contain exactly bundle.json and manifest.json.")
        for item in members:
            limit = MAX_BATCH_BYTES if item.filename == "bundle.json" else MAX_MANIFEST_BYTES
            if item.file_size > limit:
                raise ModelError("Return archive member exceeds its size limit.")
        raw = archive.read("bundle.json")
        manifest = decode(archive.read("manifest.json"))
    if (not isinstance(manifest, dict) or set(manifest) != {"kit_version", "sha256"}
            or manifest["kit_version"] not in SUPPORTED_KIT_VERSIONS or manifest["sha256"] != digest(raw)):
        raise ModelError("Return manifest version or checksum mismatch.")
    bundle = decode(raw)
    require(isinstance(bundle, dict) and bundle.get("kit_version") == manifest["kit_version"],
            "Return bundle and manifest kit versions differ.")
    return bundle


def require(condition: bool, message: str) -> None:
    """Raise a useful contract error when a cross-field requirement fails."""
    if not condition:
        raise ModelError(message)


def validate_record(item: dict[str, Any], domain: str) -> dict[str, Any]:
    """Check references and safe scalar arithmetic; scientific unit review is separate."""
    identity = f"{item['id']}@{item['revision']}"
    require(item["id"].startswith(f"{domain}--"), f"{identity}: ID must begin {domain}--.")
    variables = {entry["symbol"]: entry for entry in item["variables"]}
    require(len(variables) == len(item["variables"]), f"{identity}: duplicate variable symbols.")
    outputs = [name for name, entry in variables.items() if entry["role"] == "output"]
    relationship = item["relationship"]
    require(outputs == [relationship["output_symbol"]], f"{identity}: exactly one declared output must match the relationship.")
    inputs = {name: entry for name, entry in variables.items() if entry["role"] == "input"}
    names = {name: DIMENSIONLESS for name in inputs}
    # Here dimensionless tags enable grammar checks only. Units are never rewritten in the record.
    expression = parse(relationship["expression"])
    dimensions(expression, names)
    referenced = {node.id for node in ast.walk(expression) if isinstance(node, ast.Name)}
    require(referenced == set(inputs), f"{identity}: expression must use exactly the declared inputs.")
    guards = [parse(guard) for guard in item["guards"]]
    for guard in guards:
        guard_dimensions(guard, names)
    sources = {source["id"]: source for source in item["sources"]}
    require(len(sources) == len(item["sources"]), f"{identity}: duplicate source IDs.")
    require(relationship["source_id"] in sources, f"{identity}: relationship source is missing.")
    for source in sources.values():
        date.fromisoformat(source["accessed"])
        if source["url"] is not None:
            url = urlsplit(source["url"])
            require(url.scheme in {"http", "https"} and bool(url.netloc) and url.username is None,
                    f"{identity}: sources require public HTTP(S) URLs without credentials.")
        require(source["kind"] != "primary" or source["url"] is not None, f"{identity}: primary source URL is required.")
    for constant in item["constants"]:
        require(constant["source_id"] in sources, f"{identity}: constant source is missing.")
    observed_inputs: set[bytes] = set()
    reference_ids: set[str] = set()
    for case in item["references"]:
        require(case["id"] not in reference_ids, f"{identity}: duplicate reference ID.")
        reference_ids.add(case["id"])
        require(set(case["inputs"]) == set(inputs), f"{identity}: reference input symbols do not match.")
        require(encoded(case["inputs"]) not in observed_inputs, f"{identity}: numerical references must use distinct inputs.")
        observed_inputs.add(encoded(case["inputs"]))
        require(all(check_guard(guard, case["inputs"]) for guard in guards), f"{identity}: reference violates a guard.")
        actual = evaluate(expression, case["inputs"])
        require(abs(actual - case["expected"]) <= case["tolerance"], f"{identity}/{case['id']}: numerical reference does not match ({actual}).")
    for case in item["rejection_cases"]:
        if case["kind"] == "missing-input":
            require(set(case["inputs"]) < set(inputs), f"{identity}: missing-input case must omit a declared input without adding symbols.")
            continue
        require(set(case["inputs"]) == set(inputs), f"{identity}: rejection input symbols do not match.")
        rejected = False
        try:
            rejected = not all(check_guard(guard, case["inputs"]) for guard in guards)
            if not rejected:
                evaluate(expression, case["inputs"])
        except NumericalError:
            raise  # An overflow is not evidence of a scientifically excluded case.
        except ModelError:
            rejected = True
        require(rejected, f"{identity}: rejection case is accepted by its declared guards/expression.")
    integration = item["integration"]
    status = integration["status"]
    require(not item["unresolved"] or status == "blocked", f"{identity}: unresolved interpretation requires blocked status.")
    require(status == "runtime-ready" or bool(integration["gaps"]), f"{identity}: describe the integration blockers.")
    raw = integration["runtime_model"]
    if status == "runtime-ready":
        require(raw is not None and not integration["gaps"], f"{identity}: runtime-ready requires a complete projection and no gaps.")
    if raw is not None:
        model = model_from_dict(raw)
        validate_model(model)
        require(model.key == identity, f"{identity}: runtime identity differs from research record.")
        require(model.expression == relationship["expression"] and list(model.guards) == item["guards"],
                f"{identity}: runtime expression/guards must equal the research record.")
        require(set(model.inputs) == set(inputs), f"{identity}: runtime inputs differ from the research record.")
        for name, port in {**model.inputs, outputs[0]: model.output}.items():
            entry = variables[name]
            require((port.meaning, port.unit, port.context) == (entry["quantity_id"], entry["unit"], entry["context"]),
                    f"{identity}: runtime port {name} differs from the research record.")
        require(set(item["assumptions"] + item["limitations"]) <= set(model.assumptions),
                f"{identity}: runtime assumptions must retain every assumption and limitation.")
        for case in item["references"]:
            require(Registry.verify_reference(model, {"reference": case}), f"{identity}: runtime reference check failed.")
    return {"id": identity, "status": status, "arithmetic_checks": len(item["references"]),
            "rejection_checks": len(item["rejection_cases"]), "runtime_contract_checked": raw is not None,
            "scientific_review": "pending"}


def validate_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Validate every record before any candidate is written."""
    validate_schema(bundle)
    date.fromisoformat(bundle["created"])
    require(len(encoded(bundle)) <= MAX_BATCH_BYTES, "Curation batch exceeds its size limit.")
    identities: set[str] = set()
    checks = []
    for item in bundle["models"]:
        require(item["id"] not in identities, "A batch may contain only one revision per model ID.")
        identities.add(item["id"])
        checks.append(validate_record(item, bundle["domain"]))
    return {"status": "valid-data-awaiting-review", "example_only": bundle["example_only"], "batch_id": bundle["batch_id"],
            "checks": checks, "limits": "Arithmetic and declared runtime contracts checked; source fidelity, physical dimensions of research records, applicability and independent oracle provenance need review."}


def pack_bundle(source: Path, destination: Path) -> dict[str, Any]:
    """Pack only validated JSON and its checksum; never copy an agent directory."""
    bundle = load_bundle(source)
    validate_bundle(bundle)
    public_path(destination, {".zip"})
    raw = encoded(bundle)
    with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("bundle.json", raw)
        archive.writestr("manifest.json", encoded({"kit_version": bundle["kit_version"], "sha256": digest(raw)}))
    return {"path": str(destination), "sha256": digest(raw), "models": len(bundle["models"])}


def import_bundle(source: Path, registry: Registry) -> dict[str, Any]:
    """Stage candidates only; retain blockers and reject conflicting external revisions."""
    bundle = load_bundle(source)
    validation = validate_bundle(bundle)
    require(not bundle["example_only"], "Teaching examples cannot be imported; curate an actual batch.")
    batch_hash = digest(encoded(bundle))
    prepared = []
    existing = registry.candidates()
    for item in bundle["models"]:
        item_hash = digest(encoded(item))
        identity = f"{item['id']}@{item['revision']}"
        for previous in existing:
            intake = previous.get("evidence", {}).get("curation_intake", {}) if isinstance(previous.get("evidence"), dict) else {}
            if intake.get("identity") == identity:
                require(intake.get("record_sha256") == item_hash,
                        f"{identity}: changed content under an existing revision; create a new revision.")
        blockers = list(item["unresolved"]) + list(item["integration"]["gaps"])
        if item["integration"]["status"] != "runtime-ready":
            blockers.insert(0, f"Curation integration status: {item['integration']['status']}.")
        payload = {
            "model": item["integration"]["runtime_model"], "intake_blockers": blockers,
            "evidence": {"curation_intake": {"identity": identity, "record_sha256": item_hash,
                         "schema_version": bundle["schema_version"], "kit_version": bundle["kit_version"],
                         "batch_id": bundle["batch_id"], "batch_sha256": batch_hash, "created": bundle["created"]},
                         "curator": bundle["curator"], "record": item},
            "checks": [{"reference": case} for case in item["references"]],
        }
        # Storage limit includes the repeated runtime projection and all evidence.
        require(len(json.dumps(payload, allow_nan=False).encode()) <= MAX_RECORD_BYTES, f"{identity}: candidate exceeds storage limit.")
        prepared.append(json.loads(encoded(payload)))
    candidates = [{"model": payload["evidence"]["curation_intake"]["identity"], "candidate_id": registry.propose(payload)} for payload in prepared]
    return {"status": "staged-not-published", "batch_id": bundle["batch_id"], "batch_sha256": batch_hash,
            "candidates": candidates, "validation": validation,
            "note": "Retain the returned ZIP and this receipt. Reimport is idempotent; no review/admission was created."}


def init_batch(domain: str, agent: str, batch_id: str, destination: Path) -> dict[str, Any]:
    """Create an empty assignment return without inventing researched models."""
    public_path(destination, {".json"})
    template = {"schema_version": SCHEMA_VERSION, "kit_version": KIT_VERSION, "batch_id": batch_id, "domain": domain,
                "curator": agent, "created": date.today().isoformat(), "example_only": False, "models": [], "deferred": [],
                "handoff": {"summary": "Replace with actual completed work.", "gaps": [], "connections": [], "queries": [],
                            "review_notes": "Replace with checks performed and checks not performed."}}
    with destination.open("xb") as stream:
        stream.write(encoded(template))
    return {"path": str(destination), "note": "Template intentionally fails final validation until research is supplied."}


def build_kit(destination: Path, domain: str | None = None) -> dict[str, Any]:
    """Build curator instructions with at most one task and no operator guidance."""
    public_path(destination, {".zip"})
    require(domain is None or domain in DOMAINS, "Unknown curation assignment domain.")
    paths = [Path("pyproject.toml"), Path("uv.lock"), Path("data/curation/example-bundle.json")]
    # Explicit implementation allowlist: do not traverse the repository or carry inference configuration.
    for name in ("__init__", "contracts", "expressions", "serialization", "solving", "runtime", "registry", "curation_schema", "curation"):
        paths.append(Path("connected_models") / f"{name}.py")
    contents = {path.as_posix(): (ROOT / path).read_bytes() for path in paths}
    guide = (ROOT / AGENT_GUIDE).read_text(encoding="utf-8")
    contents["AGENTS.md"] = guide.split("\n---\n", 2)[-1].encode("utf-8")
    contents["data/curation/batch.schema.json"] = encoded(SCHEMA)
    contents["data/curation/runtime-vocabulary.json"] = encoded({"kit_version": KIT_VERSION, "meanings": MEANINGS,
        "profile": VOCABULARY_PROFILE, "dimension_axes": DIMENSION_AXES, "numerical_basis": NUMERICAL_BASIS,
        "units": {name: {"dimensions": unit.dimensions, "scale": unit.scale} for name, unit in UNITS.items()},
        "known_model_ids": ["heat-to-electricity", "electricity-cost", "annual-saving", "uniform-present-value", "net-present-value"],
        "limits": "Bounded mechanics and energy/currency vocabulary. Contexts must match exactly. No automatic vocabulary extension. See guide for known source revisions."})
    if domain is not None:
        assignments = decode((ASSETS / "assignments.json").read_bytes())
        assignment = next(item for item in assignments if item["domain"] == domain)
        contents["assignment.json"] = encoded(assignment)
    contents["KIT-MANIFEST.json"] = encoded({"kit_version": KIT_VERSION, "schema_version": SCHEMA_VERSION,
        "files": {path: digest(raw) for path, raw in contents.items()}})
    with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, raw in contents.items():
            archive.writestr(path, raw)
    return {"path": str(destination), "kit_version": KIT_VERSION, "domain": domain, "files": len(contents)}


def main() -> int:
    """Expose offline, zero-inference curation operations with actionable errors."""
    parser = argparse.ArgumentParser(description="Portable Connected Models curation kit")
    commands = parser.add_subparsers(dest="command", required=True)
    for operation in ("validate", "import"):
        command = commands.add_parser(operation)
        command.add_argument("source", type=Path)
        if operation == "import":
            command.add_argument("--registry", type=Path, default=REGISTRY)
    pack = commands.add_parser("pack")
    pack.add_argument("source", type=Path)
    pack.add_argument("destination", type=Path)
    kit = commands.add_parser("kit")
    kit.add_argument("destination", type=Path)
    kit.add_argument("--domain", choices=DOMAINS, help="Include only this task; omit when providing the assignment in the prompt")
    init = commands.add_parser("init")
    init.add_argument("domain", choices=DOMAINS)
    init.add_argument("destination", type=Path)
    init.add_argument("--agent", required=True)
    init.add_argument("--batch-id", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            result = validate_bundle(load_bundle(args.source))
        elif args.command == "import":
            result = import_bundle(args.source, Registry(args.registry))
        elif args.command == "pack":
            result = pack_bundle(args.source, args.destination)
        elif args.command == "init":
            result = init_batch(args.domain, args.agent, args.batch_id, args.destination)
        else:
            result = build_kit(args.destination, args.domain)
        print(json.dumps(result, indent=2))
        return 0
    except (ModelError, OSError, ValueError, sqlite3.Error, zipfile.BadZipFile, RuntimeError) as exc:
        print(f"Cannot complete curation operation: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
