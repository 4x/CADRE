"""Build slice-E review.json files from verdicts.py (reviewer: ingest-cfa-b3a).

Reads worker bundles (read-only), binds review hashes with the repo's own
curation helpers, and writes review artifacts for b04-b50. b01-b03 are
invalid bundles and get report-only verdicts (no review.json possible:
auditing.validate_review validates the bundle first).
Usage: uv run --no-env-file python ingest-notes/slice-e-work/gen_reviews.py
"""

import json
from pathlib import Path

from connected_models.curation import digest, encoded

import verdicts

REVIEWER = "ingest-cfa-b3a"
REVIEWED = "2026-11-04"
SCHEMA_VERSION = "cm-scientific-review/1"
ROOT = Path("from-offline-curation-workers")
OUT = Path("ingest-notes/slice-e-work/reviews")

CHECKS = ("source-fidelity", "scope", "dimensions", "reference-independence",
          "guards-inverses", "rights-provenance")
KEYS = ("sf", "sc", "di", "ri", "gi", "rp")


def build_batch(n):
    """Build and write one batch review file; return recommendation counts."""
    batch = f"financial-analysis-cfa-l1-b3-b{n:02d}"
    bundle = json.loads((ROOT / batch / "bundle.json").read_text(encoding="utf-8"))
    spec = verdicts.V[f"b{n:02d}"]
    ids = {m["id"] for m in bundle["models"]}
    assert set(spec["rec"]) == ids, f"{batch}: verdict coverage mismatch"
    models = []
    for item in bundle["models"]:
        v = spec["rec"][item["id"]]
        if v["r"] == "recommend-admit":
            assert not item.get("unresolved"), f"{item['id']}: unresolved present"
            assert not v["b"], f"{item['id']}: admit with blockers"
        checks = {}
        for name, key in zip(CHECKS, KEYS):
            status, _, evidence = v[key].partition("|")
            assert status in ("passed", "failed", "not-checked"), (item["id"], key)
            assert evidence.strip(), (item["id"], key)
            checks[name] = {"status": status, "evidence": evidence}
        if v["r"] == "recommend-admit":
            assert all(c["status"] == "passed" for c in checks.values()), item["id"]
        sources = []
        for skey in v["s"]:
            src = dict(verdicts.S[skey])
            assert src["url"].startswith(("https://", "http://")), skey
            sources.append(src)
        assert sources, item["id"]
        models.append({
            "id": item["id"],
            "revision": item["revision"],
            "record_sha256": digest(encoded(item)),
            "checks": checks,
            "sources": sources,
            "blockers": list(v["b"]),
            "recommendation": v["r"],
            "permitted_use": v["u"],
        })
    review = {
        "schema_version": SCHEMA_VERSION,
        "batch_id": batch,
        "batch_sha256": digest(encoded(bundle)),
        "reviewer": REVIEWER,
        "reviewed": REVIEWED,
        "models": models,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{batch}-review.json").write_text(json.dumps(review, indent=1) + "\n",
                                              encoding="utf-8")
    counts = {}
    for m in models:
        counts[m["recommendation"]] = counts.get(m["recommendation"], 0) + 1
    return counts


def run():
    """Build all batch reviews and print totals."""
    totals = {}
    for n in range(4, 51):
        for rec, cnt in build_batch(n).items():
            totals[rec] = totals.get(rec, 0) + cnt
    print(f"batches=47 totals={totals}")


if __name__ == "__main__":
    run()
