# Project state — Connected Models

> Compact cold-start document for a human or agent returning after time away.
> Keep this current and decision-oriented. It is not a diary.

## Current thesis

To make high-stakes decisions, we must model their consequences and impacts. However, individual quantitative models are bounded by their assumptions and domain scope: when modelers expand their models to include more parameters, they risk venturing far outside their expertise. Because *one model's input is another model's output, and one model's assumption is another model's projection*, composing models into an open dependency graph replaces arbitrary assumptions with verified upstream outputs ([[concept-connected-models-thesis]]).

Furthermore, the system serves as an external deterministic **quantitative reasoning layer** for autonomous AI agents and LLMs ([[concept-agent-quantitative-reasoning-layer]]). Rather than performing multi-step arithmetic, numerical simulations, and sensitivity sweeps in-context—which consumes massive prompt tokens, increases latency, and risks arithmetic hallucinations—agents delegate quantitative evaluation to the model graph.

## Where things stand

- Historical legacy materials (spanning the 2020 conceptual pitch and 2025 prototype notes) have been reconciled and migrated into a lean, 16-artifact Project Memory corpus.
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

- `[[question-execution-runtime-for-heterogeneous-models]]`: What architecture can orchestrate and execute heterogeneous, polyglot models (spanning algebra, ODEs/PDEs, scientific Python/R, and external APIs)?
- `[[question-initial-domain-beachhead]]`: Which initial vertical (e.g., corporate valuation, FX forecasting, prediction markets) offers the best combination of commercial traction and benchmark clarity?
- `[[question-agent-interaction-patterns]]`: What protocols, schemas, and division of labor should govern how parallel autonomous agents discover, compose, and execute model graphs?

## Abandoned / paused directions

- **Standalone Math.js client as the sole execution engine**: Incapable of supporting differential equations, stochastic simulations (Monte Carlo), or polyglot scientific software.
- **Premature human social features**: Building user profiles, starring systems, voting, and comment boards before solving semantic interoperability and multi-engine execution.

## Next useful moves

1. **Research representation, ontology, and runtime**: First of all, identify and articulate the fundamental questions we need to ask regarding mathematical representation, type safety, dimensional compatibility, and polyglot execution.
2. **Vision for end state**: Start constructing a concrete, vivid picture of what the final deliverable looks like. What could one do with it? What are some real-world problems that could be solved? What might get cheaper, faster, more accurate, or fundamentally possible that isn't today?

## Last material update

2026-10-24
