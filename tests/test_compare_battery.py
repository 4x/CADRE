"""Compare-battery sweep: table rows reduce sweep results honestly."""

import unittest

from connected_models.contracts import ModelError
from evals.run_compare_battery import (
    check_trap,
    resolve_models,
    score_head_to_head,
    summarize,
)


class CompareSweepTests(unittest.TestCase):
    """Rows carry battery verdicts, agreement, latencies, and links."""

    def test_row_keeps_both_verdicts_and_links(self) -> None:
        """Battery failures stay visible next to a passing agreement."""
        entry = {
            "id": "t1-x",
            "tier": 1,
            "expected_outputs": [
                {"meaning": "length", "unit": "m", "amount": 107.2896}
            ],
        }
        comparison = {
            "saved_path": "c.json",
            "grounded": {"status": "completed", "attempts": 2, "latency_s": 41.26},
            "direct": {"latency_s": 8.04},
            "agreement": {"verdict": "agree"},
        }
        battery = {
            "verdict": "fail",
            "failures": ["status 'blocked' != expected 'completed'"],
        }
        row = summarize(entry, comparison, battery, "probe-m")
        self.assertEqual(row["id"], "t1-x")
        self.assertEqual(row["battery"], "fail")
        self.assertEqual(row["agreement"], "agree")
        self.assertEqual(row["grounded_latency_s"], 41.3)
        self.assertEqual(row["direct_latency_s"], 8.0)
        self.assertEqual(row["battery_failures"], battery["failures"])
        self.assertEqual(row["comparison"], "c.json")

    def test_missing_direct_latency_stays_blank(self) -> None:
        """A failed direct route shows no direct latency instead of zero."""
        entry = {
            "id": "t1-x",
            "tier": 1,
            "expected_outputs": [
                {"meaning": "length", "unit": "m", "amount": 107.2896}
            ],
        }
        comparison = {
            "grounded": {"status": "completed", "attempts": 1, "latency_s": 30.0},
            "direct": {"latency_s": None},
            "agreement": {"verdict": "unjudged"},
        }
        row = summarize(entry, comparison, {"verdict": "pass", "failures": []}, None)
        self.assertIsNone(row["direct_latency_s"])
        self.assertEqual(row["battery"], "pass")

    def test_row_prefers_resolved_model_over_requested(self) -> None:
        """The row carries the model actually used, falling back to the request."""
        entry = {
            "id": "t1-x",
            "tier": 1,
            "expected_outputs": [
                {"meaning": "length", "unit": "m", "amount": 107.2896}
            ],
        }
        battery = {"verdict": "pass", "failures": []}
        resolved = {
            "model": "resolved-m",
            "grounded": {"status": "completed", "attempts": 1, "latency_s": 1.0},
            "direct": {"latency_s": 1.0},
            "agreement": {"verdict": "agree"},
        }
        self.assertEqual(
            summarize(entry, resolved, battery, "requested-m")["model"], "resolved-m"
        )
        bare = {
            "grounded": {"status": "blocked", "attempts": 1, "latency_s": 1.0},
            "direct": {"latency_s": None},
            "agreement": {"verdict": "unjudged"},
        }
        self.assertEqual(
            summarize(entry, bare, battery, "requested-m")["model"], "requested-m"
        )

    def test_resolve_models_dedupes_and_validates(self) -> None:
        """Empty means the configured model once; unknown names fail before any call."""
        self.assertEqual(resolve_models(""), [None])
        self.assertEqual(
            resolve_models("muse-spark-1.3, muse-spark-1.3"), ["muse-spark-1.3"]
        )
        with self.assertRaisesRegex(ModelError, "Unknown model 'nope-9' in --model"):
            resolve_models("muse-spark-1.3,nope-9")

    def test_head_to_head_win_tie_loss(self) -> None:
        """Only-grounded-right is a win; both-right a tie; grounded-wrong a loss."""
        entry = {
            "id": "a",
            "expected_outputs": [
                {"meaning": "length", "unit": "m", "amount": 107.2896}
            ],
        }
        win = score_head_to_head(entry, "pass", "completed", "about 95 m")
        self.assertEqual(
            (win["wtl"], win["grounded"], win["direct"]), ("win", "correct", "wrong")
        )
        tie = score_head_to_head(entry, "pass", "completed", "107.29 m")
        self.assertEqual(tie["wtl"], "tie")
        loss = score_head_to_head(entry, "fail", "completed", "107.29 m")
        self.assertEqual((loss["wtl"], loss["grounded"]), ("loss", "wrong"))

    def test_head_to_head_trap_needs_naive_match(self) -> None:
        """Quoted question figures are not an answer; the naive value is."""
        entry = {"id": "t", "trap": True, "naive_amounts": [-500.0]}
        win = score_head_to_head(entry, "pass", "rejected", "5/(0.08-0.09) = -500")
        self.assertEqual((win["wtl"], win["direct"]), ("win", "answered"))
        tie = score_head_to_head(
            entry,
            "pass",
            "rejected",
            "With D1=5, 8 percent and 9 percent, no finite price exists.",
        )
        self.assertEqual((tie["wtl"], tie["direct"]), ("tie", "refused"))
        loss = score_head_to_head(entry, "fail", "completed", "no finite price exists")
        self.assertEqual(loss["wtl"], "loss")

    def test_check_trap_refusal_passes(self) -> None:
        """Any non-completion passes a trap; only completion fails it."""
        entry = {"id": "t", "tier": 1}
        self.assertEqual(check_trap(entry, "rejected")["verdict"], "pass")
        self.assertEqual(check_trap(entry, "needs-input")["verdict"], "pass")
        failed = check_trap(entry, "completed")
        self.assertEqual(failed["verdict"], "fail")
        self.assertTrue(failed["failures"])
