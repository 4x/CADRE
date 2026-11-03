# Correction brief: named speed of light for waves record (r2 × 1)

To: waves-and-optics curator (batch codex-b02)
From: dev intake, 2026-11-03
Status: needs-revision (mechanical, not scientific — the review stands as recommend-admit)

## What happened

`waves-and-optics--refractive-index-phase-speed` passed scientific review
(recommend-admit, reviewer AG) but cannot project: it inlines `299792458`
(the vacuum speed of light in m/s) as a bare literal, which the engine
reads as dimensionless, so staging fails fail-closed with
`Expression/output dimensions differ`. No evidence was questioned and
nothing was modified.

## Fix: name the registry constant

Runtime 0.28.0 resolves `speed_of_light` (299792458 m/s, SI defining
constant, exact) inside expressions. Rewrite (nothing else changes —
same variables, ports, units, references, guards, sources):

- `waves-and-optics--refractive-index-phase-speed` (codex-b02, r1 → r2)
  - `299792458 / n` → `speed_of_light / n`

Cite `speed_of_light` in `translation_notes`; drop the inlined entry
from `constants` metadata (registry-named values are not repeated
there).

## References: no changes needed

The registry value is digit-identical to the inlined literal (exact SI
defining constant, exactly representable), so every `inputs`,
`expected`, `tolerance`, and `method` stays byte-identical.

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as
usual) for re-review per protocol since record text changes.
