"""Dimensional mechanics, conversions, inversions and strict semantic bindings."""

from dataclasses import replace
from fractions import Fraction
import json
import math
import unittest

from connected_models.contracts import DIMENSIONLESS, MASS, TIME, Composition, Model, ModelError, Node, Port, UNITS, Value
from connected_models.expressions import dimensions, evaluate, parse
from connected_models.query_inputs import bind_fact, validate_fact
from connected_models.runtime import execute, validate_model


class MechanicsTests(unittest.TestCase):
    """Synthetic formula fixtures verify engineering support, not source auditing."""

    def model(self) -> Model:
        """Declare a bounded speed-to-energy fixture with an explicit inertial frame."""
        context = "test particle, frame A"
        return Model("synthetic-energy", "test1", {"m": Port("mass", "kg", context), "v": Port("speed", "m/s", context)},
            Port("translational_kinetic_energy", "J", context), "0.5 * m * v**2", ("m >= 0", "v >= 0"),
            "Synthetic engineering fixture", ("Test-only nonrelativistic particle.",))

    def test_dimensional_power_and_mixed_unit_conversion(self) -> None:
        """A known 80 kg, 36 km/h case returns 4000 J through canonical normalization."""
        model = self.model()
        context = model.output.context
        node = Node("energy", model.key, {"m": Value(80000, Port("mass", "g", context), "fixture", "test"),
                    "v": Value(36, Port("speed", "km/h", context), "fixture", "test")})
        result = execute(Composition("mixed-units", (node,), (node.id,)), {model.key: model})
        self.assertEqual(result["status"], "completed")
        self.assertAlmostEqual(result["outputs"][node.id]["amount"], 4000)
        self.assertEqual(UNITS["kWh"].scale, 1)
        self.assertEqual(UNITS["Wh"].scale, 0.001)
        self.assertEqual(UNITS["USD/kWh"].scale, 1)
        output_kwh = replace(model, output=replace(model.output, unit="kWh"))
        converted = execute(Composition("converted", (node,), (node.id,)), {model.key: output_kwh})
        self.assertAlmostEqual(converted["outputs"][node.id]["amount"], 4000 / 3600000)

    def test_physical_speed_inverse_retains_nonnegative_branch(self) -> None:
        """Inverse solver returns speed in declared units and applies original guards."""
        model = self.model()
        node = Node("speed", model.key, {"m": Value(80, model.inputs["m"], "fixture", "test"),
                    "__output__": Value(4, replace(model.output, unit="kJ"), "fixture", "test")}, solve_for="v")
        result = execute(Composition("inverse", (node,), (node.id,)), {model.key: model})
        self.assertEqual(result["status"], "completed", result.get("error"))
        self.assertAlmostEqual(result["outputs"][node.id]["amount"], 10)

    def test_bad_dimensions_powers_meanings_and_frames_are_rejected(self) -> None:
        """Same dimensions do not authorize a speed/velocity or frame conversion."""
        model = self.model()
        for expression in ("m * v", "m * v**0.5", "m * v**m"):
            with self.assertRaises(ModelError):
                validate_model(replace(model, expression=expression))
        for port in (Port("velocity", "m/s", model.output.context), Port("speed", "m/s", "frame B")):
            with self.assertRaises(ModelError):
                Value(10, port, "fixture", "test").bind(model.inputs["v"])
        with self.assertRaises(ModelError):
            Port("duration", "J", "test").validate()

    def test_rational_powers_close_fractional_dimensions(self) -> None:
        """A Kleiber-shaped B0*M**0.75 fixture validates, evaluates and serializes to JSON."""
        context = "test taxon, kcal/day"
        model = Model("synthetic-kleiber", "test1",
            {"B0": Port("metabolic_normalization", "kcal/day per kg^0.75", context),
             "M": Port("body_mass", "kg", context)},
            Port("basal_metabolic_rate", "kcal/day", context), "B0 * M ** 0.75", ("B0 > 0", "M > 0"),
            "Synthetic allometry fixture", ("Test-only rational-power shape.",))
        validate_model(model)
        node = Node("bmr", model.key, {"B0": Value(70, model.inputs["B0"], "fixture", "test"),
                    "M": Value(100, model.inputs["M"], "fixture", "test")})
        result = execute(Composition("kleiber", (node,), (node.id,)), {model.key: model})
        self.assertEqual(result["status"], "completed", result.get("error"))
        self.assertAlmostEqual(result["outputs"][node.id]["amount"], 2213.59, places=2)
        json.dumps(result, allow_nan=False)

    def test_rational_exponent_grammar_rules(self) -> None:
        """Exact rationals and integer ratios power dimensional bases; names and sloppy floats fail."""
        mass = {"M": MASS}
        self.assertEqual(dimensions(parse("M ** 0.75"), mass), (Fraction(3, 4), Fraction(0), Fraction(0), Fraction(0)))
        self.assertEqual(dimensions(parse("M ** (1/3)"), mass), (Fraction(1, 3), Fraction(0), Fraction(0), Fraction(0)))
        self.assertEqual(dimensions(parse("M ** 2"), mass), (Fraction(2), Fraction(0), Fraction(0), Fraction(0)))
        self.assertEqual(dimensions(parse("x ** N"), {"x": DIMENSIONLESS, "N": DIMENSIONLESS}), DIMENSIONLESS)
        for bad in ("M ** 0.1", "M ** z", "M ** 101", "M ** (1/1025)", "M ** (1/0)"):
            with self.assertRaises(ModelError, msg=bad):
                dimensions(parse(bad), {**mass, "z": DIMENSIONLESS})
        with self.assertRaises(ModelError):
            evaluate(parse("x ** 0.5"), {"x": -4.0})
        self.assertEqual(evaluate(parse("x ** 2"), {"x": -4.0}), 16.0)
        self.assertAlmostEqual(evaluate(parse("x ** 0.5"), {"x": 16.0}), 4.0)

    def test_scalar_functions_validate_dimensions_and_evaluate(self) -> None:
        """Doubling time log(2)/log(lam) executes end to end; sqrt halves dimensions."""
        mass = {"M": MASS}
        self.assertEqual(dimensions(parse("log(x)"), {"x": DIMENSIONLESS}), DIMENSIONLESS)
        self.assertEqual(dimensions(parse("exp(x)"), {"x": DIMENSIONLESS}), DIMENSIONLESS)
        self.assertEqual(dimensions(parse("sqrt(M)"), mass), (Fraction(1, 2), Fraction(0), Fraction(0), Fraction(0)))
        self.assertEqual(dimensions(parse("sum(a, b)"), {"a": MASS, "b": MASS}), MASS)
        self.assertEqual(evaluate(parse("log(2) / log(lam)"), {"lam": 1.5}), math.log(2) / math.log(1.5))
        context = "test fixture, doubling time"
        model = Model("synthetic-doubling", "test1", {"lam": Port("parallel_fraction", "1", context)},
            Port("overall_speedup", "1", context), "log(2) / log(lam)", ("lam > 1",),
            "Synthetic logarithm fixture", ("Test-only function shape.",))
        validate_model(model)
        node = Node("double", model.key, {"lam": Value(1.5, model.inputs["lam"], "fixture", "test")})
        result = execute(Composition("doubling", (node,), (node.id,)), {model.key: model})
        self.assertEqual(result["status"], "completed", result.get("error"))
        self.assertAlmostEqual(result["outputs"][node.id]["amount"], 1.70951129, places=6)
        json.dumps(result, allow_nan=False)

    def test_function_domain_and_grammar_errors(self) -> None:
        """Bad domains, arities, keywords, unknown functions and dimensional logs fail closed."""
        for bad_eval in ("log(0)", "log(-2)", "sqrt(-1)", "log(x, 2)", "sum()", "log(x=1)", "sin(x)", "x(2)"):
            with self.assertRaises(ModelError, msg=bad_eval):
                evaluate(parse(bad_eval), {"x": 4.0})
        for bad_dims in ("log(M)", "exp(M)", "sum(M, t)", "log(x, y)", "sum()", "pow(x, 2)"):
            with self.assertRaises(ModelError, msg=bad_dims):
                dimensions(parse(bad_dims), {"M": MASS, "t": TIME, "x": DIMENSIONLESS, "y": DIMENSIONLESS})
        self.assertAlmostEqual(evaluate(parse("exp(1)"), {}), 2.718281828, places=8)
        self.assertAlmostEqual(evaluate(parse("prod(2, 3, 4)"), {}), 24.0)
        self.assertAlmostEqual(evaluate(parse("sum(2, 3, 4)"), {}), 9.0)

    def test_query_units_are_grounded_and_aliases_bind(self) -> None:
        """Explicit physical units cannot be silently replaced during query parsing."""
        question = "A particle of mass 80 kilograms moves at 36 km/h."
        raw = {"id": "mass", "name": "mass", "value_type": "number", "value": "80", "unit": "kg", "quote": "mass 80 kilograms"}
        fact = validate_fact(raw, question)
        self.assertEqual(bind_fact(fact, self.model().inputs["m"]).amount, 80)
        with self.assertRaises(ModelError):
            validate_fact({**raw, "unit": "g"}, question)
        acceleration = {"id": "a", "name": "acceleration", "value_type": "number", "value": "2", "unit": "m/s^2", "quote": "2 m/s^2"}
        validate_fact(acceleration, "Acceleration is 2 m/s^2.")
        with self.assertRaises(ModelError):
            validate_fact({**acceleration, "unit": "m/s"}, "Acceleration is 2 m/s^2.")


if __name__ == "__main__":
    unittest.main()
