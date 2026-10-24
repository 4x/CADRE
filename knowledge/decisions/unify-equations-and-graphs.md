---
id: decision-unify-equations-and-graphs
type: decision
title: Unify Equations and Graphs (Prototype Schema)
summary: Schema decision from the 2025 prototype to unify equations and models into a single table. Adopted for the prototype, but kept provisional for future architecture pending ontology groundwork.
status: provisional
created: '2026-10-24'
updated: '2026-10-24'
topics:
  - schema
  - database
  - representation
confidence: medium
relations:
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: investigation-prototype-2025-mathjs-supabase
---

# Unify Equations and Graphs (Prototype Schema)

## Decision

In the 2025 prototype implementation, the separate `equation` database table was deprecated and merged into the `computational_graph` table. Standalone equations became atomic graphs (`is_atomic: true`) and composite models became parent graphs linking child components through a polymorphic `graph_component` table.

This decision is documented as **provisional**. It resolved concrete schema redundancy in the 2025 Math.js prototype, but is not accepted as a permanent universal architectural choice for future iterations.

## Context

The initial 2025 prototype architecture maintained two parallel data models: `equation` for mathematical formulas and `computational_graph` for interconnected models. This created severe operational friction:
- Duplicate code and relational tables for variables, units, comments, citations, and user starring.
- Inability to nest composite models cleanly within other composite models.
- Migration `20250620024514_fierce_wave.sql` resolved this by unifying them into a single polymorphic entity.

## Alternatives considered

- **Strict relational separation**: Maintaining distinct `equation` and `workflow` entities. (Rejected in 2025 due to duplicated metadata and awkward nesting).
- **Pure document/JSON store**: Storing entire model graphs as unstructured JSON blobs. (Rejected in 2025 to retain PostgreSQL relational integrity and Row Level Security).
- **Formal semantic ontology**: Defining formal types for mathematical equations, simulation models, and data pipelines. (Deferred pending deeper foundational groundwork).

## Rationale

Unification allowed recursive composition (graphs containing graphs) and provided a consistent API surface for the 2025 React frontend and Supabase RPC functions.

## Consequences

- Successfully enabled the hierarchical DuPont ROI demonstration model ([[investigation-prototype-2025-mathjs-supabase]]).
- Kept provisional because a single flat database schema may not scale to heterogeneous models spanning differential equations, stochastic simulations, or distributed external runtimes.

## Revisit if

Comprehensive groundwork on mathematical representation and ontology demonstrates that atomic formulas, simulation environments, and data pipelines have fundamentally incompatible operational semantics.

## Legacy provenance

Reconstructed from `Legacy/mathJSArchitectureStructureOverview.md` (migration `20250620024514_fierce_wave.sql`) and `Legacy/Simple mathJS implementation attempt [2025].md`.
