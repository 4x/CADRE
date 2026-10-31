"""Dimensional mechanics, conversions, inversions and strict semantic bindings."""

from dataclasses import replace
import unittest

from connected_models.contracts import Composition, Model, ModelError, Node, Port, UNITS, Value
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
