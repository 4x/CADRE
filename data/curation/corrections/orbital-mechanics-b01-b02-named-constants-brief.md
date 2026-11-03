# Correction brief: named registry constants for orbital records (r2 × 6)

To: orbital-mechanics curator (batches a-b01, a-b02)
From: dev intake, 2026-11-03
Status: needs-revision (mechanical, not scientific — the reviews stand as recommend-admit)

## What happened

The six records below passed scientific review (recommend-admit, reviewer AE)
but cannot project: each inlines `6.67e-11` (G, 3 s.f.) as a bare literal,
and two also inline `39.47841760435743` (4π²). The engine reads bare literals
as dimensionless, so staging fails fail-closed with `Expression/output
dimensions differ` (e.g. Kepler evaluates to length³/mass instead of time²).
No evidence was questioned and nothing was modified.

## Fix: name the registry constants

Runtime 0.23.0+ resolves `gravitational_constant` (6.67430e-11 m3/(kg*s^2),
CODATA 2022) and `pi` inside expressions, converting through the registry
scales. Rewrite (nothing else changes — same variables, ports, units,
references, guards, sources):

1. `orbital-mechanics--kepler-third-law-period-squared` (a-b01, r1 → r2)
   - `39.47841760435743 * a ** 3 / (6.67e-11 * M)` →
     `4 * pi ** 2 * a ** 3 / (gravitational_constant * M)`
2. `orbital-mechanics--circular-orbit-velocity-squared` (a-b01, r1 → r2)
   - `6.67e-11 * M / r` → `gravitational_constant * M / r`
3. `orbital-mechanics--standard-gravitational-parameter` (a-b02, r1 → r2)
   - `6.67e-11 * M` → `gravitational_constant * M`
4. `orbital-mechanics--circular-orbit-total-energy` (a-b02, r1 → r2)
   - `-6.67e-11 * m * M / (2 * r)` → `-gravitational_constant * m * M / (2 * r)`
5. `orbital-mechanics--circular-orbit-velocity-squared-kinematic` (a-b02, r1 → r2)
   - `39.47841760435743 * r ** 2 / T ** 2` → `4 * pi ** 2 * r ** 2 / T ** 2`
6. `orbital-mechanics--escape-velocity-squared` (a-b02, r1 → r2)
   - `2 * 6.67e-11 * M / R` → `2 * gravitational_constant * M / R`

In each record: cite the registry names in `translation_notes`; drop the
inlined G / 4π² entries from `constants` metadata (registry-named values
are not repeated there).

## References: no changes needed

All twelve reference expectations already fit their tolerances under the
registry values (verified by intake: G moves results ~0.06%, inside every
published-oracle bound; 4π² is digit-identical). Keep every `inputs`,
`expected`, `tolerance`, and `method` byte-identical.

## Resubmission

Submit the six r2 records as a small correction batch (bundle + return as
usual). This is a mechanical expression swap with unchanged expectations,
but resubmit for re-review per protocol since record text changes.
