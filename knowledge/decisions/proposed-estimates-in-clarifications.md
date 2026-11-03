---
id: decision-proposed-estimates-in-clarifications
type: decision
title: Proposed estimates allowed in needs-input clarifications, never silent in graphs
summary: 'Owner-directed policy change: when no model can produce a dependency, the composer may propose
  a specific assumed value with justification inside needs-input clarifications and ask the user to confirm
  or replace it. Estimates never fill graph bindings silently; the user confirms by stating the value
  in a follow-up question, where it enters as an ordinary traceable user-scenario fact. No runtime change:
  generated-origin bindings and any consent-gated auto-fill stay out of scope. Partially answers the disclosed-provisional-fallback
  trace in [[question-assumption-resolution-and-fallback-policy]].'
status: accepted
created: '2026-11-02'
updated: '2026-11-02'
topics:
- policy
- reliability
- llm
confidence: null
relations:
- {type: addresses, target: question-assumption-resolution-and-fallback-policy}
- {type: relates-to, target: concept-connected-models-thesis}
- {type: extends, target: decision-unified-single-call-answer}
---

# Proposed estimates allowed in needs-input clarifications, never silent in graphs

## Decision

Reverse the blanket estimates ban: when backward chaining reaches a
dependency no model can produce, the composer uses its best judgment to
either ask for the input or propose a specific assumed value — with exact
value, unit, and justification in plain language — inside needs-input
clarifications, asking the user to confirm or replace it. The run still
stops: estimates never fill graph bindings. User confirmation arrives as a
stated value in a follow-up question and enters as an ordinary
user-scenario fact with its quote, so the whole loop stays traceable with
zero new machinery.


## Context

The unified-answer decision shipped a strict step 6 (never invent, assume,
or estimate). The owner directed a change toward the draft prompt: the
composer should exercise judgment about when an assumed value could
suffice, provided it is clearly documented and communicated. The standing
question [[question-assumption-resolution-and-fallback-policy]] explicitly
lists "a disclosed provisional fallback" among the traces that would
resolve it; this decision delivers that trace in its weakest safe form.


## Alternatives considered

- Keep the blanket ban: rejected by the owner; it turns the system into a
  calculator that stalls on every difficult input instead of helping.
- Estimate bindings with consent (`source: estimate`, generated origin,
  auto-filled runs): deferred, not rejected. It needs a consent mechanism
  (what counts as approval?), report surfacing for generated values, and
  sensitivity handling when a fallback moves a conclusion — all open in
  the parent question. The `generated` origin and the runtime's consent
  gate stay reserved for exactly this.
- Silent estimates: rejected outright; combines the worst of both (false
  certainty with no trace).


## Rationale

Propose-in-clarifications is the only option that adds helpfulness without
new attack surface: no schema change, no runtime change, no new origins in
runs, and the confirmation path reuses the exact-quote fact machinery, so
a confirmed estimate is indistinguishable from — and as traceable as — any
user-supplied input. The thesis principle (explicit, provisional,
replaceable, traceable gaps) holds: the proposal is explicit in the saved
run's clarifications, provisional until confirmed, replaceable by the
user's own value, and traceable through the follow-up quote.


## Consequences

- Prompt step 6 rewritten; prompt test pins the new rule's key phrase.
- The parent question stays active: budgets, consent-gated bindings, and
  sensitivity semantics are still unresolved.
- Eval note: the composer eval battery should include a case that must
  propose (not fill) an estimate and a case that must ask without one.


## Revisit if
