---
id: question-model-node-ast-and-schema-representation
type: question
title: Model Node AST and Schema Representation
summary: What unified schema or AST representation can formally express discrete equations, continuous ODEs/PDEs, stochastic processes, and black-box oracles?
status: active
created: '2026-10-24'
updated: '2026-10-28'
topics:
  - representation
  - architecture
confidence: high
relations:
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: question-execution-runtime-for-heterogeneous-models
  - type: relates-to
    target: investigation-model-variable-quantity-representation
  - type: relates-to
    target: concept-layered-model-representation
  - type: relates-to
    target: decision-representation-contract-v0
  - type: derived-from
    target: source-historical-mathjs-prototype-architecture
---

# Model Node AST and Schema Representation

## Question

What formal Abstract Syntax Tree (AST) or declarative schema can comprehensively represent the full spectrum of quantitative models—spanning closed-form scalar algebra, implicit equations, continuous differential systems (ODEs/PDEs), stochastic processes, and black-box proprietary oracles—without sacrificing mathematical expressiveness or execution performance?

## Why it matters

The 2025 prototype stored formulas as strings (`expression_latex` and `expression_code`) parsed at runtime by Math.js ([[source-historical-mathjs-prototype-architecture]]). Its demonstrated scope was algebraic composition. **Correction, 2026-10-28:** strings in a specified language can represent rich mathematics; the limitation is not the storage primitive. Unspecified raw text alone does not establish scoped symbols, formalism, initialization, solver/operation semantics, type checking, source fidelity, or safe execution.

Expressions, simultaneous equation systems, ODE/DAE models, probability programs, optimization tasks, and executable simulator interfaces need different semantics. Structural expression trees are useful substructures, not automatically complete models. Define a supported grammar/profile and explicit validation/adapter boundaries rather than assuming arbitrary source text is executable or one AST covers everything.

## Current partial answer

- Primary-source research in [[investigation-model-variable-quantity-representation]] compares MathML/OpenMath, CellML/SBML, Modelica, FMI/BMI, symbolic IRs, statistical/optimization programs, units/semantics, and data/provenance layers. See its linked source digests for exact evidence/version limits. Mathematical syntax, executable interfaces, and evidence records serve different roles; none alone supplies the complete contract.
- The likely path forward is a **two-tier representation**:
  1. An outer **Declarative Interface Envelope** that standardizes variable roles, assumptions, citations, transparency badging, and boundary contracts across all nodes.
  2. A polymorphic **Execution Payload** that supports engine-specific representations (e.g., symbolic AST for algebra, state-space vector fields for ODEs, or container/API endpoint descriptors for black-box oracles).

## Investigation result — provisional, not a schema decision

[[concept-layered-model-representation]] recommends distinct semantic concepts/contextual quantity specifications, model-local declarations, value assertions, immutable model revisions, implementations/calibrations, instances/bindings, experiments/runs, and evidence claims. Canonicalize common contracts and source maps, not every model into one mathematical normal form. Roles such as state/unknown/parameter, input/output/internal, and observed/scenario/generated are separate axes; direction can depend on the requested operation.

For a bounded first profile, evaluate a typed JSON-compatible envelope and allowlisted structural explicit-algebra payload with deterministic reference/type/domain checks. Preserve native richer formalisms as catalog-only until adapters exist. Unknown required semantics or unsupported operators/formalisms cannot be silently lowered to formulas. JSON Schema validates structure, not mathematical equivalence, source fidelity, or scientific truth. A tiny native expression profile versus a restricted existing format remains a trial choice; no dependency or exact AST is selected.

The report contains a logical entity map, illustrative serialized model, ten hand-analyzed compatibility/lineage cases, and proposed source-extraction/roundtrip trials. These are desk-analysis results, **not performed implementation tests**. This question remains active pending an accepted v0 contract and affected trials.

## Concrete v0 proposal — awaiting review

[[decision-representation-contract-v0]] makes the recommended first subset concrete: `cm-repr/0.1` records and `scalar-algebra/0.1` payload, an exact restricted expression/predicate grammar, model-local symbols/roles, source mappings, explicit constants and input bindings, pinned units/meanings, scalar numeric semantics, diagnostics and run manifests. An embedded sole implementation avoids a premature plugin/artifact registry. Arrays/short series and rich model execution are deferred with explicit extension triggers, aligned with [[note-mvp-build-sequence-and-extension-triggers]]. A synthetic fixture and proposed positive/negative outcomes make the draft reviewable; no executable schema or runtime tests are claimed. Review the concrete draft rather than reopening the full standards survey; this question stays active pending acceptance and affected implementation checks.

## Minimum answer for the first build

**B — before model definitions and tool payloads become shared contracts** ([[question-build-readiness]]). Decide the supported model/payload classes, outer interface envelope, input/output bindings, parameter/state roles, preconditions, and unsupported-kind behavior. Distinguish reusable model definitions/versions from graph node instances and concrete input bindings, including Meta-generated contributions. Which fields may agents propose, and which does deterministic validation require?

The two-tier envelope/payload approach is a candidate, not an accepted universal AST. A first schema need not encode every ODE/PDE or oracle, but must not silently reinterpret unsupported kinds as scalar equations. Compare viable schemas against the chosen workflow's ordinary, invalid, and provisional cases; establish schema-version/extension rules.

Co-design with [[question-registry-storage-and-versioning]] (identity/provenance ownership), [[question-dimensional-and-unit-type-system]], [[question-semantic-variable-disambiguation]], and [[question-uncertainty-and-epistemic-bounds-serialization]]. An initial contract can be decided while the universal representation question remains active.

## What would resolve it?

1. Benchmarking candidate AST schemas against the three exemplar models from our legacy materials: the algebraic DuPont model, the Intrinsic Valuation network, and a continuous physical model.
2. Determining whether the internal AST should be language-agnostic (e.g. custom JSON/Protobuf AST) or leverage an existing scientific intermediate representation.

## Linked context

- `[[concept-end-state-vision]]`: Mandates the multi-tier cascade uniting algebraic, continuous, and discrete models.
- `[[concept-unified-computational-graph]]`: Identifies the limits of the initial flat relational schema.
- `[[question-execution-runtime-for-heterogeneous-models]]`: Runtime orchestration depends directly on the chosen node representation.
