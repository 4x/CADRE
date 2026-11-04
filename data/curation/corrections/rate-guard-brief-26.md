# Correction brief: finite rate upper guard for uniform-present-value (brief 26)

To: rate-guard curator (batch engineering-finance-rateguard-b01, 1 revised record)
From: dev, 2026-11-04
Status: prescribed (mechanical — no admitted record is revised; all reviews stand)

## What happened

The admitted `uniform-present-value@source-3`
(`annual * ((1 + rate) ** years - 1) / (rate * (1 + rate) ** years)`,
guards `rate > 0`, `years >= 1`, `years <= 100`) carries no explicit finite
upper bound on `rate`. The project fixture it descends from
(`uniform-present-value@1` in `connected_models/demo.py`, NIST-sourced)
carries `rate <= 1`; the admitted revision dropped it. Without a finite
bracket, implied-rate inversion is unreachable: exact solving reports
`unsupported_degree` and bracketed bisection correctly refuses for lack of
guards (`unbounded_search` peek fails, original diagnostic preserved).

No evidence was questioned and nothing was modified; `@source-3` stands as
reviewed for all forward and period-count views.

## Prescription

Author the next research revision of `uniform-present-value` (next after
`source-3` per kit convention) in a fresh batch
`engineering-finance-rateguard-b01` (single record), restoring an explicit
finite rate upper guard. Everything else — expression, variables, units,
contexts, remaining guards, assumptions — stays byte-identical to `source-3`
unless the sources demand otherwise.

REQUIRED:

- The bound (e.g. the fixture's `rate <= 1`) must be justified from the
  model's published sources, not convenience: cite the scope that bounds
  the periodic rate, and record the NIST lead from the fixture as checked
  or superseded with reason.
- At least one reference must exercise the implied-rate view: a published
  present-value case recomputed by solving for `rate` (documents the
  bisection path the bound unlocks), plus the usual forward references.
- Rejection cases cover the new bound (above-bound rate rejected) alongside
  the existing rate/years domains.

## Resubmission

Validate, pack, and report bundle + return-ZIP verification hashes with each
hash labeled by artifact. Intake will packet the return for independent
re-review; on admission, a live implied-rate battery entry follows.
