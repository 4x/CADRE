# Brief 6 — island-species-area-scaling r3 (dimension of `c`)

Revision of `biology--island-species-area-scaling@r2`
(reviewed 2026-11-03 by revAT-independent: **needs-revision**;
evidence in `data/curation/reviews/biology-nbio-c01-{bundle,review}.json`).
Five of six checks passed; source, scope, license, and both
reference doublings verified independently.

## Blocker (only)

Variable `c` (species per unit area) declares dimensions
`count / length^(2z)` — the dimension of the *unnormalized*
form — contradicting all of:

- the r2 expression, normalized so `c` must be a **count**;
- its own declared unit `count`;
- its definition and translation notes.

## Required correction

In a new revision r3, set `c` dimensions to `count`. Nothing
else in the record needs to change. Re-review required.
