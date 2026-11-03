# Correction brief: named registry constants for orbital records (r2 × 7)

To: orbital-mechanics curator (batches a-b03, a-b04, a-b05)
From: dev intake, 2026-11-03
Status: needs-revision (mechanical, not scientific — the reviews stand as recommend-admit)

## What happened

Seven records below passed scientific review (recommend-admit, reviewer AF)
but cannot project: each inlines `6.67e-11` (G, 3 s.f.) as a bare literal,
and one also inlines `39.47841760435743` (4π²). The engine reads bare
literals as dimensionless, so staging fails fail-closed with
`Expression/output dimensions differ`. An eighth record, mean-motion,
stages (its inlined `6.283185307179586` is genuinely dimensionless) but is
held unstaged-unadmitted under the named-constants rule per the 4π²
precedent: universal constants ride registry names, never literals. No
evidence was questioned and nothing was modified.

## Fix: name the registry constants

Runtime 0.23.0+ resolves `gravitational_constant` (6.67430e-11 m3/(kg*s^2),
CODATA 2022) and `pi` inside expressions, converting through the registry
scales. Rewrite (nothing else changes — same variables, ports, units,
references, guards, sources):

1. `orbital-mechanics--mean-motion-from-period` (a-b03, r1 → r2)
   - `6.283185307179586 / T` → `2 * pi / T`
2. `orbital-mechanics--circular-orbit-specific-angular-momentum-squared` (a-b03, r1 → r2)
   - `6.67e-11 * M * r` → `gravitational_constant * M * r`
3. `orbital-mechanics--central-mass-from-surface-gravity` (a-b03, r1 → r2)
   - `g * R ** 2 / 6.67e-11` → `g * R ** 2 / gravitational_constant`
4. `orbital-mechanics--kepler-third-law-binary-period-squared` (a-b04, r1 → r2)
   - `39.47841760435743 * a ** 3 / (6.67e-11 * (M1 + M2))` →
     `4 * pi ** 2 * a ** 3 / (gravitational_constant * (M1 + M2))`
5. `orbital-mechanics--gravitational-potential-energy` (a-b04, r1 → r2)
   - `-6.67e-11 * M * m / r` → `-gravitational_constant * M * m / r`
6. `orbital-mechanics--circular-orbit-kinetic-energy` (a-b04, r1 → r2)
   - `6.67e-11 * m * M / (2 * r)` → `gravitational_constant * m * M / (2 * r)`
7. `orbital-mechanics--vis-viva-velocity-squared` (a-b05, r1 → r2)
   - `6.67e-11 * (M1 + M2) * (2 / r - 1 / a)` →
     `gravitational_constant * (M1 + M2) * (2 / r - 1 / a)`

In each record: cite the registry names in `translation_notes`; drop the
inlined G / 2π / 4π² entries from `constants` metadata (registry-named
values are not repeated there).

## References: no changes needed

All seventeen reference expectations already fit their tolerances under the
registry values (verified by intake probe
`.runs/review-2026-11-02-wave3/work/probe-orbital-b03-b05-r2-gfit.py`: G
moves results ~0.06%, inside every published-oracle bound; 2π is
digit-identical). Keep every `inputs`, `expected`, `tolerance`, and
`method` byte-identical.

## Resubmission

Submit the seven r2 records as a small correction batch (bundle + return
as usual). This is a mechanical expression swap with unchanged
expectations, but resubmit for re-review per protocol since record text
changes. Note: `orbital-mechanics--hyperbolic-excess-velocity-squared`
is separately needs-revision on its `v` dimensions declaration (reviewer
AF blocker); when it is re-issued, its inlined `6.67e-11` must likewise
become `gravitational_constant` (its two references also fit unchanged —
see the probe output).
