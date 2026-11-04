"""Run the chain battery: live composer answers against engine oracle values.

Each entry sends its question through workflows.answer and compares the
returned outputs (matched by meaning) against the battery's expected
amounts within the entry tolerance. Tier-2 entries expect "blocked" until
their named bridge lands; a tier-2 entry that completes with correct
values is reported as FIXED so unblockings are detected automatically.

Needs live inference; the owner runs it with credentials:

    uv run --env-file .env -m evals.run_chain_battery [--ids t1-fisher,t2-dosing]

Reports print as a table and save to .runs/eval-<utc-timestamp>/report.json
alongside the per-query saved runs.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from connected_models.registry import Registry
from connected_models.workflows import REGISTRY_PATH, answer

ROOT = Path(__file__).resolve().parent.parent

BATTERY = ROOT / "data" / "eval" / "chain-battery.json"


def check_entry(
    entry: dict[str, Any], record: dict[str, Any], tolerance: float
) -> dict[str, Any]:
    """Compare one live answer against its oracle expectations."""
    expected_status = entry["expected_status"]
    status = record.get("status")
    failures: list[str] = []
    if status != expected_status:
        failures.append(f"status {status!r} != expected {expected_status!r}")
    outputs = record.get("outputs") or {}
    by_meaning = {value["port"]["meaning"]: value for value in outputs.values()}
    values_ok = True
    if status == "completed":
        for expected in entry["expected_outputs"]:
            actual = by_meaning.get(expected["meaning"])
            if actual is None:
                failures.append(f"missing output meaning {expected['meaning']}")
                values_ok = False
                continue
            if actual["port"]["unit"] != expected["unit"]:
                failures.append(
                    f"{expected['meaning']}: unit {actual['port']['unit']} != {expected['unit']}"
                )
                values_ok = False
            if "amounts" in expected:
                actual_list = actual.get("amounts")
                if actual_list is None and "amount" in actual and len(expected["amounts"]) == 1:
                    actual_list = [actual["amount"]]
                if actual_list is None or len(actual_list) != len(expected["amounts"]):
                    failures.append(f"{expected['meaning']}: {actual_list} != {expected['amounts']}")
                    values_ok = False
                else:
                    for position, (got, want) in enumerate(zip(actual_list, expected["amounts"])):
                        root_scale = max(1.0, abs(want))
                        if abs(got - want) > tolerance * root_scale:
                            failures.append(f"{expected['meaning']}[{position}]: {got} != {want}")
                            values_ok = False
                continue
            scale = max(1.0, abs(expected["amount"]))
            actual_amount = actual.get("amount")
            if actual_amount is None and len(actual.get("amounts") or []) == 1:
                actual_amount = actual["amounts"][0]
            if actual_amount is None:
                failures.append(f"{expected['meaning']}: no single amount in {sorted(actual)}")
                values_ok = False
            elif abs(actual_amount - expected["amount"]) > tolerance * scale:
                failures.append(f"{expected['meaning']}: {actual_amount} != {expected['amount']}")
                values_ok = False
    fixed = (
        bool(failures)
        and status == "completed"
        and values_ok
        and expected_status != "completed"
    )
    return {
        "id": entry["id"],
        "tier": entry["tier"],
        "status": status,
        "expected_status": expected_status,
        "run_id": record.get("run_id"),
        "saved_path": str(record.get("saved_path") or ""),
        "verdict": "fixed" if fixed else ("pass" if not failures else "fail"),
        "failures": [] if fixed else failures,
        "error": record.get("error"),
        "clarifications": record.get("clarifications"),
    }


def main() -> int:
    """Parse flags, run the selected entries, and save the report."""
    parser = argparse.ArgumentParser(description="Run the chain battery.")
    parser.add_argument(
        "--ids", default="", help="Comma-separated entry IDs; default runs all."
    )
    parser.add_argument(
        "--retrieval",
        default="subset",
        choices=("full", "subset"),
        help="Catalog retrieval mode; default sends a retrieved subset.",
    )
    args = parser.parse_args()
    battery = json.loads(BATTERY.read_bytes())
    wanted = {part.strip() for part in args.ids.split(",") if part.strip()}
    entries = [
        entry for entry in battery["entries"] if not wanted or entry["id"] in wanted
    ]
    if wanted and len(entries) != len(wanted):
        missing = wanted - {entry["id"] for entry in entries}
        raise SystemExit(f"Unknown battery IDs: {sorted(missing)}")
    registry = Registry(REGISTRY_PATH)
    tolerance = float(battery.get("tolerance_relative", 1e-6))
    results = []
    for entry in entries:
        record = answer(
            registry,
            entry["question"],
            fill_in_assumptions=bool(entry.get("fill_in_assumptions", True)),
            retrieval=args.retrieval,
        )
        results.append(check_entry(entry, record, tolerance))
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    folder = ROOT / ".runs" / f"eval-{stamp}"
    folder.mkdir(parents=True)
    (folder / "report.json").write_text(
        json.dumps(
            {
                "battery": battery["name"],
                "version": battery["version"],
                "results": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    for item in results:
        print(f"{item['verdict']:>5}  {item['id']:<18} {item['status']}")
        for failure in item["failures"]:
            print(f"         - {failure}")
    summary = {
        verdict: sum(1 for item in results if item["verdict"] == verdict)
        for verdict in ("pass", "fail", "fixed")
    }
    print(
        f"pass={summary['pass']} fail={summary['fail']} fixed={summary['fixed']}  report: {folder / 'report.json'}"
    )
    return 0 if summary["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
