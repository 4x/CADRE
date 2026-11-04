# Adapter brief: item-scope → leg-scope bridge feeding the two-leg parallel input (brief 18)

To: component-scope adapter curator (batch computer-science-compscope-b01, 1 new record)
From: component-scope bridge curation (native compat-curation subagent), 2026-11-04
Status: proposed (mechanical — no admitted record is revised; all reviews stand)

## What happened

The redundant-availability chains cannot start: two producers emit
`component_availability` in the item scope, but the two-leg
parallel-availability record takes its leg inputs `A1`/`A2` in the
system scope, so no audited edge exists from any component value into any
parallel leg input and composers stop before the combination. No evidence
was questioned and nothing was modified; the endpoint records stand as
reviewed (recommend-admit: inherent-adapter via brief 13 as admitted,
parallel-bridge via brief 16 as admitted, two-leg parallel via b02).

Exact port triples, read read-only from `.registry/models.sqlite3` on
2026-11-04 (`mode=ro`; never staged, reviewed, admitted, or otherwise touched):

Producer 1 —
`computer-science--inherent-availability-component-scope@r1.runtime1` output:

- (`component_availability`, `1`,
  `same item, mission instant and conditions as U`)

Producer 2 —
`computer-science--parallel-availability-component-scope@runtime1` output:

- (`component_availability`, `1`,
  `same item, mission instant and conditions as U`)

Consumer —
`computer-science--parallel-availability@r1.runtime1` inputs:

- `A1`: (`component_availability`, `1`,
  `same system, mission instant and environment as A2 and A`)
- `A2`: (`component_availability`, `1`,
  `same system, mission instant and environment as A1 and A`)

Same meaning, same unit on every port — only the contexts differ
(item/instant/conditions-as-`U` vs system/instant/environment-as-legs-and-`A`).

The two producers carry byte-identical triples, so one adapter input binds
both — the brief-7/14 minimality shape (one record fixes both upstream
legs). The two consumer faces differ from each other (each names the other
leg), so one adapter output face can bind exactly one of them; this brief
binds `A1` and leaves `A2` a separate near-miss.

Three-leg scoping check (done, out of scope): every three-leg
parallel-availability input face names three co-ports
(`as A2, A3 and A`, `as A1, A3 and A`, `as A1, A2 and A`), so no three-leg
face is byte-identical to the two-leg `A1` face — this adapter is scoped to
the two-leg `A1` face explicitly. The three-leg faces are additionally
byte-equal to the same-named series-three input faces, so a three-leg bridge
would bind across parallel/series topologies and needs its own review.

## Registry orphan survey (all 249 admitted models, 2026-11-04)

`component_availability` (`1`) — 2 producers, 13 consumer ports, 2 working edges:

| side | record@rev | port | context |
|---|---|---|---|
| OUT | inherent-availability-component-scope@r1 | — | `same item, mission instant and conditions as U` ✅ |
| OUT | parallel-availability-component-scope@r1 | — | `same item, mission instant and conditions as U` ✅ |
| IN | parallel-availability-n-identical@r1 | `X` | `same legs, mission instant and environment as N and A` |
| IN | parallel-availability-three@r1 | `A1` | `same system, mission instant and environment as A2, A3 and A` |
| IN | parallel-availability-three@r1 | `A2` | `same system, mission instant and environment as A1, A3 and A` |
| IN | parallel-availability-three@r1 | `A3` | `same system, mission instant and environment as A1, A2 and A` |
| IN | parallel-availability@r1 | `A1` | `same system, mission instant and environment as A2 and A` 🎯 |
| IN | parallel-availability@r1 | `A2` | `same system, mission instant and environment as A1 and A` |
| IN | series-availability-n-identical@r1 | `X` | `same legs, mission instant and environment as N and A` |
| IN | series-availability-three@r2 | `A1`/`A2`/`A3` | same three system contexts as parallel-three (byte-equal per leg) |
| IN | series-availability@r1 | `A1`/`A2` | `same system, mission instant, environment and support conditions as ...` (2 distinct) |
| IN | unavailability-complement@r1 | `A` | `same item, mission instant and conditions as U` ✅ |

