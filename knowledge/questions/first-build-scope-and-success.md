---
id: question-first-build-scope-and-success
type: question
title: First-Build Scope and Success Contract
summary: Provisional first-build contract with separate offline agent curation into a model repository and query-time composition/execution; inline curation forbidden or last-resort only, with exact policy open.
status: active
created: '2026-10-27'
updated: '2026-10-29'
topics:
  - strategy
  - product
  - benchmarks
confidence: null
relations:
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: question-initial-domain-beachhead
  - type: relates-to
    target: question-evaluation-and-reference-evidence
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: relates-to
    target: decision-representation-contract-v0
---

# First-Build Scope and Success Contract

## Question

What exactly should the first runnable Connected Models build let its first operator accomplish, and what evidence would justify calling that build successful?

## Decisions to answer

- Is the primary operator a human analyst, a model curator, or an external agent? Which other roles must be visible in the same workflow?
- Which offline curation and separate query-answering capabilities must the slice demonstrate? Which steps may initially be manual? Curation primarily or exclusively precedes answering; should inline curation be forbidden entirely or allowed only as an explicit last resort?
- Which existing candidate problem and small set of model classes anchor the slice? Which supported operation is required: evaluation, scenario comparison, forecasting, optimization, or counterfactual inquiry? Do not silently treat a forecast as a causal answer.
- What minimum interaction surface makes model evidence, connections, errors, and Meta-filled gaps inspectable: a tool/CLI trace, an analyst interface, or both? Is graph authoring required now, or only inspection and controlled substitution?
- What is explicitly excluded: live/private data, arbitrary code, cycles, authentication, collaboration, federation, or advanced solvers? Which exclusions would invalidate the intended demonstration?
- What are the actual time, compute, inference-cost, and latency budgets? Is the immediate target still hackathon submission, a local research prototype, or another milestone? If the event still constrains the build, what rules/access/prior-work conditions need confirmation?
- Which observable outcomes demonstrate value, and which numerical, source-fidelity, and disclosure failures block acceptance?

## Current partial answer

The universal vision, model-first assumption policy, and desired specialized curation agents are established directions. Neither hydropower nor a technology stack is selected. The end-state examples are sufficient for now; this question asks for a build boundary, not more examples. Long-term commercial domain choice belongs to [[question-initial-domain-beachhead]].

## Proposed first-build contract — awaiting agreement

### Status and objective

Recommended on 2026-10-27 at the user's request to help resolve this question. These are proposed defaults, not accepted decisions, implementation authorization, or evidence of feasibility. The question remains active. The established model-first policy and desired Meta/Muse curation are not reopened here.

**User-endorsed boundary, 2026-10-28:** Dedicated Meta/Muse agents curate models primarily or exclusively **offline**, meaning outside individual question-answering requests, not without internet access. They extract models from scientific papers, textbooks, and other sources, transform them into canonical form, extract variables/constants/parameters and provenance, and store reusable versions in the model repository. Routine on-the-fly curation is ruled out; whether it is entirely forbidden or allowed only as a last resort remains open. This boundary corrects the earlier inline-curation proposal; other scope defaults remain provisional.

**Objective:** Dedicated Meta/Muse agents first populate and maintain a reusable model repository through offline curation. Separately, a single analyst can ask bounded quantitative questions answered by retrieving and composing eligible stored models, executing the graph, inspecting sources and generated gaps, and changing a dependency to see a traced revised answer.

The first build should prove a small version of the product's complete loop, not a chatbot over a permanently hand-authored catalog, an isolated curation catalog, or a universal modeling platform.

### Recommended defaults and rationale

