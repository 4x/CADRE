---
id: source-mvp-heating-and-meta-evidence
type: source
title: Heating MVP and Meta Inference Evidence
summary: Primary-source checks for the selected heating scenario, NIST numerical oracle, and Meta API configuration/pricing; authenticated access remains unverified.
status: active
created: '2026-10-29'
updated: '2026-10-29'
topics:
  - runtime
  - benchmarks
  - llm
confidence: medium
relations:
  - type: supports
    target: note-mvp-build-sequence-and-extension-triggers
  - type: supports
    target: question-first-build-scope-and-success
---

# Heating MVP and Meta Inference Evidence

## Meta documentation

Retrieved directly on 2026-10-29: https://dev.meta.ai/docs/coding-agents, https://dev.meta.ai/docs/models, https://dev.meta.ai/docs/protocols/chat-completions, https://dev.meta.ai/docs/structured-output and https://dev.meta.ai/docs/pricing-rate-limits.

The coding-agent guide documents https://api.meta.ai/v1 and the process variable MODEL_API_KEY. Spark 1.3 supports the initial structured request; app configuration selects Standard mode. The pricing page lists $1.25 per million input tokens and $4.25 per million output tokens for Spark Standard; ignoring cache discounts gives conservative accounting. Completion limits use max_completion_tokens on Chat Completions. The application independently checks output structure and usage. These documentation checks establish advertised capability, not this account's access or a successful live exchange. No coding-agent configuration outside the repository was altered.

## Heating relationship

University of Maryland Extension, Drew Schiavone, Home Energy: Heat Pump, updated July 14, 2026; directly retrieved 2026-10-29: https://www.extension.umd.edu/resource/home-energy-heat-pump. Its explanation of heat transfer and energy input/output supports using a heat/electricity ratio as a bounded starting relationship. The fixture equation rearranges that ratio to electricity = delivered heat / effective performance. Applying it over a representative year requires supplied whole-system seasonal performance; a point COP is insufficient. The source does not establish this hypothetical home's demand, performance or economics. The original DOE URLs attempted during research returned 404; no unavailable DOE content is claimed as retrieved evidence.

## Independent numerical oracle

NIST Handbook 135, 2020 edition, equation 3-7, printed page 29 (PDF page 61): https://nvlpubs.nist.gov/nistpubs/hb/2020/NIST.HB.135-2020.pdf#page=61. Direct PDF text retrieval on 2026-10-29 exposes the uniform annual present-value formula and an example: $100 at each year end for five years, discounted at 3%, gives $457.97. The focused test allows half a cent for that rounded published reference. This historical equation/reference is used, not historical mandated discount rates or a claim of current federal compliance. A separate Decimal sum of individual year-end payments checks the full synthetic scenario to eight decimal places.

## Evidence limits

Electricity cost, baseline-minus-alternative savings and net benefit-minus-investment are explicitly project-derived accounting identities. Five handwritten fixture definitions are not agent-curated evidence. No empirical household validation, provider billing reconciliation, live inference or broad performance comparison has been performed. Tests use fake network responses only.
