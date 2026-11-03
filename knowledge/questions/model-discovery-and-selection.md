---
id: question-model-discovery-and-selection
type: question
title: Model Discovery, Applicability, and Selection
summary: How do agents discover suitable models, verify applicability, choose among alternatives, and distinguish missing coverage from retrieval failure or unavailable inputs?
status: active
created: '2026-10-27'
updated: '2026-10-31'
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

## Observed planning failure — requested unknown treated as missing input

**Implementation update, 2026-10-31:** the bounded inverse-view facility and composer support below now resolve this reported case. The exact original question succeeded as run `fb880a63-2725-4bee-a4f1-69cf205b0dc0`, returning first discounted year-end crossing at year 5 by solving the stored present-value relationship over its declared integer domain. No payback-specific canonical model was created. The composer now receives candidate inverse views, distinguishes known values from requested unknowns, and records target bindings separately from factual inputs. General intent understanding is not thereby proven; tests and supported profile limits are in [[question-execution-runtime-for-heterogeneous-models]]. The following paragraphs preserve the original diagnosis, not an assertion that no solving capability still exists.

On 2026-10-31 the user reported run `446a7a14-64e8-4994-b085-b29ba44aea89`, asking when a heating investment would pay off given its cost, discount rate, annual heat, two performance values and tariff. Inspection confirms all six numeric facts were extracted with correct values/units and no parser issues. The composer nevertheless requested an evaluation horizon. It selected the needs of forward present-value evaluation rather than recognizing discounted payback as the desired output.

The eligible registry contains electricity use/cost, savings, uniform present value and net present value, but no discounted-payback model; the runtime evaluates forward scalar DAGs and has no registered inverse/threshold-search operation. These are two distinct problems: a coverage/operation gap and misclassification of that gap as missing user data. The prompt's prohibition on inventing horizons is appropriate for fixed-horizon evaluation, but does not distinguish an unspecified input from an explicitly requested unknown.

Required regression: distinguish “NPV after ten years” (horizon input, value output) from “when do discounted savings cover the investment?” (time output). Clarifications may address genuine ambiguities such as simple versus discounted payback, but must not ask the user to supply the solution. If the requested operation is unavailable, record unsupported model/operation coverage rather than `needs-input` for the requested unknown. This is an observed defect and design requirement, not an implemented fix or evidence that every other applicability condition is resolved.

Candidate remedies remain proposals: curate/review a dedicated payback model offline, or add a bounded runtime search over the existing forward graph with explicit no-crossing behavior. Both should follow an explicit separation of supplied facts, requested outputs/unknowns and operation intent before selecting a computation. No general solver or new model was implemented during this diagnosis.

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

A discovery request/result contract and adjudicated cases containing a suitable match, same-unit wrong-meaning candidate, out-of-domain candidate, competing valid models, and no eligible match. Record selection/rejection reasons and unresolved ambiguity. Choose retrieval technology only after these needs are clear. Include an adversarial binding case with two same-unit dimensionless quantities where the composer must pick by meaning (e.g. emissivity vs any other unit-1 value); meaning alignment is LLM-side only, backstopped by guards and inspectable assignments.

## Provenance

Extracted from the 2026-10-27 curation concept and build-readiness review. This concerns product model discovery, not the existing pmem retrieval tool.
