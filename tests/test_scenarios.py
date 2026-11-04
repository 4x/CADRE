"""Meta-proposed what-if scenarios, each executed by the deterministic engine.

The model designs experiments; revise_run decides them. Accepted scenarios
carry executed engine figures (Dana's pessimistic case reproduces the
documented -417.40 USD NPV) and rejected ones carry the exact machine
error. No test here makes a network call.
"""

import json
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from connected_models.contracts import ModelError
from connected_models.demo import catalog, composition
from connected_models.registry import Registry
from connected_models.runtime import execute, save_run
from connected_models.scenarios import explore
from tests.support import scratch_directory

PESSIMISTIC_SETS = [
    "upgrade-energy.performance=2",
    "baseline-cost.tariff=0.25",
    "upgrade-cost.tariff=0.25",
    "investment-npv.investment=12000",
]
PESSIMISTIC_NPV_USD = -417.40


def _fixture_run_id(folder: str) -> str:
    """Execute and save the scripted investment case; return its run id."""
    manifest = execute(composition(operation="investment"), catalog())
    assert manifest["status"] == "completed"
    save_run(manifest, Path(folder))
    return str(manifest["run_id"])


def _scripted(*scenarios: dict[str, Any]) -> dict[str, Any]:
    """Wrap scripted scenarios as a fake priced-adapter response."""
    return {
        "content": {"scenarios": list(scenarios)},
        "audit": {"model": "scripted-test-model", "call_id": "test-call"},
    }


class ScenarioExplorationTests(unittest.TestCase):
    """Machine execution accepts or rejects every proposed scenario."""

    def test_accepted_scenario_executes_and_broken_one_is_rejected(self) -> None:
        """The pessimistic case reproduces the documented NPV; bad input is named."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            run_id = _fixture_run_id(folder)
            proposal = _scripted(
                {
                    "name": "pessimistic",
                    "rationale": "Weak performance, cheap power, pricey quote.",
                    "sets": PESSIMISTIC_SETS,
                },
                {
                    "name": "broken",
                    "rationale": "Targets an input the model never declared.",
                    "sets": ["upgrade-energy.voltage=2"],
                },
            )
            with patch(
                "connected_models.scenarios.live_request", return_value=proposal
            ) as live:
                record = explore(
                    registry,
                    run_id,
                    "What if the quote disappoints?",
                    directory=Path(folder),
                )
            self.assertEqual(record["accepted"], 1)
            self.assertEqual(record["rejected"], 1)
            self.assertEqual(
                record["inference"],
                {"model": "scripted-test-model", "call_id": "test-call"},
            )
            accepted, rejected = record["results"]
            self.assertEqual(accepted["verdict"], "accepted")
            self.assertAlmostEqual(
                float(accepted["outputs"]["investment-npv"]["amount"]),
                PESSIMISTIC_NPV_USD,
                places=2,
            )
            self.assertTrue(Path(str(accepted["saved_path"])).exists())
            self.assertEqual(rejected["verdict"], "rejected")
            self.assertIn("has no input 'voltage'", rejected["error"])
            self.assertTrue(Path(str(record["saved_path"])).exists())
            sent = json.loads(live.call_args[0][0][1]["content"])
            entries = sent["run"]["revisable_inputs"]
            self.assertIn(
                {
                    "node": "upgrade-energy",
                    "input": "performance",
                    "unit": "1",
                    "meaning": "seasonal_performance",
                    "current_amount": 3.0,
                },
                entries,
            )

    def test_malformed_proposals_fail_closed(self) -> None:
        """Shape violations abort the exploration instead of guessing."""
        bad_contents = [
            {"scenarios": []},
            {"scenarios": "pessimistic"},
            {"unexpected": []},
            "not-an-object",
            {
                "scenarios": [
                    {"name": "only-name"},
                ]
            },
            {
                "scenarios": [
                    {
                        "name": "too-many-sets",
                        "rationale": "Exceeds the per-scenario cap.",
                        "sets": [f"upgrade-energy.performance={n}" for n in range(9)],
                    }
                ]
            },
        ]
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            run_id = _fixture_run_id(folder)
            for content in bad_contents:
                with (
                    self.subTest(content=content),
                    patch(
                        "connected_models.scenarios.live_request",
                        return_value={"content": content, "audit": {}},
                    ),
                    self.assertRaises(ModelError),
                ):
                    explore(
                        registry,
                        run_id,
                        "Vary something.",
                        directory=Path(folder),
                    )

    def test_request_and_count_limits_never_call_the_model(self) -> None:
        """Empty or oversized requests and bad counts fail before inference."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            run_id = _fixture_run_id(folder)
            with patch("connected_models.scenarios.live_request") as live:
                with self.assertRaises(ModelError):
                    explore(registry, run_id, "   ", directory=Path(folder))
                with self.assertRaises(ModelError):
                    explore(registry, run_id, "x" * 2001, directory=Path(folder))
                with self.assertRaises(ModelError):
                    explore(
                        registry,
                        run_id,
                        "Vary something.",
                        max_scenarios=0,
                        directory=Path(folder),
                    )
                with self.assertRaises(ModelError):
                    explore(
                        registry,
                        run_id,
                        "Vary something.",
                        max_scenarios=6,
                        directory=Path(folder),
                    )
            live.assert_not_called()

    def test_non_completed_parent_is_rejected(self) -> None:
        """Scenarios need executed base outputs to vary and diff against."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            manifest = execute(composition(operation="investment"), catalog())
            manifest["status"] = "blocked"
            save_run(manifest, Path(folder))
            with (
                patch("connected_models.scenarios.live_request") as live,
                self.assertRaises(ModelError),
            ):
                explore(
                    registry,
                    str(manifest["run_id"]),
                    "Vary something.",
                    directory=Path(folder),
                )
            live.assert_not_called()
