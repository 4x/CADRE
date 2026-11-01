"""Reference, compatibility, topology and lineage checks for the scalar core."""

from dataclasses import replace
from decimal import Decimal
import json
from pathlib import Path
from test_support import scratch_directory
import unittest

from connected_models.contracts import DIMENSIONLESS, INVERSE_MONEY, INVERSE_TIME, MEANINGS, MONEY, TIME, Composition, ModelError, Node, Port, Reference, Value
from connected_models.demo import ANNUAL, HEAT, RATE, SAVING, YEARS, catalog, composition, fixture
from connected_models.runtime import execute, save_run


class RuntimeTests(unittest.TestCase):
    """Exercise independent oracles and deliberately invalid compositions."""

    def test_cashflow_oracle_and_reuse(self) -> None:
        """Compare closed-form execution to a separately summed Decimal cash flow."""
        models = catalog()
        run = execute(composition(), models)
        expected = sum(Decimal(2400) / Decimal("1.05") ** year for year in range(1, 11)) - Decimal(10000)
        self.assertEqual(run["status"], "completed")
        self.assertAlmostEqual(run["outputs"]["investment-npv"]["amount"], float(expected), places=8)
        costs = execute(composition(operation="operating-cost"), models)
        self.assertEqual(costs["outputs"]["annual-savings"]["amount"], 2400)
        self.assertEqual(len(run["steps"]), 7)
        self.assertEqual(len(costs["steps"]), 5)
        self.assertEqual(costs["outputs"]["baseline-cost"]["amount"], 3600)
        self.assertEqual(costs["outputs"]["upgrade-cost"]["amount"], 1200)

    def test_nist_published_reference(self) -> None:
        """Reproduce NIST HB135 (2020), equation 3-7, printed page 29."""
        graph = Composition("nist-reference", (Node("pv", "uniform-present-value@1", {
            "annual": fixture(100, SAVING, "NIST reference annual amount"),
            "rate": fixture(0.03, RATE, "NIST reference discount rate"),
            "years": fixture(5, YEARS, "NIST reference horizon"),
        }),), ("pv",))
        run = execute(graph, catalog())
        self.assertEqual(run["status"], "completed")
        self.assertAlmostEqual(run["outputs"]["pv"]["amount"], 457.97, delta=0.005)

    def test_units_and_meanings(self) -> None:
        """Convert Wh to kWh but reject electricity bound to delivered heat."""
        value = Value(12000, Port("delivered_heat", "Wh", ANNUAL), "fixture", "conversion case")
        self.assertEqual(value.bind(HEAT), 12)
        with self.assertRaisesRegex(ModelError, "meaning/context"):
            Value(12, Port("electricity_consumption", "kWh", ANNUAL), "fixture", "wrong meaning").bind(HEAT)
        with self.assertRaisesRegex(ModelError, "cannot use unit"):
            Port("delivered_heat", "USD", ANNUAL).validate()
        with self.assertRaisesRegex(ModelError, "meaning/context"):
            Value(12, replace(HEAT, context="different-home"), "fixture", "wrong context").bind(HEAT)

    def test_invalid_domains_and_nonfinite(self) -> None:
        """Invalid performance, prices and nonfinite inputs yield saved rejections."""
        for graph in (composition(performance=0), composition(tariff=-1), composition(performance=float("nan"))):
            with self.subTest(graph=graph):
                run = execute(graph, catalog())
                self.assertEqual(run["status"], "rejected")
                self.assertIn("error", run)
                with scratch_directory() as folder:
                    saved = save_run(run, Path(folder))
                    self.assertEqual(json.loads(saved.read_text())["status"], "rejected")

    def test_cycle_and_missing_input(self) -> None:
        """Reject cycles and missing inputs before producing any numerical steps."""
        original = composition()
        first = original.nodes[0]
        missing = replace(first, bindings={"heat": first.bindings["heat"]})
        run = execute(replace(original, nodes=(missing,) + original.nodes[1:]), catalog())
        self.assertEqual(run["status"], "rejected")
        self.assertEqual(run["steps"], [])
        model = replace(catalog()["annual-saving@1"], id="identity", inputs={"annual": SAVING},
                        output=SAVING, expression="annual", guards=())
        cycle = Composition("cycle", (Node("a", model.key, {"annual": Reference("b")}),
                                      Node("b", model.key, {"annual": Reference("a")})), ("a",))
        run = execute(cycle, {model.key: model})
        self.assertIn("cycle", run["error"])

    def test_expression_boundary(self) -> None:
        """Reject arbitrary code and dimensionally incorrect arithmetic."""
        for expression in ("__import__('os').getcwd()", "heat + performance", "heat[0]"):
            models = catalog()
            models["heat-to-electricity@1"] = replace(models["heat-to-electricity@1"], expression=expression)
            run = execute(composition(), models)
            self.assertEqual(run["status"], "rejected")
            self.assertEqual(run["steps"], [])

    def test_finance_vocabulary_batch(self) -> None:
        """Finance-1 meanings validate with their units; financial years stay non-physical."""
        pairs = {"future_value": ("USD", MONEY), "periodic_payment": ("USD", MONEY),
                 "effective_rate": ("1", DIMENSIONLESS), "nominal_rate": ("1", DIMENSIONLESS),
                 "signed_point_price_elasticity": ("1", DIMENSIONLESS), "unit_price": ("USD/unit", MONEY),
                 "quantity_price_derivative": ("unit^2/USD", INVERSE_MONEY),
                 "gross_domestic_product_current_price": ("USD", MONEY),
                 "gradient_amount": ("USD", MONEY), "interest_payment": ("USD", MONEY),
                 "principal_payment": ("USD", MONEY), "payment_index": ("periods", DIMENSIONLESS),
                 "implicit_price_deflator": ("index-point", DIMENSIONLESS),
                 "midyear_resident_population": ("person", DIMENSIONLESS),
                 "gross_domestic_product_real": ("USD_ref", MONEY),
                 "real_gdp_per_capita": ("USD_ref/person", MONEY),
                 "economic_profit": ("USD", MONEY),
                 "produced_quantity": ("unit", DIMENSIONLESS),
                 "finite_increment_marginal_cost": ("USD/unit", MONEY),
                 "gross_domestic_income_current_price": ("USD", MONEY),
                 "personal_saving_fraction": ("1", DIMENSIONLESS),
                 "unit_contribution_margin": ("USD/unit", MONEY),
                 "degree_operating_leverage": ("1", DIMENSIONLESS),
                 "allele_frequency": ("1", DIMENSIONLESS),
                 "effective_size": ("count", DIMENSIONLESS),
                 "selection_response": ("trait-units", DIMENSIONLESS),
                 "mutation_rate": ("1/site/generation", DIMENSIONLESS),
                 "genotype_count": ("count", DIMENSIONLESS),
                 "individual_count": ("count", DIMENSIONLESS),
                 "break_even_quantity": ("unit", DIMENSIONLESS),
                 "unit_variable_cost": ("USD/unit", MONEY),
                 "initial_payment": ("USD", MONEY),
                 "parallel_availability": ("1", DIMENSIONLESS),
                 "execution_time": ("s", TIME),
                 "byte_count": ("B", DIMENSIONLESS),
                 "gigabyte_count": ("GB", DIMENSIONLESS),
                 "gibibyte_count": ("GiB", DIMENSIONLESS),
                 "parallel_fraction": ("1", DIMENSIONLESS),
                 "component_speedup": ("1", DIMENSIONLESS),
                 "data_size": ("B", DIMENSIONLESS),
                 "transfer_rate": ("B/s", INVERSE_TIME),
                 "transfer_time": ("s", TIME),
                 "record_count": ("1", DIMENSIONLESS),
                 "record_size": ("B", DIMENSIONLESS),
                 "storage_capacity": ("B", DIMENSIONLESS),
                 "series_availability": ("1", DIMENSIONLESS)}
        for meaning, (unit, dimensions) in pairs.items():
            Port(meaning, unit, "test-context").validate()
            self.assertEqual(MEANINGS[meaning], dimensions)
        financial_year = Port("elapsed_time", "years", "test-context")
        financial_year.validate()
        with self.assertRaises(ModelError):
            Port("elapsed_time", "s", "test-context").validate()
        with self.assertRaises(ModelError):
            Port("duration", "years", "test-context").validate()

    def test_currency_units_never_convert_implicitly(self) -> None:
        """USD, CAD and reference-year dollars bind only to their own unit string."""
        usd = Port("future_value", "USD", "test-context")
        usd.require_compatible(Port("future_value", "USD", "test-context"))
        kwh = Port("delivered_heat", "kWh", "test-context")
        kwh.require_compatible(Port("delivered_heat", "Wh", "test-context"))
        with self.assertRaisesRegex(ModelError, "never convert implicitly"):
            Port("future_value", "USD", "test-context").require_compatible(Port("future_value", "CAD", "test-context"))
        with self.assertRaisesRegex(ModelError, "never convert implicitly"):
            Port("economic_series_current_price", "USD", "test-context").require_compatible(
                Port("economic_series_current_price", "USD_ref", "test-context"))

    def test_revision_and_old_run_preservation(self) -> None:
        """New inputs and a compatible model revision leave earlier runs intact."""
        models = catalog()
        old = execute(composition(), models)
        new_model = replace(models["heat-to-electricity@1"], version="2", expression="heat / performance * 1.0")
        models[new_model.key] = new_model
        graph = composition(performance=2)
        graph = replace(graph, nodes=tuple(replace(node, model=new_model.key) if node.id == "upgrade-energy" else node for node in graph.nodes))
        new = execute(graph, models)
        self.assertEqual(new["status"], "completed")
        self.assertNotEqual(old["model_snapshot_sha256"], new["model_snapshot_sha256"])
        self.assertEqual(old["outputs"]["annual-savings"]["amount"], 2400)
        self.assertEqual(new["outputs"]["annual-savings"]["amount"], 1800)
        with scratch_directory() as folder:
            first = save_run(old, Path(folder))
            contents = first.read_bytes()
            save_run(new, Path(folder))
            self.assertEqual(first.read_bytes(), contents)
            with self.assertRaises(FileExistsError):
                save_run(old, Path(folder))
