# Demo video — 3-minute shot plan

Total: 3:00. One terminal plus one browser window, screen-recorded at
1080p. Four acts: the hook (live trap), the comparison (three more
traps), the conduits montage (offline heat-pump receipt), future plus
use cases. Pre-run everything; the only live call is the Act 1 beat, and
even that has an offline fallback.

## Prep (before recording)

```powershell
uv sync
uv run --no-env-file connected-models demo-seed
uv run --env-file .env connected-models serve --port 8000
```

Pre-run the four trap compares and save their terminal output (this is
the Act 2 footage and the break-glass fallback):

```powershell
uv run --env-file .env connected-models compare 'We bought 500 tons of diesel, started the year with 100 tons in the tank, and ended with 700. How much did we burn?' 2>$null | Tee-Object .runs/demo-cmp-fuel.txt
uv run --env-file .env connected-models compare 'Our contribution margin is $8,000 and our operating leverage is 0.8x. What''s our operating income?' 2>$null | Tee-Object .runs/demo-cmp-leverage.txt
uv run --env-file .env connected-models compare 'My statement says $2,000 at full retirement, and I''m getting $3,000. How many years did I delay?' 2>$null | Tee-Object .runs/demo-cmp-delay.txt
uv run --env-file .env connected-models compare 'Our shop made $200,000 in revenue with $120,000 in costs, for a true profit of $100,000. What salary did I give up to run it?' 2>$null | Tee-Object .runs/demo-cmp-profit.txt
```

Do not pass `--fill-in-assumptions` for trap commands: traps run with
fill-in off (the default). Confirm all four captures show the grounded
refusal beside the naive number before recording. Open
http://127.0.0.1:8000/ and confirm a saved run renders. Run `demo-seed`
last, after any revision experiments: the page opens the newest saved
run per scenario, so a stale revision would displace the base $8,532.16
run. Exact commands, expected outputs, and per-step fallbacks are in
[demo-script.md](demo-script.md). Set the terminal font large (18pt+)
and clear the screen between beats.

## 0:00–0:30 — Act 1, the hook: AI burns negative diesel

Narration: "Ask any AI a numbers question with broken books and it will
answer with total confidence. Watch the same model answer twice — once
bare, once through Connected Models."

Shot: terminal, one live command:

```powershell
uv run --env-file .env connected-models compare 'We bought 500 tons of diesel, started the year with 100 tons in the tank, and ended with 700. How much did we burn?'
```

Point at the split: `grounded: needs-input` asking what is wrong with
the books, beside `direct:` prose printing `**Burned: -100 tons**` as
its answer (a caveat sentence may trail the answer; the answer itself is
still the naive number). "Same question, same model. One side answered:
negative one hundred tons of diesel. The other asked what was wrong
with the books."

Fallback: if the live call fails on camera, show the pre-run capture
(`Get-Content .runs/demo-cmp-fuel.txt`) and keep going.

## 0:30–1:20 — Act 2, the comparison: three more traps

Narration: "It is not one lucky question. Every stated number looks
sane; the violation emerges only from solving — and the bare model
prints through it every time."

Shots: terminal, one pre-run capture per trap (~15s each):

1. `Get-Content .runs/demo-cmp-leverage.txt` — grounded refuses;
   direct prints `**Operating income: $10,000**` on $8,000 of margin.
2. `Get-Content .runs/demo-cmp-delay.txt` — grounded refuses; direct
   prints `**Delayed time = 6.25 years**` past the 4-year credit limit.
3. `Get-Content .runs/demo-cmp-profit.txt` — grounded refuses; direct
   prints `Foregone salary = -$20,000 dollars`.

One line each (see [demo-script.md](demo-script.md) Act 2), then: "Four
questions, four refusals, four confident wrong numbers. The engine's
edge here is principled refusal, not arithmetic."

Fallback: if a trap tied live in rehearsal, say so honestly for that
trap and show its pre-run win capture.

## 1:20–2:25 — Act 3, conduits montage: Dana's receipt

Narration: "Refusal is half the story. When the books do balance, every
number carries its provenance. Follow one household decision end to
end."

Shots (all offline from the seed):

1. Browser: click the `investment` sample chip, press Answer. The graph
   animates node by node — quoted inputs on the left, one box per
   model — then the metric cards land: costs, savings, net present
   value $8,532.16.
2. Browser: drag the performance slider from 3 to 2 and the investment
   to 12000, press Apply revision. The "What changed" table appears
   with signed deltas. "The original run is preserved; the revision is
   a new receipt."
3. Browser: open the first calculation step — expression, exact input
   quotes, source link, assumptions, reviewer. Click "Open standalone
   evidence report" — a self-contained page with zero API calls.
4. Cut to terminal:

```powershell
uv run --no-env-file connected-models replay RUN_ID
```

Point at `"matched": true`. "Deterministic. Replay it in a year, get
the same bytes."

Fallback: if the live Ask call fails on camera, click "open saved
investment" instead; the animation is identical.

## 2:25–3:00 — Act 4, future and use cases: give every agent this calculator

Narration: "And it ships as a Muse skill — any agent in this repo
answers quantitatively through the engine instead of hallucinating
arithmetic. One model's output is another model's input. No invented
numbers — every figure has a receipt. Connected Models."

Shot: terminal `registry-list` glimpse (eligible stored versions),
then a Muse session with `/connected-models` answering a numbers
question and citing a run id. Keep this beat to the registry glimpse
plus one cited answer. Alternative: show any MCP client calling the
`answer` then `inspect` tools — same receipts, no Muse required.

Close: browser graph full-frame, then repo URL. End card: stack
(Python + uv, zero runtime deps, Muse Spark 1.3) and the thesis line.

## If anything breaks live

Everything except the Act 1 beat is offline or pre-run: seeded runs,
trap captures, sliders, reports, and replay need no network and no key.
If the API fails, say so on camera and use the break-glass section in
[demo-script.md](demo-script.md) — determinism under failure is itself
the demo.
