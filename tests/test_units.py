"""Canonical unit registry, lexical aliases, and their inspection surface."""

import json
from pathlib import Path
import unittest
import zipfile

from connected_models.contracts import UNITS, UNIT_ALIASES, describe_units
from connected_models.curation import build_kit
from connected_models.query_inputs import UNIT_PATTERN, unit_identity
from test_support import scratch_directory


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
        self.assertEqual(UNIT_PATTERN.match(" V").group(1), "V")
        self.assertEqual(UNIT_PATTERN.match(" dollars").group(1), "dollars")
        self.assertEqual(UNIT_PATTERN.match(" ohm m").group(1), "ohm m")
        self.assertIsNone(UNIT_PATTERN.match(" furlongs"))

    def test_kit_ships_aliases_with_vocabulary(self) -> None:
        """Curators see the alias map offline next to units and meanings."""
        with scratch_directory() as folder:
            path = Path(folder) / "kit.zip"
            build_kit(path)
            with zipfile.ZipFile(path) as archive:
                payload = json.loads(archive.read("data/curation/runtime-vocabulary.json"))
        self.assertEqual(payload["aliases"], UNIT_ALIASES)
        self.assertEqual(set(payload["units"]), set(UNITS))

    def test_describe_units_lists_scales_and_aliases(self) -> None:
        """The inspection surface shows dimensions, exact scales, and alias groupings."""
        rendered = describe_units()
        self.assertIn("USD | currency^1 | scale 1.0 | aliases: $, dollar, dollars, usd", rendered)
        self.assertIn("kWh | mass^1 length^2 time^-2 | scale 1.0 | aliases: kwh", rendered)
        self.assertIn("S | mass^-1 length^-2 time^3 current^2 | scale 3600000", rendered)
        filtered = describe_units("dollar")
        self.assertIn("USD | currency^1", filtered)
        self.assertIn("USD/kWh", filtered)
        self.assertNotIn("m/s^2", filtered)
        self.assertEqual(describe_units("no-such-unit"), "")
