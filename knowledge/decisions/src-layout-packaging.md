---
id: decision-src-layout-packaging
type: decision
title: Source layout and packaging standard
summary: src layout with hatchling packaging, single-source version, console entry point, ruff/pytest/strict-mypy
  gates with CI, and package-data resources; curation kit layout follows with KIT_VERSION 2026-11-04.1.
status: accepted
created: '2026-11-04'
updated: '2026-11-04'
topics:
- architecture
- lifecycle
confidence: null
relations: []
---

# Source layout and packaging standard

## Decision

The repository follows standard Python packaging: `src/connected_models/` built by hatchling, version single-sourced in `pyproject.toml` (0.32.0, read via `importlib.metadata`), a `connected-models` console entry point, dev tooling in the `dev` dependency group, and CI gating ruff check, ruff format, strict mypy and pytest on Python 3.12 and 3.14.

## Context

Hackathon engineering review values visible craft. The prototype had a flat layout, `package = false`, version drift (0.3.0 vs 0.32.0), no lint/type/test configuration, `sys.path` workarounds in every script, CWD- and `__file__`-relative resource loading, and 27 KB of README as the only docs. Branch `chore/python-packaging-craft` restructured this without changing runtime behavior (166 offline tests green throughout).

## Alternatives considered

- Flat layout kept: rejected; `src/` proves the package installs cleanly and prevents accidental imports of the checkout.
- `setuptools` or `setuptools-scm`: rejected; hatchling is the uv default and static versions keep run-manifest provenance legible.
- Pytest-only without unittest compat: rejected; the stdlib fallback (`discover -s tests -t .`) costs nothing and keeps zero-dependency verification possible.
- Mypy lenient or advisory: rejected after measuring; the 88 strict findings were mechanical (annotations, one list/dict variable reuse, duplicate vocab keys) and all were fixed.

## Rationale

- Bundled inputs (LLM prompts, NIST packet) load via `importlib.resources`, so the installed CLI works from any directory; runtime state (`.runs/`, `.registry/`, `.usage/`) and `inference.toml` stay working-directory-relative by design.
- Curation kit archives mirror the `src/` layout so the embedded `pyproject.toml` stays valid; the layout change bumped `KIT_VERSION` to `2026-11-04.1` with older kits still accepted.
- Lint scope is deliberately `E,F,W,I,UP` plus formatting: the broader rule families report 1200+ stylistic findings that would churn the codebase without changing behavior.

## Consequences

- New code must pass `ruff check`, `ruff format --check` and strict `mypy`; tests live in `tests/` as `test_*.py` with shared helpers in `tests/support.py`.
- Commands are `uv run connected-models ...`, `uv run -m evals.run_*_battery`, `uv run pytest -q`; `--cache-dir .uv-cache` was a sandbox workaround and is no longer documented.
- Worker kits now install dev dependencies on sync and carry a non-functional `connected-models` entry point (only 10 modules ship); slimming the kit project file is deferred follow-up, not a blocker, since workers use documented `-m` commands.

## Revisit if

Packaging needs change (namespace plugins, compiled extensions), the kit worker environment needs offline installs, or the project outgrows a single distribution.