The 13 consumer ports sit in 9 distinct contexts (unchanged from briefs
13/16). The two working edges today are both producers → complement `A`
(exact triple match). The adapter input (shared item triple) matches exactly
both producers and becomes their second consumer alongside the complement;
the adapter output (two-leg-`A1` triple) matches ONLY the `A1` input among
the 13 consumers, and no registry producer emits that triple today, so the
adapter is its first producer and creates no accidental composition edges.
The bridge orphans zero working chains by construction, and after admission
the two-leg redundant chain starts: either item-scope component value → this
bridge → parallel `A1` (with `A2` still user-supplied or separately
bridged) → parallel combination → brief-16 bridge → complement → steady-scope
→ annual-downtime.

## Decision: one context adapter, not a revision

The brief-7–9 convention picks the minimal honest side that orphans
nothing. This is the same-meaning/different-contexts near-miss shape as
briefs 7–9 and 15/17, and no one-sided r2 is honest here:

- Producer-side r2 (restamp both item-scope outputs to the `A1` context)
  costs two revisions against one record and misdescribes the value's primary
  role — and it would orphan the two WORKING producer → complement edges,
  the brief-14 rejection shape (a move that breaks live chains). Rejected.
- Consumer-side r2 (`A1` input → item context) would stamp `as U` onto the
  parallel record, asserting a symbol undefined in that record; brief 8
  rejects exactly this shape (stamping a context with undefined symbols is
  false). Rejected.

One identity adapter (input face = shared producer output, output face =
two-leg `A1` input) binds the leg with 0 revisions and 0 orphans, preserving
every reviewed record.

## Scope reading (why the relabel is honest)

All endpoint ports carry the same meaning — a steady-state probability that
the item is operable — so only the context face changes, from the
single-item complement view to the first-leg-of-the-parallel-pair view. The
tight scope carried in assumptions: the evaluated item plays the `A1` leg
role of the two-leg parallel system at the same mission instant
(item-as-leg identity; same environment/conditions; `A2` a distinct item at
that same instant/environment; no fleet averaging or cross-item
substitution). The parallel record's mutual-independence precondition is
explicitly NOT discharged here — whoever composes the carried `A1` value
with an `A2` value must assert it, which also covers hierarchical-RBD feeds
where an already-composed subsystem result enters as a leg (subsystem-to-`A2`
independence then required). Bridge use into the two-leg parallel record
only; the `A2` face, three-leg faces, legs contexts, series
support-conditions contexts, and non-steady-state scopes are excluded.

## Record authored (batch computer-science-compscope-b01)

`computer-science--component-availability-system-leg-scope@r1`: IN `Ac` =
shared producer-output face, OUT `A1` = two-leg-`A1` face, expression
`Ac`, guards `Ac >= 0`, `Ac <= 1` (mirror the producers' `[0,1]` range).

It is a `definition`-kind identity record: the compatibility claim above
lives in assumptions, never in arithmetic. Faces were embedded byte-exact
by reading the registry read-only at author time. It carries 3 numeric
references (the 0.99 EventHelix leg value from the two-leg record's own
oracle, the 0.5 mid-scale leg carry, plus the shared perfect-leg boundary
1), 1 domain + 1 missing-input rejection case, and project-derivation
sources citing both producer keys and the consumer key. Reference replay is
exact substitution.

Out of scope (separate near-misses for other briefs): the two-leg `A2` face,
the three-leg parallel/series faces (with their cross-topology byte-equality),
the N-identical legs faces, and the two-leg series support-conditions faces —
12 consumer ports stay unbound (fail-closed, as today).

## Resubmission

Batch `computer-science-compscope-b01` is validated and packed in
`.runs/compat-curation/adapters-compscope/` (bundle + return ZIP as usual)
for re-review per protocol. It was never staged or imported; the registry
is untouched.
