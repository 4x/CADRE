---
id: decision-retire-standalone-mathjs-implementation
type: decision
title: Retire Standalone Math.js Architecture
summary: Retire the standalone Math.js browser/RPC stack as the primary calculation engine, while preserving Math.js as a potential sub-engine for scalar algebraic evaluation in a future multi-engine runtime.
status: accepted
created: '2026-10-24'
updated: '2026-10-24'
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
---

# Retire Standalone Math.js Architecture

## Decision

Retire the standalone Math.js browser/RPC architecture as the sole or primary calculation engine of Connected Models. Math.js will not serve as the universal execution platform, but may still be retained as one specialized evaluation engine within a future multi-engine runtime (specifically for fast, lightweight symbolic and scalar algebraic evaluation).

## Context

The 2025 prototype implemented model evaluation using Math.js (`evaluateExpression` and `calculateGraph`) inside a React frontend, coupled with Supabase PostgreSQL functions for topological sorting. While this proved sufficient for basic financial ratios (e.g., the DuPont ROI model), it proved incapable of supporting real-world quantitative modeling across scientific, macro-economic, and risk engineering domains.

## Alternatives considered

- **Retaining standalone Math.js as the sole platform**: Rejected. Cannot evaluate ordinary differential equations (ODEs), stochastic processes (Monte Carlo), heavy matrix optimizations, or Python-native machine learning models.
- **Completely eliminating Math.js from future consideration**: Rejected. For basic arithmetic and scalar algebraic expressions, Math.js is fast, portable, and has zero heavy runtime dependencies. It remains a viable candidate sub-engine.
- **Polyglot multi-engine runtime**: Adopted as the strategic direction. A central graph orchestrator dispatches sub-graph execution to specialized backends (e.g., Python/SciPy, R, Julia, external APIs, and Math.js for simple algebra).

## Rationale

Connected Models aims to compose models spanning climate science, financial engineering, epidemiology, and prediction markets. These disciplines require numerical integration, statistical estimation, and external data ingestion that cannot execute inside a browser Math.js sandbox.

## Consequences

- The 2025 standalone frontend architecture is permanently retired as the primary execution path.
- Resolving the execution runtime for heterogeneous models becomes a primary open engineering question ([[question-execution-runtime-for-heterogeneous-models]]).
- Preserves the ability to reuse Math.js as a lightweight scalar execution engine where appropriate.

## Revisit if

Never revisit as the *sole* standalone architecture. Revisit Math.js specifically when selecting and benchmarking sub-engines for scalar algebraic evaluation.

## Legacy provenance

Reconstructed from evaluation limits documented in `Legacy/Simple mathJS implementation attempt [2025].md` and `Legacy/mathJSArchitectureStructureOverview.md`.
