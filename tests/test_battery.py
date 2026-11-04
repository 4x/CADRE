"""Chain-battery integrity and verdict semantics (the runner needs live inference)."""

import json
from pathlib import Path
import unittest

from evals.run_chain_battery import check_entry

BATTERIES = (Path("data/eval/chain-battery.json"), Path("data/eval/deep-battery.json"),
             Path("data/eval/adversarial-battery.json"))


def _record(status: str, outputs: dict | None = None) -> dict:
    """Build a minimal answer record for verdict testing."""
    return {"run_id": "test", "status": status, "outputs": outputs or {},
            "saved_path": "test.json", "error": None, "clarifications": []}


def _output(meaning: str, unit: str, amount: float) -> dict:
    """Build one node output in the saved-run shape."""
    return {"amount": amount, "port": {"meaning": meaning, "unit": unit}}


class ChainBatteryTests(unittest.TestCase):
    """Entries stay well-formed; fixed-detection never masks a value mismatch."""

    def test_battery_entries_are_well_formed(self) -> None:
        """Every entry carries a tier, a question, and oracle expectations."""
        for battery_path in BATTERIES:
            battery = json.loads(battery_path.read_bytes())
            self.assertGreaterEqual(len(battery["entries"]), 8)
            for entry in battery["entries"]:
                with self.subTest(battery=battery_path.name, id=entry["id"]):
                    self.assertIn(entry["tier"], (1, 2))
                    self.assertTrue(entry["question"].strip())
                    self.assertIn(entry["expected_status"], ("completed", "rejected"))
                    if entry.get("trap"):
                        self.assertEqual(entry["expected_status"], "rejected")
                        self.assertEqual(entry["expected_outputs"], [])
                        self.assertTrue(entry["naive_amounts"])
                        continue
                    self.assertTrue(entry["expected_outputs"])
                    for expected in entry["expected_outputs"]:
                        self.assertTrue(expected["meaning"] and expected["unit"])
                        if "amounts" in expected:
                            self.assertTrue(expected["amounts"])
                            for amount in expected["amounts"]:
                                self.assertIsInstance(amount, (int, float))
                        else:
                            self.assertIsInstance(expected["amount"], (int, float))

    def test_verdicts_cover_pass_fail_and_fixed(self) -> None:
        """Status/value comparison drives pass, fail, and tier-2 fixed detection."""
        entry = {"id": "t", "tier": 1, "expected_status": "completed",
                 "expected_outputs": [{"meaning": "m", "unit": "u", "amount": 10.0}]}
        good = _record("completed", {"n1": _output("m", "u", 10.0 + 1e-9)})
        self.assertEqual(check_entry(entry, good, 1e-6)["verdict"], "pass")
        bad = _record("completed", {"n1": _output("m", "u", 11.0)})
        failed = check_entry(entry, bad, 1e-6)
        self.assertEqual(failed["verdict"], "fail")
        self.assertTrue(failed["failures"])
        blocked = dict(entry, tier=2, expected_status="blocked")
        self.assertEqual(check_entry(blocked, good, 1e-6)["verdict"], "fixed")
        self.assertEqual(check_entry(blocked, bad, 1e-6)["verdict"], "fail")

    def test_multi_expected_amounts_compare_elementwise(self) -> None:
        """Branch-all oracles match the full root list in order, not one root."""
        entry = {"id": "m", "tier": 1, "expected_status": "completed",
                 "expected_outputs": [{"meaning": "m", "unit": "u", "amounts": [-2.0, 2.0]}]}
        port = {"meaning": "m", "unit": "u"}
        good = _record("completed", {"n1": {"amounts": [-2.0, 2.0], "port": port}})
        self.assertEqual(check_entry(entry, good, 1e-6)["verdict"], "pass")
        swapped = _record("completed", {"n1": {"amounts": [2.0, -2.0], "port": port}})
        self.assertEqual(check_entry(entry, swapped, 1e-6)["verdict"], "fail")
        scalar = _record("completed", {"n1": _output("m", "u", 2.0)})
        self.assertEqual(check_entry(entry, scalar, 1e-6)["verdict"], "fail")

    def test_single_root_matches_either_scalar_or_branch_shape(self) -> None:
        """One admitted root passes whether the run stores amount or amounts."""
        entry = {"id": "s", "tier": 1, "expected_status": "completed",
                 "expected_outputs": [{"meaning": "m", "unit": "u", "amount": 3.0}]}
        port = {"meaning": "m", "unit": "u"}
        branch = _record("completed", {"n1": {"amounts": [3.0], "excluded": [0.0],
                                            "port": port, "branch": "all"}})
        self.assertEqual(check_entry(entry, branch, 1e-6)["verdict"], "pass")
        ambiguous = _record("completed", {"n1": {"amounts": [3.0, 4.0], "port": port, "branch": "all"}})
        self.assertEqual(check_entry(entry, ambiguous, 1e-6)["verdict"], "fail")
        singular = {"id": "s", "tier": 1, "expected_status": "completed",
                    "expected_outputs": [{"meaning": "m", "unit": "u", "amounts": [3.0]}]}
        scalar = _record("completed", {"n1": _output("m", "u", 3.0)})
        self.assertEqual(check_entry(singular, scalar, 1e-6)["verdict"], "pass")
