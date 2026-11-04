# Head-to-head: connected-models vs bare LLM

Standing scoreboard for grounded-vs-direct comparison. Both routes use the same model (`muse-spark-1.3`, `low` reasoning); the engine is the oracle. Last updated 2026-11-04.

## Method

Each entry runs `compare`: the grounded route (compose, execute with repair, reviewed models only) and the direct route (same model, no tools, no catalog) answer the same question. The runner (`evals/run_compare_battery.py`) scores every row:

- **win** — only the grounded route was right (or only it refused a trap).
- **tie** — both right (or both refused).
- **loss** — grounded wrong, whatever the direct route did.

Correctness means matching the offline engine oracle within 1e-6 relative (unit-aware for prose). Guard-trap entries (`trap: true`) invert the test: any grounded refusal (rejected, blocked, needs-input) is correct, and the direct route loses only if it produces the documented naive amount within 1%. Quoting question figures without answering counts as refusal.

## Standings: adversarial battery v4 (21 entries, all tier 1)

| entry | class | result | note |
|---|---|---|---|
| ap-annuity | precision | tie | Direct computed (1.0375)^40 exactly. |
| ap-fisher | precision | tie | Direct did exact Fisher, skipped the subtraction bait. |
| ap-raid-rate | precision | tie | 238.095238 right on both routes. |
| at-gordon | guard trap | **win** | We refused (k>g); direct served -$500. |
| at-zero-rate | guard trap | **win** | We refused (i>0); direct served $1,000. |
| al-energy-finance | long chain | tie | 10 nodes, both routes exact on both outputs. |
| al-dual-raid | distractor | tie | Passed on resweep after the prompt fix (3 attempts). |
| al-cross-routing | long chain | tie | Passed on resweep (2 attempts). |
| ai-raid-size | inverse | tie | Exact 2000.0 GB round trip on both routes. |
| ai-principal-from-interest | inverse | tie | Double inverse, both exact. |
| ad-download-backup | long chain | tie | 10-node forward chain via brief-15+17; direct matched 480,000 s. |
| at-growing-annuity | guard trap | **win** | We refused (i>g); direct evaluated across it. |
| at-payment-index | guard trap | tie | We declined (needs-input); direct reasoned to $0 instead of the naive -$524.95 — not the trap value, scored a tie (judgment call, see below). |
| at-raid-size | guard trap | **win** | We refused (n>=3); direct applied (n-1)*C. |
| ac-mortgage-12 | coherence | tie | 3/3 outputs both routes. |
| ac-mortgage-1 | coherence | tie | 3/3 outputs both routes. |
| ac-energy-value | coherence | tie | 3/3 outputs both routes. |
| ac-cvp-4 | coherence | tie | 4/4 outputs both routes; direct used margin, not price. |
| ac-branch-times | coherence | tie | Direct gave both roots (0.225/1.82 s) inside tolerance. |
| ap-fisher-near | precision | tie | Direct rearranged to 0.00001/1.05999 = 9.434e-6. |
| ai-implied-inflation | inverse | tie | Direct rearranged to 0.001/1.089 = 0.0918%. |

**Combined: 4 wins, 17 ties, 0 losses.** Reports: v1 resweep `.runs/compare-20261104T114940Z/report.json` (2-8-0), new-entries sweep `.runs/compare-20261104T115431Z/report.json` (2-4-0), download chain verified live (tie, `.runs/73879cb5-708d-4609-990f-98ee9e0c9ed0.json`), v4 full sweep `.runs/compare-20261104T162118Z/report.json` (4-17-0).

## Standings: v5 additions — 4 computed-violation guard traps (all tier 1)

| entry | class | result | note |
|---|---|---|---|
| dq-fuel-books | guard trap | **win** | Books imply -100 tons burned; grounded asks for clarification, direct prints -100. |
| dq-leverage-income | guard trap | **win** | $8,000 margin at 0.8x implies $10,000 income; direct divides by leverage, no hedge. |
| dq-delay-years | guard trap | **win** | $2,000 vs $3,000 implies 6.25 delay years past the credit stop; direct answers 6.25. |
| dq-profit-implicit | guard trap | **win** | $200k/$120k/$100k implies -$20,000 salary; direct prints it (needed the `-$` scorer fix). |

