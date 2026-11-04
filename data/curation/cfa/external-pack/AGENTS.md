# CFA curation pack — start here

Your mission: extract every quantifiable model and equation from the CFA PDF the owner names (under `sources/`), as atomic reusable `financial-analysis` records. One PDF per session unless the owner says otherwise.

## Folder map

- `AGENTS.md` — this file: mission, first steps, commands.
- `assignment.json` — your exact assignment (domain, priorities, boundaries, session contract).
- `cfa-source-brief.md` — how to cite the PDF, corroboration rule, finance-specific rules.
- `source-manifest.template.json` — fill one copy per PDF before the first batch.
- `sources/` — the owner's PDFs. Read the one named in your dispatch; never copy, rename, or redistribute them.
- `kit/` — the extracted curation kit: full protocol (`kit/AGENTS.md`), validator, schema, vocabulary, inventory. All work files live here: `kit/returns/`, `kit/SESSION.json`, `kit/source-manifest.json`.

## Step 0 — manifest the PDF (before any research)

1. Capture the actual UTC start time first (host clock); you need it for `SESSION.json` elapsed-work accounting.
2. Confirm the dispatched PDF is in `sources/`. If it is missing, stop and ask the owner — do not substitute another PDF.
3. Confirm you can read PDFs (a document reader, `pypdf`/`fitz`, or equivalent). The kit ships no PDF tooling: if nothing is installed, one networked `uv run --with pypdf` (or your host's package install) covers the session; curation and validation themselves stay offline. If you truly cannot read the PDF, report that as a blocker instead of guessing content.
4. Hash it (any OS with Python):
   `python -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" sources/NAME.pdf`
5. Copy `source-manifest.template.json` to `kit/source-manifest.json` and fill every field: filename, SHA-256, CFA level, book number, publisher, title, edition/year, page count if your tools report it.
6. Start `kit/SESSION.json`: session ID, assigned PDF + manifest SHA-256, curator label, start timestamp, status, next action.

## Step 1 — read the protocol

Read `kit/AGENTS.md` (the complete curation protocol), then `assignment.json`, then `cfa-source-brief.md`. Where the brief and the kit conflict on sources, the brief wins for source handling only.

## Step 2 — work the PDF cover to cover

Follow the kit session contract (60+ useful minutes, ~15-minute checkpoints, 3–5 records per batch, validate + pack each batch, then continue without asking). Queue at least ten candidates ahead from upcoming readings. Batch IDs name the PDF: `financial-analysis-cfa-l1-b1-b01`, `b02`, … (level/book from your manifest, lowercase slugs only); if the dispatch names a batch ID explicitly, the dispatched ID wins. Model IDs use the `financial-analysis--` prefix.

Every record needs its exact PDF locator (reading/section, printed page AND PDF page, equation/exhibit number) plus one directly inspected accessible corroborating source, per the brief.

## Commands (run from `kit/`)

```powershell
cd kit
New-Item -ItemType Directory -Path returns/financial-analysis-cfa-l1-b1-b01
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation init financial-analysis returns/financial-analysis-cfa-l1-b1-b01/bundle.json --agent YOUR-LABEL --batch-id financial-analysis-cfa-l1-b1-b01
# Edit the bundle with actual research, then:
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation validate returns/financial-analysis-cfa-l1-b1-b01/bundle.json
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation pack returns/financial-analysis-cfa-l1-b1-b01/bundle.json returns/financial-analysis-cfa-l1-b1-b01-return.zip
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation validate returns/financial-analysis-cfa-l1-b1-b01-return.zip
```

Use your own label and the next unused batch ID per batch. Never overwrite a packed return. `--offline` may be added once Python is installed; validation and packing need no third-party packages or credentials (only a PDF reader install may need the network once, per Step 0). Note `uv` writes progress to stderr: on PowerShell a successful command may still show red text — trust the JSON result, not the stream color.

## Rights (non-negotiable)

- The PDF stays in `sources/`. Returns contain single-formula transcriptions with locators only — never the PDF, pages, screenshots, or long verbatim passages.
- Cite the PDF exactly per the brief (title, edition, locator, `Purchased owner copy; personal-use terms assumed; no redistribution`).
- Never claim access you lack, and never invent legal clearance.

## Hand back

At session end, hand back every `kit/returns/*-return.zip` plus one consolidated report (batches, records, validation results, deferred coverage, blockers, next priorities), per the kit session contract. Keep `kit/SESSION.json` current throughout.
