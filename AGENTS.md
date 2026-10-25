<!-- PROJECT_MEMORY:BEGIN MANAGED PROTOCOL -->

# Project Memory agent protocol

This repository's durable project state lives in the repository, not in the current chat or agent session.

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

## Status vocabulary

Use canonical lowercase statuses: `provisional`, `active`, `accepted`, `paused`, `resolved`, `completed`, `rejected`, `superseded`, `archived`.

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

In the future, when implementation starts, Source code and Project Memory may coexist in this repository. Before substantial design or architectural work, consult Project Memory. After implementation, update Project Memory only when the project's durable understanding, decisions, hypotheses, or open questions changed.
