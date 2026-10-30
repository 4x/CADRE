---
id: source-outsider-prediction-market-examples
type: source
title: "Outsider Prediction-Market Examples \u2014 October 2026 Snapshot"
summary: "Imported 13 Polymarket US and 13 Kalshi example questions with proposed model pipelines and abbreviated settlement claims; not verified forecasts or live opportunities."
status: provisional
created: '2026-10-29'
updated: '2026-10-29'
topics:
  - finance
  - exemplars
  - uncertainty
confidence: null
relations:
  - type: relates-to
    target: idea-prediction-market-question-catalog
  - type: relates-to
    target: question-evaluation-and-reference-evidence
  - type: relates-to
    target: question-model-discovery-and-selection
---

# Outsider Prediction-Market Examples — October 2026 Snapshot

## Provenance and interpretation

The document claims a research snapshot of 2026-10-28. That date is a source claim, not an independent retrieval performed during this import. P1–P13 and K1–K13 are retained source locators. Market status, contract terms, quoted nowcasts, API records and linked evidence have NOT been rechecked. Pipeline and platform recommendations remain outsider opinions, not selected designs or trading advice.

- Imported on 2026-10-29 from `Queue/prediction markets.md`.
- Created/updated metadata dates describe this source record, not the original document.
- Original payload SHA-256 (including original line endings): `4e771daeedea8552426e6d45ad58a9e021cb608011f0b190a9072bc74c6ddcaf`.
- The original payload follows unchanged after the marker; line references to the original are relative to that payload.
- User clarification, 2026-10-29: Queue contains candidate questions and outsider thoughts, NOT prescriptive solutions. The outsider's identity, generation process, and full conversation provenance are not supplied; no author or model is inferred.

## Original document (verbatim)

<!-- ORIGINAL DOCUMENT:BEGIN -->

Prediction markets are a useful test case for ConnectedModels because they turn a broad question into a measurable target. But they also reveal a critical distinction:

> The quantity to forecast is usually **what a specified source will report under the contract’s rules**, not the underlying real-world phenomenon in the abstract.

A weather contract may depend on a particular airport observation; a GDP contract may use the first release rather than later revisions; and a technology contract may depend on a leaderboard’s ranking procedure rather than an independent assessment of product quality.

Below are **13 distinct event examples from Polymarket US and 13 from Kalshi**, each tied to a specific contract rather than merely an event headline. For each, I describe the resolution target, a proposed connected-model pipeline, and the most important information to resolve before relying on its output.

## Scope and limitations

- **Research snapshot:** October 28, 2026. The linked sources are official platform API records; their status, rules and prices can change.
- **Closed examples are labeled retrospective.** They illustrate how to construct and backtest a model using only information available before settlement; they are not live opportunities.
- These are **model designs, not executed forecasts**. I have not collected the underlying datasets, fitted the models, verified their predictive performance, or produced real probability estimates.
- Rules below are abbreviated. Before implementing a forecast—or acting on one—retrieve the current full contract and any incorporated product rules.
- The “critical unknown” in each section is a candidate for observation or modeling, not a claim that all other uncertainties have been resolved.

---

# 1. A common architecture

## 1.1 Start with a settlement function

For an ordinary binary contract, define:

\[
Y=\begin{cases}
1 & \text{if the specified settlement condition is met}\\
0 & \text{otherwise}
\end{cases}
\]

The aim is to estimate:

\[
P(Y=1\mid \text{information available at forecast time})
\]

But not every contract is strictly binary in its economics. Some provide a **partial payout on a tie**, or a **fair-price settlement** after cancellation or missing data. The more general target is therefore:

\[
E[\text{contract payout}\mid \text{available information}]
\]

This distinction matters whenever a contract can pay something other than $0 or $1.

A useful decomposition is:

\[
\text{Underlying world}
\rightarrow
\text{measurement or announcement process}
\rightarrow
\text{published source}
\rightarrow
\text{contract settlement}
\]

For example, a statistical agency’s first GDP estimate is an imperfect and later-revised measurement of economic output. A market resolving on that first estimate requires a model of the **release**, not just the latent economy.

## 1.2 Connect models by explicit interfaces

Each component should specify:

- Its **input and output variables**, units, time horizon and geography.
- The information available when a forecast is made.
- Model version, training data, validation and known scope.
- Uncertainty—including shared errors and dependencies with adjacent models.
- Whether the output is an observed measurement, prediction or causal counterfactual.

A generic pipeline is:

> **Evidence ingestion → domain model → measurement/publication model → exact contract rule → payout distribution → validation and sensitivity**

For most examples, the output should include:

1. A distribution or probability of the specified settlement.
2. The strongest alternative models and how much their answers differ.
3. The variables that most change the result.
4. Data provenance and limitations.
5. A comparison with market quotes, **if requested**, with fees, spreads, liquidity and settlement risk shown separately.

## 1.3 Forecasting is not automatically trading

A quoted price is useful evidence about what traders are willing to pay, but it is not necessarily an unbiased real-world probability. Bid–ask spreads, stale quotes, liquidity, fees, risk preferences, information and settlement terms all matter.

For an illustrative $1 binary contract, a simple no-fee expected payoff from buying Yes at price \(c\) is:

