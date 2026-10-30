---
id: decision-retire-standalone-mathjs-implementation
type: decision
title: Retire Standalone Math.js Architecture
summary: Retire the standalone Math.js browser/RPC stack as the primary calculation engine, while preserving Math.js as a potential sub-engine for scalar algebraic evaluation in a future multi-engine runtime.
status: accepted
created: '2026-10-24'
updated: '2026-10-28'
topics:
  - runtime
  - architecture
  - engines
confidence: high
relations:
  - type: relates-to
    target: investigation-prototype-2025-mathjs-supabase
  - type: addresses
    target: question-execution-runtime-for-heterogeneous-models
  - type: derived-from
    target: source-historical-mathjs-prototype-overview-2025
  - type: derived-from
    target: source-historical-mathjs-prototype-architecture
---

# Retire Standalone Math.js Architecture

## Decision

Retire the standalone Math.js browser/RPC architecture as the sole or primary calculation engine of Connected Models. Math.js will not serve as the universal execution platform, but may still be retained as one specialized evaluation engine within a future multi-engine runtime (specifically for fast, lightweight symbolic and scalar algebraic evaluation).

## Context

The 2025 prototype implemented model evaluation using Math.js (`evaluateExpression` and `calculateGraph`) inside a React frontend, coupled with Supabase PostgreSQL functions for topological sorting. While this proved sufficient for basic financial ratios (e.g., the DuPont ROI model), it proved incapable of supporting real-world quantitative modeling across scientific, macro-economic, and risk engineering domains.

## Alternatives considered

- **Retaining standalone Math.js as the sole platform**: Rejected as the universal architecture. The documented prototype did not supply the heterogeneous model, solver, environment, semantic and safety contracts needed across these domains. This is not proof that Math.js lacks matrices, derivatives, or that numerical methods cannot be programmed using its primitives.
- **Completely eliminating Math.js from future consideration**: Rejected. For basic arithmetic and scalar algebraic expressions, Math.js is fast, portable, and has zero heavy runtime dependencies. It remains a viable candidate sub-engine.
- **Polyglot multi-engine runtime**: Adopted as the strategic direction. A central graph orchestrator dispatches sub-graph execution to specialized backends (e.g., Python/SciPy, R, Julia, external APIs, and Math.js for simple algebra).

## Rationale

Connected Models aims to compose models spanning climate science, financial engineering, epidemiology, and prediction markets. These disciplines require declared numerical integration, statistical estimation, external data and environment interfaces, source/evidence semantics, and controlled execution. The old browser/RPC design did not supply those contracts; it should not be treated as a universal runtime merely because expressions can be evaluated.

**Evidence correction, 2026-10-28:** [[source-mathematical-model-representation-standards]] verifies Math.js matrix support and a symbolic derivative API. [[investigation-model-variable-quantity-representation]] distinguishes source language, expression backend, model semantics and execution profile. This qualifies older categorical capability claims; the accepted retirement of the old sole-engine architecture remains unchanged. A small first build can still use one suitable engine, and no new engine or distributed runtime is selected by this clarification.

## Consequences

- The 2025 standalone frontend architecture is permanently retired as the primary execution path.
- Resolving the execution runtime for heterogeneous models becomes a primary open engineering question ([[question-execution-runtime-for-heterogeneous-models]]).
- Preserves the ability to reuse Math.js as a lightweight scalar execution engine where appropriate.

## Revisit if

Never revisit as the *sole* standalone architecture. Revisit Math.js specifically when selecting and benchmarking sub-engines for scalar algebraic evaluation.

## Legacy provenance

Reconstructed from evaluation limits documented in [[source-historical-mathjs-prototype-overview-2025]] and [[source-historical-mathjs-prototype-architecture]].
