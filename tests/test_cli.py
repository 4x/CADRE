"""CLI entry point: run-id validation and the offline demo sequence."""

import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from uuid import uuid4

from connected_models.__main__ import main

from .support import scratch_directory


def run_cli(arguments: list[str], workspace: str) -> tuple[int, str]:
    """Run the CLI in a scratch working directory; capture exit code and stdout."""
    previous_argv = sys.argv
    previous_cwd = os.getcwd()
    buffer = StringIO()
    sys.argv = ["connected-models", *arguments]
    os.chdir(workspace)
    try:
        with redirect_stdout(buffer):
            code = main()
    finally:
        sys.argv = previous_argv
        os.chdir(previous_cwd)
    return code, buffer.getvalue()


class CliRunIdTests(unittest.TestCase):
    """A mistyped run id must explain itself, not blame configuration."""

    def test_inspect_malformed_run_id_reports_invalid(self) -> None:
        """A non-UUID run id fails fast with an actionable message."""
        with scratch_directory() as workspace:
            code, output = run_cli(["inspect", "does-not-exist"], workspace)
        self.assertEqual(code, 1)
        self.assertIn("That run id is not valid", output)
        self.assertNotIn("configuration", output)

    def test_inspect_unknown_run_id_reports_missing(self) -> None:
        """A well-formed but unsaved run id names the missing run."""
        missing = str(uuid4())
        with scratch_directory() as workspace:
            code, output = run_cli(["inspect", missing], workspace)
        self.assertEqual(code, 1)
        self.assertIn("No saved run has that id", output)
        self.assertIn("demo-seed", output)

    def test_replay_unknown_run_id_reports_missing(self) -> None:
        """Replay of an unsaved run id names the missing run."""
        missing = str(uuid4())
        with scratch_directory() as workspace:
            code, output = run_cli(["replay", missing], workspace)
        self.assertEqual(code, 1)
        self.assertIn("No saved run has that id", output)

    def test_revise_unknown_run_id_reports_missing(self) -> None:
        """Revision of an unsaved run id names the missing run."""
        missing = str(uuid4())
        with scratch_directory() as workspace:
            code, output = run_cli(
                ["revise", missing, "--set", "upgrade-energy.performance=2"],
                workspace,
            )
        self.assertEqual(code, 1)
        self.assertIn("No saved run has that id", output)

    def test_report_unknown_run_id_reports_missing(self) -> None:
        """A report over an unsaved run id names the missing run."""
        missing = str(uuid4())
        with scratch_directory() as workspace:
            code, output = run_cli(["report", missing], workspace)
        self.assertEqual(code, 1)
        self.assertIn("No saved run has that id", output)

    def test_scenarios_malformed_run_id_fails_before_inference(self) -> None:
        """A malformed scenarios run id is rejected without touching inference."""
        with scratch_directory() as workspace:
            code, output = run_cli(
                ["scenarios", "does-not-exist", "what if"], workspace
            )
        self.assertEqual(code, 1)
        self.assertIn("That run id is not valid", output)

    def test_serve_rejects_invalid_port(self) -> None:
        """An out-of-range serve port fails with a range message, not a traceback."""
        with scratch_directory() as workspace:
            code, output = run_cli(["serve", "--port", "0"], workspace)
        self.assertEqual(code, 1)
        self.assertIn("Port must be between 1 and 65535", output)


class CliDemoSequenceTests(unittest.TestCase):
    """The scripted demo runs end to end through the real CLI, offline."""

    def test_seed_inspect_replay_round_trip(self) -> None:
        """demo-seed output feeds inspect and replay with the documented figures."""
        with scratch_directory() as workspace:
            code, seeded = run_cli(["demo-seed"], workspace)
            self.assertEqual(code, 0)
            runs = json.loads(seeded)["runs"]
            investment_id = runs["investment"]["run_id"]
            self.assertAlmostEqual(
                runs["investment"]["outputs"]["investment-npv"]["amount"],
                8532.16,
                places=2,
            )
            code, inspected = run_cli(["inspect", investment_id], workspace)
            self.assertEqual(code, 0)
            self.assertIn(investment_id, inspected)
            code, replayed = run_cli(["replay", investment_id], workspace)
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(replayed)["matched"])
