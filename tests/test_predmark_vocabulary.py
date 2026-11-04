"""Prediction-market vocabulary extension: meanings and projection closure."""

import json
import unittest
from pathlib import Path
from typing import Any

from connected_models.contracts import DIMENSIONLESS, MONEY, Dimensions
from connected_models.contracts import MEANINGS as MEANING_TABLE
from connected_models.integration import project_record

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "data/curation/reviews"

# Every meaning added by the predmark-1 batch with its exact dimensions.
NEW_MEANINGS: dict[str, Dimensions] = {
    "binary_contract_payoff": MONEY,
    "kelly_net_odds": DIMENSIONLESS,
    "kelly_wealth_fraction": DIMENSIONLESS,
    "event_probability": DIMENSIONLESS,
    "complement_event_probability": DIMENSIONLESS,
    "conditional_event_probability": DIMENSIONLESS,
    "conditioning_event_probability": DIMENSIONLESS,
    "joint_event_probability": DIMENSIONLESS,
}

# Bundle, report and model id for every recommend-admit predmark record.
ADMITTABLES: tuple[tuple[str, str, str], ...] = (
    (
        "predmark-binary-ev-bundle.json",
        "predmark-binary-ev-review.json",
        "financial-analysis--binary-event-discounted-fair-value",
    ),
    (
        "predmark-kelly-bundle.json",
        "predmark-kelly-review.json",
        "financial-analysis--kelly-optimal-fraction-simple-bet",
    ),
    (
        "predmark-probability-r3-bundle.json",
        "predmark-probability-r3-review.json",
        "financial-analysis--probability-complement",
    ),
    (
        "predmark-probability-r3-bundle.json",
        "predmark-probability-r3-review.json",
        "financial-analysis--conditional-probability",
    ),
)


def _load_json(path: Path) -> dict[str, Any]:
    """Read a committed JSON artifact as UTF-8 without mutation."""
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


class PredmarkVocabularyTests(unittest.TestCase):
    """The predmark-1 batch is exact, closed, and conservatively bound."""

    def test_new_meanings_carry_exact_dimensions(self) -> None:
        """All 8 added meanings pin the dimensions the records need."""
        self.assertEqual(len(NEW_MEANINGS), 8)
        for meaning, dims in NEW_MEANINGS.items():
            with self.subTest(meaning=meaning):
                self.assertIn(meaning, MEANING_TABLE)
                self.assertEqual(MEANING_TABLE[meaning], dims)

    def test_payoff_is_money_and_probabilities_are_dimensionless(self) -> None:
        """Money stays money; odds and probabilities never gain dimensions."""
        self.assertEqual(MEANING_TABLE["binary_contract_payoff"], MONEY)
        for meaning in (
            "kelly_net_odds",
            "kelly_wealth_fraction",
            "event_probability",
            "complement_event_probability",
            "conditional_event_probability",
            "conditioning_event_probability",
            "joint_event_probability",
        ):
            with self.subTest(meaning=meaning):
                self.assertEqual(MEANING_TABLE[meaning], DIMENSIONLESS)

    def test_admittables_project_without_diagnostics(self) -> None:
        """Every recommend-admit predmark record stages cleanly."""
        for bundle_name, report_name, model_id in ADMITTABLES:
            with self.subTest(model=model_id):
                bundle = _load_json(REVIEWS / bundle_name)
                report = _load_json(REVIEWS / report_name)
                revision = next(
                    item["revision"]
                    for item in bundle["models"]
                    if item["id"] == model_id
                )
                payload = project_record(
                    bundle, report, model_id, f"{revision}.runtime1"
                )
                self.assertEqual(payload["intake_blockers"], [])
                self.assertIn(
                    "predmark-1",
                    payload["evidence"]["projection"]["profile"],
                )


if __name__ == "__main__":
    unittest.main()
