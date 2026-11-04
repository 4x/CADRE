---
id: finding-demo-question-hunt-guard-traps-only
type: finding
title: 'Demo-question hunt: only guard traps beat the bare LLM'
summary: Against muse-spark-1.3, all forward chains, inverses, coherence multis and routing-chaos questions
  tie; only guard refusals (stated or computed-violation) win. Four dq- trap entries added; extract_numbers
  -$ scorer gap fixed.
status: accepted
created: '2026-11-04'
updated: '2026-11-04'
topics:
- demo
- evaluation
- llm
confidence: null
relations: []
---

# Demo-question hunt: only guard traps beat the bare LLM

## Finding

Against muse-spark-1.3 (November 2026 calibration), the bare direct-LLM route derives essentially everything correctly: 5-node availability chains, Markov-level MTBF derivations, cubic TMR inversion in prose, Karp-Flatt via Amdahl inversion, Ne, CAGR, even the SSA 5/9 early-claiming rule. Of 21 existing adversarial entries, only guard traps (at-gordon, at-zero-rate, at-growing-annuity, at-raid-size) and the two-root branch entry win; every forward chain, inverse, coherence multi, and routing-chaos entry ties. Thirteen new non-guard probes all tied. The four new dq- entries are therefore all guard traps, three of them a subtler computed-violation shape: every stated number looks sane and the violation only emerges from solving (inverse back-check), so the naive answer prints flatly with no hedge trigger.

## Basis

Full adversarial compare sweep (21 entries: 5 win, 16 tie, 0 loss) plus 13 direct-route probes, all on muse-spark-1.3. New entries (data/eval/adversarial-battery.json v5): dq-fuel-books (forward balance refusal, naive -100 tons, no hedge), dq-leverage-income (inverse NOI back-check, naive $10,000, no hedge), dq-delay-years (inverse y back-check, naive 6.25 years), dq-profit-implicit (inverse C_imp back-check, naive -$20,000). All four verified offline via runtime.execute and won live (grounded needs-input, direct printed naive). Also fixed the extract_numbers scorer gap for "-$X" forms (plain "-X" was already caught), which the dq-profit-implicit tie exposed; covered by a unit test in tests/test_compare.py.

## Implications

Future demo/adversarial questions should lead with guard-shaped traps, preferably computed-violation (inconsistent books revealed by inversion) over stated-violation, and naive amounts that print plainly. Non-guard derivation questions are tie-prone against this model family and need re-probing before admission. Multi-model composition alone does not beat careful derivation; the engine's edge here is principled refusal, not arithmetic.

## Limitations / uncertainty

Single-model calibration (muse-spark-1.3, one run each; direct-route formatting varies run to run, e.g. "-$20,000" vs "-20,000 dollars"). Weaker models may fall for derivation traps that tie here. Computed-violation traps rely on inverse back-checks rejecting inconsistent knowns, which is solver behavior worth pinning if the solver evolves.
