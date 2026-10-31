---
id: concept-specialized-model-curation-agents
type: concept
title: Specialized Model Curation Agents
summary: Dedicated Meta/Muse agents curate a canonical model repository offline from papers, textbooks, and other sources; query-time agents consume it. On-the-fly curation is forbidden or last-resort only, with the exact policy open.
status: active
created: '2026-10-27'
updated: '2026-10-31'
topics:
  - agents
  - epistemology
  - lifecycle
  - ontology
confidence: null
relations:
  - type: relates-to
    target: concept-connected-models-thesis
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: concept-agent-quantitative-reasoning-layer
  - type: addresses
    target: question-agent-interaction-patterns
  - type: addresses
    target: question-semantic-variable-disambiguation
  - type: relates-to
    target: question-model-node-ast-and-schema-representation
  - type: relates-to
    target: question-uncertainty-and-epistemic-bounds-serialization
  - type: relates-to
    target: idea-end-state-question-gallery
---

# Specialized Model Curation Agents

## Current understanding

### Implemented fleet handoff — 2026-10-31

The owner has five or more standby agents across three PCs and requested exact domain assignments and a return process. [[note-offline-curation-agent-kit]] is the operational handoff: a versioned self-contained ZIP with six assignments, source/formalization instructions, a research schema, independent numerical/rejection checks, a teaching fixture and offline validator/packer/importer. Each agent uses an isolated copy; the central integrator imports data-only returns as unapproved candidates, preserving source evidence and explicit blockers. No fleet research or new scientific coverage is claimed merely by shipping the kit.

The v1 research record can describe physical quantities beyond the current heating/finance runtime. Numerical replay alone does not certify physical dimensions, source fidelity or empirical applicability. Unsupported vocabulary/operators are retained as requires-extension candidates; unresolved interpretation is blocked. Exact current-runtime projections receive additional contract checks but still require attributed review. One canonical equation supports multiple derived solve views; curators record domain/branch caveats rather than publishing each rearrangement. Clones/worktrees are reserved for explicitly assigned code/vocabulary integration, not required for source research. General ontology, review policy and federation remain open.

Connected Models must not assume a complete registry already exists. The current knowledge base is an early seed, far from a complete account of the platform or the world's quantitative models. A central capability is therefore **specialized Meta/Muse agents that build and maintain the model collection itself**.

Curation is more than finding a paper or adding an equation to a catalog. It turns scattered quantitative knowledge into discoverable, inspectable, executable, appropriately qualified components—and maintains the evidence for when they should be used. A successful curator can conclude that a candidate is unsuitable or that no adequate model exists.

The user explicitly requested specialized Meta/Muse curation on 2026-10-27. The direction is user-endorsed; the roles, records, and workflow below are a proposed elaboration, not an implemented system or a claim about verified model/API capabilities. "Meta/Muse" names the intended agent backing, not an assumed available fleet or a fixed API contract.

Two graphs must be distinguished:
- **Project Memory now:** concepts, questions, decisions, and their typed relations record the design and its uncertainties.
- **The future model registry and computational graph:** versioned model definitions, evidence, compatibility links, and execution dependencies are product artifacts. Their implementation/schema is still unresolved. Project Memory does not itself constitute that runtime.

## Offline curation versus query-time answering — user-endorsed boundary

**Curation is primarily, and potentially exclusively, offline:** outside the process of answering an individual user question. "Offline" does not mean disconnected from the internet; curators may access scientific papers, textbooks, code, and other sources. A dedicated agent or fleet builds and maintains the repository proactively or through separate curation jobs, rather than reconstructing models whenever an answer is requested.

The two activities are:

- **Offline curation:** discover source models → transform them into a canonical representation → extract equations, variables, constants, parameters, units, assumptions, applicability, and provenance → check/review → store qualified, reusable versions in the model repository. The exact canonical schema and approval mechanism remain open.
- **Query-time answering:** retrieve eligible existing models → select and compose them → bind inputs → execute → explain the result and any gaps. Selecting, composing, or instantiating existing models is not itself new source-model curation.

A question may reveal a coverage gap and inform a separate offline curation backlog; that does not make curation a required step in the current response. **On-the-fly curation is either disallowed altogether or permitted only as an explicit last resort.** The user has not yet selected between these two policies; routine query-triggered curation is ruled out. Any permitted exception must retain provenance and satisfy the applicable checks/review, not silently become trusted repository coverage.

This boundary clarifies, rather than cancels, the earlier Meta gap-filling principle: a disclosed provisional input estimate is not the same as discovering, formalizing, and publishing a new reusable model. Generating a new relationship/submodel during answering must not bypass the eventual on-the-fly policy by being called a fallback.

## Domain specialization and curation responsibilities

Specialize along two axes: subject knowledge and curation function. A finance curator needs accounting conventions and valuation context; a hydrology curator needs basin boundaries and calibration regimes; a pharmacology curator needs populations, dosage, and evidence limitations. These are examples of future specialties, not new domain commitments.

