# Deferred, overlap and source-review register

This is the append-only historical investigation record. A deferred entry can describe an overlap, an unsupported operator, an apparent source error, or work that was subsequently completed. It is not a count of unique omitted formulas.

Later resolutions: financial ratios and inventory cost were completed in b21; BH critical line in b22; regression diagnostics in b18–b20. The general F realization ratio and distribution qualification remain deferred. b23 supersedes one b19 coefficient-unit revision without adding a unique model.

## financial-analysis-cfa-l1-b1-b01

### Discrete lump-sum FV, PV, growth-rate and time rearrangements

LM1 printed pp6-11,17-20,29-32/PDF16-21,27-30,39-42, Eqs1-3,8-9,14 and Example19 overlap engineering-finance--lump-sum-future-value-discrete. Algebraic inverses are not new models.

### Discrete periodic and effective rates

LM1 printed pp11,14/PDF21,24 Eq5 overlaps engineering-finance--periodic-rate-from-nominal and engineering-finance--effective-annual-rate-nominal.

## financial-analysis-cfa-l1-b1-b02

### Ordinary-annuity present value

LM1 printed p21/PDF31 Eqs10-11 overlaps supplied runtime ID uniform-present-value and the inverse of engineering-finance--level-loan-periodic-payment. Keep exact locator as additional evidence; no new clone.

### Level perpetuity

LM1 printed p26/PDF36 Eqs12-13 is the zero-growth case of engineering-finance--constant-growth-stock-present-value; deferred as overlap, with source support for general level cash-flow meaning.

### Annuity due, ordinary-annuity future value and payment inversions

LM1 printed pp15-16,22-24,33-37/PDF25-26,32-34,43-47 Eq7 and Eq11 inversions overlap engineering-finance--ordinary-annuity-future-value, engineering-finance--annuity-due-present-value and engineering-finance--level-loan-periodic-payment.

### Arbitrary dated cash-flow vectors without prevaluation

LM1 printed pp16,25/PDF26,35 Exhibits5,10: sum(CF_t*(1+r)^(T-t)) or sum(CF_t/(1+r)^t). Full vector expression requires aligned elementwise transformations, unavailable in the scalar grammar. Covered individual accumulation plus cash-flow-value-additivity compose once same-date values are prepared.

## financial-analysis-cfa-l1-b1-b04

### Median, mode, trimmed and winsorized means on raw arrays

LM2 printed pp104-107/PDF114-117: median selects ranked central values; mode selects maximal frequency; trimmed/winsorized means sort, select or clamp observations. These need sorting/indexing/selection or piecewise family operations beyond current scalar grammar. Arithmetic mean over already prepared data remains covered.

### Claim that arithmetic mean times harmonic mean equals geometric mean squared

LM2 printed p115/PDF125 states A*H=G^2 without restricting sample size. It holds for two positive observations, not in general. Counterexample[1,2,8]:A*H=88/13~6.76923, whileG^2=16^(2/3)~6.34960. Preserve as a source error for review; no false general model returned.

### Weighted-mean Example9 Year1 arithmetic discrepancy

LM2 printed p109/PDF119 gives10.50%, but its displayed weights(.25,.45,.30) and returns(5.3%,12.7%,11.5%) sum to10.49%. The completed weighted-mean record uses the consistent Year2 published result instead; no oracle tolerance was widened to conceal this discrepancy.

## financial-analysis-cfa-l1-b1-b07

### Arithmetic/geometric mean minus half-variance approximation

LM2 printed pp127-128/PDF137-138 gives R_G approximately arithmetic mean-s^2/2. Source example contrasts3.1566% with approximate3.1338%. Exact approximation/error regime beyond small returns and leading variance is not supplied; queue corroboration and approximation-scope review before a completed record.

### Sample correlation worked-example transcription inconsistencies

LM2 printed p142/PDF152 Exhibit54 gives5.7318 but adjacent prose gives5.7138 for the A/B covariance; printed p143/PDF153 discusses A/C then namesFundB. Completed correlation record uses exact constructed checks and the unambiguous Eq15, not these inconsistent labels.

