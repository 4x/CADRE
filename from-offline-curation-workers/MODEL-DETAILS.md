# CFA Level I Volume 1 — model details

Latest revision of each distinct model. Each section is an equation-level formalization with original explanations, not a page or chapter reproduction. No registry integration or scientific approval is claimed.

## Additive decomposition of a nominal required interest rate

`financial-analysis--interest-rate-premium-decomposition@r1`

Source equation: `r = real risk-free interest rate + inflation premium + default risk premium + liquidity premium + maturity premium`

Evaluator: `real + inflation + default + liquidity + maturity`

Locator: Learning Module 1, Interest Rates, printed p5 (PDF p15), unnumbered decomposition and footnote 2

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `real` | input | Real risk-free periodic interest rate | 1 |
| `inflation` | input | Compensation for expected inflation over the security maturity | 1 |
| `default` | input | Compensation for failure to pay contracted amounts on time | 1 |
| `liquidity` | input | Compensation for cost of conversion to cash at fair value | 1 |
| `maturity` | input | Compensation for interest-rate sensitivity from maturity | 1 |
| `r` | output | Nominal required periodic interest rate | 1 |

Translation: All rates are decimal dimensionless numbers; addition is dimensionally consistent. The reduced nominal-risk-free form sets the other three premiums to zero. The exact Fisher relation is already covered by engineering-finance--fisher-real-rate and is not resubmitted.

Assumptions: Source assumption: components refer to the same currency, maturity and rate basis.; Source assumption: additive relationships are approximations used to explain the economics; footnote 2 distinguishes exact multiplicative inflation adjustment.

Limitations: Not a calibrated rate forecast or an exact Fisher identity; no parameters are estimated here.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b01/bundle.json). Corroboration: [Agricultural Use-Value Property Tax Assessment: Estimation and Policy Issues](https://aaec.vt.edu/content/dam/aaec_vt_edu/extension/use-value/Ag-Use-Value-Property-Tax-Assessment-Anderson-2012.pdf).

## Total simple interest on fixed original principal

`financial-analysis--simple-interest-total@r1`

Source equation: `Simple interest is interest rate times original principal each period; two periods on $100 at 5% produce $10 of simple interest.`

Evaluator: `P * r * N`

Locator: Learning Module 1, Future Value of a Single Cash Flow, printed pp6-7 (PDF pp16-17), original-principal example and unnumbered simple-interest definition

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `P` | input | Unchanged original principal | USD |
| `r` | input | Simple interest rate per financial period | 1 |
| `N` | input | Number of interest periods without capitalization | periods |
| `I` | output | Cumulative interest excluding all interest on interest | USD |

Translation: Derived definition from the CFA per-period simple-interest statement: sum N equal principal-only interest amounts. Pearson explicitly supplies I=Prt. N is a dimensionless financial count, not seconds. Currency times two dimensionless factors gives currency. Distinct from loan-payment-interest-portion because N-period cumulative simple interest never changes its original principal.

Assumptions: Source assumption: original principal is unchanged and interest is not capitalized.; Application profile: USD chosen as one currency; the same formula applies separately to any single currency.

Limitations: A fractional term requires an explicitly agreed financial-year fraction; this record supplies no day-count convention.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b01/bundle.json). Corroboration: [Mathematics of Finance, Chapter 5 publisher sample](https://www.pearson.com/content/dam/one-dot-com/one-dot-com/us/en/higher-ed/en/products-services/course-products/lial-applied-mathematics-info/pdf/LGR-Finite-Ch5.pdf).

## Continuous-compounding value of a single cash flow

`financial-analysis--lump-sum-future-value-continuous@r1`

Source equation: `FV_N = PV e^(r_s N)`

Evaluator: `PV * exp(r * N)`

Locator: Learning Module 1, Continuous Compounding, printed pp12-13 (PDF pp22-23), Equation (4), Example 6

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `PV` | input | Amount at the initial valuation date | USD |
| `r` | input | Constant continuously compounded rate per financial year | 1 |
| `N` | input | Financial years between initial and final dates | years |
| `FV` | output | Amount at the final valuation date | USD |

Translation: Map source r_s to r; exp implements the mathematical exponential without inlining e. Financial years are dimensionless, hence r*N is dimensionless and the result has currency dimension. Negative r represents continuous decay within the same relationship; PV>0 makes rate and term inverse discussion meaningful.

Assumptions: Source assumption: rate is constant and compounding continuous, with no interim deposits or withdrawals.; Application profile: all amounts use one declared currency and price basis.

Limitations: This is a continuous accumulation convention, distinct from the already covered discrete lump-sum record; the rate cannot be substituted unchanged between conventions.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b01/bundle.json). Corroboration: [Precalculus 2e](https://openstax.org/books/precalculus-2e/pages/4-1-exponential-functions).

## Effective annual rate from a continuous annual rate

`financial-analysis--effective-annual-rate-continuous@r1`

Source equation: `EAR = e^(r_s) - 1`

Evaluator: `exp(r) - 1`

Locator: Learning Module 1, Stated and Effective Rates, printed p14 (PDF p24), Equation (6); Exhibit 3 printed p13/PDF23

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `r` | input | Continuously compounded annual rate | 1 |
| `EAR` | output | Effective one-financial-year interest rate | 1 |

Translation: Map r_s to r and use exp rather than a numeric approximation of e. The literal 1 is the initial unit gross accumulation, not a conversion coefficient. Both sides are dimensionless decimal rates.

Assumptions: Source assumption: the quoted rate uses continuous compounding over one financial year.

Limitations: Not the discrete nominal-to-effective annual-rate record engineering-finance--effective-annual-rate-nominal; compounding convention differs.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b01/bundle.json). Corroboration: [Mathematics of Finance, Chapter 5 publisher sample](https://www.pearson.com/content/dam/one-dot-com/one-dot-com/us/en/higher-ed/en/products-services/course-products/lial-applied-mathematics-info/pdf/LGR-Finite-Ch5.pdf).

## Additivity of financial amounts valued at one date

`financial-analysis--cash-flow-value-additivity@r1`

Source equation: `Amounts of money indexed at the same point in time are additive.`

Evaluator: `sum(values)`

Locator: Learning Module 1, The Cash Flow Additivity Principle, printed p38 (PDF p48), Exhibit 15; unequal-cash-flow PV printed p25/PDF35 Exhibit 10

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `values` | family | Values of individual cash flows or streams already transported to a common date | USD |
| `V` | output | Combined signed financial value at that common date | USD |

Translation: Introduced family values maps the source prose to sum over same-date amounts. Currency terms add to currency. The same record supports sums of present values or future values; these are not minted as separate models. Individual cash-flow discounting is the covered discrete lump-sum relationship. Independent source contains a typo in Eq9.22; corroboration uses the explicit common-date addition prose and Table9.6, not that typo.

Assumptions: Source assumption: amounts share one date before addition.; Source assumption: values share currency and nominal/real basis and represent distinct, nonoverlapping cash-flow claims.

Limitations: Raw differently dated cash flows must first be discounted or accumulated; this record does not perform that transformation.; Family bounded to 256 terms per evaluation; family inverses are unavailable.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b02/bundle.json). Corroboration: [Principles of Finance](https://openstax.org/books/principles-finance/pages/9-1-timing-of-cash-flows).

## Rule of 72 approximate annual doubling time

`financial-analysis--rule-of-72-doubling-time@r1`

Source equation: `Approximate doubling periods = 72 / annual interest rate stated in percent`

Evaluator: `0.72 / r`

Locator: Learning Module 1, Solving for the Number of Periods, printed p32 (PDF p42), footnote 9 (Rule of 72)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `r` | input | Annual-compounding interest rate as a decimal | 1 |
| `N` | output | Heuristic financial years to double principal under annual compounding | years |

Translation: r is already a decimal unit-1 rate. The normalized heuristic coefficient .72 is attributed in constants, not an additional percent conversion applied by the engine. Financial-year count is dimensionless. Comparison at r=.08 gives heuristic9 versus exact9.00647; approximation uncertainty is not measurement uncertainty.

Assumptions: Source assumption: annual discrete compounding at a constant positive rate.; Application profile: 5%-12% rate range follows inspected Pearson corroboration, narrower than the unqualified CFA heuristic.

Limitations: Approximate, with no rigorous source error bound. Exact time is log(2)/log(1+r), already an inverse of the covered discrete lump-sum model.; No prediction of future achieved returns is asserted.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b02/bundle.json). Corroboration: [Mathematics of Finance, Chapter 5 publisher sample](https://www.pearson.com/content/dam/one-dot-com/one-dot-com/us/en/higher-ed/en/products-services/course-products/lial-applied-mathematics-info/pdf/LGR-Finite-Ch5.pdf).

## Relative frequency of a category or bin

`financial-analysis--relative-frequency@r1`

Source equation: `Relative frequency = absolute frequency / total number of observations`

Evaluator: `f / n`

Locator: Learning Module 2, Summarizing Data Using Frequency Distributions, printed pp71-72 (PDF pp81-82), definition and Exhibit 8

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `f` | input | Count in one selected category or bin | unit |
| `n` | input | Positive total observation count in the reference set | unit |
| `RF` | output | Observed fraction belonging to the selected category | 1 |

Translation: Source prose translated directly to f/n. Integer count units cancel to dimensionless fraction; no multiplication by100 is performed. Cumulative relative frequency is this same definition applied to a prefix-bin count, not a renamed model.

Assumptions: Source assumption: category and total refer to the same observation set.; Source assumption: f and n are counts; integrality is a semantic input contract, not expressible by the available guard operators.

Limitations: Relative frequency is an empirical fraction, not automatically a model probability.; Row or column conditional frequencies use the corresponding marginal count as n; distinct reference sets must be explicit.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b02/bundle.json). Corroboration: [Introductory Statistics 2e](https://openstax.org/books/introductory-statistics-2e/pages/1-3-frequency-frequency-tables-and-levels-of-measurement).

## Unrounded width of equal histogram bins

`financial-analysis--equal-bin-width@r1`

Source equation: `Bin width = Range / k`

Evaluator: `(upper - lower) / k`

Locator: Learning Module 2, Summarizing Data Using Frequency Distributions, printed pp72-73 (PDF pp82-83), construction Steps2-5 and Exhibit9

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `upper` | input | Upper endpoint of the covered data span | data-unit |
| `lower` | input | Lower endpoint of the covered data span | data-unit |
| `k` | input | Chosen positive number of equal bins | unit |
| `w` | output | Unrounded width required to span the endpoints with k equal bins | data-unit |

Translation: The CFA chooses sample extrema; the corroborating example chooses enclosing endpoints. Both give width=(upper-lower)/k before rounding. Unit U divided by dimensionless count preserves U. Extrema and integer k must be supplied because the scalar grammar cannot compute min/max or enforce integer type.

Assumptions: Source assumption: equal-width bins span the chosen endpoints.; Application profile: nondegenerate data span; k is a positive integer supplied externally.

Limitations: Does not select k, round the width or count observations into bins.; Constant datasets need a separate bin-selection convention.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b02/bundle.json). Corroboration: [Introductory Statistics 2e](https://openstax.org/books/introductory-statistics-2e/pages/2-2-histograms-frequency-polygons-and-time-series-graphs).

## Additivity of disjoint observation counts

`financial-analysis--disjoint-observation-count-additivity@r1`

Source equation: `Marginal frequency = sum of joint frequencies over the complementary categories; cumulative frequency = ordered prefix sum.`

Evaluator: `sum(counts)`

Locator: Learning Module2, Summarizing Data Using Frequency Distributions, printed p74/PDF84 Exhibit11; Contingency Table printed p78/PDF88 Exhibit14

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `counts` | family | Counts in mutually disjoint subsets of one dataset | unit |
| `total` | output | Count in the union of those subsets | unit |

Translation: One generic count-union definition captures both marginal and cumulative variants, avoiding separate sum-only clones. Counts are dimensionless numbers of observations and sum to counts. Financial cash-flow additivity uses a different scientific quantity and currency units.

Assumptions: Source assumption: subsets are disjoint and use the same observation unit.; Source assumption: category ordering is retained when interpreting a prefix sum as cumulative frequency.

Limitations: No classification or counting of raw observations is performed here.; Per-element nonnegative integrality must be checked at binding; the current guard grammar cannot quantify over a family.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b03/bundle.json). Corroboration: [Introductory Statistics 2e](https://openstax.org/books/introductory-statistics-2e/pages/1-3-frequency-frequency-tables-and-levels-of-measurement).

## Equity market capitalization from outstanding shares

`financial-analysis--equity-market-capitalization@r1`

Source equation: `Market capitalization = number of shares outstanding times price per share`

Evaluator: `shares * price`

Locator: Learning Module2, Summarizing Data Using a Contingency Table, printed p78 (PDF p88), opening unnumbered market-capitalization definition

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `shares` | input | Outstanding shares represented by the matching public share price | shares |
| `price` | input | Public market price for one matching outstanding share | USD/share |
| `cap` | output | Public market value of outstanding equity represented by the inputs | USD |

Translation: Source prose formalized directly. USD/share times shares yields USD. Fractional share counts can arise in units/scale conventions; counts and price must use matching per-share scale. No exchange-rate conversion included.

Assumptions: Source assumption: current share price and outstanding-share count refer to the same equity perimeter and valuation instant.; Application profile: one homogeneous share class and one currency; aggregate multiple classes only after separately valuing them.

Limitations: Not enterprise value, book value, free-float-adjusted capitalization or shares authorized.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b03/bundle.json). Corroboration: [Investor.gov: Market Capitalization](https://www.investor.gov/introduction-investing/investing-basics/glossary/market-capitalization).

## Expected contingency-table cell count under independence

`financial-analysis--contingency-expected-cell-count@r1`

Source equation: `Expected Value_i,j = (Total Row_i * Total Column_j)/Overall Total`

Evaluator: `row * column / n`

Locator: Learning Module2, Contingency Tables and Association, printed p81 (PDF p91), Equation(1), Example5 Step2

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `row` | input | Observed marginal count in the selected row | unit |
| `column` | input | Observed marginal count in the selected column | unit |
| `n` | input | Grand total count in the contingency table | unit |
| `E` | output | Fitted cell count implied by marginal proportions under independence | unit |

Translation: Count*count/count yields count. E can be fractional even when all observed margins are integers. Row and column margins must come from one consistent table. This is not a forecast of a future financial event.

Assumptions: Source assumption: expected counts are calculated under row/column independence with fitted observed margins.

Limitations: The formula itself is defined below five expected observations; minimum expected-cell rules apply to chi-square approximation validity, not this count definition.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b03/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm).

