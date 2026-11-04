# Adapter brief: parallel-availability → complement bridge for the redundant-downtime chain (brief 16)

To: parallel-availability adapter curator (batch computer-science-parallel-b01, 1 new record)
From: parallel-availability bridge curation (native compat-curation subagent), 2026-11-04
Status: proposed (mechanical — no admitted record is revised; all reviews stand)

## What happened

The redundant-downtime chain cannot execute: the two-leg and three-leg
parallel-availability records output (`parallel_availability`, `1`), but
`computer-science--unavailability-complement@r1` takes input `A` as
(`component_availability`, `1`), so no audited edge exists from any
parallel-availability output into the unavailability/downtime chain. The
downstream chain itself is admitted and working
(complement → `unavailability-steady-scope` → `annual-downtime-hours@r2`,
brief 13 as admitted); only the parallel-subsystem head is a terminus.
No evidence was questioned and nothing was modified; the endpoint records
stand as reviewed (recommend-admit, b02 and b11).

Exact port triples, read read-only from `.registry/models.sqlite3` on
2026-11-04 (`mode=ro`; never staged, reviewed, admitted, or otherwise touched):

Producer leg 1 —
`computer-science--parallel-availability@r1.runtime1` output (`A`):

- (`parallel_availability`, `1`,
  `same system, mission instant and environment as inputs`)

Producer leg 2 —
`computer-science--parallel-availability-three@r1.runtime1` output (`A`):

- (`parallel_availability`, `1`,
  `same system, mission instant and environment as inputs`)

Producer leg 3 (out of scope, see below) —
`computer-science--parallel-availability-n-identical@r1.runtime1` output (`A`):

- (`parallel_availability`, `1`,
  `same legs, mission instant and environment as inputs`)

Consumer —
`computer-science--unavailability-complement@r1.runtime1` input `A`:

- (`component_availability`, `1`,
  `same item, mission instant and conditions as U`)

Legs 1 and 2 carry byte-identical triples, so one adapter input binds
both — the brief-7/14 minimality shape (one record fixes both upstream
legs). Leg 3 differs (`legs` vs `system`) and needs its own face, a
separate near-miss for another brief.

## Registry orphan survey (all 247 admitted models, 2026-11-04)

`parallel_availability` (`1`) — 3 producers, 0 consumers, zero working edges:

| side | record@rev | port | context |
|---|---|---|---|
| OUT | parallel-availability@r1 | `A` | `same system, mission instant and environment as inputs` |
| OUT | parallel-availability-three@r1 | `A` | `same system, mission instant and environment as inputs` |
| OUT | parallel-availability-n-identical@r1 | `A` | `same legs, mission instant and environment as inputs` |

`component_availability` (`1`) — 1 producer, 13 consumer ports, 1 working edge:

| side | record@rev | port | context |
|---|---|---|---|
| OUT | inherent-availability-component-scope@r1 | `A` | `same item, mission instant and conditions as U` |
| IN | parallel-availability-n-identical@r1 | `X` | `same legs, mission instant and environment as N and A` |
| IN | parallel-availability-three@r1 | `A1`/`A2`/`A3` | `same system, mission instant and environment as ...` (3 distinct) |
| IN | parallel-availability@r1 | `A1`/`A2` | `same system, mission instant and environment as ...` (2 distinct) |
| IN | series-availability-n-identical@r1 | `X` | `same legs, mission instant and environment as N and A` |
| IN | series-availability-three@r2 | `A1`/`A2`/`A3` | `same system, mission instant and environment as ...` (3 distinct) |
| IN | series-availability@r1 | `A1`/`A2` | `same system, mission instant, environment and support conditions as ...` (2 distinct) |
| IN | unavailability-complement@r1 | `A` | `same item, mission instant and conditions as U` |

The 13 consumer ports sit in 9 distinct contexts (unchanged from brief 13).
The single working edge today is inherent-adapter → complement `A` (exact
triple match). The adapter input (shared system triple) matches exactly
legs 1–2 and becomes their first consumer; the adapter output
(complement-`A` triple) matches ONLY the complement `A` input among the 13
consumers, so it binds no series/parallel leg input and creates no
accidental composition edges — a combination result can never re-enter as
a leg. The output triple equals the inherent-adapter output triple, making
this the second producer of that triple; dual emission of one triple is
precedented in this registry (inherent-availability r1 and r2 emit an
identical triple). The bridge orphans zero working chains by construction,
and after admission both redundant chains execute end to end:
two-leg/three-leg parallel → this bridge → complement → steady-scope →
annual-downtime.

