---
id: note-offline-curation-agent-kit
type: note
title: Portable Offline Curation Agent Kit and Fleet Handoff
summary: Owner-only fleet dispatch, isolated worker kits, compatible data returns and central review; curator protocol lives separately and targets atomic reusable models.
status: active
created: '2026-10-31'
updated: '2026-10-31'
topics:
  - agents
  - lifecycle
  - interoperability
confidence: medium
relations:
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: relates-to
    target: question-curation-evidence-and-approval
  - type: relates-to
    target: note-mvp-build-sequence-and-extension-triggers
  - type: supported-by
    target: source-offline-curation-starter-sources
---

# Owner/operator guide: offline model curation

Kit version `2026-10-31.3`; return schema `cm-curation-batch/1`; earlier .1/.2 data returns remain readable. This document is for the owner/integrator and is excluded from worker ZIPs. The complete curator protocol is [[note-offline-curator-instructions]], exported directly as each kit's `AGENTS.md`. It contains the actual instructions, not a redirect to this guide.

## Corrected scope and packaging

The owner clarified that the long-term collection should contain thousands of atomic, granular, composable models. Curators should qualify individual relationships independently of how they will be composed later. No chain, existing-demo fit, application scenario or connection to another model in the same batch is required. Three to five models is an initial review-batch size, not a target catalog size. Successive batches can expand coverage after the first review.

The first kit mixed operator and worker guidance, and its thin `AGENTS.md` redirected workers to both. It also required a connected chain and nonempty connection/query lists. Those choices are corrected: the full curator-only protocol is now in `AGENTS.md`; operator material and other assignments are omitted from every worker ZIP; `handoff.connections` and `handoff.queries` may be empty. The earlier kit is retained in history. Returns created with kit `2026-10-31.1` remain accepted; the original building-energy return was not rewritten.

## Recommended distribution

Use an isolated extracted ZIP per worker, on this PC or another PC. Git clones/worktrees are unnecessary for source research; reserve them for agents actually assigned code or vocabulary integration. A standalone long prompt is insufficient to pin the validator/schema, but the task prompt should stay as short as the owner's preferred form:

```text
Read @AGENTS.md and work on <the single assignment JSON object>.
```

There are two supported package shapes:

| Package | Worker sees | Dispatch prompt |
| --- | --- | --- |
| Generic kit | Complete AGENTS.md, schema/example/vocabulary, minimal offline tools; no assignments | Read @AGENTS.md and work on {the one assigned JSON object} |
| Domain kit | The same files plus only that domain's assignment.json | Read @AGENTS.md and work on @assignment.json. |

There is no `START-HERE.md`, operator document, full assignment catalog, or collection of other workers' briefs in either shape. The central repository keeps all six assignment configurations for the owner's selection. Both shapes use the same curator protocol and validator. If updating already-dispatched workers, provide the new whole kit in a fresh directory; do not replace only AGENTS.md while leaving an older validator that still requires connections/queries.

## Six available assignments

The complete JSON objects live in `data/curation/assignments.json`. Missions now ask for independently reusable atomic models; priorities are seeds for continuing coverage. Domain boundaries organize source-search effort and do not create separate scientific meanings for the same quantity. Existing inventory entries are duplicate-checking hints, not mandatory future destinations.

| Domain | Initial coverage |
| --- | --- |
| building-energy | Constant power/energy, sensible heat, slab conduction, thermal resistance/conductance |
| engineering-finance | Discounting, annualization, rate conventions and deterministic project definitions |
| electric-circuits | Ohmic behavior, DC power and bounded resistance definitions |
| water-hydraulics | Flow, volume, pressure/head and hydraulic efficiency definitions |
| classical-mechanics | Scalar motion, kinetic/potential energy and bounded work relationships |
| probability | Event identities, conditioning and explicitly qualified dependence |

Do not hand a worker this table or the entire configuration file. Give only its JSON object or domain kit. Workers may select their own attributable label and unique batch ID if none was supplied. If assigning multiple workers to one broad domain, narrow each assignment's priorities/source families and allocate disjoint batch/model ownership; repeated discoveries should be recorded as overlaps, not different formulas solely because of names.

## Build or rebuild packages

Run from the central repository. Each destination must be new; no existing ZIP is overwritten. Requires uv and Python 3.12+, with no third-party Python packages. The generated archives contain no credentials, inference adapter/configuration, SQLite files, caches or working-copy state. SHA-256 manifests pin file contents but do not prove authorship or scientific correctness.

