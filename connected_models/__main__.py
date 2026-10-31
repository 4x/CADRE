"""Local commands for reproducible fixtures and a manually launched API check."""

import argparse
import json
import logging
from pathlib import Path
import sqlite3

from .contracts import ModelError
from .demo import DEFAULT_CAPEX, DEFAULT_COP, DEFAULT_TARIFF, catalog, composition
from .inference import BudgetLedger, InferenceSettings, smoke_test
from .runtime import execute, save_run
from .registry import Registry
from .reports import read_run, write_report
from .revisions import replay_run, revise_run
from .workflows import REGISTRY_PATH, answer, curate, review_bundle, seed_candidates


def main() -> int:
    """Run a selected operation and report useful errors without exposing secrets."""
    parser = argparse.ArgumentParser(description="Connected Models prototype")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Run a synthetic heating scenario; no inference calls")
    demo.add_argument("--performance", type=float, default=DEFAULT_COP)
    demo.add_argument("--investment", type=float, default=DEFAULT_CAPEX)
    demo.add_argument("--tariff", type=float, default=DEFAULT_TARIFF)
    demo.add_argument("--question", choices=("operating-cost", "investment"), default="investment")
    commands.add_parser("meta-smoke", help="One paid structured-output check using META_API_KEY")
    commands.add_parser("usage", help="Report application inference spending and reservations")
    commands.add_parser("seed-candidates", help="Stage four supporting manual candidates; does not publish")
    commands.add_parser("curate", help="Offline Meta extraction from the bundled NIST source packet")
    commands.add_parser("registry-list", help="List eligible stored versions")
    commands.add_parser("review-bundle", help="Prepare a readable review report without approving candidates")
    candidate = commands.add_parser("candidate", help="Inspect an extraction and its source/check evidence")
    candidate.add_argument("id")
    review = commands.add_parser("review", help="Record an owner's review of a candidate")
    review.add_argument("id")
    review.add_argument("--reviewer", required=True)
    review.add_argument("--notes", required=True)
    review.add_argument("--decision", required=True, choices=("accepted", "rejected", "withdrawn"))
    query = commands.add_parser("answer", help="Parse a self-contained question and compose reviewed stored models")
    query.add_argument("question")
    inspect = commands.add_parser("inspect", help="Inspect a saved run's result and actual lineage")
    inspect.add_argument("run_id")
    report = commands.add_parser("report", help="Export saved runs to a readable standalone HTML report")
    report.add_argument("run_ids", nargs="+")
    revise = commands.add_parser("revise", help="Revise a saved run's inputs or model revisions and rerun; preserves the original")
    revise.add_argument("run_id")
    revise.add_argument("--set", dest="sets", action="append", default=[],
                        help="Revise a direct input: node.input=amount in the model's declared unit")
    revise.add_argument("--model", dest="models", action="append", default=[],
                        help="Substitute a node model: node=model@version")
    replay = commands.add_parser("replay", help="Re-execute a saved run's graph against its pinned models and compare; saves nothing")
    replay.add_argument("run_id")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        if args.command == "inspect":
            record = read_run(args.run_id)
            print(json.dumps(record, indent=2))
            return 0
        if args.command == "report":
            print(f"Report: {write_report(args.run_ids)}")
            return 0
        if args.command == "replay":
            result = replay_run(args.run_id)
            print(json.dumps(result, indent=2))
            return 0 if result["matched"] else 1
        if args.command in {"meta-smoke", "usage"}:
            settings = InferenceSettings.load(Path("inference.toml"))
            ledger = BudgetLedger(Path(".usage/meta.sqlite3"), settings)
            result = ledger.summary() if args.command == "usage" else smoke_test(settings, ledger)
            print(json.dumps(result, indent=2))
            return 0
        if args.command in {"seed-candidates", "curate", "candidate", "review", "registry-list", "answer", "review-bundle", "revise"}:
            registry = Registry(REGISTRY_PATH)
            if args.command == "seed-candidates":
                print(json.dumps({"candidate_ids": seed_candidates(registry), "status": "awaiting-owner-review"}, indent=2))
            elif args.command == "curate":
                candidate_id = curate(registry)
                print(json.dumps(registry.candidate(candidate_id), indent=2))
            elif args.command == "candidate":
                print(json.dumps(registry.candidate(args.id), indent=2))
            elif args.command == "review":
                print(json.dumps({"review_id": registry.review(args.id, args.reviewer, args.notes, args.decision)}))
            elif args.command == "registry-list":
                _, admissions = registry.snapshot()
                print(json.dumps(admissions, indent=2))
            elif args.command == "review-bundle":
                print(f"Review report: {review_bundle(registry)}")
            elif args.command == "revise":
                record = revise_run(args.run_id, args.sets, args.models, registry)
                print(json.dumps({key: record.get(key) for key in ("run_id", "status", "revised_from", "revision", "outputs", "diff", "error", "saved_path")}, indent=2))
                return 0 if record["status"] == "completed" else 1
            else:
                record = answer(registry, args.question)
                print(json.dumps({key: record.get(key) for key in ("run_id", "status", "outputs", "clarifications", "solve_diagnostic", "error", "saved_path")}, indent=2))
                return 0 if record["status"] == "completed" else 1
            return 0
        manifest = execute(composition(args.performance, args.investment, args.tariff, args.question), catalog())
        path = save_run(manifest, Path(".runs"))
        print("Synthetic heating scenario — not measured household data or a validated forecast.")
        if manifest["status"] == "rejected":
            print(f"Cannot calculate: {manifest['error']}")
            print(f"Saved rejection evidence: {path}")
            return 1
        for name, value in manifest["outputs"].items():
            print(f"{name}: {value['amount']:,.2f} {value['port']['unit']}")
        print(f"Saved inputs, models, sources and intermediate results: {path}")
        return 0
    except (ModelError, OSError, sqlite3.Error, ValueError) as exc:
        if isinstance(exc, ModelError):
            print(f"Cannot complete operation: {exc}")
        else:
            logging.error(f"Operation failed with {type(exc).__name__}.")
            print("Could not read configuration or save local artifacts; check paths and permissions.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
