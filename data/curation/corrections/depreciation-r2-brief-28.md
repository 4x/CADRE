# Correction brief: depreciation dims r2 (brief 28)

To: dctco r2 curator (batch computer-science-dctco-b02, 1 revised record)
From: dev, 2026-11-04
Status: prescribed (mechanical — no admitted record is revised; all reviews stand)

## What happened

Batch `computer-science-dctco-b01` reviewed 5/6 recommend-admit (revBM,
review at `data/curation/reviews/computer-science-dctco-b01-review.json`,
validator-accepted). The 5 admitted records are live as `@r1/runtime1`
projections.

`computer-science--straight-line-annual-depreciation@r1` returned
needs-revision on one dimensions/unit defect, quoted verbatim:

"Dimensions/unit defect: output annual_depreciation declares dimensions
'currency' with unit 'USD', but (C-S)/n with n in count yields currency per
period (as the record's own translation_notes state). Currency/count must
not silently reduce to currency; a rate could mis-bind as a plain amount.
Required correction: declare compound dimensions and a matching per-period
unit, then re-review."

Note the standing project rule that financial periods are dimensionless
counts (so currency/count reduces to currency dimensionally). The reviewer's
objection stands regardless as a mis-binding risk: resolve it, do not
dismiss it.

## Prescription

Author `computer-science--straight-line-annual-depreciation@r2` in a fresh
batch `computer-science-dctco-b02` (single record), resolving the blocker
via exactly one of:

- (a) Satisfy the reviewer literally: declare compound dimensions and a
  matching per-period unit for the output (naming any new unit as an
  explicit vocabulary gap for dev shipment), keeping the equation and
  oracles otherwise intact; or
- (b) Rebut with the standing dimensionless-periods rule AND eliminate the
  mis-binding risk another honest way (tighter meaning, context, or
  guard/assumption scope that prevents rate-as-amount binds), with the
  reasoning written into the record for the re-reviewer to judge.

Either way: keep the equation, oracle values and all other ports identical
to `r1` unless the chosen resolution forces a change; say which changes it
forced and why.

## Resubmission

Validate, pack, and report bundle + return-ZIP verification hashes with each
hash labeled by artifact. Intake will packet the return for independent
re-review.
