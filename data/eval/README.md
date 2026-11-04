# Chain battery

Thirteen queries where connected-models should beat a plain LLM doing in-context arithmetic: exact inverse solving, guarded domains, unit/dimension discipline, and multi-hop chains with provenance. All thirteen are tier 1 and complete live as of 2026-11-04; five flipped from tier 2 when their bridges (context r2s and meaning adapters) were admitted. The runner still reports a tier-2 completion with correct values as `fixed`, so future blocked-until-bridged entries are detected automatically.

## Run it

Needs live inference; run with credentials:

```powershell
uv --cache-dir .uv-cache run --env-file .env evals/run_chain_battery.py
uv --cache-dir .uv-cache run --env-file .env evals/run_chain_battery.py --ids t1-fisher,t1-dosing
uv --cache-dir .uv-cache run --env-file .env evals/run_compare_battery.py --battery deep
uv --cache-dir .uv-cache run --env-file .env evals/run_compare_battery.py --battery deep --models muse-spark-1.3
```

`--models` sweeps every selected entry once per model (each name validated against `MODEL_PRICING` before any call is sent). Rows carry the model actually used; the report adds the model list and the ledger's per-model spend. Only one model is priced today, so multi-model matrices await researched rates.

## Files

- `chain-battery.json` — entries with questions, oracle amounts, tiers, and the blocker each tier-2 entry waits on. Oracle amounts were computed offline with `runtime.execute` (fixture purpose); tier-2 links ran stepwise with hand wiring.
- `deep-battery.json` — eight longer entries: chains up to 9 nodes, mixed forward/inverse views, fork graphs, and fact-routing stress. All eight are tier 1 with end-to-end offline oracles as of 2026-11-04; d4 flipped when the brief-14 schedule-rate adapter was admitted.
- `adversarial-battery.json` — ten head-to-head entries where a bare LLM is expected to lose: precision traps, guard traps (`trap: true`, refusal is correct, compare-runner only), long fork-join chains, and multi-hop inverses. The sweep scores each row win/tie/loss: win means only the grounded route was right.
- `../evals/run_chain_battery.py` — the chain runner. Matches live outputs to oracle values by meaning within 1e-6 relative tolerance, prints a verdict table, and saves `.runs/eval-<timestamp>/report.json`.
- `../evals/run_compare_battery.py` — the compare runner (`--battery chain|deep`). Runs `compare` per entry (grounded answer vs direct LLM answer, engine as oracle) and saves `.runs/eval-<timestamp>-compare-battery/report.json`.

## Design notes

- The battery measures the composer, not the engine: the engine is the independent oracle.
- `compat-audit` (`-m connected_models compat-audit`) reports the structural edges tier-2 entries wait for; use it to confirm a bridge landed before flipping an entry to tier 1.
- Known engine limit surfaced by the battery: exponents above magnitude 100 reject, so 360-payment loans cannot execute yet (t1-loan-single uses 30 annual payments).
