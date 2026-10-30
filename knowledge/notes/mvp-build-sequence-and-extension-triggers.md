---
id: note-mvp-build-sequence-and-extension-triggers
type: note
title: MVP Delivery Plan, Milestones, and Extension Triggers
summary: Active delivery plan for a runnable core, complete offline-curation/query loop, user testing, and hackathon release; records urgent inputs, working defaults, exit gates, scope cuts, and later expansion triggers.
status: active
created: '2026-10-28'
updated: '2026-10-29'
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
  - type: relates-to
    target: question-evaluation-and-reference-evidence
  - type: relates-to
    target: question-technology-stack-and-meta-access
  - type: relates-to
    target: source-meta-hackathon-and-model-api-2026
  - type: derived-from
    target: finding-graph-compilation-caching-requirement
---

# MVP Delivery Plan, Milestones, and Extension Triggers

## Scope and status

This is the active delivery plan following the user's 2026-10-29 instruction: resolve urgent issues, build an MVP as soon as possible, test it, adjust, then add features and scale. It updates the 2026-10-28 sequencing proposal in place. The user confirmed the hackathon as the immediate milestone, six days away; milestone outcomes take precedence over optional calendar targets. Technical defaults below are agent recommendations for implementation, not falsely attributed user decisions. No application has been implemented or scalability measured.

This note owns delivery order, milestone status and scope trade-offs. [[question-first-build-scope-and-success]] owns detailed product acceptance; [[decision-representation-contract-v0]] owns the representation draft and critical review. Avoid creating parallel plans. The earlier hydropower hackathon plan remains historical/provisional input, not the selected domain or current delivery schedule.

Established: offline curation, query-time reuse, model-first resolution, explicit assumptions, and now build-first delivery with iteration before submission. Paused/retired: social features and the standalone Math.js universal runtime. Unresolved: anchor workflow, available inference access/spending, source-specific references, and implementation feasibility. Historical schema and imported solution proposals remain provisional. Event timing was rechecked on 2026-10-29; detailed submission rules and authenticated access remain unverified. No universal ontology or complete platform-design review blocks a bounded implementation.

## Immediate decision queue

| Issue | Working answer / next action | Owner and blocking boundary |
| --- | --- | --- |
| Immediate objective | Working local prototype, user exercise and fixes, then hackathon release. Resolved by the user's 2026-10-29 instruction. | Agent maintains plan; no further milestone-preference question needed. |
| Anchor workflow | User may name a workflow or delegate selection. Evaluate a small connected scenario question against accessible source equations, independent answers, reusable components and available data. Existing finance/market questions are candidates, not prescribed pipelines. | User choice/delegation pending; agent selects exact sources and models. Does not block domain-neutral fixture work. |
| Inference access and total spend | Obtain provider/access route and total ceiling without requesting secrets; verify one real structured response and record cost/latency before relying on it. No paid calls until the budget/access boundary is established. | User supplies access facts/ceiling; agent handles setup and bounded smoke test within authorization. Blocks live integration, not deterministic core. |
| Runtime and persistence | Default to one local uv-managed Python core, one numerical evaluator, serial execution, versioned serializable records and local persistence behind a small registry interface. Choose concrete packages/storage/UI in a short M1 feasibility check; do not start a broad stack survey. | Agent implementation responsibility, not a technology questionnaire for the user. |
| Executable profile | Bootstrap with explicit scalar algebra and acyclic composition. Inventory the anchor's actual operators/shapes before fixing the complete MVP profile; add only indispensable supported operations with checks. | Agent; before the affected models are implemented. |
| Representation blockers | Replace universal node-context equality with explicit per-port requirements/bindings; constrain meanings to allowed unit dimensions. Use the anchor's finite set of context relationships. | Agent revises and exercises the relevant v0 sections during M1. Do not implement the known-broken rules first. |
| Curation and execution authority | Separate candidate extraction from executable eligibility; one owner review/publication step; reviewed declarative payloads, no arbitrary generated-code execution. Disable inline model curation for this milestone. | Working default. The permanent exception policy can remain open. |
| Missing data and assumptions | Existing model/data first; explicit user scenarios or permitted, disclosed provisional estimates next; otherwise conditional/unresolved. Estimates cannot introduce unreviewed model relationships. | Agent implements bounded resolution; user controls use of generated estimates. |
| Event requirements | Check participant rules, required Meta usage, allowed prior work, final submission fields and asset limits early. Public details retrieval still exposes only Loading. | Agent checks accessible material; user supplies account-only facts if necessary. Blocks event-specific claims/submission, not core work. |

