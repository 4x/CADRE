# Adapter brief: finance context bridges for rate chains (brief 11)

To: engineering-finance adapter curator (batch engineering-finance-adapters-b01)
From: compat adapter curation, 2026-11-03
Status: assigned

## What happened

Two finance chains fail fail-closed on meaning/context mismatch
(`Port.require_compatible` in `connected_models/contracts.py` needs exact
equality). Both record pairs stand as reviewed (recommend-admit); the gaps
are documented near-miss shapes, fixed by small adapter records, not by
revising any admitted record.

F1 — nominal conversion to loan schedule (same meaning, different
contexts). `engineering-finance--periodic-rate-from-nominal@r1.runtime1`
outputs `periodic_rate`/`1` in context
`same-rate-year:nominal-basis:discrete-compounding`, but
`engineering-finance--level-loan-periodic-payment@r2.runtime1` takes `i`
(`periodic_rate`/`1`) in context
`same-loan:end-of-period-level-payments:fixed-rate`.

F2 — Fisher real rate to lump-sum nominal rate (different meanings,
scoped identity). `engineering-finance--fisher-real-rate@r1.runtime1`
outputs `real_rate`/`1` in context
`same-period:same-currency:exact-fisher`, but
`engineering-finance--lump-sum-future-value-discrete@r1.runtime1` takes
`r` (`nominal_rate`/`1`) in context
`same-investment:nominal-basis:discrete-compounding`. At unit compounding
frequency (m==1) the nominal annual rate is definitionally the per-period
rate, so the real rate passes through unchanged; everywhere else the
identity is false and must be rejected, not rescaled.

## Required records (2)

F1 `engineering-finance--periodic-rate-for-loan-schedule` (r1): pure
context bridge. IN `periodic_rate`/`1`/rate-year context from the F1
producer OUT above; OUT `periodic_rate`/`1`/loan context of the F1
consumer IN `i` above. Identity expression; guard mirroring the producer
range; one scope assumption naming the end-of-period level-payment
amortization-schedule family it feeds.

F2 `engineering-finance--real-rate-as-unit-frequency-nominal` (r1): IN
`real_rate`/`1` from the F2 producer OUT above plus IN
`compounding_frequency` (`periods/year`, investment context), with guard
m==1 written as two guards (`m>=1` and `m<=1`, one comparison each); OUT
`nominal_rate`/`1` of the F2 consumer IN `r` above. Identity expression
on the rate; assumptions stating validity only at unit compounding
frequency.

Each record: 2+ numeric references replaying the bridged records'
published oracles through the identity, 1+ rejection case, and
project-derivation sources citing both bridged records. Port triples
must be byte-identical to the registry reads above.

## Resubmission

Author, validate, and pack ONE batch (`engineering-finance-adapters-b01`)
in scratch `.runs/compat-curation/adapters-finance/` with the central
package. Never stage, review, admit, or touch the registry.
