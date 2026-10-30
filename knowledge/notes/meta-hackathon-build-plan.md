---
id: note-meta-hackathon-build-plan
type: note
title: 'Connected Models: Meta Hackathon Build Plan'
summary: Proposed ten-day build of a Meta-assisted, typed water-to-energy-to-investment graph, with deterministic execution, traceability, evaluation, scope cuts, and rule-verification gates.
status: provisional
created: '2026-10-26'
updated: '2026-10-26'
topics:
  - strategy
  - architecture
  - benchmarks
confidence: medium
relations:
  - type: derived-from
    target: concept-end-state-vision
  - type: derived-from
    target: concept-agent-quantitative-reasoning-layer
  - type: derived-from
    target: finding-graph-compilation-caching-requirement
  - type: addresses
    target: question-initial-domain-beachhead
  - type: addresses
    target: question-model-node-ast-and-schema-representation
  - type: addresses
    target: question-semantic-variable-disambiguation
  - type: addresses
    target: question-agent-interaction-patterns
  - type: relates-to
    target: question-execution-runtime-for-heterogeneous-models
  - type: relates-to
    target: hypothesis-graph-grounded-agent-reliability
  - type: relates-to
    target: source-meta-hackathon-and-model-api-2026
  - type: relates-to
    target: source-hydropower-investment-demo-reference
---

# Connected Models: Meta Hackathon Build Plan

## 0. Recommendation in one minute

**Build a Meta-assisted quantitative workbench, not a universal modeling platform.** Its first demonstration answers:

> Should a processing plant upgrade its on-site hydropower turbine, and under which water, electricity-cost, and investment assumptions is that upgrade worthwhile?

The user asks a question. A Meta model selects and connects trusted model components, identifies missing assumptions, and proposes a graph. A deterministic compiler checks the connections. A server-side runtime computes water availability → electrical generation → avoided grid purchases → incremental cash flow → investment NPV. The interface reveals every equation, input, source, assumption, and downstream change. The assistant explains only results tied to that execution trace.

**Primary theme: Push the Frontier.** Give an AI agent a new capability: assembling and interrogating a typed, executable model of a physical-to-economic system. This is decision support, not autonomous turbine control and not a validated digital twin. **Alternative framing: Build for Your World** if the builder can substantiate firsthand modeling/financial-analysis experience. Do not invent personal experience with hydro operations.

**Pitch:** “AI can explain a decision. Connected Models lets it show and rerun the model behind that decision.”

Success at the hackathon is one useful, inspectable, working vertical slice. The long-term platform remains the destination, not the ten-day deliverable. This is a proposed direction, not an accepted commercial beachhead or a claim that the system is already implemented.

## 1. What the repository actually says

### 1.1 Materials studied

All substantive project Markdown was read: the current state and configuration; four legacy documents; four concepts; three decisions; the prototype investigation and compilation finding; two hypotheses; three ideas; and all nine open questions. There is no current application source, package manifest, lockfile, deployed service, benchmark implementation, or test suite in this checkout. The React/Supabase/Math.js system exists here as historical documentation, not reusable source code.

### 1.2 Already known and worth preserving

- The thesis is composition across domain boundaries: one model's assumption can become another model's explicit output, with traceable provenance ([[concept-connected-models-thesis]]).
- The end state combines an analyst workbench, epistemic ledger, and heterogeneous execution layer, with Query, Author, and Stress-Test workflows ([[concept-end-state-vision]]).
- The physical-to-financial cascade is already part of the vision. The proposed hydro example compresses it; it does not introduce an unrelated product.
- Agents are intended both to consume and assemble models, with deterministic execution outside the language model ([[concept-agent-quantitative-reasoning-layer]]).
- The 2025 prototype established hierarchical composition and the importance of separating definition, compilation, and execution. Reuse those lessons, not its entire database design ([[investigation-prototype-2025-mathjs-supabase]], [[finding-graph-compilation-caching-requirement]]).
- DuPont and intrinsic valuation remain valuable small regression/ontology examples. FX is preserved for later research, not a second hackathon product.

### 1.3 Previously rejected or paused

- Do not restore standalone browser Math.js as the universal execution engine ([[decision-retire-standalone-mathjs-implementation]]).
- Do not spend the event on public profiles, stars, comments, feeds, voting, model royalties, or a marketplace ([[decision-deprecate-human-social-features-priority]]).
- Do not silently promote the prototype's unified relational table into a universal ontology ([[decision-unify-equations-and-graphs]]).

### 1.4 Unresolved

The universal AST, unit ontology, semantic equivalence policy, temporal/spatial alignment, uncertainty format, cycles, distributed runtime, agent protocol, and commercial beachhead are still open. The hackathon should test bounded answers, not claim to resolve these globally.

### 1.5 Possibly stale or overstrong

- Historical stack choices and implementation limits are evidence about that prototype, not a current audit of all capabilities of Math.js or Supabase.
- “Eliminates hallucinations,” “100% reliability,” “60% fewer tokens,” and “50% fewer turns” are unmeasured hypotheses, not product facts. Correct arithmetic cannot repair a wrong model, mistaken source, bad binding, software bug, or misleading explanation.
- Zero-ETL interoperability and fully automated verification remain aspirations. A curated registry proves a bounded mechanism, not arbitrary cross-domain compatibility.
- This plan's dates, model IDs, API behavior, judging information, and access assumptions must be rechecked at implementation time.

**Delta addressed:** turn the knowledge base into an executable, measurable, hackathon-sized experiment, with a concrete decision, model contract, runtime boundary, and demo story.

## 2. Hackathon alignment and rules gates

Evidence and retrieval limitations are recorded in [[source-meta-hackathon-and-model-api-2026]]. The official landing page was readable; the requested official details page returned only “Loading…” through text retrieval. Do not treat missing extracted text as evidence that a rule does not exist.

### 2.1 Confirmed on the official landing page, retrieved October 26

