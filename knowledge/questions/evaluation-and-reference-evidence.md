---
id: question-evaluation-and-reference-evidence
type: question
title: Evaluation, Reference Evidence, and Release Gates
summary: What independent evidence demonstrates source-faithful curation, safe composition, correct execution, visible fallbacks, and useful answers, with explicit tolerances and fair comparisons?
status: active
created: '2026-10-27'
updated: '2026-10-28'
topics:
  - benchmarks
  - reliability
  - epistemology
confidence: null
relations:
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: question-first-build-scope-and-success
  - type: relates-to
    target: question-curation-evidence-and-approval
  - type: relates-to
    target: hypothesis-graph-grounded-agent-reliability
  - type: relates-to
    target: question-assumption-resolution-and-fallback-policy
---

# Evaluation, Reference Evidence, and Release Gates

## Question

What evidence will tell us the first build is correct, honest about its limits, and useful—and what failures prevent us from presenting it as working?

## Decisions to answer

- What independent reference results, domain examples, source equations, empirical datasets, or expert judgments anchor correctness? Who adjudicates cases without simply trusting the same generating model or implementation?
- What separately measures source-faithful curation, semantic compatibility, numerical execution, empirical adequacy, and explanation/disclosure fidelity? Passing one does not imply the others.
- What numerical tolerances, units, solver/seed settings, input snapshots, and validity regimes make comparisons meaningful? How are unverifiable or non-reproducible external components reported?
- Which minimal deliberate failures must be detected: wrong units/meaning/scope, invalid preconditions, unsupported topology, unavailable inputs, out-of-domain candidates, failed tools, and a generated fallback that could change the conclusion?
- How is the desired curation workflow evaluated: reference reproduction, rejection of an unsuitable candidate, provenance retention, appropriate review, alternative-model preservation, and no automatic laundering of a Meta estimate into trusted coverage?
- What proves that the final answer follows the executed run, discloses generated assumptions and uncertainty limits, and does not claim a causal/optimal/probabilistic conclusion that the model cannot support?
- Which claims need baselines? For reliability/token/latency claims, how do we fairly compare native reasoning, an agent with general calculation/code tools, and Connected Models under matched tasks, data, model access, and correctness criteria?
- Which costs count: curation/bootstrap, retrieval, failed attempts, validation, cold/warm compilation, inference, and execution? What is first-build evidence versus a future generalization claim?
- What are release-blocking thresholds, explicitly permitted limitations, and the procedure for recording failures? Which cases need manual domain review rather than an invented automated truth score?

## Current partial answer

The repository's strong reliability/token/turn claims are hypotheses, not measured properties. Deterministic arithmetic cannot validate generated assumptions or a model's real-world adequacy. A small hand-adjudicated benchmark can be sufficient initially; proving universal superiority or building a large evaluation platform is unnecessary.

## Proposed first-build acceptance cases

[[question-first-build-scope-and-success]] now separates offline repository curation from query-time use, with provisional acceptance cases: source-faithful Meta curation, reuse across two supported compositions, independent numerical references, rejection of invalid bindings/candidates, model-first resolution, disclosed Meta gap-filling, conditional/unresolved outcomes, revision/version lineage, usage visibility, and live Meta contribution. These are proposed requirements, not performed checks or an accepted evaluation protocol. The offline/query separation itself is user-endorsed (2026-10-28): demonstrate real source-model canonicalization and variable/constant extraction into a stored qualified version first, then answer supported queries using existing versions without repeating curation. A missing-model case must not silently trigger inline curation; recommend disabling it for the first build, while the permanent total-ban-versus-last-resort policy remains open. Real earlier offline Meta curation counts as the curation contribution; it need not rerun live during each answer. Record curation cost/time separately from query-response cost/time.

Once the user confirms the anchor problem and milestone, choose exact source/reference cases, numerical tolerances, and required disclosure checks before implementing them. Keep synthetic failure cases distinct from empirical validation; do not add a broad comparative benchmark unless making comparative claims. Budget/latency gates need actual user limits and feasibility evidence, not invented targets.

## Build gate and dependencies

**A — define observable success and reference evidence with first-build scope. B — run the affected acceptance checks before claiming the slice works.** No experiments are run by creating this record. Comparisons are required for comparative claims, not as a blanket requirement before every coding spike.

## What would resolve it?

A compact acceptance matrix linking each supported capability to its independent oracle/evidence, tolerance, expected failure behavior, and release threshold. A later recorded evaluation must distinguish passed, failed, blocked, and untested cases, and separate implementation correctness from empirical/model validity. Broader statistical claims remain open until supported by adequate experiments.

## Provenance

Identified during the user's 2026-10-27 pre-build review to make the scope decision falsifiable and avoid treating agent agreement or a polished demonstration as verification.