## Arithmetic mean of a finite numerical dataset

`financial-analysis--arithmetic-mean@r1`

Source equation: `X_bar = sum(X_i)/n`

Evaluator: `sum(x) / len(x)`

Locator: Learning Module2, The Arithmetic Mean, printed p101 (PDF p111), Equation(2); properties printed p103/PDF113

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `x` | family | Homogeneously measured numerical observations | data-unit |
| `mean` | output | Equally weighted average of the supplied observations | data-unit |

Translation: n becomes len(x), avoiding a freely supplied count inconsistent with data. Sum of U-valued observations divided by dimensionless n retains U. Generic data-unit requires extension; return-valued uses bind decimal returns with unit1, without changing the relationship. Sum of deviations equals0 is a consequence of this record, not new coverage.

Assumptions: Source assumption: numerical observations have comparable meaning, unit and support; categorical labels are not arithmetically averaged.; No random-sampling assumption is needed to define a mean; population inference requires additional assumptions.

Limitations: Not a geometric compound return; observations may have unequal economic exposure even though this definition weights them equally.; Family length1-256; empty dataset excluded by the family contract.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b03/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm).

## Weighted mean with normalized, possibly signed weights

`financial-analysis--normalized-weighted-mean@r1`

Source equation: `X_bar_w = sum_i(w_i X_i), sum_i(w_i)=1`

Evaluator: `sum(contributions)`

Locator: Learning Module2, The Weighted Mean, printed p108 (PDF p118), Equation(3); Example9 solution printed p109/PDF119

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `contributions` | family | Each element is one correctly paired product w_i*X_i; the underlying weights sum to1 | data-unit |
| `mean` | output | Weighted mean over the observations represented by the contribution family | data-unit |

Translation: Exact reparameterization c_i=w_i X_i; no approximation. The kit explicitly permits pretransformed family values. Each contribution has unit U, so its sum has U. For probability-weighted expectations the underlying weights additionally satisfy nonnegativity; that is a qualified use of this definition, not a clone.

Assumptions: Source assumption: the underlying weights sum to1 and pair with the intended observations.; Source assumption: negative weights may encode short positions; results need not lie between observations.

Limitations: The scalar grammar cannot multiply paired input families; contributions must be bound as precomputed w_i X_i terms with weight provenance.; Normalization and element alignment are binding conditions and cannot be inferred from the contribution values alone.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b04/bundle.json). Corroboration: [NumPy average documentation](https://numpy.org/doc/stable/reference/generated/numpy.average.html).

## Geometric mean of nonnegative observations

`financial-analysis--geometric-mean@r1`

Source equation: `X_bar_G = (X_1 X_2 ... X_n)^(1/n), X_i>=0`

Evaluator: `prod(x) ** (1 / len(x))`

Locator: Learning Module2, The Geometric Mean, printed pp109-110 (PDF pp119-120), Equation(4) and logarithmic equivalents

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `x` | family | Nonnegative observations of one numerical variable | data-unit |
| `G` | output | Equal-weight multiplicative mean of the observations | data-unit |

Translation: n is len(x). Symbolic dimensional check: product has U^n and its nth root has U. Research-only record uses a generic U; runtime dimensional projection requires dedicated family support/review. Do not infer all Xi>=0 from product>=0; that implication would be false for an even number of negatives.

Assumptions: Source assumption: every observation is nonnegative; negative observations are not accepted even when their product happens to be positive.; Source assumption: the observations share one numerical meaning and unit.

Limitations: Per-element nonnegativity requires binding validation; the product guard alone is necessary but insufficient.; The log representation requires strictly positive observations; the product form retains the admitted zero boundary.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b04/bundle.json). Corroboration: [SciPy geometric mean documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gmean.html).

## Geometric mean of linked periodic returns

`financial-analysis--geometric-mean-periodic-return@r1`

Source equation: `R_G = [product_t(1+R_t)]^(1/T)-1`

Evaluator: `prod(gross) ** (1 / len(gross)) - 1`

Locator: Learning Module2, The Geometric Mean, printed p110 (PDF p120), Equation(5); linked-wealth interpretation printed p112/PDF122

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `gross` | family | One plus each decimal holding-period return; matched equal-length sequential periods | 1 |
| `R` | output | Constant per-period net return reproducing the linked wealth growth | 1 |

Translation: Introduced gross family maps exactly to1+R_t. All factors and the root are dimensionless. The final1 subtracts the gross-return principal baseline; it is not a percent conversion. This record defines a statistic of a return history; the covered discrete lump-sum rate inverse instead relates a fixed rate and endpoint amounts.

Assumptions: Source assumption: returns are decimal simple net returns with corresponding gross factors>=0.; Source assumption: periods have equal duration and the cash-flow treatment permits geometric linking.

Limitations: Prebind gross factors; the engine cannot add1 to every member of a raw-return family.; The mean is per input period, not annual unless periods are annual. No money-weighted rate is solved.; Every factor must be nonnegative; product-level guard does not fully enforce that semantic condition.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b04/bundle.json). Corroboration: [SciPy geometric mean documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gmean.html).

## Harmonic mean of positive observations

`financial-analysis--harmonic-mean@r1`

Source equation: `X_bar_H = n / sum_i(1/X_i), X_i>0`

Evaluator: `len(reciprocals) / sum(reciprocals)`

Locator: Learning Module2, The Harmonic Mean, printed p113 (PDF p123), Equation(6); cost-averaging Example12 printed p114/PDF124

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `reciprocals` | family | Reciprocals of the original strictly positive observations, each with paired source provenance | 1/data-unit |
| `H` | output | Reciprocal of the arithmetic mean of the observation reciprocals | data-unit |

Translation: Exact substitution q_i=1/X_i preserves the original definition. Dimensionless n divided by U^-1 yields U. Sum positivity alone does not prove all reciprocals positive; the element domain is checked at binding. Negative or zero original values are outside this source model.

Assumptions: Source assumption: all original observations are strictly positive.; Source assumption: equal-cash cost averaging is a use case only when the cash amount invested each period is constant.

Limitations: Reciprocal inputs must be prepared outside the family expression; this is not a raw-array reciprocal operator.; Does not apply the generally false all-sample identity A*H=G^2 printed later in the source.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b04/bundle.json). Corroboration: [SciPy harmonic mean documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hmean.html).

## R6 percentile location in an ordered dataset

`financial-analysis--percentile-r6-location@r1`

Source equation: `L_y=(n+1)y/100`

Evaluator: `(n + 1) * p`

Locator: Learning Module2, Quantiles, printed p117 (PDF p127), Equation(7)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `n` | input | Number of sorted observations | unit |
| `p` | input | Requested cumulative fraction | 1 |
| `L` | output | Possibly fractional one-based rank of the requested percentile | unit |

Translation: Introduced p is the decimal quantile fraction y/100. It uses unit1; no percent conversion factor is inlined. The arithmetic1 shifts from n to n+1 order spacing. Counts and locations are dimensionless.

Assumptions: Source assumption: this is the n+1 percentile convention with one-based ascending order.

Limitations: Not a universal quantile convention; R7 and R8 differ.; At extreme p, L may lie outside the observed ranks1..n; this location record does not choose an endpoint-clamping rule.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b05/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm).

## Interior percentile interpolation between adjacent order statistics

`financial-analysis--percentile-linear-interpolation@r1`

Source equation: `For L_y=k+d, estimate the percentile by linear interpolation between X_(k) and X_(k+1).`

Evaluator: `low + d * (high - low)`

Locator: Learning Module2, Quantiles, printed p117 (PDF p127), paragraph following Equation(7), linear-interpolation rule

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `low` | input | Observed value at externally selected integer rank k | data-unit |
| `high` | input | Observed value at the next rank | data-unit |
| `d` | input | Fractional distance from rank k toward k+1 | 1 |
| `Q` | output | Interior quantile value under the n+1 location convention | data-unit |

Translation: Derived symbolic transcription of the source interpolation prose. U+d*(U-U) has unitU. d is introduced, not a printed CFA symbol. No precision beyond the supplied order statistics is implied.

Assumptions: Source assumption: adjacent order statistics and fractional position are supplied from one consistent sorted dataset.; Application profile: interior ranks; d=0 admits the exact lower order statistic.

Limitations: Sorting, floor/rank selection and endpoint clamping are not computed by this scalar record.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b05/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm).

## Interquartile range

`financial-analysis--interquartile-range@r1`

Source equation: `IQR=Q_3-Q_1`

Evaluator: `q3 - q1`

Locator: Learning Module2, Quantiles, printed p117 (PDF p127), unnumbered IQR definition; Example14 printed p119/PDF129

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `q3` | input | 75th percentile under the chosen convention | data-unit |
| `q1` | input | 25th percentile under the same convention | data-unit |
| `IQR` | output | Width of the central quartile interval | data-unit |

Translation: Subtract two U-valued quantiles to obtain a U-valued nonnegative spread. Reference percentage returns are decimal input numbers, not percent-scale unit values.

Assumptions: Source assumption: quartiles use the same sample, units and quantile convention.

Limitations: Does not measure tail extent or select a quantile method.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b05/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm).

## Tukey inner fence for a selected side of a boxplot

`financial-analysis--boxplot-inner-fence@r1`

Source equation: `Upper fence=Q_3+1.5*IQR; lower fence=Q_1-1.5*IQR`

Evaluator: `q + side * 1.5 * IQR`

Locator: Learning Module2, Quantiles, printed p120 (PDF p130), unnumbered fence rules and Exhibit46

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `q` | input | UseQ3 for upper side andQ1 for lower side | data-unit |
| `side` | input | Side code matched to the selected quartile | 1 |
| `IQR` | input | Nonnegative spread of the same dataset | data-unit |
| `fence` | output | Selected1.5-IQR outlier threshold | data-unit |

Translation: Introduced signed side unifies the two otherwise identical fence definitions. All data terms have unitU and side is dimensionless. The1.5 multiplier is source-attributed in constants. No claim that source example rounding is exact.

Assumptions: Source assumption: q is the matching first or third quartile and IQR uses the same dataset.; Application profile: side encodes the two source formulas in one canonical relationship.

Limitations: A fence is a threshold, not automatically the observed whisker endpoint; observations beyond it are potential outliers.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b05/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm).

## Range of a numerical dataset

`financial-analysis--data-range@r1`

Source equation: `Range=Maximum value-Minimum value`

Evaluator: `maximum - minimum`

Locator: Learning Module2, Measures of Dispersion, printed p123 (PDF p133), Equation(8); earlier construction printed p72/PDF82

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `maximum` | input | Largest observation, supplied externally | data-unit |
| `minimum` | input | Smallest observation, supplied externally | data-unit |
| `R` | output | Full observed max-minus-min spread | data-unit |

Translation: The extrema are bound inputs because min/max are outside the scalar function set. U-U yieldsU; zero range is admitted for constant data.

Assumptions: Source assumption: extrema belong to the same dataset and use the same units.

Limitations: Uses only two order statistics and does not describe within-range distribution.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b05/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm).

## Mean absolute deviation about the arithmetic mean

`financial-analysis--mean-absolute-deviation@r1`

Source equation: `MAD = sum_i |X_i-X_bar| / n`

Evaluator: `sum(deviations) / len(deviations)`

Locator: Learning Module2, The Mean Absolute Deviation, printed p124 (PDF p134), Equation(9); Example16 printed p125/PDF135

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `deviations` | family | Absolute deviations for every original observation about the same sample arithmetic mean | data-unit |
| `MAD` | output | Average absolute distance from the sample arithmetic mean | data-unit |

Translation: Introduced a_i maps the absolute-value terms exactly. The expression averages U-valued distances and retainsU. Published examples in percentage points are explicitly given as a data-unit profile; no engine percent scale conversion is applied.

Assumptions: Source assumption: every element is an absolute deviation about the same arithmetic mean and all observations are represented.

Limitations: Precomputed absolute deviations are required because elementwise abs is unavailable; provenance of their center must be retained.; CFA MAD here means mean absolute deviation, not median absolute deviation used by some software.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b06/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm).

## Sample variance with Bessel correction

`financial-analysis--sample-variance@r1`

Source equation: `s^2 = sum_i(X_i-X_bar)^2/(n-1)`

Evaluator: `sum(squares) / (len(squares) - 1)`

Locator: Learning Module2, Sample Variance, printed p125 (PDF p135), Equation(10); Example17 printed p127/PDF137

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `squares` | family | Squared deviations of every observation about their common sample mean | data-unit^2 |
| `variance` | output | Sum of squared sample-mean deviations divided by n-1 | data-unit^2 |

Translation: n=len(squares); the literal1 removes the estimated-mean degree of freedom, not an empirical constant. U^2 divided by a dimensionless count yieldsU^2. All terms are squared values even if their original deviations were negative.

Assumptions: Source assumption: at least two observations; the center is their sample arithmetic mean.; For the unbiased-population-variance interpretation, observations are identically distributed independent draws with finite variance; the descriptive statistic itself needs no such sampling claim.

Limitations: Precomputed squared deviations must share a common center and include every observation.; Not population variance, which uses a different denominator and center definition.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b06/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm).

## Sample standard deviation from its variance

`financial-analysis--sample-standard-deviation-from-variance@r1`

Source equation: `s = sqrt(s^2)`

Evaluator: `sqrt(variance)`

Locator: Learning Module2, Sample Standard Deviation, printed p126 (PDF p136), Equation(11) and square-root definition

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `variance` | input | Sample variance using the matching n-1 convention | data-unit^2 |
| `s` | output | Nonnegative square root of matching sample variance | data-unit |

Translation: sqrt(U^2)=U, selecting the nonnegative statistical root. The source also supplies the equivalent full n-1 formula; that expanded equation is not a second record.

Assumptions: Source assumption: variance and standard deviation describe the same sample, numerical units and estimator convention.

Limitations: Taking the square root does not change sample variance into a population estimator or provide inferential uncertainty.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b06/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm).

