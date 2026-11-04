# Live demo script — the bare LLM prints the trap; we refuse it

The centerpiece a judge can inspect: four verified questions where the
grounded engine asks for clarification and the bare LLM — same question,
same model (`muse-spark-1.3`) — prints the naive number as its answer. The
heat-pump workflow stays as the offline-safe beat in Act 3. Every step
below was run against this checkout; expected outputs are exact. Timed
video plan: [demo-video.md](demo-video.md). Four acts, ~3 minutes.

The four traps live in `data/eval/adversarial-battery.json` (v5, `dq-`
entries). Each runs with fill-in-assumptions **off**: the battery entries
carry `fill_in_assumptions: false`, and single-question `compare` defaults
to off — do **not** pass `--fill-in-assumptions` for any trap command.

| Trap | Question | Bare LLM prints | Why it is wrong |
| --- | --- | --- | --- |
| dq-fuel-books | 500 t bought, 100 t opening, 700 t closing — how much burned? | `-100 tons` | Closing stock exceeds opening plus purchases; negative fuel burn is unphysical |
| dq-leverage-income | $8,000 margin at 0.8x leverage — operating income? | `$10,000` | Income above contribution margin implies negative fixed costs |
| dq-delay-years | $2,000 at full retirement, getting $3,000 — years delayed? | `6.25 years` | Delayed-retirement credits stop at 4 years (age 70) |
| dq-profit-implicit | $200k revenue, $120k costs, $100k true profit — salary given up? | `-$20,000` | True profit above accounting profit implies a negative salary |

On all four, grounded returns `needs-input` with the clarification
prompt instead of a number; the direct side prints the naive amount as
its answer. Win = only the grounded route was right (here: only it
refused). Fresh evidence (2026-11-04): single-question compares
`.runs\0f9793f0-*.json` (fuel), `.runs\22795754-*.json` (leverage),
`.runs\b76a5bae-*.json` (delay), `.runs\f9985db5-*.json` (profit), plus
the official sweep `.runs\compare-20261104T204140Z\report.json`
(win=4 tie=0 loss=0), all at registry size 282 eligible.

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

Pre-run the four trap compares (live; ~15–60s each) and save their
terminal output for Act 2 and break-glass:

```powershell
uv run --env-file .env connected-models compare 'We bought 500 tons of diesel, started the year with 100 tons in the tank, and ended with 700. How much did we burn?' 2>$null | Tee-Object .runs/demo-cmp-fuel.txt
uv run --env-file .env connected-models compare 'Our contribution margin is $8,000 and our operating leverage is 0.8x. What''s our operating income?' 2>$null | Tee-Object .runs/demo-cmp-leverage.txt
uv run --env-file .env connected-models compare 'My statement says $2,000 at full retirement, and I''m getting $3,000. How many years did I delay?' 2>$null | Tee-Object .runs/demo-cmp-delay.txt
uv run --env-file .env connected-models compare 'Our shop made $200,000 in revenue with $120,000 in costs, for a true profit of $100,000. What salary did I give up to run it?' 2>$null | Tee-Object .runs/demo-cmp-profit.txt
```

(PowerShell single-quoted strings double the apostrophe: `What''s`,
`I''m`. `$` stays literal inside single quotes.)

Expected per file: `grounded: needs-input`, the `error:` clarification
line, `direct:` prose ending in the naive number, `agreement: unjudged`,
and a `saved:` path. Confirm all four show the refusal-vs-number split
before recording; exact outputs are quoted under each act.

Optional one-line re-certification of all four through the official
scorer (same questions, same fill-in-off flag from the battery):

```powershell
uv run --env-file .env python -m evals.run_compare_battery --battery adversarial --ids dq-fuel-books,dq-leverage-income,dq-delay-years,dq-profit-implicit
```

Expected: a header row plus one row per trap (`dq-fuel-books pass
unjudged win ...`, etc.) and `head-to-head: win=4 tie=0 loss=0
battery-fail=0  report: <repo>\.runs\compare-<stamp>\report.json` (the
report path prints absolute).

Start the web page only if you need the visual beats:

```powershell
uv run --env-file .env connected-models serve --port 8000
```

Expected: `Connected Models demo: open http://127.0.0.1:8000/ in a
browser.` With `--no-env-file` the page still opens saved runs, revises,
and reports, but Ask is blocked because the key never reaches the
process.

## Act 1 — The hook: impossible books (live, ~25s)

The fastest trap (~20s end to end, usually 1 grounded attempt). Run
it live on camera:

```powershell
uv run --env-file .env connected-models compare 'We bought 500 tons of diesel, started the year with 100 tons in the tank, and ended with 700. How much did we burn?'
```

Expected (latencies vary; the verdict lines do not):

```text
question: We bought 500 tons of diesel, started the year with 100 tons in the tank, and ended with 700. How much did we burn?
model: muse-spark-1.3
grounded: needs-input in 12.8s (1 attempt(s))
  error: Please clarify the conflicting or ambiguous statements in the question.
direct: 6.1s
  Assuming no other diesel added or removed except the purchase and burning, and all figures are in same tons:

  Available = starting + bought = 100 + 500 = 600 tons
  Burned = available - ending = 600 - 700 = -100 tons

  **Burned: -100 tons**

  That is negative, so the numbers are inconsistent - you can't end with more than you started with + bought unless there was unrecorded supply / measurement error.
agreement: unjudged
saved: .runs\0f9793f0-c20b-4320-b98e-048b9c0df3b0.json
```

(Latencies and attempt counts vary run to run; the refusal-vs-number
split does not. The direct side's wording also varies — this run
appends a caveat sentence, but only after printing `**Burned: -100
tons**` as its answer.)