User answered on 2026-10-29: workflow selection is delegated; use Meta inference per the coding-agent documentation; total inference ceiling is $150; the user will supply the key in their own `.env`. The agent selected heating-upgrade scenario comparison under that delegation. The application now reads only META_API_KEY from its process environment; agents must not access `.env`. A user-launched uv command can populate that environment. Public configuration and a persistent budget ledger are implemented; live account access remains unverified. This is a ceiling, not a target, and other tools' spending is outside the application's ledger.

### Current execution evidence — 2026-10-29

- Selected question: under explicit assumptions, does replacing electric resistance heating with a heat pump pay off, and how does that change with performance, tariff or investment? Secondary question: compare annual operating costs using the same stored-in-code definitions and executor. Physical-to-economic composition, accessible primary references and a small independent numerical oracle motivated this choice. It does not choose the long-term vertical. Prediction-market forecasting was deferred because source/data and probabilistic validation would enlarge the first slice; company valuation remains a future candidate.
- Added a dependency-free uv-managed Python package, local demo commands, allowlisted scalar evaluator, per-port meaning/unit/context checks, topology compilation and saved run snapshots. Five manual fixture definitions form seven independent instances in the investment graph; the operating-cost composition uses five instances. The unit/meaning/context core addresses the two blocking v0 problems for this bounded fixture; it is not full v0 conformance.
- Default synthetic result: $3,600 baseline operating cost, $1,200 alternative cost, $2,400 annual savings and $8,532.16 investment NPV. Annual heat 12,000 kWh, seasonal performance 3, tariff $0.30/kWh, incremental investment $10,000, horizon ten years and annual real discount rate 5% are illustrative assumptions, not measured facts.
- Ten offline tests pass: published NIST reference, independent Decimal cash-flow sum, composition reuse, unit/meaning/context rejection, missing inputs/cycles, domain/nonfinite errors, arbitrary-code rejection, compatible revision substitution, old-run preservation, persistent budget reservations and mocked structured API output. No real API request or charge was made. Source provenance: [[source-mvp-heating-and-meta-evidence]].
- M0's delegation/budget decisions are resolved; source/reference checks exist, but authenticated access and detailed event requirements remain open. M1 has a runnable computational slice; registry loading/admission is not yet implemented, so M1 remains active rather than claiming every exit gate. M2 has not passed: real offline extraction, eligible publication, query-time agent composition and interactive inspection remain to build.

## Milestones and completion evidence

### Live loop demonstrated — 2026-10-29

The owner granted runtime-only uv loading of `.env`; no contents were inspected or displayed. Live smoke access succeeded. The initial extracted candidate exposed missing timing/price-basis evidence and remained blocked. The next candidate also remained blocked (and its intermediate packet had a section-number typo). The final packet adds NIST sections 3.3.1, 4.3.1 and 6.1.1 plus Figure 3-1, separates declared application limitations from genuinely blocking ambiguities, and uses a new immutable revision. Muse extracted `uniform-present-value@source-3` with complete source mapping, no in-scope unresolved fields and a passing published reference.

The development agent separately reviewed/admitted four manual supporting models and this extracted model under identity `codex-prototype-review`, strictly for local conditional tests; this is not human domain validation. The owner-only default was a recommendation, not an accepted requirement to pause local build/testing. Curator and composer inference roles still have no publication tools. The broader review-policy question remains active.

Three live supported queries now pass: investment, operating cost, and changed investment assumptions. All consume reviewed stored versions without repeated source curation. Default NPV $8,532.16 and changed NPV -$417.40 match independent Decimal year-by-year sums within 1e-8. A fourth query asking for a price forecast was correctly blocked rather than substituting a flat-price scenario. Exact run/candidate IDs and primary source locations are in [[source-mvp-heating-and-meta-evidence]].

A standalone HTML inspector reports requested outputs, actual graph steps, input origins, equations, sources, limitations and attributed reviews using saved evidence only. Open `.runs/report-32796605-4d48-4a0a-8dcb-89d3f90633f3.html`; opening makes no network requests. Twenty-three offline tests pass, including report escaping and the live-discovered completion/ambiguity boundaries. One failed generation is retained in spending evidence; its historical finish reason is unknown, so output-budget exhaustion is only a plausible explanation. The adapter now explicitly sets low reasoning effort and reports completion reasons before parsing content. Nine live calls total $0.100793 conservatively, all settled.

M2's bounded source-to-stored-model-to-answer/inspection/revision loop is demonstrated. M3 is now active and needs an actual user trial to assess usefulness and friction. This is not full acceptance of every earlier proposed first-build gate: generated gap estimates remain disabled pending scoped consent; UI is a standalone inspector plus CLI reruns, not a graphical authoring tool; broad empirical/predictive validity, general solver support and performance superiority remain unproven. No public deployment or submission occurred. Event-specific requirements remain a separate M0/M4 checklist item, not a blocker to local use.

