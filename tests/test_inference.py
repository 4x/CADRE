"""Model selection: the LLM variable overrides inference.toml everywhere."""

import sqlite3
import unittest
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from connected_models.contracts import ModelError
from connected_models.inference import (
    MODEL_PRICING,
    MODEL_VARIABLE,
    BudgetLedger,
    InferenceSettings,
)


class ModelSelectionTests(unittest.TestCase):
    """One override point feeds composer, repair, direct, and curator calls."""

    def test_toml_model_used_without_override(self) -> None:
        """Empty LLM means the TOML model and rates stand."""
        with patch.dict("os.environ", {MODEL_VARIABLE: ""}):
            settings = InferenceSettings.load(Path("inference.toml"))
        self.assertEqual(settings.model, "muse-spark-1.3")

    def test_llm_override_selects_model_and_rates(self) -> None:
        """LLM picks the model and applies its researched table rates."""
        with patch.dict("os.environ", {MODEL_VARIABLE: "muse-spark-1.3"}):
            settings = InferenceSettings.load(Path("inference.toml"))
        self.assertEqual(settings.model, "muse-spark-1.3")
        self.assertEqual(
            (settings.input_usd_per_million, settings.output_usd_per_million),
            MODEL_PRICING["muse-spark-1.3"],
        )
        self.assertEqual(
            (settings.input_usd_per_million, settings.output_usd_per_million),
            (Decimal("1.25"), Decimal("4.25")),
        )

    def test_unknown_llm_model_fails_closed(self) -> None:
        """Unpriced models refuse to load with a named remediation."""
        with patch.dict("os.environ", {MODEL_VARIABLE: "nope-9"}):
            with self.assertRaisesRegex(
                ModelError, "Unknown model 'nope-9'.*MODEL_PRICING"
            ):
                InferenceSettings.load(Path("inference.toml"))

    def test_explicit_override_beats_env_and_toml(self) -> None:
        """--model wins over LLM; LLM still wins over TOML when no flag is given."""
        priced = {"probe-b": (Decimal("2"), Decimal("3"))}
        with patch.dict(MODEL_PRICING, priced, clear=False):
            with patch.dict("os.environ", {MODEL_VARIABLE: "probe-b"}):
                flagged = InferenceSettings.load(
                    Path("inference.toml"), "muse-spark-1.3"
                )
                self.assertEqual(flagged.model, "muse-spark-1.3")
                self.assertEqual(
                    (flagged.input_usd_per_million, flagged.output_usd_per_million),
                    MODEL_PRICING["muse-spark-1.3"],
                )
                unflagged = InferenceSettings.load(Path("inference.toml"))
                self.assertEqual(unflagged.model, "probe-b")
                self.assertEqual(
                    (unflagged.input_usd_per_million, unflagged.output_usd_per_million),
                    (Decimal("2"), Decimal("3")),
                )

    def test_unknown_flag_model_fails_closed(self) -> None:
        """Unpriced --model names refuse to load with a named remediation."""
        with patch.dict("os.environ", {MODEL_VARIABLE: ""}):
            with self.assertRaisesRegex(
                ModelError, "Unknown model 'nope-9' in --model.*MODEL_PRICING"
            ):
                InferenceSettings.load(Path("inference.toml"), "nope-9")


class LedgerAttributionTests(unittest.TestCase):
    """One budget ceiling, with spend attributed per model."""

    def _settings(self, model: str) -> InferenceSettings:
        """Load deterministic settings for one priced model."""
        with patch.dict("os.environ", {MODEL_VARIABLE: ""}):
            return InferenceSettings.load(Path("inference.toml"), model)

    def test_spend_is_attributed_per_model(self) -> None:
        """Settled calls land under their own model; the ceiling stays shared."""
        priced = {"probe-b": (Decimal("2"), Decimal("3"))}
        with (
            TemporaryDirectory() as folder,
            patch.dict(MODEL_PRICING, priced, clear=False),
        ):
            path = Path(folder) / "usage.sqlite3"
            first = BudgetLedger(path, self._settings("muse-spark-1.3"))
            first.settle(first.reserve(), {"prompt_tokens": 10, "completion_tokens": 5})
            other_settings = replace(
                self._settings("muse-spark-1.3"),
                model="probe-b",
                input_usd_per_million=Decimal("2"),
                output_usd_per_million=Decimal("3"),
            )
            second = BudgetLedger(path, other_settings)
            second.settle(
                second.reserve(), {"prompt_tokens": 10, "completion_tokens": 5}
            )
            summary = second.summary()
        by_model = summary["by_model"]
        self.assertEqual(by_model["muse-spark-1.3"]["calls"], 1)
        self.assertEqual(by_model["probe-b"]["calls"], 1)
        self.assertGreater(
            by_model["probe-b"]["conservative_usd"],
            by_model["muse-spark-1.3"]["conservative_usd"],
        )
        self.assertEqual(summary["groups"]["settled"]["calls"], 2)

    def test_legacy_ledger_migrates_with_unattributed_rows(self) -> None:
        """Pre-model ledgers gain the column; old rows stay honestly unattributed."""
        with TemporaryDirectory() as folder:
            path = Path(folder) / "legacy.sqlite3"
            setup = sqlite3.connect(path)
            try:
                setup.execute(
                    "CREATE TABLE calls (id TEXT PRIMARY KEY, amount INTEGER NOT NULL, state TEXT NOT NULL)"
                )
                setup.execute("INSERT INTO calls VALUES ('old', 7, 'settled')")
                setup.commit()
            finally:
                setup.close()
            ledger = BudgetLedger(path, self._settings("muse-spark-1.3"))
            ledger.settle(
                ledger.reserve(), {"prompt_tokens": 10, "completion_tokens": 5}
            )
            by_model = ledger.summary()["by_model"]
        self.assertEqual(by_model["unattributed"]["calls"], 1)
        self.assertEqual(by_model["muse-spark-1.3"]["calls"], 1)
