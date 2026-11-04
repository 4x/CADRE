"""Local commands for reproducible fixtures and a manually launched API check."""

import argparse
import json
import logging
import sqlite3
from pathlib import Path
from uuid import UUID

from .compare import compare
from .compatibility import audit_pairs
from .contracts import ModelError, describe_units
from .demo import DEFAULT_CAPEX, DEFAULT_COP, DEFAULT_TARIFF, catalog, composition
from .demo_seed import seed_demo
from .inference import BudgetLedger, InferenceSettings, smoke_test
from .mcp_server import run_stdio
from .registry import Registry
from .reports import read_run, write_report
from .revisions import replay_run, revise_run
from .runtime import execute, save_run
from .scenarios import explore
from .serve import ServerConfig, serve
from .workflows import (
    REGISTRY_PATH,
    RUNS_PATH,
    answer,
    curate,
    fill_in_assumptions_enabled,
    review_bundle,
    seed_candidates,
)

RUN_ID_COMMANDS = frozenset({"inspect", "replay", "revise", "scenarios", "report"})


def command_run_ids(args: argparse.Namespace) -> list[str]:
    """Collect the run ids a command addresses, so the CLI can validate them early."""
    if args.command in {"inspect", "replay", "revise", "scenarios"}:
        return [str(args.run_id)]
    if args.command == "report":
        return [str(run_id) for run_id in args.run_ids]
    return []


def is_missing_run_file(exc: BaseException) -> bool:
    """Detect a saved-run lookup that failed because the run file is absent."""
    return isinstance(exc, FileNotFoundError) and str(
        getattr(exc, "filename", "") or ""
    ).endswith(".json")


