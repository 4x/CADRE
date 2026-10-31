"""Revision-pinned offline reviewer packets and strict data-only review intake."""

import argparse
from datetime import date
import json
from pathlib import Path
from typing import Any
import zipfile

from .contracts import ModelError
from .curation import ROOT, digest, encoded, load_bundle, public_path, require, validate_bundle
from .curation_schema import STRING, array, choice, record, validate_schema

REVIEW_VERSION = "cm-scientific-review/1"
CRITERIA = ("source-fidelity", "scope", "dimensions", "reference-independence", "guards-inverses", "rights-provenance")
CHECK = record({"status": choice("passed", "failed", "not-checked"), "evidence": STRING})
SOURCE = record({"url": STRING, "locator": STRING, "accessed": STRING, "finding": STRING})
MODEL_REVIEW = record({"id": STRING, "revision": STRING, "record_sha256": STRING,
    "checks": record({name: CHECK for name in CRITERIA}), "sources": array(SOURCE),
    "blockers": array(STRING), "recommendation": choice("recommend-admit", "needs-revision", "blocked"),
    "permitted_use": STRING})
SCHEMA = record({"schema_version": choice(REVIEW_VERSION), "batch_id": STRING,
    "batch_sha256": STRING, "reviewer": STRING, "reviewed": STRING, "models": array(MODEL_REVIEW, 1, 12)})


def template(bundle: dict[str, Any]) -> dict[str, Any]:
    """Create an explicitly unfinished report bound to canonical original evidence."""
    return {"schema_version": REVIEW_VERSION, "batch_id": bundle["batch_id"],
        "batch_sha256": digest(encoded(bundle)), "reviewer": "REPLACE-with-reviewer-identity",
        "reviewed": date.today().isoformat(), "models": [{"id": item["id"], "revision": item["revision"],
        "record_sha256": digest(encoded(item)), "checks": {name: {"status": "not-checked", "evidence": "Not inspected."}
        for name in CRITERIA}, "sources": [], "blockers": ["Scientific review not performed."],
        "recommendation": "blocked", "permitted_use": "None pending review."} for item in bundle["models"]]}


def validate_review(bundle: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    """Validate every disposition and reject stale, partial or self-authored reviews."""
    validate_bundle(bundle)
    validate_schema(report, SCHEMA, "review")
    date.fromisoformat(report["reviewed"])
    require(report["reviewer"] != bundle["curator"] and not report["reviewer"].startswith("REPLACE-"),
            "A separate identified reviewer is required.")
    require(report["batch_id"] == bundle["batch_id"] and report["batch_sha256"] == digest(encoded(bundle)),
            "Review batch identity/hash mismatch.")
    originals = {item["id"]: item for item in bundle["models"]}
    require(len(report["models"]) == len(originals) and {item["id"] for item in report["models"]} == set(originals),
            "Review must cover every model exactly once.")
    for item in report["models"]:
        original = originals[item["id"]]
        require(item["revision"] == original["revision"] and item["record_sha256"] == digest(encoded(original)),
                "Review record identity/hash mismatch.")
        for source in item["sources"]:
            require(source["url"].startswith(("https://", "http://")), "Review evidence needs an actual source URL.")
            date.fromisoformat(source["accessed"])
        if item["recommendation"] == "recommend-admit":
            require(not item["blockers"] and item["sources"] and not original["unresolved"]
                    and all(check["status"] == "passed" for check in item["checks"].values()),
                    "Admission recommendation requires all checks, accessed evidence and no unresolved blockers.")
    return {"status": "valid-review-not-published", "batch_id": report["batch_id"],
            "reviewer": report["reviewer"], "recommendations": {item["id"]: item["recommendation"] for item in report["models"]}}


def build_packet(source: Path, destination: Path) -> dict[str, Any]:
    """Package one unchanged return, reviewer-only instructions, schema and template."""
    bundle = load_bundle(source)
    validate_bundle(bundle)
    public_path(source, {".zip"})
    public_path(destination, {".zip"})
    guide = (ROOT / "knowledge/notes/offline-auditor-instructions.md").read_text(encoding="utf-8")
    contents = {"AGENTS.md": guide.split("\n---\n", 2)[-1].encode(), "return.zip": source.read_bytes(),
        "review.schema.json": encoded(SCHEMA), "review-template.json": encoded(template(bundle)),
        "assignment.json": encoded({"task": "Audit every record and return review.json as instructed by AGENTS.md",
            "batch_id": bundle["batch_id"], "archive_sha256": digest(source.read_bytes()),
            "batch_sha256": digest(encoded(bundle))})}
    with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in contents.items():
            archive.writestr(name, raw)
    return {"path": str(destination), "batch_id": bundle["batch_id"], "files": len(contents)}


def main() -> int:
    """Expose zero-inference packet creation and report validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for operation in ("packet", "validate"):
        command = commands.add_parser(operation)
        command.add_argument("source", type=Path)
        command.add_argument("artifact", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "packet":
            result = build_packet(args.source, args.artifact)
        else:
            public_path(args.artifact, {".json"})
            result = validate_review(load_bundle(args.source), load_bundle(args.artifact))
        print(json.dumps(result, indent=2))
        return 0
    except (ModelError, ValueError, OSError, zipfile.BadZipFile) as exc:
        print(f"Cannot complete audit operation: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
