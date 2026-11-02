---
id: decision-seven-axis-dimension-migration
type: decision
title: Seven-axis dimension migration with SI temperature, current and amount
summary: 'Owner-approved: Dimensions grow 4->7 (mass, length, time, currency, temperature, current, amount).
  K/A/mol base units at scale 1; V and ohm carry 1/3.6e6 and S carries 3.6e6 off the kWh energy base so
  V=IR and P=IV close through registry scales. Curator unit strings adopted verbatim (m^2, ohm m, K^-1,
  S/m). K serves absolute temperatures and differences; guards and review scope carry the distinction
  (known limitation). Stored digests unaffected (models hash meaning/unit strings, not vectors): 98/98
  baseline digests identical, no DB migration, 109 tests green, 7/7 legacy replays exact. Finance-owned
  elapsed_time stays dimensionless; inlined dimensional literals must be canonical, physical constants
  ride input variables (Kleiber precedent).'
status: accepted
created: '2026-11-01'
updated: '2026-11-01'
topics:
- engine
- vocabulary
- representation
confidence: null
relations:
- {type: resolves, target: question-dimensional-and-unit-type-system}
- {type: extends, target: decision-canonical-expressions-for-conversion-records}
- {type: evidence, target: finding-wave2-intake-axes-blocked}
---

# Seven-axis dimension migration with SI temperature, current and amount

## Decision

Extend the engine dimension vector from 4 to 7 axes, appending temperature,
current, and amount-of-substance after the existing mass/length/time/currency
positions (currency stays at index 3, so the no-implicit-FX guard is
untouched). Ship SI base units K, A, mol at scale 1; derive electrical units
from the kWh energy base (V and ohm at 1/3.6e6, S at 3.6e6) so Ohm's law and
P=IV close through registry scales with no inlined factors.


## Context

Wave-2 intake admitted everything the 4-axis engine could express (98
eligible) and queued 14 recommend-admit records on missing axes: 5 thermal
(temperature), 8 circuits (current), 1 carrier-density (amount); see
[[finding-wave2-intake-axes-blocked]]. Thermodynamics and materials-science
lanes need the same axes. The owner approved the migration.


## Alternatives considered

- Collapse temperature/current onto existing axes: rejected, a silent remap
  (voltage is not dimensionless; absolute temperature is not energy).
- Per-record dimensionless workarounds: rejected, destroys composition (V=IR
  could not connect to P=IV through meanings).
- Defer until more records queue: rejected, the engine was the proven binding
  constraint and the migration turned out digest-safe (below).


## Rationale

Discovery showed all dimension arithmetic is length-agnostic (generic zip over
vectors) and `model_digest` hashes meaning/unit strings, never vectors — so
the migration preserves every stored digest by construction. The only
touchpoints were the contracts table, one test literal, and two mechanics
literals. Proof before vocabulary: 108 tests green, 98/98 baseline digests
identical with no DB migration, 7/7 legacy runs replay exact.


## Consequences

- Runtime 0.21.0 ships be-2 + circuits-1 vocabulary and admits 11 queued
  records (4 thermal, 7 circuits); registry 98 -> 109.
- K serves both absolute temperatures and differences (curator convention);
  guards and review scope carry the distinction. A future dK split is
  possible but unrequested.
- `elapsed_time` stays finance-owned (dimensionless); physical durations use
  `duration` (one circuits r2 briefed for the rename).
- Inlined dimensional literals must be canonical; physical constants ride
  input variables with registry units (Kleiber precedent; one radiative r2
  briefed for a sigma input).
- New runs embed 7-vector manifests; old run files are untouched and replay
  exact.


## Revisit if
