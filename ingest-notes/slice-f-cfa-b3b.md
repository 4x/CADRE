# Slice F — CFA financial-analysis b51–b99, b100–b101 (ingest-cfa-b3b)

Reviewer: `ingest-cfa-b3b`. Date: 2026-11-04. Curator: `codex-cfa-l1v3` (never impersonated; reviewer identity is distinct in all 51 reviews).

## Outcome

- 51/51 bundles validated, staged, packeted, and review-validated. Zero financial-analysis pairs existed in `data/curation/reviews/` before; this slice adds 51 bundle + 51 review files.
- 94 records: **88 recommend-admit, 6 needs-revision, 0 blocked**.
- **All 88 recommend-admit records are blocked-on-vocab-extension**: one clean `integration` attempt each, all 88 refused with `Unsupported meaning/unit`, zero for any other reason. No projections exist, so no `connected-models review` decisions were possible (verified: `review` on a research candidate fails pre-write with `Invalid object fields`, since research candidates carry `model=None`). The validated review JSONs are the decision record.
- Registry lock incidents: **0** across 51 imports + 88 integration attempts + probes.
- 45 unique public source URLs dispositioned; 12+ published oracles matched verbatim/figure-exact.

## Pipeline ledger

| Step | Result |
|---|---|
| `curation validate` | 51/51 pass |
| `curation import` | 51/51 staged (94 research candidates, UUIDs in temp mechanical.log) |
| `curation pack` + `auditing packet` | 51/51 (temp only; packets are transient handoff artifacts) |
| `auditing validate` | 51/51 pass (after fixing my own `checks` array→object shape error) |
| `integration` (one attempt per recommend-admit) | 0 staged / 88 refused, all `Unsupported meaning/unit` |
| `connected-models review` | not applicable: no projection candidates exist |

## Per-record decisions

`A` = recommend-admit, `NR` = needs-revision. "Sup." = superseded in-slice (integrate successor only).

