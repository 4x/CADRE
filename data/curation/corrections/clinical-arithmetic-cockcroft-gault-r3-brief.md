# Correction brief: Cockcroft-Gault scope gap plus dimensional literal (r3 × 1)

To: clinical-arithmetic curator (batches codex-b02, codex-b05)
From: dev intake, 2026-11-03
Status: needs-revision (one science item, one mechanical — neither record admitted)

## What happened

Two revisions of `clinical-arithmetic--cockcroft-gault-creatinine-clearance`
exist and neither can project yet:

- b05 r2 drew needs-revision (reviewer AA): the empirical
  input-calibration scope is unresolved — no inspected source establishes
  the validated serum-creatinine interval, so guard `sCr>0` admits
  uncalibrated inputs. The revision must incorporate the NKF-FAQ-attested
  validation context (mClcr approximately 30–130 mL/min,
  non-standardized-Scr era, White-men derivation) into scope/limitations
  or add an explicit calibrated-domain limitation. Its integration status
  is curator-declared blocked.
- b02 r1 drew recommend-admit (reviewer Z) but cannot stage: the
  expression `(1 - 0.15*z) * (140 - a) * w / (432000000000 * sCr)`
  evaluates to m³ while the output port is m³/s. The inlined `432000000000`
  carries an implicit time dimension (seconds); the engine reads bare
  literals as dimensionless, so staging fails fail-closed with
  `Expression/output dimensions differ`. The Z review stands on science.

## Fix: one r3 addressing both

1. Carry the b05 scope fix forward: validated-Scr calibration context in
   scope/limitations (or an explicit calibrated-domain limitation) and a
   reviewable integration status.
2. Remove the inlined dimensional literal. The 4.32e11 s divisor is an
   empirical-formula constant, not a universal, so it must ride a
   declared input variable (Kleiber-B0 / copper-coefficient precedent),
   e.g. a `cockcroft_gault_divisor`-style input in `s` supplied as
   4.32e11 s in the references — or an equivalent curator-designed
   reformulation that type-checks in canonical SI units. The engine
   evaluates in canonical base units; no inlined dimensional literals.

The clinical-2 vocabulary already ships every meaning and unit the r3
needs (`chronological_age_year_index`, `cockcroft_gault_female_branch_indicator`,
`creatinine_clearance`, `years`, `kg/m^3`, `m^3/s`).

## Resubmission

Submit the r3 record as a small correction batch (bundle + return as
usual) for re-review per protocol. It supersedes both the b02 r1 and the
b05 r2; neither earlier revision will be admitted.
