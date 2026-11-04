"""A bounded Meta smoke-test adapter with persistent, conservative spend accounting.

Credentials come only from the process environment. This module never loads dotenv
files. The ledger covers this application, not other tools sharing the account.
"""

import http.client
import json
import logging
import os
import sqlite3
import tomllib
from contextlib import closing
from dataclasses import dataclass
from decimal import Decimal
from importlib.resources import files
from pathlib import Path
from typing import Any
from uuid import uuid4

from .contracts import ModelError

MODEL_VARIABLE = "LLM"
# Researched per-million-token rates (input, output); the ledger refuses to
# price anything else. Add a row with verified rates before selecting a new
# model through the LLM environment variable or inference.toml.
MODEL_PRICING = {"muse-spark-1.3": (Decimal("1.25"), Decimal("4.25"))}
MAX_PROMPT_FILE_BYTES = 32_768
APPROVED_BUDGET_USD = Decimal("150")
MAX_CONTEXT_TOKENS = 1_048_576
MAX_COMPLETION_TOKENS = 4096
MAX_RESPONSE_BYTES = 1_048_576
# Composer requests embed the eligible-model catalog, which outgrew the
# original 32 KiB cap at ~100 models. 1 MiB matches the response cap and the
# 1M-token context; per-call cost still accrues through the ledger. The
# long-term fix is catalog retrieval instead of full-catalog prompts (see
# question-model-discovery-and-selection).
MAX_PROMPT_BYTES = 1_048_576


def load_prompt(filename: str) -> str:
    """Load one editable system prompt; fail closed on missing, empty or oversize files."""
    if (
        not isinstance(filename, str)
        or Path(filename).name != filename
        or not filename.endswith(".md")
    ):
        raise ModelError("Prompt must be a plain Markdown filename inside prompts/.")
    resource = files("connected_models").joinpath("prompts").joinpath(filename)
    try:
        raw = resource.read_bytes()
    except OSError as exc:
        raise ModelError(f"Prompt file {filename} is not readable.") from exc
    if len(raw) > MAX_PROMPT_FILE_BYTES:
        raise ModelError(f"Prompt file {filename} exceeds the size limit.")
    try:
        content = raw.decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise ModelError(f"Prompt file {filename} is not valid UTF-8.") from exc
    if not content:
        raise ModelError(f"Prompt file {filename} is empty.")
    return content


MINOR_UNITS_PER_USD = 1_000_000
API_HOST = "api.meta.ai"
API_PATH = "/v1/chat/completions"
KEY_VARIABLE = "META_API_KEY"
LOGGER = logging.getLogger(__name__)


def _apply_priced_model(
    data: dict[str, Any], model: str, source: str
) -> dict[str, Any]:
    """Apply a priced model selection; unknown models fail closed with a named fix."""
    if model not in MODEL_PRICING:
        known = ", ".join(sorted(MODEL_PRICING))
        raise ModelError(
            f"Unknown model {model!r} in {source}; priced models: {known}. "
            "Add researched rates to MODEL_PRICING first."
        )
    return {
        **data,
        "model": model,
        "input_usd_per_million": float(MODEL_PRICING[model][0]),
        "output_usd_per_million": float(MODEL_PRICING[model][1]),
    }


