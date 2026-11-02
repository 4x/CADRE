"""Versioned, portable research handoff schema and its dependency-free validator."""

import math
import re
from typing import Any

from .contracts import ModelError

SCHEMA_VERSION = "cm-curation-batch/1"
KIT_VERSION = "2026-10-31.6"
SUPPORTED_KIT_VERSIONS = ("2026-10-31.1", "2026-10-31.2", "2026-10-31.3", "2026-10-31.4", "2026-10-31.5", KIT_VERSION)
MAX_MODELS = 12
MAX_BATCH_BYTES = 1_048_576
DOMAINS = ("building-energy", "engineering-finance", "electric-circuits", "water-hydraulics", "classical-mechanics", "probability",
           "economics", "computer-science", "chemistry", "biology",
           # Wave-2 breadth lanes (assignments staged in data/curation/wave2/).
           "statistics", "materials-science", "thermodynamics",
           # Wave-3 breadth lanes (assignments staged in data/curation/wave3/).
           "structural-mechanics", "waves-and-optics", "demography", "clinical-arithmetic",
           "environmental-accounting", "orbital-mechanics")
STRING = {"type": "string", "minLength": 1, "maxLength": 4096}
NUMBER = {"type": "number"}
IDENTIFIER = {**STRING, "pattern": "^[a-z][a-z0-9-]{0,95}$"}
SYMBOL = {**STRING, "pattern": "^[A-Za-z][A-Za-z0-9_]{0,63}$"}
DATE = {**STRING, "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}


def array(items: dict[str, Any], minimum: int = 0, maximum: int = 40) -> dict[str, Any]:
    """Describe a bounded array in the shared JSON Schema subset."""
    return {"type": "array", "items": items, "minItems": minimum, "maxItems": maximum}


def record(properties: dict[str, Any], optional: tuple[str, ...] = ()) -> dict[str, Any]:
    """Require every declared field and reject undeclared fields, except listed optional fields."""
    return {"type": "object", "properties": properties,
            "required": [name for name in properties if name not in optional], "additionalProperties": False}


def choice(*values: str) -> dict[str, Any]:
    """Describe an exact string enumeration."""
    return {**STRING, "enum": list(values)}


PORT = record({"meaning": STRING, "unit": STRING, "context": STRING})
FAMILY_PORT = record({"meaning": STRING, "unit": STRING, "context": STRING, "max_size": NUMBER})
RUNTIME_MODEL = record({
    "id": IDENTIFIER, "version": IDENTIFIER,
    "inputs": {"type": "object", "minProperties": 0, "maxProperties": 16, "additionalProperties": PORT},
    "output": PORT, "expression": STRING, "guards": array(STRING), "source": STRING, "assumptions": array(STRING, 1),
    "families": {"type": "object", "maxProperties": 16, "additionalProperties": FAMILY_PORT},
}, ("families",))
INPUT_VALUE = {"type": ["number", "array"], "items": NUMBER, "minItems": 1, "maxItems": 256}
INPUTS = {"type": "object", "minProperties": 1, "maxProperties": 16, "additionalProperties": INPUT_VALUE}
SOURCE = record({
    "id": IDENTIFIER, "kind": choice("primary", "project-derivation"), "title": STRING,
    "url": {"type": ["string", "null"], "minLength": 1, "maxLength": 4096},
    "version": STRING, "accessed": DATE, "locator": STRING, "evidence": STRING,
    "license": STRING, "redistribution": STRING,
})
VARIABLE = record({
    "symbol": SYMBOL, "source_symbol": STRING, "role": choice("input", "output", "family"),
    "quantity_id": STRING, "definition": STRING, "unit": STRING, "dimensions": STRING,
    "context": STRING, "domain": STRING, "max_size": NUMBER,
}, ("max_size",))
MODEL = record({
    "id": IDENTIFIER, "revision": IDENTIFIER, "title": STRING, "summary": STRING,
    "kind": choice("definition", "theoretical", "empirical"),
    "relationship": record({"output_symbol": SYMBOL, "expression": STRING, "original_equation": STRING,
                            "source_id": IDENTIFIER, "locator": STRING, "translation_notes": STRING}),
    "variables": array(VARIABLE, 2, 17),
    "constants": array(record({"literal": NUMBER, "meaning": STRING, "unit": STRING, "source_id": IDENTIFIER, "locator": STRING})),
    "guards": array(STRING), "assumptions": array(STRING, 1), "limitations": array(STRING, 1), "unresolved": array(STRING),
    "sources": array(SOURCE, 1, 10),
    "references": array(record({"id": IDENTIFIER, "inputs": INPUTS, "expected": NUMBER,
                                "tolerance": {**NUMBER, "exclusiveMinimum": 0}, "method": STRING, "provenance": STRING}), 2, 10),
    "rejection_cases": array(record({"kind": choice("domain", "missing-input"), "inputs": {**INPUTS, "minProperties": 0}, "reason": STRING}), 1, 10),
    "inverse_notes": STRING,
    "integration": record({"status": choice("runtime-ready", "requires-extension", "blocked"),
                           "runtime_model": {**RUNTIME_MODEL, "type": ["object", "null"]},
                           "gaps": array(STRING), "duplicate_of": array(STRING)}),
})
SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Connected Models portable offline curation batch, version 1",
    **record({
        "schema_version": choice(SCHEMA_VERSION), "kit_version": choice(*SUPPORTED_KIT_VERSIONS), "batch_id": IDENTIFIER,
        "domain": choice(*DOMAINS), "curator": STRING, "created": DATE, "example_only": {"type": "boolean"},
        "models": array(MODEL, 1, MAX_MODELS),
        "deferred": array(record({"title": STRING, "reason": STRING, "source_urls": array(STRING)})),
        "handoff": record({"summary": STRING, "gaps": array(STRING), "connections": array(STRING),
                           "queries": array(STRING), "review_notes": STRING}),
    }),
}


