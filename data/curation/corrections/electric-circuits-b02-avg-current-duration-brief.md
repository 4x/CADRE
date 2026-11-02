# Correction brief: physical duration meaning (average-signed-current)

To: electric-circuits curator (batch codex-b02)
From: dev intake, 2026-11-01
Status: needs-revision (mechanical, not scientific — the review stands as recommend-admit)

## What happened

The record below passed scientific review (recommend-admit, reviewer Y) but
cannot project: its `delta_t` variable uses quantity_id `elapsed_time` with
unit `s`. In the registry, `elapsed_time` is finance-owned and dimensionless
by design (period counts / financial years, deliberately not physical time),
so a seconds-denominated port fails validation fail-closed. No evidence was
questioned and nothing was modified.

## Requested r2 revision (1 record, one field)

1. `electric-circuits--average-signed-current` (codex-b02, r1 → r2)
   - `delta_t` variable: quantity_id `elapsed_time` → `duration`
   - Keep symbol, unit (`s`), context, definition, expression
     (`delta_Q / delta_t`), references, guards, and sources byte-identical.
   - Optionally note in `translation_notes` that physical durations use the
     `duration` meaning; `elapsed_time` is reserved for financial periods.

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as usual).
Reference replay will then pass unchanged: 720 C / 4.00 s → 180 A and the
boundary cases.
