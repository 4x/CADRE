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

The application accepts `MODEL_API_KEY` from its process environment. You can place that variable in your own `.env` and launch the following command yourself; repository agents must not inspect or load that file:

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

The catalog is currently handwritten fixture code. Real offline agent extraction, owner review/publication, durable registry loading, query-time agent composition and an interactive inspector are still required for the complete MVP. Only fixture execution is enabled until admission is implemented. The current contracts implement a small subset of the representation draft; they do not claim full v0 conformance.

The canonical delivery plan is [MVP milestones](knowledge/notes/mvp-build-sequence-and-extension-triggers.md); current project context is in [PROJECT_STATE.md](PROJECT_STATE.md). Source/evidence records and design decisions live in Project Memory under `knowledge/`.
