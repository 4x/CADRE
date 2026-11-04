# Correction brief: availability-chain bridges for MTBF → inherent-A → complement → downtime (brief 13)

To: computer-science curator (batch computer-science-availability-b01 records)
From: availability bridge curation, 2026-11-03
Status: needs-curation (mechanical, not scientific — all endpoint reviews stand as recommend-admit)

## What happened

Four reviewed records form an intended end-to-end chain — MTBF accounting →
inherent availability → unavailability complement → annual downtime — but all
three links fail fail-closed under exact `(meaning, context)` port equality
(`Port.require_compatible` in `connected_models/contracts.py`). Units already
match on every link. No evidence was questioned and nothing was modified; the
endpoint records stand as reviewed:

- `computer-science--mtbf-from-mttf-mttr@r1` (batch computer-science-b06,
  recommend-admit, no blockers)
- `computer-science--inherent-availability-mtbf-mttr@r1` (batch
  computer-science-b06, recommend-admit, no blockers)
- `computer-science--unavailability-complement@r1` (batch computer-science-b02,
  recommend-admit, no blockers)
- `computer-science--annual-downtime-hours@r2` (r1 in computer-science-b06
  recommend-admit; r2 in computer-science-ncs-c01)

Exact ports, read read-only from `.registry/models.sqlite3` on 2026-11-03:

Link 1 — same meaning, different contexts (context-alignment shape):

- Producer OUT `computer-science--mtbf-from-mttf-mttr@r1.runtime1`:
  (`mtbf`, `h`, `same element, stated conditions and steady-state scope as
  inputs`)
- Consumer IN `computer-science--inherent-availability-mtbf-mttr@r1.runtime1`
  `MTBF`: (`mtbf`, `h`, `same element, stated conditions and ideal support
  environment as MTTR and A`)

Link 2 — different meanings AND different contexts (adapter shape):

- Producer OUT `computer-science--inherent-availability-mtbf-mttr@r1.runtime1`:
  (`inherent_availability`, `1`, `same element, stated conditions and ideal
  support environment as inputs`)
- Consumer IN `computer-science--unavailability-complement@r1.runtime1` `A`:
  (`component_availability`, `1`, `same item, mission instant and conditions
  as U`)

Link 3 — different meanings AND different contexts (adapter shape):

- Producer OUT `computer-science--unavailability-complement@r1.runtime1`:
  (`unavailability`, `1`, `same item, mission instant and conditions as A`)
- Consumer IN `computer-science--annual-downtime-hours@r2.runtime1` `U`:
  (`steady_unavailability`, `1`, `same system, stated conditions and
  accounting year as D`)

## Prescription (3 records, 1 batch)

Link 1 → consumer-side context-r2 (briefs 7–9 precedent: same meaning with
different contexts wants a context-alignment revision).

`computer-science--inherent-availability-mtbf-mttr` (computer-science-b06,
r1 → r2):

- Input `MTBF` variable: context → `same element, stated conditions and
  steady-state scope as inputs` (the mtbf-from-mttf-mttr output context,
  adopted verbatim).
- Keep symbol, source symbol, role, meaning (`mtbf`), definition, dimensions,
  domain, unit (`h`), co-input `MTTR`, output `A`, expression, guards,
  references, rejection cases, assumptions, limitations, sources, and every
  other field byte-identical.
- Append one sentence to `translation_notes` stating the `MTBF` input carries
  the steady-state-scope context shared with
  `computer-science--mtbf-from-mttf-mttr`, marking it as the repairable-element
  accounting MTBF that record computes.

Reference replay passes unchanged: contexts do not enter arithmetic.

Why the consumer side moves (minimal-side convention):

- Honest: the shared string must truthfully describe the linked value on both
  sides. `same element, stated conditions and steady-state scope as inputs`
  is true of the inherent input — that record's own assumptions state
  `steady-state (limiting) availability` — and `as inputs` names no
  record-foreign symbols. The reverse move would stamp `ideal support
  environment as MTTR and A` onto the MTBF record, asserting a support-scope
  qualifier plus a symbol `A` undefined in that record; brief 8 rejects
  exactly this shape (stamping a context with undefined symbols is false).
- Minimal: one variable in one record; both endpoints are r1 so neither side
  wins on revision count, and honesty breaks the tie.
- Breaks nothing: the registry survey below shows no producer emits `mtbf` in
  the old consumer context, so the old input matched nothing — moving it
  orphans zero chains. The untouched `MTTR` input has no producers and the
  untouched `A` output has no consumers, so no other chain is affected either
  way. Mixed contexts within one record are precedented (brief 9).

