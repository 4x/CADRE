"""CFA-L1 vocabulary extension: units, meanings, conversions and guards."""

import json
import unittest
from dataclasses import replace
from pathlib import Path
from typing import Any

from connected_models.contracts import (
    AREA,
    DIMENSIONLESS,
    INVERSE_MONEY,
    METERS_PER_FOOT,
    MONEY,
    MONEY_PER_AREA,
    TIME,
    Dimensions,
    ModelError,
    Port,
    Value,
)
from connected_models.contracts import MEANINGS as MEANING_TABLE
from connected_models.contracts import UNITS as UNIT_TABLE
from connected_models.integration import project_record
from connected_models.runtime import execute
from connected_models.serialization import model_from_dict

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "data/curation/reviews"
MANIFEST = ROOT / "data/curation/inventories/intake-2026-11-04-cfa-wave.json"

# Every unit added by the cfa-l1-1 batch with its exact dimensions and scale.
NEW_UNITS: dict[str, tuple[Dimensions, float]] = {
    "EUR": (MONEY, 1.0),
    "GBP": (MONEY, 1.0),
    "CNY": (MONEY, 1.0),
    "currency": (MONEY, 1.0),
    "data-unit": (DIMENSIONLESS, 1.0),
    "data-unit^2": (DIMENSIONLESS, 1.0),
    "data-unit^3": (DIMENSIONLESS, 1.0),
    "data-unit^4": (DIMENSIONLESS, 1.0),
    "data-unit-x*data-unit-y": (DIMENSIONLESS, 1.0),
    "1/data-unit": (DIMENSIONLESS, 1.0),
    "predictor-unit": (DIMENSIONLESS, 1.0),
    "1/predictor-unit": (DIMENSIONLESS, 1.0),
    "response-unit": (DIMENSIONLESS, 1.0),
    "response-unit^2": (DIMENSIONLESS, 1.0),
    "good-unit": (DIMENSIONLESS, 1.0),
    "input-service-unit": (DIMENSIONLESS, 1.0),
    "good-unit/input-service-unit": (DIMENSIONLESS, 1.0),
    "good-unit/labor-hour": (DIMENSIONLESS, 1.0),
    "labor-hour": (DIMENSIONLESS, 1.0),
    "machine-hour": (DIMENSIONLESS, 1.0),
    "employee": (DIMENSIONLESS, 1.0),
    "persons": (DIMENSIONLESS, 1.0),
    "room_night": (DIMENSIONLESS, 1.0),
    "share": (DIMENSIONLESS, 1.0),
    "unit^2": (DIMENSIONLESS, 1.0),
    "price_currency_per_base_currency": (DIMENSIONLESS, 1.0),
    "base_currency_per_price_currency": (DIMENSIONLESS, 1.0),
    "currency_a_per_currency_b": (DIMENSIONLESS, 1.0),
    "currency_a_per_currency_c": (DIMENSIONLESS, 1.0),
    "currency_b_per_currency_c": (DIMENSIONLESS, 1.0),
    "USD per EUR": (DIMENSIONLESS, 1.0),
    "EUR/good-unit": (MONEY, 1.0),
    "EUR/good-unit**2": (MONEY, 1.0),
    "EUR/labor-hour": (MONEY, 1.0),
    "EUR/machine-hour": (MONEY, 1.0),
    "EUR/person": (MONEY, 1.0),
    "USD_per_unit": (MONEY, 1.0),
    "USD_per_employee": (MONEY, 1.0),
    "USD_per_room_night": (MONEY, 1.0),
    "good-unit/(EUR/good-unit)": (INVERSE_MONEY, 1.0),
    "good-unit/(EUR)": (INVERSE_MONEY, 1.0),
    "good-unit**2/EUR": (INVERSE_MONEY, 1.0),
    "square_foot": (AREA, METERS_PER_FOOT**2),
    "USD_per_square_foot": (MONEY_PER_AREA, 1.0 / METERS_PER_FOOT**2),
}

_PROJECTIONS: list[dict[str, Any]] | None = None


