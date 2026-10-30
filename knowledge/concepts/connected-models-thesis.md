---
id: concept-connected-models-thesis
type: concept
title: Connected Models Thesis
summary: Connecting domain-bounded models into a dependency graph eliminates arbitrary assumptions, integrates fragmented data, and enables objective quantitative decision-making.
status: accepted
created: '2026-10-24'
updated: '2026-10-28'
topics:
  - vision
  - architecture
  - decision-support
confidence: high
relations:
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: concept-agent-quantitative-reasoning-layer
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: addresses
    target: question-initial-domain-beachhead
  - type: addresses
    target: question-execution-runtime-for-heterogeneous-models
  - type: derived-from
    target: source-historical-problem-statement-and-initial-thoughts
  - type: derived-from
    target: source-historical-connected-models-slides-2020
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

## Model-first assumption resolution

User clarification on 2026-10-27: a missing assumption should ideally be resolved by plugging in the appropriate upstream model, not by asking the user to supply a plausible number. If no suitable model is available or usable, a Meta/Muse agent should fill the gap and make that contribution unmistakable.

The product principle is accepted; the following operational details are proposed:

1. **Search and bind before guessing.** Resolve a missing quantity through an appropriate existing model in the curated repository and its empirical inputs. Match meaning, validity conditions, place, time, and uncertainty—not just variable names or units. Prefer a direct observation when the quantity is observable; do not manufacture a projection unnecessarily.
2. **Recurse into dependencies.** Expose the chosen model's own unresolved inputs and resolve them in turn. A model moves and structures assumptions; it does not magically eliminate them. Track repeated dependencies, shared evidence, and feedback loops rather than expanding forever.
3. **Use an explicit Meta fallback when needed.** Where retrieval, access, evidence, compatibility, or practical limits prevent a suitable binding, the earlier proposal permits parameter estimates, proxy relationships, distributions, or provisional submodels. This is not blanket permission for query-time model creation: new relationships/submodels must respect the offline-curation boundary below and the unresolved no-inline-versus-last-resort policy. Label which kind of contribution it made and why. Where possible, encode its proposed relationship as an executable node so that trusted code still performs subsequent calculations.
4. **Retain provenance and consequence.** Record the agent/model version, generation time, supporting sources if any, rationale, scope, uncertainty or an explicit lack of calibrated uncertainty, and the dependent results. A citation does not make a generated estimate an observed fact. A source-backed model translated by AI also requires checking that the translation preserves the source.
5. **Keep the fallback replaceable and visible.** Mark the specific node or binding and surface it in the final answer, including downstream reliance and material sensitivity where measurable. Re-run affected results when a suitable curated model becomes available; preserve the old run and its lineage.

Illustrative disclosure: **“Meta-generated estimate: customer switching rate. No suitable model for this market was available. This provisional input affects the revenue forecast and valuation; its uncertainty has not been calibrated.”** This is a disclosure example, not a domain estimate.

Distinguish an empirical input, a model-derived projection, a user-chosen scenario or preference, and a Meta-generated contribution. Preferences and hypothetical interventions are not missing facts to be silently replaced. Nor should the agent invent private information, fabricate evidence, attach unjustified probability bounds, or force a numerical answer when a defensible estimate is impossible. In those cases, keep an explicitly unresolved dependency or return a conditional answer.

**Offline-curation boundary (user clarification, 2026-10-28):** Dedicated agents primarily or exclusively discover and formalize models from papers, textbooks, and other sources outside individual question-answering requests. They normalize models, extract equations/variables/constants/parameters, and store reusable versions in the repository. Query-time agents primarily select, compose, and execute that existing collection. They may surface gaps for separate offline curation, not routinely curate during an answer. Whether inline curation is forbidden entirely or permitted only as an explicit last resort remains open. A disclosed provisional input estimate is distinct from curating/publishing a new reusable model; calling a new relationship a fallback cannot bypass this boundary. "Offline" describes timing relative to answering, not network isolation.

Search-depth/cost limits and review requirements for consequential uses remain open. [[concept-specialized-model-curation-agents]] develops how temporary gaps become candidates for durable coverage rather than recurring hidden guesses. [[question-uncertainty-and-epistemic-bounds-serialization]] remains responsible for the formal representation of epistemic status and uncertainty.

## What changed recently

On 2026-10-27, the user clarified the model-first resolution principle and the requirement for explicit Meta-generated gap-filling; this extends rather than replaces the original thesis.

The thesis originated in 2020 as a human-centric knowledge-sharing platform ("Wikipedia + GitHub + Bloomberg + Scratch for models"). While the human value proposition remains relevant, the primary operational focus has evolved: autonomous AI agents require deterministic, external quantitative execution environments to prevent hallucinations, reduce token consumption, and cut multi-turn prompt latency.

## Uncertainties

- How to balance the long-term grand vision ("all the world's models connected in one place") with selecting an immediate commercial and technical beachhead ([[question-initial-domain-beachhead]]).
- How to handle proprietary models, code boundaries, and heterogeneous execution environments across institutions ([[question-execution-runtime-for-heterogeneous-models]]).

## Legacy provenance

Reconstructed from [[source-historical-problem-statement-and-initial-thoughts]] and [[source-historical-connected-models-slides-2020]].
