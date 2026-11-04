# Curate, review and reuse models

For multiple offline research agents, use the [owner/operator guide](../knowledge/notes/offline-curation-agent-kit.md). Each isolated worker kit contains the complete [curator protocol](../knowledge/notes/offline-curator-instructions.md) as `AGENTS.md`, exact schema/example and offline validation tools. It contains no owner guidance and at most one assignment. Curators build atomic reusable models; chains and sample queries are optional. Give a generic-kit worker `Read @AGENTS.md and work on {assignment JSON}`, or use a domain kit and `Read @AGENTS.md and work on @assignment.json`. Subsequent assignments select new batch folders/IDs and preserve earlier returns automatically. Candidates with new physical units retain integration blockers; curators do not publish models or merge databases.

```powershell
# Build a portable snapshot; the output must not already exist.
uv run --no-env-file -m connected_models.curation kit curation-generic-2026-10-31.5.zip
# Or include only the chosen worker's assignment:
uv run --no-env-file -m connected_models.curation kit curation-building-energy-2026-10-31.5.zip --domain building-energy
# Check and stage a returned batch on the integration PC; this does not publish.
uv run --no-env-file -m connected_models.curation validate incoming/building-energy-a01-b01-return.zip
uv run --no-env-file -m connected_models.curation import incoming/building-energy-a01-b01-return.zip
```

The kit pins its own version and JSON schema. It carries no credentials, inference adapter/configuration, local databases or third-party dependencies. The validator checks scalar arithmetic and optional current-runtime projections; scientific source review and physical-dimensional validation of new-domain research remain explicit integration work. See the guide for source restrictions, version conflicts, repeat imports, review commands and the optional Git workflow for agents assigned code integration.

Generate a dated catalog snapshot before dispatch to reduce duplicates and catch conflicting immutable IDs before import:

```powershell
uv run --no-env-file -m connected_models.curation inventory from-offline-curation-workers fleet-inventory.json
uv run --no-env-file -m connected_models.curation kit building-energy-worker.zip --domain building-energy --inventory fleet-inventory.json
```

Create a separate reviewer packet, then validate the returned report and stage a supported recommended record:

```powershell
uv run --no-env-file -m connected_models.auditing packet incoming/return.zip reviewer-packet.zip
uv run --no-env-file -m connected_models.auditing validate incoming/return.zip incoming/review.json
uv run --no-env-file -m connected_models.integration incoming/return.zip incoming/review.json MODEL_ID --version r1.runtime1
```

