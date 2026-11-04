# Correction brief: RAID-fill chain identity adapters (brief 10)

To: computer-science curator (new batch computer-science-adapters-b01)
From: dev intake (compat audit), 2026-11-03
Status: new-records (mechanical, not scientific — all cited reviews stand as recommend-admit)

## What happened

The RAID-fill chain cannot execute: RAID 5 usable capacity (GB) →
decimal-gigabyte-to-byte → byte count (B) → transfer-time data size,
with the transfer-time rate leg fed by decimal-megabyte-rate-to-byte-rate.
All four endpoint records passed review, but chaining requires exact
`(meaning, context)` equality on linked ports (units already match on
each leg), and each leg joins different meanings — a different near-miss
shape from the same-meaning context alignments of briefs 8 and 9, which
wants explicit identity adapter records rather than a revision of either
side. No evidence was questioned and nothing was modified.

Exact port triples (registry, read 2026-11-03):

Leg A1 (capacity GB → converter input GB):

- Producer `computer-science--raid5-usable-capacity@r1.runtime1` output `U`:
  meaning `parity_usable_capacity`, unit `GB`, context

> same homogeneous parity array as inputs

- Consumer `computer-science--decimal-gigabyte-to-byte@r2.runtime1` input `N`:
  meaning `gigabyte_count`, unit `GB`, context

> same stored object and decimal convention as B

Leg A2 (converter output B → transfer data size B):

- Producer `computer-science--decimal-gigabyte-to-byte@r2.runtime1` output `B`:
  meaning `byte_count`, unit `B`, context

> same stored object and decimal convention as N

- Consumer `computer-science--transfer-time@r1.runtime1` input `D`:
  meaning `data_size`, unit `B`, context

> same transfer, link, encoding and averaging window as R and T

Leg A3 (converter output B/s → transfer rate B/s):

- Producer `computer-science--decimal-megabyte-rate-to-byte-rate@r2.runtime1`
  output `R_Bps`: meaning `byte_rate`, unit `B/s`, context

> same interface, averaging interval and sustained/peak basis as R_MBps

- Consumer `computer-science--transfer-time@r1.runtime1` input `R`:
  meaning `transfer_rate`, unit `B/s`, context

> same transfer, link, encoding and averaging window as D and T

## Why adapters, not revision

Neither side of any leg can adopt the other's port without
misdescribing itself: the RAID output is an array property while the
converter input counts a stored object; a converter byte count is a
stored-object tally while the transfer input sizes one transfer; an
interface byte rate is an asserted converter output while the transfer
input must be the sustained rate of the transfer itself. Relabeling any
endpoint would assert provenance or application-profile conditions its
record does not establish. Each adapter instead states the compatibility
claim explicitly — same decimal volume / same byte tally / same
sustained rate, carried from the producer view to the consumer view —
with its scope in `assumptions`.

A registry survey of all 235 admitted models shows each adapter slot is
clean: no producer emits `gigabyte_count`, `data_size`, or
`transfer_rate` today; no consumer takes `parity_usable_capacity`,
`byte_count`, or `byte_rate` today; the exact-triple producers are
exactly the three cited above. (`binary-gibibyte-to-byte@r2` emits
`byte_count` in a second context, and eight further converters emit
`byte_rate` in their own contexts; those binary- and rate-side legs are
separate near-misses for other briefs.) The adapters therefore orphan
zero chains and break zero working edges: after admission the full
RAID 5 → gigabyte → byte → transfer-time chain executes at the stated
decimal conventions.

## Prescription (3 new records, r1)

All three records are definition-kind expression identities over
same-unit ports (so display replay passes directly): the input variable
carries the PRODUCER view (producer symbol, meaning, unit, context
byte-identical) and the output variable carries the CONSUMER view
(consumer symbol, meaning, unit, context byte-identical).

A1 `computer-science--parity-capacity-as-gigabyte-count` (r1):

- Input `U`: `parity_usable_capacity`, `GB`, the RAID output context
  above, byte-identical. Guard `U >= 0` (producer nonnegativity).
- Output `N`: `gigabyte_count`, `GB`, the converter input context
  above, byte-identical. Expression `U`.
- Assumptions: compatibility claim (a RAID 5 usable capacity in decimal
  GB is consumable as the decimal-gigabyte count of the same stored
  volume) + scope (decimal GB only; the array volume is the converter's
  stored object; overhead/formatting exclusions inherited from both
  sides).

A2 `computer-science--byte-count-as-data-size` (r1):

- Input `B`: `byte_count`, `B`, the converter output context above,
  byte-identical. Guard `B >= 0` (producer nonnegativity).
- Output `D`: `data_size`, `B`, the transfer input context above,
  byte-identical. Expression `B`.
- Assumptions: compatibility claim (the converter's byte tally sizes
  the transfer) + scope (same byte tally moved into one transfer's
  link/encoding/averaging window; ideal bulk-transfer bound inherited
  from the consumer).

A3 `computer-science--byte-rate-as-transfer-rate` (r1):

- Input `R_Bps`: `byte_rate`, `B/s`, the rate-converter output context
  above, byte-identical. Guard `R_Bps >= 0` (producer nonnegativity).
- Output `R`: `transfer_rate`, `B/s`, the transfer input context above,
  byte-identical. Expression `R_Bps`.
- Assumptions: compatibility claim (the asserted interface byte rate is
  the transfer's sustained rate) + scope (sustained-average basis on the
  same interface and averaging interval; peak/burst substitution
  excluded, inherited from both sides).

Each record: 2+ numeric references with independent arithmetic (recompute
the carried value through the producer's own expression or an
independent count, never by restating the identity), 1+ rejection case
(negative input against the guard), and `project-derivation` sources
citing both bridged records plus the registry vocabulary. No new
meanings or units: every port reuses admitted vocabulary.

## Resubmission

Submit the three r1 records as ONE batch (`computer-science-adapters-b01`,
bundle + return as usual) for review per protocol since record text is new.
