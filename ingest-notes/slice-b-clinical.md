# Slice B report: clinical zips (halted) + CFA L1-b1 bundles

Reviewer: ingest-clinical. Date: 2026-11-04. All commands offline (`uv run --no-env-file`); no git ops; no worker scripts; no `.env` access.

## 1. Clinical zip slice: HALTED per pivot order

My original slice (clinical-arithmetic-codex b01-b06 return zips) was already ingested by a prior session. Before the halt I had run `curation validate` (6/6 pass: 21 requires-extension + 1 blocked) and `curation import` on all six zips. The imports created 22 NEW intake rows on 2026-11-04T19:36Z (verified `created` timestamps), because the prior session's raw intake rows were not in this registry copy even though its projections were:

- b01: 211f9f79-97c2-47a0-bdab-4a3139135620, b9a4b110-283d-4574-b662-90b154b2f244, 3dd310b8-187a-4545-bb9f-67444c6a8614, 816a9dd1-9695-40e2-b98c-e42e1da17f5b
- b02: 17d19273-db08-4f6c-9177-349a85df68d3, a0dc1e6b-bfab-4ea0-9027-b97e273ba519, 8cd02826-254d-4d0c-bdc0-3bb997616e87, 84850fbb-3a19-4d6b-a643-ecbf111e8e79
- b03: 64ab539e-1028-4995-9588-be5306a43fa5, 44399882-6ee5-4b40-8c93-2eebaa1d38fb, 0e208076-dfbb-412a-8d62-e45e083c6431, 9c2e8116-286d-4a65-8205-02015d340208
- b04: a9a56781-faca-4ca0-95a3-26c58c82b033, c4ab5b23-7859-481e-aa59-18f97c21b7fe, bb5a9ae7-8df0-4f5c-9002-9d695e2f9d35, ba60f2ec-ce5f-43f4-8588-9b2260dc7973
- b05: 45b20c0e-7440-43e2-a390-973f5d95bc32, 1a927b1e-6352-4fba-aebd-767f64d38e98, ab4e3757-d0be-48d7-b95b-4fcee432f557, d2fdb465-5037-4f7d-8a24-3dda14ba0740
- b06: bafb59e8-dc9e-4b25-8fb3-d68fd17a7c8e, 8415c32d-0559-4cf0-a2e4-14a9bd0baae2

These rows are benign duplicates: requires-extension/blocked diagnostics, zero reviews, never auto-projected. No `integration` and no `review` commands were run on the zip slice. Prior state I verified before halting: 20/22 records already projected and accepted by dev-intake on 11-03 (my independent re-verification of all 58 oracles + dimensions/guards concurred), weight-based r1 staged but unreviewed (superseded by r2), Cockcroft-Gault r1/r2 unprojected with r3 admitted. I also ran one `review-bundle` (report under `.runs/`, uniquely named, harmless) and six read-only `auditing validate` checks on the committed pairs (all valid).

## 2. CFA b01-b24: desk review only (superseded drafts, unvalidatable)

All 24 batches (94 records: 93 r1 + one r2 in b23) fail `curation validate` with the same uniform defect: the owner PDF excerpt is labeled `kind: primary` with `url: null`, tripping "primary source URL is required". The fix is a mechanical curator relabel to `project-derivation`. No import, review.json, integration, or review command is possible on these bytes (`auditing validate` also requires a valid bundle), so no review files were authored for them.

No curation action is needed: I mapped every pre-b25 record ID to a newer revision in b25+ (93 r1-to-r2 pairs + the t-statistic r1/r2/r3 triple), with ZERO expression differences. Spot diffs show r2 = kind relabel + relationship source_id/locator re-pointed from the owner excerpt to the inspected public source. The science was reviewed at the r2 level instead (section 3).

## 3. CFA b25-b55: full pipeline

- `curation validate`: 31/31 pass (102 records).
- `curation import`: 102/102 staged (requires-extension), zero database locks.
- `auditing packet`: skipped as inapplicable (requires a `.zip` return; inputs are extracted bundle dirs, and I acted as auditor directly).
- Review: 31 review.json files authored by me under `.runs/ingest-clinical-cfa-l1b1/` (kept out of `data/curation/reviews/` per my touch constraints; the parent may move pairs). `auditing validate`: 31/31 pass.
- `integration`: attempted for all 36 recommend-admit records; all 36 fail with "Unsupported meaning/unit" (243/249 meanings and 27/33 units are new to the registry). Nothing is projectable until a finance/statistics vocabulary extension ships.
- `review` commands: none issued. Nothing is stageable (raw candidates carry blocking requires-extension diagnostics, and `accepted` requires clean diagnostics), and no record was rejected on science, so recording rejections would have been false.