## Sample target downside deviation with full n-1 denominator

`financial-analysis--sample-target-downside-deviation@r1`

Source equation: `s_Target = sqrt(sum_{X_i<=B}(X_i-B)^2/(n-1))`

Evaluator: `sqrt(sum(shortfall_squares) / (len(shortfall_squares) - 1))`

Locator: Learning Module2, Downside Deviation, printed p128 (PDF p138), Equation(12); Example18 printed p129/PDF139

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `shortfall_squares` | family | One nonnegative element per original observation, including zero for every nonshortfall | data-unit^2 |
| `s` | output | Root mean-square shortfall with full sample n-1 denominator | data-unit |

Translation: Exact zero-filled reparameterization preserves the full denominator through len(shortfall_squares); equality at target contributes0. U^2 under sqrt yieldsU. This source-specific statistic is not asserted to be an unbiased variance estimator.

Assumptions: Source assumption: one fixed target B applies to the whole sample.; Source assumption: n counts all observations, including those above the target; n>1.

Limitations: Conditional squared-shortfall preprocessing is external to the family grammar; raw returns and target provenance must be retained.; Other downside-risk conventions divide by n or by downside count; they are not interchangeable with this n-1 source convention.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b06/bundle.json). Corroboration: [Semi-Deviation and Coefficient of Variation: Downside Risk and Risk per Unit of Return](https://analystprep.com/cfa-level-1-exam/uncategorized/semi-deviation-and-coefficient-of-variation-downside-risk-and-risk-per-unit-of-return/).

## Coefficient of variation for a positive-mean dataset

`financial-analysis--coefficient-of-variation@r1`

Source equation: `CV = s/X_bar`

Evaluator: `s / mean`

Locator: Learning Module2, Coefficient of Variation, printed p131 (PDF p141), Equation(13); Example20 printed pp132-133/PDF142-143

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `s` | input | Sample standard deviation of the numerical observations | data-unit |
| `mean` | input | Positive arithmetic mean of the same observations | data-unit |
| `CV` | output | Standard deviation per unit of positive mean | 1 |

Translation: U/U is dimensionless; no100 multiplier is applied. CV1.4 is a ratio, not a1.4% value.

Assumptions: Source assumption: mean is positive for the source financial interpretation.; Source assumption: mean and standard deviation use the same numerical scale; meaningful comparisons require a ratio scale with meaningful zero.

Limitations: Undefined for mean0; a negative-mean signed quotient is excluded from this positive-mean profile.; Near-zero positive means make the statistic highly sensitive.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b06/bundle.json). Corroboration: [NIST Dataplot Reference Manual](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/coefvari.htm).

## Sample covariance of paired observations

`financial-analysis--sample-covariance@r1`

Source equation: `s_XY=sum_i((X_i-X_bar)(Y_i-Y_bar))/(n-1)`

Evaluator: `sum(cross) / (len(cross) - 1)`

Locator: Learning Module2, Correlation between Two Variables, printed p140 (PDF p150), Equation(14)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `cross` | family | One centered product for each matched observation pair | data-unit-x*data-unit-y |
| `cov` | output | Signed paired-sample covariance using n-1 | data-unit-x*data-unit-y |

Translation: c_i is introduced as an exact paired transformation. n=len(cross), and the1 represents the mean-estimation degree-of-freedom correction. U*V remainsU*V after division by a count.

Assumptions: Source assumption: every centered product uses the matching pair and the corresponding sample means.; Independent identically distributed pairs with finite second moments justify the unbiased-population-covariance interpretation.

Limitations: Precomputed centered cross products are required; covariance alone does not imply causation.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b07/bundle.json). Corroboration: [NumPy covariance documentation](https://numpy.org/doc/stable/reference/generated/numpy.cov.html).

## Pearson sample correlation from covariance and standard deviations

`financial-analysis--pearson-correlation-from-covariance@r1`

Source equation: `r_XY=s_XY/(s_X*s_Y)`

Evaluator: `cov / (sx * sy)`

Locator: Learning Module2, Correlation between Two Variables, printed p140 (PDF p150), Equation(15)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `cov` | input | Covariance of the paired sample | data-unit-x*data-unit-y |
| `sx` | input | Positive sample standard deviation of X | data-unit-x |
| `sy` | input | Positive sample standard deviation of Y | data-unit-y |
| `r` | output | Dimensionless linear association for the same paired sample | 1 |

Translation: U*V/(U*V) is dimensionless. The denominator is strictly positive; sign comes entirely from covariance. The same standardization also describes population covariance when all three moments have consistent population semantics; no separate clone is minted.

Assumptions: Source assumption: covariance and both standard deviations use the same paired sample and compatible estimator normalization.; Source assumption: neither variable is constant.

Limitations: Correlation measures linear association and can miss nonlinear dependence; no causal inference follows.; The covariance magnitude must satisfy the Cauchy bound implied by the supplied variances.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b07/bundle.json). Corroboration: [NumPy Pearson correlation documentation](https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html).

## CFA large-sample skewness approximation using sample s

`financial-analysis--large-sample-skewness-approximation@r1`

Source equation: `Skewness approximately (1/n)*sum_i(X_i-X_bar)^3/s^3`

Evaluator: `sum(cubes) / (len(cubes) * s ** 3)`

Locator: Learning Module2, The Shape of Distributions, printed p135 (PDF p145), unnumbered large-sample skewness approximation

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `cubes` | family | One signed cubed centered deviation per original observation | data-unit^3 |
| `s` | input | Positive standard deviation computed with denominator n-1 | data-unit |
| `skew` | output | Source large-n approximation to sample skewness | 1 |

Translation: The corroborating NIST g1 uses s0 with denominator n, unlike CFA sample s. Since s0^2=(n-1)*s^2/n, the CFA approximation equals NISTg1*((n-1)/n)^(3/2). This explicit normalization translation corroborates the standardized moment without falsely claiming identical finite-sample estimators. U^3/U^3 cancels.

Assumptions: Source assumption: n>=100 and s is the source sample standard deviation.; Exact correspondence to a standardized central moment requires matching finite-sample scale conventions.

Limitations: This is the source approximation, not a finite-sample bias-corrected skewness estimator.; Per-element transformations and sample-scale consistency need binding review.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b07/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35b.htm).

## CFA large-sample excess kurtosis approximation using sample s

`financial-analysis--large-sample-excess-kurtosis-approximation@r1`

Source equation: `K_E approximately [(1/n)*sum_i(X_i-X_bar)^4/s^4]-3`

Evaluator: `sum(fourths) / (len(fourths) * s ** 4) - 3`

Locator: Learning Module2, The Shape of Distributions: Kurtosis, printed p137 (PDF p147), unnumbered sample excess-kurtosis approximation

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `fourths` | family | One fourth-power centered deviation per observation | data-unit^4 |
| `s` | input | Positive standard deviation computed with denominator n-1 | data-unit |
| `excess` | output | Source large-sample standardized fourth moment less the Gaussian baseline | 1 |

Translation: NIST uses denominator-n standard deviation s0; CFA fourth-moment ratio=NISTkurtosis*((n-1)/n)^2. This states the actual convention difference. UnitU^4 cancels againsts^4;3 is the Gaussian population baseline and is source-attributed. Large-n approximation uncertainty has no source-reported error bound.

Assumptions: Source assumption: n>=100 and s uses the n-1 convention.; Fourth powers and s must derive from the same centered dataset.

Limitations: Not an exactly unbiased sample-kurtosis estimator; finite-sample values differ from software using denominator-n moments.; The approximate sample statistic is not subject to every population kurtosis bound without normalization adjustment.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b07/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35b.htm).

## Probability of an event complement

`financial-analysis--probability-complement@r1`

Source equation: `P(S)+P(S^C)=1`

Evaluator: `1 - p`

Locator: Learning Module3, Total Probability Rule, printed p188 (PDF p198), complement identity preceding Equation(5); probability axioms printed pp175-176/PDF185-186

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `p` | input | Probability of the defined eventS | 1 |
| `q` | output | Probability of every outcome outsideS | 1 |

Translation: All quantities are dimensionless probabilities;1 is the probability of the full sample space. This identity is its own inverse and is not duplicated for opposite event labels.

Assumptions: Source assumption: complement is taken in the same complete probability space.

Limitations: Does not estimate the original probability.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b08/bundle.json). Corroboration: [Introductory Statistics 2e](https://openstax.org/books/introductory-statistics-2e/pages/3-1-terminology).

## Odds in favor of an event

`financial-analysis--probability-to-odds@r1`

Source equation: `Odds forE=P(E)/[1-P(E)]`

Evaluator: `p / (1 - p)`

Locator: Learning Module3, Probability Stated as Odds, printed p177 (PDF p187), unnumbered odds-for and odds-against definitions

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `p` | input | Event probability with a nonzero complement | 1 |
| `odds` | output | Ratio of occurrence probability to nonoccurrence probability | 1 |

Translation: The1 in the denominator denotes total probability. Odds againstE are odds for the complement; no renamed reciprocal model is minted. Input probability and output odds use distinct quantity meanings despite both being dimensionless.

Assumptions: Source assumption: finite odds require p<1.

Limitations: Odds are ratios, not probabilities; they may exceed1.; The certain-event endpoint has infinite odds and is outside the finite-scalar representation.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b08/bundle.json). Corroboration: [How do I interpret odds ratios in logistic regression?](https://stats.oarc.ucla.edu/other/mult-pkg/faq/general/faq-how-do-i-interpret-odds-ratios-in-logistic-regression/).

## Conditional probability from a joint and conditioning probability

`financial-analysis--conditional-probability@r1`

Source equation: `P(A|B)=P(AB)/P(B), P(B)!=0`

Evaluator: `joint / given`

Locator: Learning Module3, Conditional and Joint Probability, printed p180 (PDF p190), Equations(1)-(2)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `joint` | input | Probability that bothAandB occur | 1 |
| `given` | input | Positive probability of the event conditioned upon | 1 |
| `conditional` | output | Probability ofA conditional onB | 1 |

Translation: Dimensional probability ratio is dimensionless but is declared conditional probability. Eq2 is an inverse view of this same relationship, not new coverage.

Assumptions: Source assumption: the joint event is the intersection ofAandB and P(B)>0.

Limitations: Conditioning on a probability-zero event needs additional measure-theoretic structure absent here.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b08/bundle.json). Corroboration: [Introductory Statistics 2e](https://openstax.org/books/introductory-statistics-2e/pages/3-1-terminology).

## Probability of the inclusive union of two events

`financial-analysis--two-event-union-probability@r1`

Source equation: `P(A orB)=P(A)+P(B)-P(AB)`

Evaluator: `a + b - joint`

Locator: Learning Module3, Conditional and Joint Probability, printed p181 (PDF p191), Equation(3); worked values printed p182/PDF192

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `a` | input | Marginal probability ofA | 1 |
| `b` | input | Marginal probability ofB | 1 |
| `joint` | input | Intersection probability forAandB | 1 |
| `union` | output | Probability that at least one ofAandB occurs | 1 |

Translation: Probability addition/subtraction is dimensionless. The guards impose the feasible Frechet bounds joint<=min(a,b) andjoint>=a+b-1 without needing min/max operators. The mutually exclusive special case joint0 remains part of this record.

Assumptions: Source assumption: all three probabilities describe the same two events and sample space.

Limitations: Does not assume independence; joint must be supplied or obtained from another justified relationship.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b08/bundle.json). Corroboration: [Introductory Statistics 2e](https://openstax.org/books/introductory-statistics-2e/pages/3-3-two-basic-rules-of-probability).

## Joint occurrence probability for mutually independent events

`financial-analysis--mutually-independent-intersection-probability@r1`

Source equation: `P(ABC...)=P(A)P(B)P(C)... under mutual independence`

Evaluator: `prod(probabilities)`

Locator: Learning Module3, Multiplication Rule for Independent Events, printed p185 (PDF p195), Equation(4) and following multi-event generalization

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `probabilities` | family | Marginal probability for each mutually independent event | 1 |
| `joint` | output | Probability that all represented events occur | 1 |

Translation: Finite product of dimensionless probabilities remains dimensionless. The two-event case is included without a separate clone. Conditional joint multiplication from Eq2 remains valid without independence but uses different conditional inputs.

Assumptions: Source assumption: mutual independence, not merely pairwise independence, for three or more events.

Limitations: All element probabilities must be in[0,1] at binding; product bounds alone are insufficient.; Historical independence is not assumed from labels or zero sample correlation.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b09/bundle.json). Corroboration: [Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/chapter1/1_4_1_independence.php).

## Total probability over a finite scenario partition

`financial-analysis--law-total-probability@r1`

Source equation: `P(A)=sum_i P(A|S_i)P(S_i)=sum_i P(A intersect S_i)`

Evaluator: `sum(joints)`

Locator: Learning Module3, Total Probability Rule, printed p188 (PDF p198), Equations(5)-(6); Bayes example printed p207/PDF217

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `joints` | family | Joint probability mass for eventA in each disjoint exhaustive scenario | 1 |
| `p` | output | Unconditional probability ofA over the partition | 1 |

Translation: Exact reparameterization of the printed conditional/scenario products as joint masses. Although weighted-mean arithmetic is shared, this named probability identity relates conditional partition masses to one unconditional event probability. Each input and output is a probability, not an observation or return.

Assumptions: Source assumption: the scenarios form a disjoint exhaustive partition.; Each q_i uses the same target eventA; zero-probability scenarios can contribute zero without defining a conditional probability on them.

Limitations: Joint contributions must be prepared with their partition and likelihood provenance; raw paired family multiplication is unavailable.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b09/bundle.json). Corroboration: [Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/chapter1/1_4_2_total_probability.php).

## Variance of a finite discrete random variable

`financial-analysis--discrete-distribution-variance@r1`

Source equation: `Var(X)=sum_i P(X_i)[X_i-E(X)]^2`

Evaluator: `sum(terms)`

Locator: Learning Module3, Expected Value and Variance, printed pp192-193 (PDF pp202-203), Equations(8)-(9)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `terms` | family | Nonnegative contribution from each possible outcome, centered on the same exact distribution mean | data-unit^2 |
| `variance` | output | Population/distribution variance over the complete finite support | data-unit^2 |

