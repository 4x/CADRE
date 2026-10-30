# Project state — Connected Models

> Compact cold-start document, not a diary. Details live in linked Project Memory records.

## Thesis and end state

**One model's input is another model's output; one model's assumption is another model's projection.** Compose qualified, domain-bounded models into an open dependency graph rather than silently invent missing inputs ([[concept-connected-models-thesis]]).

The mature vision combines an analyst workbench, provenance/badging ledger and polyglot dependency operating system ([[concept-end-state-vision]]), also serving as a deterministic quantitative reasoning layer for agents ([[concept-agent-quantitative-reasoning-layer]]). Reliability and token/turn savings are unmeasured hypotheses. Design and model coverage are early seeds; no Connected Models application or authenticated API integration is implemented here.

## Current understanding and boundaries

- **Offline curation — user-endorsed, 2026-10-28:** Dedicated Meta/Muse agents curate reusable models outside answering: discover papers/textbooks → extract/formalize mathematics, variables, units, assumptions and provenance → check/review → store. Query-time agents retrieve, compose and execute existing versions. Routine inline curation is ruled out; total prohibition versus last-resort exceptions remains open. “Offline” permits internet access. Roles/schema/approval/API capabilities are unsettled ([[concept-specialized-model-curation-agents]]).
- **Model-first assumptions — user-endorsed, 2026-10-27:** Use existing models/empirical inputs before guesses. Permitted Meta gaps must be explicit, provisional, replaceable and traceable downstream. Run-specific estimates differ from reusable-model curation; new relationships cannot bypass offline policy as “fallbacks.” Preserve preferences/unknowns; estimates are not observations or calibrated uncertainty ([[concept-connected-models-thesis]], [[question-assumption-resolution-and-fallback-policy]]).
- **Active MVP delivery plan — user direction, 2026-10-29:** Build ASAP, test with the user, adjust, then add features and scale; hackathon submission is the immediate milestone. [[note-mvp-build-sequence-and-extension-triggers]] is the canonical plan: M0 unblock → M1 runnable deterministic core → M2 complete offline-curation/query loop → M3 user testing/fixes → M4 release candidate → M5 submission → M6 evidence-led expansion. Calendar targets aim for a complete loop October 31, testing November 1–2 and release candidate November 3; these are targets, not promises. M0 is active; no application milestone has passed. Workflow/delegated selection and API access/spending were requested and remain pending. Domain-neutral core work need not wait for API access. Other technical defaults are agent recommendations, not automatically user-endorsed decisions.
- **First-build contract:** [[question-first-build-scope-and-success]] retains detailed acceptance for offline curate/review/store, then query-time retrieve/connect/execute/inspect/revise. Demonstrate actual offline extraction, later reuse, visible permitted gaps and independent references. No inline curation is the recommended milestone restriction; exact sources, references, access and feasibility still need evidence. Preserve testing time by cutting catalog/UI breadth before correctness and provenance.
- **Question ideas, NOT prescribed solutions — user clarification, 2026-10-29:** [[idea-end-state-question-gallery]] retains twelve questions; [[idea-domain-exemplars-intrinsic-value-and-fx]] adds equity/FX/bond questions; [[idea-prediction-market-question-catalog]] lists 26 market examples with P/K locators. Five former Queue documents are provisional `source-outsider-*` records. Their schemas, pipelines, rankings and pilot suggestions are **unverified outsider thoughts, NOT requirements or accepted solutions**. Author/full provenance is unknown; claimed 2026-10-28 snapshots were not rechecked. No pilot/model collection selected; synthetic Python is an unchanged source attachment, not product code.

## Representation and runtime groundwork

