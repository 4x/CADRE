---
id: question-semantic-variable-disambiguation
type: question
title: Semantic Variable Disambiguation and Ontology
summary: How can the ontology prevent "type-safe nonsense" across identical units (e.g., trailing GAAP revenue vs forward ARR) without requiring centralized manual curation for every edge?
status: active
created: '2026-10-24'
updated: '2026-10-24'
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

- **Monolithic ontologies (e.g., FIBO, SNOMED, Cyc)**: Historically attempt to build universal semantic taxonomies. They suffer from severe brittleness, slow update cycles, and high barriers to entry for modelers.
- **Purely informal naming conventions**: Free-form variable names guarantee name collisions, semantic drift, and catastrophic agent hallucinations.
- **Compositional Semantic Typing (Promising Direction)**: Rather than requiring a central dictionary entry for every possible variable, a variable's semantic identity is defined by a multi-faceted compositional tuple:
  1. **Base Phenomenon / Concept**: What real-world quantity is being observed (e.g., `Corporate.Revenue`, `Atmospheric.Precipitation`).
  2. **Temporal Frame**: The temporal nature of the quantity (e.g., `Point-in-Time-Instant`, `Trailing-Interval(12M)`, `Forward-Projection(1Y)`, `Historical-Mean(1991-2020)`).
  3. **Methodological Standard**: The measurement or accounting rule (e.g., `GAAP`, `IFRS`, `NOAA-NClimDiv`, `Svensson-Yield-Curve-Fit`).
  4. **Boundary / Aggregation Scope**: The population or spatial envelope (e.g., `Consolidated-Entity`, `Central-Valley-Basin`, `Core-Ex-Food-Energy`).

## What would resolve it?

1. Testing whether a compositional semantic tagging schema can unambiguously distinguish conflicting variables in our Intrinsic Valuation and FX benchmark suites.
2. Determining the validation rule for edge compilation: what degree of semantic mismatch generates a hard compile error versus a warning with an explicit assumption override.
3. Defining how autonomous agents use vector embeddings or ontology reasoning to search and map variables without human intervention.

## Linked context

- `[[concept-end-state-vision]]`: Mandates the Epistemic Ledger and total audit provenance.
- `[[hypothesis-global-variable-namespace-compatibility]]`: The core hypothesis that variables can link without central rewriting hinges on solving this question.