@dataclass(frozen=True)
class InferenceSettings:
    """Public settings with a ceiling bounded by the user's authorization."""

    model: str
    total_budget_usd: Decimal
    max_completion_tokens: int
    timeout_seconds: int
    input_usd_per_million: Decimal
    output_usd_per_million: Decimal
    reasoning_effort: str = "low"

    @classmethod
    def load(cls, path: Path, model_override: str | None = None) -> "InferenceSettings":
        """Load public TOML settings; explicit override beats the LLM variable beats TOML."""
        with path.open("rb") as handle:
            data = tomllib.load(handle)
        flag = (model_override or "").strip()
        if flag:
            data = _apply_priced_model(data, flag, "--model")
        else:
            override = os.environ.get(MODEL_VARIABLE, "").strip()
            if override:
                data = _apply_priced_model(data, override, MODEL_VARIABLE)
        try:
            settings = cls(
                data["model"],
                Decimal(str(data["total_budget_usd"])),
                data["max_completion_tokens"],
                data["timeout_seconds"],
                Decimal(str(data["input_usd_per_million"])),
                Decimal(str(data["output_usd_per_million"])),
                data.get("reasoning_effort", "low"),
            )
            settings.validate()
            return settings
        except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
            raise ModelError("Invalid public inference configuration.") from exc

    def validate(self) -> None:
        """Reject unknown pricing and accidental budget/limit expansion."""
        if self.model not in MODEL_PRICING:
            known = ", ".join(sorted(MODEL_PRICING))
            raise ModelError(
                f"Unknown model {self.model!r}; priced models: {known}. "
                "Add researched rates to MODEL_PRICING first."
            )
        listed = MODEL_PRICING[self.model]
        if (self.input_usd_per_million, self.output_usd_per_million) != listed:
            raise ModelError(
                f"Rates differ from the verified {self.model} price; reverify before sending."
            )
        if self.reasoning_effort not in {"minimal", "low", "medium", "high"}:
            raise ModelError("Unsupported reasoning effort setting.")
        if (
            not self.total_budget_usd.is_finite()
            or not Decimal(0) < self.total_budget_usd <= APPROVED_BUDGET_USD
        ):
            raise ModelError("Inference budget must be positive and at most $150.")
        if (
            type(self.max_completion_tokens) is not int
            or not 0 < self.max_completion_tokens <= MAX_COMPLETION_TOKENS
        ):
            raise ModelError("Unsupported completion token limit.")
        if type(self.timeout_seconds) is not int or not 0 < self.timeout_seconds <= 120:
            raise ModelError("Timeout must be between 1 and 120 seconds.")

    def cost(self, input_tokens: int, output_tokens: int) -> int:
        """Return conservatively rounded microdollars, ignoring cache discounts."""
        amount = (
            input_tokens * self.input_usd_per_million
            + output_tokens * self.output_usd_per_million
        )
        return int(amount.to_integral_value(rounding="ROUND_CEILING"))


