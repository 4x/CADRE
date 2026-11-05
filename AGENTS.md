# Connected Models

Connected Models (aka **CADRE**: **C**omposable **A**tomic **D**eterministic **R**egistry **E**ngine) connects reusable quantitative models across domains: one model's output can supply another's input, replacing arbitrary assumptions with explicit, traceable dependencies. It enables people and AI agents to compose and execute models to answer quantitative questions, explore scenarios, and support decisions.

# Agent conduct

## Make life easy for human developer and user

**Save the humans time.** Human monitoring, inspection, and intervention are important, but should be invoked only when necessary.

To the extent possible, the agent should do all activities needed to achieve the goal, including research, coding, scripting, documentation, and the work around what the human must do. For example, while the agent is not allowed to read or write `.env` files, it can prepare perhaps 80% in a file such as `draft.profile`, where the human only fills in actual secrets.

## Ask

The agent is encouraged to bring up questions for discussion **when direction is not clear or obvious**. Concisely present the options, pros, cons, expected consequences, implications, and recommendation as appropriate. If there is a strong recommendation, proceed with it rather than unnecessarily deferring the decision.

## Version control

1. Do not work directly on `main`

2. Commit often, with meaningful commit messages

3. Merge up to main and push when completed features (or fixed bugs) have been tested.

## API Budget

You have **no hard limit** in terms of API usage - but the expectation is that you use it responsibly: run as many queries needed, as often as needed - but not more than that.

# Safety and permissions

- Direct access to `.env` files, account numbers, API tokens, and other secrets is normally off-limits unless the human explicitly grants permission. Running project scripts that normally read .env variables (e.g. for API tokens) is allowed.
- Do not touch anything outside this repository without explicit permission.
- Make sure you have permission before destructive actions.

<!-- PROJECT_MEMORY:BEGIN MANAGED PROTOCOL -->

# Project Memory agent protocol

This repository's durable project state lives in the repository, not in the current chat or agent session.

Project Memory (`pmem`) is supporting tooling for structure, continuity, and decisions—not the product or the main deliverable. Use it to support implementation, not as a substitute for delivering the MVP.

## Mandatory preflight

Before external research or substantial new work:

1. Read `PROJECT_STATE.md`.
2. Run `pmem search "<task>"` and inspect the top summaries.
3. For non-trivial work, run `pmem context "<task>"`.
4. Explicitly identify what is already known, previously rejected/paused, unresolved, and possibly stale.
5. Work on the delta unless the task explicitly calls for re-evaluation.

## Write-back

After substantial work:

1. Before creating a durable object, use `pmem similar <id-or-file>` when overlap is plausible; prefer updating an existing canonical `concept` over creating a near-duplicate.
2. Create durable `finding`, `decision`, `question`, `hypothesis`, `experiment`, `investigation`, `idea`, or `note` objects only when they are independently useful later.
3. Link objects with `relations` metadata and/or `[[artifact-id]]` wikilinks.
4. Do not promote every intermediate agent thought to canonical knowledge.
5. Preserve disagreement and uncertainty. Use status, confidence, alternatives, and supersession rather than silently erasing history.
6. If a prior artifact is replaced, use `pmem supersede <old-id> <new-id>` rather than deleting history.
7. Update `PROJECT_STATE.md` only when the project's current intellectual state materially changes.
8. Run `pmem validate` after edits and `pmem doctor` periodically. The derived index auto-refreshes on retrieval; `pmem index` can rebuild it explicitly.

## Vocabulary

Use canonical lowercase **status**: `provisional`, `active`, `accepted`, `paused`, `resolved`, `completed`, `rejected`, `superseded`, `archived`.

When creating a new **question**, reuse existing topics where possible. Prefer 2–4 topics: one broad domain, one subdomain, and optionally one or two specific subjects. Do not create synonyms for existing topics. Make topics:

- lowercase
- singular where natural
- kebab-case
- conceptual, not procedural
- reused before creating new ones.

## External sources

External evidence belongs in `knowledge/sources/`. Sources support or challenge project-created knowledge; they are not the primary knowledge layer. Preserve provenance where it matters.

## Cold-start standard

A human or new agent returning after roughly three months should be able to recover where the project stands, why it got there, what was tried/rejected, what remains unresolved, and what to do next from `PROJECT_STATE.md` plus bounded retrieval—not by replaying the whole project history.

<!-- PROJECT_MEMORY:END MANAGED PROTOCOL -->

# Repository Agent Guidelines

## Prohibited Tooling & Conventions

- **Do NOT use Superpowers**: Do not invoke Superpowers skills, workflows, or templates in this repository.
- **No Superpowers Directories**: Never create, write to, or reference `docs/superpowers/` or any other superpowers directories.

## Project Memory is the Sole Knowledge Base

- All durable project knowledge, specifications, designs, findings, decisions, and hypotheses must strictly follow the **Project Memory** protocol (`knowledge/` directory, `PROJECT_STATE.md`, and the `pmem` CLI).
- Preserve uncertainty, maintain provenance, link objects with typed relations and `[[wikilinks]]`, and validate with `pmem validate` and `pmem doctor`.

## Source Code

Source code and Project Memory belong together in this repository; implementation is the current priority. Before substantial design or architectural work, consult Project Memory. After implementation, update Project Memory only when the project's durable understanding, decisions, hypotheses, or open questions changed.