Within a domain, agents can take the following responsibilities. They need not all be separate processes or distinct underlying models.

| Responsibility | Work | Durable output |
| --- | --- | --- |
| **Coverage editor** | Identifies missing capabilities, repeated fallback use, important broken connections, and neglected domains; prioritizes by reuse, decision impact, evidence availability, and curation cost. | Coverage map and prioritized gaps, including known absence rather than apparent completeness. |
| **Model scout** | Finds relevant scientific papers, textbooks, code, standards, spreadsheets, and existing registries; checks provenance and access/licensing; looks for duplicates and competing approaches. | Sourced candidates with reasons to pursue, defer, or reject. |
| **Domain formalizer** | Transforms source models into canonical form; extracts equations, variables, constants, parameters, units, assumptions, calibration, and applicability; distinguishes the source's claims from the agent's interpretation. | Model card and a traceable proposed definition or wrapper. |
| **Connection curator** | Finds compatible inputs/outputs; proposes semantic mappings and explicit transformations across place, time, units, and scope. | Qualified compatibility links, adapters, and explicit incompatibilities—not merely keyword matches. |
| **Reproduction and challenge reviewer** | Attempts to reproduce reference results, checks limits and counterexamples, compares alternatives, and challenges extracted claims and code. | Reproduction evidence, test results, unresolved objections, and use recommendations. |
| **Maintainer** | Tracks source revisions, new evidence, calibration drift, failures, and changed licenses; assesses affected consumers. | Versioned updates, re-review requests, deprecation notices, and replacement suggestions. |

Query-time agents consume this collection to answer questions. Dedicated offline curation agents improve it for future questions, independently of individual answer requests. Query-discovered gaps can inform later curation; they must not routinely launch inline source discovery and formalization as part of the current answer.

## What a curated model contains

A model record should make the following inspectable. This is a conceptual minimum, not a final serialization schema:

- **Identity and lineage:** stable identity, version, original author, curator/reviewer identities, source URLs or document locations, exact equation/table/code references, extraction date, and license/access restrictions.
- **Purpose and validity:** what the model represents, what it does not establish, predictive versus causal interpretation, population/geography, time horizon, calibration period, valid regimes, and known breakdown conditions.
- **Canonical model content and boundary contract:** equations/relationships, extracted variables and their input/output roles, constants and their values/units/source locations, parameters and calibration, meanings, shape, temporal/spatial scope, preconditions, internal assumptions, and unresolved dependencies. Distinguish source-defined constants from fitted parameters, observations, and scenario choices; retain the mapping from source notation to canonical form. The exact serialization remains unresolved.
- **Execution status:** mathematical description only, executable wrapper, or reproduced implementation; dependencies, numerical method, environment, reference cases, and safe execution constraints where relevant. Cataloging a model does not imply that it runs.
- **Evidence and uncertainty:** supporting and challenging evidence, validation datasets, held-out results where available, uncertainty treatment, and limitations. Missing evidence is recorded as missing, not filled with an impressive-looking confidence score.
- **Relationships:** alternative formulations, shared assumptions/data, compatible providers/consumers, adaptations, contradictions, and version/replacement lineage. A code implementation and its source paper may describe one underlying model; do not count them as independent corroboration.
- **AI contributions:** source-backed extraction, agent-proposed semantic mapping, AI-authored implementation, or Meta-generated proxy/estimate/submodel, each separately attributable. Review does not erase origin.

These fields extend the epistemic ledger in [[concept-end-state-vision]], not a separate competing catalog design.

## Proposed curation lifecycle

1. **Identify the gap.** Capture a useful unanswered quantity, unresolved input, repeated Meta fallback, missing alternative, or stale existing model. Search existing records before creating another identity.
2. **Discover and compare.** Gather plausible candidates and their original evidence, record duplicates and unsuitable matches, and preserve competing schools of thought rather than choosing a single universal winner.
3. **Formalize a candidate.** Extract its contract, source assumptions, validity, and provenance. Distinguish quoting/translation from new agent invention. A paper without runnable code can still be cataloged honestly.
4. **Prepare execution where feasible.** Wrap existing code or propose an implementation. Treat retrieved documents and code as untrusted inputs; respect licensing and use sandboxed, resource-limited execution rather than executing arbitrary downloads with project privileges.
5. **Check and challenge.** Use dimensional/semantic checks and executable tests, reference cases, conservation laws or invariants, limiting cases, and independent reproduction as appropriate. An agent's favorable opinion is not a passing test or empirical validation. A second agent using the same model and sources is not necessarily independent evidence.
6. **Review for a declared use.** Record which checks actually passed, which were blocked, dissent, and remaining risks. Apply risk-appropriate human/domain review for consequential uses. Scientific suitability, execution correctness, and connection compatibility are separate claims.
7. **Publish qualified knowledge.** Admit a discoverable version with explicit eligibility and limitations; keep unreviewed candidates distinct from approved-for-use versions. Preserve rejected/paused records and the reason. Promotion authority and thresholds remain to be designed.
8. **Maintain and revisit.** Watch revisions and observed failures. Propose new versions and affected reruns; do not silently mutate the model underlying an old result. Retain run lineage and disagreements when a recommendation changes.

