# Slice E intake report: CFA L1 b3 b01–b50 (reviewer ingest-cfa-b3a)

50 extracted worker bundles, 155 records, curator codex-cfa-l1v3, kit 2026-10-31.9. No committed reviews existed for these dirs; this independent review is the decision. Reviewer: ingest-cfa-b3a. Date: 2026-11-04.

## Verdict counts

- recommend-admit: 97 (all currently blocked-on-vocab-extension at integration; see below)
- needs-revision: 17 (all citation/provenance defects; math verified and stands in every case)
- blocked: 41 (11 invalid-superseded b01–b03; 7 in-slice superseded/withdrawn; 20 superseded by newer staged lineage in sibling slices; 3 duplicates of eligible records)

## Pipeline results

- `curation validate`: b01–b03 FAIL (null-URL primary: the worker cited the purchased CFA PDF as `primary`, against the direct-PDF brief); b04–b50 all `valid-data-awaiting-review`.
- `curation import`: 47/47 valid batches staged (144 intake candidates). Idempotent (re-import mints nothing new). Zero lock incidents.
- `auditing packet`: skipped with reason — sources are extracted bundle.json dirs, not return zips (packet requires `.zip`), and there is no separate reviewer recipient (I am the reviewer).
- `auditing validate`: 47/47 `valid-review-not-published` (review files in `ingest-notes/slice-e-work/reviews/`).
- `integration --version runtime1`: 97/97 recommend-admit records refused with `Unsupported meaning/unit` (first missing meaning per record logged in §Integration). One clean attempt each, no retries, no remapping, per parent instruction. All 97 are scientifically approved but blocked-on-vocab-extension.
- `connected-models review`: 0 recordable — all staged candidates are model-less intake rows and the CLI refuses them (probe on e6ace2e9 confirmed: `Invalid object fields; required: assumptions, expression, ...`). All decisions live in the review JSONs + this report.

## Verification methods (what I actually did)

- Read all 50 bundles in full (5845-line condensed dump; every variable, guard, reference, rejection case, source, and handoff note).
- Independent arithmetic: my own restricted evaluator (`slice-e-work/refcheck.py`) recomputed all 310 references: 310/310 in tolerance; all 554 guard evaluations satisfied on reference inputs; rejection-case structure sane. Inverse identities spot-verified algebraically (trade-credit EAR inversion, treasury-stock proceeds identity).
- Source verification: opened ~45 cited/accessible pages and PDFs. PDF text extracted with a stdlib Flate/Tj scraper (`slice-e-work/pdfextract.py`): CFA ratio list (all 41 ratios confirmed verbatim), revenue-recognition paper (Fig 8/9/10 topics confirmed p13), Wiley CFA excerpt (Reading-16 LIFO material + Caterpillar 3557/4010 solution confirmed), SME modules 05/06/07/29 (TCI definition, equity structure, cash components, current-tax measurement confirmed). Truncated HTML fetches were verified by grepping the full saved page text.
- Registry overlap: intersected all 155 IDs against staged candidates and eligible models; compared expressions/variables of every same-ID and same-science case.
- Worker validation-logs treated as signal: spot-checked, never trusted for verdicts.

## Per-batch verdicts (rationale condensed; full 6-criteria evidence in review JSONs)

