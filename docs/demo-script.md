# Live demo script — every number has a receipt

The centerpiece a judge can inspect: two questions that just work —
a fully grounded two-model chain with exact amounts, and a partially
grounded forecast with its receipt attached. Then the offline
heat-pump workflow. Every step below was run against this checkout;
expected outputs are exact. Timed video plan:
[demo-video.md](demo-video.md). Four acts, ~3 minutes.

No bare-LLM comparison appears in this demo: the answers stand on
their own receipts. (`compare` remains a measurement tool, with
`agree` / `disagree` / `guarded` / `unjudged` verdicts.)

## Prep (10 minutes, do it in this order)

```powershell
uv sync
uv run --no-env-file connected-models demo-seed
```

Run `demo-seed` **last**, after any revision experiments: the web page
opens the newest saved run per scenario, so a stale revision would
displace the base $8,532.16 run from the "saved investment" slot. Then
capture the run ids once:

```powershell
$seed = uv run --no-env-file connected-models demo-seed 2>$null | ConvertFrom-Json
$op = $seed.runs.'operating-cost'.run_id
$inv = $seed.runs.investment.run_id
```

(All CLI JSON goes to stdout; `INFO:` progress lines go to stderr, so
`2>$null` keeps pipes clean.)

Pre-run the two live answers (~30–90s each) and save their terminal
output for Act 1, Act 2, and break-glass:

```powershell
uv run --env-file .env connected-models answer 'A binary contract pays 100 USD if a candidate wins an election. The market implies a 60 percent win probability. The risk-free discount rate is 5 percent for a horizon of 1 period. At net odds of 1 to 1, what Kelly fraction of bankroll should be staked, and what is the fair value of the contract today?' 2>$null | Tee-Object .runs/demo-ans-kelly.txt
$env:CADRE_ALLOW_LLM_STEPS = '1'; uv run --env-file .env connected-models answer 'EUR/USD now trades at 1.12 US dollars per euro. The ECB policy rate is 2.65 percent and the Fed policy rate is 4.00 percent. What could we expect the EUR/USD exchange rate to be half a year from now?' 2>$null | Tee-Object .runs/demo-ans-fx.txt
```

Expected: a `completed` / `full` Kelly record (0.2 and 57.14) and a
`completed` / `partial` FX record (1.12746 with one LLM step). Confirm
both shapes before recording; exact outputs are quoted under each act.

Start the web page only if you need the visual beats:

```powershell
uv run --env-file .env connected-models serve --port 8000
```

Expected: `Connected Models demo: open http://127.0.0.1:8000/ in a
browser.` With `--no-env-file` the page still opens saved runs, revises,
reports, and browses models, but Ask is blocked because the key never
reaches the process.

## Act 1 — The hook: an election bet, priced two ways (live, ~60s)

One command, on camera:

```powershell
uv run --env-file .env connected-models answer 'A binary contract pays 100 USD if a candidate wins an election. The market implies a 60 percent win probability. The risk-free discount rate is 5 percent for a horizon of 1 period. At net odds of 1 to 1, what Kelly fraction of bankroll should be staked, and what is the fair value of the contract today?'
```

Expected (latencies vary; the numbers do not):

```text
"status": "completed",
"grounding": "full",
"outputs": {
  "n_kelly": { "amount": 0.19999999999999996, ... },
  "n_fair": { "amount": 57.14285714285714, ... }
}
```

Say: "Twenty percent of bankroll, fifty-seven fourteen fair value —
two reviewed models, one chain, fully grounded. Now watch where those
numbers live." Open the run in the browser: the result graph shows the
two model boxes with quoted inputs. Then open the Models tab, pick the
Kelly card: "Kelly optimal wealth fraction for a simple bet" — plain
English title, the formula, guards, source, and the reviewer's
permitted use. "Every number has a receipt, and every model has a
name."

Fallback: if the API fails, say so and show the pre-run capture
(`Get-Content .runs/demo-ans-kelly.txt`) — determinism under failure is
itself the demo.

## Act 2 — Half-questions: the forecast with a receipt (~50s)

Show the FX capture (pre-run with `CADRE_ALLOW_LLM_STEPS=1`), or run
it live on camera:

```powershell
$env:CADRE_ALLOW_LLM_STEPS = '1'; uv run --env-file .env connected-models answer 'EUR/USD now trades at 1.12 US dollars per euro. The ECB policy rate is 2.65 percent and the Fed policy rate is 4.00 percent. What could we expect the EUR/USD exchange rate to be half a year from now?'
```

Expected: `"status": "completed"`, `"grounding": "partial"`,
`"n_exp": {"amount": 1.1274611082145514, ...}`, one `llm_steps` entry
(`s_fwd`, covered-interest-parity forward) feeding the reviewed
expectation model.

Say: "One twelve spot, two policy rates, six months out: 1.1275. No
reviewed model covers the forward link, so the engine calculates that
one step itself — and marks exactly that link. Partial grounding, full
honesty." Open the Models tab on the forward-implied card to show the
reviewed half of the chain with its BIS source.

Fallback: same as Act 1 — show the capture; the numbers above are the
evidence.

## Act 3 — Conduits montage: Dana's receipt (offline, ~65s)

