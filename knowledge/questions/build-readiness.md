---
id: question-build-readiness
type: question
title: 'Build Readiness: Which Decisions Must Precede Implementation?'
summary: Decision map separating the minimum answers needed for a first Connected Models build from contract-level gates and later universal-platform research.
status: active
created: '2026-10-27'
updated: '2026-10-29'
topics:
  - strategy
  - architecture
confidence: null
relations:
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: relates-to
    target: question-first-build-scope-and-success
  - type: relates-to
    target: question-technology-stack-and-meta-access
  - type: relates-to
    target: question-model-node-ast-and-schema-representation
  - type: relates-to
    target: question-evaluation-and-reference-evidence
---

# Build Readiness: Which Decisions Must Precede Implementation?

## Question

Which unresolved choices genuinely block a useful first build, what minimum answers suffice, and what can remain open without locking the project into the wrong architecture?

## Current partial answer

We do not need a complete universal ontology, every execution engine, or the final business model before writing code. We do need a bounded implementation contract and explicit treatment of unsupported cases. Research spikes can help answer these questions; a speculative component is not the same as an accepted architecture.

Known: connected quantitative execution, definition/compilation/execution separation, specialized Meta/Muse curation as a desired capability, model-first resolution, and visible Meta-generated fallbacks. Retired/paused: standalone Math.js as the universal runtime and human social features. Unsettled: the first workflow, initial domain, stack, access, and the contracts below. Historical database/stack choices remain provisional; earlier hackathon plan/source records have incomplete bodies and are not sufficient evidence for current access or rules.

This is a proposed decision agenda, not a list of choices already made. It adds no new domain examples. All records remain active until evidence or an explicitly accepted scoped decision resolves the relevant part.

## Decision map

**A — Bound before committing to an application architecture.** A scoped written answer suffices; do not require a production system or every long-term answer.

| Canonical question | Minimum answer needed |
| --- | --- |
| [[question-first-build-scope-and-success]] | First operator, one end-to-end workflow, supported question/model classes, non-goals, budget, and observable success. |
| [[question-evaluation-and-reference-evidence]] | Reference evidence, tolerances, deliberate failure cases, and a release gate independent of agent self-assessment. |
| [[question-technology-stack-and-meta-access]] | Verified inference route/capabilities and a feasible local development/execution boundary; deploy only if requested later. |
| [[question-execution-security-and-access]] | Explicit trust boundary: reviewed-only code or untrusted execution, data scope, allowed tools/network, resource limits, and secret handling. |

**B — Specify before implementing the affected shared contracts.** These can be answered iteratively alongside small spikes, but cannot be left implicit in a working end-to-end slice.

| Canonical question | First-build decision required; broader research may remain open |
| --- | --- |
| [[question-model-node-ast-and-schema-representation]] | Minimum node/interface envelope, identity of definitions versus instances, supported payload kinds, and unsupported-type behavior. |
| [[question-dimensional-and-unit-type-system]] | Supported quantities/shapes, conversion rules, and explicit rejection of unsupported conversions. |
| [[question-semantic-variable-disambiguation]] | Required meaning/scope metadata and the rules for accepting, adapting, reviewing, or rejecting a binding. |
| [[question-temporal-and-spatial-data-alignment]] | Supported time/place scopes, data freshness/as-of rules, explicit transforms, and rejection policy. |
| [[question-uncertainty-and-epistemic-bounds-serialization]] | Epistemic origin and validity labels, unknown uncertainty, supported propagation, and downstream fallback disclosure. |
| [[question-graph-topology-and-feedback-cycles]] | Whether first-build graphs allow cycles and, if not, how they are detected/rejected; solver scope if permitted. |
| [[question-execution-runtime-for-heterogeneous-models]] | First engine/adapter contract, compilation and run lifecycle, errors, cancellation, invalidation, and reproducibility. |
| [[question-registry-storage-and-versioning]] | Source of truth, immutable version/run references, provenance, data snapshots, and atomic update boundaries. |
| [[question-model-discovery-and-selection]] | A bounded candidate-selection/applicability procedure and visible no-match or alternative-model outcomes. |
| [[question-assumption-resolution-and-fallback-policy]] | Search/recursion budget, fallback eligibility, disclosure, and conditional/unresolved-answer behavior. |
| [[question-curation-evidence-and-approval]] | Evidence required for declared use, review/publication authority, and separation of candidates from eligible versions. |
| [[question-agent-interaction-patterns]] | Minimum tools/state transitions, authority, retries/cancellation, and role separation actually needed. |

**C — Not universal prerequisites.** [[question-initial-domain-beachhead]] remains a strategic question, not a requirement to identify three paying customers before a technical prototype. Likewise, full federation, marketplace incentives, exhaustive ontologies, arbitrary polyglot execution, all cycle solvers, probabilistic inference across every model family, and an autonomous agent fleet can wait. For each, declare what is excluded and what extension boundary is preserved. An omission becomes a blocker only if the chosen first workflow requires it.

## Suggested resolution order and dependencies

**Delivery update, 2026-10-29:** [[note-mvp-build-sequence-and-extension-triggers]] is now the active M0–M6 build plan. The user confirmed build ASAP, test/adjust, and hackathon submission as the immediate milestone. Use this question map to resolve affected implementation contracts, not to require all 17 substantive questions to be closed before coding. Domain-neutral fixture work can proceed while workflow/access inputs are pending; real curation and composition still require actual access and source evidence.

1. Bound the first workflow and evaluation evidence together. Do not reopen the end-state question gallery as a substitute for selecting a build contract.
2. Verify Meta access and the execution/security boundary early; they can invalidate an otherwise attractive technology choice. Vendor/library comparisons are future research, not recommendations made here.
3. Co-design model contracts, types, epistemic metadata, topology, storage/versioning, and the runtime around the bounded workflow. These constrain each other; no database or universal AST is preselected.
4. Specify discovery, resolution/fallback, curation authority, and agent tools against those contracts. Make the path from a source to a qualified model to a traced answer inspectable.
5. Apply the independent acceptance cases. Record remaining exclusions and evidence gaps before declaring build readiness.

## What would resolve it?

A short build contract with linked scoped decisions, required evidence/access checks, and explicit non-goals; each A item and every B contract exercised by the first workflow has an answer or an explicit supported restriction. Larger canonical questions may remain active with a recorded first-build decision. Do not mark an entire universal question resolved because one prototype case works.

Decisions should state alternatives, rationale, evidence, scope, and reconsideration triggers in Project Memory. No architecture decisions, provider selections, external research, or implementation were performed to create this agenda.

## Provenance

Created in response to the user's 2026-10-27 request to identify and store questions needed before building. Extends the nine existing question records rather than replacing their historical context.