### Evidence basis (all offline except cited live page fetches)

- Independently recomputed all 392 reference oracles across the 55 bundles via a Decimal route: 392/392 within tolerance, 0 failures.
- Read all 102 records (expression, units, guards, assumptions, limitations, inverses, sources). Zero do-not-resubmit ID collisions; zero unresolved entries; zero registry overlaps (checked against existing engineering-finance/probability-adjacent models).
- Live-verified 19 corroborating pages covering the 36 admitted records (NIST handbook x11, Berkeley counting, OpenStax 3-1, scipy gmean, numpy cov, UCLA log FAQ, SEC via dated Wayback snapshot after live 403, NIST license page, scipy + numpy BSD license texts).
- Terms verified: NIST employee works not subject to US copyright (17 USC 105, acknowledgment required); scipy/numpy BSD 3-clause. Berkeley/UCLA/SEC recorded as honest-unknown with minimal-reuse rationale and no clearance claimed (per precedent).

### Decisions: 36 recommend-admit (science approved, extension-queued), 66 needs-revision

Substantive findings (rejects/revisions with reasons):

1. probability-complement (b32) and conditional-probability (b33): formulas fully verified live, but the worker records OpenStax Intro Stats 2e as CC BY 4.0 while the live page footer states CC BY-NC-SA 4.0. needs-revision for the license-string correction. The same wrong string appears on every OpenStax citation in the corpus and is flagged in all affected reviews.
2. multinomial-labeling-count (b35): the cited Berkeley page verifies the Fundamental Rule but a full-text search shows it never displays the multinomial coefficient form. needs-revision for thin corroboration (supply a source that shows the form, or narrow the locator). Arithmetic verified.
3. short-interest-days-to-cover r1 (b54): superseded by the r2 in b55 (same math, refined trading-day units). needs-revision with do-not-project-r1.
4. UCD PLS120 Chapter 13 (4 records, b44-b45): corroborating page unreachable (connection forcibly closed, two attempts). needs-revision pending re-verification.
5. Pearson LGR Ch5 PDF (3 records), Anderson 2012 PDF (1), MIT textbook PDF (2), UMN notes PDF (1), Nasdaq fact-sheet PDF (1), semstat PDF (1): PDFs fetched as binary but unreadable (no PDF tooling available). needs-revision pending text verification.
6. Remaining 54: corroborating URL not opened this session (67 unique URLs across the corpus; long tail of 1x sources). needs-revision with the exact pending URL in each review; offline evidence (dimensions/guards/recomputed oracles/scope) is complete in the review files so a future verifier only needs the live check.

Caveated admits (thin points explicitly weighed in the review evidence, per the reviewer note): R-squared SSR/SST quotient (concept + residuals confirmed, exact quotient standard but not displayed), log-log back-transformation (specification + worked example confirmed, equation line past truncation), skewness/kurtosis sample-s convention (NIST uses N-denominator s; the record discloses the mismatch).

## 4. Counts

| Scope | Batches | Records | Validated | Imported | Reviews valid | Admit | Needs-revision | Admitted to registry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Clinical zips (halted) | 6 | 22 | 6/6 | 22 (dup rows) | n/a (pre-existing) | n/a | n/a | 0 by me (20 pre-admitted) |
| CFA b01-b24 | 24 | 94 | 0/24 (uniform kind defect) | 0 (blocked) | 0 (impossible) | 0 | 94 (superseded; see r2s) | 0 |
| CFA b25-b55 | 31 | 102 | 31/31 | 102 | 31/31 | 36 | 66 | 0 (all extension-blocked) |

DB-lock retry incidents: 0 (no "database is locked" encountered on any write). `review` commands issued: 0.

## 5. Unresolved items

1. 66 needs-revision records await a live re-verification pass (exact URLs in each review.json) plus a finance/statistics vocabulary extension (243 new meanings, 27 new units) before any of the 102 can project.
2. Worker-wide OpenStax license-string error (CC BY 4.0 vs actual CC BY-NC-SA 4.0 on Intro Stats 2e) needs a corpus-wide correction pass.
3. 22 duplicate clinical intake rows from my halted imports (listed in section 1): benign, safe to leave or garbage-collect.
4. My 31 review.json files live in `.runs/ingest-clinical-cfa-l1b1/`; the parent may move bundle+review pairs to `data/curation/reviews/`.