## financial-analysis-cfa-l1-b1-b08

### Odds-against worked example inconsistency

LM3 printed p177/PDF187 correctly prints probability=b/(a+b) for odds againsta:b, then gives1/(4+1)=.20 for odds against1:4. The correct event probability is4/5=.80. Preserve source error; completed odds record follows the symbolic definition.

### Equally likely and empirical probability from counts

LM3 printed pp175-176/PDF185-186 ratio favorable/total is the relative-frequency/count-ratio relationship already curated. Applicability differs:equal-likelihood assumptions are needed for a priori probability, and stability assumptions for empirical extrapolation. No cloned arithmetic record.

## financial-analysis-cfa-l1-b1-b09

### Discrete expectation, conditional expectation and iterated expectation

LM3 printed pp191,193-194/PDF201,203-204 Eqs7,10-12 are normalized-weighted-mean relationships using probabilities and possibly scenario-conditional means. Preserve distinct expectation semantics through input/output binding contexts; no resubmitted sum-of-weighted-values clone.

### Portfolio mean return and expected product under zero covariance

LM3 printed p197/PDF207 Eq13 is the curated normalized-weighted-mean relationship. Printed p204/PDF214 E(XY)=E(X)E(Y) under zero covariance follows the joint covariance definition with cov0; record as qualified inverse/overlap evidence, not a new equation clone.

## financial-analysis-cfa-l1-b1-b10

### Factorial, r-permutations, combinations and covariance-entry counts

LM3 printed pp213-216/PDF223-226: factorial and Eq23 permutations are special branch products in sequential-counting-product; Eq22 combinations are the two-label multinomial case. Printed p199/PDF209 n(n-1)/2 distinct off-diagonal covariances is nC2; n diagonal variances and n^2 ordered matrix entries are counting specializations. Exact source locators retained without equation clones.

### Equal-prior Bayesian prose overgeneralization

LM3 printed p211/PDF221 says equal priors make likelihood and posterior equal. That only follows in its specific example where likelihoods sum to1; it is not a general property of diffuse priors. Bayes record retains the explicit evidence denominator.

## financial-analysis-cfa-l1-b1-b11

### Discrete uniform PMF and cumulative sum

LM4 printed pp241-243/PDF251-253:in-support massp(x)=1/n is the equal-likelihood one-outcome special case of the existing favorable-count/total relationship; CDF accumulates masses for outcomes<=x, a disjoint probability sum. Full raw-support filtering and outside-support branches require selection; source evidence retained without arithmetic clones.

### General continuous probability integral

LM4 printed p244/PDF254 Eq1:P(a<=X<=b)=integral_a^b f(x)dx. Arbitrary density integration is not an available scalar operator; retain as deferred, with analytic uniform cases curated separately.

## financial-analysis-cfa-l1-b1-b12

### Financial ratios embedded in distribution examples

LM4 printed p245/PDF255 defines trailing-four-quarter EBITDA/interest coverage. LM2 printed p115/PDF125 defines forwardP/E as price per share/projectedEPS. Both are candidates for a later financial-ratio batch with precise numerator/denominator context; not yet curated.

### Binomial CDF and degenerate PMF endpoints

LM4 printed pp249-251/PDF259-261 computes cumulative binomial masses by summation. A prebound probability-family sum is supported, but generation and filtering bysuccesscount require additional operators. Endpointp0orp1 follows deterministic branches; no0^0 convention is silently used.

## financial-analysis-cfa-l1-b1-b13

### Normal/lognormal CDFs, quantiles and shortfall risk probabilities

LM4 printed pp258-265/PDF268-275 usesnormalCDFPhiandinversePhi;shortfall probabilityPhi(-SFRatio)and normalVaRquantiles require those unavailable operators. Density,standardization andSFRare curated without substituting an approximation.

### Normality of arbitrary sums requires joint normality or independence

