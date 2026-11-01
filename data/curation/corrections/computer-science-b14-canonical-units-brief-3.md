# Correction brief: canonical-unit r2s for peta/exa rate conversions

To: computer-science curator (batch cs-b14)
From: dev intake, 2026-11-01
Status: needs-revision (mechanical, not scientific — the review stands as recommend-admit)

## What happened

Four recommend-admit records cannot project to the runtime in their r1 form,
under the same canonical-units rule as the two earlier briefs (see
[[decision-canonical-expressions-for-conversion-records]]): the engine
evaluates every expression in canonical base units, converting each input
BEFORE evaluating. No evidence was questioned and nothing was modified.

## Prescription (4 records)

Keep every variable, port, unit, reference, guard, constant and source
byte-identical; change ONLY the expression to the bare input symbol and update
`translation_notes` to state the expression is written in canonical base units
with the factor carried by the registry unit scales (dev ships the matching
rate vocabulary at admission time):

| record | r1 expression | r2 expression |
|---|---|---|
| decimal-petabyte-rate-to-byte-rate | `R_PBps * 1000000000000000` | `R_PBps` |
| decimal-petabit-rate-to-byte-rate | `R_pbps * 125000000000000` | `R_pbps` |
| binary-pebibyte-rate-to-byte-rate | `R_PiBps * 1125899906842624` | `R_PiBps` |
| binary-exbibyte-rate-to-byte-rate | `R_EiBps * 1152921504606846976` | `R_EiBps` |

Reference display values stay exactly as printed; the identities replay them
through the registry scales.

## Resubmission

Submit the four r2 records as a correction batch (bundle + return as usual),
bundled with the r2s from the two earlier briefs if convenient. This closes the
known wave-1 CS correction queue: 2 byte + 19 brief-2 + 4 brief-3 records.
