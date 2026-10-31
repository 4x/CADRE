# Connected Models

Compose reusable quantitative models and inspect their inputs, assumptions, dependencies and results. The first runnable slice compares electric resistance heating with a heat pump, then connects operating savings to discounted investment value.

Returning agents: start with the session handoff in [PROJECT_STATE.md](PROJECT_STATE.md), then the [active MVP plan](knowledge/notes/mvp-build-sequence-and-extension-triggers.md). M2-A/B/C are complete; the broader acceptance exercise (M2-D) is next. Current worker release files are directly in `.runs/curation-kits-2026-10-31.4/`; build/test artifacts are archived separately. The full offline suite has 85 passing tests. Incoming ZIPs and the live registry/runs are local state; migration details are in the handoff.

## Run the current prototype

Requires uv and Python 3.12 or newer. No third-party Python packages are required.

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models demo
uv --cache-dir .uv-cache run --no-env-file -m connected_models demo --performance 2 --investment 12000
uv --cache-dir .uv-cache run --no-env-file -m connected_models demo --question operating-cost
```

The synthetic default scenario uses 12,000 kWh of delivered annual heat, seasonal performance 3, a flat $0.30/kWh tariff, $10,000 incremental investment, a ten-year study period and a 5% annual effective real discount rate. It yields $2,400 annual operating savings and $8,532.16 net present value under those assumptions. These are illustrative inputs, not household measurements or purchasing advice. Every run saves its complete model definitions, input bindings, provenance and intermediate results under `.runs/`; earlier runs are preserved.

The `demo` command is a developer fixture with known presets. The real `answer` command accepts only a self-contained question: put assumptions, numbers, units and requested outputs in its text. It has no performance, tariff or investment options and never loads the demo's preset inputs. The present-value model currently requires a positive discount rate and an integer horizon from 1 to 100 years. Performance must represent seasonal whole-system delivered heat divided by electricity use; a single temperature's COP rating is insufficient. Maintenance, cooling benefits, replacements, incentives, tariff escalation and uncertainty propagation are excluded from the initial heating models.

## Meta inference setup

The public settings in `inference.toml` select `muse-spark-1.3` in Standard mode and a $150 application-wide ceiling. The adapter uses the [Meta API route documented for coding agents](https://dev.meta.ai/docs/coding-agents). It does not change the coding agent running this session.

The application accepts `META_API_KEY` from its process environment. On October 29, 2026 the owner authorized runtime-only loading with uv; this permission does not authorize inspecting or displaying `.env` or its contents. Launch a bounded connection check with:

```powershell
uv --cache-dir .uv-cache run --env-file .env -m connected_models meta-smoke
```

This sends one bounded paid structured-output request. The command prints only connection status, model, request identifier and conservative cost. It never displays the key or raw API response. Live connection, source extraction and three supported query compositions were verified on October 29, 2026. An unsupported forecasting question was correctly blocked. Offline tests use a fake transport and placeholder credential.

The persistent `.usage/meta.sqlite3` ledger reserves worst-case token cost before sending and settles against reported usage. Failed or ambiguous requests retain their reservation and are not retried automatically. Preserve this ledger across runs. Its ceiling covers calls through this application; spending in other tools or accounts is outside its accounting. Prices are pinned to the [Meta Standard-mode rates checked October 29, 2026](https://dev.meta.ai/docs/pricing-rate-limits); reverify pricing before changing models or rates. Use an account-side spending limit as well if the provider supports it.

## Test

```powershell
uv --cache-dir .uv-cache run --no-env-file -m unittest discover -s tests -v
```

Tests compare execution with a separately summed Decimal cash flow and NIST Handbook 135 (2020), equation 3-7, printed page 29 ($457.97 for five year-end payments of $100 discounted at 3%). They also exercise dimensional and semantic rejection, cycles, missing inputs, unsafe expressions, model substitution, saved-run preservation and persistent budget controls. All tests run without network calls.

## Implementation status

Implemented: bounded scalar algebra, explicit per-port context and meaning checks, ratio-unit conversions, graph compilation, deterministic evaluation, immutable run snapshots, two fixture compositions and a budgeted Meta connection-check adapter. Expressions are interpreted through an allowlisted AST; arbitrary Python code is not executed.

The `demo` command uses handwritten fixtures. The separate registry workflow supports offline source extraction, candidate storage, attributed review/publication, withdrawal and query-time composition against eligible stored versions. Sixty-seven offline tests pass, including isolated curator packaging, compatible data returns and candidate-only import. Live question-only evaluation, inverse solving, discounted payback and missing-input clarification have been verified. The development agent recorded a scoped local prototype review under `codex-prototype-review`; it does not claim human scientific approval. The inspector prints saved evidence and can export a standalone HTML report, including inputs quoted from the question. The contracts implement a bounded subset of the representation draft, not full v0 conformance.

## Curate, review and reuse models

For multiple offline research agents, use the [owner/operator guide](knowledge/notes/offline-curation-agent-kit.md). Each isolated worker kit contains the complete [curator protocol](knowledge/notes/offline-curator-instructions.md) as `AGENTS.md`, exact schema/example and offline validation tools. It contains no owner guidance and at most one assignment. Curators build atomic reusable models; chains and sample queries are optional. Give a generic-kit worker `Read @AGENTS.md and work on {assignment JSON}`, or use a domain kit and `Read @AGENTS.md and work on @assignment.json`. Subsequent assignments select new batch folders/IDs and preserve earlier returns automatically. Candidates with new physical units retain integration blockers; curators do not publish models or merge databases.

```powershell
# Build a portable snapshot; the output must not already exist.
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation kit curation-generic-2026-10-31.4.zip
# Or include only the chosen worker's assignment:
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation kit curation-building-energy-2026-10-31.4.zip --domain building-energy
# Check and stage a returned batch on the integration PC; this does not publish.
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation validate incoming/building-energy-a01-b01-return.zip
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation import incoming/building-energy-a01-b01-return.zip
```

The kit pins its own version and JSON schema. It carries no credentials, inference adapter/configuration, local databases or third-party dependencies. The validator checks scalar arithmetic and optional current-runtime projections; scientific source review and physical-dimensional validation of new-domain research remain explicit integration work. See the guide for source restrictions, version conflicts, repeat imports, review commands and the optional Git workflow for agents assigned code integration.

Earlier `.1`–`.3` worker returns remain compatible with the revised tools. Release `.4` authorizes sustained sessions of at least 60 minutes, multiple saved batches, `SESSION.json` checkpoints and automatic continuation between batches. The [operator guide](knowledge/notes/offline-curation-agent-kit.md#sustained-sessions-and-fleet-dispatch) contains the existing-worker update prompt, domain partitioning and interruption handling; actual host execution limits still apply. The [fleet intake](knowledge/sources/curation-fleet-intake-2026-10-31.md) reports eight new mechanically valid returns and one cross-worker identity conflict. Scientific review remains separate.

Generate a dated catalog snapshot before dispatch to reduce duplicates and catch conflicting immutable IDs before import:

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation inventory from-offline-curation-workers fleet-inventory.json
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation kit building-energy-worker.zip --domain building-energy --inventory fleet-inventory.json
```

