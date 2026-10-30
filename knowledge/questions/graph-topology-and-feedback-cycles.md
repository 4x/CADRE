---
id: question-graph-topology-and-feedback-cycles
type: question
title: Graph Topology and Feedback Cycle Resolution
summary: Should Connected Models permit cyclic dependency graphs (feedback loops and market equilibria), and what mathematical resolution mechanics should govern them?
status: active
created: '2026-10-24'
updated: '2026-10-28'
topics:
  - representation
  - graph-algorithms
  - runtime
confidence: high
relations:
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: finding-graph-compilation-caching-requirement
  - type: relates-to
    target: question-execution-runtime-for-heterogeneous-models
  - type: relates-to
    target: investigation-model-variable-quantity-representation
---

# Graph Topology and Feedback Cycle Resolution

## Question

Should Connected Models restrict computational graphs strictly to Directed Acyclic Graphs (DAGs), or support cyclic dependencies (feedback loops, simultaneous equilibria, and system dynamics), and what compilation and execution algorithms must govern cyclic resolution?

## Why it matters

Many real-world quantitative systems are inherently cyclic:
- **Economics & Markets**: Supply and demand simultaneously determine price, which in turn influences supply and demand (market-clearing equilibrium).
- **Climate & Earth Systems**: Temperature increases melt polar ice, lowering planetary albedo, which increases solar absorption and further accelerates warming (positive feedback loop).
- **Corporate Finance**: Interest expense reduces net income, which reduces retained earnings, which affects borrowing capacity and future debt issuance (circular debt-service loop in three-statement financial models).

If Connected Models enforces a strict DAG architecture, modelers cannot express these coupled dynamics without manually decoupling them or embedding complex iterative solvers inside single opaque monolithic nodes. However, allowing cycles complicates the compilation phase: naive topological sorting fails, and execution risks infinite recursion, numerical instability, or divergent oscillations.

## Current partial answer

- **Strict DAG Architecture**:
  - *Advantages*: Linear topological sort, simpler scheduling/caching, and straightforward dependency invalidation (`[[finding-graph-compilation-caching-requirement]]`). A finite DAG prevents graph-traversal cycles; it does not guarantee that node code or external calls terminate.
  - *Disadvantages*: Cannot natively represent system dynamics or simultaneous equilibria.
- **Cycle Resolution Strategies**:
  1. **Discrete Temporal Unrolling ($t \to t+\Delta t$)**: Loops are broken by enforcing an explicit temporal lag operator ($z^{-1}$ delay). Feedback affects the *next* time step, converting a cyclic continuous graph into an unrolled acyclic chain over time.
  2. **Compile-Time Symbolic Reduction**: For closed-form algebraic loops, a computer algebra system (CAS) symbolically solves the simultaneous system at compile time, eliminating the cycle before execution.
  3. **Runtime Fixed-Point / Relaxation Solvers**: The runtime identifies strongly connected components (SCCs via Tarjan's algorithm) and wraps them in iterative numerical solvers (e.g., Newton-Raphson or Picard iteration) with declared convergence criteria and maximum iteration bounds.

## Representation investigation — 2026-10-28

[[investigation-model-variable-quantity-representation]] distinguishes a mathematical relation/incidence structure, component composition, and the compiled dependency schedule. Modelica's unordered equations, CellML/SBML state/events and statistical/optimization constructs demonstrate why a universal pure-function DAG loses meaning. A source equation system can later be causalized/solved under explicit assumptions; that transformation is not ordinary output-port wiring or a proof of unique solution.

Recommend a first acyclic **execution profile** for supported explicit algebra, while richer declared formalisms can remain catalog-only. Do not ban all non-DAG mathematics from the repository simply because the first executor cannot run it. No solver or causalization trial was performed; dynamic/implicit adapters, convergence rules, and cycle handling remain open.

## Minimum answer for the first build

**B — before graph compilation** ([[question-build-readiness]]). Decide whether the first representation/executor permits cycles, time-delayed feedback only, or no cycles. Define cycle detection, shared/nested dependency identity, diagnostics, and unsupported-topology behavior. This can be a scoped restriction without settling the eventual universal representation.

If cycles are supported now, distinguish an algebraic equilibrium from temporal dynamics, and specify solver/state semantics, initialization, convergence/residual tolerances, iteration/time limits, multiple solutions, non-convergence, and uncertainty limitations. A generic fixed-point loop is not a justified solver for every coupled model. If cycles are excluded, do not silently break one with an invented delay or Meta estimate.

Runtime safety/time limits remain required even for a DAG ([[question-execution-security-and-access]]). Compilation scheduling belongs to [[question-execution-runtime-for-heterogeneous-models]].

## What would resolve it?

1. Deciding whether the foundational specification permits cycles in the core graph representation, or if Phase 1 restricts graphs to DAGs with time-delay unrolling.
2. If cyclic loops are permitted, defining the syntax for loop convergence tolerances, failure handling on non-convergence, and how uncertainty propagates through recursive iterations.

## Linked context

- `[[concept-end-state-vision]]`: The computational OS must manage execution dependencies robustly.
- `[[finding-graph-compilation-caching-requirement]]`: Topological compilation and invalidation depend fundamentally on graph topology.
- `[[question-execution-runtime-for-heterogeneous-models]]`: Runtime schedulers must know how to execute coupled loops.