```powershell
# Generic kit for the owner's inline JSON assignment prompt:
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation kit curation-generic-2026-10-31.3.zip
# A worker-specific kit containing only one assignment:
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation kit curation-building-energy-2026-10-31.3.zip --domain building-energy
```

Copy/extract each kit into a new worker folder, such as `C:\Curation\worker-a`. Provide the short prompt and optionally an agent label/batch ID. There is no API key to distribute; these tools make no inference requests. External agent-service spending is outside the central application's ledger. Do not copy the inference ledger or run independent paid application-curation loops on several PCs under the assumption that their local limits add up to a global budget.

The toolkit is a frozen task snapshot. Standalone workers do not need the central Project Memory CLI or repository AGENTS.md. Their package's own AGENTS.md supplies the full role protocol. Integration agents working in the repository continue to follow its normal instructions and memory protocol.

## Return and integrate data

### After a worker completes a batch

Keep its return ZIP and validation summary. Review an early batch before scaling the same worker's output, so systematic mistakes are corrected once. Publication/import is independent of assigning more research: you can queue useful new work while central review continues. The worker does not need a fresh clone or a repeated setup ceremony; reuse its isolated kit workspace with a new batch directory. If the shared protocol/validator changed, distribute the updated kit once in a fresh folder and carry over only public prior return artifacts for duplicate checking.

For another batch in the same domain:

```text
Thank you. Continue with the next batch in the same domain, using your prioritized backlog. Follow AGENTS.md, preserve previous returns and avoid resubmitting models already covered. Return the next validated batch.
```

For a different domain, the owner's short form is sufficient:

```text
Thank you. Now work on {the new assignment JSON object}.
```

The revised AGENTS.md makes this replace the old assignment, while preserving the shared protocol, stable curator label and prior evidence. The worker selects a fresh batch ID/folder and checks its known inventory automatically. If the new assignment was saved as a file, say `Now work on @new-assignment.json` explicitly; do not leave it unclear whether an old packaged assignment still applies.

For corrections to this first batch before more building-energy expansion:

```text
Revise your first building-energy batch using the attached review findings. Keep the original ZIP unchanged. Return a new correction batch with incremented revisions for the changed model IDs, and explain which findings each revision addresses. Validate and package it under the updated AGENTS.md. This is revision work, not approval of the first batch.
```

Provide the actual findings or the review document, not just a claim that a review exists. The relevant findings are recorded in [[source-building-energy-first-curation-review]]. Once those are addressed, use either continuation prompt above. There is no need to tell the other workers to stop while one worker corrects its batch.

Workers return a data-only ZIP containing exactly `bundle.json` and `manifest.json`. Keep the original ZIP and final message. Do not copy their toolkit, merge working folders, or combine SQLite databases. Validate with central trusted tools; the importer reads allowlisted ZIP members without extracting or executing agent files.

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation validate incoming/building-energy-a-b01-return.zip
# Run only when ready to stage the reviewed intake for further central review:
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation import incoming/building-energy-a-b01-return.zip
uv --cache-dir .uv-cache run --no-env-file -m connected_models candidate CANDIDATE_ID
uv --cache-dir .uv-cache run --no-env-file -m connected_models review-bundle
```

Validation checks format, bounded scalar arithmetic, references/guards and optional runtime contracts. It does not verify scientific dimensions for research-only records, source fidelity, oracle independence, prose assumptions/inverses, rights or claimed composition edges. Inspect those before admission. New domains can produce useful research records long before the runtime supports their units. Never coerce a new quantity into an existing label to make a candidate execute.

Import stages candidates only and preserves evidence, curator, original kit version and blockers. It creates no admissions. Reimporting an identical batch is idempotent. Changed record content under an existing ID/revision fails; corrections need a new revision. Validation/collision checks precede staging; after a partial storage failure, reimport safely completes the batch. Serialize central intake/review; this is not a distributed registry. Keep the original ZIP and printed receipt as the full batch record, including deferred discoveries.

Once a candidate fits the runtime and an authorized reviewer has checked the relevant evidence, the existing local command records that attributed decision:

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models review CANDIDATE_ID --decision accepted --reviewer REVIEWER_ID --notes 'Evidence actually checked, permitted scope and remaining limitations'
```

Workers do not self-admit. An independent agent technical review is not automatically human expert validation. Extension candidates remain blocked until a separately tested integration produces a new checked projection/revision. Scientific uncertainties remain blockers even after code supports the units. Subsequent application query tests validate integration; they are not a curation requirement for every atomic model.

## Separate auditor handoff and technical integration