Translation: The introduced family stores each source probability-weighted square exactly. Dimensionless probability timesU^2 givesU^2. The CFA EPS example rounds its center from2.3405 to2.34; the references avoid treating its rounded-center result as an exact population variance.

Assumptions: Source assumption: outcomes form complete finite support with nonnegative probabilities summing to1.; Center is the exact expectation from that distribution, not an arbitrarily rounded estimate.

Limitations: Terms must be prepared consistently; this record does not estimate probabilities from data.; No sample degrees-of-freedom correction belongs in this population definition.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b09/bundle.json). Corroboration: [Introductory Statistics 2e](https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation).

## Covariance from a finite joint distribution

`financial-analysis--joint-distribution-covariance@r1`

Source equation: `Cov(R_A,R_B)=sum_i sum_j P(R_Ai,R_Bj)(R_Ai-E R_A)(R_Bj-E R_B)`

Evaluator: `sum(terms)`

Locator: Learning Module3, Covariance Given a Joint Probability Function, printed p203 (PDF p213), Equation(19), Exhibit16; expectation definition printed p198/PDF208 Eq14

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `terms` | family | Signed centered cross-product contributions covering the complete joint support | data-unit-x*data-unit-y |
| `cov` | output | Covariance under the supplied joint probability law | data-unit-x*data-unit-y |

Translation: Each term hasU*V because probability is dimensionless. No n-1 divisor: this is distribution covariance, scientifically distinct from the sample estimator. Sparse zero-probability cells contribute0 and may be omitted if full-support accounting is documented.

Assumptions: Source assumption: the joint probability table is coherent, nonnegative and normalized, with means from its own marginals.

Limitations: All probability-weighted cross terms must be bound externally with correct pairing; no independence assumption is required.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b09/bundle.json). Corroboration: [Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/chapter5/5_3_1_covariance_correlation.php).

## Variance of a fixed-weight portfolio

`financial-analysis--fixed-weight-portfolio-variance@r1`

Source equation: `Var(Rp)=sum_i sum_j w_i w_j Cov(R_i,R_j)`

Evaluator: `sum(terms)`

Locator: Learning Module3, Portfolio Expected Return and Variance, printed pp198-199 (PDF pp208-209), Equations(16)-(18); two-asset example printed p201/PDF211

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `terms` | family | All ordered covariance contributions, or equivalently diagonal terms and doubled unique off-diagonal terms, for one portfolio | 1 |
| `variance` | output | Variance of the fixed-weight portfolio return | 1 |

Translation: Exact flattened quadratic form, with either both ordered off-diagonals or one doubled representative but never both conventions together. The two-asset form w1^2*v1+w2^2*v2+2*w1*w2*cov12 is a qualified case of this same record. Decimal returns are dimensionless; percent-squared references are normalized once during binding.

Assumptions: Source assumption: deterministic weights and all asset moments share the same horizon and return definition; source portfolio weights sum to1.; Covariance matrix is symmetric positive semidefinite; short positions may create signed cross contributions.

Limitations: Precomputed contributions must preserve weights and matrix provenance; sum positivity alone cannot establish matrix coherence.; Full raw matrix operations are outside the scalar grammar. At most256 supplied contributions per evaluation; larger exact sums require explicit aggregation outside this record.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b09/bundle.json). Corroboration: [WWWFinance: Optimal Portfolio Control](https://people.duke.edu/~charvey/classes/ba350/control/opc.htm).

## Bayes posterior probability from likelihood and prior

`financial-analysis--bayes-posterior-probability@r1`

Source equation: `P(Event|Information)=P(Information|Event)*P(Event)/P(Information)`

Evaluator: `likelihood * prior / evidence`

Locator: Learning Module3, Bayes Formula, printed p206 (PDF p216), Equation(20); frequency example printed pp207-208/PDF217-218

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `likelihood` | input | Probability of the observed information conditional on the selected event | 1 |
| `prior` | input | Probability of the event before the new information | 1 |
| `evidence` | input | Strictly positive marginal probability of the observed information | 1 |
| `posterior` | output | Event probability conditional on the observed information | 1 |

Translation: Source symbols map directly to separately defined prior, likelihood, marginal evidence and posterior quantities. All are dimensionless; likelihood is a conditional probability here, not a density. Coherence bounds require likelihood*prior<=evidence<=likelihood*prior+1-prior.

Assumptions: Source assumption: likelihood, prior and evidence are coherent probabilities for the same event and information.; Positive prior is required to give the supplied event-conditional likelihood its ordinary event-conditioning meaning.

Limitations: Does not estimate priors or likelihoods, and supplies no financial forecast or recommendation.; Impossible evidence has no posterior under this finite-event formula.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b10/bundle.json). Corroboration: [Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/chapter1/1_4_3_bayes_rule.php).

## Multiplication rule for finite sequential task counts

`financial-analysis--sequential-counting-product@r1`

Source equation: `Number of ways=(n_1)(n_2)...(n_k)`

Evaluator: `prod(branches)`

Locator: Learning Module3, Principles of Counting, printed pp212-213 (PDF pp222-223), unnumbered multiplication rule, Exhibit21 and factorial definition; permutation printed p215/PDF225 Eq23

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `branches` | family | Number of admissible choices at each successive stage, conditional on each preceding path | unit |
| `ways` | output | Number of complete admissible task sequences | unit |

Translation: All counts are dimensionless cardinalities. n! is the specialization branches=[n,n-1,...,1]; ordered r-permutations use[n,n-1,...,n-r+1]. The conventional empty product0!=1 or r0 count1 can be bound as identity-family[1], explicitly identified as the empty-task boundary rather than a physical choice stage.

Assumptions: Source assumption: branch count at a stage is the same for every admissible preceding path.; Choice counts are integers and refer to the declared replacement/order convention.

Limitations: A nonuniform branching tree needs a sum over paths or a recursive representation.; The family grammar does not generate descending integer sequences automatically.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b10/bundle.json). Corroboration: [SticiGui: Counting](https://www.stat.berkeley.edu/~stark/SticiGui/Text/counting.htm).

## Multinomial count of fixed-size labeled groups

`financial-analysis--multinomial-labeling-count@r1`

Source equation: `n!/(n_1! n_2! ... n_k!), sum_i n_i=n`

Evaluator: `total_factorial / prod(group_factorials)`

Locator: Learning Module3, Principles of Counting, printed p214 (PDF p224), Equations(21)-(22), bond-fund labels and combination examples

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `total_factorial` | input | Factorial of the total number of distinct objects, prepared by the counting-product relationship | unit |
| `group_factorials` | family | Factorial of each fixed category size, including0!=1; category sizes sum to the total | unit |
| `ways` | output | Number of assignments to distinct labeled groups with the specified sizes | unit |

Translation: This is an exact substitution of the printed factorial quantities, not an approximation. Factorials are scientific input quantities derived from integer counts and can be supplied through the counting-product record. A combination nCr is the two-label case with sizesr,n-r; do not mint it as another equivalent relationship.

Assumptions: Source assumption: objects are distinct, labels are distinct, and ordering within a labeled group is irrelevant.; Each factorial input derives from a nonnegative category size and those sizes sum to the total object count.

Limitations: Factorial preparation and category-size consistency are external binding requirements; arbitrary positive numbers are not admissible substitutes.; At most256 label-factorial terms per evaluation; full combinatorial big-integer arithmetic may exceed numeric precision for large counts.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b10/bundle.json). Corroboration: [SticiGui: Counting](https://www.stat.berkeley.edu/~stark/SticiGui/Text/counting.htm).

## Interval probability from two cumulative probabilities

`financial-analysis--interval-probability-from-cdf@r1`

Source equation: `P(a<X<=b)=F(b)-F(a)`

Evaluator: `Fb - Fa`

Locator: Learning Module4, Discrete and Continuous Uniform Distribution, printed p242 (PDF p252), unnumbered CDF-difference examples; continuous endpoint equivalence printed p245/PDF255

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `Fb` | input | Cumulative probability at the interval upper endpoint | 1 |
| `Fa` | input | Cumulative probability at the excluded lower endpoint | 1 |
| `p` | output | Probability of lower-open upper-closed interval | 1 |

Translation: Both inputs and output are dimensionless probabilities. The interval endpoint values themselves are not required once matching CDF evaluations are supplied; their ordering remains a context condition.

Assumptions: Source assumption: both CDF evaluations belong to the same random variable with ordered endpoints.

Limitations: For discrete data, including the lower endpoint requires a left-limit CDF or an additional point mass.; For continuous laws, endpoint inclusion has no effect because point masses vanish.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b11/bundle.json). Corroboration: [Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/chapter3/3_2_1_cdf.php).

## Density height inside a continuous uniform support

`financial-analysis--continuous-uniform-density@r1`

Source equation: `f(x)=1/(b-a) for a<=x<=b;0 otherwise`

Evaluator: `1 / (b - a)`

Locator: Learning Module4, Continuous Uniform Distribution, printed p243 (PDF p253), unnumbered piecewise density definition

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `a` | input | Lower support endpoint | data-unit |
| `b` | input | Upper support endpoint | data-unit |
| `density` | output | Constant density for a query point inside the declared uniform support | 1/data-unit |

Translation: No query x port is needed for an interior constant density, but support membership is an explicit binding condition. ReciprocalU givesU^-1. The literal1 encodes normalized total mass.

Assumptions: Source assumption: b>a and the query point lies inside[a,b].

Limitations: The outside-support branch is0 and is not evaluated by this interior scalar record.; Density is not a point probability and carries inverse observation units.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b11/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3662.htm).

## Interior cumulative probability of a continuous uniform law

`financial-analysis--continuous-uniform-cdf-interior@r1`

Source equation: `F(x)=(x-a)/(b-a) for a<=x<=b`

Evaluator: `(x - a) / (b - a)`

Locator: Learning Module4, Continuous Uniform Distribution, printed p244 (PDF p254), unnumbered piecewise CDF and F(3) example

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `x` | input | Threshold inside the uniform support | data-unit |
| `a` | input | Lower support endpoint | data-unit |
| `b` | input | Upper support endpoint | data-unit |
| `F` | output | Probability X<=x under the uniform law | 1 |

Translation: U/U is dimensionless probability. NIST states the standard support CDF F(z)=z; substituting z=(x-a)/(b-a) produces this general form exactly.

Assumptions: Source assumption: x lies in[a,b], with b>a.

Limitations: Full CDF has0 belowa and1 aboveb; those piecewise branches need a selector beyond this scalar profile.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b11/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3662.htm).

## Mean of a continuous uniform distribution

`financial-analysis--continuous-uniform-mean@r1`

Source equation: `mu=(a+b)/2`

Evaluator: `(a + b) / 2`

Locator: Learning Module4, Example2, printed p245 (PDF p255), unnumbered uniform-mean formula and Solution2

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `a` | input | Lower support endpoint | data-unit |
| `b` | input | Upper support endpoint | data-unit |
| `mu` | output | Population mean under the continuous uniform law | data-unit |

Translation: The arithmetic2 averages the two support endpoints, expressing the source symmetry result. U+U divided by a dimensionless count yieldsU.

Assumptions: Source assumption: continuous uniform probability law on a nondegenerate finite support.

Limitations: Not an estimated sample mean; input endpoints specify the distribution.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b11/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3662.htm).

## Variance of a continuous uniform distribution

`financial-analysis--continuous-uniform-variance@r1`

Source equation: `sigma^2=(b-a)^2/12`

Evaluator: `(b - a) ** 2 / 12`

Locator: Learning Module4, Example2, printed pp245-246 (PDF pp255-256), unnumbered uniform-variance formula and Solution2

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `a` | input | Lower support endpoint | data-unit |
| `b` | input | Upper support endpoint | data-unit |
| `variance` | output | Population variance under the continuous uniform law | data-unit^2 |

Translation: Squaring a support width producesU^2;12 is the source theoretical divisor, attributed as a constant. This is a distribution variance, not the sample n-1 estimator.

Assumptions: Source assumption: continuous uniform law with finite endpointsb>a.

Limitations: Support location cannot be inferred from variance alone.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b11/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3662.htm).

## Binomial probability of an exact success count

`financial-analysis--binomial-probability-mass@r1`

Source equation: `P(X=x)=C(n,x)*p^x*(1-p)^(n-x)`

Evaluator: `c * p ** x * (1 - p) ** (n - x)`

Locator: Learning Module4, Binomial Distribution, printed p247 (PDF p257), Equation(2); Exhibit6 printed p249/PDF259

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `n` | input | Nonnegative number of independent binary trials | unit |
| `p` | input | Common probability of success on every trial | 1 |
| `x` | input | Specified number of successes | unit |
| `c` | input | Exact combination count for the matchingn,x, prepared by the multinomial-labeling model | unit |
| `mass` | output | Probability of exactlyx successes inntrials | 1 |

Translation: Introducedc is the printed combination term, not an independently adjustable fit parameter. All factors are dimensionless; countcweights the separate sequence probabilities. Factorials are supplied by the curated counting relationship rather than an unsupportedfactorialcall.

Assumptions: Source assumption: trials are mutually independent and share a common fixed probabilityp.; Application profile:0<p<1 avoids degenerate0^0 branches; x,n are nonnegative integers and c is their exact combination count.

Limitations: Degeneratep0or1 requires explicit endpoint branches and is deferred rather than assigning0^0 silently.; The evaluator exponent limit100 restricts numerical evaluation of larger scientifically admissible trial counts; no altered probability law is asserted.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b12/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm).

## Mean success count of a binomial distribution

`financial-analysis--binomial-mean@r1`

Source equation: `E(X)=np`

Evaluator: `n * p`

Locator: Learning Module4, Binomial Distribution, printed p252 (PDF p262), Exhibit7; Example4 printed p253/PDF263

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `n` | input | Nonnegative number of independent binary trials | unit |
| `p` | input | Common probability of success on every trial | 1 |
| `mean` | output | Expected number of successes in the specified trials | unit |

Translation: Dimensionless probability times event-count cardinality gives expected count. Bernoulli meanp is the n1 specialization, not a separate record.

Assumptions: Source assumption: binomial model with fixed trial count and common success probability.; Linearity makes the mean expression valid even without independence when every trial has the same marginalp; independence is needed for the full binomial law and variance.

Limitations: Expected counts need not be integers and are not claims about any specific financial outcome.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b12/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm).

