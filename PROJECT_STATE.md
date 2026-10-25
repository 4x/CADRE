# Project state — Connected Models

> Compact cold-start document for a human or agent returning after time away.
> Keep this current and decision-oriented. It is not a diary.

## Current thesis

To make high-stakes decisions, we must model their consequences and impacts. However, individual quantitative models are bounded by their assumptions and domain scope: when modelers expand their models to include more parameters, they risk venturing far outside their expertise. Because *one model's input is another model's output, and one model's assumption is another model's projection*, composing models into an open dependency graph replaces arbitrary assumptions with verified upstream outputs ([[concept-connected-models-thesis]]).

The mature deliverable is conceived as a universal computational medium unifying an interactive analyst workbench, an epistemic ledger of model components with full provenance and badging, and a polyglot dependency operating system ([[concept-end-state-vision]]). Furthermore, the system serves as an external deterministic **quantitative reasoning layer** for autonomous AI agents and LLMs ([[concept-agent-quantitative-reasoning-layer]]). Rather than performing multi-step arithmetic, numerical simulations, and sensitivity sweeps in-context—which consumes massive prompt tokens, increases latency, and risks arithmetic hallucinations—agents delegate quantitative evaluation to the model graph.

## Where things stand

- Historical legacy materials (spanning the 2020 conceptual pitch and 2025 prototype notes) have been reconciled and migrated into Project Memory.
- A comprehensive end-state vision has been established ([[concept-end-state-vision]]), detailing the three-tier lifecycle (Querying, Authoring, Stress-Testing), the flagship physical-to-financial cross-domain cascade, transparency badging (white-box to proprietary black-box oracles), and the capability delta.
- The 2025 prototype proved the viability of hierarchical graph composition (e.g. nested DuPont ROI financial models) and established that graphs require explicit compilation phases and dirty-state tracking ([[investigation-prototype-2025-mathjs-supabase]], [[finding-graph-compilation-caching-requirement]]).
- The unified relational graph schema used in the 2025 prototype is classified as **provisional** ([[concept-unified-computational-graph]], [[decision-unify-equations-and-graphs]]); it solved concrete database redundancy in the prototype, but is not accepted as a universal architectural truth pending deeper research into representation and ontology.
- The standalone browser/RPC Math.js architecture is retired as the primary execution engine ([[decision-retire-standalone-mathjs-implementation]]), while remaining a candidate sub-engine for lightweight scalar algebra in a future multi-engine runtime.
- Human social networking features (starring, comments, public feeds) are paused ([[decision-deprecate-human-social-features-priority]]) to concentrate technical resources on foundational computational semantics and agent execution interfaces.

## Major decisions

- `[[decision-retire-standalone-mathjs-implementation]]`: Retired standalone Math.js as the sole execution engine, preserving it as a potential sub-engine for scalar algebraic evaluation in a future multi-engine runtime.
- `[[decision-unify-equations-and-graphs]]`: (Provisional) Merged equations and composite graphs into a polymorphic table for the 2025 prototype; kept provisional pending ontology groundwork.
- `[[decision-deprecate-human-social-features-priority]]`: (Paused) Paused social web features to focus engineering on representation, ontology, and runtime mechanics.

## Active hypotheses

- `[[hypothesis-graph-grounded-agent-reliability]]`: Grounding AI agents in deterministic model graphs eliminates calculation hallucinations and dramatically reduces token consumption and execution turns.
- `[[hypothesis-global-variable-namespace-compatibility]]`: (Provisional) Disparate domain models can be linked across boundaries via shared dimensions, standardized units, and semantic ontologies without rewriting internal source code.

## Open questions

### Representation & Ontology
- `[[question-model-node-ast-and-schema-representation]]`: What unified schema or AST representation can formally express discrete equations, continuous ODEs/PDEs, stochastic processes, and black-box oracles?
- `[[question-dimensional-and-unit-type-system]]`: How should Connected Models represent physical/economic dimensions, unit systems, state-dependent conversions, and higher-order tensor/distribution shapes?
- `[[question-semantic-variable-disambiguation]]`: How can the ontology prevent "type-safe nonsense" across identical units (e.g., trailing GAAP revenue vs forward ARR) without requiring centralized manual curation for every edge?
- `[[question-temporal-and-spatial-data-alignment]]`: How should the graph reconcile mismatching temporal and spatial resolutions when connecting continuous time-series, periodic averages, and static projections?
- `[[question-uncertainty-and-epistemic-bounds-serialization]]`: How should error bounds, probability distributions, sensitivity gradients, and validity domains be serialized and propagated across heterogeneous graph nodes?
- `[[question-graph-topology-and-feedback-cycles]]`: Should Connected Models permit cyclic dependency graphs (feedback loops and market equilibria), and what mathematical resolution mechanics should govern them?

### Runtime, Strategy & Agents
- `[[question-execution-runtime-for-heterogeneous-models]]`: What architecture can orchestrate and execute heterogeneous, polyglot models (spanning algebra, ODEs/PDEs, scientific Python/R, and external APIs)?
- `[[question-initial-domain-beachhead]]`: Which initial vertical (e.g., corporate valuation, FX forecasting, prediction markets) offers the best combination of commercial traction and benchmark clarity?
- `[[question-agent-interaction-patterns]]`: What protocols, schemas, and division of labor should govern how parallel autonomous agents discover, compose, and execute model graphs?

## Abandoned / paused directions

- **Standalone Math.js client as the sole execution engine**: Incapable of supporting differential equations, stochastic simulations (Monte Carlo), or polyglot scientific software.
- **Premature human social features**: Building user profiles, starring systems, voting, and comment boards before solving semantic interoperability and multi-engine execution.

## Next useful moves

1. **Research node AST and unit type system**: Deep-dive into `[[question-model-node-ast-and-schema-representation]]` and `[[question-dimensional-and-unit-type-system]]`, surveying candidate AST and unit schemas (SymPy, MathML, QUDT, UCUM).
2. **Prototype semantic disambiguation**: Evaluate the compositional semantic typing model (`[[question-semantic-variable-disambiguation]]`) against the Intrinsic Valuation benchmark to formalize how "type-safe nonsense" is prevented.

## Last material update

2026-10-24
