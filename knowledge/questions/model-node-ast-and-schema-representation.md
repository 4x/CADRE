---
id: question-model-node-ast-and-schema-representation
type: question
title: Model Node AST and Schema Representation
summary: What unified schema or AST representation can formally express discrete equations, continuous ODEs/PDEs, stochastic processes, and black-box oracles?
status: active
created: '2026-10-24'
updated: '2026-10-24'
topics:
  - representation
  - architecture
confidence: high
relations:
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: question-execution-runtime-for-heterogeneous-models
---

# Model Node AST and Schema Representation

## Question

What formal Abstract Syntax Tree (AST) or declarative schema can comprehensively represent the full spectrum of quantitative models—spanning closed-form scalar algebra, implicit equations, continuous differential systems (ODEs/PDEs), stochastic processes, and black-box proprietary oracles—without sacrificing mathematical expressiveness or execution performance?

## Why it matters

The 2025 prototype relied on storing formulas as raw strings (`expression_latex` and `expression_code`) parsed at runtime by Math.js (`Legacy/mathJSArchitectureStructureOverview.md`). While functional for scalar arithmetic (e.g., the DuPont ROI model), string-based parsing cannot support:
- Continuous differential equations requiring initial/boundary conditions and numerical integration schemes.
- Implicit systems requiring numerical root-finding or iterative solvers.
- Gradient and automatic differentiation extraction for sensitivity analysis.
- Safe serialization and sandboxing across polyglot execution engines.

Without a rigorous representation schema, graph compilers cannot perform semantic validation, dependency optimization, or multi-engine code generation.

## Current partial answer

- Existing open standards offer domain-specific precedents:
  - **MathML / OpenMath**: Highly expressive for mathematical semantics, but historically heavy and detached from software runtime execution.
  - **CellML & SBML**: Well-tested standards in systems biology for coupled differential equations and biochemical networks.
  - **Symbolic ASTs (e.g. SymPy / CAS S-expressions)**: Strong for analytical manipulation, symbolic simplification, and exact differentiation.
  - **Declarative Node Envelopes (Protobuf / JSON-Schema)**: Excellent for interface boundaries, variable typing, and network transport.
- The likely path forward is a **two-tier representation**:
  1. An outer **Declarative Interface Envelope** that standardizes variable roles, assumptions, citations, transparency badging, and boundary contracts across all nodes.
  2. A polymorphic **Execution Payload** that supports engine-specific representations (e.g., symbolic AST for algebra, state-space vector fields for ODEs, or container/API endpoint descriptors for black-box oracles).

## What would resolve it?

1. Benchmarking candidate AST schemas against the three exemplar models from our legacy materials: the algebraic DuPont model, the Intrinsic Valuation network, and a continuous physical model.
2. Determining whether the internal AST should be language-agnostic (e.g. custom JSON/Protobuf AST) or leverage an existing scientific intermediate representation.

## Linked context

- `[[concept-end-state-vision]]`: Mandates the multi-tier cascade uniting algebraic, continuous, and discrete models.
- `[[concept-unified-computational-graph]]`: Identifies the limits of the initial flat relational schema.
- `[[question-execution-runtime-for-heterogeneous-models]]`: Runtime orchestration depends directly on the chosen node representation.
