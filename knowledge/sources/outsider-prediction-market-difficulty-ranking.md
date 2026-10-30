---
id: source-outsider-prediction-market-difficulty-ranking
type: source
title: "Outsider Ranking of 26 Prediction-Market Examples"
summary: "Imported subjective modelability ranking of 26 markets; no fitted models, backtests, measured readiness, or selected pilot."
status: provisional
created: '2026-10-29'
updated: '2026-10-29'
topics:
  - finance
  - exemplars
  - benchmarks
confidence: null
relations:
  - type: relates-to
    target: idea-prediction-market-question-catalog
  - type: relates-to
    target: source-outsider-prediction-market-examples
  - type: relates-to
    target: question-initial-domain-beachhead
---

# Outsider Ranking of 26 Prediction-Market Examples

## Provenance and interpretation

The ordering refers to the author's claimed 2026-10-28 snapshot. It is a subjective ranking of apparent model/data availability and settlement match, NOT evidence of predictive accuracy, profitability, readiness, or a project decision to start with rain/CPI/sports. The canonical question catalog deliberately does not adopt this ordering.

- Imported on 2026-10-29 from `Queue/Ranking 26 markets.md`.
- Created/updated metadata dates describe this source record, not the original document.
- Original payload SHA-256 (including original line endings): `80b2b8e6dd7a702d3fbe3e8f089fbdd1588f7c67ae01a37d39508bab5c2c24cd`.
- The original payload follows unchanged after the marker; line references to the original are relative to that payload.
- User clarification, 2026-10-29: Queue contains candidate questions and outsider thoughts, NOT prescriptive solutions. The outsider's identity, generation process, and full conversation provenance are not supplied; no author or model is inferred.

## Original document (verbatim)

<!-- ORIGINAL DOCUMENT:BEGIN -->

# Ranking 26 markets: easiest to hardest to model

I’m ranking these this definition of **easy**: the relevant data and models are identifiable, accessible, reasonably reliable, and well matched to the contract’s actual settlement question.

This is **not a ranking of how certain the outcome is**, how easy it is to make money, or which market is mispriced. A rare event can be easy to define yet hard to forecast accurately.

## How to read the ranking

The positions are **judgment calls, not measured model performance**. I haven’t fitted or backtested the proposed pipelines. In particular, the middle of the list contains close calls that could move substantially with access to better data.

I’m evaluating each as a **pre-settlement forecasting problem**: for already-settled markets, imagine making the forecast shortly before resolution using only information then available. The ordering reflects the prior October 28, 2026 research snapshot; it is not a fresh check of market availability.

## Overall ranking

| Rank | Market | Main reason for placement |
|---:|---|---|
| **1** | Polymarket US: Central Park rain | Strong public weather data, mature models, unusually precise settlement rule |
| **2** | Polymarket US: monthly CPI | Public nowcasts and official historical releases closely match the target |
| **3** | Kalshi: next SOFR publication | Precisely defined official rate with abundant recent observations |
| **4** | Kalshi: annual GDP growth | Established nowcasting framework, with an extra annual-aggregation step |
| **5** | Kalshi: monthly payrolls | Public data and established nowcasting methods, but a noisy initial estimate |
| **6** | Kalshi: hottest October | Public climate data and physical models; exact record methodology needs checking |
| **7** | Kalshi: Seattle–Kansas City winner | Abundant historical games and established matchup models |
| **8** | Polymarket US: San Francisco season wins | Same strong sports data, but several correlated future games |
| **9** | Polymarket US: real wages versus inflation | Two well-defined BLS series, but a joint forecast and composition effects are needed |
| **10** | Polymarket US: Jordan Love passing yards | Good play-level data, but availability and usage introduce substantial uncertainty |
| **11** | Kalshi: Rotten Tomatoes score | Clearly observed target and comparable films; critic selection is difficult |
| **12** | Kalshi: Fed decision plus dissent | Public policy and voting data, but limited comparable meetings and correlated outcomes |
| **13** | Kalshi: Florida Category 4+ landfall | Mature physical models, but a rare, long-horizon joint track-and-intensity event |
| **14** | Polymarket US: Netflix #1 show | Direct chart target, but limited visibility into US title-level demand |
| **15** | Polymarket US: Missouri House margin | Official votes are accessible; current district-specific evidence may be sparse |
| **16** | Polymarket US: governorship count | Many identifiable races, but correlated errors and complicated aggregation |
| **17** | Polymarket US: union membership count | Public official series, but survey noise and weak visibility into future flows |
| **18** | Polymarket US: Solana price range | Excellent market data and precise rules, but short-term price distributions are unstable |
| **19** | Kalshi: Bitcoin versus gold | Observable prices, but a joint, potentially regime-dependent relative-return forecast |
| **20** | Kalshi: OpenRouter market share | Direct published target, but data and behavior can change quickly |
| **21** | Kalshi: Best Picture nomination | Observable historical outcomes, but small samples and changing voter behavior |
| **22** | Polymarket US: top AI leaderboard company | Observable current rankings, but future releases and ranking changes are hard to model |
| **23** | Polymarket US: state data-center moratorium | Traceable bills, but legal classification and passage probabilities are difficult |
| **24** | Kalshi: Ukrainian TPS ends | Defined legal process, but decisions and legal interpretations are hard to forecast |
| **25** | Kalshi: Ukraine presidential election | Institutional and security conditions have few strong historical analogues |
| **26** | Polymarket US: official extraterrestrial confirmation | Precise speaker/deadline rule, but extremely sparse comparable evidence |