def validate_schema(value: Any, schema: dict[str, Any] = SCHEMA, path: str = "$", depth: int = 0) -> None:
    """Validate our fixed schema subset; this is not a general JSON Schema engine."""
    if depth > 16:
        raise ModelError(f"{path}: nesting limit exceeded.")
    types = schema["type"]
    allowed = types if isinstance(types, list) else [types]
    actual = ("null" if value is None else "boolean" if isinstance(value, bool) else
              "number" if isinstance(value, (float, int)) else "string" if isinstance(value, str) else
              "array" if isinstance(value, list) else "object" if isinstance(value, dict) else "unknown")
    if actual not in allowed:
        raise ModelError(f"{path}: expected {allowed}, got {actual}.")
    if "enum" in schema and value not in schema["enum"]:
        raise ModelError(f"{path}: expected one of {schema['enum']}.")
    if actual == "number":
        try:
            valid = math.isfinite(value)
        except OverflowError:
            valid = False
        if not valid or ("exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]):
            raise ModelError(f"{path}: invalid finite numeric value or bound.")
    elif actual == "string":
        if not value.strip() or not schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", 4096):
            raise ModelError(f"{path}: invalid string length.")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            raise ModelError(f"{path}: invalid identifier/date format.")
    elif actual == "array":
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", 40):
            raise ModelError(f"{path}: invalid array length.")
        for index, item in enumerate(value):
            validate_schema(item, schema["items"], f"{path}[{index}]", depth + 1)
    elif actual == "object":
        if not schema.get("minProperties", 0) <= len(value) <= schema.get("maxProperties", 64):
            raise ModelError(f"{path}: invalid object size.")
        properties = schema.get("properties", {})
        if not set(schema.get("required", [])) <= value.keys():
            raise ModelError(f"{path}: missing {sorted(set(schema['required']) - value.keys())}.")
        additional = schema.get("additionalProperties", False)
        for name, item in value.items():
            if name in properties:
                child = properties[name]
            elif isinstance(additional, dict):
                child = additional
            else:
                raise ModelError(f"{path}: unknown field {name}.")
            validate_schema(item, child, f"{path}.{name}", depth + 1)