\[
EV=p-c
\]

That is only a starting point. A realistic decision must incorporate execution price and depth, fees, settlement timing, partial outcomes, model uncertainty, risk limits and dependence with other positions. The examples below are **not investment recommendations**.

---

# 2. Polymarket US: 13 examples

## P1. Missouri House election: margin of victory

**Contract:** Republican nominee wins Missouri’s 4th Congressional District by **at least 30 percentage points** in the 2026 election. The contract defines the margin using valid vote shares and has special tie provisions.  
[Official event and contract record](https://gateway.polymarket.us/v1/events/slug/ushrmov-mo-04-2026-11-03) · Contract `vmc-ushrmov-mo-04-2026-11-03-rgte30`

### Pipeline

> District election history + candidate and incumbency data + available polling  
> → hierarchical district vote-share model  
> → turnout and third-party vote model  
> → certified vote shares  
> → contract’s margin and tie calculation.

1. Use a **hierarchical Bayesian election model** to combine district fundamentals with sparse local polling. National political conditions act as a shared factor, while district effects capture local variation.
2. Where suitable individual survey data exist, use **multilevel regression and poststratification (MRP)** to estimate likely-voter preferences across demographic and geographic cells.
3. Simulate valid vote totals, including the possibility of additional candidates, rather than assuming a two-candidate race.
4. Apply the contract’s margin definition to each simulated result.

**Output:** Probability of a Republican win by at least 30 points; simulated margin distribution; sensitivity to turnout and national swing.

**Resolve before assuming:** District-specific polling and likely-voter composition. If direct polling is scarce, partial pooling can help, but it does not eliminate the possibility of local candidate effects.

---

## P2. Which party will hold more governorships?

**Contract:** The Democratic Party has a larger count of governorships than Republicans as a result of the 2026 midterms. The rules include non-contested seats, runoffs and party attribution conventions.  
[Official record](https://gateway.polymarket.us/v1/events/slug/demvrep-2026-11-03) · Contract `usgovcc-demvrep-2026-11-03-dem`

### Pipeline

> State race polls + fundamentals + incumbent party counts  
> → correlated state-level election forecasts  
> → runoff and uncontested-seat attribution  
> → nationwide party totals  
> → comparison of Democratic and Republican counts.

1. Model each contested race with a **state-level hierarchical election model**.
2. Simulate a shared national polling error plus region- and state-specific errors. Treating states as independent would generally understate the likelihood of many races moving together.
3. Carry fixed and uncontested seats through the contract’s attribution rules.
4. For races requiring a runoff, model the runoff conditional on the first-round outcome.

**Output:** Distribution of governorship counts and probability Democrats have strictly more.

**Resolve before assuming:** The actual set of elections included under the contract’s October 31 cutoff and the parties associated with non-contested seats. Fetch those rather than assuming the current governor map is sufficient.

---

## P3. Data-center moratorium by a US state

**Contract:** At least one state enacts a qualifying statewide data-center moratorium by December 31, 2027. Local measures and suspensions of incentives alone do not qualify.  
[Official record](https://gateway.polymarket.us/v1/events/slug/anyst-datactrmor) · Contract `lawec-anyst-datactrmor-2027-12-31`

### Pipeline

> State legislative bills + grid/water stress + legislative calendars  
> → bill classification and stage-transition models  
> → enactment and legal-instrument classification  
> → probability at least one qualifying state law is enacted.

1. Maintain a state-by-state inventory of relevant bills and their current stages.
2. Classify whether each bill’s text would meet the contract: statewide scope, covered activity, and actual legal enactment.
3. Use a **discrete-time legislative hazard model** for progression through committee, chambers and enactment, with state-session calendars.
4. Couple states through shared drivers, such as national public attention or grid demand; do not multiply 50 independent state probabilities by default.
5. Re-run classification if amendments change scope.

**Output:** Overall probability, state-level contribution, most relevant pending bills and the stage most likely to prevent enactment.

**Resolve before assuming:** Whether proposed bills actually qualify after amendment. Legal-text classification should produce auditable evidence and flag ambiguous bills for review; it should not replace legal interpretation.

---

## P4. October CPI month over month

**Contract:** Seasonally adjusted October 2026 CPI-U one-month change is **above −0.2%**, using the specified BLS release and fallback rules. Later revisions are excluded.  
[Official record](https://gateway.polymarket.us/v1/events/slug/uscpi-october-mom-2026-11-10) · Contract `cpic-uscpi-october-mom-2026-11-10-gtneg0pt2pct`

### Pipeline

> Energy prices + rents + goods/services indicators + prior CPI data  
> → component inflation nowcasts  
> → weighted CPI release estimate  
> → reported-value/rounding model  
> → strict threshold and release-fallback logic.

1. Start with the [Cleveland Fed Inflation Nowcasting model](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting), which uses data including oil, gasoline and inflation releases.
2. Compare it with a bottom-up component nowcast and historical release errors.
3. Forecast the **published seasonally adjusted figure**, not a private inflation estimate.
4. Apply the actual display and threshold rules, and model the delayed-release fallback separately.

**Output:** Predictive distribution for the first published CPI figure and probability that the contract settles Yes.

**Resolve before assuming:** Release timing, component weights and the relevant reporting precision. Obtain real-time data vintages for historical backtests; revised data would make a nowcast appear better informed than it was.

---

## P5. Will wages beat inflation?

**Contract:** BLS’s first-published December 2026 **12-month change in real average hourly earnings** for private nonfarm employees is greater than 0.0%. This is not a claim about every worker’s pay.  
[Official record](https://gateway.polymarket.us/v1/events/slug/usrealwage-v-infl-2026) · Contract `rahec-usrealwage-v-infl-2026-yes`

### Pipeline

> Payroll employment composition + nominal hourly earnings  
> + CPI components  
> → joint wage-and-price forecast  
> → BLS-style real-earnings calculation  
> → published 12-month change  
> → strict positive threshold.

1. Nowcast nominal average hourly earnings from payroll and industry indicators.
2. Connect that forecast to a CPI nowcast, preserving the correlation between wages and prices.
3. Account for changing industry and worker composition: an average can move even if the same workers receive no raise.
4. Forecast the first reported BLS figure and apply the threshold and fallback rules.

**Output:** Probability the reported series is positive, alongside separate distributions for nominal earnings growth and inflation.

**Resolve before assuming:** How much of recent earnings growth reflects worker composition versus individual pay increases. Alternative microdata-based composition models can bracket this uncertainty.

---

## P6. Will union membership rise?

**Contract:** The BLS-reported **number**, not percentage, of wage and salary workers aged 16+ who are union members in 2027 exceeds the corresponding first-published 2026 count.  
[Official record](https://gateway.polymarket.us/v1/events/slug/usunion-rise-2027) · Contract `unmbc-usunion-rise-2027-yes`

### Pipeline

> Industry employment and hiring forecasts  
> + union-election and membership flows  
> → industry-level union membership model  
> → aggregate count  
> → BLS survey/reporting model  
> → year-over-year comparison.

1. Forecast employment by industry using a time-series or labor-demand model.
2. Estimate union join, exit and organizing flows by industry, using administrative and survey evidence where available.
3. Combine industry employment and membership rates to estimate total members.
4. Add an observation layer for the BLS survey estimate and published rounding.

**Output:** Distribution of reported membership change and probability it exceeds zero.

**Resolve before assuming:** Which organizing wins translate into members, when they do so, and how survey noise affects a small year-to-year change. Administrative election wins are informative but are not identical to the BLS membership count.

---

## P7. Rain in Central Park

**Contract:** Rain is reported at station **KNYC** on October 29, 2026, according to the specified observation-code rules. A qualifying present-weather rain code is required; drizzle alone, vicinity reports and remarks alone do not count.  
[Official record and detailed rules](https://gateway.polymarket.us/v1/events/slug/rain-daily-2026-10-29) · Contract `rainc-rain-daily-2026-10-29-knyc`

### Pipeline

> Radar and atmospheric observations  
> → numerical weather forecast ensemble  
> → station-level precipitation type, timing and duration  
> → METAR/SPECI observation and reporting process  
> → contract’s code parser and time-window rule.

1. Use a numerical weather ensemble plus local statistical post-processing to estimate rain at KNYC.
2. Simulate precipitation **type and timing**, not just a daily accumulation.
3. Model whether rain coincides with routine or special observations and is encoded in the qualifying field.
4. Convert timestamps to the contract’s **local standard time** definition and apply correction/fallback rules.

**Output:** Probability of at least one qualifying report, plus sensitivity to station observation timing and precipitation type.

**Resolve before assuming:** Local calibration between forecast precipitation and qualifying KNYC codes. A forecast of “rain somewhere in New York City” is not a substitute.

---

## P8. Which company has the top AI model?

**Contract:** Anthropic holds the #1 model on the specified Arena AI Text Arena leaderboard on December 31, 2026 at noon ET, with style control off and explicit tie-break rules.  
[Official market records](https://gateway.polymarket.us/v1/markets?active=true&categories=technology&limit=5) · Contract `aimrc-company1-2026-12-31-anthro`

### Pipeline

> Existing leaderboard comparisons and uncertainty  
> + model-release histories  
> → latent model-strength estimates  
> → future release and improvement scenarios  
> → simulated paired comparisons and leaderboard ranking  
> → contract’s company and tie-break rule.

1. Use a **Bradley–Terry paired-comparison model**, or an appropriate extension, to estimate uncertainty in current relative strengths.
2. Model future model-release timing and potential capability changes separately; an existing leaderboard model alone cannot predict an unreleased model.
3. Simulate the contest and apply the actual ranking and tie-break procedure.
4. Compare with simpler baselines, such as persistent current leader and empirical transition frequencies.

**Output:** Company-level probability of holding the specified rank, with scenarios for new releases versus no new releases.

**Resolve before assuming:** Future releases, leaderboard sampling and methodology changes. “Best on this leaderboard at a particular moment” should not be translated into “best AI company” generally.

---

## P9. Solana price at a specified time

**Contract:** The specified CF Benchmarks Solana-dollar index settlement value is **$89.99 or below** at 5:00 p.m. ET on October 29, 2026. The contract uses a 60-price average rounded to two decimals.  
[Official record](https://gateway.polymarket.us/v1/events/slug/sol-range-day-2026-10-29) · Contract `cpcsol-sol-range-day-2026-10-29-below-90`

### Pipeline

> Current index and underlying market data  
> → short-horizon return and volatility model  
> → simulated second-by-second index path  
> → final-minute average and rounding  
> → contract boundary.

1. Estimate a baseline return distribution using historical returns and a volatility model such as **GARCH**.
2. Compare with a heavier-tailed or jump model; a normal distribution can underestimate large moves.
3. Simulate the specified index, not just a price from an unrelated exchange.
4. Average and round exactly as required before applying the boundary.

**Output:** Distribution of the settlement average and probability it falls in the contract’s range.

**Resolve before assuming:** Index composition, basis relative to accessible spot data, and how well short-horizon volatility estimates handle sudden news. Options-derived distributions can be a useful comparison, but are not automatically real-world probabilities.

---

## P10. San Francisco regular-season wins

**Contract:** San Francisco records **more than 8.5 wins** in the 2026 professional football regular season.  
[Official record](https://gateway.polymarket.us/v1/events/slug/nfl-wins-2027-01-10-sf) · Contract `aachc-nfl-wins-2027-01-10-sf-8pt5wins`

### Pipeline

> Results to date + remaining schedule + team ratings + injuries  
> → game-by-game win/loss/tie probabilities  
> → correlated season simulation  
> → official regular-season win total  
> → over-8.5 threshold.

1. Use [NFL Elo](https://github.com/fivethirtyeight/nfl-elo-game) as a transparent baseline for each matchup.
2. Compare it with a team-strength model incorporating quarterback availability and injuries.
3. Simulate remaining games, allowing persistent team-strength and injury shocks to affect several games together.
4. Add already recorded wins and calculate the official-season total.

**Output:** Win-total distribution and probability of at least nine wins.

**Resolve before assuming:** Current record, schedule and roster availability. A pure Poisson-binomial model with independent game probabilities can miss correlated injuries or changes in team strength.

---

## P11. Jordan Love passing yards

**Contract:** Jordan Love records **more than 3,250.5 passing yards** in the 2026 regular season.  
[Official record](https://gateway.polymarket.us/v1/events/slug/nfl-passyds-2027-01-10-jorlov) · Contract `astatc-nfl-passyds-2027-01-10-jorlov-3250pt5yds`

### Pipeline

> Yards accumulated + remaining games + availability  
> → play-volume model  
> → pass-attempt and yards-per-attempt model  
> → injury/participation scenarios  
> → official season passing yards.

1. Model game participation and starts separately from performance when playing.
2. Forecast team offensive plays and pass rate based on opponent, game state and team tendencies.
3. Model yards per attempt with quarterback and opponent effects.
4. Simulate remaining games jointly, including persistent injury or lineup scenarios.

**Output:** Probability of exceeding the threshold, conditional on different availability paths.

**Resolve before assuming:** Injury status and expected playing time. Multiplying “average yards per game” by remaining games hides both missed-game risk and game-to-game dependence.

---

## P12. US government confirmation of extraterrestrial life or technology

**Contract:** By December 31, 2026, one of the specified US officials or agencies definitively states that extraterrestrial life **or technology** exists.  
[Official record](https://gateway.polymarket.us/v1/events/slug/aliens) · Contract `usgcc-aliens-12-31-2026`

### Pipeline

> Relevant government announcements and historical disclosure events  
> → model of eligible institutional statements  
> → classification of whether statement is definitive and within scope  
> → contract verification and settlement.

1. Build a monitored corpus of statements by the qualifying institutions.
2. Model announcement timing with a **rare-event or survival model**, while acknowledging that historical analogues are thin.
3. Classify candidate statements using explicit criteria: eligible speaker, definitive wording, life or technology, and deadline.
4. Route ambiguous statements for human review.

**Output:** A broad scenario-dependent probability range and an auditable evidence trail—not a precise claim about whether extraterrestrial life exists.

**Resolve before assuming:** What the exchange would regard as a “definitive” statement. This market concerns **institutional communication**, not directly the scientific truth of extraterrestrial life.

---

## P13. Top US Netflix show — retrospective

**Contract:** *Below: Limited Series* is #1 on the Netflix Top 10 US shows chart published October 20, 2026. The linked record reports the market as resolved.  
[Official record](https://gateway.polymarket.us/v1/events/slug/ntflx-1shwus-2026-10-20) · Contract `ccrc-ntflx-1shwus-2026-10-20-below`

### Pipeline

> Historical chart positions and viewing patterns  
> + release timing and competing shows  
> → show-level weekly viewership model  
> → rank distribution  
> → chart-publication rule.

1. Model title-level demand using prior chart history, release age, comparable shows and expected decay.
2. Model competing titles jointly: a show can grow and still lose the #1 rank if another grows faster.
3. Simulate the weekly chart and apply Netflix’s specified publication rule.

**Output:** Retrospective pre-publication probability of ranking first, plus the most consequential competitor and demand assumptions.

**Resolve before assuming:** The forecast-time availability of title-level views and comparables. For backtesting, hide the final chart and all later revisions; the fact that the contract settled Yes is not evidence that a proposed forecast was calibrated.

---

# 3. Kalshi: 13 examples

## K1. US real GDP growth in 2026

**Contract:** First-published BEA annual real GDP growth for 2026 is **1.6% to 2.0%, inclusive**, as specified in the contract.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXGDPYEAR-26?with_nested_markets=true) · `KXGDPYEAR-26-B1.8`

### Pipeline

> Quarterly consumption, investment, government and trade data  
> → GDP component nowcasts  
> → quarterly GDP-level forecasts  
> → annual-average 2026 versus annual-average 2025 calculation  
> → first BEA release and inclusive bracket.

1. Use [Atlanta Fed GDPNow](https://www.atlantafed.org/research-and-data/data/gdpnow/explainer) as a current-quarter benchmark; it is not itself a complete annual forecast.
2. Combine already published quarterly levels with distributions for remaining quarters.
3. Recreate the annual-average calculation and model first-release uncertainty.
4. Apply the **inclusive** bracket to the published figure.

**Output:** Distribution across GDP brackets, with contributions from uncertain components.

**Resolve before assuming:** The distinction between annual-average growth and Q4-over-Q4 growth. Historical backtesting must use the data vintages available before the advance release.

---

## K2. October nonfarm payrolls

**Contract:** The BLS-reported change in total nonfarm payroll employment for October 2026 is **above 50,000**.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXPAYROLLS-26OCT?with_nested_markets=true) · `KXPAYROLLS-26OCT-T50000`

### Pipeline

> Initial claims + labor-market surveys + employment indicators  
> → sector-level employment nowcast  
> → BLS aggregate and publication process  
> → reported payroll change  
> → strict threshold.

1. Estimate a **dynamic-factor nowcast** from timely labor indicators and compare it with a simpler autoregressive baseline.
2. Model sector-level employment changes and possible shocks such as strikes or weather.
3. Add uncertainty for the initial BLS estimate and publication convention.
4. Apply the exact “above” condition.

**Output:** Payroll-change distribution, probability above 50,000 and sensitivity to sector shocks.

**Resolve before assuming:** Whether a particular administrative source is representative of BLS’s survey population. Also check full product rules for delayed releases and revisions rather than infer them from the headline.

---

## K3. Bitcoin versus gold

**Contract:** Bitcoin outperforms gold in 2026, using the contract’s designated Bitcoin and gold price sources.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXBTCVSGOLD-26?with_nested_markets=true) · `KXBTCVSGOLD-26`

### Pipeline

> Starting and current benchmark prices  
> + remaining-horizon return data  
> → joint Bitcoin/gold return model  
> → settlement-source price and performance comparison  
> → outperformance indicator.

1. Retrieve the exact benchmark start values and the specified settlement conventions.
2. Model the **joint** distribution of Bitcoin and gold returns, using historical data and alternative volatility or regime models.
3. Include dependence that may change under a macroeconomic stress scenario.
4. Apply the contract’s performance comparison.

**Output:** Distribution of the performance difference and probability Bitcoin outperforms.

**Resolve before assuming:** Exact start/end observations and whether accessible proxy prices reproduce the designated sources. The API excerpt identifies the sources, but a production system should verify full product rules for all calculation details.

---

## K4. Florida Category 4+ hurricane landfall

**Contract:** A Category 4 or stronger hurricane’s **center** crosses the specified Florida coastline, excluding the Keys, during the contract window. NHC’s initial operational landfall report governs, subject to the stated correction rule.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXHURRLANDFL4-31DEC26?with_nested_markets=true) · `KXHURRLANDFL4-31DEC26-YES`

### Pipeline

> Current tropical disturbances + ocean and atmospheric conditions  
> → storm formation model  
> → track and intensity ensembles  
> → coastline-intersection and intensity-at-landfall model  
> → NHC operational-report outcome.

1. For active storms, use [NHC track and intensity guidance](https://www.nhc.noaa.gov/modelsummary.shtml?text), including dynamical and consensus models.
2. For the remaining season, add a storm-formation model; today’s active storms do not cover all future possibilities.
3. Simulate both the storm center’s path and its intensity at crossing.
4. Apply the specified geography and the initial-report convention.

**Output:** Probability of a qualifying landfall, broken down by current storms versus future formation.

**Resolve before assuming:** Formation risk beyond the reliable lead time of weather models and the relationship between simulated intensity and NHC’s operational classification. This is a rare-event problem with substantial structural uncertainty.

---

## K5. Hottest October on record

**Contract:** October 2026 is the hottest October on record; Kalshi lists NOAA’s NCEI global temperature series as the settlement source.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXHMONTH-26OCT?with_nested_markets=true) · `KXHMONTH-26OCT`

### Pipeline

> Observed daily global temperatures + ocean conditions  
> + remaining-month weather forecasts  
> → global monthly temperature-anomaly nowcast  
> → NCEI measurement/publication mapping  
> → comparison with the source’s historical October record.

1. Assimilate available observations and use an ensemble forecast for remaining days.
2. Map the estimate to the NCEI series’ geographic coverage, baseline and calculation method.
3. Simulate the published anomaly and compare with the relevant record.

**Output:** Distribution of the published October anomaly and probability it exceeds the record under the applicable rule.

**Resolve before assuming:** The exact NCEI series, baseline, ranking and tie treatment. The API record’s secondary rules are sparse, so the full product rules must be checked before treating a numerical implementation as authoritative.

---

## K6. OpenAI’s OpenRouter market share — retrospective

**Contract:** OpenAI’s reported OpenRouter text market share by model author for the week of October 19, 2026 is **above 18.4%**, using the specified Monday update and rounding. The API reports the contract finalized.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXOPENSHARE-26OCT26?with_nested_markets=true) · `KXOPENSHARE-26OCT26-18.4`

### Pipeline

> OpenRouter usage time series + model releases + relative pricing  
> → author-level share dynamics  
> → weekly aggregation and publication model  
> → rounding and threshold rule.

1. Model daily author shares as a **compositional time series**: increasing one author’s share affects the others.
2. Add release and pricing events as predictors where their timing is known.
3. Simulate the weekly aggregate and the rounded published value.
4. Include the rule that an author not separately identified in the source chart results in No.

**Output:** Historical pre-settlement probability distribution for OpenRouter’s reported share.

**Resolve before assuming:** Whether “share” counts requests, tokens or another measure and whether historical data use the same methodology. OpenRouter share is not the same as share of all AI usage.

---

## K7. Best Picture nomination

**Contract:** *The Odyssey* receives a Best Picture nomination at the 99th Academy Awards.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXOSCARNOMPIC-27?with_nested_markets=true) · `KXOSCARNOMPIC-27-ODY`

### Pipeline

> Film eligibility + prior awards + critics’ reception + campaign indicators  
> → latent support model  
> → nomination-ballot simulation  
> → official nomination announcement.

1. Check eligibility and applicable nomination rules.
2. Use historical nominations to estimate a hierarchical model linking precursors and film characteristics to Academy support.
3. Simulate nominations jointly across films, respecting the nomination procedure and number of slots.
4. Update as precursor awards and official information arrive.

**Output:** Probability of nomination, with sensitivities to eligibility and precursor evidence.

**Resolve before assuming:** Which historical predictors remain informative after changes in Academy membership or rules. Multiple films can be nominated, so nomination probabilities should not be forced to sum to one.

---

## K8. Rotten Tomatoes score

**Contract:** *The Hunger Games: Sunrise on the Reaping* has a Tomatometer **above 60** at 10:00 a.m. ET on November 23, 2026. A score exactly equal to the strike is not above it.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXRT-HUN?with_nested_markets=true) · `KXRT-HUN-60`

### Pipeline

> Comparable films and critic histories  
> → latent positive-review propensity  
> → review arrival and critic-selection model  
> → observed Tomatometer at the specified time  
> → rounding and strict threshold.

1. Build a prior from comparable films, franchise history and relevant creative personnel.
2. Update using observed reviews, modeling which critics are likely to publish by the deadline.
3. Simulate review arrival and positive/negative classification.
4. Map simulated reviews to the displayed score at the contract time.

**Output:** Probability the displayed score exceeds 60, and a distribution for the score.

**Resolve before assuming:** Review selection and timing. Critics are not independent random draws, and a film’s eventual score is not necessarily its score at the settlement timestamp.

---

## K9. Ukraine presidential election

**Contract:** Ukraine holds a presidential election **before January 1, 2027**.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXELECTUKRAINE-30JAN01?with_nested_markets=true) · `KXELECTUKRAINE-30JAN01-27JAN01`

### Pipeline

> Legal and electoral calendar + security conditions  
> + official announcements  
> → institutional-state transition scenarios  
> → election scheduling and conduct model  
> → contract’s “held before” condition.

1. Model a sequence of necessary or relevant states: legal permissibility, scheduling, preparation and election conduct.
2. Assign uncertainty to transitions using historical analogues and expert elicitation where data are weak.
3. Allow security conditions and institutional decisions to co-evolve; do not assume independent stages.
4. Check whether any announced event actually satisfies the contract’s “held” criterion.

**Output:** Scenario-dependent probability and the transitions preventing or enabling settlement.

**Resolve before assuming:** The legal and operational feasibility of conducting an election on the required timeline, and the exchange’s treatment of unusual or disputed election arrangements.

**Important limit:** A geopolitical event model can organize uncertainty; it cannot manufacture a reliable frequency estimate when comparable cases are scarce.

---

## K10. Temporary Protected Status for Ukraine

**Contract:** US Temporary Protected Status for Ukraine ends before January 1, 2027. The rule distinguishes termination or lapse from continued protection during a pending decision, including an automatic extension.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXTPSUKR-27?with_nested_markets=true) · `KXTPSUKR-27`

### Pipeline

> Statutory timeline + DHS notices + legal proceedings  
> → administrative decision and status-transition model  
> → effective protection status on relevant dates  
> → contract classification.

1. Parse current notices and statutory deadlines into a dated state machine.
2. Model agency decisions, automatic extensions and legal challenges as distinct transitions.
3. Determine whether protection actually ends in the contract window, not merely whether a termination is announced.
4. Apply the exchange’s treatment of each status.

**Output:** Probability of qualifying termination/lapse and a timeline of the decisions that matter.

**Resolve before assuming:** Current DHS notices and legal effects. A legal state-machine model should cite its inputs and expose uncertainty; it is not a substitute for legal advice.

---

## K11. Seattle versus Kansas City — retrospective

**Contract:** Seattle wins the October 25, 2026 professional football game. A tie pays $0.50; postponement and non-start conditions have special treatment. The API reports the contract finalized Yes.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXNFLGAME-26OCT25KCSEA?with_nested_markets=true) · `KXNFLGAME-26OCT25KCSEA-SEA`

### Pipeline

> Pre-game team ratings + venue + injuries + weather  
> → game-score distribution  
> → win/tie/loss probabilities  
> → postponement and payout rules  
> → expected settlement value.

1. Start with [NFL Elo](https://github.com/fivethirtyeight/nfl-elo-game).
2. Compare with a score-distribution model incorporating offensive and defensive strengths.
3. Add quarterback and key-player availability as uncertain scenarios.
4. Calculate:

\[
E[\text{payout}]
= P(\text{Seattle win}) + 0.5P(\text{tie}) + \text{other settlement contributions}
\]

**Output:** A pre-game payout distribution, not merely a win probability.

**Resolve before assuming:** Pre-game lineup and postponement risk. The final result must be withheld from retrospective training features.

---

## K12. Federal Reserve decision plus dissent — retrospective

**Contract:** No change in the Federal Funds Rate **and** more than zero dissents at the October 2026 meeting. The API reports this contract finalized Yes. Its displayed primary-rule text appears to omit the `>` sign in one field, while the title, subtitle and recorded result identify the “>0” contract.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXFEDCOMBO-26OCT?with_nested_markets=true) · `KXFEDCOMBO-26OCT-0-T0`

### Pipeline

> Inflation and labor nowcasts + prior FOMC votes and communications  
> → policy-decision model  
> → conditional member-vote model  
> → joint outcome: no change **and** at least one dissent.

1. Forecast the meeting decision from economic conditions, policy communications and a historical meeting model.
2. Model member votes **conditional on the decision**, since dissent risk is related to the action chosen.
3. Simulate the joint outcome rather than multiplying unrelated marginal probabilities.
4. Apply the corresponding component rules and settlement logic.

**Output:** Joint outcome probability, plus separate rates for the decision and dissent conditional on that decision.

**Resolve before assuming:** The apparent API-text inconsistency. Consult the incorporated contract rules and official exchange clarification before relying on a parser. This is exactly the type of contradiction ConnectedModels should surface rather than silently normalize.

---

## K13. SOFR — retrospective

**Contract:** The initially reported SOFR for October 26, 2026 is **at most 3.85%**; later revisions do not count. The API reports this contract finalized No.  
[Official record](https://external-api.kalshi.com/trade-api/v2/events/KXSOFRD-26OCT27?with_nested_markets=true) · `KXSOFRD-26OCT27-T3.85`

### Pipeline

> Policy target range + Treasury repo conditions  
> + funding flows and collateral supply  
> → overnight repo-rate distribution  
> → official SOFR publication model  
> → inclusive threshold.

1. Use recent SOFR and secured-funding observations to estimate a short-horizon baseline.
2. Add known funding pressures, settlement dates and liquidity conditions.
3. Model the initially reported rate and its publication precision.
4. Apply the **at most** condition.

**Output:** Pre-publication distribution for the reported SOFR and probability it is at or below 3.85%.

**Resolve before assuming:** Availability and representativeness of repo data before the publication. Do not use revised SOFR values or information published after the forecast timestamp in the backtest.

---

# 4. A worked example: why the measurement layer matters

Consider **P4**, the contract for October CPI month-over-month inflation above −0.2%.

The actual Cleveland Fed page supplied a **0.24% point nowcast** for October CPI as of October 28, 2026. That is useful as an input, but it does **not**, by itself, give the probability of a contract settling Yes. We also need an uncertainty distribution and the contract’s measurement conventions.  
[Source: Cleveland Fed Inflation Nowcasting](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting)

Here is a **hypothetical calculation**, not a fitted forecast:

1. Suppose an unrounded release-generating measure \(X\) is normally distributed with mean **0.20%** and standard deviation **0.20 percentage points**.
2. Suppose, for this illustration, the published value is rounded conventionally to one decimal place.
3. A published value strictly above **−0.2%** would begin at **−0.1%**, corresponding approximately to \(X>-0.15\%\).
4. Then:

\[
P(\text{published CPI}>-0.2\%)
=
P(X>-0.15\%)
\approx 96.0\%.
\]

If we incorrectly tested the unrounded number against −0.2%, the same illustrative normal model would give approximately **97.7%**.

The difference comes entirely from the assumed reporting transformation. In a production model I would:

- Verify the BLS release’s actual rounding and the exchange’s exact interpretation.
- Estimate forecast errors from **real-time** historic nowcasts and first releases.
- Compare a normal model with empirical or heavy-tailed alternatives.
- Account for the contract’s fallback if the expected figure is not published.
- Report uncertainty in the probability itself.

The example illustrates a general design principle: **a good domain forecast can still be the wrong contract forecast if the observation and settlement layers are missing.**

---

# 5. Models worth implementing as reusable building blocks

These 26 examples do not require 26 isolated systems. They suggest a smaller library of reusable, composable models.

| Reusable component | Example applications | Input → output |
|---|---|---|
| **Dynamic-factor nowcasting** | CPI, payrolls, GDP, wages | Mixed-frequency indicators → current-period distribution |
| **Hierarchical election forecasting** | District margin, governorship count | Polls and fundamentals → correlated vote shares and outcomes |
| **Survival / event-history modeling** | Legislation, AI releases, agency action | States and time-varying signals → transition timing |
| **Numerical weather ensembles** | Station rain, hurricane landfall | Atmospheric observations → weather trajectories |
| **Observation-process modeling** | METAR, economic releases, leaderboard scores | Latent outcome → reported observation |
| **Joint financial return modeling** | Bitcoin/gold, SOL | Market data → correlated price paths |
| **Team and player simulation** | Game winner, season wins, passing yards | Team strength and availability → scores and player totals |
| **Paired-comparison / ranking models** | AI leaderboard, film competition | Pairwise evidence → latent strengths and rank probabilities |
| **Institutional state machines** | TPS, elections, legislative enactment | Laws, notices and events → legally relevant states |
| **Contract settlement engine** | All markets | Source observations + rule version → payout |

The key is that these components must be **compatible at their interfaces**. For example:

- A quarterly GDP nowcast needs a separate transformation before it can answer an annual-average GDP contract.
- A weather trajectory needs a station observation model before it can answer the KNYC rain contract.
- A player-performance model needs an availability model before it can forecast a season total.
- A latent-review model needs a review-arrival and display model before it can forecast a score at a precise timestamp.

---

# 6. How ConnectedModels should choose between models

## 6.1 Prefer a hierarchy of evidence

For every consequential unknown:

1. **Observe directly**, if the relevant information is available at forecast time.
2. **Infer with an identifiable model**, such as estimating local weather-to-METAR reporting rates from archived observations.
3. **Compare model structures**, such as a heavy-tailed financial return model versus GARCH.
4. **Use explicit scenarios or expert elicitation** when the historical record cannot identify a reliable model.
5. **Report irreducible uncertainty** rather than presenting a precise point estimate.

For example, no model can reliably infer the exact legal meaning of an ambiguous future agency statement merely by fitting historical prices. The appropriate output may be a wide scenario range plus a flag for human review.

## 6.2 Backtest without hindsight

For each market family, record forecasts at multiple fixed lead times:

- What data and model version were available at that moment?
- What was the actual contract rule at that moment?
- What did the specified source first publish?
- What did the exchange ultimately settle?
- Were there corrections, cancellations or fair-price outcomes?

Then compare with simple baselines. For binary outcomes, use the **Brier score** or log score and calibration plots; for continuous distributions, use an appropriate proper scoring rule such as CRPS.

A model that produces persuasive narratives but does not improve on baselines in out-of-time testing should not be presented as more reliable merely because it connects more domains. For discussion of proper scoring rules, see [Gneiting and Raftery](https://doi.org/10.1198/016214506000001437) and the open [review of proper scoring rules](https://arxiv.org/html/2504.01781v1).

## 6.3 Preserve dependence

A recurring mistake would be to connect models while assuming their errors are independent:

- State election errors can move together.
- Wages and inflation respond to shared economic shocks.
- A football player’s availability affects both game outcomes and season yardage.
- Gold and Bitcoin can respond to the same macroeconomic news.
- Multiple state legislatures can respond to a shared national event.

ConnectedModels should pass **joint samples or shared latent variables**, not just isolated point estimates, across interfaces.

## 6.4 Separate model uncertainty from event probability

Suppose one defensible model gives a 35% probability and another gives 60%. That difference may reflect structural uncertainty, not randomness that can be summarized away by displaying “47.5%.”

The platform should show:

- Each model’s forecast and historical performance.
- The assumptions causing divergence.
- A combined forecast only if its weighting method is justified.
- Sensitivity to plausible alternative weights.
- The next observation most likely to distinguish the models or change a decision.

For example, on the data-center moratorium market, the most valuable new information might be an amended bill’s statewide scope; on the passing-yards market, it might be a credible injury update.

---

# 7. What these examples imply for the platform

The most valuable abstraction is not “a model that predicts markets.” It is a **contract-aware, versioned causal and measurement graph**.

A useful record for each forecast would include:

```text
Question:
Contract and platform:
Rule version and retrieval time:
Forecast timestamp:
Settlement source and observation window:
Required payout transformation:
Models and versions:
Input data and publication timestamps:
Shared dependencies:
Forecast distribution:
Alternative model results:
Key sensitivities and unresolved ambiguities:
Historical validation:
Final observed source value:
Exchange settlement:
```

This structure would let the platform answer not only:

> “What is the chance of this contract settling Yes?”

but also:

> “Is the uncertainty mostly about the world, the measurement, the institution’s decision, or the exchange’s interpretation—and what information would narrow it?”

That distinction is the main opportunity revealed by these markets. **The strongest connected forecast is not necessarily the most elaborate one; it is the one that tracks the actual settlement target, exposes its assumptions, and performs well against simpler alternatives.**

---

If useful, the natural next step is to turn these examples into a reusable specification for models, data and contract settlement rules.