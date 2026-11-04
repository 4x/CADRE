"""Audit retrieval recall: every chain-battery question must retrieve its reference models.

Ground truth comes from the latest passing sweep rows: each passing run's
saved composition records the models the question actually executed. The
audit rebuilds the retrieval shortlist per question and fails if any
reference model falls outside it. Offline; no inference calls.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from connected_models.compatibility import audit_pairs  # noqa: E402
from connected_models.registry import Registry  # noqa: E402
from connected_models.retrieval import (  # noqa: E402
    FALLBACK_CAP,
    FALLBACK_K,
    RETRIEVAL_CAP,
    SEED_K,
    build_index,
    neighbors_from_audit,
    retrieve,
)
from connected_models.workflows import REGISTRY_PATH, catalog_card  # noqa: E402

BATTERY = ROOT / "data" / "eval" / "chain-battery.json"


def latest_passing_rows() -> dict[str, dict]:
    """Map each entry ID to its latest passing sweep row, newest report first."""
    latest: dict[str, dict] = {}
    reports = sorted((ROOT / ".runs").glob("eval-*/report.json"), reverse=True)
    for report in reports:
        try:
            rows = json.loads(report.read_bytes())["results"]
        except (KeyError, ValueError):
            continue
        for row in rows:
            if row.get("verdict") == "pass" and row["id"] not in latest:
                latest[row["id"]] = row
    return latest


def executed_models(run_id: str) -> set[str]:
    """Return the model keys one saved run executed."""
    run = json.loads((ROOT / ".runs" / f"{run_id}.json").read_bytes())
    return {node["model"] for node in (run.get("composition") or {}).get("nodes", [])}


def main() -> int:
    """Run the audit and report per-question recall."""
    battery = json.loads(BATTERY.read_bytes())
    models, _ = Registry(REGISTRY_PATH).snapshot()
    index = build_index(models)
    neighbors = neighbors_from_audit(audit_pairs(models))
    full_bytes = len(
        json.dumps({key: catalog_card(model) for key, model in models.items()}).encode()
    )
    rows = latest_passing_rows()
    failures = []
    uncovered = []
    worst_recall = 1.0
    for entry in battery["entries"]:
        row = rows.get(entry["id"])
        if row is None:
            uncovered.append(entry["id"])
            continue
        need = executed_models(row["run_id"])
        got = set(
            retrieve(
                entry["question"], index, neighbors, k=SEED_K, cap=RETRIEVAL_CAP
            ).keys
        )
        missed = sorted(need - got)
        recall = len(need & got) / len(need) if need else 1.0
        worst_recall = min(worst_recall, recall)
        subset_bytes = len(
            json.dumps({key: catalog_card(models[key]) for key in sorted(got)}).encode()
        )
        print(
            f"{entry['id']:<24} recall={recall:.2f} retrieved={len(got):>3} "
            f"bytes={subset_bytes / 1024:6.1f}KB missed={missed}"
        )
        if missed:
            wide = set(
                retrieve(
                    entry["question"], index, neighbors, k=FALLBACK_K, cap=FALLBACK_CAP
                ).keys
            )
            print(f"  fallback retrieves {sorted(need - wide) or 'all'}")
            failures.append(entry["id"])
    print(
        f"catalog: {len(models)} models, {full_bytes / 1024:.1f}KB full cards; "
        f"worst recall {worst_recall:.2f}"
    )
    if uncovered:
        print(f"UNCOVERED (no passing run): {uncovered}")
    if failures:
        print(f"RECALL FAILURES: {failures}")
    return 0 if not failures and not uncovered else 1


if __name__ == "__main__":
    raise SystemExit(main())