---

# 1–6: Strong data, established models, close measurement match

## 1. Central Park rain — **easiest overall**

**Contract:** A qualifying rain code is reported at KNYC on the specified date.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/rain-daily-2026-10-29)

- **Data:** Public station observations, radar and numerical weather forecasts.
- **Models:** Weather ensembles and station-level statistical calibration.
- **Match:** The contract spells out exactly which observation codes count.
- **Remaining difficulty:** A forecast of rain in the area is not identical to a qualifying station report. Timing, precipitation type, special observations and the contract’s local-standard-time rule matter.

**Why #1:** Both sides of the interface—the physical event and the reporting mechanism—are unusually observable and testable.

---

## 2. Monthly CPI

**Contract:** The specified first-published October CPI-U monthly change is above −0.2%.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/uscpi-october-mom-2026-11-10)

- **Data:** Public BLS releases, energy prices and component-level indicators.
- **Models:** Established inflation nowcasts, including the [Cleveland Fed’s model](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting).
- **Match:** The nowcast aims at essentially the same published statistic as the contract.
- **Remaining difficulty:** First-release forecast error, reporting precision and delayed-release fallback rules.

**Why #2:** The measurement target is close to existing nowcasts. It ranks below station rain because the first release is an aggregate statistical estimate rather than a directly observed local report.

---

## 3. Next SOFR publication

**Contract:** The initially reported SOFR for October 26 is at most 3.85%.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXSOFRD-26OCT27?with_nested_markets=true) · **Retrospective**

- **Data:** Official historical SOFR and public information about secured funding conditions.
- **Models:** Short-horizon rate and repo-market models.
- **Match:** An exact published rate, date and inclusive threshold.
- **Remaining difficulty:** The relevant transactions occur before publication, but a forecaster may not have the complete underlying transaction data before the release.

**Why #3:** Very clear and short-horizon, although access to real-time repo information may be uneven.

---

## 4. Annual GDP growth

**Contract:** First-published annual real GDP growth is between 1.6% and 2.0%, inclusive.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXGDPYEAR-26?with_nested_markets=true)

- **Data:** Public BEA releases and component economic indicators.
- **Models:** [Atlanta Fed GDPNow](https://www.atlantafed.org/research-and-data/data/gdpnow/explainer) and alternative GDP nowcasts.
- **Match:** High, provided the model targets the **first annual-average estimate**, not a different growth measure.
- **Remaining difficulty:** GDPNow forecasts the current quarter; ConnectedModels must combine quarterly **levels** into annual growth and account for first-release error.

**Why #4:** Strong public infrastructure, with a nontrivial but explicit transformation.

---

## 5. Monthly nonfarm payrolls

**Contract:** The BLS-reported October payroll increase is above 50,000.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXPAYROLLS-26OCT?with_nested_markets=true)

- **Data:** BLS releases, claims, surveys and other labor indicators.
- **Models:** Dynamic-factor and sector-level labor nowcasts.
- **Match:** The published payroll figure is explicit.
- **Remaining difficulty:** Initial payroll estimates can be noisy, and alternative labor indicators are imperfect proxies for the BLS survey.

**Why #5:** Identifiable and accessible, but the initial monthly measurement is difficult to predict precisely.

---

## 6. Hottest October on record

**Contract:** October 2026 is the hottest October in the specified NOAA/NCEI record.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXHMONTH-26OCT?with_nested_markets=true)

