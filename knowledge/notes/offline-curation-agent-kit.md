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

Kit version `2026-10-31.5`; return schema `cm-curation-batch/1`; earlier .1–.4 data returns remain readable. Release .5 adds economics, computer-science, chemistry and biology domains and supersedes the engineering-finance and probability briefs with broadened wave-1 coverage; curator instructions are unchanged from .4. This document is for the owner/integrator and is excluded from worker ZIPs. The complete curator protocol is [[note-offline-curator-instructions]], exported directly as each kit's `AGENTS.md`. It contains the actual instructions, not a redirect to this guide.

## Sustained sessions and fleet dispatch

The owner now requests at least an hour of useful work per session. The previous first-batch stop rule caused short 3–5 minute turns even though 3–5 models was intended as a review checkpoint. Instruction release .4 makes session completion independent of batch completion: default minimum 60 minutes, checkpoints about every 15 minutes or four defensible records, successive batches at most 12 records each, immediate continuation without owner acknowledgement, and a final consolidated report. Quality and scope remain unchanged. Sources/records that block one candidate go to a backlog while the worker advances to another in-scope candidate. There is no model-count quota for an hour.

For existing workers, replace only the extracted worker's `AGENTS.md` with the generated .4 instructions and add the current inventory under `data/curation/catalog-inventory.json`. Preserve its prior returns, toolkit and actual version metadata. Do not replace this repository's root AGENTS.md. Then send:

Ready-made files are directly under `.runs/curation-kits-2026-10-31.5/`. For existing workers, extract `existing-worker-update.zip` into their isolated kit workspace to put those two files in place; it contains no assignment or toolkit replacement. For new workers choose the corresponding `curation-DOMAIN.zip` from that folder, or `curation-generic.zip` for an inline task. Keep this owner guide out of the worker workspace. The former `ready/` nesting is retired: build staging and extracted smoke-test copies are archived separately at `.runs/_archive/curation-kits-2026-10-31.5-build/`. Only the flat release directory is for distribution; do not use archived AGENTS.md files as current instructions. The `.runs/curation-kits-2026-10-31.4/` release remains valid for its six domains; new-domain workers must use .5 kits.

> Read the updated @AGENTS.md and @data/curation/catalog-inventory.json. Continue your current assignment for a sustained session of at least 60 minutes of useful work. Save, validate and pack checkpoints, then continue automatically; do not stop after a batch or await my acknowledgement. Preserve earlier returns, record SESSION.json, and provide one consolidated report at the end. Follow the interruption/resume rules if the host forces you to stop early.

For new workers, hand over the updated domain ZIP and say `Read @AGENTS.md and complete @assignment.json`. Each assignment carries the session defaults. A generic kit still takes the inline assignment JSON; the protocol supplies defaults when older JSON lacks `session`. Explicit smaller correction tasks override this default.

The worker keeps `SESSION.json` and its next research queue outside the data-only ZIPs. On a forced early stop use `Resume the unfinished session from SESSION.json; continue useful work to its time target and then consolidate`. A prompt cannot override a provider's turn/tool limit. If a host repeatedly terminates it, use that host's persistent-task mechanism or an operator-controlled continuation loop that inspects session status and remaining time; do not assume a background worker is running because a file says running. No scheduler or cross-PC orchestration was installed by this change.

Give each concurrent curator a distinct source-family/subtopic lane. Domain boundaries should constrain scientific scope and conventions, while priorities remain seeds. For example, thermal-material/steady heat-transfer relationships and thermodynamic performance/phase-change relationships can be separate building-energy lanes. Do not issue the same broad domain and seed list to multiple workers without a partition. Keep canonical model identities independent of worker names; a worker label belongs in batch IDs and provenance. Changing prefixes would hide, rather than resolve, duplicate science. Additional agents can serve the distinct reviewer role using the auditor kit; curation throughput alone is not reviewed catalog growth.

