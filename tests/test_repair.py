"""Compose-execute-repair loop: machine errors feed bounded retries."""

import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from connected_models.registry import Registry
from connected_models.workflows import answer, seed_candidates
from tests.support import scratch_directory


def _proposal(key: str, bad_input: str | None = None) -> dict[str, Any]:
    """Build a cost proposal with an optionally broken binding target."""
    return {
        "facts": [
            {
                "id": "fact-e",
                "name": "energy",
                "value_type": "number",
                "value": "20",
                "unit": "kWh",
                "quote": "Energy is 20 kWh",
                "assumption": "",
            },
            {
                "id": "fact-t",
                "name": "tariff",
                "value_type": "number",
                "value": "0.25",
                "unit": "USD/kWh",
                "quote": "0.25 USD/kWh",
                "assumption": "",
            },
        ],
        "issues": [],
        "status": "proposed",
        "graph": {
            "id": "cost",
            "nodes": [
                {
                    "id": "n1",
                    "model": key,
                    "bindings": [
                        {"input": "energy", "source": "fact", "ref": "fact-e"},
                        {
                            "input": bad_input or "tariff",
                            "source": "fact",
                            "ref": "fact-t",
                        },
                    ],
                }
            ],
            "outputs": ["n1"],
        },
        "reason": "Direct model.",
        "clarifications": [],
    }


class RepairLoopTests(unittest.TestCase):
    """Repairable machine errors retry; human declines stop immediately."""

    def _key(self, registry: Registry) -> str:
        """Admit the seed fixtures and return the cost model key."""
        for candidate_id in seed_candidates(registry):
            registry.review(candidate_id, "test-reviewer", "Test-only admission.")
        models, _ = registry.snapshot()
        return next(name for name in models if "electricity-cost" in name)

    def test_repair_recovers_and_records_both_attempts(self) -> None:
        """A binding error plus the repair prompt yields a completed run."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            key = self._key(registry)
            question = "Energy is 20 kWh at 0.25 USD/kWh. What is the cost?"
            responses = [
                {"content": _proposal(key, "voltage"), "audit": {"call": 1}},
                {"content": _proposal(key), "audit": {"call": 2}},
            ]
            with (
                patch(
                    "connected_models.workflows.live_request", side_effect=responses
                ) as request,
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, question)
            self.assertEqual(request.call_count, 2)
            self.assertEqual(run["status"], "completed")
            self.assertEqual(run["outputs"]["n1"]["amount"], 5)
            self.assertEqual(len(run["attempts"]), 2)
            self.assertIn("undeclared input", run["attempts"][0]["error"])
            self.assertIsNone(run["attempts"][1]["error"])
            repair_messages = request.call_args_list[1][0][0]
            self.assertIn("Repair round", repair_messages[0]["content"])
            self.assertIn("machine_error", repair_messages[1]["content"])

    def test_answer_without_audits_records_no_model(self) -> None:
        """Dead inference on every attempt leaves model unset instead of crashing."""
        from connected_models.contracts import ModelError

        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            self._key(registry)
            with (
                patch(
                    "connected_models.workflows.live_request",
                    side_effect=ModelError("Unknown model 'nope-9' in --model"),
                ),
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(
                    registry,
                    "Energy is 20 kWh at 0.25 USD/kWh. What is the cost?",
                    False,
                    "nope-9",
                )
            self.assertIsNone(run["model"])
            self.assertEqual(run["status"], "blocked")

    def test_model_survives_into_repair_attempts(self) -> None:
        """The node loop must not shadow the inference-model selection on retries."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            key = self._key(registry)
            question = "Energy is 20 kWh at 0.25 USD/kWh. What is the cost?"
            responses = [
                {"content": _proposal(key, "voltage"), "audit": {"model": "probe-m"}},
                {"content": _proposal(key), "audit": {"model": "probe-m"}},
            ]
            with (
                patch(
                    "connected_models.workflows.live_request", side_effect=responses
                ) as request,
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, question, False, "probe-m")
            self.assertEqual(request.call_count, 2)
            self.assertEqual(
                [call[0][3] for call in request.call_args_list], ["probe-m", "probe-m"]
            )
            self.assertEqual(run["status"], "completed")

    def test_answer_threads_model_and_records_it(self) -> None:
        """The --model selection reaches every attempt and the saved run."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            key = self._key(registry)
            question = "Energy is 20 kWh at 0.25 USD/kWh. What is the cost?"
            response = {"content": _proposal(key), "audit": {"model": "probe-m"}}
            with (
                patch(
                    "connected_models.workflows.live_request", return_value=response
                ) as request,
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, question, False, "probe-m")
            self.assertEqual(request.call_count, 1)
            self.assertEqual(request.call_args[0][3], "probe-m")
            self.assertEqual(run["status"], "completed")
            self.assertEqual(run["model"], "probe-m")

    def test_repair_stops_after_max_attempts(self) -> None:
        """A persistently broken proposal fails with the last error standing."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            key = self._key(registry)
            question = "Energy is 20 kWh at 0.25 USD/kWh. What is the cost?"
            bad = {"content": _proposal(key, "voltage"), "audit": {}}
            with (
                patch(
                    "connected_models.workflows.live_request",
                    side_effect=[bad, bad, bad, bad],
                ) as request,
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, question)
            self.assertEqual(request.call_count, 3)
            self.assertEqual(run["status"], "blocked")
            self.assertIn("undeclared input", run["error"])
            self.assertEqual(len(run["attempts"]), 3)

    def test_decline_is_terminal_without_retry(self) -> None:
        """A needs-input decline never spends a repair call."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            key = self._key(registry)
            declined = _proposal(key)
            declined["status"] = "needs-input"
            declined["reason"] = "Tariff unknown."
            response = {"content": declined, "audit": {}}
            with (
                patch(
                    "connected_models.workflows.live_request", return_value=response
                ) as request,
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(
                    registry, "Energy is 20 kWh at 0.25 USD/kWh. What is the cost?"
                )
            self.assertEqual(request.call_count, 1)
            self.assertEqual(run["status"], "needs-input")
            self.assertEqual(len(run["attempts"]), 1)

    def test_late_decline_gets_one_more_round(self) -> None:
        """A retreat to needs-input after a machine error is challenged once."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            key = self._key(registry)
            declined = _proposal(key)
            declined["status"] = "needs-input"
            declined["reason"] = "Conflicting statements."
            responses = [
                {"content": _proposal(key, "voltage"), "audit": {}},
                {"content": declined, "audit": {}},
                {"content": _proposal(key), "audit": {}},
            ]
            with (
                patch(
                    "connected_models.workflows.live_request", side_effect=responses
                ) as request,
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(
                    registry, "Energy is 20 kWh at 0.25 USD/kWh. What is the cost?"
                )
            self.assertEqual(request.call_count, 3)
            self.assertEqual(run["status"], "completed")
            self.assertEqual(len(run["attempts"]), 3)
            self.assertIn("undeclared input", run["attempts"][0]["error"])