def _load_json(path: Path) -> dict[str, Any]:
    """Read a committed JSON artifact as UTF-8 without mutation."""
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def _recommend_admits() -> list[tuple[dict[str, Any], dict[str, Any], str, str]]:
    """List every wave recommend-admit record as bundle, report, id, revision."""
    manifest = _load_json(MANIFEST)
    found: list[tuple[dict[str, Any], dict[str, Any], str, str]] = []
    for name in sorted(manifest["review_files"]):
        report = _load_json(REVIEWS / name)
        bundle = _load_json(REVIEWS / name.replace("-review.json", "-bundle.json"))
        revisions = {item["id"]: item["revision"] for item in bundle["models"]}
        for item in report["models"]:
            if item.get("recommendation") == "recommend-admit":
                found.append((bundle, report, item["id"], revisions[item["id"]]))
    return found


def _projections() -> list[dict[str, Any]]:
    """Project the whole wave corpus once; every entry proves closure and replay."""
    global _PROJECTIONS
    if _PROJECTIONS is None:
        entries: list[dict[str, Any]] = []
        for bundle, report, model_id, revision in _recommend_admits():
            payload = project_record(bundle, report, model_id, f"{revision}.runtime1")
            entries.append(
                {"model_id": model_id, "revision": revision, "payload": payload}
            )
        _PROJECTIONS = entries
    return _PROJECTIONS