- Virtual build dates: October 26–November 4, 2026.
- Submission deadline: **November 4, 2026, 9:00 PM ET** (November 5, 02:00 UTC, subject to organizer changes).
- Judging: November 4–8; closing ceremony/live finals November 9.
- Applications closed October 25, 11:59 PM ET, or sooner at the participant cap. Participation requires selection; this plan assumes the builder is already accepted and does not imply eligibility.
- Themes: Build for Your World and Push the Frontier.
- Indie lens: creativity, technical ambition, and whether it works. Startup lens: technical execution and whether it holds up in production.
- The page names Muse Spark, Muse Wonder, Muse Image, SAM 3.1, Meta open-weight models, and Muse Code. **Do not assume Llama is the required model.**

### 2.2 Provisional judging map: weights are secondary-only

A secondary guide reports the following weights from an event waiver. The inaccessible primary details/waiver text was not independently verified. Use this as a provisional planning aid, **not official confirmation**. The landing page's equally weighted application criteria are a different rubric.

| Reported project criterion | Reported weight | Evidence we should show |
| --- | ---: | --- |
| Impact | 30% | A concrete operator decision; user feedback; assumptions that change the conclusion; a reusable workflow beyond one hard-coded calculator. |
| Use of Meta AI Tooling | 25% | A visible Meta model proposes a graph, resolves missing inputs, reacts to typed validation errors, and explains results. Not just a chat box or coding-tool usage. |
| Demo | 25% | A reliable live path and recorded demonstration: ask → compile → execute → inspect → change → rerun. |
| Technical Depth and Execution | 20% | Typed semantic boundaries, explicit compiler, two trusted adapters if completed, revision-aware invalidation, provenance, adversarial fixtures, honest benchmarks. |

### 2.3 First-session rule checklist — must confirm, not guess

1. Confirm acceptance, track, team membership/size, and eligibility in the actual participant materials. Recommend Indie unless a genuine startup/team and its eligibility support the Startup track.
2. Obtain the official rules, exact judging text, submission fields, video length/format, repository/demo-access requirements, and public-access expectations.
3. Ask organizers how prior concepts, prior code, and pre-event planning may be reused. Keep the existing history intact and a clear baseline separating 2020/2025 ideas, this plan, and new event implementation. Do not assume that pre-existing work is permitted or prohibited.
4. Verify Meta API credit/access conditions, allowed model versions, data policies, any external-model restrictions, and licenses.
5. Confirm whether public posting, voting, repositories, or promotion are permitted and when. Never expose confidential information or create unauthorized publicity.
6. Check the bonus section directly. Secondary reporting mentions a **bonus pool up to $50,000**, possibly community-vote/viral-project awards; exact categories, amounts, qualification, and timing are **unconfirmed**. Do not invent a SAM, multimodal, open-source, or model-specific bonus.

If official information differs, amend this plan before building around an eligibility or submission assumption. If acceptance is missing, the build can still be useful, but cannot be represented as an eligible contest entry.

### 2.4 Bonus strategy without scope distortion

Make the core demo easy to understand and share: a short lawful recording of an assumption changing a real computed decision, an inspectable graph, and an honest limitations card. Only pursue an award after its official requirements are confirmed. No vote manipulation, paid engagement, unsolicited posting, or extra model integrations merely to chase an unspecified bonus. The event deadline, not virality, controls engineering priority.

## 3. Why this wedge, and what would change it

| Candidate | Strength | Main hackathon liability | Treatment |
| --- | --- | --- | --- |
| Full hydrology → crops/grid → factory → equity valuation | Closest to mature flagship vision | Too many scientific assumptions, datasets, engines, and causal links to validate in ten days | Defer. |
| Hydro upgrade → self-consumption → incremental NPV | Short physical-to-economic chain; clear formulas and falsifiable constraints; useful graph semantics | Needs truthful synthetic-data labels and practitioner feedback | **Recommended demonstration.** |
| Intrinsic equity valuation | Strongest legacy modeling detail and likely builder familiarity | Easy to look like a generic finance assistant; finance-specific data and accounting ambiguity | First-session fallback only if domain credibility or source availability blocks hydro. |
| FX/prediction markets | Potential commercial value | Predictive truth and profitability cannot be shown by a short demo; market data scope | Defer. |
| Universal model marketplace | Big vision | Cold-start, governance, sharing, payments, and ontology scope swamp the engine | Exclude. |

**Person and job:** an energy/operations analyst evaluating whether an existing small run-of-river installation should improve electrical efficiency to offset a plant's grid purchases. It is not a proposal to build a new dam or change permitted water operations.

**Value to validate:** reduced manual reconciliation between physical-output calculations, load matching, and investment spreadsheets, with a reusable audit trail and quick assumption changes. Dollar savings and time savings are not yet measured.

**First-session decision gate (maximum four hours):** confirm the narrative with the builder and, if reachable, an energy/operations practitioner. If no firsthand hydro relevance can be honestly claimed, use Push the Frontier without inventing a customer story. If even the simplified physics cannot be responsibly explained, switch to one intrinsic-valuation example using the same contract/compiler approach; do not build both products.

The fallback is a tightly scoped CAPM + FCFE/DCF case with explicit cash-flow horizon, equity-vs-firm boundaries, and growth/discount-rate validity checks, not a full valuation research platform. Hydro remains the concrete plan below until that gate changes it.

## 4. Demo product and non-goals

### 4.1 End-to-end story

1. Ask: “With this flow profile, should we pay $80,000 to improve total electrical efficiency from 60% to 80%?”
2. Meta proposes a graph from a small registry. The UI shows required inputs and explicitly asks for any missing value, such as net head or discount rate.
3. The user reviews the assumptions and approves the proposed scenario. No invented site measurements or hidden defaults.
4. The compiler validates IDs, units, semantic roles, time alignment, domain checks, and acyclicity. A displayed valid graph is not a certificate that the physical model is true.
5. Execute baseline and upgrade, display intermediate values, avoided energy, annual savings, NPV, and break-even capex.
6. Inspect a node to see its formula, trusted implementation revision, source reference, input origin, and limitations.
7. Change tariff or water-flow multiplier. Reuse the compiled structure; invalidate affected result nodes and recalculate. Highlight the affected chain and show numerical deltas.
8. Ask “Why did that change?” The assistant cites computed result references and states omitted factors.
9. Demonstrate a deliberately invalid edge, explicitly labeled as a test: kW → kWh without integration, or gross flow → turbine-available flow without an allocation step. The compiler rejects it even if the model's text sounds confident.