The heat-pump workflow, fully offline from the seed. Dana's inputs, five
model connections, deterministic execution, results with provenance.

Inspectable inputs — every number has a quote:

```powershell
uv run --no-env-file connected-models inspect $inv
```

Expected: the `heating-investment` composition — five nodes
(`baseline-energy`, `upgrade-energy`, `baseline-cost`, `upgrade-cost`,
`annual-savings`, present value, `investment-npv`), each binding
carrying its amount, unit, meaning, and exact question quote. Point at
one `evidence` field.

Fallback: if the id is mistyped the CLI now says `That run id is not
valid` or `No saved run has that id` with recovery hint — re-run the
`$seed` capture.

Execution and results — the receipt:

```powershell
uv run --no-env-file connected-models replay $inv
uv run --no-env-file connected-models report $inv
```

Expected: `"matched": true` with empty `output_mismatches`; then
`Report: .runs\report-<uuid>.html`. Open the report: metric cards 3600
/ 1200 / 2400 USD and NPV **8,532.16 USD**, expandable steps with
expressions, sources, assumptions, and reviews. Say: "Deterministic.
Replay it in a year, get the same bytes."

Fallback: none needed — both commands touch only saved local files.

What if — revise without re-rolling the dice:

```powershell
uv run --no-env-file connected-models revise $inv --set upgrade-energy.performance=2 --set baseline-cost.tariff=0.25 --set upgrade-cost.tariff=0.25 --set investment-npv.investment=12000
```

Expected: `"status": "completed"`, a new `run_id`, `investment-npv` of
**-417.40 USD**, and a `diff` table with signed deltas. The original run
is preserved (`revised_from`). Say: "Same models, same evidence, new
scenario — the pessimistic case flips the decision."

Fallback: on a bad `--set` the CLI prints the exact expected shape, e.g.
`Invalid --set '...'; use node.input=amount` — fix the flag and retry.

The animated graph (browser, offline except Ask): click the `investment`
sample chip, press Answer (live), watch the graph animate node by node,
then use the What-if sliders (offline) and open a calculation step plus
the standalone evidence report. Expected: metric cards land at 3600 /
1200 / 2400 USD and NPV $8,532.16; the "What changed" table mirrors the
revision above; the evidence report needs zero API calls.

Fallback: if the live call fails on camera, click "open saved
investment" instead — the animation is identical.

## Act 4 — Future and use cases: every agent gets this calculator (~35s)

```powershell
uv run --no-env-file connected-models registry-list 2>$null | Select-Object -First 8
```

Expected: eligible stored model versions — the five `demo-seed`
fixtures on a fresh clone (581 entries on the curated dev machine). Say:
"And it ships as a Muse skill — any agent in this repo answers
quantitatively through the engine instead of hallucinating arithmetic."
Keep this beat to the registry glimpse plus one cited run id. Close:
"One model's output is another model's input. No invented numbers —
every figure has a receipt. Connected Models."

## Shot list for the demo video

Timed narration is in [demo-video.md](demo-video.md); these are the
frames:

1. Terminal, live Kelly `answer`: `completed`, `full`, 0.2 and 57.14.
2. Browser: result graph, then the Models tab Kelly card (title,
   formula, review).
3. Terminal: FX `partial` 1.12746 with the step receipt beside the
   Models forward-implied card.
4. Browser: sample chip → Answer → graph animating node by node →
   metric cards ($8,532.16).
5. Browser: sliders 3→2 and investment→12000 → Apply → "What changed"
   deltas.
6. Browser: expanded calculation step (expression, quote, source,
   review) → standalone evidence report.
7. Terminal: `replay` output closing on `"matched": true`.
8. Close: browser graph full-frame, then repo URL and the thesis line.

## Break glass (live inference is down)

Use this section — and only this section — when the API fails. Nothing
here needs a key or network:

1. Say on camera that live inference is unavailable; the captures below
   are pre-run real output, labeled with capture time (`Get-Item
   .runs/demo-ans-*.txt | Select-Object Name, LastWriteTime`).
2. Show both captures in order:
   `Get-Content .runs/demo-ans-kelly.txt`,
   `Get-Content .runs/demo-ans-fx.txt`. Each shows a completed record
   with its receipts.
3. Optionally open one saved answer record: the `saved:` line in each
   capture names a `.runs\<uuid>.json` file holding the full grounded
   record and latency.
4. Continue at Act 3 — the heat-pump montage, revision, sliders,
   reports, and replay are fully offline.

## If anything breaks live

- API down or key missing: say so on camera; use Break glass above,
  then Acts 3–4 offline.
- An amount differs from the script quote: report what the run showed,
  show the pre-run capture, continue. Never narrate a number the
  current run did not show.
- Wrong run id: the CLI names the problem and points at `demo-seed`;
  re-run the `$seed` capture.
- Port 8000 busy: `serve` says the address may be in use — retry with
  `--port 8001` and open the printed URL.
- Page shows the revised (-417.40) run instead of the base: a revision
  is newer than the seed — re-run `demo-seed` right before recording.
- `Tee-Object` files missing: re-run the two prep answers; each
  re-saves its capture.
