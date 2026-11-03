# Correction brief: named registry constant for radiative exchange (r2)

To: building-energy curator (batch be-a-b04)
From: dev intake, 2026-11-01
Status: needs-revision (mechanical, not scientific — the review stands as recommend-admit)

Note: this brief supersedes the earlier sigma-as-input direction. Runtime
0.23.0 ships a named physical-constants registry, so the record should name
the constant instead of inlining it or adding an input variable. No sigma
input is needed.

## What happened

The record below passed scientific review (recommend-admit, reviewer X) but
cannot project: its expression inlines the Stefan-Boltzmann constant
`5.67e-08` as a bare number. The engine evaluates every expression in
canonical base units, where power is kWh/s, so a watt-based SI literal is
interpreted 3,600,000× too large. No evidence was questioned and nothing was
modified.

## Requested r2 revision (1 record)

1. `building-energy--net-radiative-exchange-gray-surface` (be-a-b04, r1 → r2)
   - `relationship.expression`: `e * 5.67e-08 * A * (To**4 - Ts**4)` →
     `e * stefan_boltzmann * A * (To**4 - Ts**4)`
   - The name resolves to 5.670374419e-8 W/(m2*K^4) (CODATA 2022, exact) and
     converts through the registry scales like any other quantity. Add no
     variable, input, or family for it.
   - Drop the sigma entry from `constants` metadata: registry-named
     universals are not repeated there. Cite the registry name in
     `translation_notes`.
   - References: `inputs` maps stay exactly as they are (no sigma input).
     Recompute expectations with the registry value:
     - `person-dark-room`: `expected` stays `-99.0` (published, tol 1.0);
       the recomputed check value moves from -98.532 to -98.538579 (still
       inside tolerance). Update the method arithmetic, not the expected.
     - `blackbody-near-ambient`: `expected` `58.241673` → `58.245519`
       (independent calculation with the registry value; tolerance stays
       1e-6). Label the method as an independent calculation.
   - Keep symbols, guards, sources, and everything else byte-identical.

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as usual).
Reference replay will then pass: the engine evaluates the named constant in
canonical units, so no inlined factor remains.