### 4.2 Required product surface

One workbench, not a multi-page platform:

- **Question/scenario panel:** prompt, required input review, explicit assumptions, baseline/upgraded configuration, live/replay status.
- **Graph panel:** fixed-layout nodes and edges, execution status, selected node inspector, error highlighting. A read-only SVG graph is enough; no drag-and-drop editor required.
- **Decision panel:** baseline vs upgrade, incremental NPV, break-even capex, annual avoided purchases, sensitivity range labeled as scenarios, limitations and provenance.
- **Run inspector:** compact actual model/tool events and deterministic execution steps. Do not expose or fabricate hidden chain-of-thought.

Query = ask and execute; Author = Meta proposes bindings among trusted components and the user approves; Stress-Test = rerun selected scenarios. These are deliberately small instances of the end-state lifecycle.

### 4.3 Explicit exclusions

No arbitrary user code or arbitrary formula execution; no full universal AST; no dynamic ontology generation; no recursive nested graph authoring; no feedback-cycle solvers; no ODE/PDE simulation; no reservoir scheduling; no hydrological or electricity-price forecasting; no live sensors; no remote turbine control; no scientific claim of calibrated forecasting accuracy; no optimization over water rights; no probabilistic confidence claims without distributions; no market data feed; no share marketplace/social features; no royalties/payments; no auth/multitenancy; no fine-tuning; no model zoo; no multimodal ingestion unless the core is finished and it solves a demonstrated need.

A trusted numerical time-profile adapter plus algebraic finance adapter is enough to test heterogeneous execution. It does not establish support for arbitrary scientific software.

## 5. Reference computation and an honest worked example

Sources and limitations: [[source-hydropower-investment-demo-reference]]. Use a small, explicitly **synthetic** profile for the default demo. Source citations justify formulas, not the reality of the example's input values.

### 5.1 Scope and equations

For each aligned time block i of duration h_i hours:

- Q_available_i = max(0, Q_river_i − Q_bypass_i).
- Q_turbine_i = min(Q_available_i, Q_design).
- P_electric_i [kW] = min(P_installed, 9.81 × Q_turbine_i [m³/s] × H_net [m] × eta_total).
- P_offset_i [kW] = min(P_electric_i, P_load_i).
- E_offset_year [kWh] = sum(P_offset_i × h_i).
- DeltaE = E_offset_upgrade − E_offset_baseline.
- Annual incremental CF [USD/year] = DeltaE × tariff [USD/kWh] − incremental O&M [USD/year].
- NPV [USD] = −capex + sum(CF_year_y / (1+r)^y), y=1…N, with capex at time zero and cash flow at each year end.
- Break-even capex = present value of future incremental cash flows (before initial capex). This can be computed directly for fixed operation assumptions; no optimizer is needed.

The 9.81 factor assumes water density approximately 1,000 kg/m³ and conversion from W to kW. H is **net** head: do not subtract head losses twice. eta_total includes turbine/drive/generator losses. A bypass subtraction is an explicit assumed layout/policy for this example, not a universal environmental-flow law. Required downstream flow may run through the turbine at a different site.

Start with a year represented by four equal-duration blocks; arbitrary aligned non-overlapping blocks can use the same contract. For repeat annual cash flows, explicitly state that the same profile, tariff, efficiency, and O&M are repeated over the evaluation horizon. No implicit year-to-year drought trend.

### 5.2 Domain and alignment rules

Require nonnegative flows, head, capacity, duration, demand, capex, and tariff in the supported scenario; eta in (0,1]; a bounded positive integer horizon; a declared finite annual discount rate (the demo may restrict it to 0–50%); finite numbers everywhere. Negative-tariff markets and unusual financing cases are unsupported, not silently clamped.

No below-cut-in turbine behavior is modeled by default beyond zero available flow. Show this as a limitation; an explicitly supplied cut-in threshold can be a later trusted parameter. Constant efficiency and constant net head are simplifications. Capacity, load, and durations are applied before aggregation, not to annual averages.

Use a single site ID, single electricity boundary, one analysis year, one currency (USD), and matching arrays/block IDs. Declare cash flows and discount rate consistently as real constant-dollar or nominal. Default to constant-dollar cash flows and a user-approved real discount rate. Reject real/nominal or currency mismatches; do not auto-convert them.

Exclude export credits, demand charges, taxes, debt financing, grants, downtime, replacement, degradation, inflation/escalation, salvage, changing head, and efficiency curves unless explicitly implemented. Therefore this is a screening calculation, not engineering or investment advice.

### 5.3 Sanity-checked synthetic fixture

| Input | Synthetic value |
| --- | --- |
| River-flow blocks | 0.3, 0.5, 0.8, 1.1 m³/s |
| Duration | 2,190 hours each; total 8,760 hours |
| Assumed bypass | 0.1 m³/s each block |
| Design turbine flow | 1.0 m³/s |
| Net head | 20 m |
| Baseline / upgraded total electrical efficiency | 0.60 / 0.80 |
| Installed electrical capacity, both cases | 150 kW |
| Constant on-site load | 100 kW |
| Flat avoided-purchase tariff | $0.15/kWh |
| Upgrade capex / incremental annual O&M | $80,000 / $500 |
| Evaluation horizon / annual real discount rate | 10 years / 8% |

Independent scratch calculation during planning (not a test of application software):

- Baseline electrical power: 23.544, 47.088, 82.404, 117.720 kW.
- Upgrade electrical power after generator cap: 31.392, 62.784, 109.872, 150.000 kW.
- Baseline avoided grid purchases: **554,148.84 kWh/year**.
- Upgrade avoided grid purchases after 100 kW load clipping: **644,245.44 kWh/year**.
- Incremental avoided purchases: **90,096.60 kWh/year**.
- Incremental annual net cash flow: **$13,014.49**.
- NPV: **+$7,328.29**; break-even capex: **$87,328.29**.
- Change only tariff to $0.12/kWh: **NPV −$10,808.38**, flipping the screening conclusion.