## Variance of a binomial success count

`financial-analysis--binomial-variance@r1`

Source equation: `Var(X)=np(1-p)`

Evaluator: `n * p * (1 - p)`

Locator: Learning Module4, Binomial Distribution, printed p252 (PDF p262), Exhibit7; Example4 printed p253/PDF263

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `n` | input | Nonnegative number of independent binary trials | unit |
| `p` | input | Common probability of success on every trial | 1 |
| `variance` | output | Population variance of the binomial success count | unit^2 |

Translation: Counts are dimensionless cardinalities; statistical variance is labeled squared-count for semantics. Bernoulli variancep(1-p) is included atn1. The literal1 is the complementary probability baseline.

Assumptions: Source assumption: independent Bernoulli trials with common probabilityp and fixed countn.

Limitations: Dependent defaults or heterogeneous probabilities invalidate this binomial variance expression.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b12/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm).

## Terminal stock price at a recombining two-factor tree node

`financial-analysis--binomial-price-tree-terminal-node@r1`

Source equation: `S_n=S*u^x*d^(n-x)`

Evaluator: `S * u ** x * d ** (n - x)`

Locator: Learning Module4, Binomial Distribution, printed pp248-249 (PDF pp258-259), Exhibit5 and terminal-price explanation

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `S` | input | Initial stock price per share | USD/share |
| `u` | input | Constant gross price multiplier on an up branch | 1 |
| `d` | input | Constant gross price multiplier on a down branch | 1 |
| `x` | input | Number of up moves to the node | unit |
| `n` | input | Total number of moves | periods |
| `terminal` | output | Stock price afterxup moves andn-xdown moves | USD/share |

Translation: Derived compact notation from the explicit source nodesuuuuS,uuudS,uuddS,... . Gross factors and financial period counts are dimensionless, leaving the initial price unit intact. Do not assumed=1/u; the source tree does not impose that restriction.

Assumptions: Source assumption: constant multiplicative up/down factors, so order of moves does not affect the terminal node.; No dividends, splits or other price adjustments occur within this stated price-path model.

Limitations: This computes a conditional node value, not an option price or forecast; transition probabilities and risk-neutral valuation are separate.; Large move counts may exceed the scalar evaluator exponent bound.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b12/bundle.json). Corroboration: [Introduction to Julia: Stock Problem](https://ucidatascienceinitiative.github.io/IntroToJulia/Html/StockProblem).

## Normal probability density

`financial-analysis--normal-probability-density@r1`

Source equation: `f(x)=exp[-(x-mu)^2/(2sigma^2)]/[sigma*sqrt(2pi)]`

Evaluator: `exp(-((x - mu) / sigma) ** 2 / 2) / (sigma * sqrt(2 * pi))`

Locator: Learning Module4, The Normal Distribution, printed p256 (PDF p266), Equation(3)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `x` | input | Point at which the normal density is evaluated | data-unit |
| `mu` | input | Normal location parameter | data-unit |
| `sigma` | input | Strictly positive normal scale parameter | data-unit |
| `density` | output | Normal probability density, distinct from point probability | 1/data-unit |

Translation: Standardizing before squaring makes the exp argument dimensionless. Density then hasU^-1. The expression names registry constantpi rather than inlining it. Arithmetic2 factors come from the stated Gaussian normalization. No registryconstant is duplicated in constants metadata.

Assumptions: Source assumption: a normal law withfinite meanand strictly positive scale.

Limitations: A density value is not the probability of one exact continuous outcome; normal CDF evaluation requires an unavailable operator.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b13/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3661.htm).

## Standardized deviation or z-score

`financial-analysis--standardized-score@r1`

Source equation: `Z=(X-mu)/sigma`

Evaluator: `(x - mu) / sigma`

Locator: Learning Module4, Standardizing a Random Variable, printed p260 (PDF p270), Equation(4)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `x` | input | Value to standardize | data-unit |
| `mu` | input | Center of the same random variable | data-unit |
| `sigma` | input | Positive scale of the same variable | data-unit |
| `z` | output | Signed number of standard deviations from the mean | 1 |

Translation: (U-U)/U cancels to a dimensionless score. No normal CDF or inverse-CDF approximation is embedded.

Assumptions: Source assumption: observation, mean and standard deviation share units and support.; Normality is needed to interpretZas a standard normal random variable, but not to define the standardized score itself.

Limitations: Replacing population moments with estimated sample moments changes the sampling distribution; the score alone is not a probability.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b13/bundle.json). Corroboration: [SciPy zscore documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.zscore.html).

## Roy safety-first ratio for a specified return threshold

`financial-analysis--roy-safety-first-ratio@r1`

Source equation: `SFRatio=[E(Rp)-R_L]/sigma_P`

Evaluator: `(mean - threshold) / sigma`

Locator: Learning Module4, Applications of the Normal Distribution, printed p264 (PDF p274), Equation(5)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `mean` | input | Expected portfolio return over the declared horizon | 1 |
| `threshold` | input | Specified shortfall threshold for that same horizon | 1 |
| `sigma` | input | Strictly positive standard deviation of the portfolio return | 1 |
| `ratio` | output | Expected-return surplus above threshold in portfolio standard-deviation units | 1 |

Translation: Decimal return differences divided by matching decimal-return standard deviation are dimensionless. It equals the negative standardized threshold; its named economic meaning and threshold port distinguish the source risk statistic. Sharpe ratio is the qualified risk-free-threshold case, not an added clone.

Assumptions: Source assumption: horizon and return basis match across all threeinputs.; Normality is required for the specific shortfall probability identityPhi(-ratio); it is not required for the ratio arithmetic.

Limitations: The ratio is not a probability and no portfolio selection or investment recommendation is returned.; Shortfall probability needs a normalCDFoperator, deferred separately.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b13/bundle.json). Corroboration: [Roy Safety-first Criterion: Overview, Formula, Example](https://www.wallstreetoasis.com/resources/skills/trading-investing/roys-safety-first-criterion).

## Mean of an exponential normal variable

`financial-analysis--lognormal-mean-from-log-moments@r1`

Source equation: `mu_L=exp(mu+0.50sigma^2)`

Evaluator: `exp(mu + variance / 2)`

Locator: Learning Module4, The Lognormal Distribution, printed p268 (PDF p278), unnumbered mean formula

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `mu` | input | Mean of dimensionless normalX=log(Y) | 1 |
| `variance` | input | Variance of normalX=log(Y) | 1 |
| `mean` | output | Expected value of dimensionlessY=exp(X) | 1 |

Translation: NIST unit-scale meanexp(sigma^2/2) multiplied by scaleexp(mu) gives this exact parameterization. All exponent arguments and outputs are dimensionless. The divisor2is an arithmetic theoretical factor.

Assumptions: Source assumption: Xis normal andY=exp(X);the logarithm is of a dimensionless variable or explicitly normalized quantity.; Application boundary:variance0is the continuous degenerate limit, included for a constantY.

Limitations: For asset prices S=S0*Y,a separately declared price scaleS0is needed; the formula does not take the log of dimensional currency.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b13/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3669.htm).

## Variance of an exponential normal variable

`financial-analysis--lognormal-variance-from-log-moments@r1`

Source equation: `sigma_L^2=exp(2mu+sigma^2)*[exp(sigma^2)-1]`

Evaluator: `exp(2 * mu + variance) * (exp(variance) - 1)`

Locator: Learning Module4, The Lognormal Distribution, printed p269 (PDF p279), unnumbered variance formula

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `mu` | input | Mean of dimensionless normalX=log(Y) | 1 |
| `variance` | input | Variance of normalX=log(Y) | 1 |
| `V` | output | Population variance of dimensionlessY=exp(X) | 1 |

Translation: NIST scale1variance isexp(v)*(exp(v)-1);multiplication by scaleexp(mu)^2 gives the stated expression. Output and exponent arguments are dimensionless. Arithmetic2and1are source algebraic factors, not fitted coefficients.

Assumptions: Source assumption: Xnormal,Y=exp(X),and both input parameters refer toXat the same horizon.; Application boundary:variance0is the constant-distribution limit.

Limitations: This is not exp(VarX) and cannot use the mean/variance ofYas if they were the log parameters.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b13/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3669.htm).

## Aggregate continuously compounded return

`financial-analysis--aggregate-continuously-compounded-return@r1`

Source equation: `r(0,T)=sum[t=1..T]r(t-1,t)`

Evaluator: `sum(r)`

Locator: Learning Module4, Continuously Compounded Rates of Return, printed p270 (PDF p280), Equation(7)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `r` | family | Finite family of log returns over successive nonoverlapping intervals | 1 |
| `total` | output | Log return over the entire sequence | 1 |

Translation: The sum is exactly the logarithm of the telescoping product of positive gross returns. Family order must follow the declared consecutive intervals. No percent conversion factors occur.

Assumptions: Source assumption: strictly positive endpoint prices and a consistent definition of reinvested distributions if total returns are used.; Application boundary: at least one interval; no independence or normality is needed for this identity.

Limitations: The engine consumes already computed log returns; it does not match price timestamps or adjust dividends.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b14/bundle.json). Corroboration: [Precalculus 2e](https://openstax.org/books/precalculus-2e/pages/4-5-logarithmic-properties).

## Mean of an equal-period aggregate log return

`financial-analysis--equal-period-log-return-mean-scaling@r1`

Source equation: `E[r(0,T)]=mu*T`

Evaluator: `mu * T`

Locator: Learning Module4, Continuously Compounded Rates of Return, printed p270 (PDF p280), Equation(8)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `mu` | input | Common finite expected log return per observation interval | 1 |
| `T` | input | Positive integer number of consecutive equal-length observation intervals | 1 |
| `mean` | output | Expected aggregate log return | 1 |

Translation: Linearity of expectation applied to Equation7 produces T identical mean terms. The common-period mean and aggregate mean have distinct horizons.

Assumptions: Source uses independent identically distributed log returns. Equal finite means alone suffice for this expectation identity; no normality is needed.; T is a dimensionless integer count, not elapsed physical seconds.

Limitations: This gives expected log return, not expected simple return; exponentiating the expectation does not commute with expectation.; Input integrability and integer-period semantics require external binding checks.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b14/bundle.json). Corroboration: [Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/chapter3/3_2_2_expectation.php).

## Volatility scaling for uncorrelated equal-variance log returns

`financial-analysis--uncorrelated-return-volatility-horizon-scaling@r1`

Source equation: `SD[r(0,T)]=sigma*sqrt(T); Var[r(0,T)]=sigma^2*T`

Evaluator: `sigma * sqrt(T)`

Locator: Learning Module4, Continuously Compounded Rates of Return, printed pp270-271 (PDF pp280-281), Equation(9) and following square-root rule

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `sigma` | input | Nonnegative common interval log-return standard deviation | 1 |
| `T` | input | Positive integer number of equal-length observation intervals | 1 |
| `volatility` | output | Standard deviation of aggregate log return | 1 |

Translation: The variance equation and its nonnegative square root are one canonical relationship, not separate copies. Signed log-return means do not restrict volatility. No normality is needed for the variance identity.

Assumptions: Source uses independent identically distributed increments. Pairwise zero covariance and identical finite variance suffice for variance addition.; The aggregation horizon uses the same observation frequency as the suppliedsigma.

Limitations: Serial correlation invalidates this square-root rule; generic portfolio/covariance aggregation must include covariance terms.; A trading-day count is a caller-supplied convention, not a universal250 constant.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b14/bundle.json). Corroboration: [Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/chapter5/5_3_1_covariance_correlation.php).

## Chi-square realization from independent standard normal squares

`financial-analysis--chi-square-realization-from-normal-squares@r1`

Source equation: `chi^2=sum[i=1..k]Z_i^2, Z_i iid N(0,1)`

Evaluator: `sum(q)`

Locator: Learning Module4, Chi-Square Distribution, printed p274 (PDF p284), unnumbered sum-of-squares definition

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `q` | family | Finite family of nonnegative squared realizations of independent standard normal variables | 1 |
| `chi_square` | output | Nonnegative chi-square realization with k degrees of freedom | 1 |

Translation: Prebinding squares permits a finite-family sum without adding an unsupported random generator. The distributional scope distinguishes this from a generic sum or sample variance. Nonnegative family members are required externally.

Assumptions: Source assumption: originalZvariables are mutually independent and each is standard normal; k is a positive integer.; Binding contract: eachq_i isZ_i squared, nonnegative, and dimensionless; the family length determinesdf.

Limitations: Arithmetic cannot verify normality or independence, and the guard cannot quantify elementwise binding checks.; This does not compute a density, CDF, quantile, or generate random draws.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b14/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm).

## Standard error of an iid sample mean

`financial-analysis--sample-mean-standard-error@r1`

Source equation: `sigma_Xbar=sigma/sqrt(n); estimated SE=s/sqrt(n)`

Evaluator: `scale / sqrt(n)`

Locator: Learning Module5, The Central Limit Theorem and Distribution of the Sample Mean, printed p317 (PDF p327), Equations(1)-(2)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `scale` | input | Nonnegative population standard deviation, or sample estimate with the estimation convention explicitly bound | data-unit |
| `n` | input | Positive integer sample size; estimated scale requires n>=2 | 1 |
| `se` | output | True standard error if scale is known population SD, otherwise estimated standard error | data-unit |

Translation: Both source equations are one canonical relationship with explicit scale-estimation convention. U divided by dimensionless sqrt(n) remainsU. The variance formVar(Xbar)=sigma^2/n is its square, not a separate model.

Assumptions: Source assumption: independent equal-variance observations; the population standard deviation is finite. Normality is not needed for this standard-error identity.; Declare whether scale is a population parameter or sample standard deviation; in the latter case n>=2 and this output is an estimate.

Limitations: Finite-population sampling without replacement may need a finite-population correction, absent here.; Correlated observations need covariance terms; this formula does not estimate the SE of an arbitrary median or statistic.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b15/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm).

## Symmetric confidence bound from an externally supplied critical value

`financial-analysis--symmetric-mean-confidence-bound@r1`

Source equation: `Xbar +/- z_(alpha/2)*SE; Xbar +/- t_(alpha/2,n-1)*SE`

Evaluator: `estimate + side * critical * se`

