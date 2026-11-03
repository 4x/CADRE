"""Validate domain-independent query facts and ground each value in the user's text."""

from datetime import date
from decimal import Decimal, InvalidOperation
import re
from typing import Any

from .contracts import UNIT_ALIASES, ModelError, Port, UNITS, Value, finite, normalize_unit_spelling
from .serialization import object_fields, text

MAX_QUERY_CHARS = 16_384
MAX_QUERY_FACTS = 64
NUMBER_PATTERN = re.compile(r"[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?")
LEXICAL_UNITS = "|".join(re.escape(name) for name in sorted(set(UNIT_ALIASES) | set(UNITS), key=len, reverse=True) if name != "1")
UNIT_PATTERN = re.compile(r"\s*((?:USD|dollars?)\s*(?:/|per)\s*kWh|" + LEXICAL_UNITS + r"|years?)(?![\w/^²])", re.IGNORECASE)


def unit_identity(unit: str) -> str:
    """Resolve a lexical spelling to a canonical unit; unknown spellings pass through for explicit rejection."""
    stripped = unit.strip() if isinstance(unit, str) else ""
    if stripped in UNITS:
        return stripped  # Canonical case first: SI case pairs (S/s) would merge under normalization.
    normalized = normalize_unit_spelling(unit)
    return UNIT_ALIASES.get(normalized, normalized)


def validate_fact(raw: dict[str, Any], question: str) -> dict[str, Any]:
    """Preserve literal evidence and reject invented/normalized numeric or date inputs."""
    object_fields(raw, {"id", "name", "value_type", "value", "unit", "quote"})
    fact = {key: text(value) for key, value in raw.items()}
    if fact["quote"] not in question or fact["value"] not in fact["quote"]:
        raise ModelError("An extracted value and its exact quote must occur in the question.")
    start = question.index(fact["quote"])
    fact["source_span"] = {"start": start, "end": start + len(fact["quote"])}
    if fact["value_type"] == "number":
        literal = fact["value"]
        if NUMBER_PATTERN.fullmatch(literal) is None:
            raise ModelError("Numeric inputs currently require an explicit digit literal in the query.")
        # Prevent '5' being presented as evidence for a user literal '15' or '0.05'.
        numeric_mentions = [match.group() for match in NUMBER_PATTERN.finditer(fact["quote"])]
        if literal not in numeric_mentions:
            raise ModelError("Extracted numeric literal does not match a complete number in its quote.")
        mention = next(match for match in NUMBER_PATTERN.finditer(fact["quote"]) if match.group() == literal)
        tail = fact["quote"][mention.end():]
        explicit = UNIT_PATTERN.match(tail)
        source_unit = explicit.group(1) if explicit else None
        if fact["quote"][:mention.start()].rstrip().endswith("$"):
            source_unit = "USD/kWh" if re.match(r"\s*/\s*kWh", tail, re.IGNORECASE) else "USD"
        if source_unit and unit_identity(source_unit) != unit_identity(fact["unit"]):
            raise ModelError("Extracted unit contradicts the explicit unit next to the number in the question.")
        try:
            fact["amount"] = finite(float(Decimal(literal.replace(",", ""))), "Query amount")
        except (InvalidOperation, OverflowError) as exc:
            raise ModelError("Numeric query input is outside the supported range.") from exc
    elif fact["value_type"] == "date":
        # Retain the source string, including dates not yet normalized/executable.
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fact["value"]):
            try:
                date.fromisoformat(fact["value"])
            except ValueError as exc:
                raise ModelError("The query contains an invalid ISO calendar date.") from exc
    elif fact["value_type"] != "text":
        raise ModelError("Unsupported query value type.")
    return fact


def bind_fact(fact: dict[str, Any], target: Port) -> Value:
    """Bind only a cited scalar, retaining its unit; do no agent arithmetic or defaults."""
    if fact["value_type"] != "number":
        raise ModelError(f"{fact['name']}: {fact['value_type']} inputs cannot execute in the current scalar engine.")
    normalized_unit = unit_identity(fact["unit"])
    if normalized_unit == "years" and target.meaning == "period_count":
        unit = "1"  # The model declares an integer number of annual periods.
    else:
        unit = normalized_unit
    if unit not in UNITS:
        raise ModelError(f"{fact['name']}: unit {fact['unit']} is unspecified or unsupported for execution.")
    evidence = f"Query fact {fact['id']} ({fact['name']}), span {fact['source_span']}: {fact['quote']}"
    value = Value(fact["amount"], Port(target.meaning, unit, target.context), "user-scenario", evidence)
    value.bind(target)
    return value