**Non-obvious result:** multiplying river flow by 0.8 gives upgrade NPV approximately **+$19,437.62**, not less than the base case. Both configurations lose total generation, but baseline and upgrade interact differently with load clipping. Incremental upgrade benefit need not be monotone in river flow. Do not script the assistant to say “drought always lowers upgrade ROI.” Test actual numbers and explain the boundary effects.

Golden tests must use a separately reviewed oracle (for example a small hand-checked spreadsheet or independently written reference), not simply call the production implementation and compare it with itself. These planning numbers are starting fixtures, not scientific validation.

## 6. Architecture: smallest credible spine

### 6.1 Proposed stack, not existing dependencies

The checkout has no implementation stack to preserve. Recommended new-build choices:

- React + TypeScript + Vite for one browser workbench, drawing the bounded graph with SVG and rendering results with simple tables/plots.
- A small Python API/orchestrator, with typed request/response validation (for example FastAPI/Pydantic, to be pinned and checked during implementation).
- Python trusted physical/time-profile functions using ordinary numeric arrays; no heavy solver dependency for this model.
- A trusted TypeScript finance adapter compiled to JavaScript and invoked by a fixed Node command over JSON stdin/stdout. Execute the entire finance stage or scenario batch per invocation, not a subprocess for every arithmetic operation.
- Version-controlled JSON model descriptors and fixtures; local run artifacts for reproducibility. No hosted database required for the hackathon.
- Meta Model API accessed server-side through one small adapter, using its documented HTTP API or compatible SDK after verifying current versions. Keep the key out of browser bundles, logs, repository, and exported runs.
- Python tests for compiler/runtime; a small cross-adapter contract/fixture check. Add tools only where justified, not a framework for every layer.

A single Python runtime is the fallback if the second adapter threatens delivery. In that case explicitly withdraw the “two-backend execution demonstrated” claim. Do not swap in a second backend just for a logo. The boundary is useful because it tests serialized typed composition across languages, a real open project question.

### 6.2 Data flow

```text
User question + reviewed scenario data
                 |
                 v
Meta model proposes bounded GraphProposal / asks a clarification
                 |
                 v
Server validates proposal -> compiler -> immutable Plan ID
                 |                     \-> typed error / bounded repair
                 v
Python physical adapter -> typed series/aggregation -> JS finance adapter
                 |
                 v
Run result + node trace + source/assumption references
                 |
                 v
Deterministic result UI + Meta explanation with result references
```

Keep graph definition, compiled plan, concrete scenario, execution result, and natural-language explanation as distinct records. Do not store the model's prose as the canonical computation.

### 6.3 Bounded registry: approximately seven model components

1. Available-flow allocation (river flow + explicit bypass policy).
2. Hydropower electrical output (net head, turbine flow cap, eta, installed capacity).
3. On-site load matching (clipping electrical generation against demand).
4. Explicit power-to-energy aggregation (kW × block hours → annual kWh).
5. Baseline-vs-upgrade energy difference.
6. Avoided-cost and incremental cash-flow calculation.
7. Discounted-cash-flow / NPV and break-even capex.

Baseline and upgrade reuse the same descriptors with different reviewed efficiency inputs. Do not duplicate a second registry for the upgrade. Add distractor ports such as gross flow, gross mechanical power, unintegrated kW, and nominal cash flows to test invalid bindings. Keep legacy DuPont as a later small contract regression, not a second full UI.

## 7. Contract, compilation, and invalidation

### 7.1 Model interface envelope

A model descriptor declares:

| Field | Purpose |
| --- | --- |
| id, version, implementation_digest | Stable identity and exact executable revision. |
| title, description, transparency | Human-readable purpose; all demo modules are inspectable/white-box. |
| inputs / outputs | Port IDs, numeric kind, shape, dimensions, units, semantic contract. |
| semantic contract | Quantity/concept, site/entity, boundary, time basis/block IDs, aggregation, currency and price basis where relevant. |
| preconditions | Trusted named rules plus typed parameters, not executable model-generated strings. |
| execution | Allowlisted engine and function ID; no model-provided command, source code, URL, or file path. |
| references / assumptions / limitations | Formula source, applicable domain, explicit simplifications, and calibration status. |

Graph definitions are bounded flat arrays of node instances and edges. Keep ModelDescriptor and GraphDefinition distinct: shared contracts do not force equations, datasets, and composites into the same database table. Do not design a universal mathematical AST before the first working graph.

Example port distinction:

```json
{
  "port_id": "electric_power",
  "kind": "number",
  "shape": "block-series",
  "dimension": "power",
  "unit": "kW",
  "semantic": {
    "concept": "net-electrical-output",
    "entity": "demo-site-1",
    "boundary": "plant-meter",
    "time_basis": "analysis-year-blocks"
  }
}
```

An input expecting annual energy cannot accept this port until the explicit integration adapter is inserted. Matching physical dimensions alone is insufficient: gross mechanical power and net electrical power can both be kW, but are not interchangeable. Similarly gross river flow and turbine-available flow share m³/s but have different meanings.

### 7.2 Input provenance types

Every scenario value has a declared origin: user-provided, explicit demo assumption, or sourced observation. Store unit, source ID/locator if any, observation date/time if relevant, entity/time boundary, and review state. Unknown must remain unknown. Source citations for equations must not turn fictional flow data into “measured” data. Mark outputs as computed, not observed.

### 7.3 Compiler pipeline

1. Validate finite bounded JSON; reject unknown fields where appropriate. Initial limits: 30 node instances, 60 edges, 100 time blocks, 100 scenario variants, fixed response-size budget.
2. Resolve versioned descriptor IDs from the registry; reject unknown modules/ports and unsupported revisions.
3. Validate unique instance IDs, edge references, input completeness, single bindings, and required graph outputs.
4. Check numeric kinds, array lengths, block identity, site identity, time basis, and currency/price basis.
5. Validate dimensions and units. Permit only a small reviewed conversion list (e.g., W↔kW, kWh↔MWh, fraction↔explicit percent representation). Never treat kW↔kWh, USD↔EUR, or nominal↔real as plain unit conversions.
6. Check semantic concepts/boundaries by explicit equality/allowlisted relation. Require a named transformation node for meaningful changes. No LLM override of hard incompatibilities.
7. Detect cycles and reject with a diagnostic path. Outer graph is a DAG for this experiment; internal time-block computations do not require graph cycles.
8. Topologically order the DAG, resolve external inputs and named outputs, and generate an immutable execution plan with a content digest.
9. Check static constraints now and value-dependent domain constraints again at execution. A graph may type-check yet fail with a negative scenario input; do not pretend compile time knows all future values.

