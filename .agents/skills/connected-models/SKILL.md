---
name: connected-models
description: Answer quantitative questions with grounded, inspectable results by composing reviewed models through the connected-models CLI instead of doing arithmetic in prose. Use when the user asks anything with numbers, units, costs, trade-offs, or "what if" scenarios.
---

# Connected Models — grounded quantitative answers

Never compute quantitative answers in prose. Route every number through the
deterministic engine so each result carries its inputs, model versions,
sources, and reviews.

## Commands (run from the repo root with uv)

```powershell
uv run connected-models answer 'QUESTION WITH ALL NUMBERS AND UNITS STATED'
uv run --no-env-file connected-models inspect RUN_ID
uv run --no-env-file connected-models report RUN_ID [RUN_ID...]
uv run --no-env-file connected-models revise RUN_ID --set node.input=amount
uv run --no-env-file connected-models replay RUN_ID
uv run --no-env-file connected-models compare 'QUESTION'   # grounded vs direct LLM
uv run connected-models serve --port 8000                  # animated web demo
uv run connected-models demo-seed                          # offline demo registry + runs
```

## Workflow

1. **Check the registry.** `registry-list` shows eligible models. If coverage
   is missing for the question, say so instead of inventing a model.
2. **Ask one self-contained question.** Put every assumption, number, unit,
   and requested output in the question text. There are no domain flags.
3. **Read the status.** `completed` means executed; `needs-input` means ask
   the user the listed clarification questions (never fill bindings
   silently — `--fill-in-assumptions` is an explicit user opt-in only);
   `blocked` means no supporting model exists.
4. **Cite the receipt.** Every answer gets its `run_id`, per-node amounts
   with units, and the models used. Link the HTML report when one exists.
5. **Revise, don't recompute.** Follow-up "what if" questions become
   `revise --set` calls against the saved run, preserving the original.

## Rules

- Exact quotes and units come from the question; the engine rejects the
  rest. Do not paraphrase numbers into the answer.
- Currency units never convert implicitly; mismatched meaning/context
  bindings are rejections, not warnings.
- Live `answer` calls spend from the Metered budget (`usage` shows spend).
  Prefer `replay`/`revise`/`report` (all offline) for follow-ups.
- For a visual demo, run `demo-seed` once, then `serve` and open the page:
  questions bloom into an animated graph with sliders for live revision.

## Repo map

- CLI: `src/connected_models/__main__.py`
- Engine and contracts: `src/connected_models/runtime.py`, `contracts.py`
- Web demo: `src/connected_models/serve.py`, `src/connected_models/web/`
- Docs: `docs/demo.md` (demo guide), `docs/architecture.md`, `docs/runs.md`
