---
id: question-execution-runtime-for-heterogeneous-models
type: question
title: Execution Runtime for Heterogeneous Models
summary: How should Connected Models orchestrate and execute heterogeneous models spanning symbolic algebra, numerical ODEs/PDEs, scientific Python/R, and external black-box APIs?
status: active
created: '2026-10-24'
updated: '2026-10-31'
topics:
  - runtime
  - orchestration
  - execution
confidence: high
relations:
  - type: relates-to
    target: decision-retire-standalone-mathjs-implementation
  - type: relates-to
    target: finding-graph-compilation-caching-requirement
  - type: derived-from
    target: source-historical-problem-statement-and-initial-thoughts
---

# Execution Runtime for Heterogeneous Models

## Question

What architecture and execution runtime should Connected Models adopt to evaluate composite graphs composed of heterogeneous, polyglot models (spanning symbolic algebra, continuous ODEs/PDEs, scientific Python/R scripts, proprietary binaries, and external real-time data feeds)?

## Why it matters

Real-world quantitative modeling is inherently polyglot and fragmented. A macro-economic model might be written in Julia, a hydrological climate simulation in Fortran or Python, an asset pricing formula in C++, and an accounting identity in basic algebra. Forcing all models into a single client-side or embedded language (as in the 2025 Math.js experiment) artificially restricts Connected Models to trivial arithmetic toys. 

To fulfill the [[concept-connected-models-thesis]], the runtime must safely orchestrate cross-model data passing across disparate execution environments.

## Current partial answer

### Bounded inverse facility implemented — 2026-10-31

Runtime 0.2 adds per-instance solve views over pinned existing model revisions, keeping source identity/evidence/review intact. `solve_for` names one original input; known bindings are the other inputs plus `__output__`, which denotes the known original output or requested output target. `relation=equal` finds admissible roots; `at_least` finds the earliest integer period meeting an output threshold within explicit original-guard bounds. Compilation uses each view's actual input/result ports and validates source admission before either direction executes. No new model publication is authorized by a solve request.

Profile `rational-polynomial-degree-2-or-bounded-integer/1`: allowlisted AST arithmetic only; exact Fraction coefficients; final degree at most two; unknown-dependent integer powers of magnitude at most two; intermediate degree at most four and coefficient numerator/denominator bit length at most 4096. Real candidates are checked in the original expression with all original predicates, finite arithmetic, denominator/domain validity, unit conversion and integer-type checks. Equality residual uses absolute/relative tolerances 1e-9. Multiple roots are not arbitrarily collapsed; fixed literals cannot be inverted. A zero numerator is reported underdetermined rather than claiming a unique result. Finite integer domains are obtained from original comparison guards and capped at 1000 candidate points. Missing bounds and no crossing within bounds are distinct; no unbounded impossibility claim is made.

Fifty offline tests pass, covering original forward behavior, rational inversions, quadratic branches/repeated/non-real roots, extraneous denominator roots, underdetermination, unsupported degree/exponents, stable quadratic evaluation, inverse-to-forward edges, original identity preservation and bounded nonmonotone threshold search. Live runs: `fb880a63-2725-4bee-a4f1-69cf205b0dc0` resolves the user's original payoff question to first year-end crossing at 5 using the source model's 1–100 domain; `d25902f1-6fec-4ed9-ba2a-1299a86b6a8d` solves seasonal performance as 3; `4553f3a2-6f92-422f-88dd-4004b3349773` solves electricity consumption as 4000 kWh. No models were re-curated or duplicated. The payback run used the immediately preceding engine build (0.1 label with the same recorded solver profile); subsequent live inverse runs use runtime 0.2. The semantic version was bumped during the increment, not retroactively rewritten in evidence.

Inspection report `.runs/report-a27fdff2-952f-47db-8035-26f691bba2ec.html` shows solver method/domain, original model and target-value provenance. Algebraic inversion is not general scientific/causal invertibility. Continuous/fractional-time solving, arbitrary systems, statistical inverse inference, larger polynomials and unrestricted symbolic simplification remain outside this implementation. Broader runtime questions stay active.

- Standalone browser execution has been retired ([[decision-retire-standalone-mathjs-implementation]]).
- Pluggable execution adapters are a candidate extension boundary (e.g., isolated workers, WebAssembly, or lightweight expression evaluators). A distributed scheduler is a possible later solution, not an established prerequisite; a bounded first build may use one engine and local scheduling.
- Intermediate caching and execution plan compilation are strictly required to avoid recomputation overhead ([[finding-graph-compilation-caching-requirement]]).

## Minimum answer for the first build

**B — before implementing the compiler/executor** ([[question-build-readiness]]). Which first model classes and backends must execute, and which are explicitly unsupported? Define the adapter input/output/error contract, data transport, numeric precision, environment/dependency capture, randomness/seeds, and pre/postcondition enforcement. Model state and external reads/writes must not be hidden inside ostensibly pure reusable nodes.

Decide synchronous versus job-based runs; compilation boundaries and cache keys; cancellation/timeouts; retries and idempotency; failed/partial-run behavior; artifact/log capture; and result-versus-plan invalidation. A retry must not duplicate external side effects or return a different data version without recording it. Who schedules independent nodes, and what concurrency/resource limits apply?

Security/isolation belongs to [[question-execution-security-and-access]], pinned version/data references to [[question-registry-storage-and-versioning]], topology to [[question-graph-topology-and-feedback-cycles]], and stack/host feasibility to [[question-technology-stack-and-meta-access]]. Specify a minimal runnable contract now, not every polyglot adapter. A two-backend prototype would inform the broader question but is not mandatory unless the selected first workflow needs it.

## What would resolve it?

1. A clear breakdown of the fundamental questions regarding representation, ontology, and runtime mechanics.
2. An architectural prototype demonstrating an end-to-end composite graph execution spanning at least two distinct backends (e.g., a Python numerical simulation coupled to a symbolic algebraic model).
3. Clear criteria for handling latency, security sandboxing, and data serialization between model nodes.

## Legacy provenance

Identified in [[source-historical-problem-statement-and-initial-thoughts]] ("Challenges: How would this run? each model needs its own platform, many if not most might need external input... Specialty hardware").