Refresh a shared scientific inventory at dispatch and between sessions. It contains equations, quantity definitions, source links and immutable record hashes, not other workers' tasks. Frozen snapshots reduce duplicates but cannot prevent simultaneous discovery; record their date/coverage. Before consolidation, reconcile conflicting IDs and review likely equivalent equations under different IDs. Do not silently rename, overwrite or bump someone else's revision to bypass a conflict. Assign a deliberate reconciliation/correction task and preserve originals.

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation inventory from-offline-curation-workers fleet-inventory.json
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation kit building-energy-worker.zip --domain building-energy --inventory fleet-inventory.json
```

Inventory scans public top-level return ZIPs only, validates each independently, reports malformed submissions without losing the rest, and detects changed content under the same model or batch identity. It performs no imports or scientific audit. Identical retransfers are distinguishable from conflicting revisions. Its distinct-ID count is not a count of scientifically distinct models. [[source-curation-fleet-intake-2026-10-31]] records the first fleet inspection and collision.

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

There is no `START-HERE.md`, operator document, full assignment catalog, or collection of other workers' briefs in either shape. The central repository keeps all ten assignment configurations for the owner's selection. Both shapes use the same curator protocol and validator. If updating already-dispatched workers, provide the new whole kit in a fresh directory; do not replace only AGENTS.md while leaving an older validator that still requires connections/queries.

## Ten available assignments

The complete JSON objects live in `data/curation/assignments.json`. Missions now ask for independently reusable atomic models; priorities are seeds for continuing coverage. Domain boundaries organize source-search effort and do not create separate scientific meanings for the same quantity. Existing inventory entries are duplicate-checking hints, not mandatory future destinations.

| Domain | Initial coverage |
| --- | --- |
| building-energy | Constant power/energy, sensible heat, slab conduction, thermal resistance/conductance |
| engineering-finance | TVM family: future value, amortization, effective rate, Gordon growth, Fisher conversion |
| electric-circuits | Ohmic behavior, DC power and bounded resistance definitions |
| water-hydraulics | Flow, volume, pressure/head and hydraulic efficiency definitions |
| classical-mechanics | Scalar motion, kinetic/potential energy and bounded work relationships |
| probability | Event identities, conditioning, total probability, odds and explicitly qualified dependence |
| economics | Elasticities, GDP identity, growth rates and break-even arithmetic |
| computer-science | Amdahl speedup, transfer/capacity accounting and availability composition |
| chemistry | Ideal gas, moles, molarity/dilution and stoichiometric ratios |
| biology | Hardy-Weinberg, discrete growth, allometry and ecological accounting |

Do not hand a worker this table or the entire configuration file. Give only its JSON object or domain kit. Workers may select their own attributable label and unique batch ID if none was supplied. If assigning multiple workers to one broad domain, narrow each assignment's priorities/source families and allocate disjoint batch/model ownership; repeated discoveries should be recorded as overlaps, not different formulas solely because of names.

## Build or rebuild packages

Run from the central repository. Each destination must be new; no existing ZIP is overwritten. Requires uv and Python 3.12+, with no third-party Python packages. The generated archives contain no credentials, inference adapter/configuration, SQLite files, caches or working-copy state. SHA-256 manifests pin file contents but do not prove authorship or scientific correctness.

```powershell
# Generic kit for the owner's inline JSON assignment prompt:
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation kit curation-generic-2026-10-31.5.zip
# A worker-specific kit containing only one assignment:
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation kit curation-building-energy-2026-10-31.5.zip --domain building-energy
```

Copy/extract each kit into a new worker folder, such as `C:\Curation\worker-a`. Provide the short prompt and optionally an agent label/batch ID. There is no API key to distribute; these tools make no inference requests. External agent-service spending is outside the central application's ledger. Do not copy the inference ledger or run independent paid application-curation loops on several PCs under the assumption that their local limits add up to a global budget.

The toolkit is a frozen task snapshot. Standalone workers do not need the central Project Memory CLI or repository AGENTS.md. Their package's own AGENTS.md supplies the full role protocol. Integration agents working in the repository continue to follow its normal instructions and memory protocol.

## Return and integrate data

### After a worker completes a batch

Keep its return ZIP and validation summary. Review an early batch before scaling the same worker's output, so systematic mistakes are corrected once. Publication/import is independent of assigning more research: you can queue useful new work while central review continues. The worker does not need a fresh clone or a repeated setup ceremony; reuse its isolated kit workspace with a new batch directory. If the shared protocol/validator changed, distribute the updated kit once in a fresh folder and carry over only public prior return artifacts for duplicate checking.

For another sustained session in the same domain (no message is needed between checkpoints of a running session):

```text
Continue the current domain from SESSION.json and your prioritized backlog for another session of at least 60 minutes. Follow AGENTS.md, preserve prior returns, avoid duplicates, and save multiple validated batches without waiting for my acknowledgement. Return one consolidated session report.
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