LM4 printed p255/PDF265 says a linear combination of normal variables is normal without qualifying joint normality; printed p256/PDF266 correctly discusses jointly normal returns. Preserve the stronger required joint condition in any derived distribution claim.

## financial-analysis-cfa-l1-b1-b14

### Single-period log return is an existing continuous-growth inverse

LM4 printed p269/PDF279 Equation6:r=log(S1/S0)=log(1+R). It is the one-period inverse of batch01 continuous accumulation/effective annual rate, so no rearrangement clone.

### Monte Carlo stock increment has an unresolved time-scale convention

LM4 printed p283/PDF293 Step3 prints deltaS=mu*S*delta_t+sigma*S*Z withZ standard normal, omitting sqrt(delta_t) from the diffusion term while naming sigma a standard deviation. No period-specific sigma convention is supplied. Defer rather than silently repair or claim standard GBM corroboration.

### Simulation generation, Asian/lookback/put payoff paths and inverse transformation

LM4 printed pp280-285/PDF290-295 and practice p288/PDF298: positive-part payoffs and path minima require unsupported branching/minimum, random generation/inverseCDF unavailable. Average already-discounted simulation values uses arithmetic-mean; terminal discounting uses existing TVM. No approximation inserted.

### F realization ratio pending qualified distribution evidence

LM4 printed p274/PDF284:F=(chi1_squared/m)/(chi2_squared/n). Distribution assertion requires independent chi-square numerator and denominator; the local sentence omits independence. Queue complete qualified record with LM6 variance-ratio material.

## financial-analysis-cfa-l1-b1-b15

### Bootstrap standard error overlaps sample standard deviation of bootstrap estimates

LM5 printed p333/PDF343 Equation7:SE_boot=sqrt(sum[(theta_b-theta_bar)^2]/(B-1)). Apply sample-variance then sample-standard-deviation-from-variance with bootstrap-estimate context. Generation of resamples is unavailable; do not relabel ordinary observation SD as meanSE.

### Sharpe ratio and sampling count examples are qualified overlaps

LM5 printed pp313-314/PDF323-324 Sharpe ratio is safety-first ratio with risk-free threshold; Example1 printed p307/PDF317 product3*10*2 counts strata using sequential-counting-product. No new algebraic copies.

### Sample-size selection with t-critical dependence is not a closed-form solver

LM5 printed p331/PDF341:n=[t*s/E]^2. With externally fixed critical and scale this is the inverse confidence half-width formula. Choosing t for unknownn may require iteration, outside assignment; ceil/integer-roundup unavailable. NIST7.2.2.2 explicitly discusses this dependence.

- [Inspected or attempted source](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm)

### Signed sampling error and estimator bias need independent exact-definition corroboration

LM5 printed p306/PDF316 defines signed error statistic-minus-parameter; p321/PDF331 defines bias by expectation-minus-parameter. Preserve distinct realized error and repeated-sampling bias. OpenStax1.2 explains sampling error but does not directly state the signed identity; leave pending rather than overclaim corroboration.

## financial-analysis-cfa-l1-b1-b16

### Source variance-unit and example transcription issues

LM6 printed p386/PDF396 describes variance16 as16%; it is16 squared-percentage-point units, equivalent to.0016 in decimal-return-squared units. Printed p367/PDF377 Example4 critical value changes2.345 to2.245 in solution. Printed p377/PDF387 norm.ppf(.975,23) incorrectly adds a location23. Preserve formulas with consistent units; do not reproduce erroneous software calls.

## financial-analysis-cfa-l1-b1-b17

### Ties and approximate Spearman tests require stronger qualification

LM6 printed pp397-398/PDF407-408 combines tied average ranks with a no-ties shortcut and treats a t transform for n>30 as if exact. General tied Spearman uses Pearson of ranks; significance approximation accuracy depends on sample/data, not a universal30 threshold. SciPy spearmanr notes asymptotic p-value accuracy only for very large samples, suggesting permutation for smaller ones.

- [Inspected or attempted source](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html)

### BH significance line and multiple-testing source terminology pending