class CfaVocabularyTests(unittest.TestCase):
    """The cfa-l1-1 batch is exact, closed, and conservatively bound."""

    def test_new_units_carry_exact_dimensions_and_scales(self) -> None:
        """All 44 added units pin the dimensions and scales the records need."""
        self.assertEqual(len(NEW_UNITS), 44)
        for unit, (dims, scale) in NEW_UNITS.items():
            with self.subTest(unit=unit):
                self.assertIn(unit, UNIT_TABLE)
                self.assertEqual(UNIT_TABLE[unit].dimensions, dims)
                self.assertEqual(UNIT_TABLE[unit].scale, scale)

    def test_area_values_convert_through_registry_scales(self) -> None:
        """Square feet bind square metres both ways at exactly ft^2."""
        context = "probe-context"
        to_metric = Value(
            10000.0,
            Port("retail_floor_area_square_feet", "square_foot", context),
            "fixture",
            "probe",
        ).bind(Port("retail_floor_area_square_feet", "m2", context))
        self.assertEqual(to_metric, 10000.0 * METERS_PER_FOOT**2)
        back = Value(
            to_metric,
            Port("retail_floor_area_square_feet", "m2", context),
            "fixture",
            "probe",
        ).bind(Port("retail_floor_area_square_feet", "square_foot", context))
        self.assertAlmostEqual(back, 10000.0, places=9)
        self.assertEqual(UNIT_TABLE["USD_per_square_foot"].dimensions, MONEY_PER_AREA)

    def test_currency_units_never_convert_implicitly(self) -> None:
        """New money spellings join the no-implicit-conversion rule, not a bypass."""
        context = "probe-context"
        refusals = (
            ("nominal_gross_domestic_product", "EUR", "USD"),
            ("government_debt_stock", "GBP", "USD"),
            ("base_period_basket_base_price_value_terms", "CNY", "USD"),
            ("income_tax_expense", "currency", "USD"),
            ("unit_variable_cost", "USD_per_unit", "USD/unit"),
            ("service_revenue_per_employee", "USD_per_employee", "USD"),
            ("own_good_unit_price", "EUR/good-unit", "USD/unit"),
        )
        for meaning, first, second in refusals:
            with self.subTest(first=first, second=second):
                value = Value(5.0, Port(meaning, first, context), "fixture", "probe")
                with self.assertRaises(ModelError):
                    value.bind(Port(meaning, second, context))
        same = Value(
            5.0,
            Port("nominal_gross_domestic_product", "EUR", context),
            "fixture",
            "probe",
        ).bind(Port("nominal_gross_domestic_product", "EUR", context))
        self.assertEqual(same, 5.0)

    def test_service_hours_are_not_physical_time(self) -> None:
        """Labor/machine hours are dimensionless services; hour ports refuse them."""
        self.assertEqual(UNIT_TABLE["labor-hour"].dimensions, DIMENSIONLESS)
        self.assertEqual(UNIT_TABLE["machine-hour"].dimensions, DIMENSIONLESS)
        self.assertNotEqual(UNIT_TABLE["labor-hour"].dimensions, TIME)
        value = Value(
            40.0,
            Port("aggregate_labor_hours", "labor-hour", "probe-context"),
            "fixture",
            "probe",
        )
        with self.assertRaises(ModelError):
            value.bind(Port("aggregate_labor_hours", "h", "probe-context"))

    def test_wave_corpus_projects_end_to_end(self) -> None:
        """Every wave recommend-admit record closes dimensions and replays."""
        entries = _projections()
        self.assertEqual(len(entries), 303)
        for entry in entries:
            with self.subTest(model=f"{entry['model_id']}@{entry['revision']}"):
                payload = entry["payload"]
                self.assertTrue(payload["checks"])
                self.assertEqual(payload["intake_blockers"], [])

    def test_every_new_unit_is_exercised_by_the_corpus(self) -> None:
        """Each added unit appears on at least one projecting port."""
        seen: set[str] = set()
        for entry in _projections():
            model = entry["payload"]["model"]
            seen.add(model["output"]["unit"])
            for port in model["inputs"].values():
                seen.add(port["unit"])
            for family in model.get("families", {}).values():
                seen.add(family["unit"])
        for unit in NEW_UNITS:
            with self.subTest(unit=unit):
                self.assertIn(unit, seen)

    def test_every_corpus_port_is_coherent(self) -> None:
        """Each corpus port validates and its meaning matches its unit dims."""
        checked = 0
        for entry in _projections():
            model = entry["payload"]["model"]
            ports = [model["output"], *model["inputs"].values()]
            for raw in ports:
                port = Port(raw["meaning"], raw["unit"], raw["context"])
                with self.subTest(port=f"{raw['meaning']}/{raw['unit']}"):
                    port.validate()
                    self.assertEqual(
                        MEANING_TABLE[raw["meaning"]],
                        UNIT_TABLE[raw["unit"]].dimensions,
                    )
                    checked += 1
        self.assertGreater(checked, 1000)

    def test_guards_fire_on_new_vocabulary(self) -> None:
        """Valid bindings complete and guard violations reject with evidence."""
        from connected_models.contracts import Composition, Node

        cases = (
            (
                "financial-analysis-cfa-l1-b3-b68-bundle.json",
                "financial-analysis--forgone-trade-discount-periodic-cost",
                {"discount": 0.02},
                2 / 98,
                [{"discount": 1.0}, {"discount": -1.0}],
            ),
            (
                "financial-analysis-cfa-l1-b3-b78-bundle.json",
                "financial-analysis--retail-sales-per-square-foot",
                {"sales": 1000000.0, "area": 10000.0},
                100.0,
                [{"sales": 1000000.0, "area": 0.0}, {"sales": -1.0, "area": 10.0}],
            ),
            (
                "financial-analysis-cfa-l1-b3-b87-bundle.json",
                "financial-analysis--days-of-sales-outstanding",
                {"period": 360.0, "turnover": 12.0},
                30.0,
                [{"period": 360.0, "turnover": 0.0}, {"period": -5.0, "turnover": 2.0}],
            ),
        )
        for bundle_name, model_id, valid, expected, violations in cases:
            with self.subTest(model=model_id):
                bundle = _load_json(REVIEWS / bundle_name)
                report = _load_json(
                    REVIEWS / bundle_name.replace("-bundle.json", "-review.json")
                )
                original = next(
                    item for item in bundle["models"] if item["id"] == model_id
                )
                payload = project_record(
                    bundle, report, model_id, f"{original['revision']}.runtime1"
                )
                model = replace(model_from_dict(payload["model"]), status="fixture")

                def run(inputs: dict[str, float]) -> dict[str, Any]:
                    """Execute one fixture node over the projected model."""
                    node = Node(
                        "probe",
                        model.key,
                        {
                            name: Value(
                                inputs[name], model.inputs[name], "fixture", "probe"
                            )
                            for name in inputs
                        },
                    )
                    return execute(
                        Composition("probe-run", (node,), (node.id,)),
                        {model.key: model},
                    )

                completed = run(valid)
                self.assertEqual(completed["status"], "completed")
                self.assertAlmostEqual(
                    completed["outputs"]["probe"]["amount"], expected, places=9
                )
                for bad in violations:
                    rejected = run(bad)
                    self.assertEqual(rejected["status"], "rejected")
                    self.assertIn("domain condition failed", rejected["error"])
