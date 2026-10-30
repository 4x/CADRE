---
id: source-outsider-prediction-market-data-and-model-suggestions
type: source
title: "Outsider Prediction-Market Data and Model Suggestions"
summary: "Imported data links and proposed formulas for 26 market examples, plus an unchanged synthetic Python attachment; neither data access nor forecast validity verified."
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
    target: idea-prediction-market-question-catalog
  - type: relates-to
    target: source-outsider-prediction-market-examples
  - type: relates-to
    target: source-outsider-prediction-market-difficulty-ranking
  - type: relates-to
    target: question-evaluation-and-reference-evidence
---

# Outsider Prediction-Market Data and Model Suggestions

## Provenance and interpretation

Claims about actual data sources, retrieval availability, formulas and contract rules are attributed to the outsider; no fresh retrieval, fitting, calibration or backtesting was performed. The ten-pipeline Python file is a source attachment, NOT Connected Models application code or a validated registry. Monte Carlo standard error in that file is simulation noise only. Its sample inputs are fictional.

- Imported on 2026-10-29 from `Queue/DataAndModels.md`.
- Created/updated metadata dates describe this source record, not the original document.
- Original payload SHA-256 (including original line endings): `aa9ca687017158feb3762969f81da3890d17c9b98f3d4c4862786f4148f35192`.
- The original payload follows unchanged after the marker; line references to the original are relative to that payload.
- User clarification, 2026-10-29: Queue contains candidate questions and outsider thoughts, NOT prescriptive solutions. The outsider's identity, generation process, and full conversation provenance are not supplied; no author or model is inferred.

## Retained code attachment

[market_pipelines.py](attachments/market_pipelines.py) was moved byte-for-byte from `Queue/market_pipelines.py`. All bare references/import examples in the original text refer to this attachment; their historical text is unchanged. It uses local inputs and does not download data. It was not executed, validated or adopted during organization. Attachment original SHA-256: `6c1e48cf93d1dbb8e43c3b98e6843a5f7ea2088d931989f5b9e0152de2c317ac`.

## Original document (verbatim)

<!-- ORIGINAL DOCUMENT:BEGIN -->

#  For every market below:
- **Actual data sources** that can be retrieved.
- An explicit **model or formula** for turning those data into a forecast.
- The main qualification about whether the data match the settlement question.

For the top 10, also executable Python pipelines in market_pipelines.py. Each pipeline connects separate modeling stages and accepts locally supplied inputs.

> **Important:** The code is a reference implementation, not a validated forecasting system. It does not download data, fit every upstream model, or produce forecasts from real observations on its own. Its demonstration inputs are fictional. In particular, inputs described as *nowcasts*, *forecast errors*, *Elo ratings* or *joint scenarios* must first be estimated from actual point-in-time data.

The numbers above are **illustrative only**. In a real run, `errors_pct` should contain historical errors calculated as:

\[
e_t =
\text{first published value}_t
-
\text{forecast available at the same lead time}_t
\]

The file’s `demo_inputs()` function shows the input structure for all ten markets. It can also be imported:

```python
from market_pipelines import forecast_cpi, forecast_nfl_game

cpi_result = forecast_cpi(cpi_data, draws=20_000, seed=1)
game_result = forecast_nfl_game(game_data, draws=20_000, seed=1)

print(cpi_result)
print(game_result)
```

The main architecture is:

```text
Local historical/forecast inputs
        ↓
Domain or scenario model
        ↓
Measurement / publication model
        ↓
Contract settlement rule
        ↓
Monte Carlo expected payout
```

For most of these contracts, expected payout equals the probability of Yes. The football game is different because a tie pays $0.50.

The reported Monte Carlo standard error measures **simulation noise only**. It does not quantify forecast-model uncertainty, bad data, structural changes, settlement disputes or model bias.

---

# 1. Central Park rain

**Contract:** A qualifying rain code appears in a KNYC observation on the specified date.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/rain-daily-2026-10-29)

## Actual data

