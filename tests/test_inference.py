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
    @patch.dict("os.environ", {"MODEL_API_KEY": "test-placeholder-not-a-key"})
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
