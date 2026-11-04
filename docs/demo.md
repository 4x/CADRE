# Demo guide: web UI, SKILL, and video

Two new ways to show Connected Models, both running off the same deterministic
engine and saved-run evidence.

## Web demo (stdlib only)

No third-party packages and no external requests; the page is one bundled file
served by `connected-models serve`.

```powershell
uv run --no-env-file connected-models demo-seed
uv run --no-env-file connected-models serve --port 8000
```

Then open http://127.0.0.1:8000/ in a browser. The page opens on a saved run,
so it is useful before any inference:

- **Ask** types a self-contained question into the normal `answer` workflow
  (live; needs `META_API_KEY`). Sample chips fill the scripted questions.
- **How it connects** animates the dependency graph: quoted inputs on the
  left, one box per reviewed model, outputs highlighted.
- **Follow the calculation** expands each step's inputs, expression, source,
  assumptions, and review.
- **What if** revises the run's direct inputs with sliders and shows a
  before/after delta table. Revisions are offline and preserve the original.
- **Recent runs** reopens any saved run without recomputing.

API surface (all JSON): `GET /api/demo`, `GET /api/runs`,
`GET /api/run/<id>`, `POST /api/answer`, `POST /api/revise`,
`GET /api/report/<id>` (standalone evidence HTML).

## Demo seed (offline)

`demo-seed` admits the five synthetic heating fixtures with reviewer
`demo-seed` and executes the two scripted scenarios. It is idempotent and
spends nothing. Admissions are labeled demo fixtures, not scientific approval;
skip keys that are already eligible in a curated registry.

## Muse SKILL

`.agents/skills/connected-models/SKILL.md` turns the CLI into an on-demand
agent workflow: route quantitative questions through `answer`, cite run ids,
revise instead of recomputing, and open `serve` for visual demos. Any Muse
session in this repo can invoke it with `/connected-models`.

## Recording the video

See [demo-video.md](demo-video.md) for the 3-minute shot plan. Practical
rules: pre-run every live call, record `replay`/`revise`/page flows offline,
and keep one terminal window plus one browser window visible.
