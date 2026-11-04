# Correction brief: loan-schedule context alignment for level-loan-periodic-payment (brief 7)

To: engineering-finance curator (batch spark-b01 record)
From: mortgage context-alignment curation, 2026-11-03
Status: needs-revision (mechanical, not scientific — all reviews stand as recommend-admit)

## What happened

`engineering-finance--level-loan-periodic-payment@r1.runtime1` outputs
`periodic_payment` in context
`same-loan:end-of-period-level-payments:fixed-rate`, but
`engineering-finance--loan-payment-interest-portion@r1.runtime1` takes input
`A` (`periodic_payment`) in context
`same-loan:end-of-period-level-payments:fixed-rate:schedule`. The engine binds
ports only on exact meaning/context equality (`Port.require_compatible` in
`connected_models/contracts.py`), so the payment→interest chain fails
fail-closed with a meaning/context mismatch — and the payment→principal
chain fails the same way, since
`engineering-finance--loan-payment-principal-portion@r1.runtime1` takes `A`
in the identical `:schedule` context. No evidence was questioned and nothing
was modified; all three r1 records stand as reviewed
(`data/curation/reviews/engineering-finance-spark-b01-review.json` and
`engineering-finance-spark-b03-review.json`: recommend-admit, no blockers).

## Required correction (1 record, 1 variable)

`engineering-finance--level-loan-periodic-payment` (spark-b01, r1 → r2):

- Output `A` variable: context
  `same-loan:end-of-period-level-payments:fixed-rate` →
  `same-loan:end-of-period-level-payments:fixed-rate:schedule`.
- Keep symbol, quantity (`periodic_payment`), unit (`USD`), definition,
  dimensions, domain, expression, inputs (`P`/`i`/`n` keep the loan-level
  context), references, guards, constants, sources, and every other field
  byte-identical.
- Append one sentence to `translation_notes` stating the output carries the
  `:schedule`-qualified context marking it as the amortization-schedule
  payment consumed by the loan-payment-interest/principal-portion records.

Reference replay passes unchanged: contexts do not enter arithmetic.

## Why the producer side moves

- Minimal: one variable in one record fixes BOTH downstream chains (interest
  and principal share the `:schedule` consumer context).
- Breaks nothing: a registry survey of all 232 admitted models shows no
  consumer takes `periodic_payment` in the plain loan-level context, so the
  old producer output matched nothing — moving it orphans zero chains, and
  the untouched `P`/`i`/`n` inputs preserve every upstream chain.
- Honest: the computed level payment IS the amortization-schedule payment
  the b03 records split, so the `:schedule` qualifier belongs on it; the
  loan terms that size it carry no schedule index and correctly stay
  unqualified. The reverse move (stripping `:schedule` from the consumer's
  `A`) would misdescribe a scheduled payment, leave `A` inconsistent with
  its schedule-bound co-inputs `i`/`n`/`t`, and fix only one of the two
  chains.

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as usual).
