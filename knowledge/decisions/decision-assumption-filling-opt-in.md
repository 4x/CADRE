---
id: decision-assumption-filling-opt-in
type: decision
title: Assumption filling is an explicit per-request opt-in with documented bindings
summary: 'Strict quoted-fact grounding stays the default. --fill-in-assumptions (or FILL_IN_ASSUMPTIONS=True)
  lets the composer supply question-implied values as assumed facts (value need not occur in the question;
  quote must name the implying phrase; justification required); every assumed binding executes and is recorded
  on the run under assumptions, shown in CLI output and the HTML report. Facts schema gains optional assumption;
  assumed facts are rejected when the flag is off. Runtime 0.32.0.'
status: accepted
created: '2026-11-03'
updated: '2026-11-03'
topics:
- engine
- composition
- question-answering
confidence: null
relations:
- {type: extends, target: decision-proposed-estimates-in-clarifications}
---

# Assumption filling is an explicit per-request opt-in with documented bindings

## Decision

Keep strict quoted-fact grounding as the default: every fact value must
occur in the question. Add one explicit exception path: when the request
opts in via `--fill-in-assumptions` or `FILL_IN_ASSUMPTIONS=True`, the
composer may supply values the question implies but does not state, as
assumed facts. Each assumed fact carries a plain-language justification
and quotes the implying phrase; each assumed binding executes like a
quoted binding and is recorded on the run under `assumptions`, surfaced
in CLI output and the HTML report. Assumed facts are mechanically
rejected when the flag is off, and quoted-fact checks are unchanged when
it is on.

## Context

A constant-speed travel-time question failed with needs-input: the only
available model needed acceleration and absolute endpoints the question
never states, and strict grounding forbids supplying the implied zero
acceleration and origin baseline. The gap generalized to three causes:
missing simple catalog coverage, no permitted channel for implied
values, and no parsimony tie-break in model selection. This decision
covers the channel; the missing constant-velocity coverage was curated
separately, and the base prompt now prefers candidates with the fewest
unsatisfiable inputs.

## Alternatives considered

- Always-on assumption filling: rejected; silent invention is the failure
  mode strict grounding exists to prevent.
- Estimates in clarifications only (status quo): kept as the default
  path; the opt-in is for users who want execution with visible
  assumptions instead of a clarification round-trip.