### Registry increment — credential rename and evidence

Historical checkpoint before the live verification above; its credential/review blockers have now been addressed within the explicitly recorded runtime and prototype-review scope.

The user clarified that the credential variable is META_API_KEY and requested continued work until input is needed. Application code, tests and launch documentation now use that name; Meta's documented MODEL_API_KEY name remains historical source evidence only. A process-environment-only smoke check found no inherited META_API_KEY. No `.env` was read, no authenticated request was sent, and no API spend occurred. A narrow permission question is pending for runtime-only uv loading; remaining independent work was completed meanwhile.

The deterministic milestone now includes durable SQLite candidate/version/review storage, strict JSON boundaries, admission digests, withdrawal for new snapshots, pinned vocabulary and review evidence in runs, and CLI inspection. Four supporting manual candidates were staged without approval. A source packet transcribes NIST equation 3-7 using original symbols, with canonical port hints and the published numerical reference. The offline curator extracts program algebra/source mapping into a candidate; it cannot publish. Query-time composition consumes only eligible versions and supplied conditional values, cannot curate or invent numeric inputs, and preserves blocked proposals. An owner review bundle is generated under `.runs/`.

Eighteen offline tests pass, including persistence/reopen, partial candidates, independent reference recomputation (rather than trusting an agent's passed flag), immutable revisions, withdrawal, forged admission rejection, a fake extraction and two fake query compositions reusing stored versions. These are integration tests with explicitly fake inference, not live Meta evidence or scientific review. M1 is completed for the bounded deterministic/registry slice. M2 is active but not accepted: live extraction, owner admission and a live composed run are still needed; the current inspector is CLI evidence, not the planned graphical workbench. Generated input estimates are currently rejected pending a scoped consent flow.

Dates are planning targets, not elapsed-work estimates or completion promises. Rebaseline after M0 access/source checks. The organizer's public page still lists November 4, 9 PM ET (6 PM Los Angeles time) as the submission deadline; aim to have the package ready the preceding day. Evidence and limitations are recorded with each milestone rather than inferred from its date.

| Milestone | Target | Deliverable and exit gate | Dependencies / current state |
| --- | --- | --- | --- |
| M0 — Unblock the first build | Oct 29; first working session | One bounded workflow, small source/model inventory, reference cases and tolerances; access/spend facts; one verified API smoke test when authorized; event requirement checklist. Identify exactly which items remain external blockers. | Bounded live access verified; workflow, budget and source references resolved. Detailed event checks remain open. Core fixtures may start before all external checks finish. |
| M1 — Runnable deterministic core | Oct 30 | A documented local command loads versioned models/inputs, validates and executes a multi-model graph, and saves results or actionable rejection diagnostics. Independent arithmetic cases pass; wrong meaning/unit, missing inputs, domain violations and cycles are rejected. Include a mixed-context case and independent instances. | Completed for the bounded deterministic/registry slice. Eighteen offline tests pass; live inference is not part of this gate. |
| M2 — Complete product loop | Oct 31 | Real offline agent extraction from source → owner review → stored eligible version → separate query-time retrieval/composition → deterministic execution → human-readable inspection and revision. A second composition reuses a stored model without source re-extraction or executor edits. | Demonstrated for the bounded local loop with real extraction, separate technical review, live registry reuse, changed inputs and HTML inspection. Earlier broader acceptance gates remain explicitly open. |
| M3 — Kick the tires and repair | Nov 1–2 | User exercises a fresh question, changes assumptions, swaps a compatible model, inspects evidence, and encounters deliberate bad/missing input. Record friction and defects, fix release blockers, rerun affected checks and the complete loop. | Active. Agent live rehearsal passed; actual user trial and resulting issue prioritization are pending. |
| M4 — Release candidate and demo package | Nov 3 | Freeze features; reproducible setup and saved example runs; reference/negative-case checks pass; no known wrong-answer or lineage blockers; prepare walkthrough/recording and submission materials to verified rules. Label live versus recorded evidence. | Provisional, not started. Depends on M3's critical repairs and event-field verification. |
| M5 — Submit | Nov 4, with buffer | Final check of required fields/assets, approved sharing/submission action, and saved submission receipt. Until a receipt exists, submission is not complete. | Provisional, not started. Depends on M4 and participant access. Creating this plan does not itself publish or submit anything. |
| M6 — Extend from observed needs | After submission | Select the highest-value limitation revealed by use; add a model/question family through the same contracts; measure before adding infrastructure. | Provisional. Driven by the M3 issue log and later usage, not a fixed feature list. |

M1 is the first runnable prototype; M2 is the first complete MVP. Start user inspection as soon as M1 is runnable, while protecting M3 for testing the complete loop. Preserve the test/fix window if dates slip: cut breadth before consuming it.

### First implementation tickets

1. Create the uv project/package, focused tests under `tests/`, and `readme.md` setup/run instructions. Add a deterministic local entry point; preserve the repository prohibition on accessing `.env` files.
2. Implement the smallest revised model/value/composition/run records and versioned local persistence. Separate mutable drafts from immutable eligible versions and saved runs. Save rejected proposals plus diagnostics without pretending they are executable graphs.
3. Implement explicit port/context, meaning/dimension, reference/domain and topology checks; compile dependencies once and evaluate each node once per run. Recompile/recompute after changes; no cross-run cache.
4. Add independent fixtures and source-specific references, then offline extraction/review/publication against the same records. At M2, retain partial candidates and allow reviewed additive vocabulary growth without invalidating unrelated entries.
5. Add bounded query composition and a minimal local inspector: result, dependency list/diagram, sources, assumptions, error explanation, scenario controls and model substitution. Share observations across scenarios through explicit reuse bindings while preserving their original provenance.

Use one explicit sequential agent workflow initially; do not build a multi-agent orchestration framework. Inference stays behind a replaceable adapter, and the deterministic core must run without it. Agent retries, graph size, expression size, run time and API use need named configurable limits and visible failure states before the corresponding capability is enabled. Exact paid-call limits follow the approved ceiling; do not invent authorization.

## MVP acceptance and testing loop

The detailed gates remain in [[question-evaluation-and-reference-evidence]] and [[question-first-build-scope-and-success]]. Minimum release evidence:

- Real source-faithful offline extraction with exact evidence locations, variables, units and assumptions; owner review for declared use; stored versions later reused at query time.
- Multi-model computation agrees with an independent reference within declared tolerances. Tolerances and reference provenance precede implementation of the selected case.
- A second composition reuses a model; input edits and compatible substitutions create new runs while old versions/results remain inspectable.
- Wrong meaning despite matching units, wrong dimensions, invalid context/domain, missing input, unsupported cycles and malformed agent output are rejected with useful diagnostics. Inference failures cannot be reported as successful answers.
- Model-first resolution is demonstrated; a permitted provisional parameter estimate is visibly labeled with downstream reliance; an unsuitable gap remains conditional/unresolved. Source-reported uncertainty is retained even if not propagated.
- Results distinguish calculation, scenario assumptions and empirical claims. Record inference usage, failures and timing separately for curation and answering; make no unmeasured reliability/token-saving claims.

During M3, record each issue with reproduction, expected/actual behavior, severity, disposition and retest evidence. Wrong answers, invalid accepted bindings, lost provenance, unsafe execution and inability to complete the supported loop block release. Confusing UI and recoverable rough edges are prioritized by whether the user can perform that loop; cosmetic enhancements go to M6. A small regression case should accompany a substantive correctness fix, not every reversible text/style change.

## Scope control and contingencies

- If an anchor needs inaccessible data or an unsupported solver, first narrow to a useful scenario with pinned inputs; otherwise choose another source-backed workflow with the user or under delegated selection. Never disguise a fixture or scenario as a real forecast.
- If API access is delayed, complete M1 and prepare the same adapter boundary with explicit test doubles. M2 stays incomplete until real curation and composition execute; preserve this distinction in any recording.
- If behind schedule, cut extra models, extra question families, live feeds, automatic source discovery, graph-editor polish and nonessential visualizations. Keep one complete workflow, reuse, source evidence, checks and revisions.
- If the core loop is incomplete near freeze, stop adding features and repair it. Report the gap honestly rather than relabeling a deterministic-only demo as the complete MVP.
- Keep public hosting, accounts, collaboration, distributed workers, arbitrary code, general uncertainty propagation, universal ontology, advanced solvers, social features and marketplace work outside this release unless a verified essential requirement forces explicit reprioritization.
- No broad comparative research, new question gallery or full representation rewrite is a prerequisite. Resolve technical choices with the smallest relevant spike and move to implementation.

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

## Sequence rationale retained from the initial proposal

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

Originally derived from repository state and the existing first-build contract on 2026-10-28. Updated on 2026-10-29 at the user's request into the active delivery plan, incorporating the representation critical review and confirmed build-first/hackathon priority. The schedule recheck is recorded in [[source-meta-hackathon-and-model-api-2026]]; no external technology comparison, live inference or application test was performed. Milestone targets and technical working defaults are assistant recommendations, not completed work or blanket acceptance of the v0 schema. Linked universal questions remain open.