| Choice | Recommendation | Reason |
| --- | --- | --- |
| First operator | The project owner acting as a single analyst and reviewer; agents do the substantive discovery, formalization, composition, and interpretation work. | Makes the agent and human workbench roles inspectable without accounts/collaboration overhead. |
| Primary workflow | Offline: curate → review → store qualified versions. Query time: retrieve → connect → compile → execute → inspect → revise. | Demonstrates both capabilities without making curation part of every answer. |
| Meta's role | Offline source interpretation and canonical model extraction; query-time selection/composition, model-first resolution, permitted disclosed gap-filling, and traced explanation. | Real agent work in both modes; live curation need not occur during a user query. |
| Curation boundary | A dedicated offline job over a bounded accessible corpus of papers, textbooks, or other sources; human source selection/access checks and execution approval may be manual. Meta must canonicalize at least one source model, extracting equations, variables, constants, parameters, units, and applicability, then persist a qualified reusable version before the query phase. Recommend disabling inline curation for the first build; that recommendation does not settle the permanent no-exceptions versus last-resort policy. | Tests actual repository-building rather than citation retrieval or per-question model invention. |
| Initial catalog | A small registry; roughly 3–5 reusable model definitions is a sizing guide, not a quota. | Enough to test composition/reuse without mistaking catalog size for progress. |
| Supported computation | Deterministic algebraic models with explicit scalar/short dated-array inputs, simple reviewed transforms, and acyclic composition; one numerical execution engine. | A bounded contract can be checked against independent examples. This is not a permanent rejection of simulations or polyglot execution. |
| Supported question family | Evaluation and scenario comparison within the selected domain, including more than one compatible composition. | Demonstrates reuse beyond a single hardwired answer; excludes claims of general causal inference or global optimization. |
| Human interface | A minimal local web workbench with source/model review, read-only dependency inspection, result lineage, and scenario/substitution controls. A simple dependency list/diagram is sufficient; no drag-and-drop authoring requirement. | A human should be able to inspect the answer without reading raw logs, but visual-editor polish is not the goal. |
| Agent organization | Distinct curator, composer, and reviewer responsibilities; sequential orchestration and shared underlying model are acceptable. | Separate responsibilities do not require a parallel agent fleet or independent-evidence claims. |
| Safety/review | Only reviewed permitted execution payloads; no unattended downloaded/generated-code execution or package installation. Generated code stays a candidate until checked. | Keeps the first trust boundary tractable while retaining real agent authoring. |
| Data | Public/licensed-for-use source material and pinned fixtures/snapshots; clearly distinguish empirical evidence from synthetic acceptance cases. | Repeatable results without making live feeds or private integrations necessary. |
| Persistence | Save model versions, review/evidence references, graph/input snapshots, and run lineage locally. | Replacing a dependency must not silently rewrite earlier results. No database or storage vendor is selected here. |
| Uncertainty | Mandatory epistemic origin and validity metadata, explicit unknown uncertainty, and scenario comparisons; no universal probabilistic propagation claim. | Avoids false precision without blocking the first loop on a universal uncertainty engine. |

### Two separate workflows

**A. Offline repository curation — independent of answering a question**

1. A dedicated curator agent/job uses accessible source material to extract a model into canonical form, including equations, variable roles/meanings, constants, parameters, units, applicability, exact source locations, and AI authorship. The exact schema remains to be designed.
2. Necessary checks and review qualify a version for a declared use; it is stored in the model repository. Human source selection and approval may be manual initially. Proactive coverage and queued gaps can guide this work; an active question need not initiate it or wait for it.

**B. Query-time answering — consume existing eligible versions**

1. The analyst asks a supported question. The system searches the repository and identifies needed outputs and unresolved dependencies. It does not routinely discover or formalize new source models.
2. A composer proposes a graph from eligible versions. The compiler validates supported units, meaning/scope, preconditions, and topology; invalid proposals must be rejected or explicitly repaired, not silently accepted.
3. Missing inputs trigger model-first resolution against existing models and empirical inputs. In an intentional gap case, a permitted Meta-generated provisional parameter estimate is separately labeled with reason, origin, uncertainty status, and downstream reliance. This is not publication of a new curated model. New relationships/submodels cannot bypass the on-the-fly restriction by being called fallbacks. Unsupported gaps remain conditional/unresolved and may inform later offline curation.
4. Trusted execution evaluates the declared graph. The answer reports the result, what was calculated, data/model versions, sources, unresolved limits, and any Meta-filled dependency. It must not turn a scenario into a factual forecast.
5. The analyst changes a scenario input or substitutes a compatible upstream version. The result is rerun with a visible dependency change; the earlier run remains inspectable. A second supported question must reuse a stored component without a bespoke calculation path or repeated source curation.

### Observable success contract

All conditions below are proposed acceptance gates for the selected bounded cases, not assertions of universal reliability. Numerical oracles/tolerances and source-specific evidence must be fixed before their implementation under [[question-evaluation-and-reference-evidence]].

| Required demonstration | Acceptance evidence |
| --- | --- |
| Real offline curation | Before the query phase, a dedicated Meta curator canonicalizes at least one source model, extracts variables/constants/parameters, preserves exact source locations, and produces a checked/reviewed version stored for a declared use. A manually authored card or citation-only retrieval is insufficient. |
| Separation of curation and answering | Supported queries consume the already-stored eligible versions without repeating source curation. A missing-model case exposes the gap and can record a separate offline curation need rather than silently authoring/publishing a new model. Inline curation is disabled under the recommended first-build restriction. |
| Reusable composition | At least two supported questions/compositions reuse a model through the same model/graph contracts; the main answer depends on multiple connected model definitions. No hidden calculation path bypasses the registry/compiler. |
| Numerical execution | Every selected numerical reference case agrees with an independent reference within predeclared tolerances. A number produced twice by the same code is not an independent oracle. |
| Meaningful rejection | Predeclared invalid cases include incompatible dimensions, matching units with wrong meaning/scope, violated preconditions, and unsupported cyclic dependencies; each is rejected with an actionable reason. An unsuitable curated candidate cannot enter the eligible collection unnoticed. |
| Model-first and fallback behavior | One trace resolves a dependency through a suitable model; a separate intentional gap produces a visible Meta-generated contribution rather than a hidden default. An indefensible/private missing fact remains conditional or unresolved. |
| Honest answers | The answer follows the executed run, exposes material generated dependencies and uncertainty limits, and does not claim unsupported causal, predictive, or probabilistic certainty. Tool/inference failure is not presented as a successful answer. |
| Revision and lineage | Change an input and substitute a compatible model/version; affected results update through the declared graph while the original versions, inputs, evidence, and result remain inspectable. |
| Reproducibility and cost visibility | Fixed versions and inputs can reproduce deterministic numerical runs within declared tolerance. Hosted inference need not reproduce identical prose. Inference usage, end-to-end duration, and failed attempts are recorded; any spending limit must be enforceable before paid calls are enabled. |
| Real Meta contribution in each mode | Offline curation and query-time composition/permitted fallback run with verified Meta access in their respective phases. Stored output from a real earlier offline job is expected during answering; rerunning curation live per question is not required. Mock traces alone cannot establish either implemented capability. |