Locator: Learning Module5, Confidence Intervals for the Population Mean and Sample Size Selection, printed pp325,327,329 (PDF pp335,337,339), Equations(4)-(6)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `estimate` | input | Observed mean estimating the declared population mean | data-unit |
| `side` | input | Exactly-1 for the lower bound or+1 for the upper bound | 1 |
| `critical` | input | Positive upper-tail critical value supplied for the declared confidence level, distribution and degrees of freedom | 1 |
| `se` | input | Nonnegative standard error appropriate to the sampling method | data-unit |
| `bound` | output | Selected endpoint of the confidence interval | data-unit |

Translation: The side port unifies two algebraic signs, and the distribution-specific critical input unifies Equations4-6 without confusing their assumptions. MarginE=critical*se; interval width2E. No percent conversion or fixed1.96 constant is embedded.

Assumptions: For known population variance and normal observations use the normal critical value. For unknown variance and normal iid data use t with n-1df.; Large-sample normal approximations require a justified CLT; no universal n30 threshold guarantees accuracy for every distribution.; Critical values must match the desired two-sided confidence coefficient1-alpha and right-tail areaalpha/2.

Limitations: Critical-value lookup/inverseCDF is unavailable; it is a required documented input.; A realized frequentist interval has no posterior probability attached to the fixed population mean.; This record returns one selected bound; call both sides for the interval.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b15/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm).

## One-sample mean t-statistic

`financial-analysis--one-sample-mean-t-statistic@r1`

Source equation: `t=(Xbar-mu0)/(s/sqrt(n))`

Evaluator: `(mean - null_mean) / (s / sqrt(n))`

Locator: Learning Module6, Identify the Appropriate Test Statistic, printed p360 (PDF p370), Exhibit4 single-mean row; also LM5 printed p328/PDF338

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `mean` | input | Observed sample mean | data-unit |
| `null_mean` | input | Fixed null-boundary population mean | data-unit |
| `s` | input | Strictly positive sample standard deviation with n-1 denominator | data-unit |
| `n` | input | Integer sample size at least2 | 1 |
| `t` | output | Signed mean test statistic with n-1df under the normal iid null model | 1 |

Translation: The null mean is a hypothesized boundary, not the true mean supplied to generic standardization. Units cancel. Known-population-SD z-statistic has the same form with population sigma replacing s; its distribution is different. Paired-difference form is this model under explicit difference-data binding, not a clone.

Assumptions: Exact t distribution requires independent identically normal observations with positive population variance, evaluated undermu=mu0;df=n-1.; For matched-pair tests the observations are within-pair differences and pairs are independent; n counts pairs ands is the SD of their differences.

Limitations: This computes the statistic only; p-values, critical values and reject/retain decisions need a separately supplied decision rule/distribution.; A test statistic is not a posterior probability of the null. Integer and pairing checks require external binding.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b15/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm).

## Pooled common variance from two independent samples

`financial-analysis--two-sample-pooled-variance@r1`

Source equation: `s_p^2=[(n1-1)s1^2+(n2-1)s2^2]/(n1+n2-2)`

Evaluator: `((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2)`

Locator: Learning Module6, Test Concerning Differences between Means with Independent Samples, printed p378 (PDF p388), unnumbered formula following Equation(5)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `n1` | input | Integer first-sample size at least2 | 1 |
| `n2` | input | Integer second-sample size at least2 | 1 |
| `v1` | input | First sample variance with n1-1 denominator | data-unit^2 |
| `v2` | input | Second sample variance with n2-1 denominator | data-unit^2 |
| `pooled` | output | Degrees-of-freedom-weighted estimate of a common population variance | data-unit^2 |

Translation: The weighted-mean structure has a distinct pooled-variance target, df bindings and U^2 units; no raw-data fitting or unknown parameters are solved. Inverse/special cases are not submitted separately.

Assumptions: For a common-variance interpretation the two populations have equal finite variance and samples are independent.; Normality is needed for exact pooled t inference, not for this arithmetic estimate. Both sample counts are integers>=2.

Limitations: This is not the sample variance of concatenated raw observations when group means differ; between-group variation is absent.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b16/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm).

## Independent two-mean t-statistic with common pooled variance

`financial-analysis--independent-two-mean-pooled-t-statistic@r1`

Source equation: `t=[(Xbar1-Xbar2)-(mu1-mu2)_0]/sqrt(s_p^2/n1+s_p^2/n2)`

Evaluator: `(mean1 - mean2 - delta) / sqrt(pooled / n1 + pooled / n2)`

Locator: Learning Module6, Test Concerning Differences between Means with Independent Samples, printed p378 (PDF p388), Equation(5)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `mean1` | input | First sample observed mean | data-unit |
| `mean2` | input | Second sample observed mean | data-unit |
| `delta` | input | Hypothesized first-minus-second population mean difference | data-unit |
| `pooled` | input | Strictly positive common variance estimate with df=n1+n2-2 | data-unit^2 |
| `n1` | input | Integer sample size>=2 | 1 |
| `n2` | input | Integer sample size>=2 | 1 |
| `t` | output | Signed pooled two-sample t-statistic | 1 |

Translation: The numerator is U and the denominator sqrt(U^2) isU, producing a dimensionless statistic. Null difference need not be0. NIST threshold discussion supplies that generalization.

Assumptions: Exact t distribution under the null requires two independent iid normal samples with a common positive population variance and a pooled sample variance.; Degrees of freedom are n1+n2-2; n1,n2 integer>=2.

Limitations: Paired observations require a difference-data one-sample test; unequal population variances require a different standard-error/df model.; P-values, quantiles and a decision rule are separate; this is no estimation algorithm.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b16/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm).

## Chi-square statistic for a normal population variance

`financial-analysis--normal-population-variance-chi-square-statistic@r1`

Source equation: `chi^2=(n-1)*s^2/sigma0^2`

Evaluator: `(n - 1) * variance / null_variance`

Locator: Learning Module6, Testing Concerning Tests of Variances, printed p384 (PDF p394), Equation(8)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `n` | input | Integer sample size>=2 | 1 |
| `variance` | input | Nonnegative sample variance with n-1 denominator | data-unit^2 |
| `null_variance` | input | Strictly positive null-boundary population variance | data-unit^2 |
| `chi_square` | output | Dimensionless variance test statistic with n-1df under the normal null | 1 |

Translation: Multiplying the sample variance byn-1 recovers the centered sum of squares; division by the nullU^2 cancels units. Allow variance0 as arithmetic boundary though exact constant samples have probability0 under a nondegenerate continuous normal model.

Assumptions: Source assumption: n independent observations from a normal population; underH0 the true variance equals the positive null variance.; Sample variance uses denominatorn-1; n integer>=2.

Limitations: This inference is sensitive to nonnormality.; A variance of returns measured in percentage points squared is not a return percentage; both variances must have the same squared scale.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b16/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda358.htm).

## Ordered two-sample variance ratio for an F-test

`financial-analysis--two-sample-variance-f-statistic@r1`

Source equation: `F=s1^2/s2^2`

Evaluator: `variance1 / variance2`

Locator: Learning Module6, Testing Concerning Tests of Variances, printed p388 (PDF p398), Equation(9)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `variance1` | input | Nonnegative first-sample variance, numerator population and sample size fixed externally | data-unit^2 |
| `variance2` | input | Positive second-sample variance, denominator population and sample size fixed externally | data-unit^2 |
| `F` | output | Ordered dimensionless sample variance ratio | 1 |

Translation: Both variances use identical U^2 units, so the ratio is dimensionless. It is an arithmetic statistic only; no Fquantile or posterior probability is implied.

Assumptions: Exact null distribution requires independent normal samples and equal positive population variances.; Bind the two sample counts n1,n2>=2 outside the arithmetic expression; Fdegrees of freedom are n1-1 andn2-1 in this order.

Limitations: Changing numerator to whichever variance is larger changes the statistic selection and requires corresponding tail/critical-value conventions. No automatic sorting is performed.; The null ratio need not be1 in a generalized variance-ratio test, which would require explicit rescaling; this source profile tests equality.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b16/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/eda/section3/eda359.htm).

## t-statistic for zero Pearson population correlation

`financial-analysis--zero-correlation-t-statistic@r1`

Source equation: `t=r*sqrt(n-2)/sqrt(1-r^2)`

Evaluator: `r * sqrt(n - 2) / sqrt(1 - r ** 2)`

Locator: Learning Module6, Tests Concerning Correlation, printed p395 (PDF p405), Equation(10)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `r` | input | Sample Pearson correlation strictly between-1 and1 | 1 |
| `n` | input | Integer number of independent observed pairs>=3 | 1 |
| `t` | output | Signed correlation statistic with n-2df under the joint-normal zero-correlation null | 1 |

Translation: All quantities are dimensionless. The magnitude denominator is positive for-1<r<1. Source t-statistic references for small-sample Spearman should not be interpreted as exact.

Assumptions: Exact Pearson null t distribution requires iid pairs from a jointly bivariate normal population with zero correlation, positive marginal variances and n>=3.; Source use for Spearman is an asymptotic approximation, not the same exact Pearson null law.

Limitations: Marginal normality alone does not imply joint normality.; Perfect sample correlations make the finite statistic singular; no infinite output is supplied.; No CDF or critical-value calculation is included.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b17/bundle.json). Corroboration: [R biotools: Pairwise Correlation t-Test](https://search.r-project.org/CRAN/refmans/biotools/html/multcor.test.html).

## Spearman correlation shortcut for untied ranks

`financial-analysis--spearman-correlation-without-ties@r1`

Source equation: `r_s=1-6*sum(d_i^2)/[n(n^2-1)]`

Evaluator: `1 - 6 * sum(q) / (len(q) * (len(q) ** 2 - 1))`

Locator: Learning Module6, Tests Concerning Correlation: Spearman Rank Correlation Coefficient, printed p397 (PDF p407), Equation(11)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `q` | family | Nonnegative squares of paired differences between two permutations of the ranks1..n; no ties | 1 |
| `r_s` | output | Spearman rank correlation for these untied paired ranks | 1 |

Translation: The integer6 comes from exact untied-rank sum-of-squares algebra. n is the family length and all quantities are dimensionless; no percent conversion. Guarded total imposes the feasible[-1,1] bound but is not a full rank-realizability check.

Assumptions: Application profile: neither original variable has ties; both rank lists are permutations1..n with the same paired ordering, n>=2.; Both variables must use the same increasing or decreasing rank convention. Squared rank differences are prebound.

Limitations: CFA preceding instructions allow average ranks for ties without restricting this shortcut; the general tied case instead needs Pearson correlation of the average ranks.; No sorting/rank-generation operator is provided. Family validity cannot be enforced by aggregate guards alone.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b17/bundle.json). Corroboration: [The Student's SEMSTAT](https://www.itl.nist.gov/div898/handbook/semstat/semstat-doc.pdf).

## Pearson chi-square statistic for a contingency table

`financial-analysis--categorical-pearson-chi-square-statistic@r1`

Source equation: `chi^2=sum_cells[(O_ij-E_ij)^2/E_ij]`

Evaluator: `sum(q)`

Locator: Learning Module6, Test of Independence Using Contingency Table Data, printed p400 (PDF p410), Equation(12)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `q` | family | One nonnegative squared count residual divided by positive expected count for every cell | 1 |
| `chi_square` | output | Uncorrected nonnegative Pearson contingency-table statistic | 1 |

Translation: All observation counts are dimensionless. Prebinding the complete cell contributions permits a sum without unsupported two-index mapping. Degrees of freedom have their own quantity definition; a sample-variance chi-square statistic is a distinct target.

Assumptions: Bind every cell exactly once, withE_ij>0 and expected counts based on the independence null; observed counts are nonnegative integers.; Chi-square reference distribution is an asymptotic approximation requiring suitable expected-cell sizes and the proper independent sampling design.

Limitations: No Yates continuity correction, structural-zero adjustment, exact test, or Monte Carlo p-value is included.; The finite-family guard cannot verify each bound contribution or the consistency of the original table margins.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b17/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm).

## Degrees of freedom for a full two-way independence table

`financial-analysis--contingency-independence-degrees-of-freedom@r1`

Source equation: `df=(r-1)(c-1)`

Evaluator: `(rows - 1) * (columns - 1)`

Locator: Learning Module6, Test of Independence Using Contingency Table Data, printed p400 (PDF p410), text following Equation(12)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `rows` | input | Integer number of nonempty row categories>=2 | 1 |
| `columns` | input | Integer number of nonempty column categories>=2 | 1 |
| `df` | output | Number of unconstrained cell deviations after estimating row/column margins | 1 |

Translation: Dimensionless category counts produce an integer count of independent deviations. This is not the number of cellsr*c.

Assumptions: Both category counts are integers>=2, margins are estimated, and no structural-zero or extra fitted-parameter constraints apply.

Limitations: Structural zeros, collapsed categories, or additional parameter fitting can change the degrees of freedom.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b17/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm).

## Pearson residual of an observed contingency-table cell

`financial-analysis--pearson-contingency-cell-residual@r1`

Source equation: `Pearson residual=(O_ij-E_ij)/sqrt(E_ij)`

Evaluator: `(observed - expected) / sqrt(expected)`

Locator: Learning Module6, Test of Independence Using Contingency Table Data, printed p402 (PDF p412), Equation(14)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `observed` | input | Nonnegative integer observed cell count | 1 |
| `expected` | input | Strictly positive expected cell count | 1 |
| `residual` | output | Signed observed-minus-expected count scaled by sqrt(expected) | 1 |

Translation: Counts are dimensionless, and the residual is a signed dimensionless diagnostic. Squaring and summing all such residuals recovers the uncorrected Pearson chi-square statistic.

Assumptions: Expected frequency must be strictly positive and correspond to this cell and sampling/null model.; Observed frequency is an integer>=0; expected need not be an integer.

Limitations: The book calls this standardized; it is the Pearson residual, which differs from the adjusted standardized residual using estimated cell variance.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b17/bundle.json). Corroboration: [R stats: Pearson Chi-squared Test for Count Data](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/chisq.test.html).

## Affine fitted response from supplied coefficients

`financial-analysis--supplied-affine-regression-response@r1`

Source equation: `Yhat_f=bhat0+bhat1*X_f`

Evaluator: `intercept + slope * x`