Links 2–3 → NEW adapter records (r1), not context-r2s. A context alignment
keeps the meaning identical by construction; here the meanings differ
(`inherent_availability` vs `component_availability`;
`unavailability` vs `steady_unavailability`), so no one-sided context edit
can bind the ports without a scientific meaning change that would destroy the
endpoint records' reviewed identities. The representation contract prescribes
reviewed explicit adapter models for exactly this case
(`knowledge/decisions/representation-contract-v0.md`: different semantic
meanings/context transformations want explicit adapter models, no silent
equivalence). Each adapter is an identity expression over registry-exact
ports, with scope assumptions that make the meaning hop reviewable:

`computer-science--inherent-availability-component-scope` (new, r1):

- Input `Ai`: (`inherent_availability`, `1`, `same element, stated conditions
  and ideal support environment as inputs`) — byte-identical to the link-2
  producer output.
- Output `A`: (`component_availability`, `1`, `same item, mission instant and
  conditions as U`) — byte-identical to the link-2 consumer input.
- Expression `Ai` (identity); guards `Ai >= 0`, `Ai <= 1`.
- Scope reading: both endpoint definitions describe the same mathematical
  object — a steady-state operable probability — under stated conditions;
  the inherent value (ideal support, corrective downtime only) counts as the
  component value at a mission instant when the instant samples the steady
  state. Assumptions/limitations carry the ideal-support, steady-state,
  single-element/item-identity, and no-composition preconditions.

`computer-science--unavailability-steady-scope` (new, r1):

- Input `U`: (`unavailability`, `1`, `same item, mission instant and
  conditions as A`) — byte-identical to the link-3 producer output.
- Output `Us`: (`steady_unavailability`, `1`, `same system, stated conditions
  and accounting year as D`) — byte-identical to the link-3 consumer input.
- Expression `U` (identity); guards `U >= 0`, `U <= 1`.
- Scope reading: the mission-instant unavailability counts as the
  steady-state unavailability for the accounting year when the instant
  samples the steady state and outages accumulate linearly; item/system
  identity and no-shaping preconditions are explicit.

Both adapters carry `project-derivation` sources on the endpoint records
(no third-party prose reused), 2+ numeric references (published-scale carry
values plus a boundary identity), 1+ rejection cases, and inverse notes.

## Registry orphan survey (235 models, 2026-11-03)

Full meaning-level survey; every claim below is read from registry payloads:

- `mtbf` producers: mtbf-from-mttf-mttr (steady-state-scope context),
  mtbf-failure-rate-reciprocal (`same system, useful-life period and
  operating environment as L`). `mtbf` consumers: inherent-availability
  `MTBF` (ideal-support context), operational-availability-mtbf-mdt `MTBF`
  (`same element, realistic support environment and mission profile as MDT
  and Ao`). No producer context equals any consumer context: link 1 is one
  of four broken producer/consumer pairs, and the r2 fixes exactly its pair
  while orphaning zero (the old input matched nothing).
- `inherent_availability`: one producer (the inherent record), zero
  consumers — the value is currently a chain terminus. The link-2 adapter
  input is its first consumer and matches it exactly.
- `component_availability`: zero producers, 13 consumer ports (parallel /
  series / three-leg / n-identical availability records plus the complement
  `A` input, in nine distinct contexts). The link-2 adapter output matches
  ONLY the complement `A` context byte-identically; it binds no series /
  parallel input, so the adapter creates no accidental composition edges.
  Those 12 remaining consumer ports stay unbound (fail-closed, as today) and
  are out of scope for this brief.
- `unavailability`: one producer (the complement record), zero consumers —
  likewise a chain terminus today. The link-3 adapter input is its first
  consumer and matches it exactly.
- `steady_unavailability`: zero producers, one consumer (annual-downtime
  `U`). The link-3 adapter output is its first producer and matches it
  exactly.
- Upstream gaps untouched: `mttf` has zero producers (one consumer port)
  and `mttr` has zero producers (two consumer ports), all in steady-state or
  ideal-support contexts; `reference_year_hours` has zero producers. The chain head
  (MTTF/MTTR supply) and the `H = 8760` supply remain user inputs, as today.

After admission, the full chain executes end to end: mtbf-from-mttf-mttr →
inherent-availability r2 → inherent/component adapter → complement →
unavailability/steady adapter → annual-downtime.

Out of scope: the failure-rate-reciprocal and operational-availability
`mtbf` near-misses, the 12 series/parallel `component_availability`
consumer ports, and the MTTF/MTTR/`reference_year_hours` supply gaps are
separate near-misses for other briefs.

## Resubmission

Submit all three records as ONE correction batch
(computer-science-availability-b01: bundle + return as usual) for re-review
per protocol since record text changes (r2) and new adapter identities are
introduced (r1s).
