# Setup and running

Requires uv and Python 3.12 or newer (`.python-version` pins 3.14 for development). No third-party runtime packages are required. Answering a question uses live inference and needs `META_API_KEY` in the environment (see below); inspection, reports, tests and curation tools run offline.

```powershell
uv sync
uv run --env-file .env connected-models answer 'Delivered heat is 12000 kWh. Heat pump seasonal performance is 3. Tariff is 0.30 USD/kWh. What is the annual operating cost?'
uv run --no-env-file connected-models inspect RUN_ID
uv run --no-env-file connected-models report RUN_ID
uv run --no-env-file connected-models usage
```

Run commands from the repo root. Runtime state (`.runs/`, `.registry/`, `.usage/`) and `inference.toml` resolve from the working directory by design; prompts and the bundled NIST source packet ship inside the installed package, so `answer`, `inspect`, `report`, `revise` and `replay` work from any directory once installed. The curation/auditing/integration operations consume repository content and must run from the root.

## Meta inference setup

The public settings in `inference.toml` select `muse-spark-1.3` in Standard mode and a $150 application-wide ceiling. The adapter uses the [Meta API route documented for coding agents](https://dev.meta.ai/docs/coding-agents). Model selection precedence is `--model` flag, then the `LLM` environment variable, then `inference.toml`; every name must have researched rates in `MODEL_PRICING` or loading fails closed. `answer` and `compare` accept `--model`; the battery runner accepts `--models a,b` to sweep entries across models. The ledger attributes settled spend per model (`usage` shows `by_model`); rows recorded before attribution read as `unattributed`.

The application accepts `META_API_KEY` from its process environment. Launch a bounded connection check with:

```powershell
uv run --env-file .env connected-models meta-smoke
```

This sends one bounded paid structured-output request. The command prints only connection status, model, request identifier and conservative cost. It never displays the key or raw API response. Offline tests use a fake transport and placeholder credential.

The persistent `.usage/meta.sqlite3` ledger reserves worst-case token cost before sending and settles against reported usage. Failed or ambiguous requests retain their reservation and are not retried automatically. Preserve this ledger across runs. Its ceiling covers calls through this application; spending in other tools or accounts is outside its accounting. Prices are pinned to the [Meta Standard-mode rates checked October 29, 2026](https://dev.meta.ai/docs/pricing-rate-limits); reverify pricing before changing models or rates. Use an account-side spending limit as well if the provider supports it.

## Test

```powershell
uv run pytest -q
uv run python -m unittest discover -s tests -t . -q
```

Both runners execute the same offline suite (no network calls); the `unittest` form is the stdlib fallback. Tests compare execution with a separately summed Decimal cash flow and NIST Handbook 135 (2020), equation 3-7, printed page 29 ($457.97 for five year-end payments of $100 discounted at 3%). They also exercise dimensional and semantic rejection, cycles, missing inputs, unsafe expressions, model substitution, saved-run preservation and persistent budget controls.

Static gates (also enforced by CI on Python 3.12 and 3.14):

```powershell
uv run ruff check src tests evals
uv run ruff format --check src tests evals
uv run mypy -p connected_models -p tests -p evals
```
