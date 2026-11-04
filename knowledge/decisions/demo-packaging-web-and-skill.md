---
id: decision-demo-packaging-web-and-skill
type: decision
title: 'Demo packaging: stdlib web UI plus Muse SKILL'
summary: Hackathon demo ships as a zero-dependency local web page plus a repo SKILL and offline demo seed;
  MCP server deferred.
status: accepted
created: '2026-11-04'
updated: '2026-11-04'
topics:
- demo
- packaging
- hackathon
confidence: null
relations: []
---

# Demo packaging: stdlib web UI plus Muse SKILL

## Decision

The hackathon demo ships two surfaces over the unchanged deterministic engine: a zero-dependency local web UI (`connected-models serve` plus one bundled page) and a repo Muse SKILL (`.agents/skills/connected-models/SKILL.md`), supported by an offline `demo-seed` command and a 3-minute video plan in `docs/demo-video.md`.


## Context

Submission is due November 4, 9 PM ET with roughly a quarter of the reported rubric on the demo and a quarter on Meta tooling use (see [[source-meta-hackathon-and-model-api-2026]]). The CLI was complete but terminal-only; the demo needed something genuinely cool to watch plus a Meta-native integration story, built in hours without new runtime dependencies.


## Alternatives considered

- MCP server exposing answer/inspect/revise/replay as agent tools: best long-term interop, but most work and most failure modes before the deadline. Deferred to the roadmap, not rejected.
- Terminal plus static report gallery only: shippable in an hour but lowest visual impact. Kept as the offline fallback inside the video plan rather than the lead.
- Streamlit or another web framework: rejected; a new dependency would break the zero-runtime-deps packaging story reviewed in [[decision-src-layout-packaging]].


## Rationale

- The web page reuses `reports.py` evidence shapes and `revise_run`/`read_run` directly, so every pixel is backed by saved manifests; the animated graph is the video money shot.
- The SKILL is the Meta-tooling story: any agent in the repo routes quantitative questions through the engine instead of hallucinating arithmetic, which matches [[concept-agent-quantitative-reasoning-layer]].
- `demo-seed` makes the demo reproducible and the video recordable offline: labeled fixture admissions, scripted runs with known amounts (1200 USD operating cost, $8,532.16 NPV), idempotent and spend-free.


## Consequences

- New package modules `serve.py` and `demo_seed.py`, package data `web/index.html`, CLI commands `serve` and `demo-seed`, tests `test_serve.py` and `test_demo_seed.py` (176 offline tests total), and docs `demo.md`/`demo-video.md`.
- Demo admissions carry reviewer `demo-seed` and fixture-only notes; they must never be mistaken for scientific approval.
- The `/api/answer` endpoint is the only live call; everything else (revise, replay, reports, page load) is offline.


## Revisit if

A hosted public demo is needed (this server binds loopback by default), or full-catalog prompting outgrows the single-page demo and needs retrieval first.

## Follow-up — 2026-11-04

The MCP agent-tool story was scheduled the same day: `connected-models mcp` now serves answer/inspect/revise/replay/report/units/registry_list over stdio with no new dependencies. The deferral above is spent; the roadmap item is `docs/mcp.md` plus `tests/test_mcp_server.py`.
