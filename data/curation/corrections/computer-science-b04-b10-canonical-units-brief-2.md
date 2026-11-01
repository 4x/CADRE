# Correction brief: canonical-unit r2s for rate conversions, annual downtime, MIPS

To: computer-science curator (batches cs-b04 through cs-b10)
From: dev intake, 2026-11-01
Status: needs-revision (mechanical, not scientific — all reviews stand as recommend-admit)

## What happened

Nineteen recommend-admit records cannot project to the runtime in their r1 form.
This is the same canonical-units rule as the earlier byte-conversion brief (see
[[decision-canonical-expressions-for-conversion-records]] and
`data/curation/corrections/computer-science-b02-b03-canonical-units-brief.md`):
the engine evaluates every expression in canonical base units, converting each
input BEFORE evaluating and the result into the output unit afterwards. No
evidence was questioned and nothing was modified.

## Part A — rate-conversion identities (17 records)

Each record below inlines its conversion factor in `relationship.expression`
(e.g. `R_mbps * 1000000`). Keep every variable, port, unit, reference, guard,
constant and source byte-identical; change ONLY the expression to the bare
input symbol and update `translation_notes` to state the expression is written
in canonical base units with the factor carried by the registry unit scales
(dev ships the matching bit/byte-rate vocabulary at admission time):

| record | r1 expression | r2 expression |
|---|---|---|
| decimal-megabit-rate-to-bit-rate | `R_mbps * 1000000` | `R_mbps` |
| binary-mebibit-rate-to-bit-rate | `R_mibps * 1048576` | `R_mibps` |
| bit-rate-to-byte-rate | `R_bps / 8` | `R_bps` |
| decimal-gigabit-rate-to-bit-rate | `R_gbps * 1000000000` | `R_gbps` |
| binary-gibibit-rate-to-bit-rate | `R_gibps * 1073741824` | `R_gibps` |
| decimal-terabit-rate-to-bit-rate | `R_tbps * 1000000000000` | `R_tbps` |
| decimal-megabyte-rate-to-byte-rate | `R_MBps * 1000000` | `R_MBps` |
| decimal-kilobit-rate-to-bit-rate | `R_kbps * 1000` | `R_kbps` |
| binary-kibibit-rate-to-bit-rate | `R_kibps * 1024` | `R_kibps` |
| decimal-gigabyte-rate-to-bit-rate | `R_GBps * 8000000000` | `R_GBps` |
| binary-mebibyte-rate-to-byte-rate | `R_MiBps * 1048576` | `R_MiBps` |
| binary-tebibit-rate-to-bit-rate | `R_tibps * 1099511627776` | `R_tibps` |
| binary-tebibyte-rate-to-byte-rate | `R_TiBps * 1099511627776` | `R_TiBps` |
| decimal-petabit-rate-to-bit-rate | `R_pbps * 1000000000000000` | `R_pbps` |
| decimal-terabyte-rate-to-byte-rate | `R_TBps * 1000000000000` | `R_TBps` |
| binary-pebibit-rate-to-bit-rate | `R_pibps * 1125899906842624` | `R_pibps` |
| binary-exbibit-rate-to-bit-rate | `R_eibps * 1152921504606846976` | `R_eibps` |

Reference display values stay exactly as printed; the identity replays them
through the registry scales.

## Part B — annual-downtime-hours (1 record)

`U * 8760` multiplies a dimensionless fraction by a bare literal but declares
its output in `h` (physical time), which the dimension checker rejects: a
dimensionless expression cannot produce time. The 8760 carries implicit
hours-per-year semantics that must become an explicit input:

- Add input `H`: suggested quantity `reference_year_hours`, unit `h`, the
  hours in the reference year for the stated window.
- `relationship.expression`: `U * 8760` → `U * H`.
- Add `H = 8760` to every reference `inputs` map; keep `U`, `expected` and
  tolerances unchanged. Add guard `H > 0`.
- Update `translation_notes` and `inverse_notes` for the new input.

## Part C — mips-rating (1 record)

`f / (CPI * 1000000)` inlines the million in the expression while labeling the
output `1/s`, which would store MIPS-numbers under a per-second unit string —
the same magnitude-lie the canonical-units decision forbids (it replays only
because both scales happen to be 1). Runtime 0.14.0 already ships the honest
target: unit `MIPS` (1/time dimensions, scale 1000000.0). Dev verified the
prescription replays all three r1 references exactly:

- Output port unit: `1/s` → `MIPS` (keep quantity `mips_rating`, keep context).
- `relationship.expression`: `f / (CPI * 1000000)` → `f / CPI`.
- Keep inputs, references, guards, constants and sources byte-identical.
- Update `translation_notes` to state the 1e6 lives in the MIPS registry scale.

## Resubmission

Submit the nineteen r2 records as correction batches (bundles + returns as
usual). Reference replay will then pass with unchanged display values. The
reviewer's separate needs-revision on `series-availability-three` (wrong
inverse arithmetic, cs-b11 review) travels through the review itself, not this
brief — but it may ride along in the same resubmission.
