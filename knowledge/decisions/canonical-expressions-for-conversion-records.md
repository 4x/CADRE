---
id: decision-canonical-expressions-for-conversion-records
type: decision
title: Record expressions must be written in canonical base units; conversion records project through
  registry scales
summary: 'The engine normalizes inputs to canonical base units before evaluating the expression and converts
  the result to the output unit (runtime.execute). A relationship whose math inlines a conversion factor
  already encoded in unit scales (first case: GB-to-B records with N*1e9) double-counts and fails reference
  replay at staging. Curators must write expressions in canonical base units; unit-conversion records
  therefore project as identities over registry scales, with the factor documented in constants and vocabulary
  evidence, never inlined. Failed projections are returned as needs-revision, never silently adjusted.'
status: accepted
created: '2026-11-01'
updated: '2026-11-01'
topics:
- curation
- runtime
- vocabulary
confidence: null
relations: []
---

# Record expressions must be written in canonical base units; conversion records project through registry scales

## Decision

Curated record expressions MUST be written in the canonical base units of the runtime unit registry. A unit-conversion record (input and output ports in different units of one dimension) MUST project as the canonical-identity expression over registry scales, with the conversion factor documented in the record `constants` array and in the vocabulary evidence — never inlined in `relationship.expression`. Projections that fail reference replay are returned to the curator as needs-revision; dev never edits record math.


## Context

`runtime.execute` normalizes every input to canonical base units (`value.bind(...) * input-scale`) before evaluating the expression, then converts the result into the output port unit. All 53 previously admitted models used scale-1 ports, so curators never encountered the rule. The first scale-bearing curated records — `computer-science--decimal-gigabyte-to-byte` and `computer-science--binary-gibibyte-to-byte` (r1, reviewer recommend-admit) — inline `N * 1000000000` / `N * 1073741824` in display units; the engine multiplies by the GB/GiB scale first, so staging fails reference replay fail-closed (`Runtime projection failed reference replay`). The reviews stand; the record math needs a canonical-units r2 (`B = N`).


## Alternatives considered

- Decorative scale-1 byte units (GB/B/GiB all scale 1) so display-unit math replays: rejected — it would make the units table lie about magnitudes and silently break any future same-meaning cross-unit binding. The km/m precedent (scale 1000) keeps scales honest.
- Dev-side expression rewriting at projection: rejected — violates the never-modify-returns rule and destroys the evidence link between reviewed research and runtime model.


## Rationale

Single source of truth for conversion factors (the versioned vocabulary, with NIST/IEC evidence) beats per-model inlining; fail-closed staging caught the mismatch with evidence instead of admitting wrong math. Meaning/context binding (`gigabyte_count` vs `byte_count`) still prevents misuse of the identity projection.


## Consequences

- CS curator owes r2 revisions for the two byte-conversion records (see `data/curation/corrections/computer-science-b02-b03-canonical-units-brief.md`).
- Future assignment kits must state the canonical-expression rule with the GB example; reviewers cannot catch this packet-isolated (they lack runtime replay).
- Conversion-heavy domains (units, metrology) will produce many identity-expression projections; that is expected, not degenerate.


## Revisit if

The engine ever evaluates expressions in display units, or a `display_expression` field is added alongside the canonical one.