Say: "Same question, same model. One side answered: negative one
hundred tons of diesel. The other asked what was wrong with the books."
Point at the `grounded:` refusal beside the `direct:` prose, closing on
the `agreement: unjudged` line (unjudged because the grounded side
produced no outputs to check — the refusal IS the right answer on a
trap).

Fallback: if the API fails, say so and show the pre-run capture
(`Get-Content .runs/demo-cmp-fuel.txt`) — determinism under failure is
itself the demo. If the direct side hedges or refuses instead of
printing `-100`, that run is a tie, not a win: say so honestly and show
the pre-run capture, which printed the naive number as its answer.

## Act 2 — The comparison: three more traps (pre-run, ~50s)

Each trap below was pre-run in prep; on camera show each capture in
turn. The pattern repeats: every stated number looks sane, the violation
emerges only from solving, and the bare model prints through it.

### 2a. Leverage — income above margin (~15s)

```powershell
Get-Content .runs/demo-cmp-leverage.txt
```

Expected: `grounded: needs-input` (1 attempt, 17.3s fresh; up to 3
attempts in rehearsal) with the same clarification `error:`; `direct:`
prose ending in:

```text
Operating Income = $8,000 / 0.8 = **$10,000**

**Operating income: $10,000**
```

Say: "Eight thousand dollars of margin cannot hold ten thousand of
income. The engine's inverse back-check catches it; the bare model
divides and moves on."

Fallback: same as Act 1 — a hedging direct side is an honest tie; the
pre-run capture is the evidence.

### 2b. Delay — credits past age 70 (~15s)

```powershell
Get-Content .runs/demo-cmp-delay.txt
```

Expected: `grounded: needs-input` (3 attempts, 39.4s fresh; 1
attempt in the re-certifying sweep — counts vary) with the same
clarification `error:`; `direct:` prose ending in:

```text
Years = 50% / 8% per year = 6.25 years

**Delayed time = 6.25 years, i.e. 75 months.**

Note: this exceeds the current maximum delay to age 70 of 3-4 years, so in practice COLAs or an old statement must account for part of the difference.
```

(As with fuel, the caveat trails the printed answer — the answer itself
is still the naive 6.25.)

Say: "Delayed-retirement credits stop at four years. Six point two five
is arithmetic without the guardrail."

Fallback: same as Act 1.

### 2c. Profit — the negative salary (~15s)

```powershell
Get-Content .runs/demo-cmp-profit.txt
```

Expected: `grounded: needs-input` (1 attempt, 17.4s fresh) with
the same clarification `error:`; `direct:` prose ending in:

```text
$100,000 = $80,000 - foregone salary
foregone salary = $80,000 - $100,000

Foregone salary = -$20,000 dollars
```

Say: "True profit above accounting profit means you paid yourself
negative twenty thousand dollars. The engine refuses; the bare model
bills you."

Fallback: same as Act 1. Note this trap tied once in rehearsal (the
direct side refused that run) — if it ties live, say so and show the
pre-run win.

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
fixtures on a fresh clone (282 entries on the curated dev machine). Say:
"And it ships as a Muse skill — any agent in this repo answers
quantitatively through the engine instead of hallucinating arithmetic."
Keep this beat to the registry glimpse plus one cited run id. Close:
"One model's output is another model's input. No invented numbers —
every figure has a receipt. Connected Models."

## Shot list for the demo video

Timed narration is in [demo-video.md](demo-video.md); these are the
frames:

1. Terminal, live fuel-books `compare`: `grounded: needs-input`
   refusal beside `direct:` prose printing `-100 tons`, closing on
   `agreement: unjudged`.
2. Terminal, three `Get-Content` captures in turn: `$10,000` income,
   `6.25 years`, `-$20,000` salary — each beside its grounded refusal.
3. Browser: sample chip → Answer → graph animating node by node →
   metric cards ($8,532.16).
4. Browser: sliders 3→2 and investment→12000 → Apply → "What changed"
   deltas.
5. Browser: expanded calculation step (expression, quote, source,
   review) → standalone evidence report.
6. Terminal: `replay` output closing on `"matched": true`.
7. Terminal or Muse session: cited run id answering a numbers question.
8. Close: browser graph full-frame, then repo URL and the thesis line.

## Break glass (live inference is down)

Use this section — and only this section — when the API fails or every
live trap ties on camera. Nothing here needs a key or network:

1. Say on camera that live inference is unavailable; the refusal-vs-
   number split below is pre-run real output, labeled with its capture
   time (`Get-Item .runs/demo-cmp-*.txt | Select-Object Name,
   LastWriteTime`).
2. Show all four captures in order:
   `Get-Content .runs/demo-cmp-fuel.txt`, `...-leverage.txt`,
   `...-delay.txt`, `...-profit.txt`. Each shows the grounded refusal
   beside the naive number.
3. Optionally open one saved comparison record: the `saved:` line in
   each capture names a `.runs\<uuid>.json` file holding the full
   grounded run, direct text, latencies, and agreement record.
4. Continue at Act 3 — the heat-pump montage, revision, sliders,
   reports, and replay are fully offline.

## If anything breaks live

- API down or key missing: say so on camera; use Break glass above,
  then Acts 3–4 offline.
- A trap ties live (direct hedges or refuses): report it as a tie, show
  the pre-run capture for that trap, continue. Never narrate a win the
  current run did not show.
- Wrong run id: the CLI names the problem and points at `demo-seed`;
  re-run the `$seed` capture.
- Port 8000 busy: `serve` says the address may be in use — retry with
  `--port 8001` and open the printed URL.
- Page shows the revised (-417.40) run instead of the base: a revision
  is newer than the seed — re-run `demo-seed` right before recording.
- `Tee-Object` files missing: re-run the four prep compares; each
  re-saves its capture.
