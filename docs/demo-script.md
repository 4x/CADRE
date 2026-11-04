# Live demo script — one command sequence, no surprises

The bounded end-to-end workflow a judge can inspect: Dana's inputs, five model
connections, deterministic execution, results with provenance. Every step below
was run against this checkout; expected outputs are exact. Timed video plan:
[demo-video.md](demo-video.md).

## Prep (5 minutes, do it in this order)

```powershell
uv sync
uv run --no-env-file connected-models demo-seed
```

Run `demo-seed` **last**, after any revision experiments: the web page opens the
newest saved run per scenario, so a stale revision would displace the base
$8,532.16 run from the "saved investment" slot. Then capture the run ids once:

```powershell
$seed = uv run --no-env-file connected-models demo-seed 2>$null | ConvertFrom-Json
$op = $seed.runs.'operating-cost'.run_id
$inv = $seed.runs.investment.run_id
```

(All CLI JSON goes to stdout; `INFO:` progress lines go to stderr, so `2>$null`
keeps pipes clean.)

Start the web page only if you need the visual beats:

```powershell
uv run --env-file .env connected-models serve --port 8000
```

Expected: `Connected Models demo: open http://127.0.0.1:8000/ in a browser.`
With `--no-env-file` the page still opens saved runs, revises, and reports, but
Ask is blocked because the key never reaches the process.

## The sequence

### 1. The hook — grounded engine vs bare LLM (live, ~25s)

```powershell
uv run --env-file .env connected-models compare 'Delivered heat is 12000 kWh per year. Baseline resistance heating has seasonal performance 1 and the proposed heat pump has seasonal performance 3. Tariff is 0.30 USD/kWh. The heat pump costs 10000 USD with a 5% real discount rate over 10 years. What is the net present value?'
```

Expected: `grounded: completed in ~18s`, `n_npv: 8532.16... USD
(net_present_value)`, a `direct:` prose answer, then `agreement: agree` with the
expected/matched pair, and a `saved:` path. Say: "Same question, same model.
Only one side shows its work."

Fallback: if the API fails, say so and continue at step 2 — everything from
here on is offline, and determinism under failure is itself the demo. If the
direct route disagrees instead, even better: point at the verdict line.

### 2. Inspectable inputs — every number has a quote (offline)

```powershell
uv run --no-env-file connected-models inspect $inv
```

Expected: the `heating-investment` composition — five nodes
(`baseline-energy`, `upgrade-energy`, `baseline-cost`, `upgrade-cost`,
`annual-savings`, present value, `investment-npv`), each binding carrying its
amount, unit, meaning, and exact question quote. Point at one `evidence` field.

Fallback: if the id is mistyped the CLI now says `That run id is not valid`
or `No saved run has that id` with recovery hint — re-run the `$seed` capture.

### 3. Execution and results — the receipt (offline)

```powershell
uv run --no-env-file connected-models replay $inv
uv run --no-env-file connected-models report $inv
```

Expected: `"matched": true` with empty `output_mismatches`; then `Report:
.runs\report-<uuid>.html`. Open the report: metric cards 3600 / 1200 / 2400
USD and NPV **8,532.16 USD**, expandable steps with expressions, sources,
assumptions, and reviews. Say: "Deterministic. Replay it in a year, get the
same bytes."

Fallback: none needed — both commands touch only saved local files.

### 4. What if — revise without re-rolling the dice (offline)

```powershell
uv run --no-env-file connected-models revise $inv --set upgrade-energy.performance=2 --set baseline-cost.tariff=0.25 --set upgrade-cost.tariff=0.25 --set investment-npv.investment=12000
```

Expected: `"status": "completed"`, a new `run_id`, `investment-npv` of
**-417.40 USD**, and a `diff` table with signed deltas. The original run is
preserved (`revised_from`). Say: "Same models, same evidence, new scenario —
the pessimistic case flips the decision."

Fallback: on a bad `--set` the CLI prints the exact expected shape, e.g.
`Invalid --set '...'; use node.input=amount` — fix the flag and retry. On the
web page the same revision is two sliders plus Apply, with identical figures.

### 5. What if, continued — the animated graph (offline except Ask)

In the browser: click the `investment` sample chip, press Answer (live), watch
the graph animate node by node, then use the What-if sliders (offline) and open
a calculation step plus the standalone evidence report.

Expected: metric cards land at 3600 / 1200 / 2400 USD and NPV $8,532.16; the
"What changed" table mirrors step 4; the evidence report needs zero API calls.

Fallback: if the live call fails on camera, click "open saved investment"
instead — the animation is identical.

### 6. The skill — every agent gets this calculator (offline)

```powershell
uv run --no-env-file connected-models registry-list 2>$null | Select-Object -First 8
```

Expected: eligible stored model versions — the five `demo-seed` fixtures on a
fresh clone (282 entries on the curated dev machine). Say: "And it ships as a
Muse skill — any agent in this
repo answers quantitatively through the engine instead of hallucinating
arithmetic." Keep this beat to the registry glimpse plus one cited run id.

## Shot list for the demo video

Timed narration is in [demo-video.md](demo-video.md); these are the frames:

1. Terminal, `compare` output: `grounded:` figures beside `direct:` prose,
   closing on the `agreement:` verdict line.
2. Browser: sample chip → Answer → graph animating node by node → metric cards
   ($8,532.16).
3. Browser: sliders 3→2 and investment→12000 → Apply → "What changed" deltas.
4. Browser: expanded calculation step (expression, quote, source, review) →
   standalone evidence report.
5. Terminal: `replay` output closing on `"matched": true`.
6. Terminal or Muse session: cited run id answering a numbers question.
7. Close: browser graph full-frame, then repo URL and the thesis line.

## If anything breaks live

- API down or key missing: say so on camera; steps 2–4 plus the saved-run page,
  sliders, reports, and replay are fully offline.
- Wrong run id: the CLI names the problem and points at `demo-seed`; re-run
  the `$seed` capture.
- Port 8000 busy: `serve` says the address may be in use — retry with
  `--port 8001` and open the printed URL.
- Page shows the revised (-417.40) run instead of the base: a revision is
  newer than the seed — re-run `demo-seed` right before recording.