Expected compiler structure is O(V+E) traversal plus descriptor/type checks for the bounded graph. Measure actual times before claiming any speed or scaling result.

Errors are data: `UNKNOWN_MODEL`, `MISSING_INPUT`, `UNIT_MISMATCH`, `SEMANTIC_MISMATCH`, `TIME_ALIGNMENT`, `PRICE_BASIS_MISMATCH`, `CYCLE`, `DOMAIN_VIOLATION`, `STALE_PLAN`, `ADAPTER_FAILURE`. Include node/port, expected/actual, and allowed remedy. The error must not leak secrets or raw system details.

### 7.4 Revisions and two separate cache layers

Preserve the 2025 lesson of explicit compilation and dirty-state tracking, without requiring PostgreSQL triggers in the new build:

- **Plan cache:** graph structure + descriptor/interface revisions + compiler/unit-policy version. An implementation revision is pinned and must be checked before executing its plan.
- **Result cache:** plan ID + node implementation revision + upstream result identities + canonical concrete inputs + adapter version. Include all meaningful configuration; avoid stale results from hidden globals.
- Changing a descriptor/edge/implementation invalidates dependent plans/results as appropriate. An old plan must never silently run new code.
- Changing tariff affects only downstream monetary nodes; changing a flow profile affects physical nodes and their dependents. Reuse graph compilation for pure value changes but re-run domain checks.
- For the event, invalidating all results for a run is an acceptable delivery fallback. Mark selective recomputation as incomplete rather than faking unchanged nodes as cached.
- Keep calculation identity separate from provenance identity. If a source's provenance changes without a numerical change, refresh the audit envelope even if a numeric result can be reused.

Each run records run ID, graph/plan digest, exact input snapshot, component revisions, executed/cached status, warnings, relevant formula/source references, adapter versions, and timing. Cache hits are an optimization, not validation.

## 8. Meta integration: substantial, constrained, and observable

### 8.1 Model/access choice

The official event explicitly features Meta Model API. Current fetched Meta docs recommend **Muse Spark 1.3 (`muse-spark-1.3`)** for new work; choose it only after verifying the participant account's enabled model list and event rules. Use one capable model, not several parallel personas. Muse Wonder is an optional later comparison, not a dependency.

A service-discovery lookup was performed for direct Meta inference; the catalog returned no supported recommendation. Therefore no catalog provider, credentials, or access is assumed. The official Meta docs, not an invented provider setup, support this proposed route. If direct access is blocked, verify an organizer-approved Meta open-weight endpoint and its exact tool/schema support before selecting it. No silent non-Meta substitution for a live demo. Self-hosting a huge model is not the default ten-day path.

### 8.2 First integration spike

Using a server-side local secret, verify one authenticated model-list request and a minimal schema-shaped response. Then verify one harmless tool round-trip and result return. Record actual accepted endpoint parameters/model ID. No credentials were requested or configured while writing this plan.

Meta's current documentation makes important distinctions:

- Structured outputs can constrain a supported JSON Schema; this is shape enforcement, not scientific or semantic correctness.
- Recursive JSON Schemas are unsupported; use flat node/edge arrays.
- Function-tool arguments are **not guaranteed to satisfy the schema**, even when a tool has `strict: true`; validate in application code.
- `tool_choice` currently supports only `auto`; do not design a flow that requires the API to honor `required` or a named function choice.
- Responses uses `text.format`, while Chat Completions uses `response_format`. Do not mix endpoint parameter shapes.

### 8.3 Minimum useful agent protocol

Use an application-owned state machine rather than open-ended agent autonomy:

1. **Discover:** supply the small trusted registry and supported question types directly; a vector database is unnecessary.
2. **Propose:** request a schema-shaped object with status (`needs_input`, `proposal`, `unsupported`), node/edge arrays, parameter references, required clarifications, and declared assumptions. No executable strings or novel model IDs.
3. **Validate:** the server compiles the proposal. Allow at most two model repair attempts with typed diagnostics; never weaken the compiler to accommodate the proposal.
4. **Approve:** require user review for missing-value assumptions and graph/scenario changes. Read-only evaluation, not a real-world action.
5. **Execute:** the application invokes validated tools only when it has a valid plan and approved values. Optional model tools such as `compile_graph`, `run_graph`, or `compare_scenarios` use validated IDs and bounded parameters. A plain-text model response without a tool call cannot become an unverified numerical answer.
6. **Explain:** provide a compact run summary and ask for explanation sections linked to result IDs. Numeric cards, units, deltas, and final decision thresholds are rendered from runtime data, not copied from generated prose.
7. **Follow up:** natural language changes become typed scenario patches, not silent edits to source data or model implementation.

If tool-choice auto declines a needed call, the UI says calculation has not run or the application advances its approved deterministic execution step. Do not display a textual estimate as a computed answer. If the API does not support the desired schema/tool combination, split proposal and explanation requests and retain the same validation boundary.

### 8.4 Claim and failure controls

Require explanation claims to reference actual run/node/output IDs. Render numerical claim values from those references. Treat free prose as interpretation; reject unsupported result references and flag claims inconsistent with the run. This reduces unchecked numerical copying but cannot certify every causal statement.

Set per-session limits: two repairs, bounded request time, finite output budget, and capped scenario count; tune token limits after the access spike. Retry transient transport/rate-limit failures with bounded backoff, not endless retries or re-execution of side effects. Escape labels/text, never execute model code, and treat source text as untrusted data.

Use visible modes: **Live Meta**, **Recorded Meta replay**, and **Deterministic-only**. A recording or cached model response is acceptable as clearly labeled demo resilience, never as fake live inference or evidence of current API access. A live Meta path is required before claiming the project demonstrates live Meta integration.

## 9. Scientific honesty, safety, and reproducibility

