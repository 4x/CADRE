# CFA 2023 Level I Volume 1 — curation session report

## Historical report notice

This report documents the original draft session and its then-current source-policy conflict. The conflict has since been resolved: [the corrected-return index](PRIOR-VOLUMES-CORRECTIONS.md) lists the officially validated Volume 1 returns b25–b48. The claims below that no official returns exist and that the PDF must be a primary source are historical, not current instructions. Volume 1 extraction remains incomplete.

Saved 93 distinct models as 94 revisions in 24 data-only draft ZIPs. The session is a partial extraction; exhaustive coverage of every equation has not been certified.

Assigned source: sources/2023-L1V1.pdf — 512 PDF pages. SHA-256: `1f5a5394ed38422c005b7def5683ab6e7c80d467360e092897e141641c4cb7d5`. The PDF remains in sources and its hash is unchanged.

## Read the results

- [Formula index](FORMULA-INDEX.md) — compact source formulas, evaluator expressions and locators.
- [CSV index](formula-index.csv) — one row per latest distinct model.
- [Model details](MODEL-DETAILS.md) — symbol definitions, units, assumptions and limitations.
- [Deferred and source-review register](DEFERRED.md) — exact overlaps, missing operators, apparent source errors and historical resolutions.
- [Machine audit](../research/audit-results.json), [active revision inventory](../research/active-models.json), [session](../SESSION.json), [source manifest](../source-manifest.json).

## Validation and packaging

Limited schema, expression arithmetic, guard/rejection and archive-integrity checks passed: 188 numerical reference cases and 95 rejection cases across all revisions. Every draft ZIP exactly matches its bundle and has only bundle.json and manifest.json; checksums were verified. The audit also invokes the unchanged official validator for every ZIP.

Official validation fails for every batch: `primary source URL is required`. cfa-source-brief.md explicitly requires the purchased CFA PDF to be primary with `url: null`; toolkit version 2026-10-31.9 rejects that citation. Sources and toolkit were left unchanged. Zero officially validated return ZIPs were produced. Draft ZIP names deliberately end in `-draft.zip`, not `-return.zip`.

The separate checker is limited: it does not establish scientific correctness, dimensional/context fidelity, valid elementwise family bindings, inverse validity, global uniqueness or runtime integration. Most finance/statistics quantities require registry extension. Official pack is blocked by the same validation prerequisite.

## Coverage

All seven learning modules were reached in source order, then earlier gaps and embedded examples were revisited. Detailed inspection and formula-neighborhood triage are recorded separately in SESSION.json. Practice/solution pages and some earlier partial outputs still need a complete detailed sweep. A custom standard-library reader decoded the local PDF in place because no PDF library/CLI was installed and package download failed. Some diagrams and lookup-table glyphs remain garbled; visual fidelity has not been certified.

Included areas: continuous interest and value additivity; data organization; means, percentiles and dispersion; covariance/correlation; event probabilities, Bayes and counting; uniform/binomial/normal/lognormal distributions; log-return aggregation; sampling and mean inference; variance, correlation and contingency tests; supplied regression functions and diagnostics; transformed regression forms; embedded financial-statement ratios and inventory arithmetic.

Previously covered TVM families were recorded as overlaps. Raw coefficient estimation, inverse-CDF/normal-tail calculations, random generation, sorting/filtering and iterative solutions were deferred under assignment boundaries. Algebraic inverses and repeated special cases are retained in notes rather than counted as new models.

## Material source issues

The review register flags the incorrect general arithmetic-mean × harmonic-mean identity; inconsistent weighted-mean arithmetic and covariance values; an odds-against arithmetic error; missing joint-normal/independence qualifications; Monte Carlo diffusion time scaling; tied-rank Spearman misuse; variance-unit notation; BH critical-value terminology; regression fitted-value notation; and the omitted residual scale in the intercept standard error. These are curator findings with locators, not a claim to have checked the publisher errata. No erroneous example was used to relax a numerical tolerance.

## Draft archives

Each ZIP link below is part of this handoff. b23 contains one correction only; use r2 for the regression coefficient t-statistic and keep the earlier r1 archive as history.

