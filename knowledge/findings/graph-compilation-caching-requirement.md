---
id: finding-graph-compilation-caching-requirement
type: finding
title: Computational Graphs Require Explicit Compilation and Invalidation
summary: Hierarchical computational graphs require pre-compiled execution plans (topological sort, input mapping) and timestamp-based dirty tracking to prevent exponential traversal overhead during execution.
status: accepted
created: '2026-10-24'
updated: '2026-10-24'
topics:
  - performance
  - compilation
  - graph-algorithms
confidence: high
relations:
  - type: derived-from
    target: investigation-prototype-2025-mathjs-supabase
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: question-execution-runtime-for-heterogeneous-models
---

# Computational Graphs Require Explicit Compilation and Invalidation

## Finding

Hierarchical computational graphs cannot be efficiently evaluated via naive runtime recursive traversal. They strictly require a dedicated **compilation phase** that topologically sorts component dependencies, identifies the precise external input boundary, and serializes a flat execution plan. Furthermore, graphs require explicit timestamp-based dirty tracking (`compiled_at` versus `updated_at`) to trigger invalidation across parent dependency chains when child components change.

## Basis

During the 2025 prototype development ([[investigation-prototype-2025-mathjs-supabase]]), on-the-fly recursive graph traversal in client components (`GraphCalculator.tsx`) caused severe execution bottlenecks and input-mapping synchronization bugs in nested multi-step models (such as the DuPont model).

The introduction of PostgreSQL migration `20250620024514_fierce_wave.sql` added:
- `compiled_graph`: A serialized JSON execution plan containing the topologically sorted sequence of atomic steps and nested sub-graphs.
- `compile_graph(graph_id)` / `rpc_compile_graph`: Stored procedures performing graph traversal and input/output binding at save-time.
- `auto_compile_parent_graphs`: Trigger functions that automatically flagged and recompiled parent models whenever a child equation or sub-graph was modified.
- `checkGraphCompilation`: Pre-run validation ensuring the graph was current before execution.

This reduced graph evaluation from an unpredictable recursive search to a deterministic linear step execution.

## Implications

- The lifecycle of a connected model must strictly decouple **definition** (authoring nodes and connections), **compilation** (type checking, topological ordering, boundary analysis), and **execution** (passing concrete input vectors to obtain outputs).
- Any future heterogeneous runtime ([[question-execution-runtime-for-heterogeneous-models]]) must include an execution plan compiler and automated cache invalidation engine.

## Limitations / uncertainty

- The 2025 mechanism relied on relational database foreign keys and PostgreSQL triggers. Managing compilation caching and invalidation across distributed, federated, or external API model nodes will be significantly more complex.

## Legacy provenance

Reconstructed from architectural mechanisms documented in `Legacy/mathJSArchitectureStructureOverview.md` (database functions `compile_graph`, `auto_compile_parent_graphs`, and component `RunGraphModal.tsx`).
