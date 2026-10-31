---
id: source-curation-fleet-intake-2026-10-31
type: source
title: Mechanical Intake of the First Multi-Batch Curation Fleet
summary: Eight new returns pass mechanical validation; one conflicting immutable identity across building-energy workers and short-batch completion instructions motivate inventory-backed hour sessions.
status: active
created: '2026-10-31'
updated: '2026-10-31'
topics: [agents, lifecycle, interoperability]
confidence: high
relations:
  - type: relates-to
    target: note-offline-curation-agent-kit
  - type: relates-to
    target: note-offline-curator-instructions
  - type: relates-to
    target: question-curation-evidence-and-approval
  - type: relates-to
    target: source-building-energy-first-curation-review
---

# Fleet intake and process findings

Inspected all ten public ZIPs present in `from-offline-curation-workers/` on 2026-10-31, including eight returns not previously inspected. Scope: ZIP integrity, schema, required fields, deterministic references/rejections, identity consistency and handoff/process disclosures. No external sources were opened or scientific content audited; no records were imported/admitted or original archives changed. Full mechanical snapshot, record hashes, variable definitions and source locations: `data/curation/inventories/fleet-2026-10-31.json`.

| New return | Records | Passing references | Passing rejections |
| --- | --- | --- | --- |
| building-energy-a-b01-return.zip | 4 | 8 | 8 |
| building-energy-a-b02-return.zip | 4 | 8 | 8 |
| building-energy-a-b03-return.zip | 3 | 6 | 6 |
| building-energy-a-b04-return.zip | 3 | 6 | 6 |
| electric-circuits-codex-b01-return.zip | 5 | 12 | 12 |
| electric-circuits-codex-b02-return.zip | 3 | 9 | 9 |
| electric-circuits-codex-b03-return.zip | 3 | 8 | 10 |
| electric-circuits-codex-b04-return.zip | 3 | 9 | 7 |
| New-return total | 28 | 66 | 66 |

All ten archives independently pass `valid-data-awaiting-review`: 37 record occurrences, 36 unique ID/revision pairs, 86 reference checks and 79 rejection checks. All new records retain `requires-extension` and null runtime projections. These are candidate counts, not counts of scientifically distinct or approved relationships. The earlier mechanics audit/admissions remain separate evidence; intake inventory does not infer review status.

## Consolidation conflict

Two different records use `building-energy--constant-power-electricity-consumption@r1`: `building-energy-a-b01-return.zip` (canonical record SHA-256 `a217751e200ca18149070a44032fee1ad853f7a19fb6d6ab3af91122c4b8377c`) and `building-energy-muse-b01-return.zip` (`63033a6f8d728a5bb2766721cdf8426fa9728dbbf63422c27ada2155e0eeaf0f`). Existing central import rejects changed content under a known immutable identity; individual bundle validation cannot detect this fleet-wide condition. Do not import both as though they were compatible revisions. A separate reconciliation/reviewer task must retain both origins, select or qualify a canonical relationship and author an intentional corrected revision if appropriate. Do not solve this by renaming equations per worker. Other similarly titled thermal records may overlap under different IDs; scientific equivalence is not assessed by this inspection.

## Process findings and changes

The old protocol explicitly instructed return after 3–5 records unless assigned a larger run, while missions repeated the same first-batch target. That encourages the reported short turns; no worker runtime instrumentation establishes the exact reason for every turn ending. Release .4 replaces the stop rule with at least 60 minutes of useful work, checkpoints/continued batches, a persistent queue/session receipt, actual timing and explicit interruption status. Scientific quality, source evidence and the 12-record per-batch schema limit are preserved. Six missions now authorize continuing exploration within their boundaries after the seed priorities are covered.

Workers already preserve prior batch identities, backlog, source-access and runtime caveats. New building-energy handoff text still says validation is required after writing; central replay passes, but the final handoff should record actual completed commands/results rather than stale template instructions. Circuits returns contain detailed prior-model and access disclosures. These are process observations, not verification of the reported scientific checks or rights claims. Old runtime-vocabulary snapshots explain some now-stale extension statements; preserve original disclosures and send a fresh snapshot rather than rewriting old returns.

The new zero-inference `curation inventory` operation scans top-level public ZIPs, reports per-file errors, immutable model/batch conflicts and a dated scientific catalog. `kit --inventory` includes only scientific catalog data alongside the one assigned task; it does not carry operator guidance or other assignments. This snapshot reduces duplicate work but does not enforce concurrent ownership or establish global uniqueness. Assign distinct source/subtopic lanes before adding workers to the same broad domain.

## Limits and next checks

Central mechanical validation proves transport/arithmetic compatibility, not source fidelity, reference independence, science or rights. Route new batches to separate auditors. Broad review throughput and semantic reconciliation remain scaling work. The new one-hour protocol has packaging/configuration tests but has not yet been observed completing a real hour-long remote session. Host-specific persistent execution may be needed if its turn limit forces early termination; no cross-PC scheduler was installed. Inspect the first actual session's timestamps, checkpoints, output quality, duplicate rate and interruption reasons before assuming the fleet now runs unattended for an hour.

Verification: all 78 offline tests pass, including conflicting-ID intake, identical retransfers, per-file failures and inventory-backed isolated kits. A freshly extracted .4 generic kit validates its teaching example offline in its own environment. Seven complete kits (generic plus six domains), standalone AGENTS.md/inventory and an existing-worker update ZIP are available directly under `.runs/curation-kits-2026-10-31.4/`. The update ZIP contains only curator instructions, the scientific inventory at its expected path, and checksums; it carries no assignment or toolkit replacement. No paid inference was used. At session closeout the former `ready/` contents were flattened into that release directory; redundant staging and the extracted smoke-test copy were preserved under `.runs/_archive/curation-kits-2026-10-31.4-build/`. Package bytes were preserved and manifest checks rerun.
