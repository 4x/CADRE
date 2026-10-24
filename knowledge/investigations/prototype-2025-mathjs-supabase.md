---
id: investigation-prototype-2025-mathjs-supabase
type: investigation
title: 2025 Math.js and Supabase Prototype Retrospective
summary: Retrospective investigation of the 2025 React/Supabase/Math.js prototype, evaluating what worked (DuPont composition, unified graph schema) and its expressiveness limits.
status: completed
created: '2026-10-24'
updated: '2026-10-24'
topics:
  - prototype
  - architecture
  - database
  - retrospective
confidence: high
relations:
  - type: relates-to
    target: decision-unify-equations-and-graphs
  - type: relates-to
    target: decision-retire-standalone-mathjs-implementation
  - type: produces
    target: finding-graph-compilation-caching-requirement
---

# 2025 Math.js and Supabase Prototype Retrospective

## Question / scope

Evaluate the technical achievements, architectural lessons, and functional limitations of the 2025 prototype web application (built with React, TypeScript, Vite, Tailwind CSS, KaTeX, Math.js, and Supabase PostgreSQL).

## What we already knew

Prior to 2025, Connected Models existed only as a high-level pitch and set of conceptual slide decks dating to 2020 (`Legacy/Slides2020.md`). No running software or formal data model had been created.

## Work performed

- Constructed a full-stack web application featuring user authentication, equation authoring with LaTeX and code expressions, interactive graph builders, and mathematical rendering.
- Implemented database migrations unifying equations and composite graphs under a single schema (`computational_graph` and `graph_component` via migration `20250620024514_fierce_wave.sql`).
- Developed server-side stored procedures for topological graph compilation (`compile_graph`, `rpc_compile_graph`, and `auto_compile_parent_graphs`).
- Built and successfully evaluated a multi-tier demonstration model: the **DuPont Return on Investment (ROI)** model, composed of nested sub-graphs for *Profit Margin* (EBIT and PM) and *Asset Turnover* (Current Assets, Fixed Assets, and Asset Turnover).

## Analysis

### What worked
1. **Hierarchical Graph Composition**: Proved that complex calculations can be cleanly decomposed into reusable, modular sub-models.
2. **Dynamic Input Resolution**: The system correctly identified external user inputs by subtracting internal component connections from the aggregate input set.
3. **LaTeX / Code Dual Representation**: Allowing users to view equations in KaTeX while evaluating them via executable code strings provided a strong mental model for mathematical tools.

### What failed / bottlenecks
1. **Math.js Expressiveness Ceiling**: Restricted strictly to basic algebraic evaluation. Could not express differential equations, numerical optimization, stochastic simulations (Monte Carlo), or matrix operations.
2. **Client-Centric Execution Bottlenecks**: Performing evaluation in the browser while maintaining compilation states in PostgreSQL created synchronization complexity and prevented server-side agentic automation.
3. **Premature Social Feature Surface**: Sizable engineering hours were spent on user profiles, starring, voting, and comment tables before the core computational and ontological mechanics were proven.

## Conclusions

- The prototype verified the core user thesis that models can be decomposed and chained into higher-order decision graphs.
- The standalone Math.js architecture must be retired as the primary execution engine ([[decision-retire-standalone-mathjs-implementation]]), but Math.js may be preserved as a lightweight scalar evaluation plugin.
- Development must shift from consumer social web UI toward deep foundational research on representation, ontology, and polyglot runtimes.

## New questions

- What execution runtime can orchestrate heterogeneous models across different languages and platforms ([[question-execution-runtime-for-heterogeneous-models]])?
- What representation and ontology will provide true semantic interoperability across domains?

## Legacy provenance

Reconstructed from `Legacy/Simple mathJS implementation attempt [2025].md` and `Legacy/mathJSArchitectureStructureOverview.md`.