class BudgetLedger:
    """Reserve worst-case cost before requests; retain it on ambiguous failures."""

    def __init__(self, path: Path, settings: InferenceSettings) -> None:
        """Initialize one local ledger, shared by all application inference roles."""
        settings.validate()
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path, self.settings = path, settings
        with closing(sqlite3.connect(path)) as connection, connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS calls (id TEXT PRIMARY KEY, amount INTEGER NOT NULL, state TEXT NOT NULL, model TEXT)"
            )
            columns = {
                row[1]
                for row in connection.execute("PRAGMA table_info(calls)").fetchall()
            }
            if "model" not in columns:
                connection.execute("ALTER TABLE calls ADD COLUMN model TEXT")

    def reserve(self) -> str:
        """Atomically reserve the maximum context plus allowed completion cost."""
        amount = self.settings.cost(
            MAX_CONTEXT_TOKENS, self.settings.max_completion_tokens
        )
        ceiling = int(self.settings.total_budget_usd * MINOR_UNITS_PER_USD)
        call_id = str(uuid4())
        with closing(sqlite3.connect(self.path)) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            spent = connection.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM calls"
            ).fetchone()[0]
            if spent + amount > ceiling:
                raise ModelError(
                    "Inference budget cannot cover the next request; no request was sent."
                )
            connection.execute(
                "INSERT INTO calls VALUES (?, ?, ?, ?)",
                (call_id, amount, "reserved", self.settings.model),
            )
        return call_id

    def settle(self, call_id: str, usage: dict[str, Any]) -> int:
        """Charge trustworthy usage; leave reservations intact on invalid evidence."""
        incoming, outgoing = usage.get("prompt_tokens"), usage.get("completion_tokens")
        if (
            type(incoming) is not int
            or type(outgoing) is not int
            or not 0 <= incoming <= MAX_CONTEXT_TOKENS
            or not 0 <= outgoing <= self.settings.max_completion_tokens
        ):
            raise ModelError(
                "Usage is missing or exceeds configured limits; reservation retained."
            )
        amount = self.settings.cost(incoming, outgoing)
        with closing(sqlite3.connect(self.path)) as connection, connection:
            cursor = connection.execute(
                "UPDATE calls SET amount = ?, state = 'settled' WHERE id = ? AND state = 'reserved'",
                (amount, call_id),
            )
            if cursor.rowcount != 1:
                raise ModelError("Unknown or already settled inference call.")
        return amount

    def summary(self) -> dict[str, Any]:
        """Report only charges/reservations and counts, never prompts or credentials."""
        with closing(sqlite3.connect(self.path)) as connection:
            rows = connection.execute(
                "SELECT state, COUNT(*), SUM(amount) FROM calls GROUP BY state"
            ).fetchall()
            per_model = connection.execute(
                "SELECT COALESCE(model, 'unattributed'), COUNT(*), SUM(amount) FROM calls GROUP BY 1"
            ).fetchall()
        return {
            "budget_usd": float(self.settings.total_budget_usd),
            "groups": {
                state: {
                    "calls": count,
                    "conservative_usd": amount / MINOR_UNITS_PER_USD,
                }
                for state, count, amount in rows
            },
            "by_model": {
                model: {
                    "calls": count,
                    "conservative_usd": amount / MINOR_UNITS_PER_USD,
                }
                for model, count, amount in per_model
            },
        }


