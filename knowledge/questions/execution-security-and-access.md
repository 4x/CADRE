---
id: question-execution-security-and-access
type: question
title: Execution Security, Data Access, and Trust Boundaries
summary: Which code, data, agent actions, and network operations are trusted in the first build; what isolation, resource limits, credential boundaries, and review controls are required?
status: active
created: '2026-10-27'
updated: '2026-10-27'
topics:
  - runtime
  - agents
  - reliability
confidence: null
relations:
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: question-execution-runtime-for-heterogeneous-models
  - type: relates-to
    target: question-technology-stack-and-meta-access
  - type: relates-to
    target: question-curation-evidence-and-approval
  - type: relates-to
    target: concept-specialized-model-curation-agents
---

# Execution Security, Data Access, and Trust Boundaries

## Question

Which parts of the first system are trusted, and how do agents, retrieved sources, generated code, model execution, and private data stay within that boundary?

## Decisions to answer

- Does the first build execute only reviewed built-in functions, permitted declarative expressions, downloaded code, AI-generated code, or some subset? May agents install dependencies or invoke arbitrary shells? What is explicitly disallowed?
- What isolation is sufficient for the allowed payloads: restricted evaluator, separate process, container, WebAssembly sandbox, stronger virtualization, or no untrusted execution initially? What protects files, network, subprocesses, and secrets beyond a language-level validation step?
- What CPU, memory, wall-time, output-size, dependency-installation, and concurrency limits apply? How are cancellation, infinite loops, malicious payloads, and failed cleanup handled?
- Which data sources are permitted, and how are credentials, private/licensed observations, and third-party access handled? If a service becomes multi-user, how are per-user data/model/run permissions checked? A single local operator can be an explicit initial boundary.
- Can sources or model code contain instructions that manipulate agents, tools, or evidence? How are source content and generated suggestions separated from tool authority, and which writes/network calls need review?
- What information may be sent to Meta or another endpoint, and what must remain local? How are sensitive inputs excluded from prompts, logs, saved artifacts, and shared model metadata?
- What does an external oracle have authority to return or request? How are unexpected output schemas, URLs, redirects, responses, and unavailable services constrained rather than trusted by default?
- Who may publish a model, execute it, access secrets, or trigger downstream runs? How are security decisions audited and distinguishable from scientific/model-quality approval?

## Current partial answer

Curation involves untrusted documents and potentially untrusted code; semantic/schema validity is not a sandbox. No execution host, security mechanism, or access policy is selected. The first build can narrow its scope to reviewed code, but must name that restriction. Model-quality review alone does not authorize unrestricted code execution or data export.

## Build gate and dependencies

**A — trust boundary before runtime/stack commitment; B — controls before the relevant capability is enabled.** Generated/untrusted execution, external fetching, private data, or multi-user publication cannot be enabled on the assumption that a future sandbox/access layer will make it safe. Co-resolve with runtime and verified hosting constraints; no production deployment is authorized by answering this question.

## What would resolve it?

A bounded threat/permission model, explicit first-build allowed/disallowed actions, resource and secret-handling rules, and a verification plan for attempted unauthorized access, runaway execution, prompt-injection content, and invalid external output. Unsupported threats must produce scope restrictions, not security claims without checks.

## Provenance

Identified in the 2026-10-27 pre-build review from the proposed automated curation and heterogeneous execution capabilities; no security solution is implemented by this record.
