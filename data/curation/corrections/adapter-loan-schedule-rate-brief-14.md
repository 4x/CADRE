# Adapter brief: loan-rate → schedule-rate bridge for the mortgage triangle (brief 14)

To: schedule-rate adapter curator (batch engineering-finance-schedule-b01, 1 new record)
From: schedule-rate bridge curation (native compat-curation subagent), 2026-11-04
Status: proposed (mechanical — no admitted record is revised; all reviews stand)

## What happened

The mortgage triangle cannot close: the rate leg into the amortization-schedule
splits fails fail-closed under exact `(meaning, context)` port equality
(`Port.require_compatible` in `connected_models/contracts.py`; units already
match at `1`). Brief 7 moved the level-payment output into the `:schedule`
context so the payment node binds to both splits, and brief 11 (F1) bridged the
nominal-conversion rate into the plain loan context — but the splits take their
rate input `i` in the `:schedule`-qualified context, so chains stop at the
payment node and composers work around with rebound facts. No evidence was
questioned and nothing was modified; the endpoint records stand as reviewed.

Exact port triples, read read-only from `.registry/models.sqlite3` on
2026-11-04 (`mode=ro`; never staged, reviewed, admitted, or otherwise touched):

Producer —
`engineering-finance--periodic-rate-for-loan-schedule@r1.runtime1` output:

- (`periodic_rate`, `1`,
  `same-loan:end-of-period-level-payments:fixed-rate`)

Consumer leg 1 —
`engineering-finance--loan-payment-interest-portion@r1.runtime1` input `i`:

- (`periodic_rate`, `1`,
  `same-loan:end-of-period-level-payments:fixed-rate:schedule`)

Consumer leg 2 —
`engineering-finance--loan-payment-principal-portion@r1.runtime1` input `i`:

- (`periodic_rate`, `1`,
  `same-loan:end-of-period-level-payments:fixed-rate:schedule`)

Both consumer legs carry byte-identical triples, so one adapter output binds
both — the brief-7 minimality shape (one record fixes both downstream chains).

## Registry orphan survey (all 246 admitted models, 2026-11-04)

`periodic_rate` (`1`) — 2 producers, 10 consumer ports, 3 working edges:

| side | record@rev | port | context |
|---|---|---|---|
| OUT | periodic-rate-from-nominal@r1 | — | `same-rate-year:nominal-basis:discrete-compounding` |
| OUT | periodic-rate-for-loan-schedule@r1 | — | `same-loan:end-of-period-level-payments:fixed-rate` |
| IN | periodic-rate-for-loan-schedule@r1 | `iper` | `same-rate-year:nominal-basis:discrete-compounding` |
| IN | level-loan-periodic-payment@r1 | `i` | `same-loan:end-of-period-level-payments:fixed-rate` |
| IN | level-loan-periodic-payment@r2 | `i` | `same-loan:end-of-period-level-payments:fixed-rate` |
| IN | loan-payment-interest-portion@r1 | `i` | `same-loan:end-of-period-level-payments:fixed-rate:schedule` |
| IN | loan-payment-principal-portion@r1 | `i` | `same-loan:end-of-period-level-payments:fixed-rate:schedule` |
| IN | annuity-due-future-value@r1 | `i` | `same-series:beginning-of-period-level-deposits:fixed-rate` |
| IN | annuity-due-present-value@r1 | `i` | `same-series:beginning-of-period-level-payments:fixed-rate` |
| IN | arithmetic-gradient-annual-equivalent@r1 | `i` | `same-series:arithmetic-gradient:end-of-period` |
| IN | effective-discount-rate@r1 | `i` | `same-period:rate-basis` |
| IN | growing-annuity-present-value@r1 | `i` | `same-series:growing-end-of-period:fixed-rates` |

Working edges today: from-nominal → for-loan-schedule (`iper`), and
for-loan-schedule → level-loan-payment `i` (both r1 and r2 legs). The two
schedule-split `i` legs match no producer — they are the only broken pair in
the loan family — and the five annuity/gradient/discount/growing consumers
match no producer either.

The adapter input (plain loan triple) matches exactly one producer
(for-loan-schedule output) and becomes its second consumer alongside the
level-loan `i` legs, which are untouched. The adapter output (schedule triple)
matches exactly the two split `i` inputs and no other consumer. No producer
emits schedule-context `periodic_rate` today, so the bridge orphans zero
working chains by construction, and after admission the full triangle executes:
from-nominal → for-loan-schedule → this bridge → interest/principal splits,
with the payment node (brief 7) supplying `A`.

## Decision: one adapter, not a context-r2

The brief-7–9 convention picks the minimal honest side that orphans nothing.
This is the same near-miss shape as brief-11 F1 (same meaning, different
contexts), and F1 is the direct precedent: it prescribed an adapter, not a
revision, because both sides' contexts honestly describe their own ends. No
one-sided r2 is honest here either:

- Producer-side r2 (for-loan-schedule output → schedule context) would orphan
  the WORKING for-loan-schedule → level-loan-payment edges — the only working
  loan-rate edges in the registry. Brief 7 could move its producer only because
  the old output matched nothing; here it matches, so the move breaks a live
  chain. Rejected.
- Consumer-side r2 ×2 (strip `:schedule` from both split `i` inputs) costs two
  revisions against one record, fragments the uniform `:schedule` family
  context of both split records (all four inputs plus the output share it),
  and contradicts the brief-7 direction that the schedule qualifier marks
  schedule-split membership. The split `i` is honestly the schedule-computation
  rate consumed alongside schedule-bound `A`/`n`/`t`. Rejected.

One identity adapter (input face = producer output, output face = the shared
consumer triple) fixes both legs with 0 revisions and 0 orphans, preserving
every reviewed record. It also completes the admitted F1 scope, which already
names the interest/principal schedule splits as the downstream family.

## Record authored (batch engineering-finance-schedule-b01)

`engineering-finance--periodic-rate-for-payment-schedule@r1`: IN `iloan` =
producer-output face, OUT `i` = shared consumer-input face, expression
`iloan`, guard `iloan >= 0` (mirrors the producer range; the splits enforce
`i > 0` at their own ports, so the `i = 0` boundary passes the bridge and is
rejected downstream — the F1 boundary convention).

It is a `definition`-kind identity record: the compatibility claim (same loan,
same fixed rate, same payment period — the `:schedule` qualifier marks
consumption within the amortization-schedule split, not a different value) and
the split-family scope live in assumptions, never in arithmetic. Faces were
embedded byte-exact by reading the registry read-only at author time. It
carries 2 numeric references (the UMD 15% split-table rate shared by both
consumer legs, plus the UMD 18%-nominal monthly carry rate from the producer
side), 1 domain + 1 missing-input rejection case, and project-derivation
sources citing the producer key and both consumer keys. Reference replay is
exact substitution.

Out of scope (separate near-misses for other briefs): the `period_count` `n`
leg (plain loan context at the payment node vs `:schedule` at the splits),
the `payment_index` `t` supply gap (zero producers), and the five
annuity/gradient/discount/growing `periodic_rate` consumer legs (distinct
contexts, no producers).

## Resubmission

Batch `engineering-finance-schedule-b01` is validated and packed in
`.runs/compat-curation/adapters-schedule/` (bundle + return ZIP as usual) for
re-review per protocol. It was never staged or imported; the registry is
untouched.
