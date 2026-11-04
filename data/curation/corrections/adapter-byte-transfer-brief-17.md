# Adapter brief: link-byte-rate → interface bridge for the download-time chain (brief 17)

To: byte-transfer adapter curator (batch computer-science-bytetransfer-b01, 1 new record)
From: byte-transfer bridge curation (native compat-curation subagent), 2026-11-04
Status: proposed (mechanical — no admitted record is revised; all reviews stand)

## What happened

Download-time chains over bit-sourced links cannot reach transfer time: the
byte leg out of the bit-to-byte grouping fails fail-closed under exact
`(meaning, context)` port equality (`Port.require_compatible` in
`connected_models/contracts.py`; units already match at `B/s`). Brief 15
bridged the decimal-megabit output into the grouping input — but the grouping
output and the transfer-rate `R_Bps` input carry the same meaning in different
contexts (same-link vs same-interface), so no audited edge exists and
composers stop at the grouping record. No evidence was questioned and nothing
was modified; the endpoint records stand as reviewed.

Exact port triples, read read-only from `.registry/models.sqlite3` on
2026-11-04 (`mode=ro`; never staged, reviewed, admitted, or otherwise touched):

Producer —
`computer-science--bit-rate-to-byte-rate@r2.runtime1` output:

- (`byte_rate`, `B/s`,
  `same link, averaging interval and sustained/peak basis as R_bps`)

Consumer —
`computer-science--byte-rate-as-transfer-rate@r1.runtime1` input `R_Bps`:

- (`byte_rate`, `B/s`,
  `same interface, averaging interval and sustained/peak basis as R_MBps`)

Same meaning, same unit — the two ports even share the symbol `R_Bps` and the
identical definition ("Same asserted rate expressed in bytes per second");
only the contexts differ (link vs interface framing, and which co-port they
name: `R_bps` at the producer, `R_MBps` at the consumer).

## Registry orphan survey (all 247 admitted models, 2026-11-04)

`byte_rate` (`B/s`) — 9 producers, 1 consumer port, 1 working edge:

| side | record@rev | port | context |
|---|---|---|---|
| OUT | decimal-megabyte-rate-to-byte-rate@r2 | — | `same interface, averaging interval and sustained/peak basis as R_MBps` ✅ |
| OUT | decimal-petabyte-rate-to-byte-rate@r2 | — | `same interface, averaging interval and sustained/peak basis as R_PBps` |
| OUT | decimal-terabyte-rate-to-byte-rate@r2 | — | `same interface, averaging interval and sustained/peak basis as R_TBps` |
| OUT | binary-mebibyte-rate-to-byte-rate@r2 | — | `same interface, averaging interval and sustained/peak basis as R_MiBps` |
| OUT | binary-tebibyte-rate-to-byte-rate@r2 | — | `same interface, averaging interval and sustained/peak basis as R_TiBps` |
| OUT | binary-pebibyte-rate-to-byte-rate@r2 | — | `same interface, averaging interval and sustained/peak basis as R_PiBps` |
| OUT | binary-exbibyte-rate-to-byte-rate@r2 | — | `same interface, averaging interval and sustained/peak basis as R_EiBps` |
| OUT | bit-rate-to-byte-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_bps` |
| OUT | decimal-petabit-rate-to-byte-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_pbps` |
| IN | byte-rate-as-transfer-rate@r1 | `R_Bps` | `same interface, averaging interval and sustained/peak basis as R_MBps` |

The single working edge is decimal-megabyte → consumer `R_Bps` (exact triple
match — the consumer context literally equals the megabyte output context).
Every other producer context names its own co-port, so the remaining eight
producers match nothing and the grouping output is a chain terminus today.

Downstream of the gap, the transfer leg already binds: `transfer_rate`
(`B/s`) has 1 producer (byte-rate-as-transfer-rate@r1 output) and 1 consumer
(transfer-time@r1 input `R`) in the identical
`same transfer, link, encoding and averaging window as D and T` context — a
working edge, verified read-only.

The adapter input (link triple) matches exactly one producer (the grouping
output) and becomes its first consumer. The adapter output (interface triple)
matches exactly the one consumer (`R_Bps`) and no other port; it re-emits the
megabyte output triple, becoming its second producer alongside the working
edge, which is untouched. The bridge orphans zero working chains by
construction, and after admission the byte-transfer leg executes:
bit-rate-to-byte-rate → this bridge → byte-rate-as-transfer-rate →
transfer-time — and together with the brief-15 bridge, the full download
chain from the decimal-megabit link.

## Decision: one adapter, not a context-r2

The brief-7–9 convention picks the minimal honest side that orphans nothing.
This is the same near-miss shape as brief-15 (same meaning, different
contexts), and brief-15 is the direct precedent: it prescribed an adapter,
not a revision, because both sides' contexts honestly describe their own
ends. No one-sided r2 is honest here either:

- Producer-side r2 (grouping output → interface context) would stamp
  `as R_MBps` onto the byte-rate record, asserting a symbol undefined in
  that record; brief 8 rejects exactly this shape (stamping a context with
  undefined symbols is false). Rejected.
- Consumer-side r2 (`R_Bps` input → link context) would stamp `as R_bps`
  onto the transfer-rate record, likewise asserting a symbol undefined
  there — and it would orphan the WORKING decimal-megabyte → consumer edge,
  the brief-14 rejection shape (a move that breaks a live chain). Rejected.

One identity adapter (input face = producer output, output face = consumer
input) fixes the leg with 0 revisions and 0 orphans, preserving every
reviewed record.

## Record authored (batch computer-science-bytetransfer-b01)

`computer-science--link-byte-rate-to-interface-scope@r1`: IN `R_Bps_link` =
producer-output face, OUT `R_Bps` = consumer-input face, expression
`R_Bps_link`, guard `R_Bps_link >= 0` (mirrors the producer range; the
transfer-rate record carries the value onward under its own `R_Bps >= 0`
guard and transfer time enforces `R > 0` at its own port, so the `R = 0`
idle-link boundary passes both bridges and is rejected only at transfer
time — the brief-14/F1 boundary convention, matching the transfer-rate
record's own stated boundary behavior).

It is a `definition`-kind identity record: the compatibility claim (the
measured link is the interface's link over the same averaging interval at
the same sustained/peak basis — the contexts differ only in link-vs-interface
framing and in which co-port they name, not in the value) and the transfer
scope live in assumptions, never in arithmetic. Faces were embedded
byte-exact by reading the registry read-only at author time. It carries 3
numeric references (the producer-side 1-Mbit/s grouping oracle at 125,000
B/s, the consumer-side 100-MB/s decimal-count input, plus the shared zero
boundary), 1 domain + 1 missing-input rejection case, and
project-derivation sources citing the producer key and the consumer key.
Reference replay is exact substitution through identical `B/s` scales.

Out of scope (separate near-misses for other briefs): the seven other
orphaned `byte_rate` producers (decimal petabit link-context, decimal
petabyte/terabyte and binary mebi/tebi/pebi/exbi interface-contexts, each
naming its own co-port). The decimal-megabyte leg already binds and is
untouched; nothing downstream is gapped.

## Resubmission

Batch `computer-science-bytetransfer-b01` is validated and packed in
`.runs/compat-curation/adapters-bytetransfer/` (bundle + return ZIP as usual)
for re-review per protocol. It was never staged or imported; the registry is
untouched.