Create one reviewer-only packet for a returned ZIP. Give the extracted packet to a different agent with `Read @AGENTS.md and complete @assignment.json`. The full protocol is [[note-offline-auditor-instructions]]; no owner instructions or other assignments are in the packet. It contains the unchanged return, exact batch/archive/record identities, JSON Schema and an unfinished report template. The auditor returns `review.json`; central tools validate it. The worker does not need the application or API credentials to investigate sources and write JSON.

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models.auditing packet incoming/return.zip reviewer-packet.zip
uv --cache-dir .uv-cache run --no-env-file -m connected_models.auditing validate incoming/return.zip incoming/review.json
uv --cache-dir .uv-cache run --no-env-file -m connected_models.integration incoming/return.zip incoming/review.json MODEL_ID --version r1.runtime1
```

The versioned review covers every original record, binding ID/revision and canonical content hashes. Each of six criteria records passed/failed/not-checked with evidence, actual source locations, blockers, permitted use and recommendation. Not-checked/failed criteria, absent accessed sources, curator self-review and stale hashes prevent an admission recommendation. A report can validly recommend revisions or block every record. This is structural enforcement, not automatic verification of the auditor's scientific claims or identity.

Integration stages only a `recommend-admit` record whose unchanged quantities/units/expression/guards fit the runtime and reproduce its references. It preserves the full original record, reviewer report/digest and profile in a separately versioned projection. The explicit attributed `review CANDIDATE_ID ...` operation above still grants executable eligibility. Neither packet creation, report validation nor projection publishes models. Reviewers must accurately qualify rights/access rather than invent clearance; current-site terms and a historical edition's license must not be conflated.

## Lessons from the first return

[[source-building-energy-first-curation-review]] records the review of `from-offline-curation-workers/building-energy-muse-b01-return.zip`. Its four records pass mechanical checks and preserve unsupported physical units. Source review found useful formula extraction alongside incorrect current-license attribution, a claimed connection with no destination port, a single-event/seasonal example mismatch, overbroad inverse exclusions and reference-oracle wording that needs correction. The original artifact remains untouched and unadmitted.

The new curator instructions explicitly address faithful source versus profile scope, signed relations, generic quantity identities, property conditions, source versus introduced symbols, source-reported versus derived oracle values, actual-port connection checks, per-target inverse checks, rights-page provenance, and active-time versus calendar/meter boundaries. These are improvements in instructions and review, not claims of a new automated scientific validator.

## Scaling toward thousands of models

1. Review the first few records from each worker to catch systematic interpretation errors before repeating them at scale.
2. Continue source-family/subdomain assignments in bounded batches. Maintain a central inventory of model identities, quantity definitions, evidence and overlaps; periodically distribute relevant read-only inventory snapshots. Until that tooling exists, workers state that duplicate checks are limited to their supplied snapshot and their own batches.
3. Count distinct qualified relationships, evidence quality and review throughput. Do not count rearrangements, renamed units, same-law sign profiles or copied references as new coverage. Preserve legitimately different calibrations/validity regimes and explain them.
4. Reconcile meanings, context requirements and model identities centrally. Domain-prefixed record IDs are provisional provenance keys, not permanent parallel ontologies. Do not make every worker design universal semantics or all possible future connections.
5. Prioritize runtime extensions from the actual returned corpus and product needs. The research catalog can grow independently. Add query/composition tests when integrating selected models, without turning those examples into catalog-wide scope restrictions.

Automated semantic deduplication, scalable retrieval, broad review governance and universal vocabulary governance remain future work. A bounded structured review handoff now exists as described above; it does not solve scientific review at catalog scale. The working MVP and hackathon submission track remain separate milestones.

## Optional Git workflow for code integration

If a worker is separately assigned runtime/vocabulary changes, use an isolated clone on another PC or a dedicated worktree on the same PC, starting from the chosen feature commit. Never work on main/develop or share live working trees/databases. Return code as a reviewed commit/PR, or a Git bundle for disconnected transport; merge/cherry-pick centrally after tests. Research records still pass through the same data importer rather than gaining publication authority through a Git merge.

```powershell
git worktree add -b integrate/curation-units ../connected-models-units BASE_COMMIT
# Remote alternative:
git clone REPOSITORY_URL connected-models-units
Set-Location connected-models-units
git switch -c integrate/curation-units BASE_COMMIT
```

## Verification history

The original kit passed 63 offline tests and a fresh extracted-environment validation. Revision .2 passes all 67 offline tests, including packaging isolation, optional connection/query coverage, and backwards-compatible transport tests. The first real return is revalidated against the new tools without altering its original kit version or content. These tests establish the machinery and role separation, not scientific approval of the returned models.
