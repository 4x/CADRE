---
id: decision-unified-single-call-answer
type: decision
title: Unified single-call answer with trimmed JSON catalog cards
summary: 'answer() collapsed from parse+compose to one AnswerQuestionGrounded call: facts and graph in
  a single response, runtime validates both halves as before. Catalog entries trimmed to ports/guards/assumptions
  (id/version/status/source/expression stay in DB); solver profile sent once; per-model inverse-views
  map deleted. Payload 289KB->206KB at 109 models, one round trip, live-verified at \.06 (was \.09). JSON
  kept over Markdown/YAML/XML: exact-key echoing mirrors the output contract and format savings are second-order
  to field trimming. Trade-off: unclear questions now cost the catalog upload (previously parse-only).'
status: accepted
created: '2026-11-02'
updated: '2026-11-02'
topics:
- architecture
- runtime
- llm
confidence: null
relations: []
---

# Unified single-call answer with trimmed JSON catalog cards

## Decision

Collapse `answer()` from two LLM calls (parse, then compose) to one unified
`AnswerQuestionGrounded` call that returns facts/issues and the
status/graph/reason proposal together. The runtime validates both halves
with the existing checks (exact-quote fact grounding, unique IDs, graph
shape, binding admissibility), so the safety profile is unchanged while
latency halves and the prompt reads as one coherent instruction set.


## Context

The two-call split predated the 109-model catalog. The compose call embedded
full `asdict` models (289KB body), and the split prompt halves duplicated
context. Owner draft proposed backward-chaining instructions and a trimmed
catalog; this decision records the adaptation (below) and the format
research.


## Alternatives considered

- Keep two calls: rejected; doubles round trips and the parse call's savings
  (skipping the catalog upload for unclear questions) no longer justify the
  split prompt and error handoff.
- Markdown/YAML catalog instead of JSON: measured and rejected for now.
  Trimmed JSON is 189KB vs 176KB Markdown (-7%) from 255KB; XML is far
  worse (+80% tokens in benchmarks). Research consensus (Microsoft/MIT
  arXiv 2411.10541, ImprovingAgents nested-data, SoftServe) is that input
  format effects are model- and task-dependent while JSON remains the
  sensible default; exact quoted keys mirror the output contract the model
  must echo (revision keys, port names), which matters more here than the
  7% token delta. Revisit with the composer eval battery if selection
  errors appear.
- Draft's unit-conversion models (C_to_K etc.): rejected as architecturally
  wrong for this runtime — ports auto-convert through registry scales, so
  no conversion models exist or are needed. The shipped prompt says so
  explicitly.
- Draft's estimated values and manual topological sort: rejected — estimates
  stay forbidden (needs-input instead) and the runtime already sorts.


## Rationale

Field trimming dominates format choice (255KB -> 193KB from dropping
id/version/status/source/expression; guards/families omitted when empty),
and the per-model inverse-views map (13KB of redundant input lists) folded
into one top-level solver profile. The unified prompt keeps the draft's
backward-chaining strategy and worked parsing example while conforming to
engine reality (`__output__` token, auto unit conversion, runtime sorting).


## Consequences

- One round trip per question; live-verified on the README example (same
  2-model chain, $1,200, $0.06 vs $0.09 before).
- `parse_query` and its prompt file removed; fact validation stays in
  `query_inputs.py` and runs inside `answer()`.
- Known trade-off: unclear questions now cost the catalog upload. Revisit
  if needs-input rate times catalog size hurts.
- Catalog retrieval still the long-term scaling fix.


## Revisit if