1. **Current KNYC METAR observations:** [NOAA Aviation Weather Center API](https://aviationweather.gov/api/data/metar?ids=KNYC&format=raw&hours=24).
2. **Historical raw station observations:** [Iowa Environmental Mesonet ASOS/METAR download](https://mesonet.agron.iastate.edu/request/download.phtml?network=NY_ASOS). Select KNYC and retain raw METAR text.
3. **Ensemble weather forecasts:** [NOAA GEFS public data](https://registry.opendata.aws/noaa-gefs/).
4. **Historical forecast context:** [NOAA GEFS archive information](https://www.ncei.noaa.gov/products/weather-climate-models/global-ensemble-forecast). Its reforecasts are not the same as forecasts actually available on historical forecast dates.

## Model

For weather scenario \(s\), let \(q_{s,t}\) be the probability that observation \(t\) contains a **qualifying** rain code. Under conditional independence across observations:

\[
P(Y=1\mid s)
=
1-\prod_{t=1}^{T}(1-q_{s,t})
\]

Average over scenarios:

\[
P(Y=1)
\approx
\frac{1}{S}\sum_{s=1}^{S}
\left[
1-\prod_{t=1}^{T}(1-q_{s,t})
\right]
\]

The \(q_{s,t}\) values can be estimated using a station-level model connecting ensemble precipitation type and timing to historical METAR codes. For example:

\[
q_{s,t}
=
P(\text{rain at station}\mid s,t)
\times
P(\text{qualifying code}\mid\text{rain},s,t)
\]

with a possible false-positive term.

## Python pipeline

```text
Joint weather scenarios
→ StationObservationModel
→ Settlement
→ MonteCarlo
```

Implemented by `forecast_rain`.

**Critical limitation:** The code accepts already estimated per-observation code probabilities; it does **not** fit the weather-to-METAR model. It assumes conditional independence between observations within each scenario. It also assumes inputs already obey the contract’s code, station and local-standard-time rules.

---

# 2. Monthly CPI

**Contract:** The first-published seasonally adjusted monthly CPI-U change is strictly above −0.2%.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/uscpi-october-mom-2026-11-10)

## Actual data

1. [BLS CPI data](https://www.bls.gov/cpi/data.htm), including seasonally adjusted all-items CPI-U series `CUSR0000SA0`.
2. [BLS CPI release archive](https://www.bls.gov/bls/news-release/cpi.htm), for contemporaneous first releases.
3. [Cleveland Fed Inflation Nowcasting](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting).
4. [BLS seasonal adjustment documentation](https://www.bls.gov/cpi/seasonal-adjustment/), important because historical seasonally adjusted values can be revised.

## Model

Let \(\hat{x}_t\) be the nowcast and \(e_i\) a historical, out-of-sample first-release error at the same forecast horizon:

\[
X_t^*=\hat{x}_t+e_i
\]

Apply the reporting transformation \(R\), then the contract condition:

\[
P(Y=1)
=
P\!\left(R(X_t^*)>-0.2\right)
\]

An empirical estimate is the fraction of bootstrapped errors for which the condition holds.

## Python pipeline

```text
CPI nowcast
→ EmpiricalErrorModel
→ PublishedEstimateModel
→ strict threshold
→ MonteCarlo
```

Implemented by `forecast_cpi`.

**Critical limitation:** The code uses an illustrative one-decimal rounding rule. Verify the precise source and exchange treatment before using it for a contract. Current BLS series alone are not a reliable substitute for first-release historical vintages.

---

# 3. Next SOFR publication

**Contract:** The initially reported SOFR is at most 3.85%.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXSOFRD-26OCT27?with_nested_markets=true) · **Retrospective**

## Actual data

1. [New York Fed SOFR page](https://www.newyorkfed.org/markets/reference-rates/sofr).
2. [New York Fed Markets API documentation](https://markets.newyorkfed.org/static/docs/markets-api.html).
3. [Example historical SOFR API query](https://markets.newyorkfed.org/api/rates/secured/sofr/search.json?startDate=2024-01-01&endDate=2024-01-10).
4. [SOFR methodology and revisions](https://www.newyorkfed.org/markets/reference-rates/additional-information-about-reference-rates).

## Model

A simple short-horizon baseline is:

\[
\widehat{\text{SOFR}}_t
=
\alpha+\beta\text{SOFR}_{t-1}+\gamma^\top z_t
\]

where \(z_t\) might include known funding and calendar conditions. Bootstrap historical first-release forecast errors:

\[
\text{SOFR}_t^*=\widehat{\text{SOFR}}_t+e_i
\]

\[
P(Y=1)=P(R(\text{SOFR}_t^*)\leq3.85)
\]

## Python pipeline

Implemented by `forecast_sofr`, using:

```text
SOFR point nowcast
→ first-publication residual model
→ reported rate
→ inclusive ≤ 3.85 rule
```

**Critical limitation:** The code consumes the point nowcast; it does not estimate the regression. A historical API pull may contain revised rates, so save dated observations or otherwise reconstruct first-publication values.

---

# 4. Annual GDP growth

**Contract:** First-published annual real GDP growth is from 1.6% through 2.0%, inclusive.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXGDPYEAR-26?with_nested_markets=true)

## Actual data

1. [BEA GDP data](https://www.bea.gov/data/gdp/gross-domestic-product).
2. [BEA dated news-release archive](https://www.bea.gov/news/archive), including advance estimates.
3. [Atlanta Fed GDPNow](https://www.atlantafed.org/research-and-data/data/gdpnow), including historical model forecasts.
4. [GDPNow methodology](https://www.atlantafed.org/research-and-data/data/gdpnow/explainer).

## Model

Given consistent quarterly real GDP levels:

\[
\bar G_y=\frac{1}{4}\sum_{q=1}^{4}G_{y,q}
\]

\[
g_y=100\left(\frac{\bar G_y}{\bar G_{y-1}}-1\right)
\]

For each joint quarterly scenario, apply any remaining first-release error and the published-value transformation:

\[
P(Y=1)=P(1.6\leq R(g_y^*)\leq2.0)
\]

**Do not** substitute Q4-over-Q4 growth or a quarterly annualized rate for annual-average growth.

## Python pipeline

```text
Joint quarterly GDP-level scenarios
→ AnnualGDPModel
→ first-release error
→ rounding
→ inclusive 1.6–2.0 bracket
```

Implemented by `forecast_gdp`.

**Critical limitation:** The supplied quarterly scenarios must already be joint and internally consistent. The error term should represent only uncertainty **not already included in those scenarios**; otherwise the pipeline double-counts uncertainty.

---

# 5. Monthly nonfarm payrolls

**Contract:** First-reported October nonfarm payroll growth is above 50,000 jobs.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXPAYROLLS-26OCT?with_nested_markets=true)

## Actual data

1. [BLS Employment Situation release archive](https://www.bls.gov/bls/news-release/empsit.htm).
2. [BLS CES vintage-data files](https://www.bls.gov/web/empsit/cesvindata.htm).
3. [Total nonfarm vintage spreadsheet](https://www.bls.gov/web/empsit/cesvin00.xlsx).
4. [BLS CES vintage methodology](https://www.bls.gov/web/empsit/cesvininfo.htm).

## Model

One option is a dynamic-factor model:

\[
z_t=A z_{t-1}+\eta_t
\]

\[
x_t=\Lambda z_t+\epsilon_t
\]

\[
\Delta N_t=\alpha+\beta^\top z_t+u_t
\]

Here \(x_t\) contains timely labor indicators, \(z_t\) is the latent labor-market state and \(\Delta N_t\) is payroll growth. Estimate the model using only data available before each release.

The reference implementation uses a simpler interface:

\[
\Delta N_t^*=\widehat{\Delta N}_t+e_i
\]

\[
P(Y=1)=P(R(\Delta N_t^*)>50{,}000)
\]

## Python pipeline

Implemented by `forecast_payrolls`:

```text
Payroll nowcast in jobs
→ historical first-release errors in jobs
→ reporting transformation
→ strict > 50,000 threshold
```

**Critical limitation:** The code does not fit the dynamic-factor model. Historical residuals must be at the same lead time and must use the first release rather than later benchmark revisions.

---

# 6. Hottest October on record

**Contract:** October is the hottest October in the designated NCEI record.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXHMONTH-26OCT?with_nested_markets=true)

## Actual data

1. [NOAA Climate at a Glance global temperature series](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series).
2. [Example global monthly temperature CSV](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/tavg/1/0/1850-2025.csv).
3. [NOAA global rankings](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/rankings/globe/tavg/land_ocean/185001).
4. [NOAAGlobalTemp product information](https://www.ncei.noaa.gov/products/land-based-station/noaa-global-temp).

## Model

For an October anomaly nowcast \(\hat T\):

\[
T^*=\hat T+e_i
\]

\[
P(Y=1)=P(R(T^*)>T_{\text{record}})
\]

The exact handling of equality must follow the full product rule.

## Python pipeline

Implemented by `forecast_hottest_october`:

```text
Monthly anomaly nowcast
→ historical NCEI nowcast errors
→ reported anomaly
→ comparison with previous October record
```

The input requires a `tie_policy` rather than silently guessing.

**Critical limitation:** NOAA products can use different baselines and versions. The nowcast, errors and record must refer to the **same product and anomaly baseline**. The contract’s full ranking and tie rules must be checked.

---

# 7. Seattle–Kansas City game winner

**Contract:** Seattle wins; a tie pays $0.50.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXNFLGAME-26OCT25KCSEA?with_nested_markets=true) · **Retrospective**

## Actual data

1. [nflverse schedules and results CSV](https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv).
2. [nflverse play-by-play documentation](https://nflreadr.nflverse.com/reference/load_pbp.html).
3. [nflverse injury-report documentation](https://nflreadr.nflverse.com/reference/load_injuries.html).
4. [FiveThirtyEight NFL Elo code and historical data](https://github.com/fivethirtyeight/nfl-elo-game).

The nflverse files are community-maintained, not official NFL data feeds. Corrections and injury reports must be aligned to the forecast timestamp.

## Model

For home and away Elo ratings \(R_h,R_a\), home advantage \(H\), and tie probability \(p_T\):

\[
P(\text{home wins}\mid\text{no tie})
=
\frac{1}{1+10^{-(R_h+H-R_a)/400}}
\]

For a selected team:

\[
E[\text{payout}]
=
P(\text{selected team wins})
+
0.5P(\text{tie})
\]

## Python pipeline

```text
Team Elo ratings + home advantage + tie probability
→ EloGameModel
→ win / loss / tie
→ contract payout
```

Implemented by `forecast_nfl_game`.

**Critical limitation:** The code consumes ratings and a tie probability. It does not fit Elo ratings from the historical games or account for cancellation/fair-price settlement.

---

# 8. San Francisco season wins

**Contract:** San Francisco wins more than 8.5 regular-season games.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/nfl-wins-2027-01-10-sf)

## Actual data

1. [nflverse schedules and results](https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv).
2. [FiveThirtyEight NFL Elo implementation](https://github.com/fivethirtyeight/nfl-elo-game).
3. [nflverse injuries](https://nflreadr.nflverse.com/reference/load_injuries.html).

## Model

For each remaining game \(g\), simulate its outcome using Elo. Add a shared season-strength shock:

\[
R_{\text{team}}^*
=
R_{\text{team}}+\epsilon,
\qquad
\epsilon\sim N(0,\sigma_{\text{team}}^2)
\]

The same \(\epsilon\) is used across the remaining schedule:

\[
W_{\text{final}}
=
W_{\text{known}}
+
\sum_g \mathbf{1}(\text{team wins game }g)
\]

\[
P(Y=1)=P(W_{\text{final}}>8.5)
\]

## Python pipeline

Implemented by `forecast_nfl_season`:

```text
Current wins + schedule + team ratings
→ shared team-strength scenario
→ EloGameModel for each game
→ season win total
→ over-8.5 rule
```

**Critical limitation:** The shared Elo shock is an illustrative way to represent dependence. It is not a full injury model or a dynamically updated season simulation.

---

# 9. Real wages versus inflation

**Contract:** The first-published 12-month change in BLS real average hourly earnings is strictly positive.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/usrealwage-v-infl-2026)

## Actual data

1. [BLS Real Earnings release](https://www.bls.gov/news.release/realer.htm).
2. [BLS private-sector all-employee hours and earnings bulk data](https://download.bls.gov/pub/time.series/ce/ce.data.05b.TotalPrivate.AllEmployeeHoursAndEarnings).
3. [BLS all-employee real earnings bulk data](https://download.bls.gov/pub/time.series/ce/ce.data.02b.AllRealEarningsAE).
4. [BLS CPI data](https://www.bls.gov/cpi/data.htm).
5. For workforce-composition analysis: [Census CPS monthly microdata](https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html).

## Model

Let \(w=W_{2026}/W_{2025}\) be the nominal earnings-index ratio and \(c=CPI_{2026}/CPI_{2025}\) the CPI ratio:

\[
g_{\text{real}}
=
100\left(\frac{w}{c}-1\right)
\]

Forecast wage and CPI ratios **jointly**, then apply a release-error and publication layer:

\[
P(Y=1)=P(R(g_{\text{real}}^*)>0)
\]

## Python pipeline

```text
Joint wage/CPI scenarios
→ RealEarningsModel
→ first-release error
→ reported real-earnings change
→ strictly positive rule
```

Implemented by `forecast_real_wages`.

**Critical limitation:** The inputs must preserve wage–inflation dependence and match the BLS measure’s seasonal adjustment and dates. Average hourly earnings can change because the mix of jobs changes, not only because individual workers get raises.

---

# 10. Jordan Love passing yards

**Contract:** More than 3,250.5 official regular-season passing yards.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/nfl-passyds-2027-01-10-jorlov)

## Actual data

1. [nflverse play-by-play files and documentation](https://nflreadr.nflverse.com/reference/load_pbp.html).
2. [nflverse schedules](https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv).
3. [nflverse injury reports](https://nflreadr.nflverse.com/reference/load_injuries.html).
4. [NFL official injury reports](https://www.nfl.com/injuries/).

## Model

For each remaining game:

\[
A_g\sim\operatorname{Bernoulli}(p_g)
\]

\[
Y_g\mid A_g=1
\sim
\operatorname{Gamma}\left(k_g,\frac{\mu_g}{k_g}\right)
\]

Then:

\[
Y_{\text{season}}
=
Y_{\text{already recorded}}
+
\sum_g A_gY_g
\]

\[
P(Y=1)=P(Y_{\text{season}}>3250.5)
\]

Availability and yardage parameters should be estimated from pre-game data and adjusted for matchup, expected pass volume and injury information.

## Python pipeline

```text
Joint remaining-season scenarios
→ PlayerAvailabilityModel
→ PassingYardsModel
→ season total
→ threshold settlement
```

Implemented by `forecast_passing_yards`.

**Critical limitation:** The Gamma model is an illustrative positive-yard baseline and cannot represent a negative passing-yard total. A production implementation should use an empirically calibrated signed/integer game-yard distribution or a play-level model, and explicitly model partial-game participation.

---

# 11. Rotten Tomatoes score

**Contract:** The displayed Tomatometer is above 60 at a specified time.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXRT-HUN?with_nested_markets=true)

## Actual data

- [Rotten Tomatoes historical movie dataset](https://data.mendeley.com/datasets/kbpvrwfp5z/1): third-party historical snapshot, not a point-in-time score history.
- [Rotten Tomatoes licensing](https://www.rottentomatoes.com/help_desk/licensing): route for an authorized feed.

## Model

For positive reviews \(K\) out of \(N\):

\[
\theta\sim\operatorname{Beta}(\alpha,\beta)
\]

\[
K\mid \theta,N\sim\operatorname{Binomial}(N,\theta)
\]

\[
S=R\left(100\frac{K}{N}\right)
\qquad
P(Y=1)=P(S>60)
\]

**Missing model:** \(N\) and the critics who publish by the settlement time are not random draws. Model review arrival and selection by critic. Historical snapshot scores do not establish historical values at the contract timestamp.

---

# 12. Fed decision plus dissent

**Contract:** No rate change **and** more than zero dissents.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXFEDCOMBO-26OCT?with_nested_markets=true) · **Retrospective**

## Actual data

- [Federal Reserve meeting calendar and statements](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm).
- [Federal Reserve historical meeting materials](https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm).
- [Cleveland Fed inflation nowcasts](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting).

## Model

\[
P(Y=1)
=
P(\text{no change})
P(\text{at least one dissent}\mid\text{no change})
\]

A logistic model for the decision could use inflation, employment and policy communications:

\[
\operatorname{logit}P(\text{no change})
=
\alpha+\beta^\top x_t
\]

A separate conditional vote model estimates dissent risk. Voter membership must be correct for each meeting.

**Limitation:** There are few genuinely comparable meetings. The previously retrieved API text had a rule-field inconsistency, so verify the full contract rules before implementing settlement.

---

# 13. Florida Category 4+ hurricane landfall

**Contract:** A hurricane center crosses the specified Florida coastline at Category 4 or above.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXHURRLANDFL4-31DEC26?with_nested_markets=true)

## Actual data

- [NHC HURDAT2 historical track archive](https://www.nhc.noaa.gov/data/hurdat/).
- [NHC track and intensity model guidance](https://www.nhc.noaa.gov/modelsummary.shtml?text).
- [NOAA historical hurricane tracks](https://coast.noaa.gov/hurricanes/).

## Model

Simulate storms, tracks \(L_{s,t}\) and intensities \(I_{s,t}\):

\[
P(Y=1)
\approx
\frac{1}{S}\sum_{s=1}^{S}
\mathbf{1}
\left(
\exists t:
L_{s,t}\text{ crosses qualifying coast}
\land I_{s,t}\geq \text{Cat 4}
\right)
\]

For future unformed storms, add a formation model:

\[
N\sim\operatorname{Poisson}(\lambda)
\]

with track and intensity conditional on formation.

**Limitation:** HURDAT2 is a revised best-track dataset; the contract uses an operational report. The model needs an explicit best-track-to-operational-report layer.

---

# 14. Top US Netflix show

**Contract:** The specified title ranks #1 on Netflix’s US weekly chart.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/ntflx-1shwus-2026-10-20) · **Retrospective**

## Actual data

- [Netflix country weekly rankings TSV](https://www.netflix.com/tudum/top10/data/all-weeks-countries.tsv).
- [Netflix global weekly data TSV](https://www.netflix.com/tudum/top10/data/all-weeks-global.tsv).
- [Netflix Top 10 methodology](https://about.netflix.com/news/top-10-things-about-netflix-top-10).

## Model

A latent-demand ranking model:

\[
D_{i,t}
=
\alpha_i+\beta^\top x_{i,t}+\epsilon_{i,t}
\]

\[
P(Y=1)
=
P(D_{\text{target},t}>\max_{j\ne\text{target}}D_{j,t})
\]

Estimate \(x_{i,t}\) from release age, prior ranks and competing releases.

**Limitation:** The country-level file provides rankings, not US title-level viewing hours. Global viewing is an imperfect proxy for US viewing.

---

# 15. Missouri House margin

**Contract:** Republican nominee wins MO-04 by at least 30 percentage points.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/ushrmov-mo-04-2026-11-03)

## Actual data

- [Missouri Secretary of State election results](https://www.sos.mo.gov/elections/s_default).
- [Missouri previous election results](https://www.sos.mo.gov/elections/resultsandstats/previouselections).
- [FiveThirtyEight polling data](https://github.com/fivethirtyeight/data/tree/master/polls).

## Model

For district vote share:

\[
\operatorname{logit}(v_d)
=
\alpha+\beta^\top x_d+u_d+\epsilon_{\text{national}}
\]

Simulate all candidates’ valid votes, then calculate:

\[
M=\frac{V_{\text{winner}}-V_{\text{runner-up}}}
        {V_{\text{all valid votes}}}
\]

\[
P(Y=1)=P(\text{Republican wins and }M\geq0.30)
\]

**Limitation:** State-certified results are available, but Missouri precinct data may require purchase; district-level current polling may be sparse.

---

# 16. Party with more governorships

**Contract:** Democrats have more governorships than Republicans under the contract’s attribution rules.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/demvrep-2026-11-03)

## Actual data

- [FiveThirtyEight governor polls](https://github.com/fivethirtyeight/data/tree/master/polls).
- [Historical gubernatorial election results](https://github.com/fivethirtyeight/election-results).
- Individual state election-authority results for certified outcomes.

## Model

For state \(i\):

\[
m_i=\hat m_i+\epsilon_{\text{national}}
+\epsilon_{\text{region}(i)}+\epsilon_i
\]

Simulate each race, its runoff if needed, and uncontested-seat attribution:

\[
D=D_{\text{fixed}}+\sum_i\mathbf{1}(\text{Democrat wins }i)
\]

\[
R=R_{\text{fixed}}+\sum_i\mathbf{1}(\text{Republican wins }i)
\]

\[
P(Y=1)=P(D>R)
\]

**Limitation:** Shared errors are essential; treating races as independent can materially distort the count distribution.

---

# 17. Union membership count

**Contract:** The first-reported 2027 union-member count exceeds the 2026 count.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/usunion-rise-2027)

## Actual data

- [BLS Union Members release](https://www.bls.gov/news.release/union2.htm).
- [BLS union tables and historical data](https://www.bls.gov/news.release/union2.toc.htm).
- [Unionstats historical compilation](https://unionstats.com/).
- [CPS microdata](https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html).

## Model

For industry \(j\):

\[
M_t=\sum_j E_{j,t}u_{j,t}
\]

where \(E_{j,t}\) is employment and \(u_{j,t}\) is the union-member share. Add a BLS survey observation layer:

\[
\widehat M_t=M_t+\epsilon_{\text{survey},t}
\]

\[
P(Y=1)=P(\widehat M_{2027}>\widehat M_{2026})
\]

**Limitation:** Model the published count, not just the membership rate. Survey changes and special collection periods can affect comparability.

---

# 18. Solana benchmark price

**Contract:** The designated 60-second average SOL benchmark is at or below $89.99.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/sol-range-day-2026-10-29)

## Actual data

- [Contract-designated CF Benchmarks SOLUSD_RTI](https://www.cfbenchmarks.com/data/indices/SOLUSD_RTI).
- [CoinGecko historical price API documentation](https://docs.coingecko.com/demo/reference/coins-id-market-chart), as a possible **proxy**, subject to access limits.

## Model

A GARCH baseline for returns:

\[
r_t=\mu+\sigma_tz_t
\]

\[
\sigma_t^2
=
\omega+\alpha r_{t-1}^2+\beta\sigma_{t-1}^2
\]

Simulate the index values over the settlement minute:

\[
\bar P=\frac{1}{60}\sum_{j=1}^{60}P_j
\]

\[
P(Y=1)=P(R(\bar P)\leq89.99)
\]

**Limitation:** CoinGecko is not the contract benchmark. Check access rights and index history before using a proxy; model jumps and basis risk separately.

---

# 19. Bitcoin versus gold

**Contract:** Bitcoin outperforms gold over the contract’s specified 2026 measurement period.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXBTCVSGOLD-26?with_nested_markets=true)

## Actual data

- [Contract-designated CF Benchmarks](https://www.cfbenchmarks.com/).
- [Contract-designated ICE data services](https://www.ice.com/fixed-income-data-services).
- [LBMA gold benchmark information](https://www.lbma.org.uk/prices-and-data/lbma-gold-price) and [CoinGecko data](https://docs.coingecko.com/demo/reference/coins-id-market-chart) are possible proxies, **not identical settlement sources**.

## Model

Simulate joint log returns:

\[
\begin{pmatrix}r_B\\r_G\end{pmatrix}
\sim F(\mu,\Sigma,\text{tail parameters})
\]

Using contract start prices \(B_0,G_0\):

\[
P(Y=1)
=
P\left(
\frac{B_T}{B_0}-1
>
\frac{G_T}{G_0}-1
\right)
\]

**Limitation:** Historical benchmark access may be licensed. Verify the contract’s exact start/end observations and use joint rather than independent return scenarios.

---

# 20. OpenRouter market share

**Contract:** OpenAI’s OpenRouter text share exceeds a threshold in the specified weekly publication.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXOPENSHARE-26OCT26?with_nested_markets=true) · **Retrospective**

## Actual data

- [OpenRouter rankings](https://openrouter.ai/rankings).
- [OpenRouter historical token totals API documentation](https://openrouter.ai/docs/api/api-reference/datasets/daily-token-totals-for-top-50-models).

## Model

For OpenAI token share \(s_t\):

\[
\operatorname{logit}(s_t)
=
\alpha+\phi\operatorname{logit}(s_{t-1})
+\beta^\top x_t+\epsilon_t
\]

Aggregate the simulated daily numerator and denominator into the contract’s weekly share:

\[
s_{\text{week}}
=
\frac{\sum_d \text{OpenAI tokens}_d}
     {\sum_d \text{all eligible tokens}_d}
\]

Apply the specified rounding and “Others” rule.

**Limitation:** Confirm the API measure matches the contract’s chart. OpenRouter token share is not overall AI market share.

---

# 21. Best Picture nomination

**Contract:** A specified film is nominated for Best Picture.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXOSCARNOMPIC-27?with_nested_markets=true)

## Actual data

- [Official Academy Awards Database](https://awardsdatabase.oscars.org/).
- [Academy database information](https://www.oscars.org/oscars/awards-databases).
- [Third-party structured Oscar data](https://github.com/DLu/oscar_data).

## Model

For film \(i\), model latent voter support:

\[
\theta_i=\alpha+\beta^\top x_i+\epsilon_i
\]

Simulate the eligible field and nomination procedure using those support levels:

\[
P(Y_i=1)
=
P(\text{film }i\text{ receives a nomination})
\]

**Limitation:** Precursor awards and reviews must be timestamped; current-year data cannot leak into a historical pre-nomination forecast. Check Academy rules for the relevant year.

---

# 22. Top AI leaderboard company

**Contract:** Anthropic holds the top model on the specified Arena leaderboard at the specified time.  
[Polymarket US records](https://gateway.polymarket.us/v1/markets?active=true&categories=technology&limit=5)

## Actual data

- [Arena historical leaderboard dataset](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset).
- [Arena leaderboard](https://huggingface.co/spaces/lmarena-ai/arena-leaderboard).

## Model

If individual pairwise vote data are available, Bradley–Terry gives:

\[
P(i\text{ beats }j)
=
\frac{\exp(\theta_i)}
     {\exp(\theta_i)+\exp(\theta_j)}
\]

Then simulate future model releases and leaderboard observations:

\[
P(Y=1)
=
P\left(\arg\max_i \text{published rank}_i
\text{ belongs to Anthropic}\right)
\]

**Limitation:** The cited historical dataset contains leaderboard snapshots, not necessarily all underlying paired votes. It supports a snapshot-based model, but cannot by itself fit the full pairwise likelihood. Future release timing and quality require a separate model.

---

# 23. State data-center moratorium

**Contract:** Any state enacts a qualifying statewide measure by the deadline.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/anyst-datactrmor)

## Actual data

- [Open States API documentation](https://docs.openstates.org/api-v3/).
- [Open States bulk legislative data](https://open.pluralpolicy.com/data/).
- [Open States data coverage report card](https://open.pluralpolicy.com/reportcard/).
- Relevant state legislature sites for authoritative bill text and enactment status.

## Model

For bill \(b\), model progression through stages \(k\):

\[
P(\text{advance at stage }k)
=
\operatorname{logit}^{-1}(\alpha_k+\beta_k^\top x_b)
\]

Simulate correlated bill paths and apply a legal qualification function \(Q_b\):

\[
P(Y=1)
=
P\left(\exists b:
\text{enacted}_b=1 \land Q_b=1\right)
\]

**Limitation:** Bill amendments can change \(Q_b\). Classification should retain the supporting text and route ambiguous cases to human review.

---

# 24. Ukrainian TPS ends

**Contract:** US Temporary Protected Status for Ukraine ends before the deadline.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXTPSUKR-27?with_nested_markets=true)

## Actual data

- [USCIS Ukraine TPS page](https://www.uscis.gov/humanitarian/temporary-protected-status/TPS-Ukraine).
- [Federal Register extension notice](https://www.federalregister.gov/documents/2025/01/17/2025-00771/extension-of-the-designation-of-ukraine-for-temporary-protected-status).
- Subsequent USCIS and Federal Register notices, plus relevant court orders.

## Model

Construct a time-dependent legal-state model:

\[
S_t\in
\{\text{active},\text{extended},\text{terminated},\text{lapsed},\ldots\}
\]

\[
P(S_{t+1}=j\mid S_t=i,x_t)=p_{ij}(t,x_t)
\]

\[
P(Y=1)=P(\exists t<T:S_t\in\{\text{qualifying termination/lapse}\})
\]

**Limitation:** Transition probabilities may require expert elicitation rather than historical fitting; legal classification must distinguish announcements from effective loss of protection.

---

# 25. Ukraine presidential election

**Contract:** Ukraine holds a presidential election before January 1, 2027.  
[Contract record](https://external-api.kalshi.com/trade-api/v2/events/KXELECTUKRAINE-30JAN01?with_nested_markets=true)

## Actual data

- [Central Election Commission of Ukraine](https://cvk.gov.ua/en/).
- [CEC presidential-election materials](https://cvk.gov.ua/election-of-the-president-of-ukraine.html).
- [IPU election data](https://data.ipu.org/parliament/UA/UA-LC01/election/UA-LC01-E20190721/) as a secondary cross-check.

## Model

Represent necessary institutional transitions:

\[
P(Y=1)
=
P(\text{legal feasibility})
P(\text{scheduled}\mid\text{feasible})
P(\text{held by deadline}\mid\text{scheduled, feasible})
\]

In practice, these are conditional probabilities within a scenario tree that also includes security and operational conditions.

**Limitation:** The formula organizes assumptions; it does not make the conditional probabilities empirically identifiable. Report scenarios and ranges rather than a spurious precise estimate.

---

# 26. Official confirmation of extraterrestrial life or technology

**Contract:** A specified US official or agency definitively states that extraterrestrial life or technology exists before the deadline.  
[Contract record](https://gateway.polymarket.us/v1/events/slug/aliens)

## Actual data

- [NASA UAP FAQ and statements](https://science.nasa.gov/uap/faqs/).
- [National Archives UAP records](https://www.archives.gov/research/topics/uaps/rg-615).
- [AARO UAP records](https://www.aaro.mil/UAP-Records/).
- Statements by the specific officials and agencies eligible under the contract.

## Model

A rare-event hazard model could be written:

\[
P(Y=1\text{ by }T)
=
1-\exp\left(-\int_0^T\lambda(t\mid x_t)\,dt\right)
\]

A separate classifier determines whether an actual statement is made by an eligible speaker and is sufficiently definitive.

**Limitation:** Writing down a hazard function does not provide credible data to estimate it. The defensible first implementation is an **evidence-monitoring and rule-classification system**, with any probability shown as an explicit, highly uncertain scenario rather than a validated frequency estimate.

---

# Cross-cutting data and model cautions

1. **Archive inputs as they were known.** BLS, BEA, weather products, sports data and market rules may be revised. A current historical series can leak later knowledge into a backtest.
2. **Don’t confuse a model output with raw data.** The top-ten Python code expects some precomputed forecasts, errors or scenarios. Each must be generated and validated separately.
3. **Use the designated settlement source.** A generic gold price, local rain report or global AI usage estimate can be useful evidence without being the contract’s target.
4. **Validate the measurement layer.** Reporting precision, publication timing, revisions, ties, fallback rules and fair-price settlements can change payouts.
5. **Bootstrap comparable errors.** Historical forecast errors must match the forecast horizon and information available. Small or obsolete residual samples create false confidence.
6. **Test against simple baselines.** The appropriate next step for any production pipeline is a genuinely out-of-time backtest with calibration plots and proper scoring rules—not interpreting the synthetic demonstration results as forecasts.