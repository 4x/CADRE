---
id: source-classical-mechanics-first-intake
type: source
title: Mechanical Intake Check of the First Classical-Mechanics Return
summary: Five mechanics candidates pass ZIP integrity, v1 schema and declared arithmetic/rejection checks; actual retrieval URLs are incomplete and scientific auditing is explicitly assigned to a separate reviewer role.
status: active
created: '2026-10-31'
updated: '2026-10-31'
topics:
  - agents
  - lifecycle
  - interoperability
confidence: high
relations:
  - type: relates-to
    target: note-offline-curation-agent-kit
  - type: relates-to
    target: question-curation-evidence-and-approval
  - type: relates-to
    target: note-mvp-build-sequence-and-extension-triggers
---

# Mechanical intake of classical-mechanics-a-b01

Checked 2026-10-31 at the owner's request, limited to packaging, schema, completeness and the existing deterministic numerical checks. No external sources were opened, no scientific assumptions/oracles were audited, no models were imported or admitted, and the submitted ZIP was not changed. The owner explicitly separates this engineering intake from scientific/source auditing, which belongs to another assigned reviewer agent.

Artifact: `from-offline-curation-workers/classical-mechanics-a-b01-return.zip`. SHA-256: `b8a32dfdeea575eb10f8191273ad302c1846abcd12a687e787c0cc465fe926a0`. Curator label: `muse-code`; created date `2026-10-31`; kit `2026-10-31.2`; return schema `cm-curation-batch/1`.

## Mechanical result

The ZIP contains exactly `bundle.json` (43,125 uncompressed bytes) and `manifest.json` (116 bytes). Its bundled checksum and version match. All five unique namespaced model IDs and revisions satisfy the schema. Required relationship, variable, unit/dimension/context/domain, constant, guard, source/locator/date/license, assumption, limitation, reference, rejection, inverse and integration fields are present and structurally valid. Numerical references match the submitted expressions within the submitted tolerances; this does not establish source fidelity or oracle independence.

| Record suffix, all classical-mechanics prefix and r1 | Forward reference cases | Rejection cases | Integration |
| --- | --- | --- | --- |
| translational-kinetic-energy | 2 | 2 | requires-extension |
| constant-acceleration-displacement | 2 | 2 | requires-extension |
| velocity-after-constant-acceleration | 2 | 2 | requires-extension |
| gravitational-potential-energy-difference | 3 | 2 | requires-extension |
| collinear-constant-force-work | 3 | 1 | requires-extension |

Total: **five records, twelve passing forward cases, nine passing rejection cases**. Each record has one source entry, three assumptions, three limitations, inverse notes and explicit integration gaps. All `runtime_model` values are null; none claims current execution eligibility. The empty `handoff.connections` array is valid under the corrected atomic-catalog policy; two optional queries, three deferred items and a continuation backlog are present. No chain is required.

Command used:

```powershell
uv --cache-dir .uv-cache run --no-env-file --offline -m connected_models.curation validate from-offline-curation-workers/classical-mechanics-a-b01-return.zip
```

Result: `valid-data-awaiting-review`. This means mechanically valid intake data, not scientific approval or an executable registry addition.

## Completeness caveats for handoff

1. The worker reports no direct full-page access and says it relied on search renderings and mirrors, naming Maricopa Pressbooks, LibreTexts and a Valdosta PDF. The individual source records provide only primary OpenStax URLs; the actual mirror/search retrieval URLs, exact edition/page identities and which claims came from each are absent. Request these locations or a precise statement that they were not retained. Do not label an indirectly seen primary page as directly inspected. This is missing provenance, not an assertion that the physics or citations are wrong.
2. Source-rights verification is explicitly incomplete. Preserve that disclosure for the auditor; the intake check does not decide rights or confirm the stated edition/license differences. Similarly, all `unresolved` arrays being empty does not mean independent review is complete.
3. The worker reports a virtual-environment creation failure and a successful `--no-project --offline` workaround. Central validation succeeded using the normal project command with `--no-env-file`; this is a worker-environment reproducibility note, not a failing submission. Future execution reports should include the exact fallback command and interpreter/version while retaining the no-environment-file rule.
4. The new quantities/units require runtime work. The current engine's fixed energy/currency vocabulary cannot execute these records, and dimensionful powers require explicit engine support. This is a platform integration gap, not an incomplete research JSON field. A separate reviewer must determine which records are suitable before eligible runtime projections are made.

## Next disposition

Keep this batch as a mechanically valid research return pending provenance completion and a separate scientific/source audit. The independent reviewer should produce per-record findings tied to the original batch hash and model revision, with evidence locations, checks performed/not performed, blockers and a recommendation. Engineering integration then handles supported quantities, units, contexts and implementation projection; publication remains a distinct attributed operation. No scientific acceptance decision was made in this inspection.