| Batch | Record | Rev | Dec | Rationale |
|---|---|---|---|---|
| b51 | fixed-coupon-bond-price-flat-periodic-yield | r1 | A | Sound; par oracle anchored (50 = .05×1000); discount case hand-recomputed. Sup. by b52 r2 (identical). |
| b52 | fixed-coupon-bond-price-flat-periodic-yield | r2 | A | Latest; byte-identical to r1. Integrate this. |
| b53 | project-npv-including-real-option | r1 | A | Matches Wiley verbatim; no-double-count fenced; guards cost/value ≥ 0. |
| b53 | unanticipated-project-npv-per-share | r1 | A | PUBLISHED ORACLE: Wiley £250m/200m = £1.25 verbatim; shares > 0. |
| b54 | combined-corporate-dividend-tax-rate | r1 | A | ABA (1-c)(1-d) verbatim; 0.5205 recomputed; rates in [0,1]. |
| b54 | distributed-profit-after-corporate-and-dividend-tax | r1 | A | ABA form; 838×0.685×0.7 = 401.821 recomputed; hypothetical rates fenced. |
| b55 | lessee-finance-lease-liability-rollforward | r2 | A | ASC 842-20-35-1(a) verbatim; no-overpayment guard; strengths sibling b44 r1 (cross-slice). |
| b56 | common-size-cash-flow-by-directional-total | r1 | A | AnalystPrep directional-total passage verbatim; line ∈ [0,total]. |
| b56 | common-size-cash-flow-line-to-net-revenue | r1 | A | AnalystPrep net-revenue passage verbatim; signed line correctly admitted. |
| b57 | liquidation-net-proceeds-proportional-cost | r1 | A | Pliant Note K corroborated; cost ∈ [0,1]. Sup. by b67 r2 (access-date). |
| b58 | free-cash-flow-equity-from-net-income | r1 | A | CFA Summary equation verbatim; signed conventions covered both refs. |
| b58 | free-cash-flow-equity-from-firm-cash-flow | r1 | A | CFA Summary equation verbatim; after-tax legs verified (15, 7). |
| b59 | credit-sales-receivables-turnover | r1 | A | PUBLISHED ORACLE: OpenStax 400,000/80,000 = 5 verbatim. Sup. by b67 r2 (access-date). |
| b60 | defined-benefit-plan-deficit | r3 | A | Cameco policy sentence verbatim; surplus sign covered. Sup. by b65 r4 (access-date). |
| b61 | asset-taxable-temporary-difference-deferred-liability | r3 | A | IAS 12 example form; carrying ≥ taxbase. Sup. by b64 r4 (access-date). |
| b61 | asset-deductible-temporary-difference-deferred-asset | r3 | A | Sound; taxbase ≥ carrying. Sup. by b64 r4 (access-date). |
| b61 | liability-deductible-temporary-difference-deferred-asset | r3 | A | PUBLISHED-FORM: IAS 12 para 25 (100,0,.25 → 25). Sup. by b64 r4. |
| b61 | liability-taxable-temporary-difference-deferred-liability | r3 | A | Sound; taxbase ≥ carrying. Sup. by b64 r4 (access-date). |
| b62 | income-tax-expense-current-and-deferred | r3 | A | AASB 112 paras 58–60 form; correctly guard-free. Sup. by b65 r4 (access-date). |
| b62 | deferred-tax-liability-rate-change-effect | r3 | A | Fixed-difference mechanics; both rate directions. Sup. by b65 r4 (access-date). |
| b62 | debt-extinguishment-gain | r2 | A | AASB 9 para 3.3.3 verbatim; gain+loss signs. Sup. by b65 r3 (access-date). |
| b62 | specific-borrowing-cost-capitalization-ifrs | r2 | A | AASB 123 paras 12–13 verbatim; costs ≥ income. Sup. by b66 r3 (access-date). |
| b63 | depreciable-asset-tax-base-from-cost-and-deductions | r2 | A | PUBLISHED-FORM: IAS 12 para 7 ex 1 (100−30 = 70). Sup. by b66 r3 (access-date). |
| b63 | liability-tax-base-from-future-deduction | r2 | A | PUBLISHED-FORM: IAS 12 para 8 ex 1 (100−100 = 0). Sup. by b66 r3. |
| b63 | deferred-revenue-liability-tax-base | r2 | A | IAS 12 para 8 ex 2 pattern. Sup. by b66 r3 (access-date). |
| b64 | asset-taxable-temporary-difference-deferred-liability | r4 | A | Latest; diffed: access-date fix only. |
| b64 | asset-deductible-temporary-difference-deferred-asset | r4 | A | Latest; diffed: access-date fix only. |
| b64 | liability-deductible-temporary-difference-deferred-asset | r4 | A | Latest; diffed: access-date fix only. |
| b64 | liability-taxable-temporary-difference-deferred-liability | r4 | A | Latest; diffed: access-date fix only. |
| b65 | income-tax-expense-current-and-deferred | r4 | A | Latest; diffed: access-date fix only. |
| b65 | deferred-tax-liability-rate-change-effect | r4 | A | Latest; diffed: access-date fix only. |
| b65 | debt-extinguishment-gain | r3 | A | Latest; diffed: access-date fix only. |
| b65 | defined-benefit-plan-deficit | r4 | A | Latest; diffed: access-date fix only. |
| b66 | specific-borrowing-cost-capitalization-ifrs | r3 | A | Latest; diffed: access-date fix only. |
| b66 | depreciable-asset-tax-base-from-cost-and-deductions | r3 | A | Latest; diffed: access-date fix only. |
| b66 | liability-tax-base-from-future-deduction | r3 | A | Latest; diffed: access-date fix only. |
| b66 | deferred-revenue-liability-tax-base | r3 | A | Latest; diffed: access-date fix only. |
| b67 | liquidation-net-proceeds-proportional-cost | r2 | A | Latest; diffed: access-date fix only. |
| b67 | credit-sales-receivables-turnover | r2 | A | Latest; diffed: access-date fix only. |
| b68 | forgone-trade-discount-periodic-cost | r1 | A | 2/98 = 0.02040816327 recomputed; discount ∈ [0,1) excludes singularity. Winkler URL redirects; corroborated via AccountingTools (identical formula). |
| b68 | accumulated-depreciation-removed-on-disposal | r1 | A | AnalystPrep reconciliation verbatim; nonnegative-removal guard. |
| b69 | cash-paid-operating-expenses-prepaid-and-accrued | r1 | A | Coherent refund-admitting profile; AnalystPrep verbatim. Sup. by b70 r2 (positive-payment narrowing). |
| b70 | cash-paid-operating-expenses-prepaid-and-accrued | r2 | A | Latest; adds paid ≥ 0 guard + refund limit. |
| b71 | equipment-gross-cost-removed-on-disposal | r1 | A | PUBLISHED ORACLE: page's Pinehaven 100k+55k−135k = 20k reproduced. |
| b72 | contract-cost-to-cost-progress | r1 | A | IFRS SME Module 23 corroborated; incurred ∈ [0,expected]. |
| b72 | contract-cumulative-over-time-revenue | r1 | A | Transaction-price × progress; progress ∈ [0,1]. |
| b72 | contract-revenue-cumulative-catch-up | r1 | A | Catch-up mechanics; source rounding (51.2%) disclosed; both signs. |
| b73 | declining-balance-book-value-uncapped | r1 | A | 600000×(2/3)⁴ = 118518.518… exact; rate ∈ [0,1). Oxford URL 404; corroborated via Pearson (identical relationship). |
| b74 | altman-original-manufacturing-z-score | r1 | A | Altman Table 1 weights verbatim incl. 1.0 sales; 2.995 leg-by-leg. Sup. by b80 r2 (constants). |
| b75 | credit-rating-funds-from-operations | r1 | A | S&P criteria verbatim FFO definition. |
| b75 | credit-rating-funds-from-operations-to-debt | r1 | A | S&P FFO/debt; debt > 0; negative coverage covered. |
| b75 | credit-rating-free-operating-cash-flow | r1 | A | S&P para 260 verbatim; capex ≥ 0 magnitude. |
| b75 | credit-rating-free-operating-cash-flow-to-debt | r1 | A | S&P FOCF/debt; debt > 0. |
| b76 | credit-rating-capital-including-deferred-taxes | r1 | A | S&P para 248 verbatim. |
| b76 | credit-rating-return-on-average-capital | r1 | A | S&P EBIT/avg-capital verbatim; beginning+ending > 0. |
| b77 | hotel-room-occupancy-rate | r1 | A | Sunstone quotient definitions verbatim; sold ∈ [0,available]. |
| b77 | hotel-average-daily-room-rate | r1 | A | Sunstone ADR verbatim; sold > 0; not-RevPAR fenced. |
| b77 | bank-net-interest-margin-average-earning-assets | r1 | A | Bank exhibit verbatim; average-denominator choice disclosed. |
| b78 | retail-sales-per-square-foot | r1 | A | PUBLISHED ORACLE: Nordstrom $8,258m/22.414m sq ft = $368. |
| b78 | bank-central-reserves-to-eligible-deposits | r1 | A | BoK ratio form; observed-ratio (not compliance) fenced. |
| b78 | service-revenue-per-employee | r1 | A | MBDA revenue/employees verbatim; employees > 0. |
| b78 | service-net-income-per-employee | r1 | A | PUBLISHED ORACLE: GoCardless 25-people/$600k example = 24,000; FTE variant fenced. |
| b79 | bank-approved-liquid-securities-to-specified-deposits | r1 | A | Ratio form corroborated via Kotak SLR page (RBI old host DNS-dead); narrower-than-statutory fenced. |
| b79 | same-store-sales-growth-aggregate | r1 | A | Domino's comparable-weeks definition verbatim; both signs. |
| b80 | altman-original-manufacturing-z-score | r2 | A | Latest; adds 5 sourced constants. |
| b81 | inventory-turnover-linear-annualization | r1 | NR | Definitions claim day counts while quarter ref uses months (12/3); quantity_ids carry wrong unit. Fixed by r2 (b82). |
| b82 | inventory-turnover-linear-annualization | r2 | A | Latest; lengths unit-free; Sanmina ×4 corroborated. |
| b83 | company-sales-from-industry-sales-and-market-share | r1 | A | Vskills market-share passage verbatim; share ∈ [0,1]. |
| b83 | noncash-working-capital-proportional-to-sales | r1 | A | PUBLISHED ORACLE: UOU 10% × 5,000,000 = 500,000 verbatim; general-vs-noncash split disclosed. |
| b84 | asset-base-accumulated-depreciation-fraction | r1 | A | Fitch verbatim; depreciation ≥ 0, gross > 0. |
| b84 | asset-base-renewal-capex-share | r1 | A | Fitch verbatim; gross+capex > 0 excludes 0/0. |
| b84 | market-value-to-tangible-book-equity | r1 | A | Saylor tangible variant; 68620/18777 = 3.65447089… full precision; tangible > 0. |
| b85 | declining-balance-final-period-depreciation-adjustment | r1 | A | Pearson final-year plug verbatim; book ≥ residual. |
| b86 | unit-contribution-margin | r1 | A | PUBLISHED ORACLE: UNG $25−$10 = $15. OVERLAP: same arithmetic as admitted economics CVP (different identities; operator reconciliation). |
| b86 | total-contribution-margin | r1 | A | PUBLISHED ORACLE: UNG $25,000−$10,000 = $15,000. Same overlap note. |
| b86 | operating-profit-from-contribution-and-fixed-costs | r1 | A | PUBLISHED ORACLE: UNG $15,000−$8,000 = $7,000; owner 50k misprint flagged + corrected. Same overlap note. |
| b86 | cost-plus-markup-selling-price | r1 | A | PUBLISHED ORACLE: Maine $1.00 @ 50%-on-cost = $1.50. |
| b87 | days-of-sales-outstanding | r2 | A | CFA ratio list verbatim (DSO = days/turnover); dual-convention handled; period/turnover > 0. Corrects sibling b16 r1 (cross-slice). |
| b88 | bond-linked-warrant-shares-from-principal | r1 | A | PUBLISHED TERMS: AMSC 3.75749 shares/lot; 335m/1000×3.75749 = 1,258,759.15; owner-grouping ambiguity flagged. |
| b89 | lifo-reserve-to-reported-inventory | r1 | NR | Owner-only sourcing, no accessible corroboration (independent search confirmed gap); superseded by r2/r3. |
| b90 | lifo-reserve-to-reported-inventory | r2 | NR | Same + owner Example 10 denominator conflict (current assets vs inventory); superseded by identical r3. |
| b91 | lifo-reserve-to-reported-inventory | r3 | NR | Latest; still unresolved corroboration + denominator conflict. Lead for r4: published reserve-to-FIFO tables (different ratio) could motivate re-scope. |
| b92 | net-sales-after-returns-and-allowances | r1 | A | Penn State sales-minus-discounts/returns verbatim. |
| b93 | consignment-agent-percentage-commission-revenue | r1 | A | Allegro percentage + Baozun agent context verbatim; base mismatch fenced; coherent [0,1] profile. Sup. by b94 r2 (bound removal). |
| b94 | consignment-agent-percentage-commission-revenue | r2 | A | Latest; rate ≥ 0; removal justified (no source states 100% cap). |
| b95 | doubtful-accounts-allowance-fraction-from-net-receivables | r1 | A | Hershey allowance-%-of-gross verbatim; 58/17932 full precision; net+allowance > 0. Sup. by b96 r2 (locator). |
| b96 | doubtful-accounts-allowance-fraction-from-net-receivables | r2 | A | Latest; locator corrected to p41 ratio table. |
| b97 | convatec-2016-adjusted-ebitda-reconciliation | r1 | NR | References in USD millions vs declared USD units (replay would misread ×1e6). Fixed by r2 (b99). |
| b98 | convatec-adjusted-ebit-from-reported-and-reconciling-items | r1 | NR | Same millions-vs-USD defect. Fixed by r2 (b99). |
| b99 | convatec-2016-adjusted-ebitda-reconciliation | r2 | A | Latest; USD-converted; figures verified vs AR p92 (507.6/473.8). |
| b99 | convatec-adjusted-ebit-from-reported-and-reconciling-items | r2 | A | Latest; USD-converted; figures verified vs AR pp90–91. |
| b100 | revenue-growth-constant-prior-period-exchange-rates | r1 | A | Conva
...[truncated 4110 chars]