There is no single "verified" badge that means all of these stages are complete. Source authority, transparency, reproducibility, applicability, and predictive/causal evidence are different dimensions. The lifecycle is a product proposal, not a replacement for Project Memory's canonical status vocabulary.

## Model selection without pretending there is one right model

A model can be good but inappropriate for a particular question. Curation should help query-time selection inspect applicability, evidence, freshness, input availability, uncertainty, computational cost, and user policy. Unit compatibility alone is insufficient ([[question-semantic-variable-disambiguation]]).

Competing models can remain side by side with explicit reasons to use each. Show divergent outcomes when they matter. Do not average incompatible models mechanically, treat shared data as independent evidence, infer causality from predictive fit, or rank truth by popularity or agent consensus. A definitive universal ranking is not required for useful curation.

## From temporary Meta fallback to reusable coverage

The model-first principle is canonical in [[concept-connected-models-thesis]]. Curation closes its improvement loop:

**Query-time:** unresolved input → search suitable existing models/empirical inputs → bind a suitable provider, use a permitted disclosed provisional fallback, or return a conditional/unresolved result → record the coverage gap.

**Separate offline curation:** prioritize gaps and proactive coverage → discover/formalize candidates → evaluate/review → publish reusable versions → offer replacement and rerun affected answers. The current response does not routinely wait for this process.

The earlier fallback proposal spans parameters, proxy relationships, distributions, and provisional submodels. It does not grant blanket permission for query-time model creation: new relationships/submodels must respect the unresolved forbidden-versus-last-resort curation policy. Keep permitted run-specific fallbacks distinct from curated repository models, with source context, model version, timestamp, reason, validity limits, and affected results. If calibrated uncertainty is unavailable, say so. Passing a schema or arithmetic check does not validate its empirical truth.

Do not promote a temporary estimate into trusted coverage because it was used often or another agent repeated it. Generated implementations of established equations still need source-fidelity and execution checks; novel generated models additionally need evidence about their real-world adequacy. A missing private measurement or irreducibly unknown quantity may remain unresolved or support only conditional results.

Example: a business query lacks a customer-switching model for a new AI market. Meta supplies a labeled provisional switching-rate estimate; the valuation discloses that dependency. A curator records the gap, looks for relevant empirical work and alternative market models, and may eventually offer a scoped, tested model. The earlier estimate and valuation remain reproducible rather than being retroactively relabeled as validated.

## Product consequences

- The library grows through dedicated offline evidence work; answering consumes that accumulated knowledge rather than routinely curating it on demand.
- Each answer can distinguish curated components from provisional AI contributions and unresolved gaps.
- Repeated queries reveal where additional curation would most improve the system; diversity of coverage matters alongside high-demand topics.
- Quality should be assessed by source fidelity, successful reproduction, valid connections, useful coverage, freshness, and known failure detection—not raw node count.
- Agents are **consumers, composers, curators, and maintainers** of quantitative knowledge. This extends the earlier consumer/assembler framing in [[concept-agent-quantitative-reasoning-layer]].

## Uncertainties and next evidence needed

No curation agents have been implemented or run as part of this work. Open design questions remain within [[question-agent-interaction-patterns]] and the representation/uncertainty questions linked above:

- Should on-the-fly curation be forbidden entirely, or allowed only as an explicit last resort? If exceptions are allowed, what eligibility, authorization, budget, review, and disclosure constraints apply?
- What may agents publish autonomously, and what requires domain review? Who can change eligibility or deprecate a version, including in federated/private deployments?
- What sufficient evidence is needed for each declared use, especially in medicine, safety, finance, or sparse-data regimes?
- How should trust/review claims, disagreement, licensing, sensitive data, and source revisions be represented without collapsing them into a misleading scalar score?
- What practical budget and stopping policy governs recursive dependency resolution, discovery, and attempted reproduction? How are domain gaps prioritized without popularity bias?
- Which roles actually benefit from separate agents, and how should contention, duplicate proposals, and correlated mistakes be handled?

A future bounded trial could first curate an existing sourced model offline, store a qualified version, and detect a deliberately unsuitable candidate; a later query would consume the stored model and expose its connections without rerunning curation. That would test the curation capability without claiming a complete library or preselecting the hackathon demonstration.

## Provenance

Developed from the user's 2026-10-27 clarification: the knowledge base is only a start; specialized Meta/Muse agents should curate models; assumptions should be resolved through suitable models first and otherwise filled explicitly by Meta. On 2026-10-28, the user clarified that dedicated agents should curate primarily or exclusively offline from sources such as scientific papers and textbooks, normalize models and extract variables/constants into a repository, with inline curation forbidden or last-resort only. This clarification replaces the earlier suggestion of routine query-triggered curation; the exact exception policy remains open. This artifact is project-created design knowledge, not external evidence of agent performance.
