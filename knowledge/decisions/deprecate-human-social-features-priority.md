---
id: decision-deprecate-human-social-features-priority
type: decision
title: Deprecate Human Social Features Priority
summary: Pause development of social web features (starring, comments, public feeds) to concentrate on core computational semantics, ontology, and agent execution interfaces.
status: paused
created: '2026-10-24'
updated: '2026-10-24'
topics:
  - strategy
  - product
  - scope
confidence: high
relations:
  - type: relates-to
    target: concept-agent-quantitative-reasoning-layer
  - type: relates-to
    target: investigation-prototype-2025-mathjs-supabase
  - type: derived-from
    target: source-historical-problem-statement-and-initial-thoughts
  - type: derived-from
    target: source-historical-mathjs-prototype-architecture
---

# Deprecate Human Social Features Priority

## Decision

Pause and deprioritize the development of human-centric social platform features (user starring, public feeds, commenting threads, voting, social collaboration pages) that consumed significant engineering effort in the 2025 web prototype. Technical effort will concentrate on representation, ontology, runtime execution, and agent interfaces.

## Context

The 2025 implementation attempted to build a complete consumer-facing social platform (`CollaborationPage.tsx`, `comment` and `comment_vote` tables, `user_equation` star/view tracking). This premature focus on social mechanics diluted focus from the core unsolved problems: semantic interoperability, variable ontology, and scalable polyglot execution.

## Alternatives considered

- **Continue building the "Wikipedia of Models" social portal**: Rejected for now. Crowdsourced social mechanics cannot succeed without a working, trustworthy computation and verification layer.
- **Pure developer API / SDK**: An improvement, but still assumes human developers write all compositions manually.
- **Agent-first quantitative infrastructure**: Adopted. Prioritize autonomous AI agents as the primary consumers and compositional operators of the graph ([[concept-agent-quantitative-reasoning-layer]]).

## Rationale

Without semantic correctness, dimensional type checking, and reliable multi-model execution, social features add zero durable value. Once the computational backbone is established and validated by autonomous agents, collaborative human sharing mechanisms can be reintroduced cleanly.

## Consequences

- Removes boilerplate web features from near-term roadmaps.
- Frees project bandwidth to tackle foundational representation, ontology, and runtime questions.

## Revisit if

The core computational graph engine is mature, trusted, and adopted, and human community crowdsourcing becomes the primary bottleneck for catalog expansion.

## Legacy provenance

Reconstructed by contrasting social features in [[source-historical-mathjs-prototype-architecture]] with priority shifts in [[source-historical-problem-statement-and-initial-thoughts]].
