"""Create pinned executable projections of separately reviewed research records."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sqlite3
from typing import Any
import zipfile

from .auditing import validate_review
from .contracts import Model, ModelError, Port, VOCABULARY_PROFILE
from .curation import REGISTRY, digest, encoded, load_bundle, public_path, require
from .registry import Registry
from .runtime import validate_model
from .serialization import text


def project_record(bundle: dict[str, Any], report: dict[str, Any], model_id: str, version: str) -> dict[str, Any]:
    """Retain unchanged research and audit evidence while deriving a runtime interface."""
    validate_review(bundle, report)
    text(version)
    original = next((item for item in bundle["models"] if item["id"] == model_id), None)
    require(original is not None, "Model ID not found in this batch.")
    review = next(item for item in report["models"] if item["id"] == model_id)
    require(review["recommendation"] == "recommend-admit", "Scientific reviewer did not recommend this record for admission.")
    require(not bundle["example_only"], "Teaching examples cannot become runtime projections.")
    require(version != original["revision"], "Use a distinct runtime projection version; preserve the research revision.")
    variables = {item["symbol"]: item for item in original["variables"]}

    def port(symbol: str) -> Port:
        """Preserve the original quantity, unit and exact context without adapters."""
        item = variables[symbol]
        return Port(item["quantity_id"], item["unit"], item["context"])

    output = original["relationship"]["output_symbol"]
    source = "; ".join(f"{item['url']} — {item['locator']}" for item in original["sources"])
    source += "; independent audit: " + "; ".join(item["url"] for item in review["sources"])
    model = Model(original["id"], version,
        {name: port(name) for name, item in variables.items() if item["role"] == "input"}, port(output),
        original["relationship"]["expression"], tuple(original["guards"]), source,
        tuple(original["assumptions"] + original["limitations"] + [f"Audited permitted use: {review['permitted_use']}"]), "candidate")
    validate_model(model)
    checks = [{"reference": case} for case in original["references"]]
    require(all(Registry.verify_reference(model, check) for check in checks), "Runtime projection failed reference replay.")
    return {"model": json.loads(json.dumps(asdict(model))), "intake_blockers": [], "checks": checks,
        "evidence": {"record": original, "scientific_review": report, "curator": bundle["curator"],
            "projection": {"profile": VOCABULARY_PROFILE, "batch_id": bundle["batch_id"],
                "batch_sha256": digest(encoded(bundle)), "record_sha256": digest(encoded(original)),
                "research_revision": original["revision"], "review_sha256": digest(encoded(report)),
                "note": "Projection resolves supported runtime gaps only; original research and disclosures retained unchanged."}}}


def stage_projection(source: Path, review_path: Path, model_id: str, version: str, registry: Registry) -> dict[str, Any]:
    """Stage reviewed technical payload without publishing it or changing the original."""
    public_path(review_path, {".json"})
    payload = project_record(load_bundle(source), load_bundle(review_path), model_id, version)
    candidate_id = registry.propose(payload)
    return {"status": "staged-not-published", "candidate_id": candidate_id,
            "model": f"{model_id}@{version}", "diagnostics": registry.candidate(candidate_id)["diagnostics"]}


def main() -> int:
    """Expose an explicit reviewed projection operation for the local integrator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("review", type=Path)
    parser.add_argument("model_id")
    parser.add_argument("--version", required=True)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    args = parser.parse_args()
    try:
        print(json.dumps(stage_projection(args.source, args.review, args.model_id, args.version, Registry(args.registry)), indent=2))
        return 0
    except (ModelError, ValueError, OSError, sqlite3.Error, zipfile.BadZipFile) as exc:
        print(f"Cannot integrate research record: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