def main() -> int:
    """Run a selected operation and report useful errors without exposing secrets."""
    parser = argparse.ArgumentParser(description="Connected Models prototype")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser(
        "demo", help="Run a synthetic heating scenario; no inference calls"
    )
    demo.add_argument("--performance", type=float, default=DEFAULT_COP)
    demo.add_argument("--investment", type=float, default=DEFAULT_CAPEX)
    demo.add_argument("--tariff", type=float, default=DEFAULT_TARIFF)
    demo.add_argument(
        "--question", choices=("operating-cost", "investment"), default="investment"
    )
    serve_parser = commands.add_parser(
        "serve", help="Serve the local web demo; no third-party packages"
    )
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--bind", default="127.0.0.1")
    commands.add_parser(
        "demo-seed",
        help="Seed labeled demo fixtures and scripted runs; offline, no inference",
    )
    commands.add_parser("mcp", help="Serve MCP tools over stdio for agent clients")
    commands.add_parser(
        "meta-smoke", help="One paid structured-output check using META_API_KEY"
    )
    commands.add_parser(
        "usage", help="Report application inference spending and reservations"
    )
    units = commands.add_parser(
        "units", help="List canonical units with dimensions, scales, and aliases"
    )
    units.add_argument("filter", nargs="?", default="")
    commands.add_parser(
        "seed-candidates",
        help="Stage four supporting manual candidates; does not publish",
    )
    commands.add_parser(
        "curate", help="Offline Meta extraction from the bundled NIST source packet"
    )
    commands.add_parser("registry-list", help="List eligible stored versions")
    commands.add_parser(
        "compat-audit",
        help="Audit chain compatibility across eligible models; no inference calls",
    )
    compare_parser = commands.add_parser(
        "compare",
        help="Answer one question via the grounded route and directly, side by side",
    )
    compare_parser.add_argument(
        "question", help="Self-contained question for both routes"
    )
    compare_parser.add_argument(
        "--fill-in-assumptions",
        action="store_true",
        help="Let the grounded route fill question-implied assumptions (direct route unaffected)",
    )
    compare_parser.add_argument(
        "--model",
        default=None,
        help="Inference model for both routes; overrides LLM and inference.toml (must be priced)",
    )
    commands.add_parser(
        "review-bundle",
        help="Prepare a readable review report without approving candidates",
    )
    candidate = commands.add_parser(
        "candidate", help="Inspect an extraction and its source/check evidence"
    )
    candidate.add_argument("id")
    review = commands.add_parser(
        "review", help="Record an owner's review of a candidate"
    )
    review.add_argument("id")
    review.add_argument("--reviewer", required=True)
    review.add_argument("--notes", required=True)
    review.add_argument(
        "--decision", required=True, choices=("accepted", "rejected", "withdrawn")
    )
    query = commands.add_parser(
        "answer",
        help="Parse a self-contained question and compose reviewed stored models",
    )
    query.add_argument("question")
    query.add_argument(
        "--fill-in-assumptions",
        action="store_true",
        help="Let the composer supply question-implied values as documented assumptions",
    )
    query.add_argument(
        "--model",
        default=None,
        help="Inference model; overrides LLM and inference.toml (must be priced)",
    )
    query.add_argument(
        "--retrieval",
        default="subset",
        choices=("full", "subset"),
        help="Catalog retrieval mode; default sends a retrieved subset.",
    )
    inspect = commands.add_parser(
        "inspect", help="Inspect a saved run's result and actual lineage"
    )
    inspect.add_argument("run_id")
    report = commands.add_parser(
        "report", help="Export saved runs to a readable standalone HTML report"
    )
    report.add_argument("run_ids", nargs="+")
    revise = commands.add_parser(
        "revise",
        help="Revise a saved run's inputs or model revisions and rerun; preserves the original",
    )
    revise.add_argument("run_id")
    revise.add_argument(
        "--set",
        dest="sets",
        action="append",
        default=[],
        help="Revise a direct input: node.input=amount in the model's declared unit",
    )
    revise.add_argument(
        "--model",
        dest="models",
        action="append",
        default=[],
        help="Substitute a node model: node=model@version",
    )
    replay = commands.add_parser(
        "replay",
        help="Re-execute a saved run's graph against its pinned models and compare; saves nothing",
    )
    replay.add_argument("run_id")
    scenarios = commands.add_parser(
        "scenarios",
        help="Propose and execute named what-if scenarios for a saved run",
    )
    scenarios.add_argument("run_id")
    scenarios.add_argument("request")
    scenarios.add_argument(
        "--model",
        default=None,
        help="Inference model; overrides LLM and inference.toml (must be priced)",
    )
    scenarios.add_argument(
        "--max",
        dest="max_scenarios",
        type=int,
        default=3,
        help="Maximum scenarios to propose (1 to 5)",
    )
    args = parser.parse_args()
    for run_id in command_run_ids(args):
        try:
            UUID(run_id)
        except ValueError:
            print(
                f"That run id is not valid: {run_id!r}. "
                "Run ids are UUIDs printed by demo-seed; check the id and retry."
            )
            return 1
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
        if args.command == "units":
            print(describe_units(args.filter))
            return 0
        if args.command == "serve":
            if not 1 <= args.port <= 65535:
                print("Port must be between 1 and 65535.")
                return 1
            try:
                serve(ServerConfig(REGISTRY_PATH, RUNS_PATH), args.bind, args.port)
            except OSError:
                logging.error(f"Serve failed on {args.bind}:{args.port} with OSError.")
                print(
                    f"Cannot serve on {args.bind}:{args.port}; "
                    "the address may be in use or blocked. Try another --port."
                )
                return 1
            return 0
        if args.command == "mcp":
            run_stdio(ServerConfig(REGISTRY_PATH, RUNS_PATH))
            return 0
        if args.command in {"meta-smoke", "usage"}:
            settings = InferenceSettings.load(Path("inference.toml"))
            ledger = BudgetLedger(Path(".usage/meta.sqlite3"), settings)
            result = (
                ledger.summary()
                if args.command == "usage"
                else smoke_test(settings, ledger)
            )
            print(json.dumps(result, indent=2))
            return 0
        if args.command in {
            "seed-candidates",
            "curate",
            "candidate",
            "review",
            "registry-list",
            "answer",
            "review-bundle",
            "revise",
            "compat-audit",
            "compare",
            "demo-seed",
            "scenarios",
        }:
            registry = Registry(REGISTRY_PATH)
            if args.command == "seed-candidates":
                print(
                    json.dumps(
                        {
                            "candidate_ids": seed_candidates(registry),
                            "status": "awaiting-owner-review",
                        },
                        indent=2,
                    )
                )
            elif args.command == "demo-seed":
                print(json.dumps(seed_demo(registry, RUNS_PATH), indent=2))
            elif args.command == "curate":
                candidate_id = curate(registry)
                print(json.dumps(registry.candidate(candidate_id), indent=2))
            elif args.command == "candidate":
                print(json.dumps(registry.candidate(args.id), indent=2))
            elif args.command == "review":
                print(
                    json.dumps(
                        {
                            "review_id": registry.review(
                                args.id, args.reviewer, args.notes, args.decision
                            )
                        }
                    )
                )
            elif args.command == "registry-list":
                _, admissions = registry.snapshot()
                print(json.dumps(admissions, indent=2))
            elif args.command == "compat-audit":
                models, _ = registry.snapshot()
                print(json.dumps(audit_pairs(models), indent=2))
            elif args.command == "compare":
                record = compare(
                    registry,
                    args.question,
                    fill_in_assumptions_enabled(args.fill_in_assumptions),
                    args.model,
                )
                grounded, direct = record["grounded"], record["direct"]
                print(f"question: {record['question']}")
                print(f"model: {record.get('model')}")
                print(
                    f"grounded: {grounded['status']} in {grounded['latency_s']:.1f}s "
                    f"({grounded['attempts']} attempt(s))"
                )
                for node_id, value in (grounded["outputs"] or {}).items():
                    print(
                        f"  {node_id}: {value['amount']} {value['port']['unit']} ({value['port']['meaning']})"
                    )
                if grounded.get("error"):
                    print(f"  error: {grounded['error']}")
                latency = direct["latency_s"]
                print(
                    f"direct: {'error: ' + direct['error'] if direct.get('error') else f'{latency:.1f}s'}"
                )
                print(f"  {direct['direct_text'][:800]}")
                print(f"agreement: {record['agreement']['verdict']}")
                for detail in record["agreement"]["details"]:
                    print(
                        f"  {detail['meaning']}: expected {detail['expected']}, "
                        f"matched {detail['matched']}"
                    )
                print(f"saved: {record['saved_path']}")
                return 0
            elif args.command == "scenarios":
                record = explore(
                    registry,
                    args.run_id,
                    args.request,
                    args.model,
                    max_scenarios=args.max_scenarios,
                )
                print(
                    json.dumps(
                        {
                            key: record.get(key)
                            for key in (
                                "run_id",
                                "parent_run_id",
                                "request",
                                "accepted",
                                "rejected",
                                "results",
                                "saved_path",
                            )
                        },
                        indent=2,
                    )
                )
                return 0
            elif args.command == "review-bundle":
                print(f"Review report: {review_bundle(registry)}")
            elif args.command == "revise":
                record = revise_run(args.run_id, args.sets, args.models, registry)
                print(
                    json.dumps(
                        {
                            key: record.get(key)
                            for key in (
                                "run_id",
                                "status",
                                "revised_from",
                                "revision",
                                "outputs",
                                "diff",
                                "error",
                                "saved_path",
                            )
                        },
                        indent=2,
                    )
                )
                return 0 if record["status"] == "completed" else 1
            else:
                record = answer(
                    registry,
                    args.question,
                    fill_in_assumptions_enabled(args.fill_in_assumptions),
                    args.model,
                    retrieval=args.retrieval,
                )
                print(
                    json.dumps(
                        {
                            key: record.get(key)
                            for key in (
                                "run_id",
                                "status",
                                "outputs",
                                "assumptions",
                                "clarifications",
                                "solve_diagnostic",
                                "error",
                                "saved_path",
                            )
                        },
                        indent=2,
                    )
                )
                return 0 if record["status"] == "completed" else 1
            return 0
        manifest = execute(
            composition(args.performance, args.investment, args.tariff, args.question),
            catalog(),
        )
        path = save_run(manifest, Path(".runs"))
        print(
            "Synthetic heating scenario — not measured household data or a validated forecast."
        )
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
        elif args.command in RUN_ID_COMMANDS and is_missing_run_file(exc):
            logging.error(f"Run file missing for {args.command}.")
            print(
                "No saved run has that id. "
                "Check the run id or run 'demo-seed' to create the scripted runs."
            )
        else:
            logging.error(f"Operation failed with {type(exc).__name__}.")
            print(
                "Could not read configuration or save local artifacts; check paths and permissions."
            )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
