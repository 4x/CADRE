"""Index-family inputs: aggregation over bound element tuples with shared ports."""

from copy import deepcopy
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import unittest

from connected_models.auditing import template, validate_review
from connected_models.contracts import DIMENSIONLESS, JOULES_PER_KWH, MASS, Composition, Family, Model, ModelError, Node, Port, Reference, Value
from connected_models.curation import validate_bundle
from connected_models.curation_schema import KIT_VERSION, SCHEMA_VERSION
from connected_models.expressions import dimensions, evaluate, parse
from connected_models.integration import project_record
from connected_models.registry import Registry
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


def element(amount: float, unit: str = "kg", origin: str = "fixture") -> Value:
    """Build one attributed family element value."""
    return Value(amount, Port("mass", unit, "test fixture, summed parts"), origin, "test")


def family_bundle() -> dict:
    """Build a complete synthetic curation bundle holding one family record."""
    context = "test fixture, summed parts"
    return {
        "schema_version": SCHEMA_VERSION, "kit_version": KIT_VERSION, "batch_id": "test-only-family-b01",
        "domain": "computer-science", "curator": "synthetic-test-only", "created": "2026-11-01",
        "example_only": False, "deferred": [],
        "handoff": {"summary": "Test.", "gaps": [], "connections": [], "queries": [], "review_notes": "Test."},
        "models": [{
            "id": "computer-science--test-only-family-sum", "revision": "r1", "title": "Test sum",
            "summary": "Test.", "kind": "definition",
            "relationship": {"output_symbol": "U", "expression": "sum(x)", "original_equation": "U = sum of x",
                             "source_id": "test-src", "locator": "Test.", "translation_notes": "Test."},
            "variables": [
                {"symbol": "x", "source_symbol": "x", "role": "family", "quantity_id": "mass",
                 "definition": "Test.", "unit": "kg", "dimensions": "mass", "context": context,
                 "domain": "Test.", "max_size": 4},
                {"symbol": "U", "source_symbol": "U", "role": "output", "quantity_id": "mass",
                 "definition": "Test.", "unit": "kg", "dimensions": "mass", "context": context,
                 "domain": "Test."},
            ],
            "constants": [], "guards": ["len(x) >= 1"], "assumptions": ["Test."], "limitations": ["Test."],
            "unresolved": [],
            "sources": [{"id": "test-src", "kind": "primary", "title": "Test.", "url": "https://example.org/test-only",
                         "version": "test", "accessed": "2026-11-01", "locator": "Test.", "evidence": "Test.",
                         "license": "Test.", "redistribution": "Test."}],
            "references": [
                {"id": "three", "inputs": {"x": [1, 2, 3]}, "expected": 6, "tolerance": 1e-9,
                 "method": "Test.", "provenance": "Test."},
                {"id": "one", "inputs": {"x": [10]}, "expected": 10, "tolerance": 1e-9,
                 "method": "Test.", "provenance": "Test."},
            ],
            "rejection_cases": [{"kind": "missing-input", "inputs": {}, "reason": "Test."}],
            "inverse_notes": "Test.",
            "integration": {"status": "requires-extension", "runtime_model": None,
                            "gaps": ["Test gap."], "duplicate_of": []},
        }],
    }


def admit(bundle: dict, folder: str) -> tuple[Registry, str]:
    """Review, project and publish one synthetic family record in a scratch registry."""
    report = template(bundle)
    report["reviewer"] = "synthetic-reviewer-test-only"
    for item in report["models"]:
        item["checks"] = {name: {"status": "passed", "evidence": "Synthetic fixture assertion, not actual review."}
                          for name in item["checks"]}
        item["sources"] = [{"url": "https://example.org/test-only", "locator": "Synthetic test",
                            "accessed": "2026-10-31", "finding": "No scientific claim."}]
        item["blockers"] = []
        item["recommendation"] = "recommend-admit"
        item["permitted_use"] = "Synthetic tests only."
    validate_review(bundle, report)
    registry = Registry(Path(folder) / "registry.sqlite3")
    payload = project_record(bundle, report, bundle["models"][0]["id"], "r1.runtime1")
    candidate = registry.propose(payload)
    assert registry.candidate(candidate)["diagnostics"] == []
    registry.review(candidate, "synthetic-integrator", "Synthetic test only.")
    return registry, bundle["models"][0]["id"]


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

    def test_family_bundle_validates_intake_rules(self) -> None:
        """Intake accepts the family bundle and rejects misshapen family payloads."""
        validate_bundle(family_bundle())
        missing = deepcopy(family_bundle())
        del missing["models"][0]["variables"][0]["max_size"]
        with self.assertRaises(ModelError):
            validate_bundle(missing)
        stray = deepcopy(family_bundle())
        stray["models"][0]["variables"][1]["max_size"] = 4
        with self.assertRaises(ModelError):
            validate_bundle(stray)
        scalar_list = deepcopy(family_bundle())
        scalar_list["models"][0]["variables"][0]["role"] = "input"
        with self.assertRaises(ModelError):
            validate_bundle(scalar_list)
        over = deepcopy(family_bundle())
        over["models"][0]["references"][0]["inputs"]["x"] = [1, 2, 3, 4, 5]
        with self.assertRaises(ModelError):
            validate_bundle(over)
        empty = deepcopy(family_bundle())
        empty["models"][0]["references"][0]["inputs"]["x"] = []
        with self.assertRaises(ModelError):
            validate_bundle(empty)

    def test_family_record_projects_admits_and_executes(self) -> None:
        """A reviewed family bundle flows from intake to an eligible executable model."""
        bundle = family_bundle()
        validate_bundle(bundle)
        with scratch_directory() as folder:
            registry, record_id = admit(bundle, folder)
            models, admissions = registry.snapshot()
            key = f"{record_id}@r1.runtime1"
            self.assertIn(key, models)
            self.assertEqual(models[key].families["x"].max_size, 4)
            node = Node("result", key, {"x": (element(80, "kg", "observation"), element(20000, "g", "observation"))})
            result = execute(Composition("admitted-family", (node,), (node.id,), "scenario"), models, admissions)
            self.assertEqual(result["status"], "completed", result.get("error"))
            self.assertAlmostEqual(result["outputs"][node.id]["amount"], 100.0)


if __name__ == "__main__":
    unittest.main()