M2-A/B are complete. The [separate mechanics audit](knowledge/sources/mechanics-independent-audit.md) recommends two constant-acceleration records for bounded local execution; three require corrections. Runtime 0.3 adds a bounded mechanics vocabulary, dimensional integer powers and physical-unit aliases, preserving the legacy kWh/USD numerical scales. Two independently reviewed runtime projections are eligible locally. Seventy-six tests pass, including fresh-registry reproduction; three saved heating runs replay with unchanged results and original files. Full report, unchanged research data and integration receipt are in `data/curation/reviews/`. The [M2 plan](knowledge/notes/mvp-build-sequence-and-extension-triggers.md#m2-closeout-assessment--2026-10-31) retains revision controls and the broader acceptance exercise as M2-C/D.

Create a separate reviewer packet, then validate the returned report and stage a supported recommended record:

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models.auditing packet incoming/return.zip reviewer-packet.zip
uv --cache-dir .uv-cache run --no-env-file -m connected_models.auditing validate incoming/return.zip incoming/review.json
uv --cache-dir .uv-cache run --no-env-file -m connected_models.integration incoming/return.zip incoming/review.json MODEL_ID --version r1.runtime1
```

Give only the extracted packet to a different reviewer agent with `Read @AGENTS.md and complete @assignment.json`. See the [operator guide](knowledge/notes/offline-curation-agent-kit.md#separate-auditor-handoff-and-technical-integration) for review criteria, projection evidence and the separate attributed admission command. Neither report validation nor projection publishes a model. To reproduce the committed example without the original ZIP, the validator and integrator also accept `data/curation/reviews/classical-mechanics-a-b01-bundle.json` with its corresponding review JSON.

The application credential variable is **META_API_KEY**. This overrides the variable name shown in Meta's generic documentation. Agents do not access `.env` unless the owner explicitly permits a runtime-loading exception. The following live commands are intended for an owner launch, or for an explicitly authorized runtime launch by the agent.

```powershell
# Stage four supporting project-derived candidates, without publishing them.
uv --cache-dir .uv-cache run --no-env-file -m connected_models seed-candidates
# Make a paid offline extraction from the bundled public NIST source packet.
uv --cache-dir .uv-cache run --env-file .env -m connected_models curate
# Produce a readable report of sources, extracted algebra, assumptions and checks.
uv --cache-dir .uv-cache run --no-env-file -m connected_models review-bundle
```

The curator receives the NIST equation with its source notation and a canonical interface, then extracts executable algebra and a symbol/source map. It does not receive the fixture's program expression. The published numerical example is checked independently before review. Incomplete or failing extractions remain candidates with diagnostics. Supporting accounting definitions are explicitly marked manual project derivations; they are not misrepresented as agent extractions.

Inspect a candidate with `candidate CANDIDATE_ID`. After checking source fidelity, applicability, interface meanings and assumptions, the owner records a scoped review:

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models review CANDIDATE_ID --decision accepted --reviewer owner --notes 'Describe the checked source and permitted scenario use'
uv --cache-dir .uv-cache run --no-env-file -m connected_models registry-list
```

Each model revision is immutable. A replacement definition needs a new version. A `withdrawn` review prevents new snapshots from using that candidate; saved runs keep their original evidence. Eligibility is snapshotted at the start of a short local run rather than revoked mid-calculation. This is a single-operator trust boundary: explicit local review commands carry publication authority, and the reviewer identity/scope are retained. For local build/testing, the development agent independently checked and admitted candidates under its own identity. The curator/composer inference roles have no publication tools and cannot approve their own outputs. Broader scientific approval policy remains unresolved.

Once all necessary versions are eligible, ask a self-contained question. For example:

```powershell
$question = @'
Annual delivered heat demand is 12000 kWh. Baseline resistance heating has seasonal performance 1 and the proposed heat pump has seasonal performance 3. Electricity has a flat tariff of 0.30 USD/kWh. The incremental upfront investment is 10000 USD. Use an annual effective real discount rate of 5 percent and a study horizon of 10 years. Assume the same delivered heat and comfort, constant real prices and annual savings paid at each year end, with no maintenance differences, replacements, cooling benefits or residual value. Calculate annual operating costs, annual savings and the investment net present value.
'@
uv --cache-dir .uv-cache run --env-file .env -m connected_models answer $question
uv --cache-dir .uv-cache run --env-file .env -m connected_models answer 'For the same annual delivered heat of 12000 kWh, compare baseline electric heating with seasonal performance 1 and a heat pump with seasonal performance 2.5, using a flat tariff of 0.25 USD/kWh in constant real prices. Exclude cooling benefits, maintenance differences, and changes in fixed charges. Calculate annual operating costs and savings only.'
uv --cache-dir .uv-cache run --no-env-file -m connected_models inspect RUN_ID
uv --cache-dir .uv-cache run --no-env-file -m connected_models report RUN_ID ANOTHER_RUN_ID
uv --cache-dir .uv-cache run --no-env-file -m connected_models usage
```

The first query-time step extracts a domain-independent list of typed facts (number, date or text), with exact quotes from the question. Numeric literals and supported adjacent units are checked against those quotes. The composer receives these facts and eligible stored definitions; each external input must reference a fact ID, and each derived input must reference an upstream node. It cannot emit a new numeric literal or use a remembered demo value. A structured graph object avoids nested JSON-string generation. The compiler checks and executes the resolved graph, saving both extraction evidence and proposed assignments to model inputs.

If the question omits required inputs, the result is `needs-input` with specific clarification questions and no calculated answer. Asking only for annual operating costs does not require an investment amount, horizon or discount rate. Unsupported model coverage remains `blocked`, with parsed inputs retained. This currently uses a self-contained follow-up question rather than persistent conversational state. Generated estimates remain disabled until a scoped consent flow exists; source curation never runs inline.

The parser is not tied to heating names: it can retain a number of apples, a birth date, or a person's name. Executing date/text operations or a new domain still requires suitable stored models and runtime support; the current engine is scalar numeric and the catalog remains small. Executable numbers currently require explicit digit literals (commas and decimal/exponent forms are supported). Percentages remain in percent until the unit layer converts them. Exact quotes and numeric checks do not prove perfect semantic interpretation; the report exposes the selected fact-to-port assignments for inspection.

## Revise a saved run and compare results

Any saved run with an executable graph can be revised without inference: change direct inputs, substitute a model revision on a node, or both. The original run file is never modified; the revision is saved as a new run linked with `revised_from`. Scenario (`answer`) runs re-execute against the registry's current eligible snapshot, so `--model` selects among reviewed revisions. Amounts use the model's declared port unit, shown by `inspect`.

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models revise RUN_ID --set upgrade-energy.performance=2 --set investment-npv.investment=12000
uv --cache-dir .uv-cache run --no-env-file -m connected_models revise RUN_ID --model upgrade-energy=heat-to-electricity@2
uv --cache-dir .uv-cache run --no-env-file -m connected_models report RUN_ID REVISED_RUN_ID
```

Only direct value inputs can be revised; calculated upstream bindings are rejected with an explanation, as are unknown nodes, undeclared inputs and unavailable model revisions (the error lists what is available). A revision that violates model guards or interface checks is saved as a rejected run with diagnostics, preserving the failure evidence. Listing two or more runs in `report` adds a "What changed" comparison of outputs with deltas, changed inputs and changed models, each run compared against the first listed.

## Solve for another quantity in an existing relationship

Version 0.2 adds directional solve views rather than separate scientific models for every rearrangement. A model revision retains its equation, source, interface meanings, guards and review. A run may select a declared input as `solve_for`, supply all other inputs and the known original output through the reserved `__output__` binding, and return the selected variable using its original unit/context. The composer creates these views through the same question-only interface. It never generates or executes a new formula as an agent-authored model.

```powershell
uv --cache-dir .uv-cache run --env-file .env -m connected_models answer 'A heating system supplies 12000 kWh of delivered heat over a representative year and consumes 4000 kWh of electricity over that same year, with auxiliaries and losses included. What effective seasonal performance does this imply?'
uv --cache-dir .uv-cache run --env-file .env -m connected_models answer 'My annual electricity operating cost is 1200 USD with a flat tariff of 0.30 USD/kWh in constant real prices. Fixed charges are unchanged, and maintenance and cooling benefits are excluded. What annual electricity consumption corresponds to that cost?'
uv --cache-dir .uv-cache run --env-file .env -m connected_models answer 'I am considering replacing my resistance heating with a $10000 heat pump. When would this pay off, assuming a 5% real discount rate? Annual delivered heat demand is 12000 kWh. Baseline resistance heating has seasonal performance 1 and the proposed heat pump has seasonal performance 3. Electricity has a flat tariff of 0.30 USD/kWh'
```

These three live checks returned seasonal performance 3, annual electricity consumption 4,000 kWh, and first discounted payback at the end of year 5, respectively. Payback applies the original present-value model's constant-real, uniform year-end savings assumptions conditionally; it does not infer actual equipment life or different maintenance/replacement costs. Its 1–100 year search domain comes from the model guards, not an invented user horizon. Report: [inverse and payback evidence](.runs/report-a27fdff2-952f-47db-8035-26f691bba2ec.html).

The first algebra profile substitutes known canonical-unit values into restricted rational arithmetic, forms an exact rational-coefficient polynomial, and solves degree one or two over real numbers. Unknown-dependent powers are restricted to integer magnitude at most two; intermediate degree and coefficient-size limits are explicit. Candidates are re-evaluated in the unmodified original expression with every source guard and type constraint; denominator exclusions survive rearrangement. Residual tolerances are recorded (1e-9 relative and absolute). Multiple admissible roots remain an explicit ambiguity with candidates, not a guessed positive branch. Unsupported forms, numerical limits, undefined domains, underdetermination and no admissible root are distinguished. Fixed literals are not free variables. The unitless E=m*c² fixture tests algebra only; this does not add a curated physics model or SI mass/speed vocabulary.

For integer period-count targets, a non-polynomial equality can use finite enumeration when original guards supply both bounds. A requested earliest threshold uses `relation=at_least`, checks each admissible integer in ascending order, and returns the first crossing without assuming monotonicity. At most 1,000 candidate integers are evaluated. Failure means no crossing within that declared domain, not no possible crossing anywhere. Fractional-time payback, general continuous root finding, systems of unknowns, higher-degree/transcendental symbolic solving and user-selected branches outside model guards remain unsupported. Algebraic reversal does not establish causal reversal or a scientifically valid inverse of a statistical/calibrated model.

Curators remain responsible for source relationships, scientific scope, variable roles/constants and domain constraints. The solver is a separate deterministic facility. Future derived implementations can be cached/indexed against a pinned source revision and solver profile without multiplying canonical model identities. Independently estimated inverse models or changed scientific assumptions would need their own linked evidence/review.

Local runtime artifacts are stored in `.registry/`, `.runs/` and `.usage/`, all excluded from version control. Preserve the registry and spend ledger when continuing the prototype.

## First live trial

Open the generated [question-only run report](.runs/report-33d01f44-a487-474c-9b94-12ac5939cf0c.html) in a browser. It contains the complete investment question, a different operating-cost question, and a question needing clarification. Each parsed input cites the original query text. Expand calculation steps to inspect dependency inputs, source references, assumptions and attributed reviews. The report is self-contained and opening it makes no API calls. If reproducing this checkout without local artifacts, generate a new report from your own run IDs. Earlier reports remain historical evidence of the preset-driven interface, which the user rejected on October 31.

The default live NPV is $8,532.16. With seasonal performance 2, tariff $0.25/kWh and incremental investment $12,000, the NPV is -$417.40. Both were separately checked against a Decimal sum of annual discounted cash flows with absolute tolerance 1e-8. These conditional examples say nothing about a particular real installation until its data and model applicability are checked.

The initial curation retained real ambiguities as blocking evidence. The final source packet adds NIST's real/nominal distinction and cash-flow timing, and records limitations separately from in-scope ambiguities. Earlier blocked candidates remain in the local registry. The adapter now reports non-stop completion reasons before attempting JSON parsing and uses explicit low reasoning effort, because reasoning and visible JSON share the output-token budget. There are no automatic retries. The first live JSON failure's finish reason was not captured, so token exhaustion is a plausible explanation, not a verified diagnosis of that historical response.

The canonical delivery plan is [MVP milestones](knowledge/notes/mvp-build-sequence-and-extension-triggers.md); current project context is in [PROJECT_STATE.md](PROJECT_STATE.md). Source/evidence records and design decisions live in Project Memory under `knowledge/`.
