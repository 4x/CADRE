"""Named physical constants resolved inside expressions."""

import math
from pathlib import Path
import unittest
import zipfile
import json

from connected_models.constants import CONSTANTS, CONSTANT_DIMENSIONS, CONSTANT_VALUES, Constant, constants_json, validate_constants
from connected_models.contracts import DIMENSIONLESS, GRAVITATION, PER_AMOUNT, POWER, STEFAN_BOLTZMANN, TEMPERATURE
from connected_models.curation import build_kit, load_bundle, validate_bundle
from connected_models.contracts import AREA
from connected_models.expressions import dimensions, evaluate, parse
from connected_models.contracts import ModelError
from test_support import scratch_directory

ROOT = Path(__file__).resolve().parent.parent


class ConstantTests(unittest.TestCase):
    """Universal fixed values resolve by name with engine-checked dimensions."""

    def test_registry_carries_dimensions_and_canonical_values(self) -> None:
        """Each constant evaluates in canonical units through its registry unit scale."""
        self.assertEqual(CONSTANT_DIMENSIONS["pi"], DIMENSIONLESS)
        self.assertEqual(CONSTANT_DIMENSIONS["stefan_boltzmann"], STEFAN_BOLTZMANN)
        self.assertEqual(CONSTANT_DIMENSIONS["gravitational_constant"], GRAVITATION)
        self.assertEqual(CONSTANT_DIMENSIONS["avogadro"], PER_AMOUNT)
        self.assertAlmostEqual(CONSTANT_VALUES["pi"], math.pi)
        self.assertAlmostEqual(CONSTANT_VALUES["stefan_boltzmann"], 5.670374419e-8 / 3600000)
        self.assertAlmostEqual(CONSTANT_VALUES["gravitational_constant"], 6.67430e-11 * 3600000)
        self.assertAlmostEqual(CONSTANT_VALUES["avogadro"], 6.02214076e23)
        self.assertTrue(all(isinstance(name, str) and constant.source.strip() for name, constant in CONSTANTS.items()))

    def test_radiative_expression_checks_and_evaluates(self) -> None:
        """The named sigma closes dimensionally to power and evaluates canonically."""
        expression = parse("e * stefan_boltzmann * A * (To**4 - Ts**4)")
        names = {"e": DIMENSIONLESS, "A": AREA, "To": TEMPERATURE, "Ts": TEMPERATURE}
        self.assertEqual(dimensions(expression, names), POWER)
        values = {"e": 0.97, "A": 1.5, "To": 295.0, "Ts": 306.0}
        expected = 0.97 * (5.670374419e-8 / 3600000) * 1.5 * (295.0**4 - 306.0**4)
        self.assertAlmostEqual(evaluate(expression, values), expected)

    def test_unknown_names_still_rejected(self) -> None:
        """Constants extend the namespace; they do not open it."""
        with self.assertRaises(ModelError):
            dimensions(parse("mystery + 1"), {})
        with self.assertRaises(ModelError):
            evaluate(parse("mystery + 1"), {})

    def test_validator_rejects_bad_entries(self) -> None:
        """Unknown units, non-identifiers, and missing provenance fail fast."""
        good = Constant(1.0, "1", "test", True)
        with self.assertRaises(ModelError):
            validate_constants({"bad name": good})
        with self.assertRaises(ModelError):
            validate_constants({"bad_unit": Constant(1.0, "furlongs", "test", True)})
        with self.assertRaises(ModelError):
            validate_constants({"bad_value": Constant(float("inf"), "1", "test", True)})
        with self.assertRaises(ModelError):
            validate_constants({"bad_source": Constant(1.0, "1", "  ", True)})
        validate_constants({"ok": good})

    def test_curation_allows_constants_and_rejects_shadowing(self) -> None:
        """Records may use registry names but must not redeclare them."""
        bundle = load_bundle(ROOT / "data" / "curation" / "example-bundle.json")
        bundle["models"][0]["relationship"]["expression"] = "energy * tariff * pi / pi"
        bundle["models"][0]["integration"]["runtime_model"]["expression"] = "energy * tariff * pi / pi"
        self.assertEqual(validate_bundle(bundle)["status"], "valid-data-awaiting-review")
        shadowed = load_bundle(ROOT / "data" / "curation" / "example-bundle.json")
        shadowed["models"][0]["relationship"]["expression"] = "energy * pi"
        for entry in shadowed["models"][0]["variables"]:
            if entry["symbol"] == "tariff":
                entry["symbol"] = "pi"
        with self.assertRaisesRegex(ModelError, "must not shadow"):
            validate_bundle(shadowed)

    def test_kit_ships_constants_with_vocabulary(self) -> None:
        """Curators see constant values, units, and provenance offline."""
        with scratch_directory() as folder:
            path = Path(folder) / "kit.zip"
            build_kit(path)
            with zipfile.ZipFile(path) as archive:
                payload = json.loads(archive.read("data/curation/runtime-vocabulary.json"))
        self.assertEqual(payload["constants"], constants_json())
        self.assertEqual(payload["constants"]["stefan_boltzmann"]["unit"], "W/(m2*K^4)")
