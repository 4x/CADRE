---
id: note-mvp-build-sequence-and-extension-triggers
type: note
title: MVP Build Sequence and Extension Triggers
summary: Provisional implementation sequence and expansion triggers for a small complete Connected Models loop; preserve durable contracts while deferring infrastructure and unsupported model classes.
status: provisional
created: '2026-10-28'
updated: '2026-10-28'
topics:
  - architecture
  - strategy
  - runtime
confidence: medium
relations:
  - type: relates-to
    target: question-first-build-scope-and-success
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: question-registry-storage-and-versioning
  - type: relates-to
    target: question-execution-runtime-for-heterogeneous-models
  - type: relates-to
    target: decision-representation-contract-v0
  - type: derived-from
    target: finding-graph-compilation-caching-requirement
---

# MVP Build Sequence and Extension Triggers

## Scope and status

Proposal in response to the user's 2026-10-28 request for a quickly working, extensible MVP. The canonical product scope and acceptance contract remain in [[question-first-build-scope-and-success]]; this note adds implementation sequencing and reasons to revisit deferred capabilities. No domain, stack, deadline, spending limit, or architecture is accepted by this note. No application has been implemented or scalability measured.

The established offline-curation/query-time separation and explicit model-first assumption resolution remain in force. Social features remain paused; the standalone Math.js runtime remains retired. The first workflow, access, resource constraints, and implementation contracts remain unresolved. Historical schema choices remain provisional. The earlier hackathon plan now has a detailed body in this working tree, unlike the earlier inspection reported in PROJECT_STATE.md; its content does not establish present API access, event rules, or user acceptance.

## Small implementation, durable boundaries

Recommend one local application with modules for curation/review, registry, discovery/composition, validation/compilation, execution, and inspection. These are logical responsibilities, not separate services. Offline curation can initially be an explicitly invoked sequential job using the same registry. A single persistence backend and numerical engine are sufficient for the proposed algebraic scope; exact technologies require feasibility checks.

Prioritize contracts that are expensive to reconstruct after data accumulates: stable model identities and immutable versions; distinct model definitions, graph instances, and runs; explicit input/output meanings, units, shape, scope, and validity; source and assumption provenance; review eligibility; and pinned execution inputs and payload versions. Preserve unknown uncertainty explicitly. A versioned envelope can hold the initially supported implementation kind without pretending to represent every future solver.

Keep dependency compilation separate from evaluation. Initially, conservatively recompile and recompute on graph/input/version changes; evaluate each node once per run in dependency order. Cross-run caching and selective invalidation can wait. If caching is introduced, its keys must include every dependency affecting results; old results cannot be silently reused after edits.

Registry access and execution should have small explicit interfaces, initially implemented in-process. Avoid a generic plugin framework until an additional implementation demonstrates what needs to vary. Preserve portability through serializable definitions, graph/run manifests, and explicit schema versions; no claim of migration-free future expansion is warranted.

## Concrete representation draft

[[decision-representation-contract-v0]] proposes `cm-repr/0.1` as the concrete review draft for this sequence: six logical record kinds (vocabulary, model, value, composition, review, run), embedded local declarations/source maps/algebra implementation, scalar-only deterministic execution, exact semantic/context matching, pinned ratio-unit conversions, owner review and saved manifests. It is **provisional**, not an implemented schema or accepted architecture. The scalar-only restriction narrows the earlier optional short-array scope; extend it only if the selected workflow requires arrays.

The draft explicitly keeps one local app/backend/evaluator, full recompilation/recomputation, offline publication and query-time consumption. Its fixture catalog can bootstrap step 2 without being mistaken for step 3's real source curation. Per-increment responsibilities, extension triggers and proposed acceptance cases are in the draft; this note continues to own sequencing rather than duplicating field definitions. No generic registry/plugin framework, distributed authority, cross-run cache or universal ontology is a prerequisite.

### Critical-review caveat

