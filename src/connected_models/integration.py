"""Create pinned executable projections of separately reviewed research records."""

import argparse
import json
import re
import sqlite3
import zipfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .auditing import validate_review
from .contracts import VOCABULARY_PROFILE, Family, Model, ModelError, Port
from .curation import REGISTRY, digest, encoded, load_bundle, public_path, require
from .registry import Registry
from .runtime import validate_model
from .serialization import text

RIGHTS_WAIVER_ASSUMPTION = (
    "TEMPORARY RIGHTS WAIVER (owner-ordered): licensing clearance waived "
    "for local use; all scientific checks passed and reference replay "
    "passed. Withdraw to reverse."
)

_WAIVER_DIRTY_BLOCKER = re.compile(r"supersede|duplicate|withdraw", re.IGNORECASE)


def rights_only_waivable(item: dict[str, Any]) -> bool:
    """Decide whether a needs-revision record is blocked only on licensing.

    Strict allowlist: a needs-revision verdict, every scientific check
    passed, rights-provenance failed, and no supersession, duplication, or
    withdrawal blocker. Anything else — including rights merely
    not-checked — is not waivable.
    """
    if item.get("recommendation") != "needs-revision":
        return False
    checks = item.get("checks")
    if not isinstance(checks, dict) or not checks:
        return False
    for name, check in checks.items():
        status = check.get("status") if isinstance(check, dict) else None
        if name == "rights-provenance":
            if status != "failed":
                return False
        elif status != "passed":
            return False
    return not any(
        isinstance(blocker, str) and _WAIVER_DIRTY_BLOCKER.search(blocker)
        for blocker in item.get("blockers", [])
    )


def project_record(
    bundle: dict[str, Any],
    report: dict[str, Any],
    model_id: str,
    version: str,
    relax_rights: bool = False,
) -> dict[str, Any]:
    """Retain unchanged research and audit evidence while deriving a runtime interface.

    With relax_rights=True, a needs-revision record whose only failed check
    is rights-provenance may project; the waiver is stamped into the
    projection evidence and model assumptions. Default False preserves the
    recommend-admit requirement. Vocabulary, dimension, guard, reference,
    and revision gates apply either way.
    """
    validate_review(bundle, report)
    text(version)
    original = next((item for item in bundle["models"] if item["id"] == model_id), None)
    require(original is not None, "Model ID not found in this batch.")
    assert original is not None
    review = next(item for item in report["models"] if item["id"] == model_id)
    waived = False
    if review["recommendation"] != "recommend-admit":
        require(
            relax_rights and rights_only_waivable(review),
            "Scientific reviewer did not recommend this record for admission.",
        )
        waived = True
    require(
        not bundle["example_only"],
        "Teaching examples cannot become runtime projections.",
    )
    require(
        version != original["revision"],
        "Use a distinct runtime projection version; preserve the research revision.",
    )
    variables = {item["symbol"]: item for item in original["variables"]}

    def port(symbol: str) -> Port:
        """Preserve the original quantity, unit and exact context without adapters."""
        item = variables[symbol]
        return Port(item["quantity_id"], item["unit"], item["context"])

    def family(symbol: str) -> Family:
        """Preserve the original element declaration and size bound without adapters."""
        item = variables[symbol]
        return Family(
            item["quantity_id"], item["unit"], item["context"], item["max_size"]
        )

    output = original["relationship"]["output_symbol"]
    source = "; ".join(
        f"{item['url']} — {item['locator']}" for item in original["sources"]
    )
    source += "; independent audit: " + "; ".join(
        item["url"] for item in review["sources"]
    )
    model = Model(
        original["id"],
        version,
        {
            name: port(name)
            for name, item in variables.items()
            if item["role"] == "input"
        },
        port(output),
        original["relationship"]["expression"],
        tuple(original["guards"]),
        source,
        tuple(
            original["assumptions"]
            + original["limitations"]
            + [f"Audited permitted use: {review['permitted_use']}"]
            + ([RIGHTS_WAIVER_ASSUMPTION] if waived else [])
        ),
        "candidate",
        {
            name: family(name)
            for name, item in variables.items()
            if item["role"] == "family"
        },
    )
    validate_model(model)
    checks = [{"reference": case} for case in original["references"]]
    require(
        all(Registry.verify_reference(model, check) for check in checks),
        "Runtime projection failed reference replay.",
    )
    payload = {
        "model": json.loads(json.dumps(asdict(model))),
        "intake_blockers": [],
        "checks": checks,
        "evidence": {
            "record": original,
            "scientific_review": report,
            "curator": bundle["curator"],
            "projection": {
                "profile": VOCABULARY_PROFILE,
                "batch_id": bundle["batch_id"],
                "batch_sha256": digest(encoded(bundle)),
                "record_sha256": digest(encoded(original)),
                "research_revision": original["revision"],
                "review_sha256": digest(encoded(report)),
                "note": "Projection resolves supported runtime gaps only; original research and disclosures retained unchanged.",
            },
        },
    }
    if waived:
        payload["evidence"]["projection"]["rights_waiver"] = {
            "relaxed": True,
            "failed_check": "rights-provenance",
            "reviewer": report["reviewer"],
            "note": (
                "Owner-ordered temporary waiver of licensing clearance; "
                "all scientific checks passed. Reversible via a withdrawn review."
            ),
        }
    return payload


def stage_projection(
    source: Path,
    review_path: Path,
    model_id: str,
    version: str,
    registry: Registry,
    relax_rights: bool = False,
) -> dict[str, Any]:
    """Stage reviewed technical payload without publishing it or changing the original."""
    public_path(review_path, {".json"})
    payload = project_record(
        load_bundle(source), load_bundle(review_path), model_id, version, relax_rights
    )
    candidate_id = registry.propose(payload)
    return {
        "status": "staged-not-published",
        "candidate_id": candidate_id,
        "model": f"{model_id}@{version}",
        "diagnostics": registry.candidate(candidate_id)["diagnostics"],
    }


def main() -> int:
    """Expose an explicit reviewed projection operation for the local integrator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("review", type=Path)
    parser.add_argument("model_id")
    parser.add_argument("--version", required=True)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument(
        "--relax-rights",
        action="store_true",
        help=(
            "Temporarily waive rights-provenance clearance for records whose "
            "scientific checks all pass (default off). Waived projections are "
            "stamped; reverse with a withdrawn review."
        ),
    )
    args = parser.parse_args()
    try:
        print(
            json.dumps(
                stage_projection(
                    args.source,
                    args.review,
                    args.model_id,
                    args.version,
                    Registry(args.registry),
                    args.relax_rights,
                ),
                indent=2,
            )
        )
        return 0
    except (ModelError, ValueError, OSError, sqlite3.Error, zipfile.BadZipFile) as exc:
        print(f"Cannot integrate research record: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
