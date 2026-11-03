# Correction brief: dimensional literals in circuits b04 records (r2 × 2)

To: electric-circuits curator (batch codex-b04)
From: dev intake, 2026-11-03
Status: needs-revision (mechanical, not scientific — the reviews stand as recommend-admit)

## What happened

Two records passed scientific review (recommend-admit, reviewer AI) but
cannot project: each inlines a unit-carrying literal that the engine
reads as dimensionless, so staging fails fail-closed with
`Expression/output dimensions differ`. No evidence was questioned and
nothing was modified.

## Fix 1: name Avogadro's number (universal constant)

`electric-circuits--carrier-density-from-material-content` (r1 → r2):
- `z * rho_m * 6.02214076e23 / M` →
  `z * rho_m * avogadro / M`

Runtime 0.23.0+ resolves `avogadro` (6.02214076e23 1/mol, SI defining
constant) inside expressions. The registry value is digit-identical to
the inlined literal, so every `inputs`, `expected`, `tolerance`, and
`method` stays byte-identical. Cite `avogadro` in `translation_notes`
and drop the inlined entry from `constants` metadata.

## Fix 2: carry the material coefficient as an input (case parameter)

`electric-circuits--copper-coefficient-conductivity-calibration` (r1 → r2):
- `0.00393 * f` → `alpha_cu * f` (new input `alpha_cu`, quantity
  `resistance_temperature_coefficient`, unit `K^-1`, guarded and
  contextualized as the 20 °C copper coefficient)

Unlike Avogadro's number, 0.00393/K is a material-specific fitted value,
not a universal constant, so it must ride an input variable (Kleiber-B0
precedent) rather than a registry name. Reference expectations stay
numerically identical with `alpha_cu = 0.00393` supplied as a reference
input; only the reference `inputs` gain the new field.

## Resubmission

Submit the two r2 records as a small correction batch (bundle + return
as usual) for re-review per protocol since record text changes.