Locator: Learning Module7, Prediction Using Simple Linear Regression and Prediction Intervals, printed p461 (PDF p471), Equation(19)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `intercept` | input | Externally supplied fitted intercept | response-unit |
| `slope` | input | Externally supplied fitted slope in response units per predictor unit | response-unit/predictor-unit |
| `x` | input | Declared predictor value; no forecast is inferred | predictor-unit |
| `fitted` | output | Deterministic response on the supplied fitted line | response-unit |

Translation: YU+(YU/XU)*XU givesYU. Percentage-point examples are converted in the inputs and intercept, never by inlining conversion constants. The population stochastic relationYi=b0+b1Xi+epsilon_i is represented by this conditional mean plus an explicitly distinct error, not by puttingepsilon into a fittedYhat.

Assumptions: Coefficients are already supplied in units consistent with predictor and response; this is deterministic evaluation, not fitting.

Limitations: The value is conditional model output, not an investment forecast or advice. Extrapolation validity and coefficient uncertainty are separate.; A future realized response can differ by an error term; no unknown error is silently set to an observation.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b18/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm).

## Signed regression response residual

`financial-analysis--regression-response-residual@r1`

Source equation: `e_i=Y_i-Yhat_i`

Evaluator: `observed - fitted`

Locator: Learning Module7, Estimating the Regression Line, printed p433 (PDF p443), unnumbered residual equation

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `observed` | input | Observed response for one predictor value | response-unit |
| `fitted` | input | Response on the supplied fitted line at that same predictor value | response-unit |
| `residual` | output | Signed observed-minus-fitted response | response-unit |

Translation: Both response values areYU; subtraction preservesYU and the signed diagnostic. This is distinct from a standardized Pearson count residual.

Assumptions: Observed and fitted response belong to the same case, predictor value, response unit and fitted model.

Limitations: A sample residual is not the unobservable population error; fitted residuals are constrained and need not be mutually independent.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b18/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm).

## Regression sum of squared response deviations

`financial-analysis--regression-sum-of-squared-deviations@r1`

Source equation: `SSE=sum(e_i^2); SST=sum((Yi-Ybar)^2); SSR=sum((Yhat_i-Ybar)^2)`

Evaluator: `sum(q)`

Locator: Learning Module7, printed p430 (PDF p440) Equation(1); p434 (PDF p444) Equation(4); p448 (PDF p458) Equation(10)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `q` | family | One nonnegative squared response deviation per included observation; binding declares residual, observed-centered, or fitted-centered definition | response-unit^2 |
| `SS` | output | Sum of squared deviations for the explicitly declared SSE/SST/SSR convention | response-unit^2 |

Translation: A sum of response-unit squares hasYU^2. The algebraic accumulation is canonical across the three named sums; their respective centering definitions remain mandatory metadata.

Assumptions: Select one deviation definition and include every observation once; all terms are nonnegative squares with identical response units.; SSE, SST andSSR are distinct context-qualified uses of this single sum-of-squares relationship, not interchangeable ports.

Limitations: No fitted coefficients, means or residual terms are estimated by this expression. Elementwise square binding must be verified externally.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b18/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd431.htm).

## Coefficient of determination for an OLS model with intercept

`financial-analysis--regression-coefficient-of-determination@r1`

Source equation: `R^2=SSR/SST=1-SSE/SST`

Evaluator: `explained / total`

Locator: Learning Module7, Analysis of Variance, printed p449 (PDF p459), Equation(11)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `explained` | input | NonnegativeSSR=sum((Yhat-Ybar)^2) for this OLS fit | response-unit^2 |
| `total` | input | PositiveSST=sum((Y-Ybar)^2) for the same observations | response-unit^2 |
| `R2` | output | Fraction of centered response variation explained by this fit | 1 |

Translation: YU^2/YU^2 is dimensionless, reported as a fraction. In one-predictor OLS with interceptR2=rXY^2; the squared-correlation expression is an equivalent qualified form, not an extra record.

Assumptions: This profile uses ordinary least squares with an intercept on the same sample and response scale; SST=SSR+SSE andSST>0.

Limitations: Constant observed responses giveSST0 and undefined centeredR2. Out-of-sample, no-intercept, weighted or differently defined scores can have different ranges.; HighR2 alone does not establish model validity or causation.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b18/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm).

## Residual standard error of simple OLS with intercept

`financial-analysis--simple-regression-residual-standard-error@r1`

Source equation: `s_e=sqrt(MSE)=sqrt(SSE/(n-2))`

Evaluator: `sqrt(SSE / (n - 2))`

Locator: Learning Module7, ANOVA and Standard Error of Estimate, printed p451 (PDF p461), Equation(15)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `SSE` | input | Nonnegative residual sum of squares from the supplied fit | response-unit^2 |
| `n` | input | Integer sample size>=3 | 1 |
| `se` | output | Residual standard-deviation estimate after fitting an intercept and one slope | response-unit |

Translation: MSE=SSE/(n-2) hasYU^2 andits square root hasYU. Equation13 MSE is this relationship squared; no separate copy is submitted.

Assumptions: The supplied fit is full-rank unweighted OLS with an intercept and one varying predictor; two coefficients consume two degrees of freedom.; Homoskedastic zero-conditional-mean errors support interpreting this as an error-scale estimate; normal errors are needed for exact t/F inference.

Limitations: This usesn-2, unlike ordinary sampleSDn-1 or unadjustedRMSEn.; Perfect fit giveszero but cannot support tests that divide by this scale.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b18/bundle.json). Corroboration: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd431.htm).

## Simple-regression ANOVA F-statistic from sums of squares

`financial-analysis--simple-regression-anova-f-statistic@r1`

Source equation: `F=(SSR/1)/(SSE/(n-2))`

Evaluator: `SSR / (SSE / (n - 2))`

Locator: Learning Module7, Analysis of Variance, printed p450 (PDF p460), Equation(14)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `SSR` | input | Nonnegative explained sum of squares for this fitted sample | response-unit^2 |
| `SSE` | input | Strictly positive residual sum of squares for the same fitted sample | response-unit^2 |
| `n` | input | Integer sample size>=3 | 1 |
| `F` | output | Nonnegative model-slope test statistic with1,n-2df under a zero-slope null | 1 |

Translation: Both sums haveYU^2 and theirdf are dimensionless, so the ratio is dimensionless. MSR=SSR since one slope is fitted. For the same zero-slope hypothesisF=t_slope^2; it loses the sign and does not provide a directional test.

Assumptions: Full-rank unweighted OLS with an intercept and one varying predictor.; Exact F(1,n-2) law under zero slope requires conditionally independent homoskedastic normal errors with zero conditional mean.

