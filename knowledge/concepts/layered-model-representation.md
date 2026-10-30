---
id: concept-layered-model-representation
type: concept
title: Layered Model Representation
summary: Provisional common contract separating semantic quantities, local declarations, contextual values, model revisions, implementations, compositions, experiments/runs, and evidence; specialized mathematical payloads preserve formalisms. Not an accepted or tested schema.
status: provisional
created: '2026-10-28'
updated: '2026-10-28'
topics:
  - representation
  - ontology
  - architecture
confidence: medium
relations:
  - type: derived-from
    target: investigation-model-variable-quantity-representation
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: relates-to
    target: decision-representation-contract-v0
  - type: addresses
    target: question-model-node-ast-and-schema-representation
  - type: addresses
    target: question-dimensional-and-unit-type-system
  - type: addresses
    target: question-semantic-variable-disambiguation
  - type: addresses
    target: question-registry-storage-and-versioning
---

# Layered Model Representation

## Status and basis

Recommendation from [[investigation-model-variable-quantity-representation]], completed 2026-10-28 as **desk research**, not an accepted architecture, implemented schema, import/export test, or measured improvement. The report compares primary-source precedents, alternatives, worked cases, and proposed falsification trials. It does not supersede the historical prototype records: those document a different implemented context.

## Core principle

**Canonicalize shared contracts, not all mathematics into one universal normal form.** Keep semantic identity, local mathematical syntax, values, executable artifacts, evidence, and run history distinct. Use a small common envelope and explicit mathematical/operation profiles; preserve native richer payloads without claiming executable support.

## Logical distinctions to preserve

1. **Semantic concept / quantity kind:** energy, torque, revenue, probability; dimensions alone do not identify these.
2. **Quantity specification:** property plus bearer/entity, convention, temporal/spatial support, aggregation and other relevant qualifiers. External ontology references can be combined with source-local definitions and scoped mappings.
3. **Local declaration / port:** a symbol scoped to a model revision/component, original notation, type/unit/shape, mathematical role and variability; input/output role is operation-dependent for acausal models. No global mutable variable slot.
4. **Value assertion / dataset version:** actual value or artifact, context/entity/time/scenario, origin, precision, missingness, uncertainty/dependence, source and information vintage. Observation, projection, scenario, calibration, and Meta estimate are not interchangeable.
5. **Model definition/version:** formalism, mathematical relationships, declarations, assumptions, applicability and evidence. A stable model family is not a specific immutable version.
6. **Implementation/calibration:** pinned artifact and environment, capabilities/fidelity, parameter set and estimation evidence. One model can have several implementations or calibrations.
7. **Composition/instance/binding:** reusable selected components with independent instance contexts and explicit adapters; a composition is not the compiled execution schedule.
8. **Experiment/run/result:** requested operation/settings versus actual resolved versions/inputs/environment, validations, execution status and generated outputs.
9. **Evidence/review/mapping claims:** attributable and version/use-scoped; source fidelity, dimensional compatibility, numerical reproduction, empirical adequacy and execution eligibility are different claims.

These are logical boundaries, not a demand for nine services or one database table per object. Local declarations can be embedded; reuse/version boundaries need explicit stable references.

## Layers and first executable subset

- **Shared envelope:** typed JSON-compatible records, schema/profile versions, identity, source spans, assumptions/applicability, interface, semantic and evidence links. Evaluate JSON Schema 2020-12 for structure plus deterministic semantic/reference/type validators. JSON-LD/RDF/SHACL can serve a graph projection when justified; no graph database is selected.
- **Math payload:** declare formalism and capabilities. Start with allowlisted structural explicit algebra, supported real scalar values (short dated arrays only if required), explicit predicates/functions, and an acyclic inter-model plan. Preserve source equations and source-to-structure mapping. Exact operator grammar and backend remain unselected.
- **Typed values:** quantity kind and contextual spec, unit/scale, dtype/precision, shape/axes/support, origin, missingness and uncertainty. Distinguish temperature points/deltas, distribution parameterizations, and joint sample identity; unknown uncertainty is valid metadata, not a zero variance.
- **Specialized future payloads:** equation systems, ODE/DAE/state/events, probabilistic programs, optimization, simulator interfaces and oracles retain their own semantics. Catalog-only support does not imply executable support; never silently convert an implicit system into a DAG by inventing a delay or solver.
- **Evidence/lineage:** PROV-aligned entity/activity/agent distinctions plus required source/review/version/run fields; pinned model, implementation, calibration, data and mapping versions. Byte digests are not semantic equivalence or scientific verification.

## Standards strategy

Borrow roles rather than adopt every standard: MathML/OpenMath for structured math/operator meaning; CellML/SBML/Modelica for model structure; FMI/BMI for execution interfaces; QUDT/UCUM for bounded kind/unit references and tested conversions; SemSim/SOSA/CF/XBRL for contextual quantities; xarray-like axes for data; PROV for lineage; SED-ML for experiment separation. No single standard fills all roles. No dependency, unit-library crosswalk, importer or exact serialized schema is selected or tested.

## Compatibility rule

Return **direct binding**, **explicit adapter required**, **review/unknown**, or **incompatible/unsupported**. Check type/shape/axes, quantity semantics and scope, units/scale, entity/time/aggregation/method/basis, actual preconditions, execution eligibility and evidence. Equal dimensions, names, annotations or embeddings cannot certify substitution. Unknown required semantics cannot pass as compatible.

Only validated conversions preserving meaning should be automatic initially. FX, inflation rebasing, aggregation, interpolation, convention changes and entity consolidation require explicit contextual transformations/models and provenance. Shared marginal distributions or equal-length sample arrays do not establish independent or paired samples.

## Offline-curation consequence

Dedicated agents extract and normalize source models, variables/constants/parameters and context into candidate records, then check/review/publish qualified versions **outside answering requests**. Partial, ambiguous and non-executable models can be cataloged honestly. Query-time agents consume existing eligible versions, compose and execute, and surface gaps for later curation. A provisional input estimate is not automatic publication of a new model; on-the-fly model creation remains forbidden or last-resort-only under the unresolved policy.

## Concrete first-contract draft

[[decision-representation-contract-v0]] now specifies a provisional `cm-repr/0.1` contract aligned with [[note-mvp-build-sequence-and-extension-triggers]]: six logical record kinds, embedded sole algebra implementation/source maps, scalar values, exact semantic/context matching, pinned units/versions, owner-scoped review, explicit bindings and actual run lineage. It includes a self-contained synthetic two-model/two-composition example and expected failure outcomes. This is a review draft, not a machine-enforced schema, model curation run, or accepted architecture; it deliberately defers arrays, multiple implementations, solvers, graph infrastructure and caching until needed. The concept here remains the broader rationale; the decision draft owns exact v0 fields/rules.

## Tradeoffs and unresolved evidence

The layered approach preserves diverse formalisms and improves auditability in principle, at the cost of adapters, mapping governance, schema/profile versioning and envelope/payload consistency checks. It is not evidence that composition will be cheap, universal or automatic.

Before acceptance: test source-faithful extraction from actual papers/textbooks; supported algebra and independent references; same-unit/wrong-meaning and same-shape/wrong-support rejections; repeated instances and revision/fallback-replacement lineage. Test richer native payload preservation only when needed. The report provides cases and proposed trials; none has been executed. Keep the broader representation/unit/semantics/registry questions active.
