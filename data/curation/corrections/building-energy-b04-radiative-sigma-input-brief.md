# Correction brief: Stefan-Boltzmann constant as an input (radiative exchange)

To: building-energy curator (batch be-a-b04)
From: dev intake, 2026-11-01
Status: needs-revision (mechanical, not scientific — the review stands as recommend-admit)

## What happened

The record below passed scientific review (recommend-admit, reviewer X) but
cannot project: its expression inlines the Stefan-Boltzmann constant
`5.67e-08` as a bare number. The engine evaluates every expression in
canonical base units, where power is kWh/s, so a watt-based SI literal is
interpreted 3,600,000× too large (canonical replay yields −3.56e8 W against
the expected −98.532 W). No evidence was questioned and nothing was modified.

## Root cause

Inlined dimensional literals must be in canonical units, and a canonical-unit
spelling of σ (1.575e-14 kWh/(s·m²·K⁴)) would obscure the physics and invite
transcription error. The established precedent is the Kleiber record
(`biology--kleiber-metabolic-rate-scaling`): the normalization lives in an
input variable whose registry unit carries the scale, and the expression
stays readable (see [[decision-canonical-expressions-for-conversion-records]]).

## Requested r2 revision (1 record)

1. `building-energy--net-radiative-exchange-gray-surface` (be-a-b04, r1 → r2)
   - Add input variable: symbol `sigma`, quantity_id
     `stefan_boltzmann_constant`, unit `W/(m2*K^4)`, context "same surface
     and enclosure pair as inputs", definition "Stefan-Boltzmann constant".
   - `relationship.expression`: `e * 5.67e-08 * A * (To**4 - Ts**4)` →
     `e * sigma * A * (To**4 - Ts**4)`
   - Add `"sigma": 5.67e-08` to every reference `inputs` map; expected
     values, tolerances, guards, and sources stay byte-identical.
   - Keep symbols `To`/`Ts` stable (the reviewer noted they are easy to
     misread, but churn helps nobody); the mapping is already documented.
   - Update `translation_notes` to state σ arrives via its registry unit.

Dev will ship the `stefan_boltzmann_constant` meaning and `W/(m2*K^4)` unit
(scale 1/3600000, dims M·T⁻³·Θ⁻⁴) with the runtime that admits the r2, so the
pinned quantity_id/unit above will project. Agree the exact strings before
resubmitting if anything here conflicts with the kit schema.

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as usual).
Reference replay will then pass unchanged: −98.532 W person case and the
58.241673 W blackbody case.