- b01 (3 r1s): BLOCKED — invalid (null-URL primary + source_id into the uninspectable PDF); superseded by b04 r2s. Report-only (no review.json possible: review validation validates the bundle first).
- b02 (3 r1s): BLOCKED — same; superseded by b05 r2s. Report-only.
- b03 (5 r1s): BLOCKED — same; superseded by b06 r2s. Report-only.
- b04: SL-depreciation r2 BLOCKED (duplicate of eligible computer-science--straight-line-annual-depreciation@r2/runtime1: identical equation/guards/oracles); declining-balance-uncapped r2 ADMIT (OpenStax 11.3 verified); basic-EPS r2 ADMIT (OpenStax eq 6.27 verbatim + ratio-list #38).
- b05: if-converted-preferred r2 ADMIT (NYU verified); if-converted-debt r2 ADMIT (KPMG URL live but text-unextractable; formula exact per opened ASC 260 guide + NYU); treasury-stock r2 ADMIT (NYU + ASC 260 guide verified).
- b06: all 5 r2s ADMIT — common-size (Appendix A verified), gross margin (key-terms exact + ratio-list #15), net margin (14-7 Table 14.4 + #18), operating margin (#16), pretax margin (#17).
- b07: all 3 ADMIT — BS common-size (Appendix A), current + quick (Banyan Goods data 200000/100000=2.0, 160000/100000=1.6 + ratio-list #1/#2).
- b08: all 3 ADMIT — cash ratio (19-1 eq 19.3 verbatim + #3), LT D/E + total D/E (Damodaran verified; interest-bearing scoping matches ratio-list #29).
- b09: all 3 ADMIT — FCFF-NI, FCFF-CFO, FCFE-CFO match the CFA refresher Summary verbatim (+ ratio-list #40/#41); negative-WC case verified.
- b10: all 3 ADMIT — direct-method reconciliations match OpenStax 16-6 Propensity computations exactly.
- b11: all 4 ADMIT — CFO performance ratios; Figure-9 topic confirmed in extracted paper; formulas exact per opened CFA cash-flow-ratios page.
- b12: all 4 ADMIT — coverage family incl. CF-per-share ((CFO-prefdiv)/shares); Figure-10 topic confirmed; formulas exact per opened page.
- b13: all 4 ADMIT — leverage ratios match CFI list + ratio-list #28/#30/#32 (+ #29 scoping).
- b14: both ADMIT — indirect reconciliation (16-3 Propensity numbers exact) + retained rollforward (4-5 verbatim 4565).
- b15: all 4 ADMIT — turnovers match ratio-list #5/#7/#9/#14; receivables is the total-revenue variant, distinct from staged sibling credit-sales variant (b59 r1 + b67 r2).
- b16: all 4 ADMIT — DSO/DOH/DPO/CCC match #6/#8/#10/#11; Apple -76-day CCC verified.
- b17: all 3 ADMIT — WC/FA turnover + defensive interval match #12/#13/#4.
- b18: all 4 ADMIT — operating ROA/ROA/ROE/ROCE match #19/#20/#21/#24.
- b19: all 4 ADMIT — tax burden/interest burden/EBIT margin/pretax ROC match #25/#26/#27/#22.
- b20: both ADMIT — DuPont 3-factor + 5-factor; Figure-8 topic confirmed; all factors in ratio-list.
- b21 (3 r1s): BLOCKED — superseded by b22 r2s (same math, fixed source metadata).
- b22: all 3 r2s ADMIT — LIFO reserve + FIFO COGS/NI; Wiley Caterpillar solution (3557→4010) + IFT verbatim.
- b23: all 4 ADMIT — fixed-charge/payout/retention/sustainable-growth match #34/#35/#36/#37.
- b24: both ADMIT — NRV (IAS 2 rule + CFA-notes formula verbatim) + LIFO-liquidation pretax unit effect (matches opened concept page method verbatim).
- b25 (3): NEEDS-REVISION — BSEC primary URL 404; math fully verified (opened CFA cash-flow-ratios page); re-cite and re-submit.
- b26 (4): NEEDS-REVISION — BSEC 404 (P/S math exact per opened page; P/CF r1 also superseded by b27 r2 metric correction; per-share math definitional).
- b27 (3): NEEDS-REVISION — BSEC 404; math verified (P/CF r2 raw-CFO binding correct).
- b28: UOP + carrying-amount ADMIT (OpenStax 11.3); age + remaining-life NEEDS-REVISION (Runsten dissertation URL 404; math exact per opened AnalystPrep CFA page).
- b29: both ADMIT — asset-sale gain/loss (16-3 land-sale mechanics) + FVLCD (IAS 36 summary verbatim).
- b30: asset DTL + asset DTA r1s BLOCKED (superseded by staged b61 r3s + b64 r4s, same math); effective-tax-rate r1 ADMIT (CFI exact; EDGAR bot-blocked, precise locator).
- b31 (4 r1s): BLOCKED — superseded by staged r3/r4 lineage (b61/b62 r3s + b64/b65 r4s, same math).
- b32: bond rollforward r1 ADMIT (13-2 tables exact both directions); extinguishment r1 BLOCKED (superseded by staged b62 r2 + b65 r3); deficit r1 BLOCKED (superseded by b33 r2 + staged b60 r3 + b65 r4).
- b33: deficit r2 BLOCKED (superseded by staged b60 r3 + b65 r4, same math).
- b34: DOL r1 BLOCKED (duplicate of eligible economics--degree-operating-leverage-at-sales-level@r1.runtime1; shared total_contribution_margin meaning); DFL + DCL r1s ADMIT (TNOU URL live; CFI exact).
- b35: market-cap r1 BLOCKED (worker-withdrawn; book-1 b27 r2 canonical, staged 5c8df121); break-even r1 BLOCKED (superseded by b36 r2; lineage duplicates eligible econ break-even); EV r1 BLOCKED (superseded by b36 r2).
- b36: break-even r2 BLOCKED (duplicate of eligible economics--break-even-units@r1/runtime1); EV r2 ADMIT (CFI verified; EDGAR bot-blocked).
- b37: tangible-BV ADMIT (formula verbatim per opened page; EDGAR bot-blocked); inventory-COGS NEEDS-REVISION (formula verified on cited 7-2, but the attributed Gearhead oracle numbers appear on neither cited page — fix provenance); EBIT-coverage ADMIT (6-4 eq 6.25 verbatim + #33).
- b38: combined-ratio ADMIT (formula verified; earned-premium basis caveat in permitted use; EDGAR bot-blocked) + after-tax-ROIC ADMIT (WSP verbatim; EDGAR bot-blocked); trade-credit-EAR NEEDS-REVISION (Winkler repository URL migrated; math + 44.59% oracle exact per opened page).
- b39: all 4 ADMIT — accounting equation (14-3 verbatim; OVERLAP: same science as staged buffy balance-sheet-identity@r1 c6658d80 — this record better evidenced, admit only one), net receivables (9-2 verbatim), treasury shares (14-1 Waystar), goodwill (IFRS 3 verbatim).
- b40: all 3 ADMIT — cash rollforward (SME-07 components extracted), direct CFO (entre 9-4 pizzeria verbatim), TCI (SME-05 glossary verbatim).
- b41: all 3 ADMIT — FIFO retained earnings (Wiley + conversion family) + writedown adjustments (CFA analytical logic; solution-7 numbers unconfirmed, disclosed).
- b42: borrowing-costs r1 BLOCKED (superseded by staged b62 r2 + b66 r3); equity-rollforward r1 BLOCKED (superseded by b43 r2); total-life NEEDS-REVISION (Runsten 404; math in CFA heuristic family).
- b43: equity-rollforward r2 ADMIT (SME-06 paras 6.2-6.3 structure extracted).
- b44: lease-liability r1 BLOCKED (superseded by staged b55 r2, same math+source); operating-lease ROU amortization ADMIT (ASC 842 single-cost mechanics per opened PwC guide; EDGAR bot-blocked).
- b45 (2 r2s), b46 (4 r2s): BLOCKED — superseded by staged r3/r4 lineage (same math, AASB re-corroboration).
- b47 (3 r1s): BLOCKED — superseded by staged b63 r2s + b66 r3s (same math).
- b48: all 3 ADMIT — trailing P/E (investor.gov live-but-JS-gated + OpenStax 6.5), EV/EBITDA (CFI verbatim; SEC bot-blocked), EBITDA build (CFI; EDGAR bot-blocked).
- b49: trend-index NEEDS-REVISION (CSUS 404; math per opened UMGC page); comprehensive-EPS NEEDS-REVISION (Columbia archive retired; only non-standard record in slice; needs a live source + confirmation).
- b50: SL bond amortization ADMIT (13-2 rule; signed form; constructed oracles honestly labeled), interest-from-coupon-and-amortization ADMIT (13-2 table mechanics), current-tax ADMIT (SME-29 verbatim).

## Integration refusals (all 97 admit-track records; first missing meaning each)

Asset/financial-statement meanings: asset_beginning_book_value, depreciable_asset_cost, asset_historical_cost, asset_fair_value, asset_sale_proceeds, total_assets, gross_accounts_receivable, acquisition_consideration_fair_value, beginning_cash_and_equivalents, gross_operating_cash_receipts, beginning_retained_earnings, beginning_shareholders_equity, fifo/lifo inventory and income meanings, inventory meanings, liquidated_inventory_unit_count, bond meanings (face, coupon, opening carrying), taxable_profit, income_tax_expense, current_assets, cash_and_cash_equivalents, balance-sheet line/asset meanings, receivables/revenue/COGS/purchases meanings, fixed/working-capital meanings, operating/net-income/EBIT/EBT meanings, contribution-margin meanings, DuPont-factor meanings, payout/retention meanings, preferred-dividend/common-share meanings, debt/equity-market-value meanings, invested-capital/NOPAT meanings, insurance meanings, lease meanings, share-count meanings, price/multiple meanings, reporting_period_duration/d and day-count meanings. Full per-record list is in the tool log; every record fails on its first finance meaning. No record reached runtime projection. No action taken beyond the single attempts (per instruction).

## Unresolved / needs-central-decision

1. Figure-image contents (revenue paper Fig 8/9/10; BSEC Annexure C ratios) are topic-verified, not pixel-verified. A human with a PDF viewer could close this in minutes.
2. EDGAR filing figures (7 filings: Prudential, Selective, Valmont, Owens, Precision, Live Oak, Johnson R10) — sec.gov 403s all bot traffic (verified: even a nonexistent Archives URL 403s), so filing numbers are worker-asserted, not reviewer-verified. Formulas all verified via alternate opened sources.
3. Overlap: my b39 accounting-equation vs staged buffy balance-sheet-identity@r1 (c6658d80) — same science; mine better evidenced (OpenStax + CFA vs Wikipedia). Admit exactly one.
4. KPMG/TNOU PDFs are live but text-unextractable with stdlib tooling (custom encoding); formulas verified via alternate opened sources.
5. needs-revision r2s (17 records, mostly URL re-cites + 1-2 oracle-provenance fixes) await curator batches; b49-comprehensive-EPS needs a live source for a non-standard measure.

## Surprises

1. b01–b03 are invalid (CFA PDF cited as `primary` with null URL, against the direct-PDF brief) AND already superseded by b04–b06 r2s — the worker self-corrected the citation pattern mid-stream (r2s change only source kind + source_id).
2. The worker caught the book-1 market-cap collision themselves and withdrew b35's record in the b36 handoff notes.
3. Three same-science duplicates of ELIGIBLE records from other domains (CS straight-line depreciation, econ DOL, econ break-even units) — cross-domain dedup the worker couldn't see.
4. Sibling slices already staged newer r2/r3/r4 of 21 of my records (same worker iterating: IAS 12 URL 2021→2022→AASB mirror across r1→r4).
5. Five dead/migrated citation URLs (BSEC, Runsten, Winkler, Columbia, CSUS) vs zero dead OpenStax/CFA/IFRS/CFI links.
6. Reviewer near-misses, caught before verdicts: (a) I initially fetched URLs from memory that 404d and wrongly suspected the worker's links — the worker's actual cited URLs resolve; (b) I transcribed shortened record IDs from memory — the review generator's coverage check caught every one and a remap fixed them; two verdicts (b50 SL, b24 liquidation) were rewritten against true expressions after re-reading. Lesson: never hand-transcribe IDs or URLs; always copy from artifacts.
7. EDGAR bot-blocks everything (see Unresolved 2) — bot reviewers cannot verify filing figures, only formulas.

## Work files

- `ingest-notes/slice-e-work/reviews/`: 47 validated review JSONs (b04–b50).
- `ingest-notes/slice-e-work/refcheck.py`: independent reference/guard checker (310/310, 554/554).
- `ingest-notes/slice-e-work/pdfextract.py`: stdlib PDF text scraper used for source verification.
- `ingest-notes/slice-e-work/verdicts.py` + `gen_reviews.py` + `remap.py`: review construction (with remap history).
- `ingest-notes/slice-e-work/details.txt`: condensed record dump read for review.

Lock incidents: 0. Did not touch: other slices, data/eval, knowledge/, others' notes, .env, git (no branches/commits/stages per brief). pmem write-back left to parent (slice-level report is the deliverable).

## Parent placement note (2026-11-04)
The 47 review JSONs this report locates at ingest-notes/slice-e-work/reviews/ were moved to data/curation/reviews/<batch-id>-review.json (content untouched) with matching <batch-id>-bundle.json copies from from-offline-curation-workers/. Verified 181 review JSONs + 181 bundles, zero missing, before the single ingestion commit.
