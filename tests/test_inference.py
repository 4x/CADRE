"""Offline tests for spend limits and safe Meta response handling."""

from dataclasses import replace
from decimal import Decimal
import json
from pathlib import Path
from test_support import scratch_directory
import unittest
from unittest.mock import MagicMock, patch

from connected_models.contracts import ModelError
from connected_models.inference import BudgetLedger, InferenceSettings, smoke_test


class InferenceTests(unittest.TestCase):
    """No test reads a credential file or sends an API request."""

    def settings(self) -> InferenceSettings:
        """Return the verified public configuration."""
        return InferenceSettings.load(Path("inference.toml"))

    @patch.dict("os.environ", {"MODEL_API_KEY": "obsolete-placeholder"}, clear=True)
    @patch("connected_models.inference.http.client.HTTPSConnection")
    def test_meta_key_is_required(self, transport: MagicMock) -> None:
        """The renamed credential is required; the obsolete variable is not consumed."""
        with scratch_directory() as folder:
            settings = self.settings()
            with self.assertRaisesRegex(ModelError, "META_API_KEY"):
                smoke_test(settings, BudgetLedger(Path(folder) / "usage.sqlite3", settings))
        transport.assert_not_called()

    def test_budget_persists_and_failed_requests_remain_reserved(self) -> None:
        """Independent ledger instances cannot bypass an existing reservation."""
        with scratch_directory() as folder:
            path = Path(folder) / "ledger.sqlite3"
            settings = replace(self.settings(), total_budget_usd=Decimal("2"))
            first = BudgetLedger(path, settings)
            call = first.reserve()
            second = BudgetLedger(path, settings)
            with self.assertRaisesRegex(ModelError, "budget"):
                second.reserve()
            first.settle(call, {"prompt_tokens": 100, "completion_tokens": 10})
            second.reserve()

    def test_budget_and_usage_validation(self) -> None:
        """Reject expanded authorization and unknown usage without releasing funds."""
        with self.assertRaises(ModelError):
            replace(self.settings(), total_budget_usd=Decimal("151")).validate()
        with scratch_directory() as folder:
            settings = replace(self.settings(), total_budget_usd=Decimal("2"))
            ledger = BudgetLedger(Path(folder) / "usage.sqlite3", settings)
            call = ledger.reserve()
            with self.assertRaises(ModelError):
                ledger.settle(call, {})
            with self.assertRaises(ModelError):
                ledger.reserve()

    @patch("connected_models.inference.http.client.HTTPSConnection")
    @patch.dict("os.environ", {"META_API_KEY": "test-placeholder-not-a-key"})
    def test_response_check(self, transport: MagicMock) -> None:
        """Validate structured content and settle returned usage without printing content."""
        response = transport.return_value.getresponse.return_value
        response.status = 200
        response.read.return_value = json.dumps({"usage": {"prompt_tokens": 100, "completion_tokens": 10},
            "choices": [{"finish_reason": "stop", "message": {"content": '{"status":"ok"}'}}]}).encode()
        with scratch_directory() as folder:
            settings = self.settings()
            result = smoke_test(settings, BudgetLedger(Path(folder) / "usage.sqlite3", settings))
        self.assertEqual(result["status"], "ok")
        self.assertNotIn("test-placeholder", json.dumps(result))
        transport.return_value.close.assert_called_once()

    @patch("connected_models.inference.http.client.HTTPSConnection")
    @patch.dict("os.environ", {"META_API_KEY": "test-placeholder-not-a-key"})
    def test_truncation_reports_reason_and_keeps_charge(self, transport: MagicMock) -> None:
        """Reasoning-budget truncation must not be misreported as a transport/JSON failure."""
        response = transport.return_value.getresponse.return_value
        response.status = 200
        response.read.return_value = json.dumps({"usage": {"prompt_tokens": 100, "completion_tokens": 4096},
            "choices": [{"finish_reason": "length", "message": {"content": ""}}]}).encode()
        with scratch_directory() as folder:
            settings = self.settings()
            ledger = BudgetLedger(Path(folder) / "usage.sqlite3", settings)
            with self.assertRaisesRegex(ModelError, "ended with length; usage recorded"):
                smoke_test(settings, ledger)
            self.assertEqual(ledger.summary()["groups"]["settled"]["calls"], 1)
        transport.return_value.request.assert_called_once()

    @patch("connected_models.inference.http.client.HTTPSConnection")
    @patch.dict("os.environ", {"META_API_KEY": "test-placeholder-not-a-key"})
    def test_bad_completed_json_keeps_charge(self, transport: MagicMock) -> None:
        """Malformed output is rejected after valid billing evidence is retained."""
        response = transport.return_value.getresponse.return_value
        response.status = 200
        response.read.return_value = json.dumps({"usage": {"prompt_tokens": 100, "completion_tokens": 10},
            "choices": [{"finish_reason": "stop", "message": {"content": "broken-json"}}]}).encode()
        with scratch_directory() as folder:
            settings = self.settings()
            ledger = BudgetLedger(Path(folder) / "usage.sqlite3", settings)
            with self.assertRaisesRegex(ModelError, "invalid JSON content"):
                smoke_test(settings, ledger)
            self.assertEqual(ledger.summary()["groups"]["settled"]["calls"], 1)
