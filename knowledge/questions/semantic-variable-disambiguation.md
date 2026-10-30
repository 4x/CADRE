---
id: question-semantic-variable-disambiguation
type: question
title: Semantic Variable Disambiguation and Ontology
summary: How can the ontology prevent "type-safe nonsense" across identical units (e.g., trailing GAAP revenue vs forward ARR) without requiring centralized manual curation for every edge?
status: active
created: '2026-10-24'
updated: '2026-10-28'
topics:
  - ontology
  - semantics
confidence: high
relations:
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: hypothesis-global-variable-namespace-compatibility
  - type: relates-to
    target: question-dimensional-and-unit-type-system
  - type: relates-to
    target: investigation-model-variable-quantity-representation
---

# Semantic Variable Disambiguation and Ontology

## Question

How can Connected Models formally represent the semantic meaning, temporal scope, accounting convention, and boundary conditions of variables to prevent "type-safe nonsense"—where variables match dimensionally (e.g., both are in $USD$ or $\%$), but represent fundamentally incompatible domain concepts?

## Why it matters

Dimensional and unit typing ([[question-dimensional-and-unit-type-system]]) ensure that we do not add meters to dollars. However, in real-world modeling, the most dangerous errors occur when units *do* match, but the underlying concepts conflict:
- **Financial modeling**: Binding *Trailing 12-Month GAAP Accounting Revenue* to an input expecting *Forward Projected Annual Recurring Revenue (ARR)*, or confusing *EBIT* with *EBITDA* or *Operating Cash Flow*.
- **Macroeconomics**: Binding *Headline Consumer Price Index (CPI)* into a model calibrated specifically for *Core Personal Consumption Expenditures (PCE)* or *5-Year Breakeven Inflation Expectations*.
- **Earth sciences**: Binding *Gross precipitation* into a model expecting *Effective soil infiltration precipitation*.

If autonomous AI agents or analysts bind model inputs based solely on unit compatibility and keyword matching, the resulting graph will execute without error and produce mathematically pristine, utterly fictitious results.

## Current partial answer

- **Established domain ontologies and vocabularies:** can supply reusable definitions and mappings, with coverage, governance, granularity, and integration costs to evaluate. The earlier blanket characterization of FIBO/SNOMED/Cyc as brittle universal taxonomies was not adequately supported and is withdrawn; these projects do not all have the same scope.
- **Purely informal naming conventions:** alone do not protect against name collisions, semantic drift, or unsupported agent mappings.
- **Compositional Semantic Typing (Promising Direction)**: Rather than requiring a central dictionary entry for every possible variable, a variable's semantic identity is defined by a multi-faceted compositional tuple:
  1. **Base Phenomenon / Concept**: What real-world quantity is being observed (e.g., `Corporate.Revenue`, `Atmospheric.Precipitation`).
  2. **Temporal Frame**: The temporal nature of the quantity (e.g., `Point-in-Time-Instant`, `Trailing-Interval(12M)`, `Forward-Projection(1Y)`, `Historical-Mean(1991-2020)`).
  3. **Methodological Standard**: The measurement or accounting rule (e.g., `GAAP`, `IFRS`, `NOAA-NClimDiv`, `Svensson-Yield-Curve-Fit`).
  4. **Boundary / Aggregation Scope**: The population or spatial envelope (e.g., `Consolidated-Entity`, `Central-Valley-Basin`, `Core-Ex-Food-Energy`).

## Investigation result — 2026-10-28

[[investigation-model-variable-quantity-representation]] finds concrete precedents for compositional context in SemSim (property plus bearer/location), SOSA/SSN (observation/property/feature/procedure/result), CF (quantity/coordinates/support/cell methods), and XBRL (concept/context/unit, instant/duration). See [[source-quantity-semantics-and-unit-standards]] for exact source evidence and limits.

Recommend shared semantic concepts plus contextual quantity specifications, **model-local symbol declarations**, and separate contextual value assertions. Symbols are not globally unique variables; two instances/scenarios can share a semantic specification without sharing one mutable value. Retain original source notation and scoped mappings rather than requiring a global ID for every composite phrase. Matching names, dimensions, embeddings, or even broad kind IDs is not sufficient to certify substitution.

Use direct/explicit-adapter/review-unknown/incompatible outcomes; unknown required qualifiers cannot pass automatically. SKOS mappings have different strengths; `owl:sameAs` is too strong for casual synonym links. SHACL/schema conformance and OWL entailment do not establish scientific truth. The compositional design remains provisional: no automatic mapping/ontology system or source extraction trial was implemented.

## Minimum answer for the first build

**B — before agents or users can create purportedly valid connections** ([[question-build-readiness]]). Select mandatory meaning/scope metadata for the supported domain and define exact-match, explicit-adapter, review-required, and rejection outcomes. Who can approve a semantic equivalence or override, with what evidence and retained provenance? An LLM can propose a mapping; dimensional compatibility or embedding similarity cannot certify it.

The compositional tuple is a candidate, not a settled ontology. A bounded vocabulary can be sufficient initially if unknown concepts fail honestly. Define treatment of entity boundaries, gross/net quantities, accounting/measurement conventions, stocks/flows, historical/projected values, and predictive versus causal purpose where exercised by the selected workflow. Include same-unit/wrong-meaning negative cases alongside valid bindings.

Candidate retrieval/ranking belongs to [[question-model-discovery-and-selection]], time/place transformations to [[question-temporal-and-spatial-data-alignment]], and source qualification to [[question-curation-evidence-and-approval]]. A first-build contract does not resolve universal cross-domain interoperability.

## What would resolve it?

1. Testing whether a compositional semantic tagging schema can unambiguously distinguish conflicting variables in our Intrinsic Valuation and FX benchmark suites.
2. Determining the validation rule for edge compilation: what degree of semantic mismatch generates a hard compile error versus a warning with an explicit assumption override.
3. Defining how autonomous agents use vector embeddings or ontology reasoning to search and map variables without human intervention.

## Linked context

- `[[concept-end-state-vision]]`: Mandates the Epistemic Ledger and total audit provenance.
- `[[hypothesis-global-variable-namespace-compatibility]]`: The core hypothesis that variables can link without central rewriting hinges on solving this question.