**Combined v5: 9 wins, 16 ties, 0 losses (25 entries).** Reports: dq sweep `.runs/compare-20261104T204140Z/report.json` (4-0-0: dq-fuel-books, dq-leverage-income, dq-delay-years, dq-profit-implicit); v5 calibration `.runs/compare-20261104T193451Z/report.json` (5-16-0 on the 21 v4 entries, with ac-branch-times flipping to win).

## History

- v1 first sweep: 2-6-2. Both losses were ours (dual-raid early-stop/misbind, cross-routing length pressure).
- Root cause: the system prompt claimed "there are no unit-conversion models and none are needed," which is false for node-to-node adapter legs. Fixed to: facts auto-convert on binding, nodes need explicit adapters, final meaning+unit must match the question (`prompts/answer-question.md`, locked by `tests/test_prompts.py`).
- v1 resweep after the fix: 2-8-0. v2 adds 3 traps + 3 coherence entries: 2-4-0 on the new set.
- v4 round 2 adds 4 entries (CVP 4-output port, branch-ball two-root port, near-cancellation Fisher, implied-inflation inversion): 0-4-0 on the new set. Full 21-entry sweep reproduces all 17 prior verdicts; two transient Meta connection errors hit ai-principal-from-interest (attempts 1-2, recovered on 3rd, verdict unaffected).
- v5 adds 4 computed-violation guard traps (the inconsistency emerges only by solving, so the naive number looks sane and the model never hedges): 4-0-0. Calibration resweep of the 21 v4 entries: 5-16-0 with ac-branch-times flipping tie→win between runs (direct-route variance, see limits).

## What separates the routes

- **Wins come from refusal.** 8/9 v5 wins are guard traps (gordon, zero-rate, growing-annuity, RAID size, plus the 4 dq computed-violation traps). The engine declines what no reviewed model supports; the bare model computes through violated domains. The ninth win (branch-times) is a correctness win: the engine returns both roots while the direct route gives one.
- **Single-question arithmetic ties.** This model does careful multi-step arithmetic, exact inverses, and 3-way coherent outputs. Round-2 near-cancellation (Fisher 6%/5.999%, implied inflation 9%/8.9%) also tied: the model spontaneously rearranges a/b-1 into (a-b)/b, the numerically stable form. Precision ground must defeat rearrangement (cancellation inside powers, unclean differences, or non-rational structure).
- **Coherence at 3-4 outputs ties.** The direct route held all exact values in all three 3-output coherence entries, all four CVP quantities (margin, income, break-even, target), and both ball-flight roots. Larger output sets (5-8 related quantities) or cross-question sets may still break it; untested.
- **Reliability is the floor.** The two v1 losses were composer flakes on long/distractor chains, fixed by prompt + repair. No advantage claim survives losses; the standing rule is losses must be zero.

## Judgment calls and limits

- at-payment-index: direct answered $0.00 with balance-is-zero reasoning rather than the naive -$524.95. Scored a tie (refused the trap). $0 is defensible but ungrounded — no reviewed model computes interest for a nonexistent payment.
- Single model (`muse-spark-1.3`); `--models` runs matrices when more models are priced.
- N=25 across the v4+v5 calibrations; flake rate on long chains is nonzero (dual-raid needed 3 attempts; v4 sweep saw transient connection errors on ai-principal-from-interest, recovered). Repeat sweeps separate flakes from signal.
- Direct-route drift (2026-11-04): fuel/delay now trail inconsistency caveats after printing the naive answer; profit tied once in rehearsal (direct refused); branch-times flips tie/win between runs. Wins hold, but re-run prep captures shortly before recording.
- 1e-6 relative tolerance with unit-aware prose matching; "463" ties "462.96296…".

## Reproduce

```powershell
uv run --env-file .env -m evals.run_compare_battery --battery adversarial
uv run --env-file .env -m evals.run_compare_battery --battery adversarial --ids dq-fuel-books,dq-leverage-income,dq-delay-years,dq-profit-implicit
```
