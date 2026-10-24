---
id: concept-connected-models-thesis
type: concept
title: Connected Models Thesis
summary: Connecting domain-bounded models into a dependency graph eliminates arbitrary assumptions, integrates fragmented data, and enables objective quantitative decision-making.
status: accepted
created: '2026-10-24'
updated: '2026-10-24'
topics:
  - vision
  - architecture
  - decision-support
confidence: high
relations:
  - type: relates-to
    target: concept-agent-quantitative-reasoning-layer
  - type: relates-to
    target: concept-unified-computational-graph
  - type: addresses
    target: question-initial-domain-beachhead
  - type: addresses
    target: question-execution-runtime-for-heterogeneous-models
---

# Connected Models Thesis

## Current understanding

To make high-stakes decisions, we must model their consequences and impacts. However, existing quantitative models suffer from severe systemic limitations:
- **Black-box opacity**: Internal logic and assumptions are frequently hidden or uninspected.
- **Scope boundaries and competence risk**: Models can always be expanded to include additional parameters, but modelers quickly venture outside their domain of expertise.
- **Siloed inputs and assumptions**: In almost every decision scenario, valuable data and domain knowledge are left on the table because practitioners lack tools to integrate external models.

The foundational thesis of Connected Models resolves this through two complementary axioms:
> *One model's input is another model's output.*  
> *One model's assumption is another model's projection.*

By composing models into an open dependency graph, arbitrary assumptions are replaced with empirical outputs or verified projections from upstream domain models. The answer to complex quantitative questions emerges through the evaluation of the graph rather than ad-hoc guesswork.

## Key points

- **Radical decomposition**: Monolithic calculations are broken down into modular, reusable sub-models and atomic equations with explicit interface contracts.
- **Assumption reduction**: An assumption in one domain (e.g., inflation rate or cost of capital) is replaced by connecting to a specialized model in that domain.
- **Cross-domain applicability**: Applicable across financial valuation, macro forecasting, risk engineering (VaR, DIMP), climate impacts, pharmacology, and prediction markets.
- **Grounding for autonomous agents**: Provides a verified mathematical foundation for LLMs and autonomous agents ([[concept-agent-quantitative-reasoning-layer]]).

## What changed recently

The thesis originated in 2020 as a human-centric knowledge-sharing platform ("Wikipedia + GitHub + Bloomberg + Scratch for models"). While the human value proposition remains relevant, the primary operational focus has evolved: autonomous AI agents require deterministic, external quantitative execution environments to prevent hallucinations, reduce token consumption, and cut multi-turn prompt latency.

## Uncertainties

- How to balance the long-term grand vision ("all the world's models connected in one place") with selecting an immediate commercial and technical beachhead ([[question-initial-domain-beachhead]]).
- How to handle proprietary models, code boundaries, and heterogeneous execution environments across institutions ([[question-execution-runtime-for-heterogeneous-models]]).

## Legacy provenance

Reconstructed from `Legacy/ProblemStatementInitialThoughts.md` and `Legacy/Slides2020.md`.
