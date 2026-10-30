---
id: source-outsider-financial-forecasting-and-schema-suggestions
type: source
title: "Outsider Financial Forecasting and Schema Suggestions"
summary: "Imported equity, FX, and bond question examples with outsider forecasting, schema, and orchestration proposals; not an accepted representation contract."
status: provisional
created: '2026-10-29'
updated: '2026-10-29'
topics:
  - finance
  - exemplars
  - representation
confidence: null
relations:
  - type: relates-to
    target: idea-domain-exemplars-intrinsic-value-and-fx
  - type: relates-to
    target: question-model-node-ast-and-schema-representation
  - type: relates-to
    target: question-temporal-and-spatial-data-alignment
  - type: relates-to
    target: question-uncertainty-and-epistemic-bounds-serialization
---

# Outsider Financial Forecasting and Schema Suggestions

## Provenance and interpretation

Contains two original parts: forecasting discussion (original lines 1–1350) and Financial data schemas and model interfaces (original lines 1351–2930). Both are outsider suggestions, NOT prescribed implementation. Instrument/Observation/ScenarioSet and other proposed records do not amend [[decision-representation-contract-v0]]. Fitting a stored model is not by itself offline curation of a new reusable source model; any suggested orchestration must be evaluated against [[concept-specialized-model-curation-agents]].

- Imported on 2026-10-29 from `Queue/Forecasting future financial prices with ConnectedModels.md`.
- Created/updated metadata dates describe this source record, not the original document.
- Original payload SHA-256 (including original line endings): `27873697bf5609f9289f1b6c91af8c59a527871c0afc16783a611f92ce29204c`.
- The original payload follows unchanged after the marker; line references to the original are relative to that payload.
- User clarification, 2026-10-29: Queue contains candidate questions and outsider thoughts, NOT prescriptive solutions. The outsider's identity, generation process, and full conversation provenance are not supplied; no author or model is inferred.

## Original document (verbatim)

<!-- ORIGINAL DOCUMENT:BEGIN -->

# Forecasting future financial prices with ConnectedModels

The central design principle is:

> Forecast a **distribution of future outcomes for a precisely defined instrument and horizon**, not a single “future price.”

A useful system should be able to say:

- “Under these assumptions, the median estimated price is X.”
- “The middle 80% of simulated outcomes is Y–Z.”
- “The forecast is most sensitive to these inputs.”
- “This simpler benchmark has historically performed better—or we do not yet know.”
- “These results predict price, not necessarily investor return.”

I’ll use three concrete examples throughout:

1. **Stock:** the price of a particular share one year from now.
2. **Currency:** USD per euro in one year.
3. **Bond:** the clean price of a specified Treasury bond in one year.

The same architecture extends to commodities, funds, derivatives and other instruments, but the models and data interfaces change.

---

# 1. First define the question precisely

“Where will the price be?” is underspecified. ConnectedModels should turn it into a typed forecast request.

## 1.1 Instrument identity

For a stock:

- Issuer and security, not just company name.
- Share class, listing venue and currency.
- Stable security identifier, because tickers change and can be reused.

For FX:

- Currency pair and **quote direction**, such as USD per EUR.
- Spot, forward, futures or a reference fixing.
- Settlement convention and market venue or source.

For a bond:

- Issuer and exact security identifier, such as a CUSIP or ISIN.
- Coupon, maturity, payment schedule and day-count convention.
- Currency, seniority, embedded options and collateral.
- Clean price, dirty price, yield or total return.

## 1.2 Time and target

Specify:

- Forecast origin \(t\), including time zone.
- Horizon \(T\): one hour, one trading day, one year, or a particular date.
- Observation: last trade, closing auction, bid, ask, midprice, daily reference rate, etc.
- Whether the target is **nominal price**, real purchasing-power-adjusted price or return.
- Whether corporate actions and cash flows are included.

### Price is not the same as return

For a stock with dividend \(D\), ignoring splits and other actions for the moment:

\[
R_{t,t+1}^{\text{total}}
=
\frac{P_{t+1}-P_t+D_{t+1}}{P_t}
\]

A stock might end the year at the same price and still provide a positive total return through dividends. Splits also change the quoted per-share price without necessarily changing an investor’s economic value.

For a bond:

\[
\text{Dirty price}
=
\text{Clean price}+\text{accrued interest}
\]

A future clean price excludes coupon income received in the meantime. A bond’s holding-period return includes both the price change and coupons, and depends on what happens to those coupons after payment.

### Forecast output

For a specified future observable price \(P_T\), the platform should return something like:

\[
\widehat{\mathcal D}_t(P_T),
\quad
\text{median},
\quad
P_{10},P_{90},
\quad
P(P_T>K)
\]

It should also return **the assumptions and validation behind that distribution**. No specific instrument was supplied here, so the numerical examples below are hypothetical—not current market forecasts.

---

# 2. Separate four jobs that are often conflated

## A. Forecasting under the real-world distribution

The practical forecasting question is:

\[
\mathcal D^{\mathbb P}(P_T\mid\mathcal I_t)
\]

where:

- \(\mathbb P\) denotes a real-world or **physical** probability distribution.
- \(\mathcal I_t\) is the information actually available at time \(t\).

This distribution is what we want for questions such as:

> “What range might the stock’s closing price fall into in one year?”

## B. Valuing an instrument today

A valuation model asks what a future stream of cash flows is worth at time \(t\):

\[
P_t
=
E_t^{\mathbb P}[m_{t+1}X_{t+1}]
\]

Here \(m_{t+1}\) is a stochastic discount factor and \(X_{t+1}\) is the payoff.

A practical discounted-cash-flow model approximates this by forecasting cash flows and discounting them at an assumed required return.

**A valuation estimate is not automatically a forecast of the market price next year.** To forecast a future market price, we also need a model for future investor expectations, discount rates, liquidity and any difference between market price and modeled value.

## C. Pricing derivatives under a risk-neutral measure

A derivative-pricing model often uses:

\[
P_t
=
\frac{1}{R_f}E_t^{\mathbb Q}[X_{t+1}]
\]

where \(\mathbb Q\) is the **risk-neutral pricing measure**.

Option prices can be used to infer a risk-neutral distribution. That distribution reflects how the market prices different states; it is **not automatically the physical probability distribution of future prices**. Converting between the two requires additional assumptions or empirical estimation.

