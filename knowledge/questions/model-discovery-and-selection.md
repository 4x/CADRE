---
id: question-model-discovery-and-selection
type: question
title: Model Discovery, Applicability, and Selection
summary: How do agents discover suitable models, verify applicability, choose among alternatives, and distinguish missing coverage from retrieval failure or unavailable inputs?
status: active
created: '2026-10-27'
updated: '2026-10-27'
topics:
  - agents
  - ontology
  - reliability
confidence: null
relations:
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: relates-to
    target: question-semantic-variable-disambiguation
  - type: relates-to
    target: question-assumption-resolution-and-fallback-policy
  - type: relates-to
    target: question-curation-evidence-and-approval
---

# Model Discovery, Applicability, and Selection

## Question

How does an agent turn a requested quantity or decision into a defensible choice of model or subgraph, rather than the most similar-looking search result?

## Decisions to answer

- What is the searchable unit: model, version, output variable, input contract, or reusable subgraph? What must a discovery request declare about target, available inputs, place/time, intended operation, evidence policy, and cost?
- Which retrieval methods are sufficient initially: structured filtering, text search, graph traversal, semantic retrieval, or a bounded combination? What distinguishes candidate generation from actual compatibility/eligibility validation?
- How is applicability checked against calibrated population, scope, forecast horizon, regimes, preconditions, available data, and predictive versus causal intent? Who can approve an adaptation or semantic mapping?
- How are quality, suitability, freshness, openness, cost, and uncertainty compared without reducing them to an unsupported universal truth score?
- When must alternatives or incompatible explanations remain visible? When is model averaging justified, and how are shared assumptions, evidence, and correlated error recognized?
- What is recorded when a search finds nothing: true missing coverage, retrieval-budget exhaustion, access/licensing restriction, insufficient inputs, or a rejected mismatch? What evidence is sufficient to justify moving to Meta gap-filling?
- Can the system explain why one candidate was selected and another rejected, and surface the resulting coverage gap to curators?

## Current partial answer

The desired behavior is suitable-model-first, not keyword-first or guess-first. A small curated collection may not require vector search or a specialized search service. The collection is not complete, and neither an empty search nor an agent's confidence proves no relevant model exists. No retrieval technology or ranking policy is chosen.

## Build gate and dependencies

**B — before autonomous candidate binding.** A bounded first-build selection procedure can be explicit/manual, but the path must not present similarity as validation. Meaning/type checks belong to [[question-semantic-variable-disambiguation]]; eligibility to [[question-curation-evidence-and-approval]]; stopping/fallback behavior to [[question-assumption-resolution-and-fallback-policy]].

## What would resolve it?

A discovery request/result contract and adjudicated cases containing a suitable match, same-unit wrong-meaning candidate, out-of-domain candidate, competing valid models, and no eligible match. Record selection/rejection reasons and unresolved ambiguity. Choose retrieval technology only after these needs are clear.

## Provenance

Extracted from the 2026-10-27 curation concept and build-readiness review. This concerns product model discovery, not the existing pmem retrieval tool.
