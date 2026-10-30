# Connected Models

Compose reusable quantitative models and inspect their inputs, assumptions, dependencies and results. The first runnable slice compares electric resistance heating with a heat pump, then connects operating savings to discounted investment value.

## Run the current prototype

Requires uv and Python 3.12 or newer. No third-party Python packages are required.

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models demo
uv --cache-dir .uv-cache run --no-env-file -m connected_models demo --performance 2 --investment 12000
uv --cache-dir .uv-cache run --no-env-file -m connected_models demo --question operating-cost
```

The synthetic default scenario uses 12,000 kWh of delivered annual heat, seasonal performance 3, a flat $0.30/kWh tariff, $10,000 incremental investment, a ten-year study period and a 5% annual effective real discount rate. It yields $2,400 annual operating savings and $8,532.16 net present value under those assumptions. These are illustrative inputs, not household measurements or purchasing advice. Every run saves its complete model definitions, input bindings, provenance and intermediate results under `.runs/`; earlier runs are preserved.

The operating-cost and investment questions reuse the same component models and executor. Change performance, tariff or investment with command options. The present-value model currently requires a positive discount rate and an integer horizon from 1 to 100 years. Performance must represent seasonal whole-system delivered heat divided by electricity use; a single temperature's COP rating is insufficient. Maintenance, cooling benefits, replacements, incentives, tariff escalation and uncertainty propagation are excluded from this initial calculation.

## Meta inference setup

The public settings in `inference.toml` select `muse-spark-1.3` in Standard mode and a $150 application-wide ceiling. The adapter uses the [Meta API route documented for coding agents](https://dev.meta.ai/docs/coding-agents). It does not change the coding agent running this session.

The application accepts `META_API_KEY` from its process environment. You can place that variable in your own `.env` and launch the following command yourself; repository agents must not inspect or load that file:

```powershell
uv --cache-dir .uv-cache run --env-file .env -m connected_models meta-smoke
```

This sends one bounded paid structured-output request. The command prints only connection status, model, request identifier and conservative cost. It never displays the key or raw API response. The agent has not run this live check. Offline tests use a fake transport and placeholder credential.

The persistent `.usage/meta.sqlite3` ledger reserves worst-case token cost before sending and settles against reported usage. Failed or ambiguous requests retain their reservation and are not retried automatically. Preserve this ledger across runs. Its ceiling covers calls through this application; spending in other tools or accounts is outside its accounting. Prices are pinned to the [Meta Standard-mode rates checked October 29, 2026](https://dev.meta.ai/docs/pricing-rate-limits); reverify pricing before changing models or rates. Use an account-side spending limit as well if the provider supports it.

## Test

```powershell
uv --cache-dir .uv-cache run --no-env-file -m unittest discover -s tests -v
```

Tests compare execution with a separately summed Decimal cash flow and NIST Handbook 135 (2020), equation 3-7, printed page 29 ($457.97 for five year-end payments of $100 discounted at 3%). They also exercise dimensional and semantic rejection, cycles, missing inputs, unsafe expressions, model substitution, saved-run preservation and persistent budget controls. All tests run without network calls.

## Implementation status

Implemented: bounded scalar algebra, explicit per-port context and meaning checks, ratio-unit conversions, graph compilation, deterministic evaluation, immutable run snapshots, two fixture compositions and a budgeted Meta connection-check adapter. Expressions are interpreted through an allowlisted AST; arbitrary Python code is not executed.

The `demo` command uses handwritten fixtures. The separate registry workflow now supports offline source extraction, candidate storage, explicit owner review/publication, withdrawal and query-time composition against eligible stored versions. Eighteen offline tests pass, including fake curator/composer responses. Live extraction and composition remain unverified until credential access and owner review complete. The inspector currently prints saved run evidence; a graphical workbench remains future work. The contracts implement a bounded subset of the representation draft, not full v0 conformance.

## Curate, review and reuse models

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

Each model revision is immutable. A replacement definition needs a new version. A `withdrawn` review prevents new snapshots from using that candidate; saved runs keep their original evidence. Eligibility is snapshotted at the start of a short local run rather than revoked mid-calculation. This is a single-operator trust boundary: commands run by the owner carry review authority. Agent extraction or composition cannot publish its own models.

Once all necessary versions are eligible, ask a question using the supplied illustrative scenario inputs:

```powershell
uv --cache-dir .uv-cache run --env-file .env -m connected_models answer 'Compare annual heating costs and the discounted value of the upgrade'
uv --cache-dir .uv-cache run --env-file .env -m connected_models answer 'Compare annual operating costs only' --performance 2 --tariff 0.25
uv --cache-dir .uv-cache run --no-env-file -m connected_models inspect RUN_ID
```

The composer sees only eligible stored definitions and explicit scenario values. It proposes bindings; the deterministic compiler validates and executes them. It cannot invent numeric inputs or curate a missing model during answering. Unsupported questions and invalid proposals are saved with actionable blocked/rejected diagnostics. Generated estimates remain disabled until a scoped consent flow exists; inputs missing from this bounded scenario remain unresolved. Old results retain pinned definitions, vocabulary, review identifiers, input origins and dependency traces.

Local runtime artifacts are stored in `.registry/`, `.runs/` and `.usage/`, all excluded from version control. Preserve the registry and spend ledger when continuing the prototype.

The canonical delivery plan is [MVP milestones](knowledge/notes/mvp-build-sequence-and-extension-triggers.md); current project context is in [PROJECT_STATE.md](PROJECT_STATE.md). Source/evidence records and design decisions live in Project Memory under `knowledge/`.
