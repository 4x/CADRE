"""Validate domain-independent query facts and ground each value in the user's text."""

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from .contracts import (
    UNIT_ALIASES,
    UNITS,
    ModelError,
    Port,
    Value,
    finite,
    normalize_unit_spelling,
)
from .serialization import MAX_RECORD_BYTES, object_fields, text

MAX_QUERY_CHARS = 16_384
MAX_QUERY_FACTS = 64
NUMBER_PATTERN = re.compile(
    r"[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?"
)
LEXICAL_UNITS = "|".join(
    re.escape(name)
    for name in sorted(set(UNIT_ALIASES) | set(UNITS), key=len, reverse=True)
    if name != "1"
)
UNIT_PATTERN = re.compile(
    r"\s*((?:USD|dollars?)\s*(?:/|per)\s*kWh|" + LEXICAL_UNITS + r"|years?)(?![\w/^²])",
    re.IGNORECASE,
)


def unit_identity(unit: str) -> str:
    """Resolve a lexical spelling to a canonical unit; unknown spellings pass through for explicit rejection."""
    stripped = unit.strip() if isinstance(unit, str) else ""
    if stripped in UNITS:
        return stripped  # Canonical case first: SI case pairs (S/s) would merge under normalization.
    normalized = normalize_unit_spelling(unit)
    return UNIT_ALIASES.get(normalized, normalized)


def validate_fact(
    raw: dict[str, Any], question: str, fill_in_assumptions: bool = False
) -> dict[str, Any]:
    """Preserve literal evidence and reject invented/normalized numeric or date inputs.

    Assumed facts (non-empty assumption) are accepted only when assumption
    filling is enabled: their quote must still occur in the question as the
    implying phrase, but the value need not occur in the quote."""
    object_fields(
        raw, {"id", "name", "value_type", "value", "unit", "quote"}, {"assumption"}
    )
    assumption = raw.get("assumption", "")
    if not isinstance(assumption, str) or len(assumption) > MAX_RECORD_BYTES:
        raise ModelError("Fact assumption must be a bounded string.")
    fact: dict[str, Any] = {
        key: text(value) for key, value in raw.items() if key != "assumption"
    }
    fact["assumption"] = assumption
    assumed = bool(assumption.strip())
    if assumed and not fill_in_assumptions:
        raise ModelError(
            "Assumed values require assumption filling to be enabled for this request."
        )
    if fact["quote"] not in question:
        raise ModelError(
            "An extracted value and its exact quote must occur in the question."
        )
    if not assumed and fact["value"] not in fact["quote"]:
        raise ModelError(
            "An extracted value and its exact quote must occur in the question."
        )
    fact["assumed"] = assumed
    start = question.index(fact["quote"])
    fact["source_span"] = {"start": start, "end": start + len(fact["quote"])}
    if fact["value_type"] == "number":
        literal = fact["value"]
        if NUMBER_PATTERN.fullmatch(literal) is None:
            raise ModelError(
                "Numeric inputs currently require an explicit digit literal in the query."
            )
        # Prevent '5' being presented as evidence for a user literal '15' or '0.05'.
        # Assumed values are exempt: they are documented implications, not quotations.
        if not assumed:
            numeric_mentions = [
                match.group() for match in NUMBER_PATTERN.finditer(fact["quote"])
            ]
            if literal not in numeric_mentions:
                raise ModelError(
                    "Extracted numeric literal does not match a complete number in its quote."
                )
            mention = next(
                match
                for match in NUMBER_PATTERN.finditer(fact["quote"])
                if match.group() == literal
            )
            tail = fact["quote"][mention.end() :]
            explicit = UNIT_PATTERN.match(tail)
            source_unit = explicit.group(1) if explicit else None
            if fact["quote"][:mention.start()].rstrip().endswith("$"):
                # A "$50 per unit" price carries its denominator in the tail;
                # only phrasing before any further number belongs to this one.
                head = NUMBER_PATTERN.split(tail, maxsplit=1)[0]
                per = re.search(r"(?:\bper\s+|/\s*)([A-Za-z][\w^]*)", head)
                source_unit = f"USD/{per.group(1)}" if per else "USD"
            else:
                # "Per" phrasing ("15 mg per kg") otherwise misreads as its
                # numerator prefix ("mg"); retry with "per" squeezed to "/"
                # and prefer the reading that agrees with the stated unit.
                squeezed = UNIT_PATTERN.match(re.sub(r"\s+per\s+", "/", tail))
                squeezed_unit = squeezed.group(1) if squeezed else None
                if squeezed_unit is not None and (
                    source_unit is None
                    or unit_identity(squeezed_unit) == unit_identity(fact["unit"])
                ):
                    source_unit = squeezed_unit
            if source_unit and unit_identity(source_unit) != unit_identity(
                fact["unit"]
            ):
                raise ModelError(
                    "Extracted unit contradicts the explicit unit next to the number in the question."
                )
        try:
            fact["amount"] = finite(
                float(Decimal(literal.replace(",", ""))), "Query amount"
            )
        except (InvalidOperation, OverflowError) as exc:
            raise ModelError(
                "Numeric query input is outside the supported range."
            ) from exc
    elif fact["value_type"] == "date":
        # Retain the source string, including dates not yet normalized/executable.
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fact["value"]):
            try:
                date.fromisoformat(fact["value"])
            except ValueError as exc:
                raise ModelError(
                    "The query contains an invalid ISO calendar date."
                ) from exc
    elif fact["value_type"] != "text":
        raise ModelError("Unsupported query value type.")
    return fact


def bind_fact(fact: dict[str, Any], target: Port) -> Value:
    """Bind only a cited scalar, retaining its unit; do no agent arithmetic or defaults."""
    if fact["value_type"] != "number":
        raise ModelError(
            f"{fact['name']}: {fact['value_type']} inputs cannot execute in the current scalar engine."
        )
    normalized_unit = unit_identity(fact["unit"])
    if normalized_unit == "years" and target.meaning == "period_count":
        unit = "1"  # The model declares an integer number of annual periods.
    else:
        unit = normalized_unit
    if unit not in UNITS:
        raise ModelError(
            f"{fact['name']}: unit {fact['unit']} is unspecified or unsupported for execution."
        )
    evidence = f"Query fact {fact['id']} ({fact['name']}), span {fact['source_span']}: {fact['quote']}"
    if fact.get("assumed"):
        evidence += f" [assumed: {fact.get('assumption', '')}]"
    value = Value(
        fact["amount"],
        Port(target.meaning, unit, target.context),
        "user-scenario",
        evidence,
    )
    value.bind(target)
    return value
