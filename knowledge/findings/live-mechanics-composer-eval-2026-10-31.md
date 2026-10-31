---
id: finding-live-mechanics-composer-eval-2026-10-31
type: finding
title: Live mechanics composer evaluation
summary: 'Six live answer runs on mechanics models: correct model selection, 3-node chaining,
  inverse solving, contradiction detection and missing-input questions all worked; number-words
  are not executable and sandbox egress needs escalation.'
status: active
created: '2026-10-31'
updated: '2026-10-31'
topics:
- reliability
- agents
confidence: medium
relations:
- type: relates-to
  target: source-m2d-acceptance-exercise
- type: relates-to
  target: question-model-discovery-and-selection
---

# Live mechanics composer evaluation

Six live `answer` runs against the 7-model registry (5 heating/finance, 2 mechanics), authorized as up to 10 composer calls; 5 composer + 6 parser calls were used. All inference: muse-spark-1.3, about $0.0085 per call, about 5–6 s per call, roughly 10–13.5 s wall per answer. Session spend +$0.094 settled (29→40 calls, $0.274631→$0.36868).

## Prompts and outcomes

1. Forward velocity — car, v0=0, a=2, t=10 → v=20.0 m/s. Correct (`3361fdc5` was the sandboxed transport failure; retry `333777bb` completed).
2. Forward displacement — ball, x0=10, v0=5, a=2, t=10 → x=160.0 m. Correct (`28b1850f`).
3. Two-phase chain, first wording — contradicted itself (coast "from position 0 m" and from end of acceleration). Parser correctly refused with `needs-input` naming the contradiction (`2cfd9f22`).
4. Two-phase chain, corrected — composer built a 3-node graph (displacement n1, velocity n2, displacement n3 with x0←n1, v0←n2) → x=1847.4768 m, exactly the hand value (`41fe88d2`).
5. Inverse — v0=70, v=10, t=40, solve a → -1.5 m/s² via `solve_for=a` with `__output__` target (`cf7c454f`).
6. Missing input — "A car accelerates along a straight road. How far does it travel?" → `needs-input` with exactly the four needed questions (x0, v0, a+constancy, t), noting constant acceleration unstated (`5d0eee9a`).

## Working

Correct mechanics model selection every time with no heating-model confusion; digit-literal fact binding with units; genuine multi-node chaining with upstream references; inverse-view selection; precise clarification questions; parser contradiction detection.

## Not working / friction

- Number words are not executable: "zero acceleration" parses as text and would fail binding ("text inputs cannot execute"); "starts from rest" needs an explicit "0 m/s" rider. Users will hit this with natural phrasing.
- Sandboxed egress is fully blocked (direct TCP and the local proxy port both raise WinError 10013), so live calls from an agent session require per-command unsandboxed escalation; owner launches are unaffected. The adapter itself has no proxy support.
- The failed transport attempt left a $1.328128 worst-case reservation held with no release path; ledger now shows a `reserved` group alongside `settled`.
- Multi-phase questions are wording-sensitive (one rephrase needed), though the failure mode was an honest contradiction flag, not a wrong answer.
