---
id: question-assumption-resolution-and-fallback-policy
type: question
title: Assumption Resolution, Stopping Rules, and Meta Fallbacks
summary: When should recursive model-first resolution stop, what may Meta fill in, how are generated dependencies disclosed, and when must the system return conditional or unresolved answers?
status: active
created: '2026-10-27'
updated: '2026-10-28'
topics:
  - agents
  - epistemology
  - reliability
confidence: null
relations:
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: concept-connected-models-thesis
  - type: relates-to
    target: question-model-discovery-and-selection
  - type: relates-to
    target: question-uncertainty-and-epistemic-bounds-serialization
  - type: relates-to
    target: question-graph-topology-and-feedback-cycles
  - type: relates-to
    target: question-curation-evidence-and-approval
---

# Assumption Resolution, Stopping Rules, and Meta Fallbacks

## Question

How do we operationalize the accepted principle of replacing missing assumptions with suitable models first, and otherwise using clearly disclosed Meta contributions, without unbounded recursion or false certainty?

## Decisions to answer

- How is a dependency classified: observation, model-derived projection, calibration, structural assumption, initial/boundary condition, user preference, or hypothetical intervention? What may the system infer versus preserve as a deliberate choice?
- What order governs existing-registry lookup, empirical input retrieval, upstream composition, and permitted Meta fallback? Can a direct observation satisfy a quantity without an unnecessary predictive model? New source-model curation normally belongs to a separate offline process, not this resolution path.
- What constitutes sufficient search before saying a suitable model is unavailable? How do depth, latency, monetary cost, and expected decision impact limit expansion? Who can change these budgets?
- How are revisited dependencies, shared evidence, and cycles detected? When can the system stop at a reviewed boundary rather than exposing every assumption recursively?
- What may Meta fill: a parameter, proxy, distribution, transformation, or entire submodel? Which types require user/reviewer approval before execution, and how does the rule vary with consequence and evidence? How do we distinguish provisional input estimation from new model creation, so fallbacks cannot circumvent the on-the-fly curation restriction?
- What is the required disclosure in the graph, tool response, and final answer: generated contribution, author/model version, reason, source support or absence, time/scope, calibration limits, and affected results? How is unknown uncertainty represented without invented numerical bounds?
- When does the system answer conditionally, present alternatives, request a private measurement/preference, or leave a dependency unresolved instead of fabricating a fact?
- What happens when a fallback materially changes a conclusion? How are scenario sensitivity and actual probabilistic confidence distinguished? How does a recurring gap trigger curation, and what happens to old results when a reviewed replacement becomes available?

## Current partial answer

The principle is accepted in [[concept-connected-models-thesis]]; stopping/approval rules are not. User clarification on 2026-10-28 establishes dedicated offline curation as the primary or exclusive model-building process. Queries consume existing curated versions and can expose gaps for later curation. Routine inline curation is excluded; whether to ban it entirely or allow only explicit last-resort exceptions remains unresolved. Recommend no inline curation in the first build. The earlier fallback proposal must be read within this boundary, not as permission to create models routinely during answering. Meta-generated does not mean forbidden, and executable does not mean empirically validated. This policy should enable useful provisional answers with explicit limits, not quietly turn the project into a calculator requiring users to supply every difficult input.

## Build gate and dependencies

**B — before recursive composition or gap-filling is presented as a supported workflow.** Discovery owns candidate/no-match evidence; this record owns what happens next. Epistemic representation belongs to [[question-uncertainty-and-epistemic-bounds-serialization]]; durable qualification of generated models belongs to [[question-curation-evidence-and-approval]].

## What would resolve it?

A resolution state/transition table with budgets and authority plus traces for a successful upstream binding, budget exhaustion, a disclosed provisional fallback, a recursive/cyclic dependency, a protected private input, and an irreducibly unknown quantity. Every trace must end in a computable, conditional, or explicitly unresolved result with retained provenance.

## Provenance

Turns the user's 2026-10-27 model-first and explicit Meta-gap-filling principle into an unanswered operational-policy question rather than reopening the principle itself.