LM6 printed pp370-372/PDF380-382 thresholdalpha*i/m is not an adjusted p-value, despite Exhibit14 labeling. FDR isE[V/max(R,1)], not simply unconditional false-positive fraction. Sorting and selecting maximum passing index are unsupported; scalar threshold can be curated with direct algorithm evidence in a later batch.

## financial-analysis-cfa-l1-b1-b18

### OLS coefficient estimation formulas excluded by assignment boundary

LM7 printed p434/PDF444 Equation5:b1=Sxy/Sxx; printed p435/PDF445 Equation6:b0=Ybar-b1*Xbar. These are closed-form estimators but assignment explicitly defers regressions needing estimation. Retain exact formulas and locators here, without claiming a fitting runtime. Independent corroboration NIST4.4.3.1 inspected.

- [Inspected or attempted source](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd431.htm)

### Regression source errors: fitted-response notation, randomness and intercept uncertainty

LM7 p434/PDF444 Exhibit5 uses a minus slope inside residual brackets; Eq4 uses correct plus. p435/PDF445 andp437/PDF447 attach epsilon toYhat; fitted response has no unknown population error. p441/PDF451 incorrectly says randomXprecludes linearity. p444/PDF454 equates uncorrelatedness with independence. Eq18 p456/PDF466 omits residual-scales_e in interceptSE and example thus uses wrong uncertainty; defer original formula rather than silently repair.

## financial-analysis-cfa-l1-b1-b19

### ANOVA decomposition, mean squares and prediction endpoints are qualified equivalent forms

LM7 p448/PDF458:SST=SSR+SSE. Combined with R2=SSR/SST gives same relationshipR2=1-SSE/SST; retained inR2translation rather than cloned. p450/PDF460 MSR=SSR/1,MSE=SSE/(n-2); retained withF/SEE. Eq21 p461/PDF471:Yhat+/-tcritical*sf has same symmetric-offset arithmetic as confidence-bound but target is an individual future response,dfn-2andscale predictionSE; requires explicit output-quantity binding,never call it mean-confidence bound.

### Incorrect intercept formula independently corroborated as missing scale

CFA Eq18 p456/PDF466 prints onlysqrt(1/n+Xbar^2/Sxx). UC Davis Eq13.7 prints sqrt(MSE*(1/n+Xbar^2/Sxx)),confirming the missing residual scale. The CFAexample claimingt2.73475andrejection is unsupported; do not accept that inference. General coefficientt remains usable only with a valid suppliedSE.

