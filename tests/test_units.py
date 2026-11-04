"""Canonical unit registry, lexical aliases, and their inspection surface."""

import json
import unittest
import zipfile
from fractions import Fraction
from pathlib import Path

from connected_models.contracts import (
    JOULES_PER_KWH,
    UNIT_ALIASES,
    UNITS,
    Port,
    describe_units,
)
from connected_models.curation import build_kit
from connected_models.query_inputs import (
    UNIT_PATTERN,
    bind_fact,
    unit_identity,
    validate_fact,
)
from tests.support import scratch_directory


def _unit_group(text: str) -> str:
    """Match the quote pattern or fail; group 1 holds the unit spelling."""
    matched = UNIT_PATTERN.match(text)
    assert matched is not None
    return matched.group(1)


class UnitRegistryTests(unittest.TestCase):
    """Aliases resolve against the versioned vocabulary, never a query-local guess."""

    def test_every_alias_resolves_to_its_canonical_unit(self) -> None:
        """The table carries no dead entries, self-maps, or unknown targets."""
        self.assertTrue(UNIT_ALIASES)
        for alias, canonical in UNIT_ALIASES.items():
            with self.subTest(alias=alias):
                self.assertIn(canonical, UNITS)
                self.assertNotIn(alias, UNITS)
                self.assertEqual(unit_identity(alias), canonical)

    def test_canonical_case_wins_over_normalization(self) -> None:
        """SI case pairs stay distinct; uppercase canonicals resolve exactly."""
        for unit in ("S", "s", "V", "C", "K", "W", "Btu", "A", "USD", "USD/kWh", "kWh"):
            with self.subTest(unit=unit):
                self.assertEqual(unit_identity(unit), unit)
        self.assertEqual(unit_identity("Dollars"), "USD")
        self.assertEqual(unit_identity("dollars per kwh"), "USD/kWh")
        self.assertEqual(unit_identity("KWH"), "kWh")

    def test_year_folds_and_unknown_passthrough(self) -> None:
        """Period spellings fold to years; anything else passes through for explicit rejection."""
        for spelling in ("year", "annual-period", "annual-periods"):
            self.assertEqual(unit_identity(spelling), "years")
        self.assertEqual(unit_identity("furlongs"), "furlongs")
        self.assertEqual(unit_identity("celsius"), "celsius")

    def test_quote_pattern_matches_aliases_and_canonicals(self) -> None:
        """Explicit units next to a number are recognized in either spelling."""
        self.assertEqual(_unit_group(" V"), "V")
        self.assertEqual(_unit_group(" dollars"), "dollars")
        self.assertEqual(_unit_group(" ohm m"), "ohm m")
        self.assertIsNone(UNIT_PATTERN.match(" furlongs"))

    def test_fx_quote_aliases_resolve_to_usd_per_eur(self) -> None:
        """Natural FX phrasings reach the USD-per-EUR quote; pair order stays unbound."""
        self.assertEqual(UNITS["USD per EUR"].scale, 1.0)
        self.assertEqual(UNITS["USD per EUR"].dimensions, UNITS["1"].dimensions)
        for spelling in (
            "USD per EUR",
            "dollar/euro",
            "dollars/euro",
            "usd/eur",
            "dollar per euro",
            "dollars per euro",
            "Dollars per Euro",
            "USD/EUR",
        ):
            with self.subTest(spelling=spelling):
                self.assertEqual(unit_identity(spelling), "USD per EUR")
        self.assertEqual(_unit_group(" dollars/euro"), "dollars/euro")
        self.assertEqual(unit_identity("EUR/USD"), "eur/usd")
        self.assertNotIn("eur/usd", UNITS)
        self.assertNotIn("eur/usd", UNIT_ALIASES)

    def test_mile_units_bind_with_exact_scales(self) -> None:
        """Faithful mph/mile facts execute; the mile is exactly 1609.344 m."""
        self.assertEqual(UNITS["mi"].scale, 1609.344)
        self.assertEqual(UNITS["mph"].scale, 1609.344 / 3600)
        self.assertEqual(UNITS["mph"].dimensions, UNITS["m/s"].dimensions)
        self.assertEqual(UNITS["mi"].dimensions, UNITS["m"].dimensions)
        for spelling, canonical in (
            ("mile", "mi"),
            ("miles", "mi"),
            ("miles/hour", "mph"),
            ("mi/h", "mph"),
            ("miles per hour", "mph"),
            ("MPH", "mph"),
        ):
            with self.subTest(spelling=spelling):
                self.assertEqual(unit_identity(spelling), canonical)
        self.assertEqual(_unit_group(" mph"), "mph")
        self.assertEqual(_unit_group(" miles"), "miles")

    def test_imperial_batch_scales_derive_from_exact_definitions(self) -> None:
        """Query-3 lengths, volumes, masses and rates match their exact definitions."""
        self.assertEqual(UNITS["in"].scale, 0.0254)
        self.assertEqual(UNITS["ft"].scale, 0.3048)
        self.assertEqual(UNITS["yd"].scale, 0.9144)
        self.assertEqual(UNITS["nmi"].scale, 1852)
        self.assertEqual(UNITS["ft/s"].scale, 0.3048)
        self.assertEqual(UNITS["kn"].scale, 1852 / 3600)
        self.assertEqual(UNITS["L"].scale, 0.001)
        self.assertEqual(UNITS["mL"].scale, 1e-6)
        self.assertEqual(UNITS["gal"].scale, 3.785411784e-3)
        self.assertEqual(UNITS["qt"].scale, 3.785411784e-3 / 4)
        self.assertEqual(UNITS["lb"].scale, 0.45359237 / JOULES_PER_KWH)
        self.assertEqual(UNITS["oz"].scale, 0.45359237 / 16 / JOULES_PER_KWH)
        self.assertEqual(UNITS["lbf"].scale, 4.4482216152605 / JOULES_PER_KWH)
        self.assertEqual(UNITS["cal"].scale, 4.184 / JOULES_PER_KWH)
        self.assertEqual(UNITS["kcal"].scale, 4184 / JOULES_PER_KWH)
        self.assertEqual(
            UNITS["hp"].scale, 550 * 0.3048 * 4.4482216152605 / JOULES_PER_KWH
        )
        for spelling, canonical in (
            ("inch", "in"),
            ("inches", "in"),
            ("foot", "ft"),
            ("feet", "ft"),
            ("feet/second", "ft/s"),
            ("feet per second", "ft/s"),
            ("yard", "yd"),
            ("yards", "yd"),
            ("nmi", "nmi"),
            ("nautical mile", "nmi"),
            ("nautical miles", "nmi"),
            ("knot", "kn"),
            ("knots", "kn"),
            ("liter", "L"),
            ("liters", "L"),
            ("litre", "L"),
            ("litres", "L"),
            ("milliliters", "mL"),
            ("ml", "mL"),
            ("ML", "mL"),
            ("cc", "mL"),
            ("gallon", "gal"),
            ("gallons", "gal"),
            ("quart", "qt"),
            ("quarts", "qt"),
            ("pound", "lb"),
            ("pounds", "lb"),
            ("lbs", "lb"),
            ("ounce", "oz"),
            ("ounces", "oz"),
            ("calorie", "cal"),
            ("calories", "cal"),
            ("kilocalorie", "kcal"),
            ("kilocalories", "kcal"),
            ("horsepower", "hp"),
        ):
            with self.subTest(spelling=spelling):
                self.assertEqual(unit_identity(spelling), canonical)
        self.assertEqual(_unit_group(" ft"), "ft")
        self.assertEqual(_unit_group(" gallons"), "gallons")
        self.assertEqual(_unit_group(" feet/second"), "feet/second")

    def test_imperial_facts_bind_to_si_ports(self) -> None:
        """Everyday imperial spellings validate and bind instead of blocking."""
        cases = (
            ("12", "inches", "in", "length", "m"),
            ("6", "feet", "ft", "length", "m"),
            ("100", "yards", "yd", "length", "m"),
            ("3", "nautical miles", "nmi", "length", "m"),
            ("88", "feet/second", "ft/s", "speed", "m/s"),
            ("20", "knots", "kn", "speed", "m/s"),
            ("2", "gallons", "gal", "volume", "m3"),
            ("5", "liters", "L", "volume", "m3"),
            ("1", "quart", "qt", "volume", "m3"),
            ("500", "milliliters", "mL", "volume", "m3"),
            ("10", "cc", "mL", "volume", "m3"),
            ("150", "pounds", "lb", "mass", "kg"),
            ("8", "ounces", "oz", "mass", "kg"),
            ("200", "lbf", "lbf", "force", "N"),
            ("250", "calories", "cal", "translational_kinetic_energy", "J"),
            ("2", "kilocalories", "kcal", "translational_kinetic_energy", "J"),
            ("3", "horsepower", "hp", "electrical_power", "W"),
        )
        for literal, spelling, canonical, meaning, target_unit in cases:
            with self.subTest(spelling=spelling):
                quote = f"{literal} {spelling}"
                fact = validate_fact(
                    {
                        "id": "fact-x",
                        "name": "reading",
                        "value_type": "number",
                        "value": literal,
                        "unit": spelling,
                        "quote": quote,
                    },
                    quote,
                )
                value = bind_fact(fact, Port(meaning, target_unit, "probe-context"))
                self.assertEqual(value.port.unit, canonical)

    def test_clinical_batch_binds_dosing_facts(self) -> None:
        """Query-4 mass and concentration spellings validate and bind."""
        self.assertEqual(UNITS["mg"].scale, 1e-6 / JOULES_PER_KWH)
        self.assertEqual(UNITS["mg/kg"].scale, 1e-6)
        self.assertEqual(UNITS["dL"].scale, 1e-4)
        ratio = UNITS["mg/dL"].scale / UNITS["kg/m^3"].scale
        self.assertEqual(Fraction(ratio).limit_denominator(1000), Fraction(1, 100))
        for spelling, canonical in (
            ("milligram", "mg"),
            ("milligrams", "mg"),
            ("mg per kg", "mg/kg"),
            ("mg/kg", "mg/kg"),
            ("deciliter", "dL"),
            ("deciliters", "dL"),
            ("dl", "dL"),
            ("mg/dL", "mg/dL"),
            ("mg per dl", "mg/dL"),
            ("mg/dl", "mg/dL"),
        ):
            with self.subTest(spelling=spelling):
                self.assertEqual(unit_identity(spelling), canonical)
        cases = (
            ("250", "milligrams", "mg", "labeled_active_drug_reference_mass", "kg"),
            ("15", "mg per kg", "mg/kg", "prescribed_drug_mass_per_body_mass", "1"),
            ("1.2", "mg/dL", "mg/dL", "serum_creatinine_mass_concentration", "kg/m^3"),
        )
        for literal, spelling, canonical, meaning, target_unit in cases:
            with self.subTest(spelling=spelling):
                quote = f"{literal} {spelling}"
                fact = validate_fact(
                    {
                        "id": "fact-x",
                        "name": "reading",
                        "value_type": "number",
                        "value": literal,
                        "unit": spelling,
                        "quote": quote,
                    },
                    quote,
                )
                value = bind_fact(fact, Port(meaning, target_unit, "probe-context"))
                self.assertEqual(value.port.unit, canonical)

    def test_kit_ships_aliases_with_vocabulary(self) -> None:
        """Curators see the alias map offline next to units and meanings."""
        with scratch_directory() as folder:
            path = Path(folder) / "kit.zip"
            build_kit(path)
            with zipfile.ZipFile(path) as archive:
                payload = json.loads(
                    archive.read("data/curation/runtime-vocabulary.json")
                )
        self.assertEqual(payload["aliases"], UNIT_ALIASES)
        self.assertEqual(set(payload["units"]), set(UNITS))

    def test_describe_units_lists_scales_and_aliases(self) -> None:
        """The inspection surface shows dimensions, exact scales, and alias groupings."""
        rendered = describe_units()
        self.assertIn(
            "USD | currency^1 | scale 1.0 | aliases: $, dollar, dollars, usd", rendered
        )
        self.assertIn(
            "kWh | mass^1 length^2 time^-2 | scale 1.0 | aliases: kwh", rendered
        )
        self.assertIn(
            "S | mass^-1 length^-2 time^3 current^2 | scale 3600000", rendered
        )
        filtered = describe_units("dollar")
        self.assertIn("USD | currency^1", filtered)
        self.assertIn("USD/kWh", filtered)
        self.assertNotIn("m/s^2", filtered)
        self.assertEqual(describe_units("no-such-unit"), "")
