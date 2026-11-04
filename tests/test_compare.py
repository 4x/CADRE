"""Grounded-vs-direct comparison: agreement logic and record shape."""

import unittest
from unittest.mock import patch

from connected_models.compare import compare, extract_numbers, numeric_agreement


def _grounded(status: str, outputs: dict | None = None) -> dict:
    """Build a minimal grounded record for agreement testing."""
    return {"run_id": "g", "status": status, "outputs": outputs or {},
            "assumptions": [], "attempts": [{"attempt": 1}], "error": None,
            "saved_path": "g.json"}


def _output(amount: float, unit: str = "m", meaning: str = "length") -> dict:
    """Build one executed output in the saved-run shape."""
    return {"amount": amount, "port": {"unit": unit, "meaning": meaning}}


class CompareTests(unittest.TestCase):
    """Agreement is one-sided: the engine is the oracle, prose is matched."""

    def test_numbers_come_out_of_prose(self) -> None:
        """Commas and decimals parse; surrounding words are ignored."""
        self.assertEqual(extract_numbers("About 1,200.5 m, or 3 ft."), [1200.5, 3.0])
        self.assertEqual(extract_numbers("no numbers here"), [])

    def test_agreement_matches_exact_and_percent_phrasing(self) -> None:
        """0.0485 matches 0.0485 and 4.85; anything else disagrees."""
        grounded = _grounded("completed", {"n1": _output(107.2896)})
        self.assertEqual(numeric_agreement(grounded, "107.29 m")["verdict"], "agree")
        ratio = _grounded("completed", {"n1": _output(0.04854, "1", "rate")})
        self.assertEqual(numeric_agreement(ratio, "4.854 percent")["verdict"], "agree")
        verdict = numeric_agreement(grounded, "about 95 m")
        self.assertEqual(verdict["verdict"], "disagree")
        self.assertIsNone(verdict["details"][0]["matched"])

    def test_closest_number_wins_over_first_in_tolerance(self) -> None:
        """A loose intermediate (0.05) must not shadow the exact value."""
        ratio = _grounded("completed", {"n1": _output(0.04854, "1", "rate")})
        verdict = numeric_agreement(ratio, "= 0.05 / 1.03 = 0.04854")
        self.assertEqual(verdict["verdict"], "agree")
        self.assertEqual(verdict["details"][0]["matched"], 0.04854)

    def test_unit_words_convert_through_registry_scales(self) -> None:
        """6.6 mL matches 6.6e-6 m^3; 352 ft matches 107.29 m."""
        dose = _grounded("completed", {"n2": _output(6.6e-06, "m^3", "volume")})
        verdict = numeric_agreement(dose, "330 mg = 6.6 mL")
        self.assertEqual(verdict["verdict"], "agree")
        self.assertEqual(verdict["details"][0]["matched"], 6.6)
        length = _grounded("completed", {"n1": _output(107.2896)})
        self.assertEqual(numeric_agreement(length, "352 ft")["verdict"], "agree")

    def test_wrong_dimension_and_wrong_percent_disagree(self) -> None:
        """Seconds never match meters; the 5% Fisher trap stays a miss."""
        length = _grounded("completed", {"n1": _output(107.2896)})
        self.assertEqual(numeric_agreement(length, "8 seconds")["verdict"], "disagree")
        ratio = _grounded("completed", {"n1": _output(0.04854, "1", "rate")})
        self.assertEqual(numeric_agreement(ratio, "5 percent")["verdict"], "disagree")
        self.assertEqual(numeric_agreement(ratio, "about 5")["verdict"], "disagree")

    def test_agreement_requires_every_branch_root(self) -> None:
        """A branch-all oracle agrees only when the prose names all roots."""
        both = _grounded("completed", {"n1": {"amounts": [1.0, 3.0],
                                              "port": {"unit": "1", "meaning": "root"}}})
        self.assertEqual(numeric_agreement(both, "roots are 1 and 3")["verdict"], "agree")
        partial = numeric_agreement(both, "the root is 3")
        self.assertEqual(partial["verdict"], "disagree")
        self.assertIsNone(partial["details"][0]["matched"])

    def test_blocked_grounded_runs_are_unjudged(self) -> None:
        """Without oracle outputs there is nothing to compare against."""
        verdict = numeric_agreement(_grounded("rejected"), "107.29 m")
        self.assertEqual(verdict["verdict"], "unjudged")

    def test_compare_records_both_routes(self) -> None:
        """The comparison saves grounded and direct runs with an agreement."""
        grounded = _grounded("completed", {"n1": _output(107.2896)})
        direct = {"run_id": "d", "created": "now", "question": "q",
                  "direct_text": "107.29 m", "inference": {}}
        with patch("connected_models.compare.answer", return_value=grounded) as grounded_call, \
                patch("connected_models.compare.direct_answer", return_value=direct), \
                patch("connected_models.compare.save_run", return_value="c.json") as saved:
            record = compare(object(), "How far?")
        self.assertEqual(grounded_call.call_count, 1)
        self.assertEqual(record["grounded"]["status"], "completed")
        self.assertEqual(record["direct"]["run_id"], "d")
        self.assertEqual(record["agreement"]["verdict"], "agree")
        self.assertEqual(saved.call_count, 2)
        self.assertEqual(record["saved_path"], "c.json")

    def test_direct_failure_keeps_the_grounded_result(self) -> None:
        """A dead direct route degrades to unjudged instead of failing."""
        from connected_models.contracts import ModelError
        grounded = _grounded("completed", {"n1": _output(107.2896)})
        with patch("connected_models.compare.answer", return_value=grounded), \
                patch("connected_models.compare.direct_answer", side_effect=ModelError("down")), \
                patch("connected_models.compare.save_run", return_value="c.json"):
            record = compare(object(), "How far?")
        self.assertEqual(record["direct"]["error"], "down")
        self.assertEqual(record["agreement"]["verdict"], "unjudged")

    def test_model_threads_to_both_routes_and_record(self) -> None:
        """One --model selection drives grounded and direct runs alike."""
        registry = object()
        grounded = {**_grounded("completed", {"n1": _output(107.2896)}), "model": "probe-m"}
        direct = {"run_id": "d", "created": "now", "question": "q",
                  "direct_text": "107.29 m", "inference": {"model": "probe-m"}}
        with patch("connected_models.compare.answer", return_value=grounded) as grounded_call, \
                patch("connected_models.compare.direct_answer", return_value=direct) as direct_call, \
                patch("connected_models.compare.save_run", return_value="c.json"):
            record = compare(registry, "How far?", False, "probe-m")
        grounded_call.assert_called_once_with(registry, "How far?", False, "probe-m")
        direct_call.assert_called_once_with("How far?", "probe-m")
        self.assertEqual(record["model"], "probe-m")

    def test_record_model_falls_back_to_direct_audit(self) -> None:
        """A grounded run without audits still records the direct route's model."""
        grounded = _grounded("rejected")
        direct = {"run_id": "d", "created": "now", "question": "q",
                  "direct_text": "107.29 m", "inference": {"model": "probe-m"}}
        with patch("connected_models.compare.answer", return_value=grounded), \
                patch("connected_models.compare.direct_answer", return_value=direct), \
                patch("connected_models.compare.save_run", return_value="c.json"):
            record = compare(object(), "How far?")
        self.assertEqual(record["model"], "probe-m")
