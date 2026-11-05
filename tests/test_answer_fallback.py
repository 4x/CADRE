"""Grounded fallback: a failed grounded route returns a labeled direct answer."""

import unittest
from pathlib import Path
from unittest.mock import patch

from connected_models.contracts import ModelError
from connected_models.registry import Registry
from connected_models.workflows import answer

from .support import scratch_directory


class AnswerFallbackTests(unittest.TestCase):
    """Fallback states the grounded reason, then shows the plain LLM answer."""

    def test_fallback_returns_direct_text_with_reason(self) -> None:
        """Dead inference plus fallback yields a labeled direct answer."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            with (
                patch(
                    "connected_models.workflows.live_request",
                    side_effect=ModelError("down"),
                ),
                patch(
                    "connected_models.compare.direct_answer",
                    return_value={
                        "direct_text": "About 42.",
                        "inference": {"model": "probe-m"},
                    },
                ),
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, "What is the cost?", direct_fallback=True)
        self.assertEqual(run["status"], "blocked")
        self.assertEqual(run["fallback"]["direct_text"], "About 42.")
        self.assertEqual(run["fallback"]["model"], "probe-m")
        self.assertIn("blocked", run["fallback"]["reason"])

    def test_no_fallback_by_default(self) -> None:
        """Without opt-in the record carries no direct answer."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            with (
                patch(
                    "connected_models.workflows.live_request",
                    side_effect=ModelError("down"),
                ),
                patch(
                    "connected_models.compare.direct_answer",
                    side_effect=AssertionError("must not call direct"),
                ),
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, "What is the cost?")
        self.assertEqual(run["status"], "blocked")
        self.assertNotIn("fallback", run)

    def test_direct_failure_is_recorded_not_raised(self) -> None:
        """A dead direct route still reports the grounded reason."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            with (
                patch(
                    "connected_models.workflows.live_request",
                    side_effect=ModelError("down"),
                ),
                patch(
                    "connected_models.compare.direct_answer",
                    side_effect=ModelError("also down"),
                ),
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, "What is the cost?", direct_fallback=True)
        self.assertEqual(run["status"], "blocked")
        self.assertIn("blocked", run["fallback"]["reason"])
        self.assertEqual(run["fallback"]["direct_text"], "")
        self.assertIn("also down", run["fallback"]["error"])


if __name__ == "__main__":
    unittest.main()
