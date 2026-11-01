"""Inverse views preserve original equations, domains, types and reviewed identity."""

from dataclasses import asdict, replace
from decimal import Decimal
import math
import unittest

from connected_models.contracts import Composition, Model, Node, Port, Value
from connected_models.demo import catalog
from connected_models.runtime import execute
from connected_models.solving import OUTPUT_BINDING

SCALAR = Port("seasonal_performance", "1", "algebra-fixture")


def polynomial(expression: str, guards: tuple[str, ...] = ()) -> Model:
    """Build a unitless algebra fixture, not a curated physical model."""
    return Model("polynomial", "1", {"x": SCALAR}, SCALAR, expression, guards,
                 "Synthetic algebra identity fixture", ("Unitless mathematical test only.",))


def inverse(model: Model, target: str, known: dict[str, float], output: float,
            relation: str = "equal") -> dict:
    """Execute one inverse instance with cited fixture input values."""
    bindings = {name: Value(value, model.inputs[name], "fixture", "Known test quantity") for name, value in known.items()}
    bindings[OUTPUT_BINDING] = Value(output, model.output, "fixture", "Requested original-output target")
    node = Node("inverse", model.key, bindings, target, relation)
    return execute(Composition("inverse-case", (node,), (node.id,)), {model.key: model})


