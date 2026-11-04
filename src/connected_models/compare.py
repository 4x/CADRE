"""Side-by-side comparison of the grounded route and a direct LLM answer.

The grounded route runs the normal compose-and-execute path; the direct
route sends the same question to the same priced model with no catalog,
no tools, and no engine. Numeric agreement treats the executed engine
outputs as the oracle: disagreements need human adjudication, which is
exactly what the side-by-side record is for.
"""

from __future__ import annotations

import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from .contracts import UNITS, ModelError
from .inference import BudgetLedger, InferenceSettings, load_prompt, text_request
from .query_inputs import MAX_QUERY_CHARS, unit_identity
from .registry import Registry
from .runtime import save_run
from .serialization import text
from .workflows import answer

DIRECT_PROMPT_FILE = "direct-answer.md"
AGREEMENT_TOLERANCE = 0.01
RUNS_PATH = Path(".runs")

NUMERIC_PATTERN = re.compile(r"-?\d[\d,]*\.?\d*(?:[eE]-?\d+)?")
PAIR_PATTERN = re.compile(
    r"(-?\d[\d,]*\.?\d*(?:[eE]-?\d+)?)\s*([A-Za-z$%/\^0-9².]*[A-Za-z$%²])?"
)


def extract_numbers(direct_text: str) -> list[float]:
    """Pull every decimal literal from direct prose for agreement checks."""
    numbers = []
    for match in NUMERIC_PATTERN.finditer(direct_text):
        try:
            numbers.append(float(match.group(0).replace(",", "")))
        except ValueError:
            continue
    return numbers


def extract_pairs(direct_text: str) -> list[tuple[float, str]]:
    """Pull number-plus-unit-word pairs; the unit word may be empty."""
    pairs = []
    for match in PAIR_PATTERN.finditer(direct_text):
        try:
            amount = float(match.group(1).replace(",", ""))
        except ValueError:
            continue
        pairs.append((amount, (match.group(2) or "").rstrip(".")))
    return pairs


def numeric_agreement(
    grounded: dict[str, Any], direct_text: str, tolerance: float = AGREEMENT_TOLERANCE
) -> dict[str, Any]:
    """Check each executed output amount against the direct answer's numbers.

    A direct number matches when it equals the engine amount in canonical
    units (the number's unit word converts through the registry scales, so
    6.6 mL matches 6.6e-6 m^3), or falls back to raw and percent phrasing
    when no unit word converts. Pairs whose units convert to a different
    dimension never match. Blocked or rejected grounded runs are unjudged:
    there is no oracle to compare against."""
    if grounded.get("status") != "completed":
        return {
            "verdict": "unjudged",
            "reason": f"grounded run {grounded.get('status')}; no oracle outputs",
            "details": [],
        }
    pairs = extract_pairs(direct_text)
    if not pairs:
        return {
            "verdict": "unjudged",
            "reason": "no numbers in the direct answer",
            "details": [],
        }
    details = []
    expanded: dict[str, Any] = {}
    for node_id, value in (grounded.get("outputs") or {}).items():
        if value.get("amounts") is not None:
            for position, amount in enumerate(value["amounts"]):
                expanded[f"{node_id}[{position}]"] = {
                    "amount": amount,
                    "port": value["port"],
                }
        else:
            expanded[node_id] = value
    for node_id, value in expanded.items():
        expected = value["amount"]
        target = UNITS.get(value["port"]["unit"])
        scored = []
        for found, word in pairs:
            canonical = unit_identity(word) if word else ""
            if (
                canonical in UNITS
                and target is not None
                and UNITS[canonical].dimensions == target.dimensions
            ):
                mine, theirs = found * UNITS[canonical].scale, expected * target.scale
            else:
                mine, theirs = found, expected
                if abs(mine - theirs) > tolerance * max(abs(theirs), 1e-9):
                    theirs = expected * 100  # Percent phrasing without a unit word.
            denom = max(abs(theirs), 1e-9)
            if abs(mine - theirs) <= tolerance * denom:
                scored.append((abs(mine - theirs) / denom, found))
        matched = min(scored)[1] if scored else None
        details.append(
            {
                "node": node_id,
                "meaning": value["port"]["meaning"],
                "unit": value["port"]["unit"],
                "expected": expected,
                "matched": matched,
            }
        )
    verdict = (
        "agree"
        if details and all(item["matched"] is not None for item in details)
        else "disagree"
    )
    return {"verdict": verdict, "details": details}


def direct_answer(question: str, inference_model: str | None = None) -> dict[str, Any]:
    """Answer with the same priced model and ledger, minus everything else."""
    settings = InferenceSettings.load(Path("inference.toml"), inference_model)
    response = text_request(
        settings,
        BudgetLedger(Path(".usage/meta.sqlite3"), settings),
        [
            {"role": "system", "content": load_prompt(DIRECT_PROMPT_FILE)},
            {"role": "user", "content": question},
        ],
    )
    return {
        "run_id": str(uuid4()),
        "created": datetime.now(UTC).isoformat(),
        "question": question,
        "direct_text": response["text"],
        "inference": response["audit"],
    }


def compare(
    registry: Registry,
    question: str,
    fill_in_assumptions: bool = False,
    inference_model: str | None = None,
) -> dict[str, Any]:
    """Run grounded and direct routes on one question and compare them."""
    text(question)
    if len(question) > MAX_QUERY_CHARS:
        raise ModelError("Question is too long.")
    started = time.perf_counter()
    grounded = answer(registry, question, fill_in_assumptions, inference_model)
    grounded_latency = time.perf_counter() - started
    try:
        started = time.perf_counter()
        direct = direct_answer(question, inference_model)
        direct["latency_s"] = time.perf_counter() - started
    except (ModelError, OSError, ValueError) as exc:
        direct = {
            "run_id": str(uuid4()),
            "created": datetime.now(UTC).isoformat(),
            "question": question,
            "error": str(exc),
            "latency_s": None,
        }
    if "direct_text" in direct:
        direct_path = save_run(direct, RUNS_PATH)
        direct["saved_path"] = str(direct_path)
    used_model = grounded.get("model") or (direct.get("inference") or {}).get("model")
    record = {
        "comparison_id": str(uuid4()),
        "created": datetime.now(UTC).isoformat(),
        "question": question,
        "model": used_model,
        "grounded": {
            "run_id": grounded.get("run_id"),
            "saved_path": str(grounded.get("saved_path") or ""),
            "status": grounded.get("status"),
            "outputs": grounded.get("outputs"),
            "assumptions": grounded.get("assumptions"),
            "attempts": len(grounded.get("attempts") or []),
            "latency_s": grounded_latency,
            "error": grounded.get("error"),
        },
        "direct": {
            "run_id": direct.get("run_id"),
            "saved_path": str(direct.get("saved_path") or ""),
            "latency_s": direct.get("latency_s"),
            "inference": direct.get("inference"),
            "error": direct.get("error"),
            "direct_text": direct.get("direct_text", "")[:4000],
        },
        "agreement": numeric_agreement(grounded, direct.get("direct_text", "")),
    }
    record["run_id"] = record["comparison_id"]
    path = save_run(record, RUNS_PATH)
    return {**record, "saved_path": str(path)}
