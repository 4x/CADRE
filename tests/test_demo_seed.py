"""Offline demo seeding: labeled admissions and deterministic scripted runs."""

import unittest
from pathlib import Path

from connected_models.demo_seed import (
    DEMO_QUESTIONS,
    seed_demo,
    seed_demo_registry,
    seed_demo_runs,
)
from connected_models.registry import Registry

from .support import scratch_directory


class DemoSeedTests(unittest.TestCase):
    """The demo seed is idempotent, labeled, and numerically exact."""

    def test_registry_seed_admits_five_labeled_fixtures(self) -> None:
        """Every heating fixture becomes eligible with demo-only provenance."""
        with scratch_directory() as workspace:
            registry = Registry(Path(workspace) / "models.sqlite3")
            admissions = seed_demo_registry(registry)
            self.assertEqual(len(admissions), 5)
            models, snapshots = registry.snapshot()
            self.assertEqual(len(models), 5)
            for key, admission in snapshots.items():
                self.assertIn(key, admissions)
                self.assertEqual(admission["reviewer"], "demo-seed")
                self.assertIn("not scientific approval", admission["notes"])

    def test_registry_seed_is_idempotent(self) -> None:
        """Reseeding keeps the same five admissions without duplicates."""
        with scratch_directory() as workspace:
            registry = Registry(Path(workspace) / "models.sqlite3")
            seed_demo_registry(registry)
            second = seed_demo_registry(registry)
            self.assertTrue(
                all(value == "already-eligible" for value in second.values())
            )
            models, _ = registry.snapshot()
            self.assertEqual(len(models), 5)

    def test_scripted_runs_match_known_amounts(self) -> None:
        """Seeded runs reproduce the documented operating and investment figures."""
        with scratch_directory() as workspace:
            registry = Registry(Path(workspace) / "models.sqlite3")
            seed_demo_registry(registry)
            models, _ = registry.snapshot()
            runs = seed_demo_runs(models, Path(workspace))
            operating = runs["operating-cost"]
            self.assertEqual(operating["status"], "completed")
            self.assertEqual(operating["outputs"]["baseline-cost"]["amount"], 3600)
            self.assertEqual(operating["outputs"]["upgrade-cost"]["amount"], 1200)
            self.assertEqual(operating["outputs"]["annual-savings"]["amount"], 2400)
            investment = runs["investment"]
            self.assertEqual(investment["status"], "completed")
            self.assertAlmostEqual(
                investment["outputs"]["investment-npv"]["amount"], 8532.16, places=2
            )

    def test_seed_demo_returns_questions_and_runs(self) -> None:
        """The combined seed returns everything the demo page needs."""
        with scratch_directory() as workspace:
            registry = Registry(Path(workspace) / "models.sqlite3")
            result = seed_demo(registry, Path(workspace))
            self.assertEqual(len(result["admissions"]), 5)
            self.assertEqual(set(result["runs"]), {"operating-cost", "investment"})
            self.assertEqual(result["questions"], DEMO_QUESTIONS)
            for run in result["runs"].values():
                self.assertEqual(run["status"], "completed")
                self.assertTrue(Path(run["saved_path"]).is_file())