- **Data:** Public historical climate observations and weather/reanalysis data.
- **Models:** Global temperature nowcasts and ensemble weather forecasts.
- **Match:** Good once the exact NCEI series and record-ranking rule are verified.
- **Remaining difficulty:** Small differences near a record threshold and differences between provisional atmospheric datasets and NCEI’s published product.

**Why #6:** Physical and measurement models are identifiable. I would not rank it higher until the sparse API rule is supplemented with the full product specification.

---

# 7–13: Strong foundations, but more uncertainty between model and settlement

## 7. Seattle–Kansas City game winner

**Contract:** Seattle wins; a tie pays $0.50.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXNFLGAME-26OCT25KCSEA?with_nested_markets=true) · **Retrospective**

- **Data/models:** Extensive historical results; [NFL Elo](https://github.com/fivethirtyeight/nfl-elo-game) offers a transparent baseline.
- **Match:** Good, provided the model includes ties and postponement rules.
- **Main difficulty:** Team strength, roster availability and game-specific conditions.

**Why #7:** Well-studied, repeatable forecasting problem, though one game remains inherently variable.

---

## 8. San Francisco season win total

**Contract:** San Francisco has more than 8.5 regular-season wins.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/nfl-wins-2027-01-10-sf)

- **Data/models:** The same game-level datasets and Elo-style models, combined in a season simulator.
- **Match:** High: simulated official wins map directly to the threshold.
- **Main difficulty:** Injuries and team-strength changes can affect several games together.

**Why #8:** Slightly harder than one game because the platform must simulate multiple dependent games, though some existing wins may already be known.

---

## 9. Real wages versus inflation

**Contract:** BLS’s first-published 12-month change in real average hourly earnings is positive.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/usrealwage-v-infl-2026)

- **Data/models:** Public BLS wage and inflation series; wage and CPI nowcasts.
- **Match:** Strong if the BLS calculation and first-release convention are reproduced.
- **Main difficulty:** Wage and inflation forecasts are correlated, and changes in workforce composition affect average earnings.

**Why #9:** Each component is well defined, but the joint forecast is harder than CPI alone.

---

## 10. Jordan Love passing yards

**Contract:** More than 3,250.5 regular-season passing yards.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/nfl-passyds-2027-01-10-jorlov)

- **Data/models:** Historical and current player statistics, play-level models, usage and availability models.
- **Match:** Direct once remaining yards and games are simulated.
- **Main difficulty:** Injury, coaching decisions, pass volume and opponent effects.

**Why #10:** The statistical target is clean, but the most influential variable—whether and how much the player participates—is not reliably recoverable from past yardage alone.

---

## 11. Rotten Tomatoes score

**Contract:** The film’s displayed Tomatometer is above 60 at a specified time.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXRT-HUN?with_nested_markets=true)

- **Data/models:** Historical film scores, review counts and comparable-title models.
- **Match:** Clear score, threshold and timestamp.
- **Main difficulty:** Which critics review the film by that timestamp is selective, and early reviews may not be representative.

**Why #11:** Easy to define and observe, harder to build a reliably calibrated pre-release distribution.

---

## 12. Fed decision and dissent

**Contract:** No rate change **and** at least one dissent.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXFEDCOMBO-26OCT?with_nested_markets=true) · **Retrospective**

- **Data/models:** Public economic releases, FOMC decisions, individual votes and communications.
- **Match:** The event is observable and the joint outcome is well specified by the title and subtitle.
- **Main difficulty:** There are relatively few comparable meetings, and dissent depends on the decision itself.

**Why #12:** More public evidence than most institutional-decision markets, but limited training examples. Also, the API’s primary-rule text appeared inconsistent with the title/subtitle; a production system must resolve that discrepancy against the full rules.

---

## 13. Florida Category 4+ hurricane landfall

**Contract:** A qualifying hurricane center crosses the specified Florida coastline at Category 4 or above.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXHURRLANDFL4-31DEC26?with_nested_markets=true)

- **Data/models:** NOAA/NHC observations and [track and intensity guidance](https://www.nhc.noaa.gov/modelsummary.shtml?text).
- **Match:** The geography, intensity, timing and official report are explicit.
- **Main difficulty:** This is a rare joint event: a storm must form, follow a particular track and retain sufficient intensity at landfall.

**Why #13:** Excellent model families and physical data, but estimating a seasonal tail probability for an exact coastline is substantially harder than forecasting tomorrow’s local rain.

---

# 14–19: Measurable targets, but evidence or predictive reliability is weaker

## 14. Top US Netflix show

**Contract:** A particular title is #1 on the specified US weekly chart.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/ntflx-1shwus-2026-10-20) · **Retrospective**

- **Data/models:** Historical charts, release schedules and viewership-decay models.
- **Match:** Directly observable chart rank.
- **Main difficulty:** Public data may not expose enough US title-level viewing information before the chart is published.

**Why #14:** The outcome is easy to verify but the underlying demand model may rely on weak proxies.

---

## 15. Missouri House election margin

**Contract:** The Republican wins MO-04 by at least 30 percentage points.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/ushrmov-mo-04-2026-11-03)

