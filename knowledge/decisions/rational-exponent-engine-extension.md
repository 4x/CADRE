---
id: decision-rational-exponent-engine-extension
type: decision
title: Rational-exponent engine extension with exact Fraction dimensions, staged functions next
summary: 'Runtime 0.16.0 extends the engine to bounded exact-rational exponents on dimensional bases with
  Fraction dimension vectors ([num,den] JSON encoding), fail-closed negative-base fractional powers, and
  an unchanged exact inverse-solver profile (fractional powers reject unknown-base solves, linear-factor
  solves still work). Staged plan confirmed: exponents first (shipped, Kleiber admitted), scalar functions
  (log/exp/sqrt) plus n-ary sum/prod next, forward-only. Variable exponents on dimensional bases stay
  rejected as dimensionally unsound (island record needs a normalized-area r2).'
status: accepted
created: '2026-11-01'
updated: '2026-11-01'
topics:
- runtime
- engine
- vocabulary
confidence: null
relations:
- type: addresses
  target: question-execution-runtime-for-heterogeneous-models
- type: relates-to
  target: question-dimensional-and-unit-type-system
- type: relates-to
  target: decision-canonical-expressions-for-conversion-records
---

# Rational-exponent engine extension with exact Fraction dimensions, staged functions next

## Decision

Extend the engine in confirmed stages: (1) rational exponents with exact `Fraction` dimension vectors (shipped in 0.16.0); (2) scalar functions (log/exp/sqrt) plus n-ary sum/prod over named inputs (next). The inverse solver keeps its exact rational-polynomial profile: models using new forms evaluate forward only, and unknown-under-fractional-power solves are rejected with `unsupported_degree` (proven by test); linear-factor solves (e.g. Kleiber for B0) still work. Variable exponents on dimensional bases stay rejected under any engine as dimensionally unsound.


## Context

Curator demand: Kleiber M^0.75 and island S=cA^z sat engine-blocked, and curators requested log, exp, sqrt and summation. Kleiber's fitted-normalization unit (`kcal/day per kg^0.75`) needs fractional dimension vectors, which the integer-only type system could not express. The owner confirmed staged delivery, forward-only solver treatment, and n-ary (not indexed) summation in the 2026-11-01 session. This supersedes the "no upgrade decision has been made" state in [[question-execution-runtime-for-heterogeneous-models]].


## Alternatives considered

- Float dimension vectors: rejected — float error (e.g. 3×(1/3)≠1) would break exact type equality; the type system must be exact even though evaluation is float64.
- Scaled-integer powers (fixed denominator): rejected — arbitrary precision cap, breaks on thirds/sevenths.
- Extending the solver to fractional/monotonic inverses: rejected for this stage — new soundness-proof burden; the exact profile is a feature, and linear-factor solves already cover the honest cases.
- Indexed summation (x[1..n]): originally deferred to the arrays/shape design owned by [[question-dimensional-and-unit-type-system]]; then designed and shipped in 0.18.0 as index-family inputs instead (shared element port + max_size bound, explicit Value/Reference tuples, sum/prod/len aggregation, expressions stay scalar, per-element transforms via upstream nodes). Elementwise family arithmetic and implicit broadcasting were rejected as unnecessary complexity.
- One big-bang increment (exponents + functions + summation): rejected — each stage independently tested and replayed instead.


## Rationale

Exact rationals keep dimensional type-checking sound (equality is exact) while float64 evaluation keeps legacy numerics bit-identical: 95 tests green, 90/90 eligible models revalidate, 7 legacy replays exact. Bounded denominators (≤1024) plus integer-ratio subtrees (`M ** (1/3)`) admit every practical science exponent while rejecting sloppy floats (`0.1` must be written `1/10`) with a message that teaches the fix. The island case proved the value of holding the line: no engine can type a variable exponent on a dimensional base, so the curator normalizes instead.


## Consequences

- Kleiber admitted (90 eligible); biology-3 ships kcal/day (thermochemical) and the fractional normalization unit.
- Manifests and kit vocabulary encode fractional powers as [num, den] pairs; whole powers serialize exactly as before (no readers needed changes).
- Island brief #4 requests a normalized-area r2 (`c * (A / A0) ** z`), which projects with no further engine work.
- Stage 2 shipped in 0.17.0: log/exp (natural, dimensionless-only), sqrt (halves dimensions), n-ary sum (uniform dims) and prod (adds dims), all forward-only with the solver profile unchanged.
- Kit curator instructions should gain the exponent-grammar and function-allowlist rules; unbounded/indexed summation (age classes, generations, k-out-of-N) stays deferred by design.
- Update 2026-11-01 (0.18.0): log10 added (pH-ready); index-family inputs shipped with forward-only solver treatment and digest-compatible serialization. Curation-schema support for family records (bundle variables, list references, integration projection) is the explicit follow-up before curators can submit family records.


## Revisit if

Curators need exponents with denominators beyond 1024, dimensional affine functions (temperature), or indexed/array summation — each reopens the grammar, not just the vocabulary.
