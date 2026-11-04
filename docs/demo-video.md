# Demo video — 3-minute shot plan

Total: 3:00. One terminal plus one browser window, screen-recorded at 1080p.
Pre-run everything; the only live call is the Ask beat, and even that has an
offline fallback.

## Prep (before recording)

```powershell
uv sync
uv run --no-env-file connected-models demo-seed
uv run --no-env-file connected-models serve --port 8000
```

Open http://127.0.0.1:8000/ and confirm a saved run renders. In the terminal,
pre-run `compare` once so its output is warm (optional; screenshots work too).
Set the terminal font large (18pt+) and clear the screen between beats.

## 0:00–0:25 — The hook: AI lies about numbers

Narration: "Ask any AI for an investment number and it will answer with total
confidence. The problem is arithmetic, not vibes — and confidence is not a
receipt."

Shot: terminal, one command:

```powershell
uv run --env-file .env connected-models compare 'Delivered heat is 12000 kWh per year. Baseline resistance heating has seasonal performance 1 and the proposed heat pump has seasonal performance 3. Tariff is 0.30 USD/kWh. The heat pump costs 10000 USD with a 5% real discount rate over 10 years. What is the net present value?'
```

Point at the verdict line: grounded engine on one side, direct LLM prose on
the other. "Same question, same model. Only one side shows its work."

## 0:25–1:10 — Ask: the question blooms into a graph

Narration: "Connected Models answers by composing reviewed, versioned models
— never by doing math in prose."

Shot: browser. Click the `investment` sample chip, press Answer. The graph
animates node by node — quoted inputs on the left, one box per model — then
the metric cards land: costs, savings, net present value $8,532.16.

Fallback: if the live call fails on camera, click "open saved investment"
instead; the animation is identical.

## 1:10–1:50 — What if: sliders, deltas, no recompute theater

Narration: "Follow-ups don't re-roll the dice. They revise the saved run —
same models, same evidence, new scenario."

Shot: browser. Drag the performance slider from 3 to 2 and the investment to
12000, press Apply revision. The "What changed" table appears with signed
deltas. "The original run is preserved; the revision is a new receipt."

## 1:50–2:25 — The receipt: sources, reviews, replay

Narration: "Every number carries its provenance. Expand any step."

Shot: browser. Open the first calculation step: expression, exact input
quotes, source link, assumptions, reviewer. Click "Open standalone evidence
report" — a self-contained page with zero API calls.

Cut to terminal:

```powershell
uv run --no-env-file connected-models replay RUN_ID
```

Point at `"matched": true`. "Deterministic. Replay it in a year, get the same
bytes."

## 2:25–2:50 — The skill: give every agent this calculator

Narration: "And it ships as a Muse skill — any agent in this repo answers
quantitatively through the engine instead of hallucinating arithmetic."

Shot: Muse session, `/connected-models` answering a numbers question and
citing a run id. Keep this beat to two commands and one cited answer.

## 2:50–3:00 — Close

Narration: "One model's output is another model's input. No invented numbers
— every figure has a receipt. Connected Models."

Shot: browser graph full-frame, then repo URL. End card: stack
(Python + uv, zero runtime deps, Muse Spark 1.3) and the thesis line.

## If anything breaks live

Everything except the Ask beat is offline: seeded runs, sliders, reports, and
replay need no network and no key. If the API fails, say so on camera and use
the saved runs — determinism under failure is itself the demo.
