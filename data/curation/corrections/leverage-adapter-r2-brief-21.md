# Correction brief: leverage-adapter r2 (brief 21)

To: CVP r2 curator (batch economics-cvp-b02, 1 revised record)
From: dev mechanical intake, 2026-11-04
Status: prescribed (mechanical — no admitted record is revised; all reviews stand)

## What happened

Batch `economics-cvp-b01` reviewed 5/6 recommend-admit (revBI, review at
`data/curation/reviews/economics-cvp-b01-review.json`, validator-accepted).
The 5 admitted records are live as `@r1/runtime1` projections; the registry
holds 252 admitted keys.

`economics--operating-leverage-as-price-elasticity@r1` returned
needs-revision with three blockers, quoted verbatim from the review:

1. "Core equivalence E=DOL is asserted without derivation (the record's own
   assumption concedes no economic equivalence proof is derived) and
   contradicts standard economics: DOL is pct-change NOI over pct-change
   sales at a CVP sales level, while price elasticity is pct-change quantity
   over pct-change price from a demand curve that CVP does not contain.
   REQUIRED: derive the equivalence with bounded conditions under which the
   values coincide, or remove the relabel."
2. "No independent oracle for the relabeled value: all references exercise
   only the identity carry (3->3, 1->1, 0->0). REQUIRED: add a published
   E=DOL oracle, or drop the claim."
3. "Guard/scope mismatch: above-break-even scope implies
   DOL=CM/(CM-FIX)>=1 (=1 iff FIX=0), but guard DOL>=0 over-admits [0,1),
   and the DOL=0 'zero-contribution boundary' contradicts the scope (CM=0
   gives NOI=-FIX below break-even, or 0/0 if FIX=0). REQUIRED: tighten the
   guard to the scoped range or re-scope with a corrected boundary
   rationale."

## Prescription

Author `economics--operating-leverage-as-price-elasticity@r2` in a fresh
batch `economics-cvp-b02` (single record), resolving all three blockers via
exactly one of:

- (a) Derive the equivalence: state bounded conditions under which the DOL
  value coincides with a price elasticity of demand, carry a published
  E=DOL oracle recomputed from source text, and tighten the guard to the
  scoped range with a corrected boundary rationale; or
- (b) Drop the relabel: re-scope the record to what the oracles support
  (identity carry within the CVP analysis), with the output meaning,
  assumptions, guard and boundary rationale corrected accordingly.

Either way: keep the batch-shared lane-B context byte-identical to the
admitted r1 records (revBI accepted it as the same-analysis coherence key),
keep all other ports/meanings, and preserve the r1 disclosures that still
hold. Do not touch the 5 admitted records.

## Resubmission

Validate, pack, and report bundle + return-ZIP verification hashes (label
which artifact each hash covers: the r1 brief mislabeled the bundle hash as
the ZIP hash). Intake will packet the return for independent re-review.
