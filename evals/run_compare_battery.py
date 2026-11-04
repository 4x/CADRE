"""Sweep the chain battery through grounded-vs-direct comparison.

For each battery entry this runs connected_models.compare (grounded route
plus direct LLM route with numeric agreement) and additionally checks the
grounded outputs against the battery oracle, so each row shows both whether
the engine is right and whether the direct answer agrees with it.

Needs live inference; the owner runs it with credentials:

    uv run --env-file .env -m evals.run_compare_battery [--battery deep] [--ids t1-fisher,t1-dosing] [--models muse-spark-1.3]

Prints one table row per query and saves .runs/compare-<timestamp>/report.json
linking every comparison, grounded run, and direct run. Each row also scores
the head-to-head: win means only the grounded route was right, tie means both
were, loss means grounded was wrong. Guard-trap entries (trap=true) invert the
test: refusal is correct, and a direct answer matching the naive amount loses.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from connected_models.compare import compare, extract_numbers, numeric_agreement
from connected_models.contracts import ModelError
from connected_models.inference import BudgetLedger, InferenceSettings
from connected_models.registry import Registry
from connected_models.workflows import REGISTRY_PATH
from evals.run_chain_battery import check_entry

ROOT = Path(__file__).resolve().parent.parent

BATTERIES = {
    "chain": ROOT / "data" / "eval" / "chain-battery.json",
    "deep": ROOT / "data" / "eval" / "deep-battery.json",
    "adversarial": ROOT / "data" / "eval" / "adversarial-battery.json",
}


def resolve_models(raw: str) -> list[str | None]:
    """Parse --models; validate every name against pricing before any call is sent."""
    names = [part.strip() for part in raw.split(",") if part.strip()]
    seen = list(dict.fromkeys(names))
    for name in seen:
        InferenceSettings.load(ROOT / "inference.toml", name)
    return cast(list[str | None], seen or [None])


def score_head_to_head(
    entry: dict[str, Any],
    battery_verdict: str,
    grounded_status: str,
    direct_text: str,
) -> dict[str, Any]:
    """Score grounded vs direct against the oracle: win means only we were right."""
    if entry.get("trap"):
        refused = grounded_status != "completed"
        naive = entry.get("naive_amounts") or []
        numbers = extract_numbers(direct_text or "")
        answered = any(
            abs(number - bad) <= 0.01 * max(1.0, abs(bad))
            for number in numbers
            for bad in naive
        )
        if refused and answered:
            wtl = "win"
        elif refused:
            wtl = "tie"
        else:
            wtl = "loss"
        return {
            "wtl": wtl,
            "grounded": "refused" if refused else "answered",
            "direct": "answered" if answered else "refused",
        }
    grounded_correct = battery_verdict in ("pass", "fixed")
    pseudo = {
        "status": "completed",
        "outputs": {
            f"e{index}": {
                "amount": expected.get("amount"),
                "amounts": expected.get("amounts"),
                "port": {"unit": expected["unit"], "meaning": expected["meaning"]},
            }
            for index, expected in enumerate(entry["expected_outputs"])
        },
    }
    direct_correct = numeric_agreement(pseudo, direct_text or "")["verdict"] == "agree"
    if grounded_correct and not direct_correct:
        wtl = "win"
    elif grounded_correct and direct_correct:
        wtl = "tie"
    else:
        wtl = "loss"
    return {
        "wtl": wtl,
        "grounded": "correct" if grounded_correct else "wrong",
        "direct": "correct" if direct_correct else "wrong",
    }


def check_trap(entry: dict[str, Any], grounded_status: str) -> dict[str, Any]:
    """Score a guard trap: any refusal is correct; any completion is a failure."""
    refused = grounded_status != "completed"
    return {
        "id": entry["id"],
        "tier": entry["tier"],
        "status": grounded_status,
        "verdict": "pass" if refused else "fail",
        "failures": [] if refused else ["guard trap was answered instead of refused"],
    }


def summarize(
    entry: dict[str, Any],
    comparison: dict[str, Any],
    battery: dict[str, Any],
    requested: str | None,
) -> dict[str, Any]:
    """Reduce one sweep result to its table row."""
    grounded, direct = comparison["grounded"], comparison["direct"]
    head = score_head_to_head(
        entry, battery["verdict"], grounded["status"], direct.get("direct_text") or ""
    )
    return {
        "id": entry["id"],
        "tier": entry["tier"],
        "model": comparison.get("model") or requested,
        "battery": battery["verdict"],
        "battery_failures": battery["failures"],
        "grounded_status": grounded["status"],
        "attempts": grounded["attempts"],
        "agreement": comparison["agreement"]["verdict"],
        "wtl": head["wtl"],
        "grounded_call": head["grounded"],
        "direct_call": head["direct"],
        "grounded_latency_s": round(grounded["latency_s"] or 0.0, 1),
        "direct_latency_s": round(direct["latency_s"] or 0.0, 1)
        if direct["latency_s"]
        else None,
        "comparison": str(comparison.get("saved_path") or ""),
    }


def main() -> int:
    """Parse flags, sweep the selected entries, and save the report."""
    parser = argparse.ArgumentParser(description="Sweep the battery through compare.")
    parser.add_argument(
        "--ids", default="", help="Comma-separated entry IDs; default runs all."
    )
    parser.add_argument(
        "--battery",
        default="chain",
        choices=sorted(BATTERIES),
        help="Which battery file to sweep; default chain.",
    )
    parser.add_argument(
        "--models",
        default="",
        help="Comma-separated inference models; default runs once with the configured model.",
    )
    args = parser.parse_args()
    try:
        models = resolve_models(args.models)
    except ModelError as exc:
        raise SystemExit(f"Cannot sweep models: {exc}") from None
    battery = json.loads(BATTERIES[args.battery].read_bytes())
    wanted = {part.strip() for part in args.ids.split(",") if part.strip()}
    entries = [
        entry for entry in battery["entries"] if not wanted or entry["id"] in wanted
    ]
    if wanted and len(entries) != len(wanted):
        missing = wanted - {entry["id"] for entry in entries}
        raise SystemExit(f"Unknown battery IDs: {sorted(missing)}")
    registry = Registry(REGISTRY_PATH)
    tolerance = float(battery.get("tolerance_relative", 1e-6))
    rows = []
    for requested in models:
        for entry in entries:
            comparison = compare(
                registry,
                entry["question"],
                fill_in_assumptions=bool(entry.get("fill_in_assumptions", True)),
                inference_model=requested,
            )
            if entry.get("trap"):
                verdict = check_trap(entry, comparison["grounded"]["status"])
            else:
                grounded_path = comparison["grounded"].get("saved_path") or ""
                record = (
                    json.loads(Path(grounded_path).read_bytes())
                    if grounded_path
                    else {"status": "missing"}
                )
                verdict = check_entry(entry, record, tolerance)
            rows.append(summarize(entry, comparison, verdict, requested))
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    folder = ROOT / ".runs" / f"compare-{stamp}"
    folder.mkdir(parents=True)
    ledger = BudgetLedger(
        ROOT / ".usage" / "meta.sqlite3",
        InferenceSettings.load(ROOT / "inference.toml"),
    )
    show_model = len(models) > 1
    header = f"{'model':<18}" if show_model else ""
    indent = " " * 18 if show_model else ""
    print(
        f"{header}{'id':<22}{'battery':<8}{'agree':<10}{'wtl':<5}{'g-lat':<7}{'d-lat':<7}{'att':<4}"
    )
    for row in rows:
        direct_latency = (
            f"{row['direct_latency_s']:.1f}"
            if row["direct_latency_s"] is not None
            else "-"
        )
        prefix = f"{row['model'] or '-':<18}" if show_model else ""
        print(
            f"{prefix}{row['id']:<22}{row['battery']:<8}{row['agreement']:<10}{row['wtl']:<5}"
            f"{row['grounded_latency_s']:<7.1f}{direct_latency:<7}{row['attempts']:<4}"
        )
        for failure in row["battery_failures"]:
            print(f"{indent}                       - {failure}")
    failed = sum(1 for row in rows if row["battery"] not in ("pass", "fixed"))
    score = {
        outcome: sum(1 for row in rows if row["wtl"] == outcome)
        for outcome in ("win", "tie", "loss")
    }
    print(
        f"head-to-head: win={score['win']} tie={score['tie']} loss={score['loss']}  "
        f"battery-fail={failed}  report: {folder / 'report.json'}"
    )
    (folder / "report.json").write_text(
        json.dumps(
            {
                "battery": battery["name"],
                "version": battery["version"],
                "score": score,
                "models": sorted({row["model"] for row in rows if row["model"]}),
                "rows": rows,
                "spend": ledger.summary(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