See the [New York Fed on option-implied risk-neutral densities](https://www.newyorkfed.org/research/staff_reports/sr677.html) and the [Bank of England on translating risk-neutral to real-world densities](https://www.bankofengland.co.uk/working-paper/2012/estimating-probability-distributions-of-future-asset-prices).

## D. Making a trading or planning decision

Even a useful forecast does not by itself tell us whether to trade. The decision requires:

- Entry and exit prices.
- Spread, commissions and market impact.
- Position size and risk tolerance.
- Financing, borrow and collateral costs.
- Taxes where relevant.
- How the proposed position interacts with existing exposures.

These four jobs should be separate objects in ConnectedModels. Otherwise, a pricing model can accidentally be represented as an empirical forecast, or a statistically interesting forecast as a profitable strategy.

---

# 3. The common ConnectedModels pipeline

```text
User question and instrument contract
                ↓
Instrument definition + forecast target
                ↓
Point-in-time data assembly
                ↓
Data-quality and adjustment models
                ↓
Shared economic / financial state models
                ↓
Instrument-specific price and cash-flow models
                ↓
Joint future scenarios
                ↓
Price, return and risk distributions
                ↓
Backtest against benchmarks
                ↓
Decision model, if requested
```

Each model should identify:

```text
Model name and version
Target variable and units
Input schema and frequency
Training window and information cutoff
Parameters and estimation method
Output distribution
Dependencies and correlations
Known domain restrictions
Historical validation and benchmarks
```

For each data point, retain at least:

```text
instrument_id
field_name
value
currency / units
observation_time
publication_time
time_received
source
source_revision / vintage
adjustment convention
quality flag
```

The crucial distinction is between:

- **Observation time:** when an event or transaction occurred.
- **Publication time:** when the information became public.
- **Ingestion time:** when ConnectedModels received it.
- **Revision time:** when a value was subsequently corrected.

A backtest should use only information actually available at the forecast origin.

---

# 4. Data: what to retrieve, and from where

## 4.1 Prices, trades and quotes

| Data | Concrete source | What it gives | Important limitation |
|---|---|---|---|
| US stock historical bars | [Stooq historical downloads](https://stooq.com/db/h/) | Downloadable historical market data | Check coverage, adjustment conventions, quality and usage rights; not a complete institutional point-in-time feed |
| US consolidated equity trades and quotes | [NYSE Daily TAQ](https://www.nyse.com/market-data/historical/daily-taq) | Historical US trades, quotes and related market messages | Licensed product; market-data rights and fees matter |
| Current US consolidated quote/trade feed | [CTA/SIP information](https://www.nyse.com/data/cta) | Consolidated real-time trade and quote data for covered markets | Subscription and redistribution terms apply |
| US dollar bilateral FX references | [Federal Reserve H.10 historical rates](https://www.federalreserve.gov/releases/h10/hist/) | Daily reference exchange rates | Reference observations, not a continuous executable FX tape |
| US Treasury par curve | [Treasury interest-rate statistics](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics) | Published daily Treasury par yields | A par curve is not the price of a particular bond |
| Individual Treasury trades | [FINRA Treasury Trade Activity](https://www.finra.org/finra-data/fixed-income/treasury-trade) | Publicly available selected Treasury trade information | Limited coverage and access terms; trades are not bid/ask quotes |
| Broader historical fixed-income transactions | [FINRA TRACE historical data](https://www.finra.org/filing-reporting/trace/historic-academic-data) | Historical transaction-level data | Product-specific fees, delay and rights |

**Design point:** Keep the raw market observations and the transformation to bars separate. A daily close can be produced from trade data, but a close cannot reconstruct the intraday order book.

## 4.2 Fundamentals, cash flows and security terms

| Data | Concrete source | Use |
|---|---|---|
| US issuer filings | [SEC EDGAR](https://www.sec.gov/search-filings) | Financial statements, risk factors, management disclosures |
| Structured issuer facts | [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Company Facts and submissions data |
| Treasury issuance and auctions | [Treasury Securities Auctions Data](https://fiscaldata.treasury.gov/datasets/treasury-securities-auctions-data/) | Issue terms and auction information |
| Corporate-action evidence | [SEC filings](https://www.sec.gov/search-filings) and [NYSE corporate-action data](https://www.nyse.com/market-data/corporate-actions) | Splits, dividends and other actions |

For equity fundamentals, the relevant timestamp is **when the filing became available**, not the financial-period end. A quarter ending March 31 cannot be used in a forecast made before the filing was published.

Corporate actions need their own event model:

```text
announcement date
ex-date
record date
payment / effective date
action type
cash or share adjustment
source and correction history
```

A current vendor-adjusted price history is useful for some analyses, but it may not reproduce exactly what was known at an earlier date.

## 4.3 Macro data and historical vintages

Useful examples:

- GDP: [FRED GDP](https://fred.stlouisfed.org/series/GDP).
- Inflation: [FRED CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL).
- Unemployment: [FRED UNRATE](https://fred.stlouisfed.org/series/UNRATE).
- Treasury yields: [FRED DGS10](https://fred.stlouisfed.org/series/DGS10).
- USD per euro reference rate: [FRED DEXUSEU](https://fred.stlouisfed.org/series/DEXUSEU).
- Historical macro vintages: [ALFRED](https://alfred.stlouisfed.org/help).

ALFRED is useful for reconstructing data versions, but it is not a substitute for checking exact release timestamps. Vintage coverage and the timing of archival updates vary by series.

## 4.4 Data that is often difficult or licensed

Depending on the problem, the platform may also need:

- Analyst forecasts and estimate revisions.
- Historical option chains and implied volatility surfaces.
- Full OTC FX spot and forward quotes.
- Bond bid/ask quotes and comprehensive corporate bond trades.
- Stock borrow cost and availability.
- Delisted securities and point-in-time index membership.

These should be represented as **optional, explicitly licensed inputs**, not silently substituted with a public proxy. A proxy can still be useful if its mismatch is documented and tested.

---

# 5. A hierarchy of models

Do not start with the most complicated model. Start with baselines, then require more elaborate models to prove their value.

## 5.1 Baseline A: no-change price

\[
\widehat P_{t+H}=P_t
\]

This is a natural benchmark for many price-level questions, particularly short-horizon FX.

It predicts no price change—not zero total return if there are dividends or coupons.

## 5.2 Baseline B: historical average return

For returns \(r_1,\ldots,r_n\):

\[
\hat\mu=\frac{1}{n}\sum_{i=1}^{n}r_i
\]

For continuously compounded returns:

\[
\widehat P_{t+H}=P_t e^{H\hat\mu}
\]

This is a simple benchmark, but estimating expected returns is difficult. Different sample windows can produce very different \(\hat\mu\).

## 5.3 Baseline C: empirical return distribution

Instead of assuming normally distributed returns, sample historical returns from comparable horizons:

\[
r^*_{t+H}\sim\{r_1,\ldots,r_n\}
\]

\[
P^*_{t+H}=P_t e^{r^*_{t+H}}
\]

For multi-period paths, resample blocks or use another model that preserves relevant serial dependence.

**Limitation:** Historical conditions may not resemble the future. A large historical dataset does not guarantee that it contains the next structural break.

## 5.4 Volatility model

A common GARCH(1,1) specification is:

\[
r_t=\mu_t+\varepsilon_t,
\qquad
\varepsilon_t=\sigma_tz_t
\]

\[
\sigma_t^2
=
\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2
\]

This models changing **conditional volatility**. It does not, by itself, predict the direction of the next price move.

The original GARCH model is described in [Bollerslev’s 1986 paper](https://scholars.duke.edu/publication/651658).

## 5.5 Fundamental model

Connect economic and operational variables to future cash flows and discount rates:

```text
Economic environment
→ company / issuer outcomes
→ cash flows and balance sheet
→ discount-rate / risk-premium scenarios
→ value distribution
→ market-price model
```

This is most useful when its long-horizon assumptions can be explained, stress-tested and compared with actual outcomes.

## 5.6 Market-implied model

Use current market prices as information:

```text
Observed price or options
→ implied assumptions / risk-neutral distribution
→ compare with independently estimated physical scenarios
```

But do not assume that a market-implied distribution under \(\mathbb Q\) equals the real-world distribution under \(\mathbb P\).

---

# 6. Stock example: forecasting a share price in one year

## 6.1 The question

> What might the closing price of a specified US company’s ordinary share be one year from today, and what assumptions drive the range?

A good answer needs both:

1. A market-based return forecast.
2. A fundamental scenario forecast.

Neither should be treated as automatically correct.

---

## 6.2 Stock pipeline A: return-factor model

### Data

- Historical stock and broad-market returns.
- A risk-free return appropriate to the horizon.
- Point-in-time factor returns and stock exposures.
- Corporate actions and delistings.

The [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library.html) is one public source for research factor returns. Verify the factor definitions, frequency and return construction before use.

### Model

A simple factor model is:

\[
r_{i,t}-r_{f,t}
=
\alpha_i
+
\beta_i(r_{m,t}-r_{f,t})
+
\epsilon_{i,t}
\]

A multi-factor version adds further terms:

\[
r_{i,t}-r_{f,t}
=
\alpha_i+\beta_i^\top f_t+\epsilon_{i,t}
\]

Where:

- \(r_i\): the stock’s return.
- \(r_f\): risk-free return.
- \(f_t\): market and other factor returns.
- \(\epsilon_i\): stock-specific return shock.

### Connected pipeline

```text
Historical stock + factor returns
→ estimate exposures and residual distribution
→ simulate joint future factors and stock-specific shock
→ simulate total returns and distributions
→ convert to the requested price target
```

### Important interface

If the model is fit on **total returns** but the requested target is the **unadjusted share price**, distributions must be modeled explicitly. In a simple one-period setting:

\[
P_{t+1}
=
P_t(1+R_{t+1}^{\text{total}})-D_{t+1}
\]

This requires consistent treatment of dividends, reinvestment and corporate actions. For splits and multiple payment dates, use a security-level cash-flow and share-count ledger rather than this simplified equation.

### What this model answers

It provides a distribution of future prices **conditional on the estimated return process**. It does not explain company operations in detail.

---

## 6.3 Stock pipeline B: operating model → valuation → future market price

### Step 1: Forecast business drivers

For a simplified company:

\[
\text{Revenue}_{t+1}
=
\text{Revenue}_t(1+g_t)
\]

\[
\text{EBIT}_{t+1}
=
\text{Revenue}_{t+1}\times \text{operating margin}_{t+1}
\]

\[
\text{NOPAT}_{t+1}
=
\text{EBIT}_{t+1}(1-\text{cash tax rate}_{t+1})
\]

\[
\text{FCFF}_{t+1}
=
\text{NOPAT}_{t+1}
+
\text{D\&A}_{t+1}
-
\text{CapEx}_{t+1}
-
\Delta\text{working capital}_{t+1}
\]

Potential upstream models include:

- Market-size and demand models.
- Unit sales × price models.
- Margin and input-cost models.
- Working-capital and investment models.
- Industry competition and pricing models.

### Step 2: Estimate enterprise value at the future date

At future time \(T\):

\[
EV_T
=
\sum_{k=1}^{N}
\frac{FCFF_{T+k}}{(1+WACC_T)^k}
+
\frac{TV_{T+N}}{(1+WACC_T)^N}
\]

A constant-growth terminal approximation is:

\[
TV_{T+N}
=
\frac{FCFF_{T+N+1}}{WACC_T-g}
\qquad \text{requiring } WACC_T>g
\]

### Step 3: Convert enterprise value to value per share

A simplified bridge is:

\[
\text{Equity value}_T
=
EV_T-\text{net debt}_T-\text{other senior claims}_T
+\text{non-operating assets}_T
\]

\[
V_T^{\text{per share}}
=
\frac{\text{Equity value}_T}
{\text{diluted shares}_T}
\]

The detailed bridge depends on leases, minority interests, options, pensions, excess cash and other company-specific items.

### Step 4: Model future market price

A DCF value is not necessarily the price the market will pay. One possible empirical bridge is:

\[
P_T=V_Te^{z_T}
\]

\[
z_T=\rho z_t+\eta_T
\]

where \(z_t=\log(P_t/V_t)\) measures the current gap between market price and the model’s value.

**But:** \(\rho\) must be estimated and tested; convergence to modeled value must not be assumed. A model can be persistently wrong, and the market may rationally disagree with its inputs.

### Illustrative calculation

Suppose a simulated **one-year-ahead scenario** gives:

- Next year’s annual FCFF after that future date: **$11.2 million**.
- Future WACC: **10%**.
- Perpetual growth: **3%**.
- Future net debt: **$20 million**.
- Diluted shares: **10 million**.

Using the constant-growth formula **at the future date**:

\[
EV_T=\frac{11.2}{0.10-0.03}=\$160\text{ million}
\]

\[
V_T^{\text{per share}}
=
\frac{160-20}{10}
=
\$14
\]

That is an **illustrative modeled value at \(T\)**, not a prediction that the stock will trade at $14. A future-price forecast still needs the market-price bridge and a distribution over the assumptions.

### What could change the result most?

Usually:

- Future margins and reinvestment needs.
- Discount rate and long-run growth.
- Debt and dilution.
- Competitor behavior.
- Whether the terminal-value approximation is plausible.

A useful output is a sensitivity surface over WACC and growth, not one number.

For the dividend-discount special case, see [Damodaran’s NYU valuation material](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/lectures/ddm.html).

---

## 6.4 Stock pipeline C: infer expectations already in the price

Rather than forecast future price directly, solve for the growth or margin assumptions consistent with today’s price:

\[
P_t=V(g^*,\text{other assumptions})
\]

Then:

\[
g^*=\text{growth rate implied by the observed price}
\]

Compare \(g^*\) with independently estimated scenarios.

This helps answer:

> “What must happen for today’s price to be justified under this model?”

It does **not** prove that any difference is mispricing. The discrepancy may reflect risk, omitted information or a flawed model.

---

# 7. Currency example: USD per EUR in one year

## 7.1 The question

> What might the USD-per-EUR spot reference rate be in one year?

If \(S=1.10\), one euro costs $1.10.

Always record quote direction. A model of EUR per USD has the inverse quote and different numerical dynamics.

---

## 7.2 Start with the random-walk benchmark

\[
\widehat S_{t+H}=S_t
\]

A probabilistic version is:

\[
\log S_{t+H}
=
\log S_t+\mu H+\sigma\sqrt{H}Z,
\qquad Z\sim N(0,1)
\]

A no-change log-price baseline sets \(\mu=0\).

The random walk is a serious benchmark, not a straw man. In the classic Meese–Rogoff comparisons, the structural exchange-rate models studied did no better than a naïve random walk in their forecast exercises. See the [Federal Reserve follow-up](https://www.federalreserve.gov/pubs/ifdp/1985/268/default.htm).

---

## 7.3 Add interest rates and macroeconomic drivers

A statistical model might use:

\[
\Delta\log S_{t+H}
=
\alpha
+
\beta_1(i_{\text{USD}}-i_{\text{EUR}})
+
\beta_2(\pi_{\text{USD}}-\pi_{\text{EUR}})
+
\beta_3x_t
+
\epsilon_{t+H}
\]

Potential \(x_t\) variables:

- Economic growth surprises.
- Current-account variables.
- Inflation expectations.
- Risk sentiment and volatility.
- Terms of trade.
- Relative monetary-policy expectations.

### Connected pipeline

```text
US and euro-area macro data
→ inflation / growth nowcasts
→ interest-rate path scenarios
→ joint currency-return model
→ USD-per-EUR price distribution
```

**Important:** A statistically estimated relationship is not necessarily causal, stable or tradable. It must outperform the random-walk benchmark out of sample to justify its added complexity.

---

## 7.4 Forward rates: useful, but not the same as a forecast

For USD per EUR, a simplified covered-interest-parity relation with one-period simple rates is:

\[
F
=
S\frac{1+r_{\text{USD}}}{1+r_{\text{EUR}}}
\]

With hypothetical inputs:

\[
S=1.10,\qquad
r_{\text{USD}}=5\%,\qquad
r_{\text{EUR}}=3\%
\]

\[
F
=
1.10\frac{1.05}{1.03}
\approx 1.1214
\]

This is a simplified hedged pricing relationship, **not a claim that spot will be 1.1214 in a year**.

Real forward pricing must account for tenor, day counts, collateral, bid–ask and cross-currency basis. The [BIS discussion of covered interest parity](https://www.bis.org/publications/qr-201609/covered-interest-parity-lost-understanding-cross-currency-basis) explains why the simple relation can differ from observed markets.

### Physical forecast example

Suppose—not as an empirical estimate—that:

\[
\log(S_T/S_t)\sim N(0.01,0.12^2)
\]

With \(S_t=1.10\), the median is:

\[
1.10e^{0.01}\approx1.1111
\]

The approximate 10th–90th percentile range is:

\[
1.10e^{0.01\pm1.2816(0.12)}
\approx [0.953,\ 1.296]
\]

This range follows from the **assumed** mean, volatility and normal distribution. It is not derived from current data, and it does not account for uncertainty in those parameters.

---

# 8. Bond example: future price of a Treasury bond

## 8.1 The question

> What might the clean price of this specific Treasury bond be one year from now?

We must know its actual:

- Coupon and payment dates.
- Maturity.
- Day-count convention.
- Settlement date.
- Current clean or dirty price.
- Applicable future yield curve.

A “10-year Treasury yield” is not itself the price of a particular Treasury bond.

---

## 8.2 Mechanical bond-pricing model

For a bond with remaining cash flows \(CF_k\):

\[
P_T^{\text{dirty}}
=
\sum_{k:T_k>T}
CF_k\,DF(T,T_k)
\]

where \(DF(T,T_k)\) is the future discount factor for each remaining cash-flow date.

Then:

\[
P_T^{\text{clean}}
=
P_T^{\text{dirty}}
-
\text{accrued interest}_T
\]

The bond-pricing function is largely mechanical once the future curve and bond terms are specified. The difficult part is predicting the **future curve**.

---

## 8.3 Forecast the future yield curve

A practical factor model is dynamic Nelson–Siegel:

\[
y_t(\tau)
=
\beta_{0,t}
+
\beta_{1,t}
\frac{1-e^{-\lambda\tau}}{\lambda\tau}
+
\beta_{2,t}
\left[
\frac{1-e^{-\lambda\tau}}{\lambda\tau}
-e^{-\lambda\tau}
\right]
\]

The factors roughly represent:

- \(\beta_0\): level.
- \(\beta_1\): slope.
- \(\beta_2\): curvature.

A simple time-series model can then forecast factors:

\[
\boldsymbol\beta_{t+1}
=
\boldsymbol\mu
+
A(\boldsymbol\beta_t-\boldsymbol\mu)
+
\boldsymbol\eta_{t+1}
\]

### Connected pipeline

```text
Historical Treasury curve observations
→ curve fitting
→ level / slope / curvature factors
→ physical-measure factor forecasts
→ future zero-coupon discount factors
→ bond cash-flow pricing
→ future clean-price distribution
```

The Federal Reserve publishes [nominal yield-curve data and methodology](https://www.federalreserve.gov/data/nominal-yield-curve.htm).

**Important distinction:** The US Treasury’s published reference curve is a **par curve**. A par yield cannot simply be inserted as the zero rate for every cash flow. The system must use a suitable zero curve or consistently bootstrap discount factors.

The ordinary dynamic Nelson–Siegel model is a forecasting model; it does not automatically impose no-arbitrage consistency. See [Diebold and Li](https://ideas.repec.org/a/eee/econom/v130y2006i2p337-364.html) and an [arbitrage-free extension](https://www.nber.org/papers/w14463).

---

## 8.4 Illustrative bond calculation

Suppose a hypothetical bond:

- Has a $100 face value.
- Pays a $4 annual coupon.
- Has three years remaining today.
- Is currently priced at $100.
- One year later has two annual cash flows remaining.
- Has a flat annual-compounded yield of 5% at that future date.

On a coupon date, ignoring accrued interest:

\[
P_T
=
\frac{4}{1.05}
+
\frac{104}{1.05^2}
\approx \$98.14
\]

The future **price** is approximately $98.14.

If the investor received a $4 coupon during the year and held to that future date, the simplified holding-period return is:

\[
\frac{98.14+4-100}{100}
\approx 2.14\%
\]

This illustration assumes the initial $100 price and the future 5% yield; neither is a forecast. It also uses annual payments to keep the arithmetic simple. Actual Treasury conventions require the actual coupon schedule and accrued-interest calculation.

---

## 8.5 Corporate bonds: add credit risk

For a corporate bond, the Treasury curve is only one part of the pipeline:

```text
Risk-free curve
+ issuer financial condition
+ default probability
+ expected recovery
+ credit spread
+ liquidity
+ embedded options
→ corporate-bond price
```

A simplified risky-cash-flow valuation might use:

\[
P_t
=
E_t\left[
\sum_k DF(t,T_k)\,
CF_k\,
\mathbf{1}(\text{no default before }T_k)
+
DF(t,\tau)R_\tau
\mathbf{1}(\text{default at }\tau)
\right]
\]

A forecast of the future bond price needs scenarios for **future spreads and liquidity**, not just an estimate of actual default probability. A quoted spread can reflect more than expected credit losses.

---

# 9. Modeling shared drivers without hiding dependencies

A connected system should not forecast each input independently.

For example:

```text
Inflation surprise
 ├─→ central-bank policy expectations
 │    ├─→ Treasury yield curve
 │    └─→ USD interest rates
 ├─→ company input costs
 ├─→ consumer demand
 └─→ risk sentiment
      ├─→ equity risk premium
      ├─→ credit spreads
      └─→ currency flows
```

If inflation shocks are shared, then the resulting interest rates, stock discount rates, credit spreads and FX outcomes should be simulated **jointly**.

One statistical framework is a vector autoregression:

\[
x_t=A_1x_{t-1}+\cdots+A_px_{t-p}+u_t
\]

where \(x_t\) might include inflation, rates, growth and spreads.

Simulate correlated innovations:

\[
u_t\sim F(0,\Sigma)
\]

Then feed the same scenario into the stock, FX and bond models.

## Important qualification

A VAR can estimate historical relationships. Its coefficients are not automatically causal. If the question is:

> “What would the stock price be **if** the central bank raised rates?”

that is a causal counterfactual, and the system needs a defensible intervention model or identification strategy. It should not simply change one VAR variable while holding all other variables fixed.

For genuine policy or geopolitical shocks, compare:

- Historical-event and local-projection estimates.
- Structural economic models where defensible.
- Explicit stress scenarios.
- Alternative causal assumptions.

The output should show where the models disagree.

---

# 10. A compact, executable Python example

The following is a deliberately simple **empirical-return baseline** for a price-only stock forecast. It illustrates the connected interfaces; it is not a complete stock valuation model.

It uses historical log returns supplied locally, resamples full horizon returns and converts each sampled return into a future price.

```python
import math
import random
from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class PriceForecastRequest:
    instrument: str
    as_of: str
    horizon_trading_days: int
    current_price: float
    price_currency: str


class HistoricalHorizonReturns:
    """
    Convert a series of comparable, point-in-time price observations
    into overlapping H-day log price returns.

    Input prices must use a consistent split/action convention.
    This is a PRICE-return model, not a total-return model.
    """

    def __init__(self, prices, horizon):
        if horizon <= 0:
            raise ValueError("horizon must be positive")
        if len(prices) <= horizon:
            raise ValueError("not enough historical prices")
        if any(p <= 0 for p in prices):
            raise ValueError("prices must be positive")

        self.returns = [
            math.log(prices[i + horizon] / prices[i])
            for i in range(len(prices) - horizon)
        ]

    def sample(self, rng):
        return rng.choice(self.returns)


class FuturePriceModel:
    @staticmethod
    def from_log_return(current_price, log_return):
        return current_price * math.exp(log_return)


class ForecastPipeline:
    def __init__(self, return_model, price_model):
        self.return_model = return_model
        self.price_model = price_model

    def run(self, request, draws=10_000, seed=1):
        if draws < 2:
            raise ValueError("draws must be at least 2")

        rng = random.Random(seed)
        prices = sorted(
            self.price_model.from_log_return(
                request.current_price,
                self.return_model.sample(rng),
            )
            for _ in range(draws)
        )

        def quantile(p):
            # Simple nearest-index sample quantile for demonstration.
            return prices[round(p * (len(prices) - 1))]

        return {
            "instrument": request.instrument,
            "as_of": request.as_of,
            "horizon_trading_days": request.horizon_trading_days,
            "currency": request.price_currency,
            "mean": mean(prices),
            "p10": quantile(0.10),
            "median": quantile(0.50),
            "p90": quantile(0.90),
            "draws": draws,
        }


# FICTIONAL input data: replace with local, properly timestamped prices.
historical_prices = [100, 102, 99, 101, 103, 98, 100, 104, 102]
request = PriceForecastRequest(
    instrument="EXAMPLE",
    as_of="example forecast date",
    horizon_trading_days=2,
    current_price=102,
    price_currency="USD",
)

returns = HistoricalHorizonReturns(
    historical_prices,
    horizon=request.horizon_trading_days,
)
pipeline = ForecastPipeline(returns, FuturePriceModel())

print(pipeline.run(request, draws=10_000, seed=7))
```

### What this example does and does not do

It does:

- Keep the target, return model and price transformation separate.
- Simulate a distribution rather than output just one number.
- Use the same return horizon as the request.

It does **not**:

- Estimate a reliable forecast from nine fictional prices.
- Handle dividends, future splits or delistings.
- Account for regime changes, changing volatility or parameter uncertainty.
- Generate a real-time data vintage.
- Establish predictive skill.

Overlapping historical returns are dependent. That is not inherently wrong for this illustrative resampling model, but it matters when estimating uncertainty and evaluating forecasts.

For a production system, the same `ForecastPipeline` idea could connect:

```text
Point-in-time data
→ fitted factor or volatility model
→ joint scenario generator
→ corporate-action model
→ price transformation
→ distribution and diagnostics
```

---

# 11. How to test whether the forecast actually works

## 11.1 Rolling-origin backtesting

For each historical forecast date \(t\):

1. Freeze data available at \(t\).
2. Fit or update the model using only that information.
3. Predict the same horizon requested in deployment.
4. Record the full predictive distribution.
5. Compare with the realized target at \(t+H\).
6. Move the origin forward and repeat.

```text
Train through date 1 → forecast horizon → score
Train through date 2 → forecast horizon → score
Train through date 3 → forecast horizon → score
...
```

This is called rolling forecasting-origin evaluation. See [Hyndman’s time-series cross-validation discussion](https://robjhyndman.com/hyndsight/tscv/).

## 11.2 Compare with the correct benchmark

| Target | Minimum useful benchmark |
|---|---|
| Stock price level | No-change price |
| Stock excess return | Historical-average excess return, with clearly specified training window |
| FX spot | No-change spot / random walk |
| Bond price | No-change price and a clearly specified yield-curve baseline |
| Volatility | Rolling historical volatility |
| Portfolio tail loss | Historical simulation or another established risk baseline |

A model that beats one weak baseline may still fail against a stronger one.

## 11.3 Score the distribution, not only the point estimate

For point forecasts:

\[
MAE=\frac{1}{N}\sum_{i=1}^{N}|\hat P_i-P_i|
\]

\[
RMSE=
\sqrt{\frac{1}{N}\sum_{i=1}^{N}(\hat P_i-P_i)^2}
\]

For distributions, use a proper score such as CRPS:

\[
\operatorname{CRPS}(F,y)
=
\int_{-\infty}^{\infty}
\left(F(z)-\mathbf{1}\{y\le z\}\right)^2dz
\]

Also test interval calibration:

> If the model repeatedly reports an 80% interval, does that interval contain the realized outcome roughly 80% of the time?

Check calibration by regime and horizon, not just in aggregate.

For a binary threshold forecast such as \(P(P_T>K)\), use the Brier score:

\[
\text{Brier}=(p-y)^2
\]

A narrow forecast interval is not good if it is systematically wrong.

## 11.4 Guard against false confidence

Key failure modes:

- **Look-ahead bias:** using information before it was published.
- **Survivorship bias:** excluding delisted or failed companies.
- **Revision bias:** using today’s revised macro history as if known at the time.
- **Selection bias:** presenting only the best of many tried models.
- **Overlapping horizons:** treating dependent forecast errors as independent.
- **Regime changes:** assuming a relationship remains stable after market structure changes.
- **Implementation bias:** assuming fills at the midprice with no costs.

For stock-return predictors, [Goyal and Welch](https://www.nber.org/papers/w10483) document how difficult it can be to outperform simple historical benchmarks out of sample. That does not prove predictability is impossible; it does justify demanding strong evidence.

## 11.5 Forecast quality versus trading quality

Evaluate these separately:

### Forecast evaluation

- Point error.
- Distribution calibration.
- Proper scoring rule.
- Stability across time and instruments.
- Performance versus baselines.

### Trading evaluation, only if requested

- Bid/ask spread.
- Fees and taxes.
- Slippage and market impact.
- Financing and borrow.
- Turnover.
- Risk and drawdowns.
- Capacity and liquidity.

A forecast can be useful for budgeting or risk planning even if no profitable trading rule follows from it. Conversely, a trading result can look attractive in a backtest while relying on unrealistic execution.

---

# 12. What ConnectedModels should return to the user

For a specific instrument, I would present five layers.

## 12.1 Executive answer

```text
Instrument: [exact security]
Target: [price definition]
Forecast date: [...]
Horizon: [...]
Currency: [...]

Median forecast: [...]
80% predictive interval: [...]
Probability above / below selected thresholds: [...]
```

The system should say whether these are real-world estimates, market-implied pricing quantities or stress scenarios.

## 12.2 Model comparison

```text
No-change benchmark: [...]
Historical-return baseline: [...]
Factor model: [...]
Fundamental model: [...]
Scenario / ensemble result: [...]
```

If a model has not beaten its benchmark historically, say so.

## 12.3 Drivers and sensitivities

For example:

```text
Largest drivers:
1. Future interest-rate curve
2. Company operating margin
3. Equity risk premium
4. Share dilution
```

Show how the answer moves when each input changes, while preserving correlations where needed.

## 12.4 Data and provenance

```text
Price source and timestamp:
Fundamental filing and publication timestamp:
Corporate-action convention:
Macro vintage:
Model versions:
Last validation date:
```

If an exact input is unavailable, label the proxy and explain its mismatch.

## 12.5 What could most change the forecast?

Examples:

- Upcoming earnings and guidance.
- A central-bank decision.
- Bond default or a ratings event.
- A change in contract terms.
- A major macro release.
- Evidence that the forecast’s volatility regime has changed.

The system can rank candidate data improvements using **value of information**: how much would obtaining the information be expected to improve the user’s actual decision, net of its cost?

---

# 13. The biggest modeling choices by instrument

| Question | Stock | Currency | Bond |
|---|---|---|---|
| What must be identified exactly? | Share class, venue, price versus total return | Quote direction, spot versus forward, fixing | Exact issue, coupon, maturity, clean versus dirty |
| Natural baseline | No-change price / historical return | Random-walk spot | No-change price and yield-curve baseline |
| Core upstream models | Cash flows, margins, factors, discount rates | Rates, inflation, growth, currency-return dynamics | Yield-curve factors, issuer credit, liquidity |
| Mechanical mapping | Equity value and share count → per-share value | Log return → spot quote | Discount factors × contractual cash flows → price |
| Critical hidden issue | Dividends, dilution and market/value gap | Forward rate is not expected future spot | Par yields are not zero rates; price excludes coupons |
| Main uncertainty | Future profits and discount rates | Weak and unstable exchange-rate predictability | Future curve, spreads and optionality |

---

## Bottom line

I would structure this as **three connected but separable systems**:

1. **A data system** that knows exactly what was observed, when, and under which adjustment convention.
2. **A model system** that generates joint real-world scenarios and maps them to instrument prices using transparent formulas.
3. **An evaluation system** that continuously asks whether those forecasts beat simple alternatives, remain calibrated and are useful for the user’s decision.

The most important output is not a confident-looking price target. It is a **forecast distribution with an auditable explanation of what drives it, how well it has performed, and what would make it unreliable**.

---

# Financial data schemas and model interfaces
The design below turns the earlier forecasting architecture into a concrete specification for **stocks, FX spot rates, and fixed-rate bonds**.

It is a proposed design, not an implementation. The examples use fictional identifiers and values; they are intended to show how records and model stages fit together, not to provide forecasts.

## Design goals
The platform should be able to answer:
> “What is the distribution of the specified observable price at a specified future time, based only on information available at the forecast origin?”

It should also be able to reconstruct:
- Which data versions were used.
- Which models produced each intermediate result.
- How common shocks propagated across instruments.
- Whether the result was a real-world forecast, a market-implied quantity, or a stress scenario.
- How the forecast performed against appropriate historical benchmarks.

The central separation is:

```text
Instrument definition
        ≠
Observed market data
        ≠
Future scenario
        ≠
Pricing model
        ≠
Forecast result
        ≠
Trading decision
```

For example, a Treasury yield curve is not a bond price; it is an input to a bond-pricing calculation. A future curve is itself a forecast, not an observation.

---

# 1. Overall architecture
```text
Forecast request
    │
    ├── Instrument and target registry
    │
    ├── Point-in-time data resolver
    │     ├── Prices, quotes, trades
    │     ├── Security terms and corporate actions
    │     ├── Fundamentals and macroeconomic releases
    │     └── Yield curves, rates and FX observations
    │
    ├── Data transformations
    │     ├── Unit and currency normalization
    │     ├── Calendar and business-day handling
    │     ├── Curve construction
    │     └── Corporate-action handling
    │
    ├── Model fitting and validation
    │     ├── Baselines
    │     ├── Statistical and factor models
    │     └── Fundamental and scenario models
    │
    ├── Joint scenario generator
    │     ├── Economic and market states
    │     ├── Instrument-specific shocks
    │     └── Parameter and model uncertainty
    │
    ├── Instrument pricing and cash-flow models
    │     ├── Stock
    │     ├── FX
    │     └── Bond
    │
    └── Forecast result
          ├── Distribution and diagnostics
          ├── Data and model provenance
          └── Backtest and benchmark comparison
```

A **joint scenario** is the shared interface between the economic and instrument-specific parts. If inflation rises in scenario 27, the associated interest rates, exchange rate, company cash flows and bond spreads should reflect that same scenario—not unrelated draws from separate models.

---

# 2. Core concepts and conventions

## 2.1 Units are part of the type

A numeric value by itself is not enough.

```text
4.5
```

could mean:

- 4.5% annualized yield.
- 4.5 basis points.
- $4.50 per share.
- 4.5 USD per EUR.
- $4.50 per $100 face value of a bond.

Every numerical series or scenario variable should carry a unit and convention.

Examples:

```text
Price[USD / share]
FXRate[USD / EUR]
Yield[decimal per annum, semiannual bond-equivalent]
DiscountFactor[dimensionless]
BondPrice[USD per USD 100 face]
Return[decimal over horizon]
```

A conversion such as `4.5 percent → 0.045 decimal` must be explicit and recorded in provenance.

## 2.2 Three kinds of time

At minimum, data need:

1. **Effective or observation time:** what period or instant the value describes.
2. **Availability time:** when the information could have been known.
3. **Ingestion time:** when this installation received or loaded it.

For a revised statistic, there can be several records for the same observation period, each with a different vintage.

For a filing, the company’s financial period end is not the filing’s public availability time. Also, SEC filing acceptance time is not necessarily the exact time the document first became publicly accessible. See the [SEC’s timestamp explanation](https://www.sec.gov/about/webmaster-frequently-asked-questions).

## 2.3 Dates and timestamps must not be conflated

Use:

- UTC timestamps for events with known intraday timing.
- Explicit local time zone and calendar where a market convention requires it.
- Date-only values for releases or sources that do not provide a reliable time.
- A confidence or precision flag when availability is only known approximately.

Do **not** invent a midnight timestamp for a date-only observation and treat it as precise.

## 2.4 Probability measure and scenario purpose

Every forecast or scenario set carries:

```text
measure = PHYSICAL | RISK_NEUTRAL | NOT_APPLICABLE
purpose = FORECAST | VALUATION | STRESS | HISTORICAL_REPLAY
```

Examples:

- A stock-price distribution intended as a real-world forecast: `PHYSICAL`, `FORECAST`.
- A derivative-pricing distribution: `RISK_NEUTRAL`, `VALUATION`.
- A user-specified recession stress: `NOT_APPLICABLE`, `STRESS`.

A deterministic stress scenario does not become a probability forecast merely because its output has a price.

## 2.5 Missing is not zero

Use explicit states:

```text
OBSERVED
ESTIMATED
MISSING
NOT_APPLICABLE
INVALID
```

For example, an unknown future dividend is `MISSING` or generated by a documented model. It is not automatically zero.

---

# 3. Core identifiers and records

This section defines logical schemas. They could be implemented in relational tables, Parquet datasets, a document store, or a combination. The important thing is the semantics, not the storage engine.

## 3.1 `Instrument`

Represents the particular security or market object.

```text
Instrument
────────────────────────────────────────────────────────
instrument_id             Stable internal identifier
instrument_type           EQUITY | FX_SPOT | BOND
description               Human-readable name
status                    ACTIVE | INACTIVE | UNKNOWN
terms_version_id          Version of associated terms
valid_from / valid_to     Economic validity period
recorded_from / to        Period this version was stored
external_identifiers[]    CUSIP, ISIN, ticker, etc.
```

External identifiers should have validity intervals because tickers and listings can change.

### Equity extension

```text
EquityTerms
────────────────────────────────────────────────────────
instrument_id
issuer_id
share_class
currency
listing_venue
trading_calendar_id
```

### FX extension

```text
FXTerms
────────────────────────────────────────────────────────
instrument_id
base_currency             EUR
quote_currency            USD
quote_convention          quote currency units per base unit
market_or_fixing          source-specific
settlement_convention     if applicable
calendar_id
```

For EUR/USD in this convention:

\[
S=\frac{\text{USD}}{\text{EUR}}
\]

Thus, \(S=1.10\) means one euro costs $1.10.

Do not infer quote direction from an ambiguous display label. The Federal Reserve’s H.10 tables explicitly identify exceptions to their usual quote convention; see [H.10](https://www.federalreserve.gov/releases/h10/current/).

### Bond extension

```text
BondTerms
────────────────────────────────────────────────────────
instrument_id
issuer_id
currency
face_value
coupon_type               FIXED for the initial implementation
coupon_rate
coupon_frequency
issue_date
maturity_date
day_count_convention
business_day_convention
payment_calendar_id
cashflow_schedule_version
seniority
embedded_options          NONE or explicit option terms
```

For an initial production scope, support fixed-rate noncallable bonds first. Callable, floating-rate, inflation-linked and defaulted instruments need additional terms and models.

---

## 3.2 `ForecastRequest`

A request should be unambiguous enough to evaluate later against an observed outcome.

```json
{
  "request_id": "forecast-001",
  "instrument_id": "equity-example-class-a",
  "forecast_origin": "2026-01-02T21:00:00Z",
  "target": {
    "kind": "OBSERVABLE_PRICE",
    "field": "OFFICIAL_CLOSE",
    "target_time": "2027-01-04T21:00:00Z",
    "currency": "USD",
    "unit": "USD_PER_SHARE",
    "adjustment": "AS_TRADED"
  },
  "measure": "PHYSICAL",
  "purpose": "FORECAST",
  "requested_outputs": {
    "quantiles": [0.10, 0.50, 0.90],
    "thresholds": [
      {"operator": "GT", "value": 120.0, "unit": "USD_PER_SHARE"}
    ]
  },
  "availability_policy_id": "conservative-public-information-v1"
}
```

The example dates and identifier are fictional. In production, the target time should be resolved against the applicable exchange calendar and checked against the intended close.

### Other target types

```text
OBSERVABLE_PRICE
TOTAL_RETURN
YIELD
CASH_FLOW
PRICE_THRESHOLD_EVENT
```

For bonds, `target` additionally needs:

```text
CLEAN_PRICE | DIRTY_PRICE
price_basis: per 100 face | currency amount
settlement_date
```

For FX, it needs:

```text
base_currency
quote_currency
spot_or_fixing
source or fixing definition
```

### Why target source matters

The future last trade, official close, bid, and midprice may differ. Forecasting “the price” without choosing an observable makes both evaluation and the meaning of the answer ambiguous.

---

## 3.3 `Observation`

An immutable observation record should preserve what the source actually said.

```text
Observation
────────────────────────────────────────────────────────
observation_id
subject_id                 instrument, issuer, curve or economy
field_id                   e.g. OFFICIAL_CLOSE, CPI, PAR_YIELD
value
unit
observation_start
observation_end
source_id
source_record_id
source_version
availability_lower_bound   earliest supported public availability
availability_upper_bound   latest supported public availability
availability_precision     EXACT | INTERVAL | DATE_ONLY | UNKNOWN
ingested_at
revision_id
supersedes_observation_id
quality_status
```

For exact timestamps, the lower and upper bounds coincide. If availability is only known within an interval, the forecast policy decides whether the observation can be used.

A conservative real-time policy can require:

\[
\text{availability upper bound}\leq\text{forecast origin}
\]

If the interval straddles the forecast origin, exclude the value or flag the backtest as availability-uncertain. If availability is unknown, do not silently assume the value was known.

### Historical reconstruction versus live operation

These are different questions:

- **Public-information backtest:** What could an appropriately equipped forecaster have known at time \(t\)? An archived dataset loaded today can be usable if its historical availability is supported.
- **Operational replay:** What did this particular ConnectedModels installation actually have by \(t\)? Here ingestion time and its historical state matter.

The request or backtest must declare which one it uses.

### Vintages

[ALFRED](https://alfred.stlouisfed.org/help/downloaddata) distinguishes observation periods from vintage and real-time periods. Its date-based vintage information is useful, but it does not by itself establish every series’ precise intraday availability.

---

## 3.4 `Source` and `DataSnapshot`

```text
Source
────────────────────────────────────────────────────────
source_id
publisher
dataset_name
dataset_version
license
access_method
source_url
known_coverage
known_limitations
```

```text
DataSnapshot
────────────────────────────────────────────────────────
snapshot_id
as_of
availability_policy_id
included_observation_ids or manifest_hash
transformation_versions
created_at
content_hash
```

A snapshot identifies the exact source records and transformation versions used for a run. In a large system, store a manifest or content-addressed references rather than embedding millions of IDs in a result object.

**Licensing matters:** access, retention, derived-data use and redistribution can differ between public government data and commercial market data.

---

# 4. Market-data schemas

## 4.1 Equity prices and quotes

```text
EquityMarketObservation
────────────────────────────────────────────────────────
instrument_id
event_time
venue or consolidated_source
observation_type          TRADE | QUOTE | OFFICIAL_CLOSE | BAR
price
currency
price_unit
bid / ask                 if quote
size                      if available
adjustment_convention     AS_TRADED | SPLIT_ADJUSTED | TOTAL_RETURN_INDEX
source_and_availability
```

A trade price is not a quote. A consolidated close is not necessarily an executable price.

### Corporate actions

```text
CorporateAction
────────────────────────────────────────────────────────
action_id
instrument_id
action_type               CASH_DIVIDEND | SPLIT | MERGER | ...
announcement_availability
ex_date
record_date
payment_or_effective_date
cash_amount_and_currency  nullable
share_ratio               nullable
terms_source
status                    ANNOUNCED | COMPLETED | CANCELED
```

Corporate actions should be recorded as events rather than silently rewriting history.

For a future **as-traded share price**, a stock split changes the number of shares and quoted per-share price. A historical total-return index does not automatically give the future as-traded close.

The system should separately track:

1. Quoted per-share price.
2. Number of shares held after corporate actions.
3. Cash distributions received.
4. Reinvestment assumptions, if any.

Delisting, acquisition and other terminal events also matter. If the requested future close no longer exists, the result should contain a **target-unavailable state** or another explicitly agreed fallback—not fabricate a continuing price.

---

## 4.2 FX spot and forward observations

```text
FXObservation
────────────────────────────────────────────────────────
pair_id
base_currency
quote_currency
observation_type          SPOT | FORWARD_OUTRIGHT | FORWARD_POINTS | FIXING
value
unit
side                      BID | ASK | MID | REFERENCE
observation_time
value_date                where applicable
tenor                     where applicable
point_scale               required for forward points
source_and_availability
```

Do not treat a daily central-bank reference rate as an executable dealer quote.

### Inverting a bid/ask

If the observed market is quoted as USD per EUR:

\[
\text{bid}_{EUR/USD}=1.0990,\quad
\text{ask}_{EUR/USD}=1.1010
\]

the inverse quote is:

\[
\text{bid}_{USD/EUR}=\frac{1}{1.1010}
\]

\[
\text{ask}_{USD/EUR}=\frac{1}{1.0990}
\]

Bid and ask switch when inverting. A system that simply inverts both without switching sides can create an invalid spread.

Forward points must include the vendor’s convention and scale. They are not interchangeable with the outright forward rate.

---

## 4.3 Bond observations and curves

### Individual bond observation

```text
BondMarketObservation
────────────────────────────────────────────────────────
instrument_id
observation_time
settlement_date
observation_type          TRADE | QUOTE | EVALUATED_PRICE
price_type                CLEAN | DIRTY
price
price_basis               PER_100_FACE | CURRENCY_AMOUNT
yield                     optional
yield_convention          required if yield is provided
bid / ask                 where available
source_and_availability
```

### Curve observation

```text
CurveObservation
────────────────────────────────────────────────────────
curve_id
curve_date
currency
curve_type                PAR_YIELD | ZERO_RATE | DISCOUNT_FACTOR
tenor_or_cashflow_date
value
unit
compounding_convention
day_count_convention
instrument_universe
source_and_availability
```

### Derived curve

```text
DerivedCurve
────────────────────────────────────────────────────────
derived_curve_id
input_observation_ids
construction_model_id
construction_version
valuation_date
interpolation_method
extrapolation_method
discount_factors[]
diagnostics
```

The [US Treasury explains](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/interest-rates-frequently-asked-questions) that its published daily reference curve is a **par curve**, and that it does not publish daily zero-coupon curve rates. A model cannot label the par yield as a zero rate without a justified transformation.

A curve transformation must record:

- Input instruments or published curve nodes.
- Compounding and day-count assumptions.
- Interpolation and extrapolation.
- Fit errors.
- Whether the derived curve satisfies required constraints.

---

# 5. Forecast model interfaces

A model is more than a function name. ConnectedModels needs both a **declaration** and a **runtime interface**.

## 5.1 `ModelDefinition`

```text
ModelDefinition
────────────────────────────────────────────────────────
model_id
version
description
model_class                BASELINE | STATISTICAL | FUNDAMENTAL | PRICING
input_schema
output_schema
supported_instruments
supported_horizons
supported_measures
training_method
required_data
optional_data
assumptions
known_limitations
validation_report_id
implementation_digest
```

Examples:

```text
historical-return-bootstrap / 1.0
equity-factor-model / 1.0
dynamic-nelson-siegel / 1.0
bond-discounted-cash-flow / 1.0
fx-random-walk / 1.0
```

A model’s declaration should say whether it is:

- Estimated from historical data.
- Calibrated to current market prices.
- Mechanically applying contractual rules.
- Given as a user-defined scenario.

Those operations have different meanings and validation requirements.

## 5.2 `FittedModel`

```text
FittedModel
────────────────────────────────────────────────────────
fitted_model_id
model_definition_id
training_snapshot_id
training_end_time
parameters
parameter_uncertainty_reference
estimation_diagnostics
fit_status
created_at
```

A fitted model must not use observations whose availability falls after the forecast origin under the selected policy.

## 5.3 Pythonic interface sketch

This is an **interface sketch**, not runnable forecasting code: `DataSnapshot`, `ScenarioSet`, and related types stand for the schemas defined here.

```python
from typing import Protocol, TypeVar

FitInput = TypeVar("FitInput")
Fitted = TypeVar("Fitted")
PredictInput = TypeVar("PredictInput")
ModelOutput = TypeVar("ModelOutput")


class TrainableModel(Protocol[FitInput, Fitted]):
    def fit(
        self,
        data: FitInput,
        *,
        context: "RunContext",
    ) -> Fitted:
        """Fit using only the information allowed by context."""


class ScenarioModel(Protocol[Fitted, PredictInput, ModelOutput]):
    def predict(
        self,
        fitted: Fitted,
        inputs: PredictInput,
        *,
        scenarios: "ScenarioSet",
        context: "RunContext",
    ) -> ModelOutput:
        """Produce scenario-indexed outputs with declared units."""


class PricingModel(Protocol[PredictInput, ModelOutput]):
    def price(
        self,
        inputs: PredictInput,
        *,
        scenarios: "ScenarioSet",
        context: "RunContext",
    ) -> ModelOutput:
        """Map scenario inputs and instrument terms to scenario outputs."""
```

Possible concrete implementations:

```text
HistoricalReturnBootstrap.fit(...)
HistoricalReturnBootstrap.predict(...)

EquityFactorModel.fit(...)
EquityFactorModel.predict(...)

DynamicNelsonSiegel.fit(...)
DynamicNelsonSiegel.predict(...)

BondDiscountedCashFlow.price(...)
```

A mechanical bond-pricing model need not have a `fit` step. Conversely, a factor model generally needs a fitted parameter object.

## 5.4 `RunContext`

```text
RunContext
────────────────────────────────────────────────────────
run_id
forecast_origin
target_time
data_snapshot_id
availability_policy_id
calendar_versions
probability_measure
scenario_purpose
random_seed_or_stream_definition
numeric_conventions
code_version
```

For reproducibility, a seed alone may not be enough: record the random-number algorithm, stream allocation, model versions and execution environment as needed.

---

# 6. Scenario and model-output interfaces

## 6.1 `ScenarioSet`

```text
ScenarioSet
────────────────────────────────────────────────────────
scenario_set_id
forecast_origin
time_grid[]
scenario_ids[]
weights[]
measure
purpose
variables[]
dependence_description
random_stream_reference
generation_model_id
```

Each variable should declare:

```text
variable_id
subject_id
unit
dimensions               scenario × time × optional tenor
values
source_model_id
status                    GENERATED | OBSERVED | USER_SPECIFIED
```

Example variables:

```text
inflation_US[scenario, time]
USD_short_rate[scenario, time]
EUR_short_rate[scenario, time]
EURUSD_spot[scenario, time]
Treasury_zero_curve[scenario, time, tenor]
company_revenue[scenario, time]
equity_risk_premium[scenario, time]
```

### Scenario IDs must stay aligned

Suppose the generator emits:

| Scenario | US rate | USD/EUR | Company margin |
|---|---:|---:|---:|
| 1 | 5.0% | 1.05 | 12% |
| 2 | 3.0% | 1.15 | 18% |

The stock, FX and bond models must consume **scenario 1 together** and **scenario 2 together**. Randomly pairing the rate from scenario 1 with the margin from scenario 2 would destroy the specified dependence.

For weighted scenarios:

\[
\sum_{s=1}^{N}w_s=1,\qquad w_s\geq0
\]

A threshold probability is:

\[
\widehat P(P_T>K)
=
\sum_{s=1}^{N}
w_s\mathbf 1(P_T^{(s)}>K)
\]

For user-defined stresses, weights may be absent. In that case, the system should not report a probability.

## 6.2 `ModelOutput`

```text
ModelOutput
────────────────────────────────────────────────────────
output_id
model_run_id
variable_id
subject_id
unit
scenario_set_id
scenario_values or data_reference
validity_status
diagnostics
assumptions
lineage_refs[]
```

Any transformation between model outputs and inputs should be a named adapter, such as:

```text
ParYieldCurve → DerivedDiscountCurve
TotalReturn + CashFlowLedger → AsTradedPrice
FXQuote[EUR/USD] → FXQuote[USD/EUR]
BondDirtyPrice + AccruedInterest → BondCleanPrice
```

Adapters validate both units and economic meaning.

---

# 7. Model graph and dependency rules

Represent a pipeline as a directed acyclic graph for a particular run:

```text
Node = model invocation or explicit transformation
Edge = typed output consumed as typed input
```

Example:

```text
Historical prices ─────→ Equity factor fit ───────────────┐
                                                          │
Macro history ─────────→ Joint scenario model ────────────┼─→ Equity price
                                                          │
Corporate-action terms → Share/cash-flow ledger ──────────┘
```

A graph validator should reject:

- A `PAR_YIELD` passed where `DISCOUNT_FACTOR` is required.
- EUR/USD data passed into a USD/EUR model without an adapter.
- A risk-neutral scenario passed to a physical forecast without an explicit conversion model.
- Scenario arrays with mismatched IDs or time grids.
- A future filing used as an input at an earlier forecast origin.
- A total-return series labeled as a share-price series.
- A future as-traded price forecast that ignores a known split without declaring that omission.

## Avoid double counting

A graph can be syntactically valid yet economically inconsistent.

For example:

```text
Inflation scenario
→ interest-rate scenario
→ equity discount rate

Inflation scenario
→ a second independently estimated discount-rate shock
```

If both shocks represent the same mechanism, the result can double count inflation’s effect.

Each node should declare:

- Which mechanisms it represents.
- Which inputs already contain those effects.
- Whether the node is conditional on another scenario.
- Whether its residual is independent, correlated or unspecified.

Graph validation can flag likely overlaps, but economic review remains necessary.

---

# 8. Stock forecasting pipeline

## 8.1 Data needed

At minimum:

```text
Instrument identity and share class
Current observable price
Historical prices and corporate actions
Market and factor returns, if using a factor model
```

For a fundamental model, add:

```text
Point-in-time issuer financial statements
Share count and dilution information
Debt, cash and other claims
Business-driver assumptions or models
```

Potential sources include [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), appropriately licensed market data, and the [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library.html). Source accessibility does not guarantee complete point-in-time coverage for every field.

## 8.2 Pipeline A: factor-return forecast

```text
Price and corporate-action history
        ↓
Historical return construction
        ↓
Equity-factor model fitting
        ↓
Joint factor scenarios + idiosyncratic shocks
        ↓
Scenario total returns
        ↓
Corporate-action and cash-flow ledger
        ↓
Future as-traded price and/or total return
```

### Factor model

For stock \(i\):

\[
R_{i,t}-R_{f,t}
=
\alpha_i+\boldsymbol\beta_i^\top\mathbf f_t+\epsilon_{i,t}
\]

The interface needs to specify:

- Whether returns are arithmetic or logarithmic.
- Whether the return is price-only or total return.
- The return period and currency.
- How factors and residual shocks are jointly sampled.
- The estimation window and parameter uncertainty.

### Price conversion

If modeling total return, the cash-flow ledger must transform it to the requested price target consistently.

For a **single-period, no-reinvestment illustration**, where \(D_T\) is the cash distribution per original share:

\[
P_T=P_t(1+R^{total}_{t,T})-D_T
\]

This simplified expression does not handle splits, multiple payment dates, reinvestment or terminal events. Production logic should use the full event ledger.

## 8.3 Pipeline B: fundamentals and market-price bridge

```text
Macro and industry scenarios
        ↓
Revenue, margins and reinvestment scenarios
        ↓
Future free cash flow scenarios
        ↓
Future discount-rate scenarios
        ↓
Future enterprise and equity values
        ↓
Diluted-share and claim adjustments
        ↓
Market-price/value relationship model
        ↓
Future market-price distribution
```

A simplified future enterprise-value scenario is:

\[
EV_T^{(s)}
=
\sum_{k=1}^{N}
\frac{FCFF_{T+k}^{(s)}}
     {(1+WACC_T^{(s)})^k}
+
\frac{TV_{T+N}^{(s)}}
     {(1+WACC_T^{(s)})^N}
\]

\[
V_T^{(s)}
=
\frac{
EV_T^{(s)}
-\text{net debt}_T^{(s)}
-\text{other claims}_T^{(s)}
+\text{non-operating assets}_T^{(s)}
}
{\text{diluted shares}_T^{(s)}}
\]

A separate market-price model is required:

\[
P_T^{(s)}=V_T^{(s)}e^{z_T^{(s)}}
\]

Here \(z_T\) represents a market/value gap. Its behavior must be estimated or explicitly assumed. The system must not assume that modeled value and market price converge unless that assumption is declared and supported.

### Stock-specific output states

```text
PRICE_OBSERVED_ON_TARGET_DATE
ACQUIRED_OR_MERGED
DELISTED
BANKRUPTCY_OR_REORGANIZATION
TARGET_PRICE_UNAVAILABLE
```

A forecast distribution can include probabilities for terminal states separately from the distribution conditional on a future tradable quote. It should not quietly discard failed or delisted firms.

---

# 9. FX forecasting pipeline

## 9.1 Data needed

```text
Spot observations with quote direction
Interest-rate or discount-curve observations in both currencies
Relevant macroeconomic vintages
Forward quotes, if used
Applicable market and settlement calendars
```

One public reference-rate source is [Federal Reserve H.10](https://www.federalreserve.gov/releases/h10/hist/). Its reference rates are not a complete record of executable OTC quotes.

## 9.2 Pipeline A: physical spot forecast

```text
Spot history
   ├──→ Random-walk baseline
   │
   └──→ Return and volatility model
              ↑
Macro and rate scenarios
              ↓
Joint FX return scenarios
              ↓
Future spot distribution
```

A simple model is:

\[
\log S_T
=
\log S_t+\mu_{t,T}+\epsilon_{t,T}
\]

where:

- \(S\) is explicitly USD per EUR.
- \(\mu_{t,T}\) and \(\epsilon_{t,T}\) are generated under the physical measure.
- Their units and horizon are declared.

The simplest baseline sets the forecast median of the future log spot equal to the current log spot. If the distribution is lognormal, that does **not** imply the arithmetic expected spot is exactly unchanged.

## 9.3 Pipeline B: forward pricing reference

With consistent discount factors and idealized no-arbitrage assumptions:

\[
F_{t,T}
=
S_t
\frac{DF_{\mathrm{EUR}}(t,T)}
     {DF_{\mathrm{USD}}(t,T)}
\]

for \(S_t\) measured in USD per EUR.

This is a pricing relationship, not automatically a physical forecast of future spot. Market forwards may also reflect collateral conventions, basis, bid–ask and other details.

The interface should distinguish:

```text
FX_SPOT_FORECAST[PHYSICAL]
FX_FORWARD_PRICE[PRICING]
FX_FORWARD_QUOTE[OBSERVED]
```

A pricing-model output should never be silently relabeled as `EXPECTED_FUTURE_SPOT`.

---

# 10. Bond forecasting pipeline

## 10.1 Data needed

```text
Exact bond terms and cash-flow schedule
Observed bond price and settlement date
Historical curve observations
Curve construction conventions
Calendar and day-count rules
```

For corporate bonds, additionally:

```text
Issuer financial data
Credit spreads or bond prices
Default and recovery information
Liquidity and optionality information
```

The Federal Reserve’s [nominal yield-curve dataset](https://www.federalreserve.gov/data/nominal-yield-curve.htm) is one possible source for fitted US Treasury curve information. Its methodology and conventions should be carried into the data registry.

## 10.2 Pipeline

```text
Bond terms
   ↓
Contractual cash-flow schedule ──────────────────┐
                                                 │
Historical curve observations                    │
   ↓                                             │
Curve construction and quality checks            │
   ↓                                             │
Curve factor model                               │
   ↓                                             │
Joint future zero-curve scenarios ────────────────┤
                                                 ↓
                                    Discount remaining cash flows
                                                 ↓
                                         Future dirty price
                                                 ↓
                                    Accrued-interest calculation
                                                 ↓
                                         Future clean price
```

### Future discounting

For scenario \(s\):

\[
P_{T,\text{dirty}}^{(s)}
=
\sum_{k:T_k>T}
CF_k^{(s)}DF^{(s)}(T,T_k)
\]

\[
P_{T,\text{clean}}^{(s)}
=
P_{T,\text{dirty}}^{(s)}
-
AI_T^{(s)}
\]

The pricing model must know whether the target date is before or after a coupon payment and how the bond’s settlement convention handles accrued interest.

### Curve forecast

A dynamic Nelson–Siegel model is one possible upstream component:

\[
y_t(\tau)
=
\beta_{0,t}
+
\beta_{1,t}
\frac{1-e^{-\lambda\tau}}{\lambda\tau}
+
\beta_{2,t}
\left(
\frac{1-e^{-\lambda\tau}}{\lambda\tau}
-e^{-\lambda\tau}
\right)
\]

A separate model forecasts the factor vector. The output must then be transformed into discount factors using its declared rate and compounding convention.

Dynamic Nelson–Siegel is an example—not the only admissible model, and not automatically an arbitrage-free one.

## 10.3 Bond return versus price

If the requested target is holding-period return, add:

```text
Purchase dirty price
→ coupon cash flows received
→ reinvestment convention
→ future sale dirty price
→ holding-period return
```

A future clean price alone omits coupon income.

For corporate bonds, the model also needs explicit default and recovery states. A risk-free discount curve plus contractual coupons is not sufficient to model a defaultable bond’s future price.

---

# 11. Example joint scenario handoff

Suppose a user requests a one-year forecast for:

1. An equity priced in USD.
2. EUR/USD spot, quoted USD per EUR.
3. A fixed-rate USD Treasury bond.

The scenario generator might output:

```json
{
  "scenario_set_id": "joint-example-001",
  "measure": "PHYSICAL",
  "purpose": "FORECAST",
  "target_date": "2027-01-04",
  "scenarios": [
    {
      "scenario_id": "s1",
      "weight": 0.5,
      "variables": {
        "USD_short_rate_decimal": 0.05,
        "EUR_short_rate_decimal": 0.03,
        "EURUSD_spot_usd_per_eur": 1.05,
        "company_operating_margin_decimal": 0.12,
        "equity_risk_premium_decimal": 0.06,
        "usd_zero_curve_id": "curve-s1"
      }
    },
    {
      "scenario_id": "s2",
      "weight": 0.5,
      "variables": {
        "USD_short_rate_decimal": 0.03,
        "EUR_short_rate_decimal": 0.025,
        "EURUSD_spot_usd_per_eur": 1.15,
        "company_operating_margin_decimal": 0.18,
        "equity_risk_premium_decimal": 0.045,
        "usd_zero_curve_id": "curve-s2"
      }
    }
  ]
}
```

These are fictional values, not a fitted forecast. Two scenarios are not sufficient for a useful predictive distribution; they merely illustrate the interface.

The downstream models return:

```text
Stock model:
    s1 → equity price or terminal state
    s2 → equity price or terminal state

FX model:
    s1 → 1.05 USD/EUR
    s2 → 1.15 USD/EUR

Bond model:
    s1 + curve-s1 + bond terms → clean and dirty prices
    s2 + curve-s2 + bond terms → clean and dirty prices
```

Because scenario IDs align, a portfolio model could later combine the outputs without losing their joint dependence. Such a portfolio model is separate from this forecasting interface.

---

# 12. Orchestration contract

A forecast runner should follow this sequence:

```text
1. Validate the request and resolve the exact instrument and target.
2. Resolve security terms valid for the relevant dates.
3. Construct an as-of data snapshot under the chosen availability policy.
4. Validate source coverage, units, calendars and conventions.
5. Fit or retrieve model versions trained only on permitted data.
6. Generate a joint scenario set.
7. Run instrument-specific pricing and cash-flow models.
8. Aggregate scenario outputs into requested summaries.
9. Attach diagnostics, lineage and validation information.
10. Persist the run manifest and immutable result.
```

Pythonic pseudocode:

```python
def run_forecast(request, registry, data_store, model_graph):
    instrument = registry.resolve_instrument(
        request.instrument_id,
        as_of=request.forecast_origin,
    )

    snapshot = data_store.build_snapshot(
        requirements=model_graph.data_requirements(request, instrument),
        as_of=request.forecast_origin,
        availability_policy=request.availability_policy_id,
    )

    model_graph.validate(
        request=request,
        instrument=instrument,
        snapshot=snapshot,
    )

    context = make_run_context(request, snapshot)

    fitted_nodes = model_graph.fit_required_nodes(
        snapshot=snapshot,
        context=context,
    )

    scenario_set = model_graph.generate_joint_scenarios(
        fitted_nodes=fitted_nodes,
        snapshot=snapshot,
        context=context,
    )

    scenario_outputs = model_graph.evaluate(
        instrument=instrument,
        fitted_nodes=fitted_nodes,
        scenarios=scenario_set,
        context=context,
    )

    return summarize_and_record(
        request=request,
        snapshot=snapshot,
        scenarios=scenario_set,
        outputs=scenario_outputs,
        context=context,
    )
```

The graph is responsible for ensuring that upstream outputs satisfy downstream input schemas. The orchestrator does not assume every pipeline has the same nodes.

---

# 13. Forecast result and provenance schema

```text
ForecastResult
────────────────────────────────────────────────────────
forecast_id
request_id
instrument_id
target_definition
forecast_origin
target_time
measure
purpose
data_snapshot_id
model_graph_version
scenario_set_id
summary_statistics
threshold_probabilities
terminal_state_probabilities
diagnostics
warnings
validation_report_id
lineage_manifest_id
```

Example:

```json
{
  "forecast_id": "result-001",
  "request_id": "forecast-001",
  "measure": "PHYSICAL",
  "purpose": "FORECAST",
  "target": {
    "field": "OFFICIAL_CLOSE",
    "unit": "USD_PER_SHARE",
    "adjustment": "AS_TRADED"
  },
  "summary": {
    "p10": 82.0,
    "median": 105.0,
    "p90": 132.0
  },
  "threshold_probabilities": [
    {
      "operator": "GT",
      "threshold": 120.0,
      "probability": 0.20
    }
  ],
  "warnings": [
    "Illustrative values only; not a calibrated forecast."
  ],
  "data_snapshot_id": "snapshot-example",
  "model_graph_version": "equity-example-v1",
  "validation_report_id": null
}
```

These figures are fictional. In a real result, the distribution should include or explicitly separate any probability that the requested observable does not exist.

## Provenance graph

Each output should be traceable backward:

```text
Forecast p90
  → scenario price distribution
  → equity price model v1
  → factor scenarios and corporate-action ledger
  → fitted factor model and input observations
  → source records and availability evidence
```

This makes it possible to answer:

> “Which observations and assumptions most affected this forecast?”

It also makes corrections possible without silently rewriting old results: a new input revision produces a new snapshot and, if rerun, a new forecast.

---

# 14. Validation and backtesting schemas

## 14.1 `BacktestDefinition`

```text
BacktestDefinition
────────────────────────────────────────────────────────
backtest_id
forecast_origins
horizon
instrument_universe
universe_membership_policy
availability_policy
training_window_policy
model_graph_versions
benchmark_definitions
target_observation_rule
scoring_rules
```

For equities, `instrument_universe` should be point-in-time and include delisted or failed securities where the research question requires them.

## 14.2 `BacktestObservation`

```text
BacktestObservation
────────────────────────────────────────────────────────
forecast_id
target_time
target_observation_id
realized_value
target_status
data_revision_policy
scoring_eligibility
```

If the requested future close is unavailable because of delisting, the evaluation protocol must specify how that state is scored. Excluding such cases without reporting them can create survivorship bias.

## 14.3 `ValidationReport`

```text
ValidationReport
────────────────────────────────────────────────────────
validation_report_id
model_graph_version
evaluation_period
number_of_forecasts
number_of_instruments
missing_target_rate
benchmark_results
point_error_metrics
distribution_scores
interval_coverage
calibration_by_horizon
calibration_by_regime
limitations
```

Recommended minimum comparisons:

| Forecast | Baseline |
|---|---|
| Stock price | No-change price and an appropriate historical-return baseline |
| FX spot | No-change spot / random walk |
| Bond price | No-change price and a clearly specified yield-curve baseline |
| Volatility | Rolling historical volatility |

For probabilistic forecasts, evaluate:

- Coverage of stated intervals.
- Proper distribution scores such as CRPS.
- Threshold-event Brier scores where relevant.
- Results by forecast horizon and regime.

Overlapping forecast horizons create dependent errors; uncertainty estimates and model comparisons should account for that dependence.

---

# 15. Failure handling and uncertainty

The platform should be able to return:

```text
COMPLETE
COMPLETE_WITH_WARNINGS
PARTIAL
UNSUPPORTED
INVALID_INPUT
INSUFFICIENT_DATA
FAILED
```

Examples:

- **Missing dividend model:** A total-return forecast exists, but conversion to future as-traded stock price is `PARTIAL`.
- **Missing curve conventions:** Bond pricing is `INVALID_INPUT`, not an estimate based on an assumed zero curve.
- **Unknown filing availability:** Exclude it under the conservative policy or label the backtest uncertain.
- **Unsupported callable bond:** `UNSUPPORTED`, rather than treating the bond as noncallable.
- **Sparse data:** Report insufficient history or a wider, explicitly assumption-dependent result rather than a falsely precise distribution.

## Separate uncertainty sources

Where feasible, track:

1. **Future shock uncertainty:** variation in simulated economic and market outcomes.
2. **Parameter uncertainty:** uncertainty in fitted coefficients and volatility.
3. **Model uncertainty:** disagreement between defensible model structures.
4. **Data uncertainty:** measurement, revisions, missingness and source quality.
5. **Target uncertainty:** ambiguity or unavailability in the eventual observable.

A Monte Carlo standard error captures only numerical simulation error. It is not the same as these uncertainties.

---

# 16. A practical first implementation boundary

A manageable first version could support:

### Instruments

- Listed ordinary equity shares.
- Spot FX pairs with explicit quote direction.
- Fixed-rate, noncallable government bonds.

### Models

- Equity: no-change and historical-return baselines.
- FX: random-walk baseline.
- Bond: no-change benchmark plus a curve-scenario and cash-flow-pricing pipeline.
- One joint-scenario interface shared across all three.

### Data infrastructure

- Instrument registry.
- Immutable observations and vintage-aware snapshots.
- Corporate-action ledger.
- Curve conventions and derived-curve lineage.
- Forecast and validation records.

### Explicit exclusions

- Automatic claims of trading profitability.
- Derivative pricing or risk-neutral-to-physical conversion.
- Callable and complex structured bonds.
- Unverified causal intervention forecasts.
- Production use before point-in-time backtesting.

That scope tests the central idea—**typed, auditable model connections**—without requiring every financial model to be built first.

---

## Bottom line

The crucial interfaces are:

1. **A precise target:** what future observable is being forecast.
2. **A point-in-time snapshot:** what information was available and under which policy.
3. **A typed model contract:** inputs, outputs, units, assumptions and measure.
4. **A shared scenario set:** aligned shocks and dependencies across models.
5. **An instrument-specific pricing or cash-flow model:** the mechanical mapping to the requested target.
6. **A result with lineage and backtest evidence:** what was produced, why, and how well the approach has worked.