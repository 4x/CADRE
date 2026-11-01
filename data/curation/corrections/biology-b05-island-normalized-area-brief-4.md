# Correction brief: normalized-area r2 for island species-area scaling

To: biology curator (batch bio-b05)
From: dev intake, 2026-11-01
Status: needs-revision (mechanical, not scientific — the review stands as recommend-admit)

## What happened

`biology--island-species-area-scaling` r1 (`c * A ** z`, with `A` in km² and a
fitted variable exponent `z`) cannot project to the runtime. Unlike the
conversion-identity cases, no engine upgrade changes this: a variable exponent
on a dimensional base has no statically defined dimensions — the result's
dimensions would depend on the VALUE of `z` — so the engine rejects it
fail-closed, correctly. (Rational literal exponents such as Kleiber's 0.75 are
now supported in runtime 0.16.0; variable exponents remain allowed only on
dimensionless bases, which is the sound rule.)

## The honest fix

The fitted model means richness at unit area times a dimensionless area ratio
raised to `z`. Make the unit area explicit:

- Add input `A0`: suggested quantity `reference_unit_area`, unit `km2`, the
  unit reference area of the island group (1 km² in the references).
- `relationship.expression`: `c * A ** z` → `c * (A / A0) ** z`.
- Add `A0 = 1` to every reference `inputs` map; keep `A`, `c`, `z`,
  `expected` and tolerances unchanged. Add guard `A0 > 0`.
- Keep variables, ports, other guards, constants and sources byte-identical.
- Update `translation_notes` to state the power acts on the dimensionless
  area ratio, which is why a fitted variable exponent is dimensionally sound.

Reference display values stay exactly as printed: (2/1)^0.32 = 1.248 and
(2/1)^0.9 = 1.866 as before.

## Dev side

Admission ships the missing vocabulary (`km2` area unit; `island_area`,
`reference_unit_area`, `fitted_richness_normalization`, `fitted_slope` and
`species_richness` meanings) with the r2 — no curator action needed beyond
the r2 itself.

## Resubmission

Submit the r2 record as a correction batch (bundle + return as usual).
