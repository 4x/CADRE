# CFA formula curation track (owner guide)

One domain (`financial-analysis`), one pack, one sentence per PDF. Everything a curator agent needs is prebuilt in `external-pack/` — the kit, the assignment, the source brief, the inventory, and the instructions.

## The human does three things

1. **Copy** `data/curation/cfa/external-pack/` to the external worker location.
2. **Drop** the purchased CFA PDFs into the pack's `sources/` folder.
3. **Say** (one curator agent per PDF):
   `Read AGENTS.md and extract all models and equations from sources/CFA-Level-1-book1.pdf`

That is all. The agent manifests the PDF itself (filename, SHA-256, level, book), works the book cover to cover in `financial-analysis-cfa-l1-b1-b01, b02, …` batches, validates and packs each batch, and hands back `*-return.zip` files plus a consolidated report. There are no lane splits and no excerpt packets to write: the agent reads the PDF directly, cites exact locators, and corroborates every record against a directly inspected accessible source.

## Rights note

The purchased PDFs are owner material for the owner's own agents. The pack enforces the safeguards where they matter: the PDF stays in `sources/`, and returns carry single-formula transcriptions with locators only — never the PDF, pages, screenshots, or long verbatim passages. Do not commit PDFs to the repo.

## What is in this folder

- `external-pack/` — the built dispatch folder (copy it, don't edit it; rebuild with the script below).
- `build_external_pack.py` — rebuilds the pack with a fresh kit + inventory: `uv --cache-dir .uv-cache run --no-env-file --offline data/curation/cfa/build_external_pack.py --force`
- `pack-AGENTS.md` — source of the pack's root `AGENTS.md` (mission, manifest step, commands).
- `cfa-source-brief-direct-pdf.md` — source of the pack's `cfa-source-brief.md` (PDF citation, corroboration rule, finance rules).
- The unified assignment lives in `data/curation/assignments.json` (domain `financial-analysis`); the build script copies it into the pack, and the kit embeds it too.
- `source-manifest.pack-template.json` — the agent-fillable manifest template shipped in the pack.
- `reviewer-note-cfa-sources.md` — attach to auditor packets for CFA returns.
- `assignments/cfa-lane-*.json`, `curator-brief-cfa-sources.md`, `excerpt-packet.template.md`, `source-manifest.template.json` — superseded by the unified pack; kept for history. Do not dispatch these.

## Intake (owner/integrator, standard flow)

Review each PDF's first batch before that worker scales:

```powershell
uv --cache-dir .uv-cache run --no-env-file --offline -m connected_models.curation validate incoming/financial-analysis-cfa-l1-b1-b01-return.zip
uv --cache-dir .uv-cache run --no-env-file --offline -m connected_models.auditing packet incoming/financial-analysis-cfa-l1-b1-b01-return.zip reviewer-packet-cfa-l1-b1-b01.zip
```

Give the auditor the extracted packet plus `reviewer-note-cfa-sources.md`. Then the standard validate/integrate/review flow from the fleet guide applies.

## Scope notes

- CFA ethics/standards material is out of scope: no quantifiable relationships, no curation.
- Several CFA formulas need engine capabilities beyond the scalar profile (iterative IRR solving, normal CDF for Black-Scholes, regressions needing summation over samples). Curators defer these with exact sources and the missing capability; they do not approximate them. The engine already supports `log`, `log10`, `exp`, `sqrt`, `sum`, `prod`, `len` forward-only, plus index families — binomial lattices and multi-asset sums may be expressible; iterative solvers are not.
- No investment advice, forecasts, or recommendations anywhere in records; records are mathematical formalizations with scope and provenance.