def structured_request(
    settings: InferenceSettings,
    ledger: BudgetLedger,
    messages: list[dict[str, str]],
    schema: dict[str, Any],
    name: str,
) -> dict[str, Any]:
    """Send a bounded JSON request; callers validate domain semantics separately."""
    settings.validate()
    key = os.environ.get(KEY_VARIABLE)
    if not key:
        raise ModelError(
            "META_API_KEY is not available to this process. Set it in your launch environment."
        )
    payload = {
        "model": settings.model,
        "messages": messages,
        "max_completion_tokens": settings.max_completion_tokens,
        "reasoning_effort": settings.reasoning_effort,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": name, "schema": schema},
        },
    }
    body = json.dumps(payload).encode()
    if len(body) > MAX_PROMPT_BYTES:
        raise ModelError("Prompt exceeds the configured byte limit.")
    call_id = ledger.reserve()
    connection = http.client.HTTPSConnection(API_HOST, timeout=settings.timeout_seconds)
    try:
        connection.request(
            "POST",
            API_PATH,
            body=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        response = connection.getresponse()
        if response.status != 200:
            raise ModelError(
                f"Meta returned HTTP {response.status}; request {call_id} reservation retained. No automatic retry."
            )
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ModelError(
                "Meta response exceeded the size limit; reservation retained."
            )
        result = json.loads(raw)
        amount = ledger.settle(call_id, result["usage"])
        choice = result["choices"][0]
        if choice["finish_reason"] != "stop":
            raise ModelError(
                f"Meta generation ended with {choice['finish_reason']}; usage recorded. Reasoning and visible output share the token limit."
            )
        raw_content = choice["message"]["content"]
        try:
            content = json.loads(raw_content)
        except (ValueError, TypeError):
            raise ModelError(
                "Meta returned invalid JSON content despite a completed generation; usage recorded."
            ) from None
        if not isinstance(content, dict):
            raise ModelError(
                "Meta responded but failed the structured-output check; usage recorded."
            )
        LOGGER.info(f"Meta structured-output check completed: {call_id}.")
        return {
            "content": content,
            "audit": {
                "model": settings.model,
                "call_id": call_id,
                "conservative_cost_usd": amount / MINOR_UNITS_PER_USD,
            },
        }
    except ModelError:
        LOGGER.warning(
            f"Meta structured request did not complete: {call_id}. Check its ledger entry before retrying."
        )
        raise
    except (
        OSError,
        http.client.HTTPException,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
    ) as exc:
        # Do not log arbitrary exception bodies: a transport can include request data.
        LOGGER.error(
            f"Meta request {call_id} failed with {type(exc).__name__}; no automatic retry."
        )
        raise ModelError(
            "Meta connection or response failed. Inspect the usage ledger before retrying; unverified charges remain reserved."
        ) from None
    finally:
        connection.close()


def text_request(
    settings: InferenceSettings, ledger: BudgetLedger, messages: list[dict[str, str]]
) -> dict[str, Any]:
    """Send a bounded plain-text request; same priced adapter and ledger discipline."""
    settings.validate()
    key = os.environ.get(KEY_VARIABLE)
    if not key:
        raise ModelError(
            "META_API_KEY is not available to this process. Set it in your launch environment."
        )
    payload = {
        "model": settings.model,
        "messages": messages,
        "max_completion_tokens": settings.max_completion_tokens,
        "reasoning_effort": settings.reasoning_effort,
    }
    body = json.dumps(payload).encode()
    if len(body) > MAX_PROMPT_BYTES:
        raise ModelError("Prompt exceeds the configured byte limit.")
    call_id = ledger.reserve()
    connection = http.client.HTTPSConnection(API_HOST, timeout=settings.timeout_seconds)
    try:
        connection.request(
            "POST",
            API_PATH,
            body=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        response = connection.getresponse()
        if response.status != 200:
            raise ModelError(
                f"Meta returned HTTP {response.status}; request {call_id} reservation retained. No automatic retry."
            )
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ModelError(
                "Meta response exceeded the size limit; reservation retained."
            )
        result = json.loads(raw)
        amount = ledger.settle(call_id, result["usage"])
        choice = result["choices"][0]
        if choice["finish_reason"] != "stop":
            raise ModelError(
                f"Meta generation ended with {choice['finish_reason']}; usage recorded. Reasoning and visible output share the token limit."
            )
        content = choice["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise ModelError("Meta returned empty text content; usage recorded.")
        LOGGER.info(f"Meta text request completed: {call_id}.")
        return {
            "text": content,
            "audit": {
                "model": settings.model,
                "call_id": call_id,
                "conservative_cost_usd": amount / MINOR_UNITS_PER_USD,
            },
        }
    except ModelError:
        LOGGER.warning(
            f"Meta text request did not complete: {call_id}. Check its ledger entry before retrying."
        )
        raise
    except (
        OSError,
        http.client.HTTPException,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
    ) as exc:
        # Do not log arbitrary exception bodies: a transport can include request data.
        LOGGER.error(
            f"Meta request {call_id} failed with {type(exc).__name__}; no automatic retry."
        )
        raise ModelError(
            "Meta connection or response failed. Inspect the usage ledger before retrying; unverified charges remain reserved."
        ) from None
    finally:
        connection.close()


def smoke_test(settings: InferenceSettings, ledger: BudgetLedger) -> dict[str, Any]:
    """Check one strict response without storing or exposing credential material."""
    response = structured_request(
        settings,
        ledger,
        [
            {
                "role": "user",
                "content": "Return status ok to confirm a structured-output connection.",
            }
        ],
        {
            "type": "object",
            "properties": {"status": {"type": "string", "enum": ["ok"]}},
            "required": ["status"],
            "additionalProperties": False,
        },
        "ConnectionCheck",
    )
    if response["content"] != {"status": "ok"}:
        raise ModelError(
            "Meta responded but failed the structured-output check; usage recorded."
        )
    return {"status": "ok", **response["audit"]}