## Decision: one meaning adapter, not a revision or a jump

The brief-7–9 convention picks the minimal honest side that orphans
nothing. This is the meaning-adapter shape of the M2-D RAID precedent
(brief 10) and brief-13 links 2–3: the meanings differ
(`parallel_availability` vs `component_availability`), so no contexts-only
r2 can bind at all, and a meaning-changing r2 is rejected on both sides:

- Producer-side r2 (stamp `component_availability` onto the parallel
  outputs) costs two revisions against one record and misdescribes both
  ends: a combination result is not a leg value, and the leg/input roles
  of the parallel records' own ports would be contradicted. Rejected.
- Consumer-side r2 (stamp `parallel_availability` onto complement `A`)
  would restrict the generic single-item complement to parallel
  subsystems only — and it would orphan the WORKING
  inherent-adapter → complement edge, the brief-14 rejection shape (a
  move that breaks a live chain). Rejected.

Rejected alternative — direct parallel-to-steady-unavailability jump
(`Us = 1 − Ap` in one record, skipping the complement): it duplicates the
complement's reviewed `1 − A` arithmetic in a second home, so one equation
would have two owners; it bypasses the admitted complement → steady-scope
→ downtime chain instead of joining it, silently re-asserting that chain's
reviewed per-hop scope readings (mission-instant → accounting-year,
item/system identity) inside a single hop; and it conflates two different
claim kinds — a scope relabel (identity, no arithmetic) and an arithmetic
complement — that the representation contract
(`knowledge/decisions/representation-contract-v0.md`: different meanings
want explicit adapter models, no silent equivalence) requires to stay
separately reviewable. One single-hop identity adapter plus the admitted
chain composes the same path with every hop audited. Rejected.

## Scope reading (why the relabel is honest)

Both endpoint definitions describe the same mathematical object: a
steady-state probability that the item is operable. The producer outputs
are defined as "Steady-state availability of the two-/three-leg parallel
combination" (b02/b11) and the complement input as "Steady-state
availability (probability operable)" (b02); the complement's own
assumption — its input "is a steady-state availability (probability
operable) under stated conditions" — is satisfied by construction. The
tight scope carried in assumptions: the evaluated parallel subsystem plays
the component/item role at the same mission instant (subsystem-as-item
identity; same environment/conditions; no fleet averaging or cross-item
substitution); independence and topology preconditions were discharged
upstream inside the parallel records, so the complement's "not a
multi-component composition model" scope is respected — composition
already happened upstream, and the adapter feeds the already-composed
result as a single item value into the `1 − A` complement only. Bridge use
into the complement record only; the N-identical legs-context output,
series/voted/window combination outputs, instantaneous/interval scope, and
any leg-input direction are excluded.

## Record authored (batch computer-science-parallel-b01)

`computer-science--parallel-availability-component-scope@r1`: IN `Ap` =
shared producer-output face, OUT `A` = complement-input face, expression
`Ap`, guards `Ap >= 0`, `Ap <= 1` (mirror the producers' `[0,1]` range).

It is a `definition`-kind identity record: the compatibility claim above
lives in assumptions, never in arithmetic. Faces were embedded byte-exact
by reading the registry read-only at author time. It carries 3 numeric
references (the EventHelix two-leg oracle 0.99/0.99 → 0.9999 recomputed
through the two-leg expression, the EventHelix three-leg oracle 0.99³ →
0.999999 recomputed through the three-leg expression, plus the shared
perfect-combination boundary 1), 1 domain + 1 missing-input rejection
case, and project-derivation sources citing both producer keys and the
consumer key. Reference replay is exact substitution.

Out of scope (separate near-misses for other briefs): the N-identical
parallel output (`legs` context), the `series_availability` terminus
(3 producers, 0 consumers), and the 12 remaining `component_availability`
leg inputs, which stay unbound (fail-closed, as today).

## Resubmission

Batch `computer-science-parallel-b01` is validated and packed in
`.runs/compat-curation/adapters-parallel/` (bundle + return ZIP as usual)
for re-review per protocol. It was never staged or imported; the registry
is untouched.
