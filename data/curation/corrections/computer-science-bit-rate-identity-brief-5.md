# Correction brief: canonical-identity r2 for bit-rate-to-byte-rate (brief 5)

To: computer-science curation (batch b04 record)
From: dev intake, 2026-11-03
Status: needs-revision (mechanical — supplements brief 2, whose table listed
this record as needing no r2)

## What happened

Brief 2 asserted `computer-science--bit-rate-to-byte-rate` r1 (`R_bps / 8`,
input `bit/s`, output `B/s`) "stages as written". That was wrong: under the
registry scales bit-denominated units carry the /8 explicitly (`bit/s` at
1/8 against `B/s` at 1.0), so the r1's inlined `/8` double-counts and the
record fails staging fail-closed with `Expression/output dimensions differ`
— more precisely a scale mismatch on replay. No evidence was questioned;
the r1 review stands.

## Prescription (1 record)

`computer-science--bit-rate-to-byte-rate` (r1 → r2):

- `relationship.expression`: `R_bps / 8` → `R_bps`
- Keep variables, ports, units, references, guards, constants and sources
  byte-identical; update `translation_notes` to state the expression is
  written in canonical base units with the 8-bits-per-byte factor carried
  by the registry unit scales.

Reference display values stay exactly as printed; the identity replays them
through the registry scales (kit 2026-10-31.8+ validates this shape).

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as usual)
for re-review per protocol since record text changes.