- Trust boundary: model proposes; compiler validates known contracts; trusted code calculates; user approves assumptions. None of these guarantees that the selected scientific model describes a real site accurately.
- No arbitrary code, shell, filesystem, network URL, or model-generated expression may be introduced through a graph proposal. Both runtime adapters dispatch reviewed functions only.
- Use fixed subprocess executable/entrypoint and JSON input; never interpolate prompt text into a command line. Enforce timeout, output-size limit, and nonzero-exit handling. A subprocess is not a sandbox for arbitrary user code; no such execution is permitted.
- Keep secrets server-side and redact logs. Run exports exclude provider keys, session identifiers, and private prompt text by default.
- Local-only synthetic demo is the initial operating mode. Do not put real plant data into an API without explicit permission and review of the provider's current data policy.
- Record exact formulas, node revisions, input snapshots, price basis, model ID, prompts/configuration where safe, and warnings. A rerun of a fixed graph and inputs should not need a fresh model call.
- Never label source provenance as peer review, claim a white-box badge proves accuracy, or say deterministic execution eliminates uncertainty.
- Scenario envelopes are not confidence intervals. One-at-a-time sweeps are not variance decomposition or causal attribution. Correlations, probabilistic water forecasts, Monte Carlo, and calibrated uncertainty are deferred.
- Any public deployment, sharing, or contest submission needs user authorization and must use infrastructure compatible with the actual Python + Node runtime. A static/Workers-only host does not run this proposed scientific backend without a redesign; do not deploy a broken substitute.

## 10. Evaluation: demonstrate the claim rather than repeat it

### 10.1 Engine/compiler acceptance fixtures

Build roughly 20–30 focused deterministic fixtures, not an elaborate testing platform:

- Correct baseline and upgrade values from Section 5, with unit-aware tolerances (for example 1e-6 kW/kWh and one cent for displayed NPV).
- Zero flow yields zero generation and no avoided energy; capex still applies.
- Equal baseline and upgrade efficiency yields zero additional energy; incremental O&M/capex still reduce NPV.
- Generator cap and on-site load cap are applied per block, not to annual averages; no export benefit is credited.
- kWh/MWh conversions preserve results, while kW→kWh requires explicit integration.
- Same-unit semantic errors (gross/net flow or mechanical/electrical output) reject before execution.
- Site, block length/identity, analysis period, nominal/real, and currency mismatches reject.
- Missing inputs, unknown module IDs, cycles, invalid efficiency, negative supported quantities, NaN/infinity, adapter timeout/failure, and invalid tool arguments fail explicitly.
- Tariff-only changes do not reuse stale finance results; flow changes refresh all affected descendants. Descriptor revisions invalidate or reject stale plans.
- Nonmonotone incremental benefit under flow changes is retained as a regression, not “fixed” to match a narrative.

**Must-pass:** every fixture designed to exercise a hard safety/type invariant passes; no invalid graph reaches execution. No suppression of failures. Each check proves only the supported contract, not universal correctness.

### 10.2 Small, fair agent benchmark

Create 18 tasks before prompt tuning, with expected outputs or expected clarification/rejection:

- 6 legitimate composition and what-if tasks, including multi-step changes and a break-even capex query.
- 6 ambiguity/missing-input/unsupported tasks.
- 6 malicious or incompatible-binding tasks, including plausible same-unit errors.

Split into six development tasks and 12 held-out tasks. Use three repeated runs on the held-out set if credits/time allow (36 per comparison arm). Report sample sizes; use raw counts for very small subsets. Do not train or tune on the held-out prompts.

Compare the **same Meta model** with the same facts and module descriptions in:

A. Text-only problem solving, no execution tools.
B. Ad-hoc code generation plus execution in a genuinely disposable, isolated evaluator.
C. Connected Models registry/compiler/runtime tools.

The code baseline is essential to test whether a typed graph adds more than a calculator. Do not execute generated code in the shared checkout. If an appropriate sandbox cannot be prepared within the event, mark arm B as not run and explicitly limit any claimed advantage to the baselines actually tested. A baseline returning text without execution is not a fair substitute for an executable-code baseline.

Metrics:

- End-to-end correctness, including numeric tolerance, model/binding selection, and requested output semantics.
- Appropriate clarification/abstention vs unsupported confident answers.
- Unsafe proposals vs unsafe executions, separately: a compiler preventing a bad proposal is good, but the proposal is still an agent error.
- Provenance completeness and explanation-result consistency.
- Input/output tokens and reasoning-token usage if the API exposes them, complete tool payloads, number of model round-trips, repairs, and tool calls.
- End-to-end latency, reported separately from engine time; cold vs warm cache conditions; model/backend version; actual measured cost where known.
- Human setup and curation effort, not just the execution savings after graphs have been prebuilt.

No hidden reasoning transcripts are required. Use observable requests/responses and runtime logs. Do not claim latency reductions from token counts, or a 60%/50% improvement without measurement. If plain code is equally accurate and faster, report it; the possible differentiation is reusable semantics, validation, and traceability, not always raw arithmetic speed.

### 10.3 Product/impact validation

By mid-event, attempt two or three short sessions with people who have relevant modeling, energy, or capital-budgeting experience. Ask them to interpret the graph, locate an assumption, and evaluate one change against their current workflow. Record role and feedback with consent; do not invent interviews if unavailable.

Ask: Is the decision realistic? What major factor is missing? Would the trace make review easier? What would justify adoption? Only report time saved if a comparable task is actually timed. Otherwise report qualitative feedback and the lack of a measured impact study.

### 10.4 Performance targets, not promises

Set provisional UX targets: deterministic run under one second for the default profile; approved scenario update under two seconds excluding a new model explanation; bounded Meta-assisted response with clear progress states. Measure on the actual demo machine and report cold/warm times. Exact targets can be adjusted after measurement without hiding failures; scientific/typing correctness takes priority.

## 11. Ten-day delivery plan

Assumption: one experienced full-time builder, roughly 55–70 focused hours across the ten days, with limited domain review. The calendar is a deadline plan, not a claim that every task fits an evening. If fewer than about 35 hours are available, use the cut order in Section 13 immediately. Helpers can parallelize after contracts freeze; headcount and contest eligibility remain unconfirmed.