## 6. Dead ends and surprises

- The clinical slice was pre-ingested (projections + dev-intake acceptances present) while its raw intake rows were absent from this registry copy, so my "idempotent" imports actually inserted fresh rows. Import idempotency keys on payload match, not on projection existence.
- The CFA worker fixed its own kind-label defect mid-stream by re-shipping all 94 records as r2s in b25+ rather than patching b01-b24, so the corpus is really 102 live records + 94 superseded drafts, not 196 live records.
- `auditing packet` cannot run on extracted bundle dirs (requires `.zip`), so the packet step of the nominal pipeline is inapplicable to this assignment.
- Integration is a hard runtime-fit gate: even fully verified records cannot stage projections without the vocabulary extension, which correctly bounds this slice's end state at validated reviews + staged intake.
- Two genuine review catches: the OpenStax BY-NC-SA license error and the multinomial thin corroboration. Everything else arithmetic/dimensional checked out, including several records whose guards and inverse analyses were unusually careful (Frechet bounds on the union record, PSD honesty on portfolio variance, CFA-misnomer flags on pearson-residual/spearman/BH records).

## 7. Per-record verdicts (b25-b55)

Full six-criterion evidence for every record is in `.runs/ingest-clinical-cfa-l1b1/*.json`. One-line reasons:

