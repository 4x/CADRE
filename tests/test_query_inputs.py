"""Grounding, typed extraction and missing-input behavior of question-only answering."""

from pathlib import Path
import unittest
from unittest.mock import patch

from connected_models.contracts import ModelError
from connected_models.demo import RATE, YEARS
from connected_models.query_inputs import bind_fact, validate_fact
from connected_models.registry import Registry
from connected_models.workflows import answer, seed_candidates
from test_support import scratch_directory


class QueryTests(unittest.TestCase):
    """Inputs must come from the question, regardless of domain or parameter names."""

    def fact(self, literal: str, unit: str, quote: str, kind: str = "number") -> dict:
        """Construct an exact source-linked test assertion."""
        return {"id": "fact-a", "name": "user input", "value_type": kind,
                "value": literal, "unit": unit, "quote": quote}

    def test_numbers_dates_and_text_are_preserved(self) -> None:
        """Fact validation accepts arbitrary subject matter independently of heating models."""
        question = "I have 12 apples. My birth date is 1990-02-03. My name is Pat."
        raw = [self.fact("12", "apple", "12 apples"), self.fact("1990-02-03", "date", "birth date is 1990-02-03", "date"),
               self.fact("Pat", "text", "name is Pat", "text")]
        for index, fact in enumerate(raw):
            fact["id"] = f"input-{index}"
        facts = [validate_fact(item, question) for item in raw]
        self.assertEqual(facts[0]["amount"], 12)
        self.assertEqual(facts[1]["value"], "1990-02-03")
        self.assertEqual(facts[2]["value"], "Pat")
        with self.assertRaisesRegex(ModelError, "date inputs cannot execute"):
            bind_fact(facts[1], YEARS)

    def test_literal_and_quote_grounding(self) -> None:
        """Reject a fabricated value, altered quote and partial numeric match."""
        question = "Use 15 percent."
        for raw in (self.fact("5", "percent", "15 percent"), self.fact("3", "1", "3"),
                    self.fact("0.15", "1", "15 percent")):
            with self.subTest(raw=raw), self.assertRaises(ModelError):
                validate_fact(raw, question)
        with self.assertRaisesRegex(ModelError, "invalid ISO"):
            validate_fact(self.fact("1990-02-30", "date", "1990-02-30", "date"), "1990-02-30")

    def test_percent_and_periods_use_explicit_units(self) -> None:
        """Keep a user percentage intact and let the unit layer perform conversion."""
        rate = validate_fact(self.fact("5", "percent", "5 percent"), "Use 5 percent.")
        self.assertEqual(bind_fact(rate, RATE).bind(RATE), 0.05)
        years = validate_fact(self.fact("10", "years", "10 years"), "Use 10 years.")
        self.assertEqual(bind_fact(years, YEARS).bind(YEARS), 10)
        unknown = validate_fact(self.fact("10", "not-specified", "10"), "10")
        with self.assertRaisesRegex(ModelError, "unspecified or unsupported"):
            bind_fact(unknown, YEARS)
        with self.assertRaisesRegex(ModelError, "unit contradicts"):
            validate_fact(self.fact("5", "1", "5 percent"), "5 percent")
        with self.assertRaisesRegex(ModelError, "unit contradicts"):
            validate_fact(self.fact("0.30", "USD", "0.30 USD/kWh"), "0.30 USD/kWh")

    def test_ambiguous_question_is_saved_without_composition(self) -> None:
        """Conflicting user statements need clarification; no preset fills the gap."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            for candidate_id in seed_candidates(registry):
                registry.review(candidate_id, "test-reviewer", "Test-only admission.")
            response = {"content": {"facts": [], "issues": ["Which of the two prices should be used?"],
                        "status": "needs-input", "graph": {"id": "ambiguous", "nodes": [], "outputs": []},
                        "reason": "Two prices conflict.", "clarifications": ["Which of the two prices should be used?"]}, "audit": {}}
            with patch("connected_models.workflows.live_request", return_value=response) as request, patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"):
                run = answer(registry, "Use $100 or $200 as the price.")
            self.assertEqual(run["status"], "needs-input")
            self.assertFalse(run["outputs"])
            self.assertTrue(run["clarifications"])
            self.assertEqual(request.call_count, 1)
            self.assertTrue(Path(run["saved_path"]).is_file())

    def test_empty_question_never_calls_model(self) -> None:
        """There are no hidden defaults even before extraction begins."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            with patch("connected_models.workflows.live_request") as request, patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"):
                run = answer(registry, "")
            request.assert_not_called()
            self.assertEqual(run["status"], "blocked")
            self.assertIn("error", run)