- [Inspected or attempted source](https://psfaculty.plantsciences.ucdavis.edu/PLS120/PLS120Book/docs/chLinReg.html)

### Practice-only weighted-average inventory cost

LM7 practice p487/PDF497 andsolution p492/PDF502 contain inventoryCOGS:unit_cost=total_cost/units_available,COGS=unit_cost*units_sold. This is outside regression but inside financial-analysis mission; queue exact stock/cost scope and accounting corroboration rather than omit it.

## financial-analysis-cfa-l1-b1-b20

### Visualization prose has a midpoint typo and implicit scaling relationships

LM2 p83/PDF93 calls the1%-2%bin midpoint0.5% while identifying coordinate1.50%; actualmidpoint1.5%. Midpoint is arithmetic-mean of the two endpoints, already curated. p87-88/PDF97-98 tree-map area and word-font size proportionality are generic proportional scaling with unspecified proportionality calibration, not new fitted financial models.

### Reporting-only ratios in fictional MDA are not definitions

LM2 p89/PDF99 Exhibit27 lists revenue growth, effective tax rate and dilutedEPS but supplies no numerator/denominator scope for these metrics. Do not invent a formula from a reported scalar value; preserve as context-only rather than new definition.

## financial-analysis-cfa-l1-b1-b22

### Further statement arithmetic discovered in structured-data exhibit

LM2 p66/PDF76 Exhibit3 also adds products+services for sales/cost totals,addsR&D+SG&Aforoperatingexpense total,andadds netotherincome tooperatingincome forpretax income. These are aggregation/signed-subtotal identities; preserve aliases and scope rather than mint every two-line addition as a separate model. Full statement policy context remains limited.

### First-passage liquidity pool exhaustion probability needs normal CDF and path assumptions

LM4 practice19 p291-292/PDF301-302:probability=2[1-Phi(lambda/(sigma*sqrt(T)))],solutionp299/PDF309. This is a path-hitting rather than terminal-loss probability;requires unavailable normalCDFand qualified continuous-time zero-drift Gaussian path assumptions beyond merely normal terminal returns. Retain exact expression/locator without approximation.

### One-period binomial up-probability is an expectation inverse

LM4 practice16 p291/PDF301 andsolutionp298/PDF308:E(ST)=p*u*S+(1-p)*d*S, hencep=(E(ST)/S-d)/(u-d). It is the two-state normalized expectation inverse,not a new risk-neutral pricing probability; no rate/measure assumptions supplied.

## financial-analysis-cfa-l1-b1-b23

### Revision supersedes one b19 record; no new coverage counted

financial-analysis--supplied-regression-coefficient-t-statistic@r2 supersedes@r1 fromb19. The earlier draft ZIP remains immutable. Revision fixes generic coefficient-unit metadata for uniformly bound slope/intercept ports and adds an explicit zero-denominator rejection; count one unique model,not two.

## financial-analysis-cfa-l1-b1-b24

### Benchmark-relative excess return is a named difference requiring its own context binding

LM5 printed p340/PDF350 explicitly constructs excess return=portfolio return-FTSE benchmark return over the same twelve months. Preserve this relationship as a candidate distinct from raw return andrisk-free excess return; obtain exact accessible benchmark-relative definition before a full record.

### Late solution arithmetic discrepancies

LM4 solution19B printed p299/PDF309 says32.2%,then rounded calculation32.0%;do not use it as an exactCDF oracle. LM7solution32 printed p492/PDF502 displays.0001/.00002=.5000;displayed operands give5. Additional sourceprecision/correction needed.

## Additional review cautions from the gap pass

LM5 printed p323/PDF333 changes the meaning of s-squared when discussing n versus n-1 denominators. Do not use s-squared/n as a population-variance estimate if s-squared already denotes the sample variance. Printed p321/PDF331 makes an unrestricted efficiency claim for sample mean and variance; efficiency requires a specified statistical model.

LM5 printed p331/PDF341 Example10 constructs a weighted mean but then applies the unweighted iid mean standard error. That step requires additional weight/design assumptions; the curated iid standard-error formula is not a general weighted-mean standard error.

LM7 printed p492/PDF502 solution32 displays .0001/.00002=.5000; the displayed operands give5. The precision of the source inputs must be clarified before treating that example as an oracle.

LM2 printed p83/PDF93 bin midpoint typo is separately noted in b20. Plot rendering, lookup-table transcription and faint/garbled glyphs were not independently certified.

## Final mathematical scope review

The half-variance return approximation at LM2 printed pp127–128/PDF137–138 uses sample variance s-squared. A Taylor expansion around arithmetic return a instead involves the finite-set variance with divisor n: g approximately a minus v_n/[2(1+a)], where v_n=(n-1)*s-squared/n. The source shorthand drops both this finite-sample normalization and the nonzero-mean denominator. Its worked small sample is therefore unsuitable as an exact oracle. A bounded approximation profile and independent scope evidence remain necessary before curating it as a model.

LM6 printed p382/PDF392 Exhibit18 reports mean returns .0157% and .0135% but a negative difference. The difference orientation and source rounding need clarification before using its signed statistic as a reference. The paired-test relationship is already curated with an explicit ordered-difference contract.

The LM6 summary at printed p407/PDF417 gives contingency-table degrees of freedom as (r-1)(c-2). This conflicts with its own main section at p400/PDF410 and the independently inspected NIST formula (r-1)(c-1). The curated record uses the supported main-section formula and does not reproduce the summary typo.