class SolvingTests(unittest.TestCase):
    """Use independent expected algebra/cash flows, including pathological domains."""

    def test_reuse_original_relation_both_input_directions(self) -> None:
        """One division model recovers either heat or performance without new definitions."""
        model = catalog()["heat-to-electricity@1"]
        snapshot = asdict(model)
        heat = inverse(model, "heat", {"performance": 3}, 4000)
        performance = inverse(model, "performance", {"heat": 12000}, 4000)
        self.assertEqual(heat["outputs"]["inverse"]["amount"], 12000)
        self.assertEqual(performance["outputs"]["inverse"]["amount"], 3)
        self.assertEqual(performance["outputs"]["inverse"]["port"]["meaning"], "seasonal_performance")
        self.assertEqual(asdict(model), snapshot)
        self.assertEqual(set(heat["models"]), {model.key})

    def test_inverse_units_convert_known_and_return_target_unit(self) -> None:
        """A solved output uses the original unknown's unit, not the original result unit."""
        model = catalog()["electricity-cost@1"]
        result = inverse(model, "tariff", {"energy": 20}, 5)
        self.assertEqual(result["outputs"]["inverse"]["amount"], 0.25)
        self.assertEqual(result["outputs"]["inverse"]["port"]["unit"], "USD/kWh")

    def test_multiple_branches_and_guard_selected_branch(self) -> None:
        """A quadratic has both signs unless a source domain excludes one."""
        ambiguous = inverse(polynomial("x ** 2"), "x", {}, 4)
        self.assertEqual(ambiguous["solve_diagnostic"]["code"], "multiple_solutions")
        self.assertEqual(ambiguous["solve_diagnostic"]["candidates"], [-2, 2])
        positive = inverse(polynomial("x ** 2", ("x > 0",)), "x", {}, 4)
        negative = inverse(polynomial("x ** 2", ("x < 0",)), "x", {}, 4)
        self.assertEqual(positive["outputs"]["inverse"]["amount"], 2)
        self.assertEqual(negative["outputs"]["inverse"]["amount"], -2)

    def test_energy_mass_relation_as_unitless_algebra(self) -> None:
        """E=m*c² yields m and both c branches; no SI vocabulary coverage is implied."""
        model = Model("energy-algebra", "1", {"m": SCALAR, "c": SCALAR}, SCALAR,
                      "m * c ** 2", (), "Synthetic unitless formula fixture", ("Not a physical model admission.",))
        mass = inverse(model, "m", {"c": 3}, 18)
        speed = inverse(model, "c", {"m": 2}, 18)
        self.assertEqual(mass["outputs"]["inverse"]["amount"], 2)
        self.assertEqual(speed["solve_diagnostic"]["candidates"], [-3, 3])

    def test_no_real_solution_and_repeated_root(self) -> None:
        """Negative discriminants reject; a repeated real root is one solution."""
        missing = inverse(polynomial("x ** 2"), "x", {}, -1)
        self.assertEqual(missing["solve_diagnostic"]["code"], "no_admissible_solution")
        repeated = inverse(polynomial("(x - 3) ** 2"), "x", {}, 0)
        self.assertEqual(repeated["outputs"]["inverse"]["amount"], 3)

    def test_original_denominator_excludes_extraneous_root(self) -> None:
        """Cross multiplication must never admit a point where the original equation fails."""
        result = inverse(polynomial("x / x"), "x", {}, 2)
        self.assertEqual(result["solve_diagnostic"]["code"], "no_admissible_solution")

    def test_underdetermined_and_inconsistent_known_values(self) -> None:
        """An identity does not identify an unknown; inconsistent equations have no root."""
        identity = inverse(polynomial("x - x"), "x", {}, 0)
        inconsistent = inverse(polynomial("x - x"), "x", {}, 1)
        self.assertEqual(identity["solve_diagnostic"]["code"], "underdetermined")
        self.assertEqual(inconsistent["solve_diagnostic"]["code"], "no_admissible_solution")

    def test_unsupported_degree_and_unknown_exponent(self) -> None:
        """The limited solver reports unsupported forms rather than making up a result."""
        cubic = inverse(polynomial("x ** 3"), "x", {}, 8)
        exponential = inverse(polynomial("2 ** x"), "x", {}, 8)
        self.assertEqual(cubic["solve_diagnostic"]["code"], "unsupported_degree")
        self.assertEqual(exponential["solve_diagnostic"]["code"], "unsupported_expression")

    def test_fractional_power_rejects_unknown_base_but_solves_linear_factor(self) -> None:
        """B0*M**0.75 inverts exactly for B0 and reports unsupported_degree for M."""
        model = Model("kleiber-algebra", "1", {"B0": SCALAR, "M": SCALAR}, SCALAR, "B0 * M ** 0.75",
                      ("B0 > 0", "M > 0"), "Synthetic allometry fixture", ("Unitless mathematical test only.",))
        target = 70 * 100 ** 0.75
        factor = inverse(model, "B0", {"M": 100}, target)
        self.assertEqual(factor["status"], "completed", factor.get("error"))
        self.assertAlmostEqual(factor["outputs"]["inverse"]["amount"], 70)
        base = inverse(model, "M", {"B0": 70}, target)
        self.assertEqual(base["solve_diagnostic"]["code"], "unsupported_degree")

    def test_function_calls_are_forward_only(self) -> None:
        """B0*log(M) inverts exactly for B0 and reports unsupported_expression for M."""
        model = Model("log-algebra", "1", {"B0": SCALAR, "M": SCALAR}, SCALAR, "B0 * log(M)",
                      ("B0 > 0", "M > 0"), "Synthetic logarithm fixture", ("Unitless mathematical test only.",))
        target = 3 * math.log(10)
        factor = inverse(model, "B0", {"M": 10}, target)
        self.assertEqual(factor["status"], "completed", factor.get("error"))
        self.assertAlmostEqual(factor["outputs"]["inverse"]["amount"], 3)
        base = inverse(model, "M", {"B0": 3}, target)
        self.assertEqual(base["solve_diagnostic"]["code"], "unsupported_expression")

    def test_discounted_payback_searches_model_domain(self) -> None:
        """The first year meeting investment follows independently summed cash flows."""
        model = catalog()["uniform-present-value@1"]
        result = inverse(model, "years", {"annual": 2400, "rate": 0.05}, 10000, "at_least")
        self.assertEqual(result["outputs"]["inverse"]["amount"], 5)
        before = sum(Decimal(2400) / Decimal("1.05") ** year for year in range(1, 5))
        at = before + Decimal(2400) / Decimal("1.05") ** 5
        self.assertLess(before, Decimal(10000))
        self.assertGreaterEqual(at, Decimal(10000))
        self.assertEqual(result["steps"][0]["solve"]["domain"], [1, 100])
        self.assertEqual(result["steps"][0]["solve"]["evaluations"], 5)

    def test_no_crossing_is_limited_to_declared_domain(self) -> None:
        """A bounded failure does not claim that no solution exists outside the bounds."""
        model = catalog()["uniform-present-value@1"]
        result = inverse(model, "years", {"annual": 2400, "rate": 0.05}, 50000, "at_least")
        self.assertEqual(result["solve_diagnostic"]["code"], "no_crossing_in_domain")
        self.assertIn("not a claim", result["error"])

    def test_threshold_requires_declared_finite_bounds(self) -> None:
        """Search bounds come from the model, never an invented user horizon."""
        model = replace(catalog()["uniform-present-value@1"], guards=("rate > 0", "years > 0"))
        result = inverse(model, "years", {"annual": 2400, "rate": 0.05}, 10000, "at_least")
        self.assertEqual(result["solve_diagnostic"]["code"], "unbounded_search")

    def test_linear_integer_equality_needs_no_search_horizon(self) -> None:
        """An analytically solvable integer target must not demand arbitrary search bounds."""
        years = catalog()["uniform-present-value@1"].inputs["years"]
        model = Model("integer-linear", "1", {"years": years}, SCALAR, "2 * years", (),
                      "Synthetic integer fixture", ("Unitless algebra with integer input.",))
        run = inverse(model, "years", {}, 10)
        self.assertEqual(run["outputs"]["inverse"]["amount"], 5)
        self.assertEqual(run["steps"][0]["solve"]["method"], "rational-polynomial")

    def test_nonmonotone_threshold_search_returns_first_crossing(self) -> None:
        """Enumeration must not assume that model output increases over the domain."""
        years = catalog()["uniform-present-value@1"].inputs["years"]
        model = Model("hump", "1", {"years": years}, SCALAR, "years * (10 - years)",
                      ("years >= 1", "years <= 9"), "Synthetic nonmonotone fixture", ("Finite integer domain only.",))
        run = inverse(model, "years", {}, 20, "at_least")
        self.assertEqual(run["outputs"]["inverse"]["amount"], 3)

    def test_stable_quadratic_small_root(self) -> None:
        """A large linear coefficient must not erase a small admissible root."""
        run = inverse(polynomial("x ** 2 + 100000000 * x + 1", ("x > -1",)), "x", {}, 0)
        self.assertAlmostEqual(run["outputs"]["inverse"]["amount"], -1e-8, places=15)

    def test_integer_equality_can_be_non_unique(self) -> None:
        """Integer equality returns ambiguity instead of silently choosing the first year."""
        model = catalog()["uniform-present-value@1"]
        result = inverse(model, "years", {"annual": 0, "rate": 0.05}, 0)
        self.assertEqual(result["solve_diagnostic"]["code"], "multiple_solutions")

    def test_guards_on_known_inputs_are_not_lost(self) -> None:
        """Inversion still enforces rate and performance domains from the source."""
        result = inverse(catalog()["heat-to-electricity@1"], "heat", {"performance": 0}, 4000)
        self.assertEqual(result["status"], "rejected")
        self.assertFalse(result["outputs"])

    def test_inverse_node_can_feed_a_forward_node(self) -> None:
        """Compiler edges must use the solved variable's port, not the source result port."""
        from connected_models.contracts import Reference
        model = catalog()["heat-to-electricity@1"]
        heat = Value(12000, model.inputs["heat"], "fixture", "known heat")
        electricity = Value(4000, model.output, "fixture", "known electricity")
        nodes = (Node("inferred-performance", model.key, {"heat": heat, OUTPUT_BINDING: electricity}, "performance"),
                 Node("reuse-performance", model.key, {"heat": heat, "performance": Reference("inferred-performance")}))
        run = execute(Composition("inverse-forward", nodes, ("reuse-performance",)), {model.key: model})
        self.assertEqual(run["status"], "completed", run.get("error"))
        self.assertEqual(run["outputs"]["reuse-performance"]["amount"], 4000)

    def test_literal_constant_is_not_a_solve_target(self) -> None:
        """A curator's embedded constant cannot silently become a free variable."""
        model = polynomial("2 * x")
        node = Node("constant", model.key, {"x": Value(3, SCALAR, "fixture", "known input"),
                    OUTPUT_BINDING: Value(6, SCALAR, "fixture", "known result")}, "constant")
        run = execute(Composition("fixed-constant", (node,), (node.id,)), {model.key: model})
        self.assertEqual(run["status"], "rejected")
        self.assertIn("declared model input", run["error"])

    def test_overflow_cannot_be_reported_as_no_crossing(self) -> None:
        """Unverifiable earlier points must stop a threshold claim, not be silently skipped."""
        years = catalog()["uniform-present-value@1"].inputs["years"]
        model = Model("overflow", "1", {"years": years}, SCALAR, "(1e200) ** years",
                      ("years >= 1", "years <= 3"), "Synthetic numerical-limit fixture", ("No overflow claims.",))
        run = inverse(model, "years", {}, 1e300, "at_least")
        self.assertEqual(run["solve_diagnostic"]["code"], "numerical_limit")
        self.assertFalse(run["outputs"])
