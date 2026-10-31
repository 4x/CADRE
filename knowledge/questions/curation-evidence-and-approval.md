---
id: question-curation-evidence-and-approval
type: question
title: Curation Evidence, Review, and Publication Authority
summary: What evidence makes a model eligible for a stated use, who can publish or withdraw versions, and how are source fidelity, reproducibility, disagreement, licensing, and AI authorship tracked?
status: active
created: '2026-10-27'
updated: '2026-10-31'
topics:
  - agents
  - epistemology
  - lifecycle
confidence: null
relations:
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: relates-to
    target: question-agent-interaction-patterns
  - type: relates-to
    target: question-registry-storage-and-versioning
  - type: relates-to
    target: question-evaluation-and-reference-evidence
---

# Curation Evidence, Review, and Publication Authority

## Question

What evidence makes a candidate model eligible for a particular use, and who may publish, qualify, revise, or withdraw it from the shared collection?

## Decisions to answer

- What curation outcomes are distinct: sourced description, source-faithful formalization, executable implementation, reproduced reference result, empirically evaluated model, and permitted-for-use version? Which claims may an agent make automatically?
- What original evidence must be retained: document/equation locations, code versions, calibration data, extraction decisions, applicable license, and blocked access? What may be stored versus merely linked or quoted?
- How are source assumptions separated from curator interpretation, AI-written wrappers, and novel Meta-generated relationships? How is source fidelity checked when the equation is translated into code?
- What minimum checks are appropriate for each supported model/use: units, boundary cases, reference examples, held-out data, causal identification, or expert assessment? Which checks are impossible with present access, and how is that limitation represented?
- Who can publish, approve for execution, override an objection, or deprecate a version? Is initial human review mandatory, and where does review become risk/domain dependent? What prevents an authoring agent from approving its own unsupported invention?
- What counts as independent evidence when multiple agents, implementations, or papers share the same source/data? How are disagreements, negative results, competing models, and rejected candidates preserved?
- When may a temporary Meta fallback become a reusable candidate, and what additional evidence is needed before it becomes eligible? How are freshness, source retractions, and changed licenses monitored?
- How are review decisions scoped and versioned so that a later source/model change cannot inherit approval silently? How are affected consumers notified without rewriting old runs?

## Current partial answer

### Separate scientific auditor — user clarification, 2026-10-31

For incoming worker batches the owner wants the development/integration agent to check packaging, schema, field completeness and deterministic contract checks. Scientific/source-content auditing should be assigned to or designed for a separate reviewer agent. [[source-classical-mechanics-first-intake]] applies that boundary: five records pass mechanical intake, actual retrieval provenance needs completion, and no scientific approval/import was performed. Historical prototype reviews and the earlier building-energy content review remain recorded evidence; they do not override this latest role direction.

A minimal reviewer handoff is the unchanged batch/hash plus per-model ID/revision and source-access disclosures. Proposed reviewer output: reviewer identity, exact evidence retrieved, each criterion's checked/failed/not-checked status, findings/blockers, and recommendation (`recommend-admit`, `needs-revision`, or `blocked`). Criteria include source fidelity, mathematical/physical scope, dimensional semantics, independent reference provenance, guards/inverse branches and source-use provenance. This is an independently assigned review role, not a claim of independent empirical evidence. The review-report schema/tooling and actual auditor assignment remain to be implemented; no automatic publication follows a recommendation.

The integrator owns vocabulary/runtime projection and compatibility tests after suitable source review. Existing local admission commands preserve attributed decisions. New-domain research remains ineligible until both review and technical requirements are satisfied. Only intake validation should be called completed for an unreviewed returned ZIP.

### Local prototype review boundary — 2026-10-29

The earlier owner-only review default was an assistant recommendation, not an accepted permanent human-only governance requirement. Under the user's instruction to build/test autonomously, the development agent separately checked and admitted four project-derived supporting candidates and one real Muse-extracted NIST candidate for local conditional experiments, with reviewer `codex-prototype-review`. Source, symbol mapping, interpretation/limitations, declared context, algebra and independent references were inspected; the exact review notes and revision digests are preserved in the registry/run manifests. This is attributed agent technical review, not human domain-expert approval or empirical model validation. Curator/composer inference roles have no publication tools; they cannot self-admit their outputs. Local trusted review commands hold authority. The universal approval policy remains open.

The first two source candidates were not admitted: inadequate evidence and conflated out-of-scope limitations remained explicit. A revised source packet and extraction retained limitations separately from true in-scope ambiguities, with no weakening of the blocking rule for unresolved semantics. Candidate history was preserved; a numerically passing result alone did not establish source fidelity.

The user clarified on 2026-10-28 that dedicated agents curate primarily/exclusively offline: extract models from scientific papers, textbooks, and other sources into canonical form, including equations, variables, constants, parameters, and provenance, and store reusable versions in the repository. Query-time agents consume that collection. Routine inline curation is excluded; a total ban versus last-resort-only policy remains open. If an exception is permitted later, it must not bypass evidence/review requirements or automatically publish a run-specific fallback.

[[concept-specialized-model-curation-agents]] proposes roles and a lifecycle but no accepted evidence threshold, review state machine, or authority model. A runnable equation, authoritative citation, or second agent's agreement alone does not establish empirical truth. A conservative first-build review boundary may suffice without a reputation system or autonomous governance.

## Build gate and dependencies

**B — before agent-created models become eligible for shared execution.** Human-only publication can be an explicit initial restriction, not a reason to omit review provenance. Record-level authority is specified here; agent tools/orchestration are specified in [[question-agent-interaction-patterns]], storage in [[question-registry-storage-and-versioning]], and actual acceptance evidence in [[question-evaluation-and-reference-evidence]].

## What would resolve it?

An evidence checklist by declared use, permission/state-transition table, and examples of one admitted candidate, one rejected candidate, one unresolved disagreement, and one AI-generated fallback that is not automatically promoted. Include revision/retraction behavior and a statement of checks not performed.

## Provenance

Separated from the general agent-protocol question during the user's 2026-10-27 build-readiness review because qualification and publication policy need their own durable answer.
