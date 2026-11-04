"""Dana's heat-pump quote: the judge-visible impact scenario stays exact.

Dana heats with resistance heating and holds a heat-pump install quote. The
base case reproduces her receipt (operating costs, annual saving, 10-year NPV)
and the pessimistic revision shows the same models flipping the decision, which
is why inspectable revision matters. See docs/impact.md.
"""

import unittest

from connected_models.demo import catalog, composition
from connected_models.runtime import execute

BASELINE_COST_USD = 3600.0
UPGRADE_COST_USD = 1200.0
ANNUAL_SAVING_USD = 2400.0
BASE_NPV_USD = 8532.16
PESSIMISTIC_NPV_USD = -417.40


def output_amount(operation: str, node: str, **overrides: float) -> float:
    """Execute one scripted heating scenario and return a single output amount."""
    manifest = execute(composition(**overrides, operation=operation), catalog())
    assert manifest["status"] == "completed"
    outputs = manifest.get("outputs", {})
    assert node in outputs
    return float(outputs[node]["amount"])


class ImpactScenarioTests(unittest.TestCase):
    """The impact narrative's figures match deterministic execution."""

    def test_base_case_receipt(self) -> None:
        """Dana's quoted case yields the documented costs, saving, and NPV."""
        self.assertEqual(
            output_amount("investment", "baseline-cost"), BASELINE_COST_USD
        )
        self.assertEqual(output_amount("investment", "upgrade-cost"), UPGRADE_COST_USD)
        self.assertEqual(
            output_amount("investment", "annual-savings"), ANNUAL_SAVING_USD
        )
        self.assertAlmostEqual(
            output_amount("investment", "investment-npv"), BASE_NPV_USD, places=2
        )

    def test_pessimistic_revision_flips_decision(self) -> None:
        """Lower performance and tariff plus a higher quote turn the NPV negative."""
        amount = output_amount(
            "investment",
            "investment-npv",
            performance=2.0,
            investment=12000.0,
            tariff=0.25,
        )
        self.assertAlmostEqual(amount, PESSIMISTIC_NPV_USD, places=2)
