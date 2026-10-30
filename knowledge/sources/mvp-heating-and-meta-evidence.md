---
id: source-mvp-heating-and-meta-evidence
type: source
title: Heating MVP and Meta Inference Evidence
summary: "Primary sources plus live Meta evidence: blocked initial source candidates, revised NIST extraction, registry reuse in three supported queries, one unsupported question, and independent numerical checks; limitations remain explicit."
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

Electricity cost, baseline-minus-alternative savings and net benefit-minus-investment are explicitly project-derived accounting identities. The fixture definitions are not agent-curated evidence. No empirical household validation, provider invoice reconciliation or broad performance comparison has been performed. Automated tests use fake network responses; the separate live evidence below uses real calls.

## Live evidence and additional source checks — 2026-10-29

Owner permission explicitly allowed runtime-only uv loading of `.env`; contents were never inspected or printed. Spark Standard returned a successful structured smoke response, three real offline extraction responses (two blocked, one admitted after separate technical review), a failed generation, three supported query compositions and one unresolved forecast request. Nine calls settled at a conservative ledger total of $0.100793; no reservations remained. The ledger and response artifacts are local evidence, not a reconciled provider invoice.

The NIST packet was expanded with section 3.3.1 Method 1 (printed p34/PDF66), section 4.3.1 (pp44–45/PDF76–77), Figure 3-1 (p26/PDF58), and section 6.1.1 (p78/PDF110). These support consistent real-price discounting, year-end timing and discounted operating savings. These passages were directly re-read. A section-number typo in the intermediate packet was corrected before the final `source-3` candidate; earlier candidates were not admitted. Case-specific performance, tariffs, horizons and heat demand remain scenario inputs.

Meta reasoning documentation, directly retrieved 2026-10-29: https://dev.meta.ai/docs/reasoning. It states that reasoning and visible output share the output-token budget, and omitted effort uses a model-selected level. The adapter now requests low effort and checks the completion reason before parsing visible JSON. The historical JSON failure's finish reason was not captured; token exhaustion is an inference, not a verified cause of that individual response. New regression tests cover explicit truncation and invalid completed JSON while retaining charge evidence.

Accepted extraction: candidate `e2118546-2868-4430-922f-ba90acff1828`, `uniform-present-value@source-3`, call `912a467f-b689-4ce7-a60a-2c077699a952`; $457.9707187194535 reproduces the rounded $457.97 reference within $0.005. Review identity `codex-prototype-review` denotes development-agent technical review, not owner scientific approval.

Live saved runs: default investment `8164f115-796f-48b2-9841-c7cc2540f23a`; operating costs `3ab13bce-0614-4fe7-a942-d3650956c174`; changed inputs `e49505cf-5f2a-48f6-8090-d07cbe9a30ae`; unsupported forecast `bca732eb-9214-4ef2-9fc4-34f0562592a6`. Separate Decimal year-by-year sums match the two NPVs within 1e-8. Shared models retain matching admissions across queries; curation was not rerun during answering. Verification artifact `.runs/live-verification.json` and HTML report `.runs/report-32796605-4d48-4a0a-8dcb-89d3f90633f3.html` preserve results and inspectable lineage locally.
