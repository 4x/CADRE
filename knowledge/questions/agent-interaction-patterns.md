---
id: question-agent-interaction-patterns
type: question
title: Agent Interaction Patterns with Model Graphs
summary: What tools, state transitions, orchestration, and authority should agents use to discover, compose, execute, curate, and maintain connected models?
status: active
created: '2026-10-24'
updated: '2026-10-28'
topics:
  - agents
  - interfaces
  - protocols
confidence: medium
relations:
  - type: relates-to
    target: concept-agent-quantitative-reasoning-layer
  - type: relates-to
    target: hypothesis-graph-grounded-agent-reliability
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: derived-from
    target: source-historical-problem-statement-and-initial-thoughts
---

# Agent Interaction Patterns with Model Graphs

## Question

How should autonomous agents discover, query, compose, and execute connected model graphs? What interaction protocols, data serialization formats, and division of labor should govern parallel agents operating across the graph?

## Why it matters

The 2026 legacy notes identify autonomous AI agents as a primary user class ([[concept-agent-quantitative-reasoning-layer]]). While human users interact through visual diagram builders and forms, agents require machine-friendly, high-density, deterministic protocols. If agents cannot efficiently navigate the model repository, discover matching inputs/outputs, or parse execution errors, the envisioned performance gains ("saving turns, time, and tokens") will be lost to orchestration friction.

## Current partial answer

Parallel agent workflows suggest specialized role divisions:
- **Retrieval / Discovery Agent**: Searches the model repository for equations or sub-graphs matching a natural-language query or quantitative goal.
- **Data Ingestion Agent**: Gathers real-world empirical parameters from external sources (e.g., Treasury rates, company filings, sensor readings) and maps them to model variable symbols.
- **Composition & Validation Agent**: Chains sub-graphs together, verifying unit compatibility and dimensional consistency.
- **Execution & Interpretation Agent**: Invokes the execution runtime, runs sensitivity analyses, and translates numeric results into decision-oriented narratives.

The user expanded this scope on 2026-10-27: agents should **curate and maintain the model collection**, not merely retrieve from it. [[concept-specialized-model-curation-agents]] develops proposed coverage, scouting, formalization, connection, reproduction/challenge, and maintenance responsibilities, specialized by domain. These are responsibilities, not a requirement to run a separate process for every role.

User clarification, 2026-10-28: a dedicated agent or fleet performs curation primarily or exclusively **offline**, outside individual answer requests. It ingests papers/textbooks and other sources, canonicalizes models, extracts equations, variables, constants, parameters, and provenance, and stores qualified versions in the repository. Query-time agents retrieve, select, compose, and execute existing models. A query-discovered gap may inform a separate curation job, not routine inline curation. Whether inline curation is entirely forbidden or allowed only as an explicit last resort remains open; "offline" does not mean no internet access.

Query-time resolution should search appropriate upstream models before using an explicitly labeled Meta-generated gap-filler ([[concept-connected-models-thesis]]). Repeated gaps should inform curation; a temporary estimate must not silently become a trusted shared model.

Unresolved protocol questions now include publication/review authority, version ownership, duplicate and conflicting proposals, evidence independence, sensitive-data boundaries, recursive search budgets, and how agent-generated contributions remain visible to downstream consumers. The direction is endorsed; these mechanisms are not settled.

## Minimum answer for the first build

**B — before implementing agent tools and orchestration** ([[question-build-readiness]]). Select the smallest role split required by the workflow: separate responsibilities do not require parallel processes, distinct models, or a multi-agent framework. What structured tool contracts cover offline source discovery, candidate creation, review/publication, and separately query-time repository retrieval, binding, validation, execution, and inspection? Which actions may an agent propose versus perform? Query-time tools must not silently cross into source-model curation/publication. Any future last-resort exception needs explicit policy and authority; it is not a default tool path.

Define persisted workflow states, tool-result/error schemas, schema-validation retries, idempotent writes, checkpoints, cancellation, budgets, authority, and human handoffs. How are duplicate/concurrent proposals handled, and how does a resumed run know which model/data versions it used? Tool outputs and retrieved sources must not override permissions.

This record owns agent protocol and orchestration, not all scientific or product policy. Dedicated questions now own [[question-model-discovery-and-selection]], [[question-assumption-resolution-and-fallback-policy]], [[question-curation-evidence-and-approval]], [[question-registry-storage-and-versioning]], and [[question-execution-security-and-access]]. Verify actual Meta API/tool behavior through [[question-technology-stack-and-meta-access]]. An inspectable sequential trace can answer the initial protocol needs while universal parallel-agent design remains open.

## What would resolve it?

1. Prototyping an end-to-end agent interaction trace on a concrete benchmark problem (e.g. intrinsic valuation).
2. Defining the schema for model discovery, parameter binding, and result return.
3. Quantifying the reduction in agent tokens and latency compared to native chain-of-thought calculation.
4. Following one sourced model through offline canonicalization, variable/constant extraction, checks, review, and versioned repository publication; following an unsuitable candidate through rejection. A later query must consume the stored version without repeating curation.
5. Following a temporary Meta fallback through explicit disclosure, coverage-gap tracking, and eventual replacement without altering the lineage of an earlier answer.

## Legacy provenance

Reconstructed from [[source-historical-problem-statement-and-initial-thoughts]] ("What would different agents be doing [as they work in parallel]?").
