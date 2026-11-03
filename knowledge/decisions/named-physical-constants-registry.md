---
id: decision-named-physical-constants-registry
type: decision
title: Named physical constants registry resolved in expressions
summary: 'New connected_models/constants.py: pi, stefan_boltzmann, gravitational_constant, avogadro with
  SI values, registry units, provenance, and exact flags, validated at import. Expressions name them (e
  * stefan_boltzmann * A * ...); engine resolves canonical value and dims; curation allows the names and
  forbids shadowing. Universal-fixed vs case-specific rule: universals in registry, parameters stay inputs
  (corrects the sigma-as-input brief, rewritten). Kits ship the table. Runtime 0.23.0, 123 tests green.'
status: accepted
created: '2026-11-02'
updated: '2026-11-02'
topics:
- engine
- vocabulary
- representation
confidence: null
relations:
- {type: extends, target: decision-canonical-expressions-for-conversion-records}
- {type: relates-to, target: decision-validated-unit-alias-registry}
---

# Named physical constants registry resolved in expressions

## Decision

Give universal physical constants names in a versioned registry table
instead of inlining magic literals or forcing them through input
variables. Each entry carries its SI value, registry unit, provenance
source, and an exact flag (definitive vs CODATA-measured). The engine
resolves names to canonical values and dimensions at the same two hooks
that serve inputs; curation permits the names in expressions and forbids
declaring symbols that shadow them, mirroring the scalar-function rule.


## Context


## Alternatives considered

- Inlined literals (status quo): rejected; unreadable, unprovenanced,
  drift-prone, and unit-carrying literals silently mis-evaluate under
  canonical units (sigma was 3.6e6x off).
- Constants as inputs (Kleiber-style): rejected for universals; it forces
  every question to state sigma as a "fact". Kept for per-case parameters
  (B0), which users genuinely supply or fit.
- Constants as zero-input models: rejected; bloats graphs and taxes the
  composer while still needing this table for values.


## Rationale


## Consequences

- Seed set (all with queued demand): stefan_boltzmann, G, avogadro, pi.
  Euler's number stays out: `e` is taken by emissivity precedent.
- Radiative r2 brief rewritten to the named-constant form with recomputed
  expectations (blackbody 58.241673 -> 58.245519 at tol 1e-6).
- Kits ship the table; curator instructions updated with the naming rule.
- Uncertainty still out of scope; source revisions make CODATA updates
  traceable.


## Revisit if
