---
id: concept-unified-computational-graph
type: concept
title: Unified Computational Graph (Prototype Model)
summary: A polymorphic graph abstraction where equations and composite models share a single schema. Pertained specifically to the 2025 Math.js prototype; provisional pending deeper research on representation and ontology.
status: provisional
created: '2026-10-24'
updated: '2026-10-24'
topics:
  - representation
  - computational-graphs
  - ontology
confidence: medium
relations:
  - type: relates-to
    target: concept-connected-models-thesis
  - type: relates-to
    target: decision-unify-equations-and-graphs
  - type: relates-to
    target: investigation-prototype-2025-mathjs-supabase
  - type: relates-to
    target: finding-graph-compilation-caching-requirement
---

# Unified Computational Graph (Prototype Model)

## Current understanding

The 2025 prototype introduced a unified graph abstraction where standalone equations and composite models share a single underlying entity schema (`computational_graph`). Standalone equations were treated as atomic graphs (`is_atomic: true`), while multi-step models were composite graphs containing equations or nested sub-graphs linked through variable binding records.

This concept is maintained as **provisional**. It pertained specifically to the 2025 Math.js and Supabase implementation, and should not be accepted as a universal architectural truth going forward until rigorous groundwork on representation, ontology, and execution semantics is completed.

## Key points

- **Polymorphic schema**: Single entity table where `is_atomic` distinguishes between a single equation node and a parent graph containing child nodes.
- **Hierarchical composition**: Composite graphs reference child components via a join table (`graph_component`), allowing arbitrary nesting (e.g., DuPont ROI model embedding Profit Margin and Asset Turnover graphs).
- **Explicit variable interface**: Variables are categorized by roles (`input`, `output`, `intermediate`), and edges bind output variables from preceding components to input variables of succeeding components.
- **Scope limitation**: Successfully supported discrete scalar algebraic expressions, but leaves continuous mathematical systems, differential equations, and dynamic state unaddressed.

## What changed recently

Reclassified from accepted to provisional. While the unified table design simplified the 2025 relational database prototype, future architectures may require distinct ontological representations for equations, pipelines, empirical datasets, and simulation containers.

## Uncertainties

- Can a single graph abstraction cleanly represent both deterministic closed-form equations and iterative/stochastic numerical simulations?
- How should higher-order units, dimensional compatibility, tensor shapes, and probability distributions be represented in the graph ontology?
- What representation best supports polyglot execution engines beyond relational database tables?

## Legacy provenance

Reconstructed from `Legacy/Simple mathJS implementation attempt [2025].md` and `Legacy/mathJSArchitectureStructureOverview.md` (migration `20250620024514_fierce_wave.sql`).
