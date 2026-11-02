# Correction brief: canonical-unit expression for constant-power record

To: building-energy curator (batch be-a-b01)
From: dev intake, 2026-11-01
Status: needs-revision (mechanical, not scientific — the review stands as recommend-admit)

## What happened

The record below passed scientific review (recommend-admit, reviewer V) but
failed runtime projection at reference replay with `Runtime projection failed
reference replay`. This is a fail-closed staging gate, not a scientific
objection: no evidence was questioned and nothing was modified.

## Root cause

The engine evaluates every expression in canonical base units: it converts each
input to base units BEFORE evaluating, then converts the result into the
output port unit. The runtime vocabulary now carries `W` with scale 1/3600000
against the kWh energy base, so a watt-denominated input arrives at the
expression already divided by 3.6e6. An expression that also inlines the /1000
W/kW prefix factor double-counts it (see
[[decision-canonical-expressions-for-conversion-records]]).

Replayed canonically, `60 * 1000 / 1000` yields 0.06 kWh against the expected
60.0 kWh: the reviewer's record-unit arithmetic (60*1000/1000 = 60) is correct
in W·h/kWh bookkeeping but the engine already performs the W→kW step through
the registry scales.

The general rule going forward: write `relationship.expression` in canonical
base units. Unit prefixes live in the vocabulary scales, never inlined.

## Requested r2 revision (1 record, nothing else changes)

1. `building-energy--constant-power-electricity-consumption` (be-a-b01, r1 → r2)
   - `relationship.expression`: `P * t / 1000` → `P * t`
   - Keep variables, ports, units (`P` in `W`, `t` in `h`, `E` in `kWh`),
     references, guards, constants, and sources byte-identical.
   - Update `translation_notes` to state the expression is written in canonical
     base units and the /1000 W/kW prefix step is carried by the W/kWh unit
     scales.

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as usual).
Reference replay will then pass unchanged: 60 W × 1000 h → 60.0 kWh and
40 W × 5 h → 0.2 kWh.