- **Data/models:** Official past vote totals, candidate information, hierarchical election models and potentially district polling.
- **Match:** The vote-margin calculation is exact.
- **Main difficulty:** A district may have limited recent polling, and local candidate or turnout effects may not be well captured by national data.

**Why #15:** The model family is mature, but evidence for a specific district can be thin.

---

## 16. Party with more governorships

**Contract:** Democrats have more governorships than Republicans under the contract’s attribution rules.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/demvrep-2026-11-03)

- **Data/models:** State polling and fundamentals, hierarchical race models and election simulations.
- **Match:** Good if all non-contested seats, runoffs and attribution rules are included.
- **Main difficulty:** Shared polling errors across states and sparse information in some individual races.

**Why #16:** Each piece is identifiable, but the aggregate is only as good as its cross-state dependence and rules mapping. If high-quality state polling were abundant, it could rank above #15.

---

## 17. Union membership count

**Contract:** The first-reported number of union members in 2027 exceeds the corresponding 2026 number.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/usunion-rise-2027)

- **Data/models:** Public BLS membership and industry employment data, labor-flow models.
- **Match:** Clear annual survey estimate—not unionization rate.
- **Main difficulty:** New organizing campaigns, job turnover and survey variation all affect a relatively small annual difference.

**Why #17:** The source is accessible, but reliably predicting a future change in the reported count is harder than explaining past membership trends.

---

## 18. Solana price range

**Contract:** A specified 60-second average of the SOL benchmark is $89.99 or below.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/sol-range-day-2026-10-29)

- **Data/models:** Extensive price and volume data; GARCH, jump and other return models.
- **Match:** Excellent once the benchmark’s averaging and rounding rules are implemented.
- **Main difficulty:** Return distributions can shift abruptly; historical volatility alone does not establish a reliable forecast under news shocks.

**Why #18:** Data access and measurement are strong, but **model reliability**, not contract interpretation, is the limiting factor.

---

## 19. Bitcoin versus gold

**Contract:** Bitcoin’s specified 2026 performance exceeds gold’s.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXBTCVSGOLD-26?with_nested_markets=true)

- **Data/models:** Historical and current prices; joint volatility and relative-return models.
- **Match:** Good after verifying benchmark start/end conventions.
- **Main difficulty:** Both assets’ future returns and their dependence can change across regimes.

**Why #19:** Similar to Solana but requires a **joint relative-performance** model over the remaining horizon.

---

# 20–26: Exact questions, but weak or unstable predictive foundations

## 20. OpenAI’s OpenRouter market share

**Contract:** OpenRouter’s reported OpenAI text share exceeds the specified threshold.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXOPENSHARE-26OCT26?with_nested_markets=true) · **Retrospective**

- **Data/models:** Published OpenRouter share data and compositional time-series models.
- **Match:** Direct, subject to the source’s definitions and rounding.
- **Main difficulty:** Model releases, price changes and customer switching can rapidly invalidate past relationships; historical data availability may be limited.

**Why #20:** The source is identifiable, but it represents one platform and can change rapidly. If granular historical data are readily available, this could move several positions higher.

---

## 21. Best Picture nomination

**Contract:** *The Odyssey* is nominated for Best Picture.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXOSCARNOMPIC-27?with_nested_markets=true)

- **Data/models:** Past nominations, eligibility, precursor awards and hierarchical ranking models.
- **Match:** The eventual nomination is unambiguous.
- **Main difficulty:** Few annual observations, changing Academy membership and nomination rules, and unobserved voter preferences.

**Why #21:** An identifiable modeling problem, but limited independent training examples.

---

## 22. Top AI leaderboard company

**Contract:** Anthropic holds the top model on the specified Arena leaderboard at the stated time.  
[Polymarket US market records](https://gateway.polymarket.us/v1/markets?active=true&categories=technology&limit=5) · `aimrc-company1-2026-12-31-anthro`

- **Data/models:** Current pairwise comparisons and **Bradley–Terry**-style ranking models.
- **Match:** Strong for estimating uncertainty about *current* leaderboard standings.
- **Main difficulty:** Forecasting future releases, their strength, voting patterns and leaderboard methodology.

**Why #22:** A good ranking model answers “how strong are observed models?” more naturally than “which unreleased model will lead later?”

---

## 23. State data-center moratorium

**Contract:** Any US state enacts a qualifying statewide moratorium by the deadline.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/anyst-datactrmor)