Limitations: No model fitting, p-value or significance decision is performed.; A perfect fit withSSE0 makes the finite ratio undefined.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b19/bundle.json). Corroboration: [Applied Statistics in Agricultural and Life Sciences with R](https://psfaculty.plantsciences.ucdavis.edu/PLS120/PLS120Book/docs/chLinReg.html).

## Standard error of a supplied simple-regression slope estimate

`financial-analysis--simple-regression-slope-standard-error@r1`

Source equation: `s_bhat1=s_e/sqrt(sum((Xi-Xbar)^2))`

Evaluator: `se / sqrt(Sxx)`

Locator: Learning Module7, Hypothesis Testing of Linear Regression Coefficients, printed p453 (PDF p463), Equation(17)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `se` | input | Nonnegative residual standard error | response-unit |
| `Sxx` | input | Strictly positive centered predictor sum of squares | predictor-unit^2 |
| `slope_se` | output | Estimated standard deviation of the fitted slope | response-unit/predictor-unit |

Translation: YU/sqrt(XU^2)=YU/XU,matching slope units. UC Davis Equation13.4 has sqrt(MSE/Sxx);s_e=sqrt(MSE) is the exact translation.

Assumptions: Homoskedastic uncorrelated zero-conditional-mean errors and a full-rank simple OLS design;Sxx>0.; The fitted summaries are supplied; no coefficient is estimated here. Exact finite-sample inference additionally needs normal errors.

Limitations: Heteroskedastic or correlated errors need different covariance estimators.; Nonvarying predictors haveSxx0 and cannot identify a slope.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b19/bundle.json). Corroboration: [Applied Statistics in Agricultural and Life Sciences with R](https://psfaculty.plantsciences.ucdavis.edu/PLS120/PLS120Book/docs/chLinReg.html).

## t-statistic for a supplied regression coefficient estimate

`financial-analysis--supplied-regression-coefficient-t-statistic@r2`

Source equation: `t=(bhat_j-B_j)/s_bhat_j`

Evaluator: `(estimate - null_value) / coefficient_se`

Locator: Learning Module7, Hypothesis Testing of Linear Regression Coefficients, printed p453 (PDF p463), Equation(16); intercept counterpart p456/PDF466

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `estimate` | input | Supplied coefficient estimate; bind intercept or slope units consistently | coefficient-unit |
| `null_value` | input | Null-boundary value of that same coefficient | coefficient-unit |
| `coefficient_se` | input | Strictly positive valid estimated standard error of that coefficient | coefficient-unit |
| `t` | output | Signed coefficient test statistic; simple-regressiondf=n-2 bound externally | 1 |

Translation: All three coefficient-valued ports share one explicitly declared unit Uc. Uc is response-unit YU for an intercept or response-unit/predictor-unit YU/XU for a slope, selected uniformly before binding. (Uc-Uc)/Uc is dimensionless. This r2 replaces r1 placeholder response-unit metadata; arithmetic, source locator and independent reference oracles are unchanged. The null port is a coefficient hypothesis and the denominator its estimation uncertainty, not an observation population scale.

Assumptions: Coefficient estimate, null and standard error refer to the same coefficient, model, units and covariance estimator.; Declared generic coefficient-unit binding isYU forintercept orYU/XU forslope; all three must match.; For exact simple-OLS t(n-2) inference require the classical conditional normal error assumptions andn>=3.

Limitations: A supplied erroneous standard error invalidates inference; CFA Equation18 intercept standard error is separately flagged and must not be used as a verified input.; No p-value or model validity probability is returned.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b23/bundle.json). Corroboration: [Applied Statistics in Agricultural and Life Sciences with R](https://psfaculty.plantsciences.ucdavis.edu/PLS120/PLS120Book/docs/chLinReg.html).

## Standard error for a new individual regression response

`financial-analysis--simple-regression-individual-prediction-standard-error@r1`

Source equation: `s_f=s_e*sqrt(1+1/n+(Xf-Xbar)^2/Sxx)`

Evaluator: `se * sqrt(1 + 1 / n + (x - xmean) ** 2 / Sxx)`

Locator: Learning Module7, Prediction Using Simple Linear Regression and Prediction Intervals, printed p461 (PDF p471), Equation(20)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `se` | input | Nonnegative residual standard error | response-unit |
| `n` | input | Integer size of fitting sample>=3 | 1 |
| `x` | input | Specified predictor value for a new independent response | predictor-unit |
| `xmean` | input | Predictor mean of the fitting sample | predictor-unit |
| `Sxx` | input | Positive predictor centered sum of squares of that fitting sample | predictor-unit^2 |
| `prediction_se` | output | Estimated scale of prediction error for one new response | response-unit |

Translation: All terms in the radical are dimensionless;output hasYU. The variance expression is its square,not a separate clone. Sxx=(n-1)*sample_predictor_variance is the equivalent source denominator.

Assumptions: One new response independent of the fitting sample at a known predictor value, same homoskedastic linear conditional-mean model and positiveSxx.; Fitting includes an intercept and one slope;integern>=3. Normal errors support exact t prediction intervals.

Limitations: A confidence interval for the conditional mean excludes the leading1; its target differs from predicting an individual.; Predictor measurement uncertainty, model-selection uncertainty and extrapolation errors are absent.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b19/bundle.json). Corroboration: [Applied Statistics in Agricultural and Life Sciences with R](https://psfaculty.plantsciences.ucdavis.edu/PLS120/PLS120Book/docs/chLinReg.html).

## Back-transformed response of a supplied log-linear regression

`financial-analysis--supplied-log-linear-regression-response@r1`

Source equation: `log(Y)=b0+b1*X; Y=exp(b0+b1*X)`

Evaluator: `exp(a + b * x)`

Locator: Learning Module7, The Log-Lin Model, printed pp465-466 (PDF pp475-476), Equation(22) and antilog example

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `a` | input | Supplied intercept for log of normalized response | 1 |
| `b` | input | Supplied coefficient per predictor unit | 1/predictor-unit |
| `x` | input | Specified predictor value in coefficient-matching units | predictor-unit |
| `Y` | output | Positive normalized response obtained by exponentiating the fitted log response | 1 |

Translation: aandb*xare dimensionless. Output isY/Yref; multiply by the separately bound reference quantity to recover dimensional response. No log of dimensional money is taken. Exact relative change acrossdelta_xisexp(b*delta_x)-1; slope-times-change is only local approximation.

Assumptions: The log response refers toY/Yref;Yref is a fixed positive reference quantity and coefficients were fitted under that normalization.; Coefficients are supplied, not estimated. The predictor may be signed when meaningful in its declared context.

Limitations: Exponentiating a fitted conditional log mean gives a geometric mean; it is a conditional median under lognormal errors, not an unbiased arithmetic-mean prediction.; Arithmetic-mean retransformation needs an error-distribution correction, absent here.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b20/bundle.json). Corroboration: [FAQ: How do I interpret a regression model when some variables are log transformed?](https://stats.oarc.ucla.edu/other/mult-pkg/faq/general/faqhow-do-i-interpret-a-regression-model-when-some-variables-are-log-transformed/).

## Response of a supplied linear-log regression

`financial-analysis--supplied-linear-log-regression-response@r1`

Source equation: `Y=b0+b1*log(X)`

Evaluator: `a + b * log(x)`

Locator: Learning Module7, The Lin-Log Model, printed p466 (PDF p476), Equation(23)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `a` | input | Supplied response intercept at normalized predictor1 | response-unit |
| `b` | input | Supplied response-unit coefficient per unit natural log of predictor | response-unit |
| `x` | input | Positive predictor ratioX/Xref under the fitting normalization | 1 |
| `Y` | output | Signed response on the supplied linear-log curve | response-unit |

Translation: log(x)is dimensionless;aandbare response-valued. Exact response difference isb*log(x2/x1). A small relative changegproduces approximatelyb*g, but no approximation is embedded.

Assumptions: x=X/Xref>0 with fixed referenceXref; coefficients use that same normalization and response unit.; No regression estimation or model-selection step is performed.

Limitations: The response can be negative; logging the predictor does not impose positivity on the response.; Extrapolation and statistical uncertainty remain outside this deterministic evaluation.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b20/bundle.json). Corroboration: [FAQ: How do I interpret a regression model when some variables are log transformed?](https://stats.oarc.ucla.edu/other/mult-pkg/faq/general/faqhow-do-i-interpret-a-regression-model-when-some-variables-are-log-transformed/).

## Back-transformed response of a supplied log-log regression

`financial-analysis--supplied-log-log-regression-response@r1`

Source equation: `log(Y)=b0+b1*log(X); Y=exp(b0)*X^b1`

Evaluator: `exp(a) * x ** b`

Locator: Learning Module7, The Log-Log Model, printed p468 (PDF p478), Equation(24)

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `a` | input | Supplied log-response intercept at normalized predictor1 | 1 |
| `b` | input | Supplied constant elasticity coefficient | 1 |
| `x` | input | Positive normalized predictorX/Xref | 1 |
| `Y` | output | Positive normalized back-transformed responseY/Yref | 1 |

Translation: Positive dimensionlessxpermits arbitrary finite real elasticityb. All logs/exponents are dimensionless; outputY/Yrefis dimensionless. Exact response ratio for predictor ratioqisq^b; b times a finite percent change is generally only approximate.

Assumptions: Both original variables are positive and divided by fixed positive reference quantities before logging; normalization matches supplied coefficients.; Coefficients are already supplied.

Limitations: Back-transformed fitted log mean is a geometric mean; normal log errors additionally make it a conditional median. It is not the conditional arithmetic mean without correction.; ComparingR2between different response transformations is not a direct like-for-like fit comparison.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b20/bundle.json). Corroboration: [FAQ: How do I interpret a regression model when some variables are log transformed?](https://stats.oarc.ucla.edu/other/mult-pkg/faq/general/faqhow-do-i-interpret-a-regression-model-when-some-variables-are-log-transformed/).

## Forward price-to-earnings ratio

`financial-analysis--forward-price-earnings-ratio@r1`

Source equation: `Forward P/E=share price/projected EPS`

Evaluator: `price / eps`

Locator: Learning Module2, Measures of Central Tendency, printed p115 (PDF p125), Example13 introduction and Exhibit42

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `price` | input | Nonnegative price per share at the declared valuation date | currency/share |
| `eps` | input | Nonzero projected earnings per share for the explicitly declared upcoming annual reporting period | currency/share |
| `pe` | output | Price relative to projected annual earnings per share | 1 |

Translation: Price and annual-window earnings per share are both currency/share amounts, yielding a dimensionless annual-earnings multiple under dimensionless financial-period convention; never convert years to seconds.

Assumptions: Price and projected EPS use the same currency, share class and split/share convention. EPS belongs to a named future annual reporting window.; Positive-earnings valuation interpretation requireseps>0; the broader arithmetic definition permitseps<0 with explicit loss meaning.

Limitations: EPS0 makes the ratio undefined. A projected earnings input is supplied, not forecast here.; This is not a trailingP/E or a recommendation. Different forward windows must not be mixed.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b21/bundle.json). Corroboration: [Forward P/E Ratio](https://corporatefinanceinstitute.com/resources/valuation/forward-pe-ratio/).

## Trailing EBITDA interest-expense coverage ratio

`financial-analysis--trailing-ebitda-interest-coverage@r1`

Source equation: `Interest coverage=trailing-four-quarter EBITDA/interest expense`

Evaluator: `ebitda / interest`

Locator: Learning Module4, Discrete and Continuous Uniform Distribution, printed p245 (PDF p255), Example2 covenant definition

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `ebitda` | input | Signed earnings before interest,taxes,depreciation andamortization over the four-quarter window | currency |
| `interest` | input | Strictly positive interest expense matched to that same four-quarter coverage window and covenant definition | currency |
| `ratio` | output | EBITDA coverage of matching interest expense | 1 |

Translation: Currency/currency cancels. Trailing-four-quarter EBITDA is the numerator scope explicitly named in the source; matching interest-period scope is required to use the ratio consistently. The projected charges in the example are treated as a supplied constant at the covenant check.

Assumptions: EBITDA and interest expense use one currency, reporting entity, trailing window and covenant-specific scope.; Positive expense magnitude is the CFA convention; source-specific debt/lease adjustments require explicit binding.

Limitations: This EBITDA-based definition differs from EBIT-based times-interest-earned.; TradingView product documentation separately filters expense signs; its data-feed convention is not imported into the CFA positive-expense model.; A covenant threshold is contract-specific, not a universal2constant.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b21/bundle.json). Corroboration: [EBITDA interest coverage](https://my.tradingview.com/support/solutions/43000734816/).

## Periodic weighted-average inventory unit cost

`financial-analysis--periodic-weighted-average-inventory-unit-cost@r1`

Source equation: `Average unit cost=cost of goods available/units available`

Evaluator: `cost / units`

Locator: Learning Module7, practice solution39, printed p492 (PDF p502), unnumbered weighted-average inventory calculation

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `cost` | input | Nonnegative total cost of goods available in this periodic inventory pool | currency |
| `units` | input | Positive count of homogeneous goods available,including beginning inventory and period additions | item |
| `unit_cost` | output | Average cost assigned per item in this periodic pool | currency/item |

Translation: Currency divided byitem count givescurrency/item. Both dimensions are explicit; raw lot quantities/costs are aggregated before this record. No source currency symbol determines an implicit FXconversion.

Assumptions: Periodic cost pool for homogeneous interchangeable units; availablecost andcount cover the same beginning balance and additions under the declared accounting policy.; Application boundary: nonnegative total available cost and positiveunits.

Limitations: This is a periodic average, not the moving average after each perpetual-system purchase.; CFApractice39 points to Question8, which is an unrelated ANOVA problem. The solution is therefore treated as an isolated worked example, not evidence of the missing full inventory fact pattern.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b21/bundle.json). Corroboration: [Principles of Accounting, Volume1: Financial Accounting](https://openstax.org/books/principles-financial-accounting/pages/10-2-calculate-the-cost-of-goods-sold-and-ending-inventory-using-the-periodic-method).

## Cost of goods sold under a supplied periodic average unit cost

`financial-analysis--periodic-average-cost-of-goods-sold@r1`

Source equation: `COGS=periodic average unit cost*units sold`

Evaluator: `unit_cost * sold`

Locator: Learning Module7, practice solution39, printed p492 (PDF p502), final weighted-average cost-of-goods-sold multiplication

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `unit_cost` | input | Nonnegative average cost per item for the declared periodic inventory pool | currency/item |
| `sold` | input | Nonnegative item count sold from that pool,not exceeding availableunits | item |
| `cogs` | output | Cost allocated to the sold items under that periodic average | currency |

Translation: Currency/item multiplied byitem givescurrency. Quantity can be a counted or continuously measured homogeneous item convention,as declared consistently. CFAquestion cross-reference is broken; only the directly displayed worked allocation is asserted.

Assumptions: The unit cost is the valid periodic average for the same homogeneous inventory pool; sold quantity belongs to that period and pool.; Bind available inventory externally and verify0<=sold<=available units; the engine cannot check an unavailable port.

Limitations: Sales revenue and selling price do not enter this cost allocation.; No perpetual moving-average update, tax rule or currency conversion is implied.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b21/bundle.json). Corroboration: [Principles of Accounting, Volume1: Financial Accounting](https://openstax.org/books/principles-financial-accounting/pages/10-2-calculate-the-cost-of-goods-sold-and-ending-inventory-using-the-periodic-method).

## Benjamini-Hochberg critical value at a supplied ordered rank

`financial-analysis--benjamini-hochberg-rank-critical-value@r1`

Source equation: `BHcritical_i=alpha*i/m`

Evaluator: `alpha * rank / tests`

Locator: Learning Module6, Multiple Tests and Significance Interpretation, printed pp370-372 (PDF pp380-382), displayed rank criterion and Exhibits12,14

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `alpha` | input | TargetFDRlevel in[0,1] | 1 |
| `rank` | input | Integer ordered rank1..m; p-values sorted ascending externally | 1 |
| `tests` | input | Positive integer total number of hypotheses in the prespecified family | 1 |
| `critical` | output | Rank-specific probability threshold,not an adjusted p-value | 1 |

Translation: All quantities are dimensionless. The alpha port is a targetFDR rather than an observation probability. No automatic multiple-test decision is returned, and a single failed comparison does not imply stopping the step-up search.

Assumptions: Rank and family size are integers with1<=rank<=tests; all p-values belong to one prespecified complete testfamily.; FDR control needs the appropriate independent/positive-dependence assumptions of BH; arbitrary dependent families need a qualified alternative.

Limitations: Sorting, selecting the largest passing rank, and rejecting all ranks up to that index are separate algorithmic steps,not performed here.; CFA calls these adjusted p-values in Exhibit14; they are critical values.; FDR is expected false discoveries among rejections,not the unconditional per-test false-positive probability.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b22/bundle.json). Corroboration: [R mutoss: Benjamini-Hochberg linear step-up procedure](https://search.r-project.org/CRAN/refmans/mutoss/html/BH.html).

## Gross profit amount from net sales and cost of sales

`financial-analysis--income-statement-gross-profit@r1`

Source equation: `Gross profit=net sales-cost of sales`

Evaluator: `sales - cost`

Locator: Learning Module2, Data Types, printed p66 (PDF p76), Exhibit3 Condensed Consolidated Statements of Operations

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `sales` | input | Signed net sales revenue after relevant returns/allowances | currency |
| `cost` | input | Cost of sales for the same sold goods/services,positive when deducted | currency |
| `gross_profit` | output | Gross profit or gross margin amount before separately reported operating expenses | currency |

Translation: Currency minuscurrency givescurrency. CFA values stated in millions are normalized in reference inputs only; no unit conversion factor is embedded.

Assumptions: Both amounts cover the same entity, period, currency and revenue/cost recognition basis. Cost uses a deduction-positive sign.

Limitations: Gross margin here is an amount,not gross margin percentage.; This is the line-item subtotal for the displayed statement scope; detailed recognition/accounting policies are not inferred.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b22/bundle.json). Corroboration: [Beginners' Guide to Financial Statement](https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide).

## Operating income from gross profit and operating expenses

`financial-analysis--income-statement-operating-income@r1`

Source equation: `Operating income=gross profit-total operating expenses`

Evaluator: `gross_profit - expenses`

Locator: Learning Module2, Data Types, printed p66 (PDF p76), Exhibit3 operating-expense and operating-income lines

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `gross_profit` | input | Gross profit after cost of sales | currency |
| `expenses` | input | Complete operating expenses separately deducted after gross profit; includes all applicable R&D,SG&A,depreciation within that presentation scope | currency |
| `operating_income` | output | Signed income from operations | currency |

Translation: This preserves source statement presentation: R&DplusSG&Aare the shown separately reported expense components. Different presentations may classify depreciation differently;the externally bound complete expense aggregate must respect that scope.

Assumptions: The expense aggregate contains all and only operating expenses deducted after this gross profit; do not duplicate costs already included in cost of sales.; Entity,currency,period and recognition basis match.

Limitations: Operating income does not include separately presented nonoperating income/expense or income tax.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b22/bundle.json). Corroboration: [Beginners' Guide to Financial Statement](https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide).

## Net income from pretax income and income tax expense

`financial-analysis--income-statement-net-income-after-tax@r1`

Source equation: `Net income=income before income taxes-income tax provision`

Evaluator: `pretax - tax`

Locator: Learning Module2, Data Types, printed p66 (PDF p76), Exhibit3 final three income-statement lines

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `pretax` | input | Signed pretax income for this complete statement scope | currency |
| `tax` | input | Signed income-tax provision:positive for expense,negative for benefit | currency |
| `net_income` | output | Signed income after the specified tax provision | currency |

Translation: Both inputs and output are currency amounts; signed tax benefits are preserved. No effective-tax-rate denominator is invented from one displayed statement.

Assumptions: Pretax and tax amounts share the entity,currency,period and operations scope.; The presented scope has no additional separately deducted post-tax/discontinued/minority lines between the named pretax and net totals.

Limitations: This does not estimate a tax rate or apply tax law; deferred/current components must already be included in the provision.; Attributing income to owners/noncontrolling interests requires separate explicitly supplied scope.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b22/bundle.json). Corroboration: [Beginners' Guide to Financial Statement](https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide).

## Price-to-book-equity ratio

`financial-analysis--price-book-equity-ratio@r1`

Source equation: `P/B=share market price/book equity per share`

Evaluator: `price / book_per_share`

Locator: Learning Module5, Sample Selection Bias, printed p338 (PDF p348), explicit parenthetical price-to-book definition; Look-Ahead Bias p339/PDF349

| Symbol | Role | Meaning | Unit |
|---|---|---|---|
| `price` | input | Nonnegative market price per share at the declared date | currency/share |
| `book_per_share` | input | Nonzero book equity attributable to that share class per matching share | currency/share |
| `pb` | output | Signed price relative to matching book equity per share | 1 |

Translation: The two currency/share ports cancel to a dimensionless multiple. Market cap/book equity is equivalent only if share/equity attribution and share counts match. It is distinct from forwardP/E because its denominator is a point-in-time book-equity stock,not future earnings flow.

Assumptions: Market price and book equity per share use the same currency,share class,share adjustments and entity scope.; Application boundary: nonnegative price and nonzero book equity per share; positive-book interpretation additionally needs positivebook equity.; For backtests use book-equity data only after the actual publication date; fiscal period-end is not an information-availability date.

Limitations: Book equity is an accounting measurement,not a guaranteed liquidation price or intrinsic value.; Zero book equity makes the ratio undefined;negative book equity changes interpretation.; No valuation or trading recommendation follows from the quotient.

[Complete record and reference cases](financial-analysis-cfa-l1-b1-b24/bundle.json). Corroboration: [Market to Book Ratio](https://corporatefinanceinstitute.com/resources/valuation/market-to-book-ratio-price-book/).

