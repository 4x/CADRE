---
id: question-technology-stack-and-meta-access
type: question
title: Implementation Stack, Deployment Boundary, and Meta Access
summary: Which verified Meta model access and capabilities, application languages, execution host, persistence, and agent orchestration choices fit the first build's actual constraints?
status: active
created: '2026-10-27'
updated: '2026-10-29'
topics:
  - architecture
  - runtime
  - llm
confidence: null
relations:
  - type: relates-to
    target: question-build-readiness
  - type: relates-to
    target: question-first-build-scope-and-success
  - type: relates-to
    target: question-execution-runtime-for-heterogeneous-models
  - type: relates-to
    target: question-registry-storage-and-versioning
  - type: relates-to
    target: question-agent-interaction-patterns
  - type: relates-to
    target: question-execution-security-and-access
  - type: relates-to
    target: source-meta-hackathon-and-model-api-2026
---

# Implementation Stack, Deployment Boundary, and Meta Access

## Question

Which concrete technology choices satisfy the first build's contracts, and what Meta/Muse access and capabilities have actually been verified rather than assumed?

## Decisions to answer

### Model access and capability

- Which exact Meta model IDs/versions, account access, API endpoints, terms, and allowed tools are available to us? Is access event-specific, generally available, or still blocked? Naming Muse as the intended backing is not proof of access.
- What tool-calling and structured-output behavior is supported, including schema limitations, validation failures, malformed output, retries, timeouts, and model/version changes? Which behaviors require application validation regardless of API features?
- What context/document support, quotas, concurrency, latency, and cost constrain discovery, formalization, review, and query-time resolution? Can roles share one model with different instructions, or is a model/role split necessary?
- What data can be sent to inference endpoints under applicable privacy/license rules? How are keys supplied server-side without entering source, logs, or client code?
- If intended access is unavailable, what can still be built/tested locally, and is an alternative Meta route allowed and appropriate? A recorded/mock trace is not a verified live integration. If hackathon participation remains the goal, which model-use and submission rules constrain fallback choices?

### Application and execution technology

- Which language/library capabilities do the first model classes actually need? Should interface/orchestration and numerical execution share a runtime or be separated? Which contract crosses that boundary?
- Does the first workflow need a web UI, CLI/tool API, or both? What framework choices serve that requirement without rebuilding historical social/editor features?
- Is a synchronous in-process orchestrator sufficient, or are durable jobs, a queue, checkpoints, cancellation, and separate workers necessary? What evidence would justify adopting an agent/workflow framework rather than a small explicit state machine?
- Which persistence/query requirements from [[question-registry-storage-and-versioning]] justify particular database/index/artifact-store technologies? Which dependencies can remain local?
- What is the intended local development and eventual deployment boundary? Can the candidate host run required numerical libraries, subprocesses, long jobs, sandboxes, and payload sizes? A frontend's hosting compatibility does not establish backend compatibility.
- What package/version constraints, reproducible environment, local test setup, and logging/redaction baseline are required? What latency/cost and representative payload measurements would invalidate the choice?

## Current partial answer

### Implementation delta — 2026-10-29

The user selected the Meta API route by linking its coding-agent guide and authorized $150 total inference spend. Documentation was checked directly; [[source-mvp-heating-and-meta-evidence]] records endpoint, Spark Standard pricing, structured responses and evidence limits. The application now has a dependency-free uv-managed Python scalar core and a bounded Chat Completions smoke adapter with a persistent conservative cost ledger. Ten offline tests pass, including mocked transport and spend controls. Credentials are runtime process variables; no `.env` was accessed. No coding-agent provider outside this repository was changed. A live exchange, durable registry/admission and interface selection still remain; the following original inventory is historical context rather than a claim that no application code exists now.

No application stack or authenticated Meta integration exists in this checkout. Historical React/Supabase/Math.js choices and the later Python/TypeScript proposal are not accepted defaults. A distributed scheduler, graph database, vector service, or multi-agent framework is not required merely by the vision. Earlier saved model/event source records have incomplete bodies and must be rechecked before relying on access/API claims.

This record identifies future research; it does not recommend providers. When choices are investigated, consult current primary documentation, research third-party services through the required discovery process, record sources under knowledge/sources/, and distinguish verified access from advertised capability.

## Build gate and dependencies

**A — verify access and a feasible execution/development boundary before committing to the stack.** Detailed persistence and orchestration choices follow their contracts. Production hosting, federation, and a fleet of specialist agents can wait unless the first workflow requires them. Choosing a host here does not authorize provisioning or deployment.

## What would resolve it?

A scoped technology decision matrix tied to the first-build requirements, current version/docs evidence, a successful bounded authenticated Meta tool/schema exchange (or an explicitly recorded blocker), and evidence that the proposed local execution environment can support the required model payloads and safety boundary. No broad performance improvement is claimed without measurement.

## Provenance

New question from the user's 2026-10-27 request for architectural and technology questions before implementation; no provider research or integration was performed for this question inventory.