- **Data/models:** State bills, legislative calendars, bill-stage and enactment models.
- **Match:** The contract offers detailed criteria, but each bill must be classified against them.
- **Main difficulty:** Amendments can change qualification; state legislative data and political processes are heterogeneous.

**Why #23:** A strong information-retrieval and legal-classification system is possible. A dependable probability of enactment across all states is much harder.

---

## 24. Ukrainian Temporary Protected Status ends

**Contract:** TPS ends before the deadline, with explicit treatment of pending decisions and automatic extension.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXTPSUKR-27?with_nested_markets=true)

- **Data/models:** Public DHS notices, statutes and legal proceedings; administrative-state transition models.
- **Match:** The contract identifies the relevant legal status.
- **Main difficulty:** A future executive decision or court action may be poorly predicted from comparable history.

**Why #24:** A platform can reliably **track the legal state and timeline** more easily than it can assign a calibrated probability to the next institutional decision.

---

## 25. Ukraine presidential election

**Contract:** Ukraine holds a presidential election before January 1, 2027.  
[Kalshi contract](https://external-api.kalshi.com/trade-api/v2/events/KXELECTUKRAINE-30JAN01?with_nested_markets=true)

- **Data/models:** Official announcements, legal rules, conflict indicators and scenario/transition models.
- **Match:** The occurrence is observable, though unusual or disputed arrangements may need interpretation.
- **Main difficulty:** Security, law, political decisions and election logistics interact; closely comparable cases are scarce.

**Why #25:** A connected scenario graph is useful, but a reliable numerical probability is difficult to validate.

---

## 26. Official confirmation of extraterrestrial life or technology — **hardest**

**Contract:** A specified US official or agency definitively states that extraterrestrial life or technology exists by the deadline.  
[Polymarket US contract](https://gateway.polymarket.us/v1/events/slug/aliens)

- **Data/models:** Public statements can be monitored; rare-event and institutional-announcement models are conceivable.
- **Match:** The rule specifies eligible speakers and timing, but “definitively states” can require interpretation.
- **Main difficulty:** There are very few meaningful historical analogues, and the probability of a qualifying statement is not the same as the probability that extraterrestrial life exists.

**Why #26:** It is straightforward to build an alerting and evidence-classification system. It is not straightforward to produce a defensible, calibrated probability of the statement.

---

# What the ranking reveals

## 1. A precise settlement rule is necessary but not sufficient

The Solana contract has an exceptionally precise settlement calculation, yet it ranks only **18th** because precise price data do not make future returns reliably predictable.

Conversely, the CPI and rain markets rank highly because their settlement targets align with existing forecasting systems that can be tested repeatedly.

## 2. “Easiest to monitor” and “easiest to forecast” differ

The platform could monitor legislative bills, DHS notices or official statements very effectively. That does not mean it can reliably predict what a legislature or agency will do next.

For institutional markets, ConnectedModels may add most value by producing:

- A **state diagram** of what must happen.
- An auditable timeline and evidence trail.
- Conditional scenarios.
- Clear warnings where numerical probabilities lack a strong empirical basis.

## 3. Existing models often need a final measurement layer

The largest implementation traps are not always in the domain model:

- **Weather → METAR code**, not just rain.
- **GDP nowcast → annual first-release growth**, not quarterly annualized growth.
- **Football result → payout**, including ties and postponements.
- **Critic reviews → displayed score at a timestamp**, not eventual reception.
- **Model strength → published leaderboard rank**, including future entrants and tie rules.

## 4. Best initial ConnectedModels prototypes

If the goal is to test the platform itself, I would start with:

1. **Central Park rain** — tests physical forecasts, station-specific observation, time zones and settlement parsing.
2. **Monthly CPI** — tests mixed-frequency data, release vintages, nowcasting and reported-value thresholds.
3. **Season football wins** — tests correlated simulations, live state and threshold aggregation.
4. **A legislative moratorium**, later — tests legal classification, event-state tracking and the platform’s ability to admit weak probability estimates.

The first three have many repeated historical cases, making it practical to evaluate whether model connections actually improve forecasts. The fourth is a harder test of interpretability and uncertainty handling.

---

A useful next step would be to score these markets against a common readiness rubric and identify the best pilot.  