Give only the extracted packet to a different reviewer agent with `Read @AGENTS.md and complete @assignment.json`. See the [operator guide](../knowledge/notes/offline-curation-agent-kit.md#separate-auditor-handoff-and-technical-integration) for review criteria, projection evidence and the separate attributed admission command. Neither report validation nor projection publishes a model. To reproduce the committed example without the original ZIP, the validator and integrator also accept `data/curation/reviews/classical-mechanics-a-b01-bundle.json` with its corresponding review JSON.

The application credential variable is **META_API_KEY**. This overrides the variable name shown in Meta's generic documentation. The following commands stage project-derived candidates, run a paid extraction from the bundled NIST source packet, and report on a bundle:

```powershell
# Stage four supporting project-derived candidates, without publishing them.
uv run --no-env-file connected-models seed-candidates
# Make a paid offline extraction from the bundled NIST source packet.
uv run --env-file .env connected-models curate
# Produce a readable report of sources, extracted algebra, assumptions and checks.
uv run --no-env-file connected-models review-bundle
```

The curator receives the NIST equation with its source notation and a canonical interface, then extracts executable algebra and a symbol/source map. It does not receive the fixture's program expression. The published numerical example is checked independently before review. Incomplete or failing extractions remain candidates with diagnostics. Supporting accounting definitions are explicitly marked manual project derivations; they are not misrepresented as agent extractions.

Inspect a candidate with `candidate CANDIDATE_ID`. After checking source fidelity, applicability, interface meanings and assumptions, the owner records a scoped review:

```powershell
uv run --no-env-file connected-models review CANDIDATE_ID --decision accepted --reviewer owner --notes 'Describe the checked source and permitted scenario use'
uv run --no-env-file connected-models registry-list
```

Each model revision is immutable. A replacement definition needs a new version. A `withdrawn` review prevents new snapshots from using that candidate; saved runs keep their original evidence. Eligibility is snapshotted at the start of a short local run rather than revoked mid-calculation. This is a single-operator trust boundary: explicit local review commands carry publication authority, and the reviewer identity/scope are retained. The curator/composer inference roles have no publication tools and cannot approve their own outputs. Broader scientific approval policy remains unresolved.

Once all necessary versions are eligible, ask a self-contained question. For example:

```powershell
$question = @'
Annual delivered heat demand is 12000 kWh. Baseline resistance heating has seasonal performance 1 and the proposed heat pump has seasonal performance 3. Electricity has a flat tariff of 0.30 USD/kWh. The incremental upfront investment is 10000 USD. Use an annual effective real discount rate of 5 percent and a study horizon of 10 years. Assume the same delivered heat and comfort, constant real prices and annual savings paid at each year end, with no maintenance differences, replacements, cooling benefits or residual value. Calculate annual operating costs, annual savings and the investment net present value.
'@
uv run --env-file .env connected-models answer $question
uv run --env-file .env connected-models answer 'For the same annual delivered heat of 12000 kWh, compare baseline electric heating with seasonal performance 1 and a heat pump with seasonal performance 2.5, using a flat tariff of 0.25 USD/kWh in constant real prices. Exclude cooling benefits, maintenance differences, and changes in fixed charges. Calculate annual operating costs and savings only.'
uv run --no-env-file connected-models inspect RUN_ID
uv run --no-env-file connected-models report RUN_ID ANOTHER_RUN_ID
uv run --no-env-file connected-models usage
```

The first query-time step extracts a domain-independent list of typed facts (number, date or text), with exact quotes from the question. Numeric literals and supported adjacent units are checked against those quotes. The composer receives these facts and eligible stored definitions; each external input must reference a fact ID, and each derived input must reference an upstream node. It cannot emit a new numeric literal or use a remembered preset value. A structured graph object avoids nested JSON-string generation. The compiler checks and executes the resolved graph, saving both extraction evidence and proposed assignments to model inputs.

If the question omits required inputs, the result is `needs-input` with specific clarification questions and no calculated answer. Asking only for annual operating costs does not require an investment amount, horizon or discount rate. Unsupported model coverage remains `blocked`, with parsed inputs retained. This currently uses a self-contained follow-up question rather than persistent conversational state. Generated estimates stay out of silent bindings; the scoped consent for implied values is the fill-in opt-in above, and source curation never runs inline.

## Temporary rights waiver (default off)

`connected_models.integration` accepts `--relax-rights` for records whose
review verdict is needs-revision with every scientific check passed and only
rights-provenance failed. Guard-trap (`blocked`) verdicts, unverified checks,
supersession/duplication blockers, vocabulary, dimension, guard, reference,
and revision-collision gates all still refuse. Waived projections are stamped
in the projection evidence and model assumptions, and owner `review` decisions
on them should carry waiver notes. Reverse with a `withdrawn` review. This is
a temporary local-use bypass, not a substitute for corrected r2 revisions.

The parser is not tied to heating names: it can retain a number of apples, a birth date, or a person's name. Executing date/text operations or a new domain still requires suitable stored models and runtime support; the current engine is scalar numeric and the catalog holds 228 eligible models across heating, finance, economics, biology, computer science, mechanics, building energy, circuits, clinical arithmetic, demography, environmental accounting, orbital mechanics, and waves-and-optics. Executable numbers currently require explicit digit literals (commas and decimal/exponent forms are supported). Percentages remain in percent until the unit layer converts them. Exact quotes and numeric checks do not prove perfect semantic interpretation; the report exposes the selected fact-to-port assignments for inspection.
