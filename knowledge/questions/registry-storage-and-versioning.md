---
id: question-registry-storage-and-versioning
type: question
title: Model Registry Storage, Identity, and Versioning
summary: What owns models, evidence, data snapshots, graph definitions, and runs; how are versions, provenance, reproducibility, and concurrent edits stored without equating the registry with the execution graph?
status: active
created: '2026-10-27'
updated: '2026-10-28'
topics:
  - architecture
  - representation
  - lifecycle
confidence: null
relations:
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: question-model-node-ast-and-schema-representation
  - type: relates-to
    target: finding-graph-compilation-caching-requirement
  - type: relates-to
    target: question-curation-evidence-and-approval
  - type: relates-to
    target: investigation-model-variable-quantity-representation
  - type: relates-to
    target: decision-representation-contract-v0
---

# Model Registry Storage, Identity, and Versioning

## Question

What is the source of truth for model knowledge and executable artifacts, and how do identity, versioning, provenance, and run snapshots remain coherent as agents curate and update the collection?

## Decisions to answer

- Which entities are distinct: source document, underlying scientific model, implementation, calibration, dataset/observation, versioned interface, graph definition, node instance, compiled plan, review claim, and execution run? How do duplicate extractions or implementations refer to the same underlying model?
- What must be immutable or content-addressed, and what may be a mutable alias such as "latest approved"? How are definitions and datasets pinned for a run, including external APIs whose historical response may be unavailable?
- Where do metadata, typed relationships, executable payloads, source evidence, large arrays, and run artifacts live? What query/transaction/access patterns justify files, a relational store, graph-oriented storage, object storage, or a combination? A graph-shaped product does not by itself require a graph database.
- What crosses the boundary between the registry's knowledge relationships and the execution graph's dependency edges? Are search/vector indexes disposable derivatives of a canonical store?
- How are source versions, extraction/AI authorship, transformations, reviews, licensing, and generated fallback provenance linked without silently editing old evidence?
- How are competing agent edits, duplicate proposals, publication transactions, rollback, schema migrations, and version conflicts handled? Which of these must the first single-operator build support?
- What invalidates a compiled plan or result: definition, data snapshot, calibration, executable/environment, approval policy, or model-access change? Can old runs still be inspected while newer versions are suggested?
- Which logs and artifacts are retained, redacted, exported, or deleted? What does reproducibility mean for stochastic code, hosted inference, and black-box services that cannot be exactly replayed?

## Current partial answer

Project Memory stores project design knowledge; it is not an already built model registry. The 2025 unified relational schema is provisional, not an accepted universal schema. Definition/compilation/execution separation and invalidation are lessons to preserve, not requirements to reproduce the old triggers or timestamp design. No storage technology has been selected.

## Investigation result — 2026-10-28

[[investigation-model-variable-quantity-representation]] provides a logical entity/relationship map and recommends separating semantic specifications/local symbols/value assertions, model family/revision, implementation/calibration, composition/instance/binding, experiment/run/result, and evidence/review claims. These are logical boundaries, not a table or service per concept. Pinned immutable references and independent instance contexts matter more than forcing every facet into a separate graph node.

PROV entity/activity/agent and qualified derivation provide lineage precedents; SED-ML separates experiments from models, and OMEX packages artifacts rather than establishing integrity or reproducibility ([[source-model-data-provenance-and-packaging-standards]]). Byte hashes establish integrity, not mathematical equivalence; mutable aliases must resolve to pinned versions in runs. Source/implementation changes must not inherit use approval silently.

Recommend evaluating versioned structured documents with a rebuildable index for a local trial before selecting storage infrastructure. A canonical manifest, semantic graph projection, array payload, and compiled dependency plan serve different roles; do not maintain unsynchronized canonical copies. No database, file format for bulk arrays, exact manifest schema, concurrency protocol, or reproducibility experiment is selected/performed. The report's lineage/replacement/roundtrip trials remain proposed; this question stays active.

## Concrete v0 proposal — awaiting review

[[decision-representation-contract-v0]] proposes four immutable reusable record kinds (vocabulary/model/value/composition) plus append-only review and run events. Local declarations, evidence fragments and the sole algebra payload are embedded rather than normalized into a large entity framework. Revisions are explicit opaque IDs with collision rejection, not claimed semantic hashes; run manifests retain exact content/references, evaluator build and authority heads. A local owner controls review, with compare-and-append withdrawal history; agent-supplied reviewer labels do not authenticate authority. Physical storage remains unselected. Full recompile/recompute replaces a premature cross-run cache. This is a documentation contract and fixture, not a persistence/authority implementation or reproducibility test.

## Build gate and dependencies

**B — before durable registry/run persistence.** Co-design with [[question-model-node-ast-and-schema-representation]] and runtime contracts; review/publication boundaries come from [[question-curation-evidence-and-approval]]. Before a shared registry, define concurrent-write and access behavior; federation and automatic distributed synchronization can remain excluded.

## What would resolve it?

An entity/relationship and ownership sketch, a first-build persistence rationale, version/reference rules, one saved run manifest, and lifecycle examples showing (a) a source/model update, (b) a generated fallback replaced by a curated version, and (c) an old run retaining its original lineage. Record reproducibility limits rather than promising exact replay of unavailable external services.

## Provenance

New question from the 2026-10-27 build-readiness review; separated from representation because storage ownership and lifecycle remain unresolved even with a valid node envelope.
