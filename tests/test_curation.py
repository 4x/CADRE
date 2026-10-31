"""Offline research handoff, integrity and candidate-admission boundary regressions."""

from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile

from connected_models.contracts import ModelError
from connected_models.curation import (ASSETS, build_kit, decode, digest, encoded, import_bundle,
                                      init_batch, load_bundle, pack_bundle, validate_bundle)
from connected_models.curation_schema import DOMAINS, KIT_VERSION, SCHEMA
from connected_models.registry import Registry
from connected_models.workflows import review_bundle
from test_support import scratch_directory


class CurationTests(unittest.TestCase):
    """Use synthetic teaching records and scratch registries; never publish real models."""

    def example(self) -> dict:
        """Load the deliberately non-importable worked contract fixture."""
        return load_bundle(ASSETS / "example-bundle.json")

    def research(self) -> dict:
        """Make a scratch-only submission from synthetic data for boundary testing."""
        bundle = self.example()
        bundle["example_only"] = False
        bundle["curator"] = "unit-test-fixture; not researched evidence"
        return bundle

    def write(self, folder: str, bundle: dict, name: str = "bundle.json") -> Path:
        """Write a bounded test payload to a test-owned workspace path."""
        path = Path(folder) / name
        path.write_bytes(encoded(bundle))
        return path

    def test_example_and_all_assignments_are_consistent(self) -> None:
        """The shipped teaching fixture passes and each advertised domain has a brief."""
        result = validate_bundle(self.example())
        self.assertTrue(result["example_only"])
        self.assertTrue(result["checks"][0]["runtime_contract_checked"])
        assignments = decode((ASSETS / "assignments.json").read_bytes())
        self.assertEqual({entry["domain"] for entry in assignments}, set(DOMAINS))
        self.assertTrue(all(len(entry["priorities"]) >= 3 for entry in assignments))

    def test_example_cannot_be_imported(self) -> None:
        """A valid teaching artifact does not become a candidate submission."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            with self.assertRaisesRegex(ModelError, "Teaching examples"):
                import_bundle(self.write(folder, self.example()), registry)
            self.assertEqual(registry.candidates(), [])

    def test_pack_roundtrip_and_idempotent_candidate_only_import(self) -> None:
        """Transport retains evidence; repeat imports create no reviews or duplicates."""
        with scratch_directory() as folder:
            source = self.write(folder, self.research())
            archive = Path(folder) / "return.zip"
            pack_bundle(source, archive)
            self.assertEqual(load_bundle(archive), load_bundle(source))
            registry = Registry(Path(folder) / "registry.sqlite3")
            first = import_bundle(archive, registry)
            second = import_bundle(archive, registry)
            self.assertEqual(first["candidates"], second["candidates"])
            self.assertEqual(len(registry.candidates()), 1)
            self.assertEqual(registry.snapshot(), ({}, {}))
            candidate = registry.candidates()[0]
            self.assertFalse(candidate["diagnostics"])
            self.assertEqual(candidate["evidence"]["record"], self.research()["models"][0])
            self.assertEqual(candidate["evidence"]["curation_intake"]["batch_sha256"], first["batch_sha256"])
            with self.assertRaises(FileExistsError):
                pack_bundle(source, archive)

    def test_research_only_record_retains_physical_units_and_blocks_admission(self) -> None:
        """Numerical checks never erase new physical vocabulary to gain eligibility."""
        bundle = self.research()
        item = bundle["models"][0]
        item["integration"].update(status="requires-extension", runtime_model=None, gaps=["New physical meanings and units need review."])
        item["variables"][0].update(quantity_id="building-energy:power", unit="W", dimensions="mass * length^2 / time^3")
        result = validate_bundle(bundle)
        self.assertFalse(result["checks"][0]["runtime_contract_checked"])
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            candidate_id = import_bundle(self.write(folder, bundle), registry)["candidates"][0]["candidate_id"]
            candidate = registry.candidate(candidate_id)
            self.assertTrue(candidate["diagnostics"])
            self.assertEqual(candidate["evidence"]["record"]["variables"][0]["unit"], "W")
            with self.assertRaises(ModelError):
                registry.review(candidate_id, "test-reviewer", "Unsupported candidate must fail.")
            with patch("connected_models.workflows.RUNS_PATH", Path(folder)):
                report = review_bundle(registry).read_text(encoding="utf-8")
            self.assertIn(item["id"], report)
            self.assertIn("has blockers", report)
            self.assertNotIn("--decision accepted", report)

    def test_unresolved_blocker_survives_valid_runtime_projection(self) -> None:
        """Valid arithmetic/model ports cannot bypass source interpretation blockers."""
        bundle = self.research()
        item = bundle["models"][0]
        item["unresolved"] = ["Source price basis remains ambiguous."]
        with self.assertRaisesRegex(ModelError, "requires blocked status"):
            validate_bundle(bundle)
        item["integration"].update(status="blocked", gaps=["Clarify the source price basis."])
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            candidate_id = import_bundle(self.write(folder, bundle), registry)["candidates"][0]["candidate_id"]
            with self.assertRaisesRegex(ModelError, "blocking diagnostics"):
                registry.review(candidate_id, "test-reviewer", "Cannot bypass unresolved evidence.")

    def test_revision_collision_preflights_entire_batch(self) -> None:
        """Changed immutable content fails before even an earlier new record is staged."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            bundle = self.research()
            source = self.write(folder, bundle)
            import_bundle(source, registry)
            new_record = deepcopy(bundle["models"][0])
            new_record["id"] += "-second"
            new_record["integration"]["runtime_model"]["id"] = new_record["id"]
            bundle["models"][0]["summary"] = "Changed evidence under the old revision is forbidden."
            bundle["models"].insert(0, new_record)
            self.write(folder, bundle)
            with self.assertRaisesRegex(ModelError, "existing revision"):
                import_bundle(source, registry)
            self.assertEqual(len(registry.candidates()), 1)

    def test_wrong_or_repeated_numeric_references_fail(self) -> None:
        """Curator claims cannot substitute for replayed independent expected values."""
        bundle = self.example()
        bundle["models"][0]["references"][0]["expected"] = 999
        with self.assertRaisesRegex(ModelError, "does not match"):
            validate_bundle(bundle)
        bundle = self.example()
        bundle["models"][0]["references"][1]["inputs"] = bundle["models"][0]["references"][0]["inputs"]
        with self.assertRaisesRegex(ModelError, "distinct inputs"):
            validate_bundle(bundle)

    def test_invalid_negative_case_and_supported_missing_input_case(self) -> None:
        """A claimed rejected value must fail; no fabricated scientific guard is needed."""
        bundle = self.example()
        case = bundle["models"][0]["rejection_cases"][0]
        case["inputs"]["energy"] = 1
        with self.assertRaisesRegex(ModelError, "rejection case is accepted"):
            validate_bundle(bundle)
        case.update(kind="missing-input", inputs={"tariff": 0.25}, reason="Energy is absent.")
        validate_bundle(bundle)

    def test_runtime_projection_cannot_change_ports_or_drop_limits(self) -> None:
        """An optional projection must faithfully retain the research declaration."""
        bundle = self.example()
        bundle["models"][0]["integration"]["runtime_model"]["inputs"]["energy"]["context"] = "different-system"
        with self.assertRaisesRegex(ModelError, "runtime port"):
            validate_bundle(bundle)
        bundle = self.example()
        bundle["models"][0]["integration"]["runtime_model"]["assumptions"].pop()
        with self.assertRaisesRegex(ModelError, "retain every"):
            validate_bundle(bundle)

    def test_unknown_keys_nan_booleans_duplicate_keys_and_code_fail(self) -> None:
        """The handoff accepts bounded data and arithmetic, not arbitrary agent code."""
        with self.assertRaisesRegex(ModelError, "Duplicate JSON"):
            decode(b'{"models": [], "models": []}')
        for value in (float("nan"), True):
            bundle = self.example()
            bundle["models"][0]["references"][0]["expected"] = value
            with self.assertRaises(ModelError):
                validate_bundle(bundle)
        bundle = self.example()
        bundle["accepted"] = True
        with self.assertRaisesRegex(ModelError, "unknown field"):
            validate_bundle(bundle)
        bundle = self.example()
        bundle["models"][0]["relationship"]["expression"] = "__import__('os')"
        with self.assertRaisesRegex(ModelError, "Only declared names"):
            validate_bundle(bundle)

    def test_zip_checksum_extra_members_and_secret_paths_fail(self) -> None:
        """Imports never extract paths or accept extra files returned by an agent."""
        raw = encoded(self.example())
        with scratch_directory() as folder:
            for index, extra in enumerate((False, True)):
                path = Path(folder) / f"bad-{index}.zip"
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("bundle.json", raw)
                    archive.writestr("manifest.json", encoded({"kit_version": KIT_VERSION, "sha256": "wrong"}))
                    if extra:
                        archive.writestr("../unexpected.txt", "must not extract")
                with self.assertRaises(ModelError):
                    load_bundle(path)
            with self.assertRaisesRegex(ModelError, "public JSON/ZIP"):
                load_bundle(Path(folder) / ".env")  # Rejected by name before any file access.

    def test_kit_is_allowlisted_and_schema_matches(self) -> None:
        """A generic kit contains full curator instructions and no operator/task bundle."""
        with scratch_directory() as folder:
            path = Path(folder) / "kit.zip"
            build_kit(path)
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                self.assertIn("AGENTS.md", names)
                self.assertNotIn("START-HERE.md", names)
                self.assertNotIn("assignment.json", names)
                self.assertNotIn("data/curation/assignments.json", names)
                self.assertFalse(any(name.startswith(("knowledge/", "assignments/")) for name in names))
                instructions = archive.read("AGENTS.md").decode("utf-8")
                self.assertIn("## Mission", instructions)
                self.assertIn("## Exact return format", instructions)
                self.assertIn("## Numerical and inverse checks", instructions)
                self.assertIn("thousands of models", instructions)
                self.assertNotIn("## Owner", instructions)
                self.assertNotIn("-m connected_models.curation import", instructions)
                self.assertNotIn("connected_models/inference.py", names)
                self.assertFalse(any(".env" in name or ".sqlite" in name for name in names))
                self.assertEqual(json.loads(archive.read("data/curation/batch.schema.json")), SCHEMA)
                manifest = json.loads(archive.read("KIT-MANIFEST.json"))
                for name, checksum in manifest["files"].items():
                    self.assertEqual(digest(archive.read(name)), checksum)

    def test_domain_kit_includes_only_its_assignment(self) -> None:
        """Each selected-domain ZIP isolates its assignment from the rest of the fleet."""
        with scratch_directory() as folder:
            for domain in DOMAINS:
                path = Path(folder) / f"{domain}.zip"
                build_kit(path, domain)
                with zipfile.ZipFile(path) as archive:
                    task = json.loads(archive.read("assignment.json"))
                    self.assertEqual(task["domain"], domain)
                    self.assertNotIn("connection_targets", task)
                    self.assertNotIn("data/curation/assignments.json", archive.namelist())
                    self.assertFalse(any(name.startswith("assignments/") for name in archive.namelist()))

    def test_atomic_batch_needs_no_chain_or_sample_queries(self) -> None:
        """A qualified standalone relationship can be returned without a proposed use."""
        bundle = self.example()
        bundle["handoff"].update(connections=[], queries=[])
        self.assertEqual(validate_bundle(bundle)["status"], "valid-data-awaiting-review")

    def test_legacy_return_keeps_original_version_through_repack_and_intake(self) -> None:
        """Updated instructions must not strand already-dispatched workers or relabel evidence."""
        bundle = self.research()
        bundle["kit_version"] = "2026-10-31.1"
        with scratch_directory() as folder:
            source = self.write(folder, bundle)
            archive_path = Path(folder) / "legacy.zip"
            pack_bundle(source, archive_path)
            with zipfile.ZipFile(archive_path) as archive:
                self.assertEqual(json.loads(archive.read("manifest.json"))["kit_version"], bundle["kit_version"])
            self.assertEqual(load_bundle(archive_path), bundle)
            registry = Registry(Path(folder) / "registry.sqlite3")
            import_bundle(archive_path, registry)
            metadata = registry.candidates()[0]["evidence"]["curation_intake"]
            self.assertEqual(metadata["kit_version"], "2026-10-31.1")

    def test_bundle_and_manifest_versions_must_agree(self) -> None:
        """A valid checksum cannot hide a relabeled or unsupported protocol version."""
        raw = encoded(self.example())
        with scratch_directory() as folder:
            path = Path(folder) / "mismatch.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("bundle.json", raw)
                archive.writestr("manifest.json", encoded({"kit_version": "2026-10-31.1", "sha256": digest(raw)}))
            with self.assertRaisesRegex(ModelError, "versions differ"):
                load_bundle(path)
            bundle = self.example()
            bundle["kit_version"] = "unknown-version"
            with self.assertRaises(ModelError):
                validate_bundle(bundle)

    def test_init_is_incomplete_and_refuses_overwrite(self) -> None:
        """Initialization supplies metadata, not fabricated research."""
        with scratch_directory() as folder:
            path = Path(folder) / "return.json"
            init_batch(DOMAINS[0], "test-agent", "test-batch", path)
            bundle = load_bundle(path)
            self.assertFalse(bundle["example_only"])
            with self.assertRaises(ModelError):
                validate_bundle(bundle)
            with self.assertRaises(FileExistsError):
                init_batch(DOMAINS[0], "test-agent", "test-batch", path)


if __name__ == "__main__":
    unittest.main()
