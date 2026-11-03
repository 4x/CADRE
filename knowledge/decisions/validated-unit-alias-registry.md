---
id: decision-validated-unit-alias-registry
type: decision
title: Validated unit-alias registry in contracts with inspection command
summary: 'UNIT_ALIASES promoted from a query-layer dict to a validated table beside UNITS: import-time
  checks reject unknown targets, canonical shadowing, chains, and dead entries. Lookup is exact-first,
  fixing uppercase canonicals (V/A/K/C/W/Btu previously lowercased to nonexistence, S wrongly hit seconds).
  Kits ship the alias map for curators; new units command inspects dims/scales/aliases. Grandfathered
  duplicate canonicals (m^2/m2) stay; future spelling variants enter as aliases. Runtime 0.22.0, 117 tests
  green.'
status: accepted
created: '2026-11-02'
updated: '2026-11-02'
topics:
- vocabulary
- engine
- representation
confidence: null
relations:
- {type: relates-to, target: question-dimensional-and-unit-type-system}
- {type: extends, target: decision-seven-axis-dimension-migration}
---

# Validated unit-alias registry in contracts with inspection command

## Decision

Promote lexical unit aliases from the query-layer `UNIT_ALIASES` dict to a
validated table in `contracts.py` beside `UNITS`, versioned with the same
per-batch provenance convention. An import-time validator rejects unknown
targets, canonical shadowing, alias chains, identically-normalizing
entries, and aliases that shadow a canonical they do not point at. Lookup
is exact-first (canonical case wins) with normalization-plus-alias as
fallback and explicit passthrough for unknown spellings, which the binder
rejects with a clear error.


## Context


## Alternatives considered


## Rationale


## Consequences

- Fixed latent misresolution: uppercase canonicals without lowercase
  aliases (V, A, K, C, W, Btu) previously lowercased to nonexistence, and
  S (siemens) wrongly resolved to seconds. New units are queryable.
- Curation kits ship the alias map; new `units [filter]` command inspects
  dimensions, scales, and alias groupings.
- Grandfathered duplicate canonicals (m^2/m2) stay pinned by admitted
  ports; future spelling variants enter as aliases only.
- Quote-consistency checking now recognizes canonical spellings too, so
  contradictions like "5 V" claimed as amperes are caught.


## Revisit if