| Batch | Revisions | Draft ZIP | JSON bundle |
|---|---:|---|---|
| financial-analysis-cfa-l1-b1-b01 | 4 | [Download](financial-analysis-cfa-l1-b1-b01-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b01/bundle.json) |
| financial-analysis-cfa-l1-b1-b02 | 4 | [Download](financial-analysis-cfa-l1-b1-b02-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b02/bundle.json) |
| financial-analysis-cfa-l1-b1-b03 | 4 | [Download](financial-analysis-cfa-l1-b1-b03-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b03/bundle.json) |
| financial-analysis-cfa-l1-b1-b04 | 4 | [Download](financial-analysis-cfa-l1-b1-b04-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b04/bundle.json) |
| financial-analysis-cfa-l1-b1-b05 | 5 | [Download](financial-analysis-cfa-l1-b1-b05-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b05/bundle.json) |
| financial-analysis-cfa-l1-b1-b06 | 5 | [Download](financial-analysis-cfa-l1-b1-b06-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b06/bundle.json) |
| financial-analysis-cfa-l1-b1-b07 | 4 | [Download](financial-analysis-cfa-l1-b1-b07-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b07/bundle.json) |
| financial-analysis-cfa-l1-b1-b08 | 4 | [Download](financial-analysis-cfa-l1-b1-b08-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b08/bundle.json) |
| financial-analysis-cfa-l1-b1-b09 | 5 | [Download](financial-analysis-cfa-l1-b1-b09-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b09/bundle.json) |
| financial-analysis-cfa-l1-b1-b10 | 3 | [Download](financial-analysis-cfa-l1-b1-b10-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b10/bundle.json) |
| financial-analysis-cfa-l1-b1-b11 | 5 | [Download](financial-analysis-cfa-l1-b1-b11-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b11/bundle.json) |
| financial-analysis-cfa-l1-b1-b12 | 4 | [Download](financial-analysis-cfa-l1-b1-b12-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b12/bundle.json) |
| financial-analysis-cfa-l1-b1-b13 | 5 | [Download](financial-analysis-cfa-l1-b1-b13-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b13/bundle.json) |
| financial-analysis-cfa-l1-b1-b14 | 4 | [Download](financial-analysis-cfa-l1-b1-b14-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b14/bundle.json) |
| financial-analysis-cfa-l1-b1-b15 | 3 | [Download](financial-analysis-cfa-l1-b1-b15-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b15/bundle.json) |
| financial-analysis-cfa-l1-b1-b16 | 4 | [Download](financial-analysis-cfa-l1-b1-b16-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b16/bundle.json) |
| financial-analysis-cfa-l1-b1-b17 | 5 | [Download](financial-analysis-cfa-l1-b1-b17-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b17/bundle.json) |
| financial-analysis-cfa-l1-b1-b18 | 5 | [Download](financial-analysis-cfa-l1-b1-b18-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b18/bundle.json) |
| financial-analysis-cfa-l1-b1-b19 | 4 | [Download](financial-analysis-cfa-l1-b1-b19-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b19/bundle.json) |
| financial-analysis-cfa-l1-b1-b20 | 3 | [Download](financial-analysis-cfa-l1-b1-b20-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b20/bundle.json) |
| financial-analysis-cfa-l1-b1-b21 | 4 | [Download](financial-analysis-cfa-l1-b1-b21-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b21/bundle.json) |
| financial-analysis-cfa-l1-b1-b22 | 4 | [Download](financial-analysis-cfa-l1-b1-b22-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b22/bundle.json) |
| financial-analysis-cfa-l1-b1-b23 | 1 | [Download](financial-analysis-cfa-l1-b1-b23-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b23/bundle.json) |
| financial-analysis-cfa-l1-b1-b24 | 1 | [Download](financial-analysis-cfa-l1-b1-b24-draft.zip) | [Bundle](financial-analysis-cfa-l1-b1-b24/bundle.json) |

## Next priorities

The exact queued sections and at least ten candidate follow-ups are in SESSION.json. First resolve the validator/source-policy conflict, then finish the detailed practice/solution sweep and unresolved source layouts. Review source corrections, general F construction, sampling error/bias, geometric/arithmetic return approximation and context-safe prediction endpoints. Recheck quantity semantics and deduplication before proposing runtime integration.

No Git repository is present in the workspace, so a feature branch and commit could not be created. The portable toolkit, source PDF and external systems were not changed. All work products are under kit.

## Measured session

Started: 2026-11-03T22:12:22.5257516Z. Latest checkpoint: 2026-11-03T23:32:13.043796+00:00. Measured useful work: 60.02 minutes. Required source inspection, ordinary tool calls and artifact verification are included; 19.82 minutes of unexpected final-tool delay are explicitly excluded. No deliberate waiting is counted. Session status: session-complete-partial-extraction. This status refers to the bounded research session, not completion of the entire extraction.