| Day / date | Deliverable | Exit condition | Budget |
| --- | --- | --- | ---: |
| 1 — Oct 26 | Confirm rules/access and wedge; define default fixture and contracts; minimal Meta request | Accepted model/access verified, known rule gaps logged, input/output contract and correct independent calculation agreed. No access by the end of session triggers a verified Meta fallback investigation, not UI expansion. | 5–7 h |
| 2 — Oct 27 | Registry + schema + compiler | Hand-authored default graph compiles; invalid units, same-unit meaning errors, missing inputs, and cycles reject with actionable diagnostics. | 6–8 h |
| 3 — Oct 28 | Python physical execution and finance adapter, run trace | Hand-authored complete graph matches oracle; two adapters exchange bounded typed JSON. If polyglot integration exceeds the session, use one Python runtime and record that limitation. | 7–8 h |
| 4 — Oct 29 | Live Meta proposal, clarification, bounded repair, result explanation | At least three differently worded requests produce valid approved runs or correct clarifications. Invalid model output cannot bypass checks. | 6–8 h |
| 5 — Oct 30 | One workbench with graph inspector, result cards, assumptions | A user can follow ask → graph → values → sources without reading code. No social/auth/editor detour. | 6–8 h |
| 6 — Oct 31 | Scenario changes, explicit invalidation, small sensitivity sweep | Tariff flip works; water effects computed rather than assumed; stale-result regression passes; every output carries scenario identity. | 5–7 h |
| 7 — Nov 1 | Hardening + first feedback + evaluation set frozen | Core fixtures pass; privacy/error/replay modes explicit; held-out questions frozen; complete demo path works. **Feature freeze.** | 5–7 h |
| 8 — Nov 2 | Held-out comparisons and fixes | Evaluation results contain counts, model IDs, failures, token/latency data, and all tested arms; genuine code-baseline blocker disclosed if applicable. | 5–7 h |
| 9 — Nov 3 | Record demo; package reproducibility and submission copy | Video includes live run, assumption change, invalid-binding rejection, and limitations; instructions work on a clean environment; required submission fields prepared. | 5–6 h |
| 10 — Nov 4 | Buffer, final checks, user-approved submission | Rehearse once, verify secrets/licensing and final requirements, submit with several hours' margin before 9 PM ET; save confirmation. No late architecture changes. | 4–5 h |

The budgets total roughly 54–71 hours. Reserve the final day for failures, not promised extras. Re-check official deadlines; do not rely on an undocumented submission grace period.

### 11.1 Critical path

Rules/access + reference math → contracts/compiler → deterministic runtime → Meta loop → usable workbench → evaluation → demo/submission. A beautiful graph UI cannot compensate for missing execution. A benchmark cannot rescue unverified Meta access. Do not wait until day nine to discover those blockers.

### 11.2 Parallel work if eligible teammates are available

- Engine owner: descriptors, compiler, runtime, invalidation, numerical fixtures.
- Agent/UI owner: Meta adapter, proposal/review flow, workbench, explanation references.
- Reviewer/demo owner (optional): source and assumptions review, independent reference, user feedback, benchmark tasks, video.

Freeze shared request/response JSON first. A solo builder follows the same dependencies sequentially. Do not turn this into a multi-agent orchestration product because multiple people help build it.

### 11.3 Proposed implementation layout

This is a future outline, **not directories or source files created by this planning task**:

```text
app/                    React/TypeScript workbench
server/                 Python API, registry loader, compiler, runtime, Meta adapter
adapters/finance/       Trusted TypeScript-to-JavaScript finance evaluator
models/                 Versioned JSON descriptors and reference citations
fixtures/               Synthetic inputs, graph fixtures, independent expected outputs
tests/                  Focused compiler/runtime/adapter tests
evaluation/             Frozen prompts, scoring code, reproducible aggregate results
knowledge/              Durable reasoning, findings, source evidence, decisions
```

Keep implementation tests/results separate from knowledge claims. Promote a result to Project Memory only when it changes durable understanding. Exact layout and dependencies can shrink at build time; no need for a monorepo tool, hosted database, or distributed queue.

## 12. Milestone acceptance gates

**Gate A — deterministic spine (end Day 3):** one graph, approved inputs, compiler checks, reproducible physical-to-financial result and trace. Missing this gate means cut UI and polyglot scope, not type safety.

**Gate B — Meta adds real capability (end Day 4):** live model interprets multiple requests, proposes supported components/bindings, requests missing facts, and handles a typed error without arbitrary code execution. No live access means no claim of live integration.

**Gate C — complete demo (end Day 6):** graph inspection, explicit input provenance, one positive-to-negative scenario flip, and one same-unit semantic rejection. No unfinished dashboard panels masquerading as functionality.

**Gate D — evidence and submission (Days 8–10):** measured comparison and limitations; working demo recording; reproducibility and actual rule compliance. Do not state that a video, repo link, or runtime has been delivered until it exists.

## 13. Cut list and risk register

### 13.1 Scope priorities

**P0 — protect:** one decision; live Meta proposal/clarification; typed graph and semantic rejection; trusted deterministic server execution; visible assumptions/provenance; baseline/upgrade calculation; one scenario change; truthful live/replay label; small correctness evaluation; demo video.

**P1 — only after the spine works:** second-language adapter, selective result caching instead of whole-run invalidation, automated larger held-out comparison, compact multi-parameter sensitivity display.

**P2 — after the event:** arbitrary model authoring, ODE/PDE adapters, empirical calibration, meaningful uncertainty/correlation modeling, standards mapping, distributed/federated execution, proprietary oracles, model discovery at scale, auth and sharing.

If time shrinks: cut custom plotting → multi-parameter sweep → selective cache UI → second runtime → benchmark repetitions (preserve honest counts). Never cut compiler checks, result provenance, numeric correctness, or transparency about replay. Keep one deterministic scenario comparison even without sliders.

### 13.2 Main risks

