# Correction brief: canonical-unit expressions for byte-conversion records

To: computer-science curator (batches cs-b02, cs-b03)
From: dev intake, 2026-11-01
Status: needs-revision (mechanical, not scientific — both reviews stand as recommend-admit)

## What happened

Both records below passed scientific review (recommend-admit) but failed runtime
projection at reference replay with `Runtime projection failed reference replay`.
This is a fail-closed staging gate, not a scientific objection: no evidence was
questioned and nothing was modified.

## Root cause

The engine evaluates every expression in canonical base units: it converts each
input to base units BEFORE evaluating, then converts the result into the output
port unit. The runtime vocabulary now carries byte units with honest scales
(`B` = 1, `GB` = 1e9, `GiB` = 2^30, sourced from NIST/IEC), so a GB-denominated
input arrives at the expression already multiplied by 1e9. An expression that
also inlines the factor double-counts it (see
[[decision-canonical-expressions-for-conversion-records]]).

The general rule going forward: write `relationship.expression` in canonical
base units. For pure unit-conversion records the projection is the identity over
registry scales; the conversion factor stays documented in `constants` and in
the vocabulary evidence, never inlined.

## Requested r2 revisions (2 records, nothing else changes)

1. `computer-science--decimal-gigabyte-to-byte` (cs-b02, r1 → r2)
   - `relationship.expression`: `N * 1000000000` → `N`
   - Keep variables, ports, units (`N` in `GB`, `B` in `B`), references,
     guards, constants, and sources byte-identical.
   - Update `translation_notes` to state the expression is written in canonical
     base units (bytes) and the 1e9 factor is carried by the GB/B unit scales.

2. `computer-science--binary-gibibyte-to-byte` (cs-b03, r1 → r2)
   - `relationship.expression`: `N * 1073741824` → `N`
   - Keep variables, ports, units (`N` in `GiB`, `B` in `B`), references,
     guards, constants, and sources byte-identical.
   - Update `translation_notes` the same way (2^30 carried by the GiB/B scales).

## Resubmission

Submit the two r2 records as a small correction batch (bundle + return as
usual). Reference replay will then pass unchanged: N=1 GB → 1e9 B,
N=400 GB → 4e11 B, and the binary equivalents.
