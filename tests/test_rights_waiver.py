"""Temporary rights waiver: default-off gate with a stamped, reversible bypass."""

import unittest
from typing import Any

from connected_models.auditing import template
from connected_models.contracts import ModelError
from connected_models.curation import ASSETS, load_bundle
from connected_models.integration import (
    RIGHTS_WAIVER_ASSUMPTION,
    project_record,
    rights_only_waivable,
)


class RightsWaiverTests(unittest.TestCase):
    """The waiver admits rights-only blocks; every other gate stands."""

    def fixture(
        self, verdict: str = "recommend-admit"
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Build a complete simulated review of the shipped teaching record."""
        bundle = load_bundle(ASSETS / "example-bundle.json")
        bundle["example_only"] = False
        report = template(bundle)
        report["reviewer"] = "synthetic-reviewer-test-only"
        for item in report["models"]:
            item["checks"] = {
                name: {
                    "status": "passed",
                    "evidence": "Synthetic fixture assertion, not actual review.",
                }
                for name in item["checks"]
            }
            item["sources"] = [
                {
                    "url": "https://example.org/test-only",
                    "locator": "Synthetic test",
                    "accessed": "2026-10-31",
                    "finding": "No scientific claim.",
                }
            ]
            item["blockers"] = []
            item["recommendation"] = verdict
            item["permitted_use"] = "Synthetic tests only."
        return bundle, report

    def rights_only(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Shape a needs-revision record blocked only on licensing."""
        bundle, report = self.fixture("needs-revision")
        item = report["models"][0]
        item["checks"]["rights-provenance"] = {
            "status": "failed",
            "evidence": "Synthetic license defect.",
        }
        item["blockers"] = ["License identifier inaccurate; correct before admission."]
        return bundle, report

    def model_id(self, bundle: dict[str, Any]) -> str:
        """Return the fixture record identity without hard-coding it."""
        return str(bundle["models"][0]["id"])

    def test_default_refuses_rights_only_blocks(self) -> None:
        """Without the flag, a reviewer rejection is final."""
        bundle, report = self.rights_only()
        self.assertTrue(rights_only_waivable(report["models"][0]))
        with self.assertRaises(ModelError):
            project_record(bundle, report, self.model_id(bundle), "runtime-waiver-off")

    def test_flag_admits_rights_only_and_stamps(self) -> None:
        """The flag projects rights-only records with visible provenance."""
        bundle, report = self.rights_only()
        self.assertTrue(rights_only_waivable(report["models"][0]))
        payload = project_record(
            bundle, report, self.model_id(bundle), "runtime-waiver-on", True
        )
        self.assertIn(RIGHTS_WAIVER_ASSUMPTION, payload["model"]["assumptions"])
        waiver = payload["evidence"]["projection"]["rights_waiver"]
        self.assertTrue(waiver["relaxed"])
        self.assertEqual(waiver["failed_check"], "rights-provenance")
        self.assertEqual(payload["intake_blockers"], [])

    def test_flag_refuses_blocked_verdicts(self) -> None:
        """Guard traps and duplicates stay out even with the flag."""
        bundle, report = self.fixture("blocked")
        report["models"][0]["blockers"] = ["No valid completion exists."]
        self.assertFalse(rights_only_waivable(report["models"][0]))
        with self.assertRaises(ModelError):
            project_record(
                bundle, report, self.model_id(bundle), "runtime-blocked", True
            )

    def test_flag_refuses_science_failures(self) -> None:
        """A failed science check is not a licensing issue."""
        bundle, report = self.rights_only()
        report["models"][0]["checks"]["dimensions"] = {
            "status": "failed",
            "evidence": "Synthetic dimension defect.",
        }
        self.assertFalse(rights_only_waivable(report["models"][0]))
        with self.assertRaises(ModelError):
            project_record(
                bundle, report, self.model_id(bundle), "runtime-science", True
            )

    def test_flag_refuses_unchecked_rights(self) -> None:
        """Uninspected clearance is not waivable clearance."""
        bundle, report = self.rights_only()
        report["models"][0]["checks"]["rights-provenance"] = {
            "status": "not-checked",
            "evidence": "Never inspected.",
        }
        self.assertFalse(rights_only_waivable(report["models"][0]))
        with self.assertRaises(ModelError):
            project_record(
                bundle, report, self.model_id(bundle), "runtime-unchecked", True
            )

    def test_flag_refuses_supersession_blockers(self) -> None:
        """Superseded records stay out even when their science passed."""
        bundle, report = self.rights_only()
        report["models"][0]["blockers"] = ["Superseded by r2; do not admit."]
        self.assertFalse(rights_only_waivable(report["models"][0]))
        with self.assertRaises(ModelError):
            project_record(
                bundle, report, self.model_id(bundle), "runtime-superseded", True
            )

    def test_flag_keeps_vocabulary_enforcement(self) -> None:
        """Unknown units still refuse under the waiver."""
        bundle, report = self.rights_only()
        variables = bundle["models"][0]["variables"]
        symbol = next(item["symbol"] for item in variables if item["role"] == "input")
        for item in variables:
            if item["symbol"] == symbol:
                item["unit"] = "no_such_unit"
        with self.assertRaises(ModelError):
            project_record(bundle, report, self.model_id(bundle), "runtime-vocab", True)

    def test_flag_leaves_normal_path_unstamped(self) -> None:
        """Recommend-admit projections carry no waiver markings."""
        bundle, report = self.fixture("recommend-admit")
        payload = project_record(
            bundle, report, self.model_id(bundle), "runtime-normal", True
        )
        self.assertNotIn(RIGHTS_WAIVER_ASSUMPTION, payload["model"]["assumptions"])
        self.assertNotIn("rights_waiver", payload["evidence"]["projection"])


if __name__ == "__main__":
    unittest.main()
