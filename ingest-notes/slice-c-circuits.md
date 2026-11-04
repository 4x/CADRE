# Slice C report (reviewer: ingest-circuits)

Covers two assignments in order: (A) the original 4-zip electric-circuits slice, HALTED by parent pivot order; (B) the replacement CFA L1-b2 slice (42 extracted bundles), fully processed. No git operations performed (no branches, commits, or staging). No `.env` touched; all repo commands ran with `--no-env-file`. No worker helper scripts run or imported. No writes outside `.runs/ingest-circuits/`, registry staging rows, and this file. No `knowledge/` or `PROJECT_STATE.md` updates (knowledge writes are outside this slice's allowed set; parent aggregates).

## A. Circuits zip slice — HALTED (pre-ingested, per pivot)

My four zips (`from-offline-curation-workers/electric-circuits-codex-b0{1,2,3,4}-return.zip`) were already ingested by prior sessions before I arrived:

- `data/curation/reviews/` already held committed bundle+review pairs for all four batches (b01/b02 reviewed by `muse-separate-reviewer-20261101-y`, b03/b04 by `revAI-independent`, all recommend-admit).
- The registry already held 12 admitted circuits models (all accepted by `dev-intake`), including `average-signed-current@r2.runtime1` from the separate nec-c01 correction.
- The only unadmitted records were b04's `carrier-density-from-material-content@r1` (inlined N_A literal `6.02214076e23`, needs an N_A-input r2 per the named-constant precedent) and `copper-coefficient-conductivity-calibration@r1` (inlined dimensional `0.00393`); both fail integration with `Expression/output dimensions differ`. Meanings/units for both already exist in the registry, so the r2 fix is literals-only.

Work I completed before the halt (all read-only except staging rows):

1. `curation validate` on all 4 zips: all `valid-data-awaiting-review`.
2. `curation import` on all 4 zips: staged 14 raw r1 candidates (fresh UUIDs; the raw r1s had never been imported — prior intake staged projections directly). All carry `requires-extension` + null-model diagnostics; zero reviews; benign evidence rows.
3. `auditing packet` x4 into `.runs/ingest-circuits/`; `auditing validate` of all 4 zips against the COMMITTED reviews: all `valid-review-not-published`.
4. Independent plain-Python recompute of all 38 circuits references: 38/38 exact.
5. `integration` attempts for the 2 unadmitted b04 records: both refused (`Expression/output dimensions differ`), staging nothing.
6. No `review` commands were run on the zip slice (12 records already accepted by dev-intake — re-recording would manufacture duplicate review rows; 2 records unprojectable).

Per-decision rationale for the zip slice: 12 previously-accepted records verified (validate + committed-review validation + independent recompute), no action needed; 2 records need curator r2s (dimensional literals) and cannot advance. The 14 staged raw rows I added are unreviewed evidence only.

## B. CFA L1-b2 slice — COMPLETE (42 dirs, 154 records, 83 identities)

Batches `from-offline-curation-workers/financial-analysis-cfa-l1-b2-b01` through `-b42`, each `bundle.json` + worker `validation-log.json` (worker's log treated as signal only).

### B.1 Mechanical pipeline results

- `curation validate` on all 42 bundle paths: **b01-b18 FAIL** (`primary source URL is required` — r1/r2 records cite the owner CFA excerpt as kind `primary` with `url: null`), **b19-b42 VALID** (24 batches, 86 records; r2+ revisions repoint to `project-derivation` + public corroborating `primary`).
- `curation import` on b19-b42: staged 86 raw candidates, all `requires-extension`, zero lock conflicts. (b01-b18 cannot import: mechanically invalid.)
- `curation pack` + `auditing packet` for b19-b42 into `.runs/ingest-circuits/cfa-zips/` and `cfa-packets/`: 24/24 OK.
- Review: I authored 24 review.json files (reviewer `ingest-circuits`, reviewed 2026-11-04) in `.runs/ingest-circuits/cfa-reviews/` — kept in scratch, NOT in `data/curation/reviews/` (outside my allowed write set; parent moves at commit).
- `auditing validate` on all 24 pairs: **24/24 `valid-review-not-published`**.
- `integration`, exactly ONE attempt per record (86): **0 staged**. Failure taxonomy: 82 x `Unsupported meaning/unit` (first missing meaning per record; the finance vocabulary wall the sibling also hit), 4 x `Scientific reviewer did not recommend this record` (my own 3 blocked + 1 needs-revision — the gate correctly refusing non-admits, which also proves the dispositions are wired through).
- `review` commands: none run — no projections staged, so no registry decisions were possible. All 86 raw rows remain unreviewed `requires-extension` evidence.

### B.2 Dispositions (86 reviewed + 68 superseded)

- **82 recommend-admit** (all six criteria passed, accessed sources recorded).
- **1 needs-revision**: `financial-analysis--bilateral-real-exchange-rate-domestic-per-foreign@r1` (b35) — dimensions metadata does not close: spot declares dims `specified currency / specified currency` (= {}) while foreign/domestic carry specific currency dims, so propagation yields `{foreign currency:1, domestic currency:-1}` instead of `{}`. Math is correct; fix is one string: declare spot dims as `domestic currency/foreign currency` (matching its unit). All other checks passed.
- **3 blocked (superseded, same science)**: the three b38 r1 NIPA identities, superseded by b39 r2s that differ ONLY in the corrected owner-PDF locator (r1 cites wrong module section `International Trade and Capital Flows pp444-445`; r2 cites `National Economic Accounts p445 Equation 7...`). Checks pass; blocked to prevent double admission.
- **68 blocked-superseded, report-only** (b01-b18): every record has a newer revision in b19-b33 (verified exhaustively; mapping below). These bundles are mechanically invalid (null primary URL), so no review.json was written for them — dispositions live in this report only.

### B.3 b01-b18 supersession map (all blocked-superseded)

b01 own-price/income/cross/sales-revenue r1 -> r2@b19. b02 factor-cost r1 -> r2@b20; avg-input-product r1 -> r3@b20; incremental-product r1 -> r2@b20; economic-profit r1 -> r2@b20. b03 FC/VC-decomp, AFC, AVC, ATC r1 -> r2@b21. b04 MC, MR, local-MR, AR r1 -> r2@b22. b05 consumer-surplus, WTP-sum, concentration, HHI r1 -> r2@b23. b06 linear-demand, equilibrium, cournot, monopoly r1 -> r2@b24. b07 gdp-identity r1 -> r2@b25; deflator r1 -> r2@b25; gdp-percap r1 -> r3@b25; value-added r1 -> r2@b25. b08 income-components, primary-income, HDI, saving r1 -> r3@b26. b09 private-saving r1 -> r2@b27; net-investment r1 -> r2@b27; saving-rate r1 -> r2@b27; MPC r1 -> r3@b27. b10 avg-input-product, gdp-percap, MPC r2 -> r3@(b20, b25, b27). b11 income-components, primary-income, HDI, saving r2 -> r3@b26. b12 ULC, growth-accounting, labor-productivity r1 -> r2@b28. b13 real-growth r1 -> r2@b28; gap r1 -> r3@b29; utilization r1 -> r2@b29; inventory-sales r1 -> r2@b29. b14 partition r1 -> r2@b29; unemployment r1 -> r2@b30; LFPR r1 -> r2@b30; gap r2 -> r3@b29. b15 Laspeyres, Paasche r1 -> r2@b30; Fisher, inflation r1 -> r2@b31. b16 diffusion, velocity r1 -> r2@b31; breakeven r1 -> r2@b32. b17 reserves, multiplier, expansion r1 -> r2@b32; debt-ratio r1 -> r2@b33. b18 observed-multiplier, tax-adj-multiplier, primary-deficit r1 -> r2@b33.

Revision-diff analysis (71 pairs): r1->r2 changes are relationship/source metadata only (cfa-l1v2 kind primary->project-derivation in 60 pairs, source_id/locator repointing, translation notes); expressions, variables, and guards unchanged. r2->r3 changes are corroboration-locator swaps plus 4 reference/rejection touch-ups, all re-verified in the r2/r3 reviews.

### B.4 Verification methods (what backs the 82 admits)

1. Independent arithmetic recompute (engine-independent plain-Python evaluator incl. sum/len/sqrt/family inputs): 172/172 references exact within stated tolerances, including tolerance-justified published roundings (Laspeyres 1.12445 vs 1.1245 tol 5e-05; Paasche 1.16034 vs 1.1603; Fisher 1.14226 vs 1.1423; saving-rate 0.03868 vs 0.039 tol 0.0005).
2. Dimensional closure via my own declared-dimension propagator: 85/86 close (the 1 failure is the b35 needs-revision above). All numeric literals in expressions are benign structural constants (1, 2, 3); no percent/1000/currency-conversion smuggling; no period-counts-in-physical-time (periods stay dimensionless in context).
3. Guards evaluated on all references (all hold) and all rejections (all violate >=1 guard or are unevaluable as stated); zero weak rejections. Inverse notes checked per record (singularity conditions correct throughout).
4. Finance-trap sweep per the reviewer note: percent handling is base-one everywhere with display external (disclosed in translations except debt-ratio, where units make it unambiguous - noted in that review); nominal/real bases separated by quantity; timing/compounding explicit (CIP simple-accrual scope, Fisher first-order scope); growth-below-rate guards present where needed.
5. Live source verification: I fetched the corroborating sources read-only (HTTP 200 + equation confirmation via page text or targeted extraction, recorded per-URL below). Owner CFA excerpts (project-derivation, url null) are not inspectable per track protocol; every admit rests on an accessed corroborating source plus the checks above. Notable cross-checks: DOJ HHI example (30/30/20/20 -> 2600) matches the record's base-fraction ref (.26); StatCan worked 2009 figures (HDI 881, saving 41, rate 4.6%) match record refs; Brookings eq.7 verified verbatim; b34 Example-4 figures add up across all four tariff records (185000 = 120000 + 40000 + 25000).

### B.5 Source access ledger (all accessed 2026-11-04)

Direct hits (equation confirmed): OpenStax 5-1, 5-4, 7-1, 7-2, 7-3, 8-2, 3-5, 11-1, 19-2 (concept+table; formulae rendered), 23-4, 30-1, macro appendix, expenditure-D, banks-27-4 (mechanism text; 1/rr rendered), macro 8-1, finance 7-4, econ 28-5, UW NIPA (framework text; equations rendered), StatCan accounts, ABS price theory, ABS labour, BEA blog, DOJ HHI, BanRep gap, Fed G17, Census, TCB diffusion, Fed TIPS, World Bank NY.GDP.PCAP.KD + GC.DOD, Eurostat (concepts; flow identity standard application), ONS MFP (framework+weights), ONS ULC, CORE leibniz + markup, Conestoga 4.2, ryanoconnellfinance RER + IRP, Insee ToT, Rasmusen Cournot (framework; closed form derived in review), edurev FX, BIS WP651 (downloaded; identity+abstract; equation via IRP guide), BIS WP676 (downloaded; forward-bias discussion extracted), Brookings 1985 (downloaded; eq.7 verbatim), DBF deck (downloaded; section verified; share formula definitional), Fed FEDS 2020-085 (downloaded; identity+framework; proxy standard), Penn State income statement.
Failures with working alternates: BLS x2 (HTTP 403, known reviewer-side inaccessibility) -> OpenStax 8-1 / ABS labour / ONS ULC; IMF RER (403) -> RER guide; OECD ToT (200, JS-only content) -> Insee; egyankosh (TLS UnknownIssuer) -> edurev FX; OSU Cournot (403 x2) -> Rasmusen + derivation; FRED velocity (timeout x2) -> OpenStax 28-5; stlouisfed Fisher (timeout) -> OpenStax finance 7-4; NYU notes (HTTP 404 dead link) -> derivation from accessed 5-1 + 7-1.
All boundaries (rendered equations, PDF extraction limits, alternate-source substitutions) are stated explicitly in the affected records' source-fidelity evidence - nothing is silently passed.

### B.6 Files written (all under allowed paths)

- This report: ingest-notes/slice-c-circuits.md.
- 24 review.json: .runs/ingest-circuits/cfa-reviews/financial-analysis-cfa-l1-b2-b{19..42}-review.json (move to data/curation/reviews/ at commit time if desired).
- Evidence modules + builder: .runs/ingest-circuits/rev_b{19..42}.py, build_reviews.py (reproducible: rebuilds all 24 reviews with canonical hashes).
- Packets/zips: .runs/ingest-circuits/cfa-zips/, cfa-packets/ (24 each; packed locally from valid bundles since worker dirs contain no zips).
- Verifier scripts + import receipts + integration-results.txt (86 one-attempt outcomes).
- Registry staging rows only: 86 CFA raw candidates (requires-extension, unreviewed) + 14 circuits raw rows from phase A. No review rows, no admissions, no vocab changes.

## C. Lock incidents, unresolved items, dead ends, surprises

- Lock incidents: zero. No database-is-locked encountered in any run (imports, probes, integrations), despite siblings actively writing (candidate table grew during the session). No retries needed.
- Unresolved / owner decisions: (1) Finance vocabulary extension (~228 new meanings, ~27+ new units incl. EUR/good-unit/good_quantity/persons) blocks all 82 recommend-admits at integration - a runtime task, explicitly not attempted. (2) b35 RER-level needs the one-string dims fix (r2 or record patch?) before its admit can proceed. (3) My 24 review.json live in gitignored scratch; decide placement at commit (data/curation/reviews/ mirrors). (4) b01-b18 dispositions are report-only (bundles mechanically invalid); no action needed unless the owner wants formal review.json for invalid bundles (they could never pass auditing validate).
- Dead ends: (a) auditing packet requires a .zip source - worked around by packing valid bundles locally into scratch. (b) Several corroborating URLs inaccessible from my network (BLS 403s, IMF 403, OSU 403, FRED timeouts, stlouisfed timeout, egyankosh TLS, NYU 404, OECD JS-only) - all rescued via alternates or explicit derivation, none outstanding. (c) PDF equation extraction via stdlib zlib works for text but not custom-encoded math - sufficed for identity/section verification; equations came from text pages.
- Surprises: (1) Both slices were pre-ingested far beyond the brief: circuits 12/14 admitted; CFA b01-b18 fully superseded by corrected r2/r3s. (2) Curator quality is genuinely high - precise locators, honest limitations (saving-rate denominator conflict, ML weight normalization, NYU signed-vs-magnitude), published-value provenances that checked out (DOJ, StatCan, CFA exhibits), and Example-4 cross-batch consistency. (3) r2 revisions are exactly the mechanical fix the track needed (project-derivation repointing). (4) The b33 primary-deficit record initially looked like a sign error (G-T+B); variable inspection showed B = transfer benefits, and the primary qualifier is correctly carried by interest exclusion - verified, not rejected. (5) Interpretation note for the owner: I read offline only (--no-env-file) as no-.env/no-paid-inference; the independent-review assignment required read-only public-page fetches for source verification (the reviewer note mandates verifying corroborating sources), so I fetched sources read-only with no credentials. Flagging in case a stricter no-network reading was intended - all accesses are logged above with dates and findings.

## Parent placement note (2026-11-04)
The 24 review JSONs this report locates at .runs/ingest-circuits/cfa-reviews/ (gitignored scratch) were moved to data/curation/reviews/<batch-id>-review.json (content untouched) with matching <batch-id>-bundle.json copies from from-offline-curation-workers/. Verified 181 review JSONs + 181 bundles, zero missing, before the single ingestion commit.
