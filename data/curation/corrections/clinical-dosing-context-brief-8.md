# Correction brief: dosing context alignment for liquid-medication-prescribed-volume (brief 8)

To: clinical-arithmetic curator (batch codex-b02 record)
From: dosing context-alignment curation, 2026-11-03
Status: needs-revision (mechanical, not scientific — all reviews stand as recommend-admit)

## What happened

`clinical-arithmetic--weight-based-prescribed-mass@r2.runtime1` outputs
`prescribed_drug_mass_per_administration` in context
`Same patient, drug/active-moiety mass basis, independently authorized prescription and one administration. Application profile: actual measured body mass is the independently authorized basis. The prescribed coefficient is per kilogram per administration, not per day or per time. Source examples are pediatric; the arithmetic has no drug-specific clinical validation population.`, but
`clinical-arithmetic--liquid-medication-prescribed-volume@r1.runtime1` takes input
`D` (same meaning, same unit `kg`) in context
`Same independently authorized single administration, active drug/moiety and homogeneous liquid stock at its labeled concentration. The supplied reference mass H and volume Q describe the same final formulation. Source is nursing calculation education, not age-specific drug validation; patient eligibility and prescription appropriateness are external.`. The engine binds
ports only on exact meaning/context equality (`Port.require_compatible` in
`connected_models/contracts.py`), so the mg/kg→mg→mL chain fails
fail-closed with a meaning/context mismatch. No evidence was questioned and
nothing was modified; both records stand as reviewed
(`data/curation/reviews/clinical-arithmetic-codex-b02-review.json`:
recommend-admit, no blockers).

## Required correction (1 record, 1 variable)

`clinical-arithmetic--liquid-medication-prescribed-volume` (codex-b02, r1 → r2):

- Input `D` variable: context
  `Same independently authorized single administration, active drug/moiety and homogeneous liquid stock at its labeled concentration. The supplied reference mass H and volume Q describe the same final formulation. Source is nursing calculation education, not age-specific drug validation; patient eligibility and prescription appropriateness are external.` →
  `Same patient, drug/active-moiety mass basis, independently authorized prescription and one administration. Application profile: actual measured body mass is the independently authorized basis. The prescribed coefficient is per kilogram per administration, not per day or per time. Source examples are pediatric; the arithmetic has no drug-specific clinical validation population.`
  (the weight-based r2 output context, adopted verbatim).
- Keep symbol, quantity (`prescribed_drug_mass_per_administration`), unit
  (`kg`), definition, dimensions, domain, expression, co-inputs (`H`/`Q`
  keep the stock context), output `V`, references, guards, constants,
  sources, and every other field byte-identical.
- Append one sentence to `translation_notes` stating the input carries the
  weight-based-prescription context shared with
  `clinical-arithmetic--weight-based-prescribed-mass`, marking it as the
  independently authorized per-administration mass that record computes.

Reference replay passes unchanged: contexts do not enter arithmetic.

## Why the consumer side moves

- Minimal: one variable in one record fixes the weight-based→liquid leg,
  and the move is r1 → r2 where the producer would need r2 → r3.
- Breaks nothing: a registry survey of all 232 admitted models shows no
  producer emits `prescribed_drug_mass_per_administration` in the old
  consumer context (the two producers emit the weight-based and
  surface-area-based contexts), so the old input matched nothing — moving
  it orphans zero chains. The untouched `H`/`Q` inputs have no producers
  and the untouched `V` output has no consumers, so no other chain is
  affected either way.
- Honest: the aligned core — same patient, same drug/moiety basis,
  independently authorized prescription, one administration — is exactly
  what this input requires (an already-specified mass on the same moiety
  basis for this administration); the per-kg application-profile sentences
  describe the provenance of masses arriving through this chain, and the
  no-validation tail agrees with this record's own stance. The reverse
  move (stamping the stock context onto the weight-based output) would
  assert homogeneous-liquid-stock conditions and `H`/`Q` formulation
  references — symbols undefined in that record — onto a
  formulation-independent mass, which is false.

Out of scope: `clinical-arithmetic--surface-area-based-prescribed-mass@r1`
emits the same meaning in a third context; its alignment with this input
is a separate near-miss for another brief.

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as usual).
