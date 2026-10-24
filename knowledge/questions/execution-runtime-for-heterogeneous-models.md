---
id: question-execution-runtime-for-heterogeneous-models
type: question
title: Execution Runtime for Heterogeneous Models
summary: How should Connected Models orchestrate and execute heterogeneous models spanning symbolic algebra, numerical ODEs/PDEs, scientific Python/R, and external black-box APIs?
status: active
created: '2026-10-24'
updated: '2026-10-24'
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
---

# Execution Runtime for Heterogeneous Models

## Question

What architecture and execution runtime should Connected Models adopt to evaluate composite graphs composed of heterogeneous, polyglot models (spanning symbolic algebra, continuous ODEs/PDEs, scientific Python/R scripts, proprietary binaries, and external real-time data feeds)?

## Why it matters

Real-world quantitative modeling is inherently polyglot and fragmented. A macro-economic model might be written in Julia, a hydrological climate simulation in Fortran or Python, an asset pricing formula in C++, and an accounting identity in basic algebra. Forcing all models into a single client-side or embedded language (as in the 2025 Math.js experiment) artificially restricts Connected Models to trivial arithmetic toys. 

To fulfill the [[concept-connected-models-thesis]], the runtime must safely orchestrate cross-model data passing across disparate execution environments.

## Current partial answer

- Standalone browser execution has been retired ([[decision-retire-standalone-mathjs-implementation]]).
- The runtime will likely require a distributed DAG scheduler with pluggable execution adapters (e.g., containerized execution workers, Wasm runtimes, and lightweight expression evaluators like Math.js or SymPy for closed-form formulas).
- Intermediate caching and execution plan compilation are strictly required to avoid recomputation overhead ([[finding-graph-compilation-caching-requirement]]).

## What would resolve it?

1. A clear breakdown of the fundamental questions regarding representation, ontology, and runtime mechanics.
2. An architectural prototype demonstrating an end-to-end composite graph execution spanning at least two distinct backends (e.g., a Python numerical simulation coupled to a symbolic algebraic model).
3. Clear criteria for handling latency, security sandboxing, and data serialization between model nodes.

## Legacy provenance

Identified in `Legacy/ProblemStatementInitialThoughts.md` ("Challenges: How would this run? each model needs its own platform, many if not most might need external input... Specialty hardware").
