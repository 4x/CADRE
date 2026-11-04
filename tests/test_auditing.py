"""Review identity, evidence completeness and nonpublishing projection boundaries."""

import unittest
import zipfile
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from connected_models.auditing import build_packet, template, validate_review
from connected_models.contracts import Composition, ModelError, Node, Value
from connected_models.curation import ASSETS, encoded, load_bundle, pack_bundle
from connected_models.integration import project_record
from connected_models.registry import Registry
from connected_models.runtime import execute
from tests.support import scratch_directory


class AuditTests(unittest.TestCase):
    """Use explicitly synthetic reports; tests do not establish scientific approval."""

    def fixture(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Create a complete simulated review of the shipped teaching record."""
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
            item["recommendation"] = "recommend-admit"
            item["permitted_use"] = "Synthetic tests only."
        return bundle, report

    def test_revision_identity_and_coverage_are_enforced(self) -> None:
        """Stale, self-authored, partial and duplicate reports cannot validate."""
        bundle, report = self.fixture()
        self.assertEqual(
            validate_review(bundle, report)["status"], "valid-review-not-published"
        )
        mutations: list[Callable[[dict[str, Any]], None]] = [
            lambda r: r.update(batch_sha256="wrong"),
            lambda r: r.update(reviewer=bundle["curator"]),
            lambda r: r["models"][0].update(record_sha256="wrong"),
            lambda r: r["models"].clear(),
            lambda r: r["models"].append(deepcopy(r["models"][0])),
        ]
        for mutate in mutations:
            altered = deepcopy(report)
            mutate(altered)
            with self.assertRaises(ModelError):
                validate_review(bundle, altered)

    def test_incomplete_checks_and_missing_evidence_block_admission(self) -> None:
        """An attractive recommendation cannot override missing scientific evidence."""
        bundle, report = self.fixture()
        for status in ("not-checked", "failed"):
            altered = deepcopy(report)
            altered["models"][0]["checks"]["dimensions"]["status"] = status
            with self.assertRaises(ModelError):
                validate_review(bundle, altered)
        report["models"][0]["sources"] = []
        with self.assertRaises(ModelError):
            validate_review(bundle, report)

    def test_projection_preserves_research_and_requires_separate_admission(
        self,
    ) -> None:
        """A projection resolves supported implementation gaps without overwriting history."""
        bundle, report = self.fixture()
        before = encoded(bundle)
        payload = project_record(
            bundle, report, bundle["models"][0]["id"], "runtime-test1"
        )
        self.assertEqual(encoded(bundle), before)
        self.assertEqual(payload["evidence"]["record"], bundle["models"][0])
        self.assertEqual(
            payload["model"]["expression"],
            bundle["models"][0]["relationship"]["expression"],
        )
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            candidate = registry.propose(payload)
            self.assertEqual(registry.candidate(candidate)["diagnostics"], [])
            self.assertEqual(registry.snapshot()[0], {})
            registry.review(candidate, "synthetic-integrator", "Synthetic test only.")
            self.assertEqual(len(registry.snapshot()[0]), 1)
        report["models"][0]["recommendation"] = "needs-revision"
        with self.assertRaises(ModelError):
            project_record(bundle, report, bundle["models"][0]["id"], "runtime-test2")

    def test_packet_is_self_contained_and_role_specific(self) -> None:
        """The auditor sees only its task and original data, with no operator instructions."""
        bundle, _ = self.fixture()
        with scratch_directory() as folder:
            source = Path(folder) / "bundle.json"
            source.write_bytes(encoded(bundle))
            original = Path(folder) / "return.zip"
            pack_bundle(source, original)
            packet = Path(folder) / "reviewer.zip"
            build_packet(original, packet)
            with zipfile.ZipFile(packet) as archive:
                self.assertEqual(
                    set(archive.namelist()),
                    {
                        "AGENTS.md",
                        "return.zip",
                        "assignment.json",
                        "review.schema.json",
                        "review-template.json",
                    },
                )
                self.assertEqual(archive.read("return.zip"), original.read_bytes())
                self.assertIn(b"Required investigation", archive.read("AGENTS.md"))

    def test_reviewed_return_projects_and_executes_in_a_fresh_registry(self) -> None:
        """Reproduce the actual reviewed subset without relying on the owner's database."""
        bundle = load_bundle(ASSETS / "reviews/classical-mechanics-a-b01-bundle.json")
        report = load_bundle(ASSETS / "reviews/classical-mechanics-a-b01-review.json")
        validate_review(bundle, report)
        selected = [
            item
            for item in report["models"]
            if item["recommendation"] == "recommend-admit"
        ]
        self.assertEqual(len(selected), 2)
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            for item in selected:
                payload = project_record(bundle, report, item["id"], "r1.runtime1")
                candidate = registry.propose(payload)
                self.assertEqual(registry.candidate(candidate)["diagnostics"], [])
                registry.review(
                    candidate,
                    "test-integration-only",
                    "Replaying separately reviewed evidence in a scratch registry.",
                )
            models, admissions = Registry(registry.path).snapshot()
            for item in bundle["models"]:
                key = f"{item['id']}@r1.runtime1"
                if key not in models:
                    continue
                model = models[key]
                for case in item["references"]:
                    node = Node(
                        "result",
                        key,
                        {
                            name: Value(
                                amount,
                                model.inputs[name],
                                "user-scenario",
                                "Reviewed test reference",
                            )
                            for name, amount in case["inputs"].items()
                        },
                    )
                    result = execute(
                        Composition(case["id"], (node,), (node.id,), "scenario"),
                        models,
                        admissions,
                    )
                    self.assertEqual(result["status"], "completed", result.get("error"))
                    self.assertLessEqual(
                        abs(result["outputs"][node.id]["amount"] - case["expected"]),
                        case["tolerance"],
                    )


if __name__ == "__main__":
    unittest.main()
