# Demo video — 3-minute shot plan

Total: 3:00. One terminal plus one browser window, screen-recorded at
1080p. Four acts: the hook (live two-model chain), half-questions (the
forecast with a receipt), the conduits montage (offline heat-pump
receipt), future plus use cases. Pre-run everything; the only live
calls are the Act 1 beat, and even that has an offline fallback. No
bare-LLM side-by-side appears anywhere.

## Prep (before recording)

```powershell
uv sync
uv run --no-env-file connected-models demo-seed
uv run --env-file .env connected-models serve --port 8000
```

Pre-run the two live answers and save their terminal output (this is
the Act 1 fallback footage and the Act 2 footage):

```powershell
uv run --env-file .env connected-models answer 'A binary contract pays 100 USD if a candidate wins an election. The market implies a 60 percent win probability. The risk-free discount rate is 5 percent for a horizon of 1 period. At net odds of 1 to 1, what Kelly fraction of bankroll should be staked, and what is the fair value of the contract today?' 2>$null | Tee-Object .runs/demo-ans-kelly.txt
$env:CADRE_ALLOW_LLM_STEPS = '1'; uv run --env-file .env connected-models answer 'EUR/USD now trades at 1.12 US dollars per euro. The ECB policy rate is 2.65 percent and the Fed policy rate is 4.00 percent. What could we expect the EUR/USD exchange rate to be half a year from now?' 2>$null | Tee-Object .runs/demo-ans-fx.txt
```

Confirm the Kelly capture shows `completed` / `full` with 0.2 and
57.14, and the FX capture shows `completed` / `partial` with 1.12746,
before recording. Open http://127.0.0.1:8000/ and confirm a saved run
renders. Run `demo-seed` last, after any revision experiments: the
page opens the newest saved run per scenario, so a stale revision
would displace the base $8,532.16 run. Exact commands, expected
outputs, and per-step fallbacks are in [demo-script.md](demo-script.md).
Set the terminal font large (18pt+) and clear the screen between beats.

## 0:00–0:35 — Act 1, the hook: an election bet, priced two ways

Narration: "An election bet. What fraction of bankroll does the math
say to stake — and what is the contract actually worth today? Watch
one command answer both, with receipts."

Shot: terminal, one live `answer` command (the Kelly question). Point
at the split that matters: two output nodes, `n_kelly` at 0.2 and
`n_fair` at 57.14, `grounding: full`. Cut to the browser: the result
graph with the two model boxes, then the Models tab Kelly card —
"Kelly optimal wealth fraction for a simple bet", formula, guards,
source, permitted use. "Two reviewed models, one chain. Every number
has a receipt, and every model has a name."

Fallback: if the live call fails on camera, show the pre-run capture
(`Get-Content .runs/demo-ans-kelly.txt`) and keep going.

## 0:35–1:25 — Act 2, half-questions: the forecast with a receipt

Narration: "Some questions the engine can only half-answer. Here is
what honest looks like."

Shots: terminal, the pre-run FX capture (or live with the flag on):
`completed`, `partial`, 1.12746, with the covered-interest-parity
step receipt attached to the reviewed expectation model. "One twelve
spot, two policy rates, six months out: 1.1275. The engine calculated
the one link no reviewed model covers — and marked exactly that
link."

Cut to the browser Models tab on the forward-implied card: the BIS
source behind the reviewed half. "Partial grounding, full honesty."

Fallback: show the capture; the numbers in
[demo-script.md](demo-script.md) Act 2 are the evidence.

## 1:25–2:25 — Act 3, conduits montage: Dana's receipt

Narration: "When the books balance end to end, every number carries
its provenance. Follow one household decision."

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
answer captures, sliders, reports, and replay need no network and no
key. If the API fails, say so on camera and use the break-glass section
in [demo-script.md](demo-script.md) — determinism under failure is
itself the demo.