The user-requested desk review in §10 of [[decision-representation-contract-v0]] recommends **revision before acceptance**, not discarding the layered approach. The original draft's one-Context-for-all-symbols rule blocks ordinary mixed-support/entity scalar models, and meaning definitions do not explicitly constrain permissible unit dimensions. Whole-vocabulary revision identity, incomplete candidate handling and exact scenario equality also need attention for continuing offline curation and scenario reuse. These are proposed revisions, not implemented failures or an accepted replacement schema.

Keep step 2's fixed-fixture skeleton small: simple local admission and pinned evidence are enough; concurrent review reconciliation, repeated revocation monitoring and custom low-level floating-point/conversion-trace machinery should not all become prerequisites. Determine the complete MVP's operators/shapes from the chosen useful workflow and actual sources rather than selecting the workflow solely to fit the scalar grammar. The review retains offline curation, honest unsupported outcomes, explicit provenance and the staged loop below.

## Incremental sequence

1. Bound one question family and its independent reference cases. Choose scope and tolerances together. Verify inference access and source availability early, with resource limits established before paid integration.
2. Build a deterministic walking skeleton: a small manually prepared fixture catalog, explicit graph, compatibility checks, compilation, execution, and saved run manifest. The fixture is a bootstrap tool, not evidence that offline curation works.
3. Add real offline agent extraction from an accessible source, review, and version publication into the same registry. Query execution must later consume the stored version without repeating extraction.
4. Add bounded query-time discovery/composition, existing-model resolution, disclosed permitted parameter estimates, and explicit conditional/unresolved outcomes. Neither model selection nor an agent's proposed edge bypasses compiler checks. Missing models may be queued for separate curation, not invented inline under this initial recommendation.
5. Add a minimal inspector for sources, dependencies, results, assumptions, failures, and input/model substitutions. Reuse a stored component in another composition through the same engine. Apply the canonical acceptance cases before calling the loop complete.

Each step should leave an inspectable runnable increment. Catalog breadth and UI polish are adjustable; source-faithful curation, numerical references, meaningful rejection, and lineage remain essential to the proposed complete MVP.

## Explicit deferrals and reconsideration triggers

| Defer | Preserve now | Reconsider when |
| --- | --- | --- |
| Distributed workers and service separation | Explicit module inputs/outputs and run identity | Measured workload, latency, or isolation requirements exceed local execution |
| Advanced retrieval infrastructure | Registry search boundary and applicability metadata | A growing catalog fails defined retrieval-quality or latency cases |
| Universal ontology and arbitrary model families | Small declared vocabulary, versioned interfaces, explicit unsupported errors | A selected second use case cannot be expressed faithfully |
| Polyglot execution, ODE/PDE solvers, feedback cycles | Implementation kind, execution adapter boundary, topology validation | An accepted workflow requires a specific additional engine or solver |
| General uncertainty propagation | Origin, validity, unknown uncertainty, scenario labels | A decision requires justified distributions/correlations beyond scenario comparison |
| Cross-run caching and incremental recomputation | Compilation/evaluation separation and pinned inputs | Measured recomputation cost justifies invalidation complexity |
| Autonomous mass curation | Candidate/review/eligible separation and source references | Reviewed ingestion quality and a real coverage bottleneck justify expansion |
| Public hosting, accounts, collaboration | Explicit single-operator/local trust boundary | A real second-user or sharing requirement arises; add access controls before exposing data/actions |
| Untrusted arbitrary code | Reviewed permitted payloads only | A concrete workflow warrants an isolated execution design before enabling that code |
| Marketplace, federation, social features | Stable identities and exportable artifacts | A validated product need justifies their separate design |

The immediate extensibility test is whether adding a compatible model and a second composition changes registry content and graph definitions without requiring a special calculation path in the executor. This is evidence of bounded reuse, not proof of universal model interoperability or production capacity.

## Provenance

Derived from repository state and the existing first-build contract, with implementation sequencing and expansion triggers proposed by the assistant. No external technology comparison or new empirical evidence was used. Earlier user edits were left intact; this note does not resolve the linked open questions.