- [[investigation-model-variable-quantity-representation]] is completed **desk research**, with three source digests, alternatives, worked cases and proposed trials. [[concept-layered-model-representation]] provisionally separates semantic quantities/context, local symbols, values, revisions, implementations/calibrations, instances/bindings, experiments/runs and evidence without forcing all mathematics into one AST/DAG. No schema/importer/unit engine/runtime trial was implemented; questions remain active.
- [[decision-representation-contract-v0]] is a **provisional review draft** aligned with [[note-mvp-build-sequence-and-extension-triggers]]: six records (vocabulary/model/value/composition/review/run), one embedded algebra implementation/source map, scalar execution, exact meaning/context, pinned units/versions, owner review and run manifests. Synthetic two-model/two-composition fixtures are not runtime evidence. Arrays, multiple engines, general adapters and caching are extensions, not automatic MVP prerequisites.
- **Revise before acceptance:** v0 §10 flags blocking single-context-per-node and missing meaning/unit-dimension constraints; also vocabulary evolution, partial candidates and scenario reuse. Stage governance/numerics; select real operator/data needs before schemas. Desk recommendations, not runtime results.
- The 2025 prototype is documented as demonstrating hierarchical composition (nested DuPont ROI), explicit compilation phases and dirty-state tracking ([[investigation-prototype-2025-mathjs-supabase]], [[finding-graph-compilation-caching-requirement]]). Historical source descriptions are retained; the application source is not present or rerun here.

## Decisions, rejected and paused directions

- [[decision-unify-equations-and-graphs]] / [[concept-unified-computational-graph]]: the polymorphic equation/composite table addressed 2025 prototype redundancy. **Provisional**, not accepted as a universal ontology or future schema.
- [[decision-retire-standalone-mathjs-implementation]]: standalone browser/RPC Math.js is **retired as the universal runtime**, but remains a possible scalar sub-engine. Matrix/symbolic-differentiation support is confirmed; corrected older capability claims do not reverse the missing model/solver, semantics, environment and safety contracts.
- [[decision-deprecate-human-social-features-priority]]: social features are **paused**; marketplaces/social systems must not displace semantics and execution.

## Active hypotheses, not measured claims

- [[hypothesis-graph-grounded-agent-reliability]]: deterministic graph execution may improve quantitative reliability and reduce token/turn costs. Correct arithmetic alone does not validate model selection, data, bindings or explanations.
- [[hypothesis-global-variable-namespace-compatibility]]: shared dimensions, units and semantic ontologies may connect disparate models without rewriting internals. Cross-domain compatibility remains provisional and requires meaning/context checks, not just identical unit dimensions.

## Open questions and dependency order

**Start at [[question-build-readiness]].** Proposed A/B/C gates organize 17 substantive questions plus this entry point (18 records): a decision agenda, not accepted architecture/stack. Universal ontology and business strategy need not precede a bounded build.

### A — first-build framing and feasibility

- [[question-first-build-scope-and-success]]: hackathon/build-first/iterate priority confirmed; anchor/delegation and resources remain pending. Scope defaults and acceptance details are linked to the active delivery plan; still active.
- [[question-evaluation-and-reference-evidence]]: independent references, tolerances, negative cases and falsifiable release gates.
- [[question-technology-stack-and-meta-access]]: actual Meta access/tool capabilities, application/execution technologies and constraints; no stack/provider selected.
- [[question-execution-security-and-access]]: trusted/untrusted code, tools, data and network actions; isolation, limits and forbidden operations before enabling affected capabilities.

### B — minimum contracts before affected capabilities; broader answers later

