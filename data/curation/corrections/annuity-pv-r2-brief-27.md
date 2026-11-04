# Correction brief: annuity present-value r2 (brief 27)

To: retire r2 curator (batch engineering-finance-retire-b02, 1 revised record)
From: dev, 2026-11-04
Status: prescribed (mechanical — no admitted record is revised; all reviews stand)

## What happened

Batch `engineering-finance-retire-b01` reviewed 5/6 recommend-admit (revBO,
review at `data/curation/reviews/engineering-finance-retire-b01-review.json`,
validator-accepted). The 5 admitted records are live as `@r1/runtime1`
projections.

`engineering-finance--ordinary-annuity-present-value@r1` returned
needs-revision on one prose-confined defect, quoted verbatim:

"due-pv-closure method text states the admitted due-record intermediate as
60790.08; independent recomputation gives 60790.58. As written,
60790.08/1.06 = 57349.13 misses the expected 57349.61 by 0.48, outside the
0.01 tolerance. Required correction: replace 60790.08 with 60790.58."

## Prescription

Author `engineering-finance--ordinary-annuity-present-value@r2` in a fresh
batch `engineering-finance-retire-b02` (single record): apply exactly the
required correction, keep everything else byte-identical to `r1`, and
re-verify every reference and rejection case against the corrected text.

## Resubmission

Validate, pack, and report bundle + return-ZIP verification hashes with each
hash labeled by artifact. Intake will packet the return for independent
re-review.
