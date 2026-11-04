# Adapter brief: megabit-sourced bit-rate bridge for the download-time chain (brief 15)

To: bits-leg adapter curator (batch computer-science-bits-b01, 1 new record)
From: bits-leg bridge curation (native compat-curation subagent), 2026-11-04
Status: proposed (mechanical — no admitted record is revised; all reviews stand)

## What happened

Download-time chains over megabit links cannot start: the bits leg into the
bit-to-byte grouping fails fail-closed under exact `(meaning, context)` port
equality (`Port.require_compatible` in `connected_models/contracts.py`; units
already match at `bit/s`). Brief 2 moved both endpoint expressions to
canonical identities and brief 5 confirmed the byte-rate identity replays
through the registry scales — but the decimal-megabit output and the
byte-rate `R_bps` input carry the same meaning in different contexts, so no
audited edge exists and composers stop at the megabit conversion. No evidence
was questioned and nothing was modified; the endpoint records stand as
reviewed.

Revision note: the delegated task named the endpoints `@r1`; the registry
holds `@r2` for both. That is the same near-miss: brief 2 changed only the
expressions (`R_mbps * 1000000` → `R_mbps`, `R_bps / 8` → `R_bps`) and kept
every variable, port, and unit byte-identical, verified by diffing the r1
variables in `data/curation/reviews/computer-science-b04-bundle.json` against
the r2 variables in
`data/curation/reviews/computer-science-ncs-c02-bundle.json`. The faces below
bind the live registry triples, which equal the r1 triples.

Exact port triples, read read-only from `.registry/models.sqlite3` on
2026-11-04 (`mode=ro`; never staged, reviewed, admitted, or otherwise touched):

Producer —
`computer-science--decimal-megabit-rate-to-bit-rate@r2.runtime1` output:

- (`bit_rate`, `bit/s`,
  `same link, averaging interval and sustained/peak basis as R_mbps`)

Consumer —
`computer-science--bit-rate-to-byte-rate@r2.runtime1` input `R_bps`:

- (`bit_rate`, `bit/s`,
  `same link, averaging interval and sustained/peak basis as R_Bps`)

Same meaning, same unit; the contexts differ only in which co-port they name
(`R_mbps` at the producer, `R_Bps` at the consumer).

## Registry orphan survey (all 247 admitted models, 2026-11-04)

`bit_rate` (`bit/s`) — 12 producers, 1 consumer port, 0 working edges:

| side | record@rev | port | context |
|---|---|---|---|
| OUT | decimal-megabit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_mbps` |
| OUT | decimal-kilobit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_kbps` |
| OUT | decimal-gigabit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_gbps` |
| OUT | decimal-terabit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_tbps` |
| OUT | decimal-petabit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_pbps` |
| OUT | binary-kibibit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_kibps` |
| OUT | binary-mebibit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_mibps` |
| OUT | binary-gibibit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_gibps` |
| OUT | binary-tebibit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_tibps` |
| OUT | binary-pebibit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_pibps` |
| OUT | binary-exbibit-rate-to-bit-rate@r2 | — | `same link, averaging interval and sustained/peak basis as R_eibps` |
| OUT | decimal-gigabyte-rate-to-bit-rate@r2 | — | `same interface, averaging interval and sustained/peak basis as R_GBps` |
| IN | bit-rate-to-byte-rate@r2 | `R_bps` | `same link, averaging interval and sustained/peak basis as R_Bps` |

Every producer context names its own input symbol; the single consumer names
`R_Bps`. No producer context equals the consumer context, so all twelve
producer/consumer pairs are broken today and the `bit_rate` value is a chain
terminus at every producer.

The adapter input (megabit triple) matches exactly one producer (the
decimal-megabit output) and becomes its first consumer. The adapter output
(byte-grouping triple) matches exactly the one consumer (`R_bps`) and no
other port. No working chain emits or consumes `bit_rate` today, so the
bridge orphans zero working chains by construction, and after admission the
bits leg executes: decimal-megabit-rate-to-bit-rate → this bridge →
bit-rate-to-byte-rate.

## Decision: one adapter, not a context-r2

The brief-7–9 convention picks the minimal honest side that orphans nothing.
This is the same near-miss shape as brief-14 (same meaning, different
contexts), and brief-14 is the direct precedent: it prescribed an adapter,
not a revision, because both sides' contexts honestly describe their own
ends. No one-sided r2 is honest here either:

- Producer-side r2 (megabit output → consumer context) would stamp `as R_Bps`
  onto the megabit record, asserting a symbol undefined in that record; brief
  8 rejects exactly this shape (stamping a context with undefined symbols is
  false). Rejected.
- Consumer-side r2 (`R_bps` input → producer context) would stamp `as R_mbps`
  onto the byte-rate record, likewise asserting a symbol undefined there, and
  would fix only the megabit leg while leaving the same question for the
  other eleven producers. Rejected.

One identity adapter (input face = producer output, output face = consumer
input) fixes the leg with 0 revisions and 0 orphans, preserving every
reviewed record.

## Record authored (batch computer-science-bits-b01)

`computer-science--megabit-bit-rate-to-byte-scope@r1`: IN `R_bps_mbit` =
producer-output face, OUT `R_bps` = consumer-input face, expression
`R_bps_mbit`, guard `R_bps_mbit >= 0` (mirrors the producer range; the
consumer enforces `R_bps >= 0` at its own port, so the `R = 0` idle-link
boundary passes the bridge and is accepted downstream — the brief-14/F1
boundary convention).

It is a `definition`-kind identity record: the compatibility claim (same
link, same averaging interval, same sustained/peak basis — the contexts
differ only in which co-port they name, not in the value) and the
byte-grouping scope live in assumptions, never in arithmetic. Faces were
embedded byte-exact by reading the registry read-only at author time. It
carries 3 numeric references (the Fast-Ethernet 100-Mbit/s producer oracle,
the consumer-side 1-Mbit/s grouping input, plus the shared zero boundary), 1
domain + 1 missing-input rejection case, and project-derivation sources
citing the producer key and the consumer key. Reference replay is exact
substitution through identical `bit/s` scales.

Out of scope (separate near-misses for other briefs): the eleven other
orphaned `bit_rate` producers (decimal kilo/giga/tera/peta, binary
kibi/mebi/gibi/tebi/pebi/exbi, and the gigabyte-interface record), and the
downstream `byte_rate` → `transfer_rate` gap (the byte-rate output is
same-link context while `byte-rate-as-transfer-rate@r1` takes its input in
the same-interface context; past that gap the transfer-rate → transfer-time
edge already binds).

## Resubmission

Batch `computer-science-bits-b01` is validated and packed in
`.runs/compat-curation/adapters-bits/` (bundle + return ZIP as usual) for
re-review per protocol. It was never staged or imported; the registry is
untouched.