- [[question-model-node-ast-and-schema-representation]]: equations, dynamics, stochastic models and oracles.
- [[question-dimensional-and-unit-type-system]]: dimensions, units, state-dependent conversion and shapes.
- [[question-semantic-variable-disambiguation]]: prevent same-unit, wrong-meaning connections without universal centralized curation.
- [[question-temporal-and-spatial-data-alignment]]: reconcile time/space resolution and support explicitly.
- [[question-uncertainty-and-epistemic-bounds-serialization]]: distinguish and propagate distributions, dependence, bounds, validity and sensitivity.
- [[question-graph-topology-and-feedback-cycles]]: whether/when cycles are supported and what resolves them.
- [[question-execution-runtime-for-heterogeneous-models]]: initial engines/adapters, runs, errors and invalidation; not automatically distributed.
- [[question-registry-storage-and-versioning]]: ownership, identity, pinned revisions, evidence, snapshots, reproducible runs and atomic updates.
- [[question-model-discovery-and-selection]]: candidate retrieval, applicability, alternatives and honest no-match outcomes.
- [[question-assumption-resolution-and-fallback-policy]]: stopping recursion, permitted Meta gaps, disclosure and unresolved/conditional results.
- [[question-curation-evidence-and-approval]]: evidence, declared-use eligibility, review, publishing, revision and withdrawal.
- [[question-agent-interaction-patterns]]: minimum tools/state transitions, authority, handoffs, retry and cancellation.

### C — strategy, not a universal pre-build blocker

- [[question-initial-domain-beachhead]]: commercial vertical, distinct from a bounded technical workflow; not selected by galleries/rankings.

## Hackathon material: available, provisional and time-sensitive

[[note-meta-hackathon-build-plan]] recommends water → energy → avoided grid purchases → incremental NPV. **Hydropower is not selected**: the user questioned that example on 2026-10-27. Older plan assumptions must yield to later offline-curation/first-build clarifications.

**2026-10-29 reinspection resolves the earlier outline-only warning:** detailed plan, [[source-hydropower-investment-demo-reference]] and [[source-meta-hackathon-and-model-api-2026]] bodies exist. Acceptance, access and freshness remain unverified.

Organizer landing page rechecked on 2026-10-29: November 4, 9 PM ET submission deadline (6 PM Los Angeles time). Judging weights, bonuses, prior-work eligibility, submission fields and participant/API access still need primary-rule/account confirmation. The detailed rules page still returned only Loading through text retrieval. See [[source-meta-hackathon-and-model-api-2026]].

## Next useful moves

1. **Execute M0/M1 in the active plan:** obtain workflow/delegation and access/spending answers; verify sources, reference cases and event requirements. Begin the domain-neutral deterministic skeleton while external access is unresolved. The immediate milestone is already confirmed; do not reopen the full question agenda.
2. **Fix the relevant v0 rules while implementing:** explicit per-port context and meaning/dimension constraints first; candidate handling, vocabulary evolution and scenario reuse by M2. See §10 of [[decision-representation-contract-v0]]. Keep one local runtime/backend, pinned evidence, independent cases and actionable rejection. Avoid implementing known-broken context rules or all future governance machinery.
3. **Complete, exercise and repair the loop:** real offline extraction and query-time reuse, inspection, substitution and preserved lineage; record defects and retests during M3, freeze at M4. Update milestone evidence in [[note-mvp-build-sequence-and-extension-triggers]]. Leave broader questions active and expand only from observed needs.

## Repository navigation and provenance

- `knowledge/ideas/`: candidate questions/use cases, not implementation requirements or a runtime registry; start at the three linked catalogs above.
- `knowledge/questions/`: unresolved platform choices, indexed by [[question-build-readiness]], not each end-user use-case question.
- `knowledge/sources/`: supporting evidence/originals. Provisional `source-outsider-*` = non-prescriptive commentary; archived `source-historical-*` = project-origin history. Imports retain prior paths, SHA-256 and **unchanged payloads**; historical line citations refer to those payloads. Concepts/decisions remain primary.
- `knowledge/sources/attachments/market_pipelines.py`: unchanged outsider code with fictional inputs, owned/contextualized by [[source-outsider-prediction-market-data-and-model-suggestions]]; not executed or validated during organization.
- Queue/Legacy content is migrated; empty Processed removed. Ignored `.kb/` and `.freebuff/` metadata, including Queue's marker, remain local, not knowledge. No application stack added.

## Last material update

2026-10-29
