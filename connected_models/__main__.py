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


def main() -> int:
    """Run a selected operation and report useful errors without exposing secrets."""
    parser = argparse.ArgumentParser(description="Connected Models prototype")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Run a synthetic heating scenario; no inference calls")
    demo.add_argument("--performance", type=float, default=DEFAULT_COP)
    demo.add_argument("--investment", type=float, default=DEFAULT_CAPEX)
    demo.add_argument("--tariff", type=float, default=DEFAULT_TARIFF)
    demo.add_argument("--question", choices=("operating-cost", "investment"), default="investment")
    commands.add_parser("meta-smoke", help="One paid structured-output check using MODEL_API_KEY")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        if args.command == "meta-smoke":
            settings = InferenceSettings.load(Path("inference.toml"))
            result = smoke_test(settings, BudgetLedger(Path(".usage/meta.sqlite3"), settings))
            print(json.dumps(result, indent=2))
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