| Risk | Early indicator | Response |
| --- | --- | --- |
| Rules/access mismatch | Missing acceptance/model access or unreadable official terms | Confirm with organizers on Day 1; never invent eligibility; use only verified alternatives. |
| Scientific overreach | Questions require basin forecasts, water rights, operating curves | Keep synthetic screening scope; expose missing factors; get review rather than adding unsupported predictions. |
| Generic chatbot appearance | Same single answer regardless of prompt or graph | Show actual component selection, a missing-input clarification, typed error response, inspectable graph, and rerun. |
| Hard-coded workflow appearance | Model always replays the same graph | Freeze a small catalog but test multiple goals/valid subgraphs (energy only, savings, NPV, break-even) and different parameters. Bound composition, do not pretend it is universal. |
| Wrong same-unit connection | kW or USD matches but meaning differs | Semantic contracts and adversarial fixtures; hard errors cannot be overridden by model prose. |
| Wrong story about water | Narrative assumes monotone incremental benefit | Use the clipped reference case and trace actual deltas. |
| Stale results | Tariff or descriptor change leaves old NPV | Explicit revision/input identities; reject stale plans; full recompute fallback. |
| Extra runtime overwhelms delivery | Cross-language integration misses Day 3 gate | One Python runtime, honest claim reduction, unchanged descriptor boundary. |
| Hallucinated explanation | Unsupported values or causal claim | Deterministic numeric rendering, claim references, human-reviewable prose, explicit limits. |
| API outage/rate limit | Demo cannot obtain a fresh proposal | Bounded retries, clear error, openly labeled recorded Meta trace and deterministic rerun. |
| Unfair benchmark | Only compare against text arithmetic | Include real code-execution baseline when isolated execution is feasible; otherwise disclose missing comparison. |
| Too little domain/user evidence | No operator can review in time | Say synthetic technical prototype; do not invent traction, customer savings, or production readiness. |
| Deadline creep | New integrations after Day 7 | Freeze features; spend remaining time on verification and recording. |

## 14. Demo, judging evidence, and deliverables

### 14.1 Suggested three-minute narrative, adjustable to actual rules

- **0:00–0:20 — problem:** a capital decision crosses physical and financial models; a confident paragraph is not an auditable calculation.
- **0:20–0:55 — Meta proposes:** ask the upgrade question, show the actual Meta model label, approve one missing assumption, and reveal the graph.
- **0:55–1:25 — compute and inspect:** execute, show NPV and break-even capex, click an upstream output to reveal formula and input provenance.
- **1:25–1:55 — decision changes:** lower tariff from $0.15 to $0.12/kWh and show the computed positive-to-negative NPV flip. If time permits, show why flow sensitivity is not necessarily monotone.
- **1:55–2:20 — defend against nonsense:** explicitly introduce a same-unit but wrong-meaning edge; show compiler rejection and a valid repair. Do not fabricate a spontaneous model error for drama.
- **2:20–2:40 — evidence:** show actual benchmark counts, not aspirational percentages; distinguish engine correctness from end-to-end model reliability.
- **2:40–3:00 — future:** one graph is the seed of an agent-accessible computational medium. State current limits and the next real-user validation step.

Three minutes is a proposed communication length, not a verified contest requirement. Adapt to official video/live-final rules. Favor a clear causal chain over spending time panning around a graph.

### 14.2 Submission package to prepare, subject to official fields

- Working local demo and any explicitly authorized judge-access route; test the actual backend, not only a static frontend.
- Short recorded demonstration and backup recording, both truthful about live/replay portions.
- Source repository or archive if required, with a baseline-history disclosure, licenses and third-party notices, no secrets, and reproducible setup instructions.
- One-page explanation of the real problem, user, chosen theme/track, Meta's substantive role, technical novelty, evidence, and limitations.
- Reproducible default scenario, graph, expected outputs, representative run export, and evaluation summary with failures.
- Explicit statement: synthetic default data; no field calibration; no automated physical actions; no claim of eliminating model error.
- Required team/eligibility disclosures and submission confirmation retained after an authorized submission.

**Judging differentiation:** this is not “an LLM using a calculator.” It demonstrates reusable typed components, semantic compatibility checks beyond units, explicit compilation, provenance-aware execution, and auditable scenario recomputation. The fair code baseline determines whether those advantages show up in the tested tasks.

## 15. After the hackathon: extend only what evidence supports

### First two weeks

- Select one real design partner and a permissioned dataset; compare a current spreadsheet workflow with the prototype on the same decision.
- Review physical assumptions and add the most consequential omitted factor, such as a genuine flow-dependent efficiency curve, downtime, or demand profile. Do not add every factor at once.
- Correct canonical claims in Project Memory using measured results. If token savings are absent, preserve that disagreement rather than moving the goalposts.
- Decide whether energy operations is a credible commercial beachhead or whether valuation is better supported by builder access and user demand. The demo alone does not resolve [[question-initial-domain-beachhead]].

### Following four to six weeks, conditional on user value

- Test the same envelope on a genuinely different model class, for example one reviewed Python ODE solver plus the existing finance adapter. Demonstrate initial conditions, solver tolerances, time integration, and failure states instead of inventing a universal AST.
- Compare the lightweight unit/semantic subset against relevant standards such as UCUM/QUDT and domain-specific conventions. Research these standards when this work actually starts; this plan does not select a universal ontology.
- Add explicit uncertainty distributions and correlated scenarios only with appropriate input justification and coverage evaluation. Separate observation error, parameter uncertainty, model discrepancy, and scenario choices.
- Define a stable agent tool API or MCP surface only after observing actual agent needs. Add model discovery, permissions, and private data boundaries before any public registry or proprietary oracle.

### Later, not automatic commitments

Federation, distributed schedulers, feedback-cycle solvers, complex PDE/Monte Carlo workloads, robust calibration/badging, public curation, billing, and model-author incentives require separate evidence and decisions. Preserve the three-layer end-state vision while earning each expansion with a demonstrated interoperability need.

## 16. Immediate next build session

1. Resolve official rule/access questions and confirm the proposed domain story without overstating lived expertise.
2. Agree the exact synthetic fixture, scope exclusions, and one decision-flipping scenario.
3. Implement descriptors and hand-authored graph compilation before a chat UI.
4. Implement and verify the deterministic calculation against an independent oracle.
5. Introduce Meta as a constrained graph proposer and interpreter only after the trusted execution boundary exists.

This task produced a plan and evidence records only. It did not install packages, implement the product, call an authenticated Meta endpoint, run an application benchmark, publish a site, or submit a hackathon entry.
