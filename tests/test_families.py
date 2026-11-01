"""Index-family inputs: aggregation over bound element tuples with shared ports."""

from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import unittest

from connected_models.contracts import DIMENSIONLESS, JOULES_PER_KWH, MASS, Composition, Family, Model, ModelError, Node, Port, Reference, Value
from connected_models.expressions import dimensions, evaluate, parse
from connected_models.reports import write_report
from connected_models.runtime import execute, save_run, validate_model
from connected_models.serialization import composition_from_dict, model_digest, model_from_dict
from test_support import scratch_directory


def total_mass_model() -> Model:
    """Declare a total-mass fixture summing one mass family with at least two legs."""
    context = "test fixture, summed parts"
    return Model("synthetic-total", "test1", {}, Port("mass", "kg", context), "sum(x)", ("len(x) >= 2",),
                 "Synthetic family fixture", ("Test-only aggregation shape.",), "fixture",
                 {"x": Family("mass", "kg", context, 4)})


def element(amount: float, unit: str = "kg") -> Value:
    """Build one attributed family element value."""
    return Value(amount, Port("mass", unit, "test fixture, summed parts"), "fixture", "test")


class FamilyTests(unittest.TestCase):
    """Families aggregate explicit element tuples; every element keeps its attribution."""

    def test_sum_over_mixed_unit_elements_with_len_guard(self) -> None:
        """80 kg plus 20000 g total 100 kg; the guard and the manifest survive JSON."""
        model = total_mass_model()
        validate_model(model)
        node = Node("total", model.key, {"x": (element(80), element(20000, "g"))})
        result = execute(Composition("family-sum", (node,), (node.id,)), {model.key: model})
        self.assertEqual(result["status"], "completed", result.get("error"))
        self.assertAlmostEqual(result["outputs"][node.id]["amount"], 100.0)
        normalized = result["steps"][0]["normalized_family_inputs"]["x"]
        self.assertAlmostEqual(normalized[0], 80 / JOULES_PER_KWH)
        self.assertAlmostEqual(normalized[1], 20 / JOULES_PER_KWH)
        json.dumps(result, allow_nan=False)
        short = Node("short", model.key, {"x": (element(80),)})
        denied = execute(Composition("family-guard", (short,), (short.id,)), {model.key: model})
        self.assertEqual(denied["status"], "rejected")
        self.assertIn("len(x) >= 2", denied["error"])

    def test_reference_elements_resolve_in_dependency_order(self) -> None:
        """Upstream outputs and direct values mix as family elements with preserved reliance."""
        context = "test fixture, summed parts"
        double = Model("synthetic-double", "test1", {"m": Port("mass", "kg", context)},
                       Port("mass", "kg", context), "2 * m", (), "Synthetic fixture", ("Test-only.",))
        total = total_mass_model()
        catalog = {double.key: double, total.key: total}
        first = Node("first", double.key, {"m": element(10)})
        node = Node("total", total.key, {"x": (Reference("first"), element(5))})
        result = execute(Composition("family-refs", (first, node), (node.id,)), catalog)
        self.assertEqual(result["status"], "completed", result.get("error"))
        self.assertAlmostEqual(result["outputs"][node.id]["amount"], 25.0)

    def test_family_binding_errors_fail_closed(self) -> None:
        """Empty, oversized, misshapen and mismatched family bindings are rejected."""
        model = total_mass_model()
        cases = [(), (element(1), element(2), element(3), element(4), element(5)),
                 (Value(1, Port("speed", "m/s", "other"), "fixture", "test"),)]
        for binding in cases:
            node = Node("bad", model.key, {"x": binding})
            result = execute(Composition("family-bad", (node,), (node.id,)), {model.key: model})
            self.assertEqual(result["status"], "rejected", binding)
        solo = Node("solo", model.key, {"x": element(1)})
        self.assertEqual(execute(Composition("s", (solo,), (solo.id,)), {model.key: model})["status"], "rejected")

    def test_bare_families_and_bad_declarations_are_rejected(self) -> None:
        """Families outside sum/prod/len, bad bounds and name collisions fail validation."""
        with self.assertRaises(ModelError):
            dimensions(parse("2 * x"), {}, {"x": MASS})
        with self.assertRaises(ModelError):
            dimensions(parse("len(x)"), {}, {})
        with self.assertRaises(ModelError):
            evaluate(parse("len(x)"), {}, {})
        with self.assertRaises(ModelError):
            dimensions(parse("log(x)"), {}, {"x": DIMENSIONLESS})
        with self.assertRaises(ModelError):
            evaluate(parse("log(x)"), {}, {"x": (4.0,)})
        context = "test"
        for bad in (0, 257, True, "4"):
            with self.assertRaises(ModelError, msg=repr(bad)):
                Family("mass", "kg", context, bad).validate()
        with self.assertRaises(ModelError):
            Family("no-such-meaning", "kg", context, 4).validate()
        with self.assertRaises(ModelError):
            Family("mass", "no-such-unit", context, 4).validate()
        model = total_mass_model()
        with self.assertRaises(ModelError):
            validate_model(Model("bad", "t", {"x": Port("mass", "kg", context)}, model.output,
                                 "sum(x)", (), "s", ("a",), "fixture", model.families))

    def test_families_are_forward_only(self) -> None:
        """Family targets fail at compile; scalar targets on family models report unsupported_expression."""
        model = total_mass_model()
        node = Node("inverse", model.key, {"x": (element(1), element(2)),
                    "__output__": Value(3, model.output, "fixture", "test")}, solve_for="x")
        result = execute(Composition("family-solve", (node,), (node.id,)), {model.key: model})
        self.assertEqual(result["status"], "rejected")
        self.assertIn("forward-only", result["error"])
        context = "test fixture, summed parts"
        mixed = Model("synthetic-offset-total", "test1", {"c": Port("mass", "kg", context)},
                      Port("mass", "kg", context), "c + sum(x)", ("len(x) >= 1",),
                      "Synthetic family fixture", ("Test-only.",), "fixture",
                      {"x": Family("mass", "kg", context, 4)})
        target = Node("scalar", mixed.key, {"x": (element(1), element(2)),
                      "__output__": Value(3, mixed.output, "fixture", "test")}, solve_for="c")
        solved = execute(Composition("family-scalar-solve", (target,), (target.id,)), {mixed.key: mixed})
        self.assertEqual(solved.get("solve_diagnostic", {}).get("code"), "unsupported_expression")

    def test_serialization_roundtrip_and_digest_compatibility(self) -> None:
        """Family models and tuple bindings survive JSON; empty families keep old digests."""
        model = total_mass_model()
        restored = model_from_dict(json.loads(json.dumps(asdict(model))))
        self.assertEqual(restored.families, model.families)
        node = Node("total", model.key, {"x": (element(80), element(20))})
        graph = Composition("family-rt", (node,), (node.id,))
        decoded = replace(composition_from_dict(json.loads(json.dumps(asdict(graph)))), purpose="fixture")
        self.assertIsInstance(decoded.nodes[0].bindings["x"], tuple)
        again = execute(decoded, {model.key: model})
        self.assertAlmostEqual(again["outputs"][node.id]["amount"], 100.0)
        plain = Model("synthetic-total", "test1", {}, model.output, "sum(x)", ("len(x) >= 2",),
                      "Synthetic family fixture", ("Test-only aggregation shape.",))
        legacy = dict(asdict(plain))
        legacy.pop("status")
        legacy.pop("families")
        expected = hashlib.sha256(json.dumps(legacy, sort_keys=True, allow_nan=False).encode()).hexdigest()
        self.assertEqual(model_digest(plain), expected)
        twin = Model("synthetic-total", "test1", {}, model.output, "sum(x)", ("len(x) >= 2",),
                     "Synthetic family fixture", ("Test-only aggregation shape.",), "fixture",
                     {"x": Family("mass", "kg", "test fixture, summed parts", 8)})
        self.assertNotEqual(model_digest(model), model_digest(twin))

    def test_family_runs_render_element_rows_in_reports(self) -> None:
        """Saved family runs report each bound element without crashing the renderer."""
        model = total_mass_model()
        node = Node("total", model.key, {"x": (element(80), element(20))})
        run = execute(Composition("family-report", (node,), (node.id,)), {model.key: model})
        with scratch_directory() as folder:
            directory = Path(folder)
            save_run(run, directory)
            html = write_report([run["run_id"]], directory).read_text(encoding="utf-8")
            self.assertIn("x[0]", html)
            self.assertIn("x[1]", html)
            self.assertIn("100", html)


if __name__ == "__main__":
    unittest.main()
