"""Small data-authoring helpers for this curator's returns, outside the toolkit."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

RETURN_ROOT = Path(__file__).resolve().parent
ACCESS_DATE = "2026-11-03"
DOMAIN = "waves-and-optics"
CURATOR = "codex"
BOOK_ROOT = "https://openstax.org/books/"
LICENSE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/"


def source(volume: int, section: str, title: str, locator: str, evidence: str) -> dict[str, Any]:
    """Describe the official live textbook section actually inspected in browsing."""
    publication = "2016-09-19" if volume == 1 else "2016-09-29"
    url = f"{BOOK_ROOT}university-physics-volume-{volume}/pages/{section}"
    return {
        "id": f"os-up{volume}-{section}", "kind": "primary",
        "title": f"OpenStax, University Physics Volume {volume}: {title}",
        "url": url,
        "version": f"Original publication {publication}; live HTML edition inspected {ACCESS_DATE}; footer copyright 2026-06-11. Authors Ling, Sanny, Moebs (Volume 1 lists Moebs first).",
        "accessed": ACCESS_DATE, "locator": locator, "evidence": evidence,
        "license": f"Directly inspected section footer Citation/Attribution and volume Preface, About OpenStax resources / Customization, {BOOK_ROOT}university-physics-volume-{volume}/pages/preface, accessed {ACCESS_DATE}: identifies CC BY-NC-SA 4.0 ({LICENSE_URL}, deed inspected). Footer additionally asserts prior written permission for LLM ingestion/AI offerings and commercial use. The current web version's terms are recorded without inferring an older license or resolving their legal interaction.",
        "redistribution": "Return contains short original evidence paraphrases, mathematical relationships, attribution and numerical data; no source images, pages or PDFs. This is not a legal clearance. Applicability of NC/SA and asserted AI-use restrictions to these research records and downstream commercial/AI use remains an owner rights-review question; no permission obtained or claimed.",
    }


def variable(symbol: str, source_symbol: str, role: str, quantity_id: str, definition: str, unit: str, dimensions: str, context: str, domain: str) -> dict[str, Any]:
    """Build one explicitly defined scalar quantity interface."""
    return dict(symbol=symbol, source_symbol=source_symbol, role=role, quantity_id=quantity_id,
                definition=definition, unit=unit, dimensions=dimensions, context=context, domain=domain)


def reference(identifier: str, inputs: dict[str, float | list[float]], expected: float, tolerance: float, method: str, provenance: str) -> dict[str, Any]:
    """Store an oracle with its actual independence and precision limitations."""
    return dict(id=identifier, inputs=inputs, expected=expected, tolerance=tolerance, method=method, provenance=provenance)


def rejection(inputs: dict[str, float | list[float]], reason: str, kind: str = "domain") -> dict[str, Any]:
    """Build a physical-domain or missing-input rejection case."""
    return dict(kind=kind, inputs=inputs, reason=reason)


def model(slug: str, title: str, summary: str, kind: str, output: str, expression: str,
          original: str, sources: list[dict[str, Any]], locator: str, translation: str,
          variables: list[dict[str, Any]], guards: list[str], assumptions: list[str],
          limitations: list[str], references: list[dict[str, Any]], rejections: list[dict[str, Any]],
          inverse: str, gaps: list[str], constants: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Assemble one research record without manufacturing a runtime projection."""
    return {
        "id": f"{DOMAIN}--{slug}", "revision": "r1", "title": title, "summary": summary,
        "kind": kind,
        "relationship": dict(output_symbol=output, expression=expression, original_equation=original,
                             source_id=sources[0]["id"], locator=locator, translation_notes=translation),
        "variables": variables, "constants": constants or [], "guards": guards,
        "assumptions": assumptions, "limitations": limitations, "unresolved": [], "sources": sources,
        "references": references, "rejection_cases": rejections, "inverse_notes": inverse,
        "integration": dict(status="requires-extension", runtime_model=None, gaps=gaps, duplicate_of=[]),
    }


def write_batch(number: int, models: list[dict[str, Any]], deferred: list[dict[str, Any]], summary: str, notes: str) -> Path:
    """Write this curator's batch while retaining the installed init version fields."""
    batch_id = f"{DOMAIN}-{CURATOR}-b{number:02d}"
    path = RETURN_ROOT / batch_id / "bundle.json"
    template = json.loads(path.read_text(encoding="utf-8"))
    template.update(created=ACCESS_DATE, models=models, deferred=deferred,
                    handoff=dict(summary=summary, gaps=[
                        "Current runtime lacks the proposed optics/wave quantity meanings. Research-only candidates; no publication or scientific approval implied.",
                        "Duplicate search limited to supplied 2026-11-01 inventory (218 records), runtime snapshot and this curator's public returns; no global uniqueness claimed.",
                        "Current OpenStax web terms require rights review before downstream redistribution/use; see each source's license and redistribution fields."
                    ], connections=[], queries=[], review_notes=notes))
    path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def checkpoint(status: str = "in-progress", **updates: Any) -> None:
    """Save measured active-session elapsed time and inventory without touching archives."""
    path = RETURN_ROOT / "SESSION.json"
    session = json.loads(path.read_text(encoding="utf-8"))
    now = datetime.now(UTC)
    start = datetime.fromisoformat(session["started_utc"])
    session.update(checkpoint_utc=now.isoformat(timespec="seconds").replace("+00:00", "Z"),
                   cumulative_useful_work_minutes=round((now - start).total_seconds() / 60, 4),
                   status=status, **updates)
    path.write_text(json.dumps(session, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
