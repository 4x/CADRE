"""Grounding, typed extraction and missing-input behavior of question-only answering."""

import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from connected_models.contracts import ModelError
from connected_models.demo import RATE, YEARS
from connected_models.query_inputs import bind_fact, validate_fact
from connected_models.registry import Registry
from connected_models.workflows import (
    answer,
    compose_system_prompt,
    fill_in_assumptions_enabled,
    seed_candidates,
)
from tests.support import scratch_directory


class QueryTests(unittest.TestCase):
    """Inputs must come from the question, regardless of domain or parameter names."""

    def fact(
        self, literal: str, unit: str, quote: str, kind: str = "number"
    ) -> dict[str, Any]:
        """Construct an exact source-linked test assertion."""
        return {
            "id": "fact-a",
            "name": "user input",
            "value_type": kind,
            "value": literal,
            "unit": unit,
            "quote": quote,
        }

    def test_numbers_dates_and_text_are_preserved(self) -> None:
        """Fact validation accepts arbitrary subject matter independently of heating models."""
        question = "I have 12 apples. My birth date is 1990-02-03. My name is Pat."
        raw = [
            self.fact("12", "apple", "12 apples"),
            self.fact("1990-02-03", "date", "birth date is 1990-02-03", "date"),
            self.fact("Pat", "text", "name is Pat", "text"),
        ]
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
        for raw in (
            self.fact("5", "percent", "15 percent"),
            self.fact("3", "1", "3"),
            self.fact("0.15", "1", "15 percent"),
        ):
            with self.subTest(raw=raw), self.assertRaises(ModelError):
                validate_fact(raw, question)
        with self.assertRaisesRegex(ModelError, "invalid ISO"):
            validate_fact(
                self.fact("1990-02-30", "date", "1990-02-30", "date"), "1990-02-30"
            )

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

    def test_per_phrasing_reads_through_the_preposition(self) -> None:
        """'15 mg per kg' agrees with mg/kg instead of misreading as mg."""
        for literal, unit, quote in (
            ("15", "mg/kg", "15 mg per kg"),
            ("20", "mph", "20 miles per hour"),
            ("88", "ft/s", "88 feet per second"),
            ("250", "mg", "250 mg in 5 mL"),
        ):
            with self.subTest(quote=quote):
                fact = validate_fact(self.fact(literal, unit, quote), quote)
                self.assertEqual(fact["unit"], unit)
        with self.assertRaisesRegex(ModelError, "unit contradicts"):
            validate_fact(self.fact("15", "kg", "15 mg per kg"), "15 mg per kg")

    def test_ambiguous_question_is_saved_without_composition(self) -> None:
        """Conflicting user statements need clarification; no preset fills the gap."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            for candidate_id in seed_candidates(registry):
                registry.review(candidate_id, "test-reviewer", "Test-only admission.")
            response = {
                "content": {
                    "facts": [],
                    "issues": ["Which of the two prices should be used?"],
                    "status": "needs-input",
                    "graph": {"id": "ambiguous", "nodes": [], "outputs": []},
                    "reason": "Two prices conflict.",
                    "clarifications": ["Which of the two prices should be used?"],
                },
                "audit": {},
            }
            with (
                patch(
                    "connected_models.workflows.live_request", return_value=response
                ) as request,
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
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
            with (
                patch("connected_models.workflows.live_request") as request,
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, "")
            request.assert_not_called()
            self.assertEqual(run["status"], "blocked")
            self.assertIn("error", run)

    def test_assumed_facts_need_the_opt_in(self) -> None:
        """Implied values are rejected by default and accepted only when filling is enabled."""
        question = "Driving at constant 30 mph, how long to cover 100 miles?"
        raw = {
            "id": "fact-a",
            "name": "acceleration",
            "value_type": "number",
            "value": "0",
            "unit": "m/s^2",
            "quote": "constant 30 mph",
            "assumption": "Constant speed implies zero acceleration.",
        }
        with self.assertRaisesRegex(ModelError, "assumption filling"):
            validate_fact(raw, question)
        fact = validate_fact(raw, question, fill_in_assumptions=True)
        self.assertTrue(fact["assumed"])
        self.assertEqual(fact["amount"], 0)
        bad_quote = {**raw, "quote": "steady cruising"}
        with self.assertRaisesRegex(ModelError, "exact quote"):
            validate_fact(bad_quote, question, fill_in_assumptions=True)
        bad_value = {**raw, "value": "zero"}
        with self.assertRaisesRegex(ModelError, "digit literal"):
            validate_fact(bad_value, question, fill_in_assumptions=True)

    def test_quoted_facts_stay_strict_when_filling(self) -> None:
        """The opt-in adds assumed facts; it never loosens quoted-fact grounding."""
        question = "Use 15 percent."
        with self.assertRaises(ModelError):
            validate_fact(
                self.fact("5", "percent", "15 percent"),
                question,
                fill_in_assumptions=True,
            )
        fact = validate_fact(
            self.fact("15", "percent", "15 percent"), question, fill_in_assumptions=True
        )
        self.assertFalse(fact["assumed"])
        self.assertEqual(fact["assumption"], "")

    def test_fill_in_resolution_and_prompt_composition(self) -> None:
        """CLI flag or environment truthy values enable filling; prompt gains the section."""
        self.assertTrue(fill_in_assumptions_enabled(True, {}))
        self.assertTrue(
            fill_in_assumptions_enabled(False, {"FILL_IN_ASSUMPTIONS": "True"})
        )
        self.assertTrue(
            fill_in_assumptions_enabled(False, {"FILL_IN_ASSUMPTIONS": "1"})
        )
        self.assertFalse(fill_in_assumptions_enabled(False, {}))
        self.assertFalse(
            fill_in_assumptions_enabled(False, {"FILL_IN_ASSUMPTIONS": "false"})
        )
        self.assertFalse(
            fill_in_assumptions_enabled(False, {"FILL_IN_ASSUMPTIONS": ""})
        )
        strict = compose_system_prompt(False)
        filled = compose_system_prompt(True)
        self.assertNotIn("Assumption filling", strict)
        self.assertIn("Assumption filling", filled)
        self.assertTrue(filled.startswith(strict))

    def test_answered_run_records_its_assumptions(self) -> None:
        """An executed assumed binding is documented on the saved run record."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            for candidate_id in seed_candidates(registry):
                registry.review(candidate_id, "test-reviewer", "Test-only admission.")
            models, _ = registry.snapshot()
            key = next(name for name in models if "electricity-cost" in name)
            question = "Energy is 20 kWh. What is the cost?"
            proposal = {
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
                        "quote": "What is the cost?",
                        "assumption": "Illustrative tariff implied by the pricing question.",
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
                                {"input": "tariff", "source": "fact", "ref": "fact-t"},
                            ],
                        }
                    ],
                    "outputs": ["n1"],
                },
                "reason": "Direct model.",
                "clarifications": [],
            }
            response = {"content": proposal, "audit": {}}
            with (
                patch("connected_models.workflows.live_request", return_value=response),
                patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"),
            ):
                run = answer(registry, question, fill_in_assumptions=True)
            self.assertEqual(run["status"], "completed")
            self.assertEqual(run["outputs"]["n1"]["amount"], 5)
            self.assertTrue(run["fill_in_assumptions"])
            self.assertEqual(len(run["assumptions"]), 1)
            self.assertEqual(run["assumptions"][0]["fact"], "fact-t")
            self.assertIn("tariff", run["assumptions"][0]["assumption"])