Successful acceptance establishes a functioning bounded loop, not scientific validation of every model, general reasoning superiority, or measured token/latency savings. Those broader claims remain separate hypotheses.

### Concrete representation proposal — narrower executable starting point

[[decision-representation-contract-v0]] proposes scalar-only explicit algebra for the first walking skeleton, with short dated arrays deferred unless the chosen anchor needs them. This refines rather than silently accepts the broader scalar/optional-array default above. It specifies local meanings/units, models, values, graph bindings, owner review and run lineage, plus fixtures that bootstrap deterministic execution before real offline Meta extraction. [[note-mvp-build-sequence-and-extension-triggers]] remains the delivery sequence. Review/accept the draft and run affected implementation checks before treating it as a settled contract; no model/domain/stack is selected by it.

### Explicit non-goals

No routine query-time curation (recommend none at all for the first build), public deployment, production decisions, user accounts, collaboration, social/marketplace features, arbitrary source crawling, unattended code execution, unrestricted polyglot workers, cycles/ODE/PDE solvers, live-data operation, universal ontology, general counterfactual/optimization engine, or calibrated uncertainty for all relationships. No new end-state question gallery. Existing illustrative domains do not become selected by this proposal.

Exclusions apply to this milestone only. If the chosen problem requires an excluded capability, narrow/change the problem or explicitly revisit scope; do not quietly stretch the contract.

### Choices requiring the user's input

1. **Anchor problem/domain and ownership:** Recommend using an existing problem the user can judge, with accessible quantitative sources. Intrinsic valuation is a repository-backed candidate, not a selection or assumption of the user's expertise. The user may name an existing alternative or delegate selection against these criteria. We do not need a long-term commercial beachhead now.
2. **Milestone and trade-off — answered 2026-10-29:** The user wants urgent issues resolved and an MVP built ASAP, followed by hands-on testing, adjustment, features and scaling. Hackathon submission in six days is the immediate milestone; the plan and milestone outcomes matter more than dates. [[note-mvp-build-sequence-and-extension-triggers]] now owns the active M0–M6 schedule and scope cuts. Do not ask this preference again. Exact feasibility still depends on access, anchor and resources; planned dates are targets rather than completion promises.
3. **Resources and spending:** What build-time/ongoing inference and other external spending ceiling is acceptable, and what resources/access can be relied upon? Do not assume access, authorize purchases, invent a dollar cap, or promise a latency target. Recommend local-first operation, metering, explicit stopping limits, and no unapproved provisioning; set actual numeric limits before resource-consuming integration.

The user may adjust technical/product defaults above. Workflow choice/delegation and access/spending were requested on 2026-10-29 and remain pending; the milestone preference is answered. The permanent no-inline-curation versus last-resort policy may remain open while the initial implementation disables inline curation. The active delivery plan supplies bounded technical working defaults; do not wait for universal architectural answers or claim all defaults are user-accepted. This question remains active for the unresolved scope/evidence details.

### Evidence-dependent choices, not questions of user preference

Exact Meta model/API route and credentials, library/host compatibility, final schema/storage/runtime technologies, source licensing/adequacy, reference tolerances, feasible latency, and reproducible numerical behavior require verification. Do not ask the user to choose an unresearched stack or treat their preference as technical evidence. These belong to the linked access, security, representation, registry, and evaluation questions; none were investigated or selected by this scope proposal.

## Build gate and dependencies

**A — before committing to application architecture.** Co-resolve with [[question-evaluation-and-reference-evidence]]; supported model/data/operation classes drive representation, runtime, security, and stack decisions. A paying-customer strategy and a complete universal library are not prerequisites.

## What would resolve it?

A concise accepted first-build contract naming the operator, one workflow, supported model/data/operation classes, minimum interaction surface, manually performed steps, non-goals, budgets, and pass/fail outcomes. Preserve the broader vision without making all of it a release requirement.

## Provenance

Identified from the current Project Memory and the user's 2026-10-27 request for pre-build questions. Extended at the user's request for help resolving the first-build contract, distinguishing agent recommendations from user decisions and evidence-dependent choices. The remaining scope defaults are proposed; no domain/stack is selected, and no implementation is authorized or performed by this record. On 2026-10-28, the user clarified that dedicated agent curation is primarily/exclusively offline and inline curation is forbidden or last-resort only. That accepted boundary corrects the earlier query-triggered workflow; the exact exception policy remains open.
