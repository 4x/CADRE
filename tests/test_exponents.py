"""Exponent cap split: evaluation allows 500, dimensional powers stay at 100."""

import unittest

from connected_models.contracts import MASS, Model
from connected_models.contracts import ModelError, NumericalError
from connected_models.demo import catalog
from connected_models.expressions import dimensions, evaluate, parse
from tests.test_solving import SCALAR, inverse

MORTGAGE_ORACLE = 1798.6515754582572
RETIRE_ORACLE = 1312406.6991666663
CANCEL_ORACLE = 0.0005001247707110733


class ExponentCapTests(unittest.TestCase):
    """The eval cap unlocks monthly schedules; physics and overflow stay fenced."""

    def test_eval_boundary_accepts_500_rejects_501(self) -> None:
        """Dimensionless powers evaluate through the new cap, then fail closed."""
        big = evaluate(parse("x ** n"), {"x": 1.01, "n": 500}, {}, {})
        self.assertTrue(140.0 < big < 150.0)
        small = evaluate(parse("x ** n"), {"x": 1.01, "n": -500}, {}, {})
        self.assertTrue(0.006 < small < 0.008)
        with self.assertRaisesRegex(NumericalError, "magnitude 500"):
            evaluate(parse("x ** n"), {"x": 1.01, "n": 501}, {}, {})

    def test_dimensional_cap_stays_at_100(self) -> None:
        """Physical dimension vectors keep the old fence."""
        mass = {"M": MASS}
        with self.assertRaisesRegex(ModelError, "at most 100"):
            dimensions(parse("M ** 101"), mass)
        with self.assertRaisesRegex(ModelError, "at most 100"):
            dimensions(parse("M ** 500"), mass)

    def test_monthly_mortgage_oracle(self) -> None:
        """30-year monthly payment matches the Decimal oracle to the cent."""
        amount = evaluate(parse("P*i*(1+i)**n/((1+i)**n - 1)"),
                          {"P": 300000.0, "i": 0.005, "n": 360}, {}, {})
        self.assertAlmostEqual(amount, MORTGAGE_ORACLE, places=2)

    def test_monthly_retirement_oracle(self) -> None:
        """40-year monthly annuity matches the Decimal oracle to the cent."""
        amount = evaluate(parse("A*((1+i)**n - 1)/i"),
                          {"A": 500.0, "i": 0.07 / 12, "n": 480}, {}, {})
        self.assertAlmostEqual(amount, RETIRE_ORACLE, places=0)

    def test_cancellation_pattern_regressed(self) -> None:
        """(1+i)**n - 1 at tiny i is the precision-sensitive shape to watch."""
        amount = evaluate(parse("(1+i)**n - 1"), {"i": 1e-6, "n": 500}, {}, {})
        self.assertAlmostEqual(amount / CANCEL_ORACLE, 1.0, places=6)

    def test_overflow_still_fail_closed(self) -> None:
        """Huge bases still raise instead of leaking inf."""
        with self.assertRaises(NumericalError):
            evaluate(parse("x ** n"), {"x": 1e200, "n": 500}, {}, {})

    def test_threshold_search_covers_500_domain(self) -> None:
        """Bounded-integer search evaluates through the raised cap."""
        years = catalog()["uniform-present-value@1"].inputs["years"]
        model = Model("growth500", "1", {"years": years}, SCALAR,
                      "100 * (1.01 ** years)", ("years >= 1", "years <= 500"),
                      "Synthetic wide-domain fixture", ("Finite integer domain only.",))
        run = inverse(model, "years", {}, 14000, "at_least")
        self.assertEqual(run["outputs"]["inverse"]["amount"], 497)