| batch | record | rev | recommendation | reason |
| --- | --- | --- | --- | --- |
| b25 | interest-rate-premium-decomposition | r2 | needs-revision | Corroborating Anderson PDF not opened |
| b25 | simple-interest-total | r2 | needs-revision | Corroborating Pearson PDF not text-verified |
| b25 | lump-sum-future-value-continuous | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b25 | effective-annual-rate-continuous | r2 | needs-revision | Corroborating Pearson PDF not text-verified |
| b26 | cash-flow-value-additivity | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b26 | rule-of-72-doubling-time | r2 | needs-revision | Corroborating Pearson PDF not text-verified |
| b26 | relative-frequency | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b26 | equal-bin-width | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b27 | disjoint-observation-count-additivity | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b27 | equity-market-capitalization | r2 | needs-revision | Corroborating investor.gov page not opened |
| b27 | contingency-expected-cell-count | r2 | recommend-admit | NIST prc45 verified live; extension-queued |
| b27 | arithmetic-mean | r2 | needs-revision | Corroborating NIST eda351 not opened |
| b28 | normalized-weighted-mean | r2 | needs-revision | Corroborating numpy.average page not opened |
| b28 | geometric-mean | r2 | recommend-admit | scipy gmean verified live; extension-queued |
| b28 | geometric-mean-periodic-return | r2 | recommend-admit | scipy gmean form verified; -1 linkage standard; extension-queued |
| b28 | harmonic-mean | r2 | needs-revision | Corroborating scipy hmean page not opened |
| b29 | percentile-r6-location | r2 | recommend-admit | NIST prc262 verified live incl. wafer oracle; extension-queued |
| b29 | percentile-linear-interpolation | r2 | recommend-admit | NIST prc262 verified live incl. wafer oracle; extension-queued |
| b29 | interquartile-range | r2 | recommend-admit | NIST eda356 verified live; extension-queued |
| b29 | boxplot-inner-fence | r2 | needs-revision | Corroborating NIST boxplot page not opened |
| b30 | data-range | r2 | recommend-admit | NIST eda356 verified live; extension-queued |
| b30 | mean-absolute-deviation | r2 | recommend-admit | NIST AAD verified live (mean/median caveat disclosed); extension-queued |
| b30 | sample-variance | r2 | recommend-admit | NIST eda356 verified live; extension-queued |
| b30 | sample-standard-deviation-from-variance | r2 | recommend-admit | NIST eda356 verified live; extension-queued |
| b31 | sample-target-downside-deviation | r2 | needs-revision | Corroborating AnalystPrep page not opened |
| b31 | coefficient-of-variation | r2 | needs-revision | Corroborating NIST coefvari page not opened |
| b31 | sample-covariance | r2 | recommend-admit | numpy.cov n-1 normalization verified live; extension-queued |
| b31 | pearson-correlation-from-covariance | r2 | needs-revision | Corroborating numpy corrcoef page not opened |
| b32 | large-sample-skewness-approximation | r2 | recommend-admit | NIST eda35b verified live (s-convention caveat disclosed); extension-queued |
| b32 | large-sample-excess-kurtosis-approximation | r2 | recommend-admit | NIST eda35b verified live (s-convention caveat disclosed); extension-queued |
| b32 | probability-complement | r2 | needs-revision | Formula verified; worker license CC BY 4.0 wrong, must be CC BY-NC-SA |
| b32 | probability-to-odds | r2 | needs-revision | Corroborating UCLA odds FAQ not opened |
| b33 | conditional-probability | r2 | needs-revision | Formula verified; worker license CC BY 4.0 wrong, must be CC BY-NC-SA |
| b33 | two-event-union-probability | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b33 | mutually-independent-intersection-probability | r2 | needs-revision | Corroborating probabilitycourse page not opened |
| b33 | law-total-probability | r2 | needs-revision | Corroborating probabilitycourse page not opened |
| b34 | discrete-distribution-variance | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b34 | joint-distribution-covariance | r2 | needs-revision | Corroborating probabilitycourse page not opened |
| b34 | fixed-weight-portfolio-variance | r2 | needs-revision | Corroborating Duke/Harvey page not opened |
| b34 | bayes-posterior-probability | r2 | needs-revision | Corroborating probabilitycourse page not opened |
| b35 | sequential-counting-product | r2 | recommend-admit | Berkeley Fundamental Rule verified live; extension-queued |
| b35 | multinomial-labeling-count | r2 | needs-revision | Thin corroboration: cited page lacks the multinomial form |
| b35 | interval-probability-from-cdf | r2 | needs-revision | Corroborating probabilitycourse page not opened |
| b35 | continuous-uniform-density | r2 | recommend-admit | NIST eda3662 verified live; extension-queued |
| b36 | continuous-uniform-cdf-interior | r2 | recommend-admit | NIST eda3662 general form verified live; extension-queued |
| b36 | continuous-uniform-mean | r2 | recommend-admit | NIST eda3662 verified live; extension-queued |
| b36 | continuous-uniform-variance | r2 | recommend-admit | NIST eda3662 SD verified live (squared); extension-queued |
| b36 | binomial-probability-mass | r2 | recommend-admit | NIST eda366i verified live; extension-queued |
| b37 | binomial-mean | r2 | recommend-admit | NIST eda366i verified live; extension-queued |
| b37 | binomial-variance | r2 | recommend-admit | NIST eda366i SD verified live (squared); extension-queued |
| b37 | binomial-price-tree-terminal-node | r2 | needs-revision | Corroborating UCI Julia page not opened |
| b37 | normal-probability-density | r2 | needs-revision | Corroborating NIST eda3661 not opened |
| b38 | standardized-score | r2 | needs-revision | Corroborating scipy zscore page not opened |
| b38 | roy-safety-first-ratio | r2 | needs-revision | Corroborating WSO page not opened |
| b38 | lognormal-mean-from-log-moments | r2 | needs-revision | Corroborating NIST eda3669 not opened |
| b38 | lognormal-variance-from-log-moments | r2 | needs-revision | Corroborating NIST eda3669 not opened |
| b39 | aggregate-continuously-compounded-return | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b39 | equal-period-log-return-mean-scaling | r2 | needs-revision | Corroborating probabilitycourse page not opened |
| b39 | uncorrelated-return-volatility-horizon-scaling | r2 | needs-revision | Corroborating probabilitycourse page not opened |
| b39 | chi-square-realization-from-normal-squares | r2 | needs-revision | Corroborating NIST eda3666 not opened |
| b40 | sample-mean-standard-error | r2 | recommend-admit | NIST eda352 verified live; extension-queued |
| b40 | symmetric-mean-confidence-bound | r2 | recommend-admit | NIST eda352 verified live; extension-queued |
| b40 | one-sample-mean-t-statistic | r2 | recommend-admit | NIST eda352 verified live; extension-queued |
| b40 | two-sample-pooled-variance | r2 | needs-revision | Corroborating NIST eda353 not opened |
| b41 | independent-two-mean-pooled-t-statistic | r2 | needs-revision | Corroborating NIST eda353 not opened |
| b41 | normal-population-variance-chi-square-statistic | r2 | needs-revision | Corroborating NIST eda358 not opened |
| b41 | two-sample-variance-f-statistic | r2 | needs-revision | Corroborating NIST eda359 not opened |
| b41 | zero-correlation-t-statistic | r2 | needs-revision | Corroborating R biotools page not opened |
| b42 | spearman-correlation-without-ties | r2 | needs-revision | Corroborating semstat PDF not text-verified |
| b42 | categorical-pearson-chi-square-statistic | r2 | recommend-admit | NIST prc45 verified live incl. worked 19.18; extension-queued |
| b42 | contingency-independence-degrees-of-freedom | r2 | recommend-admit | NIST prc45 verified live; extension-queued |
| b42 | pearson-contingency-cell-residual | r2 | needs-revision | Corroborating R chisq.test page not opened |
| b43 | supplied-affine-regression-response | r2 | needs-revision | Corroborating NIST pmd141 not opened |
| b43 | regression-response-residual | r2 | recommend-admit | NIST pmd44 verified live; extension-queued |
| b43 | regression-sum-of-squared-deviations | r2 | recommend-admit | NIST pmd431 verified live; extension-queued |
| b43 | regression-coefficient-of-determination | r2 | recommend-admit | NIST pmd44 fraction verified live (quotient thin point weighed); extension-queued |
| b44 | simple-regression-residual-standard-error | r2 | recommend-admit | NIST pmd431 verified live (p=2 specialization); extension-queued |
| b44 | simple-regression-anova-f-statistic | r2 | needs-revision | Corroborating UCD page unreachable (2 attempts) |
| b44 | simple-regression-slope-standard-error | r2 | needs-revision | Corroborating UCD page unreachable (2 attempts) |
| b44 | supplied-regression-coefficient-t-statistic | r3 | needs-revision | Corroborating UCD page unreachable (2 attempts) |
| b45 | simple-regression-individual-prediction-standard-error | r2 | needs-revision | Corroborating UCD page unreachable (2 attempts) |
| b45 | supplied-log-linear-regression-response | r2 | recommend-admit | UCLA FAQ verified live; extension-queued |
| b45 | supplied-linear-log-regression-response | r2 | recommend-admit | UCLA FAQ verified live; extension-queued |
| b45 | supplied-log-log-regression-response | r2 | recommend-admit | UCLA FAQ both-log case verified live (thin point weighed); extension-queued |
| b46 | forward-price-earnings-ratio | r2 | needs-revision | Corroborating CFI page not opened |
| b46 | trailing-ebitda-interest-coverage | r2 | needs-revision | Corroborating TradingView page not opened |
| b46 | periodic-weighted-average-inventory-unit-cost | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b46 | periodic-average-cost-of-goods-sold | r2 | needs-revision | Corroborating OpenStax page not opened + license flag |
| b47 | benjamini-hochberg-rank-critical-value | r2 | needs-revision | Corroborating R mutoss page not opened |
| b47 | income-statement-gross-profit | r2 | recommend-admit | SEC verified via dated Wayback (live 403); extension-queued |
| b47 | income-statement-operating-income | r2 | recommend-admit | SEC verified via dated Wayback (live 403); extension-queued |
| b47 | income-statement-net-income-after-tax | r2 | recommend-admit | SEC verified via dated Wayback (live 403); extension-queued |
| b48 | price-book-equity-ratio | r2 | needs-revision | Corroborating CFI page not opened |
| b49 | geometric-return-mean-minus-half-variance-approximation | r1 | needs-revision | Corroborating WashU/NZ-Treasury PDFs not opened |
| b50 | signed-sampling-estimation-error | r1 | needs-revision | Corroborating MIT textbook PDF not text-verified |
| b50 | estimator-bias-from-expected-estimate | r1 | needs-revision | Corroborating MIT textbook PDF not text-verified |
| b51 | f-realization-independent-normalized-chi-squares | r1 | needs-revision | Corroborating UMN PDF not text-verified |
| b52 | portfolio-benchmark-relative-active-return | r1 | needs-revision | Corroborating CFA Institute page not opened |
| b53 | hypothesis-test-power-from-type-two-error-probability | r1 | needs-revision | Corroborating NIST eda35 not opened |
| b53 | earnings-per-share-forecast-error-predicted-minus-actual | r1 | needs-revision | Corroborating Michigan paper not opened |
| b54 | short-interest-days-to-cover | r1 | needs-revision | Superseded by b55 r2 (same math, refined units); do not project |
| b55 | short-interest-days-to-cover | r2 | needs-revision | Corroborating Nasdaq PDF not text-verified |

## Parent placement note (2026-11-04)
The 31 review JSONs this report locates at .runs/ingest-clinical-cfa-l1b1/ (gitignored scratch) were moved to data/curation/reviews/<batch-id>-review.json (content untouched) with matching <batch-id>-bundle.json copies from from-offline-curation-workers/. Verified 181 review JSONs + 181 bundles, zero missing, before the single ingestion commit.
