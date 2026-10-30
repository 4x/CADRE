---
id: idea-prediction-market-question-catalog
type: idea
title: Prediction-Market Question Catalog
summary: Twenty-six imported candidate questions with original P/K source locators; no selected pilot, adopted pipeline, validated forecast, or accepted ranking.
status: provisional
created: '2026-10-29'
updated: '2026-10-29'
topics:
  - finance
  - exemplars
  - decision-support
confidence: null
relations:
  - type: derived-from
    target: source-outsider-prediction-market-examples
  - type: relates-to
    target: source-outsider-prediction-market-difficulty-ranking
  - type: relates-to
    target: source-outsider-prediction-market-data-and-model-suggestions
  - type: relates-to
    target: idea-end-state-question-gallery
  - type: relates-to
    target: idea-domain-exemplars-intrinsic-value-and-fx
  - type: relates-to
    target: question-first-build-scope-and-success
  - type: relates-to
    target: question-initial-domain-beachhead
  - type: relates-to
    target: question-evaluation-and-reference-evidence
---

# Prediction-Market Question Catalog

## Scope and epistemic status

These are **candidate questions Connected Models could explore**, not questions about the platform's architecture. They therefore belong in `ideas`, not as 26 new open design questions. The source claims a 2026-10-28 market snapshot; current contracts, market availability, rules, prices, and data access were not checked during organization on 2026-10-29. Some examples were already retrospective in the supplied material.

The user explicitly identified the accompanying schemas, models and proposed solutions as **outsider thoughts, NOT prescriptions**. Neither importing them nor listing the questions accepts the proposed pipelines, validates forecasts, commits to a model collection, or chooses an initial domain. The outsider's identity and complete conversation provenance are unknown.

## Candidate questions

The order below preserves the source's P1–P13 / K1–K13 locators, **not** its separate difficulty ranking. The question wording is condensed from the source; exact contracts, dates, sources, thresholds, exceptions and tie/cancellation rules remain in [[source-outsider-prediction-market-examples]] and must be rechecked before use. Numeric thresholds below are imported target descriptions, not newly verified market facts.

| Locator | Source platform | Candidate question | Source scope note |
| --- | --- | --- | --- |
| P1 | Polymarket US | Will the Republican nominee win Missouri's 4th House district by at least 30 percentage points? | Specified 2026 election and valid-vote margin rule. |
| P2 | Polymarket US | Will Democrats hold more governorships than Republicans after the 2026 midterms? | Includes source-specific seat and runoff attribution. |
| P3 | Polymarket US | Will a US state enact a qualifying statewide data-center moratorium by the deadline? | Legal scope and enactment, not merely a proposal. |
| P4 | Polymarket US | Will first-published seasonally adjusted October CPI-U monthly growth exceed −0.2%? | First release, threshold and fallback rules. |
| P5 | Polymarket US | Will first-published real average hourly earnings show positive 12-month growth? | Exact BLS real-earnings measure. |
| P6 | Polymarket US | Will the published union-membership count rise? | Survey statistic, population and release convention. |
| P7 | Polymarket US | Will a qualifying KNYC rain code be reported on the specified day? | Station observations and contract time window. |
| P8 | Polymarket US | Which company will have the top model on the designated AI leaderboard? | Published ranking and evaluation cutoff. |
| P9 | Polymarket US | Will Solana's benchmark price fall in the specified range at the specified time? | Exact price source and aggregation. |
| P10 | Polymarket US | Will San Francisco record more than 8.5 regular-season wins? | Official season total and contract rules. |
| P11 | Polymarket US | Will Jordan Love exceed 3,250.5 regular-season passing yards? | Availability and official statistic. |
| P12 | Polymarket US | Will a qualifying US government confirmation of extraterrestrial life or technology occur? | Defined speaker, statement and deadline. |
| P13 | Polymarket US | Which show will top the specified US Netflix chart? | **Retrospective in source.** Chart and publication window. |
| K1 | Kalshi | Will first-published annual real GDP growth fall between 1.6% and 2.0%, inclusive? | Annual-average growth, not quarterly annualized growth. |
| K2 | Kalshi | Will the first October nonfarm payroll increase exceed 50,000 jobs? | Initial publication rather than revised history. |
| K3 | Kalshi | Will Bitcoin outperform gold under the designated comparison? | Common return window and source conventions. |
| K4 | Kalshi | Will a Category 4-or-higher hurricane make qualifying Florida landfall? | Joint location, intensity and deadline criteria. |
| K5 | Kalshi | Will October 2026 be the hottest October in the designated NOAA/NCEI record? | Exact product and record/tie treatment. |
| K6 | Kalshi | Will OpenAI's OpenRouter market share satisfy the contract condition? | **Retrospective in source.** Platform metric, not worldwide AI usage. |
| K7 | Kalshi | Will the specified film receive a Best Picture nomination? | Designated nomination event and eligibility. |
| K8 | Kalshi | Will the specified film's displayed Rotten Tomatoes score meet the threshold? | Displayed score at cutoff, not eventual score. |
| K9 | Kalshi | Will a qualifying Ukraine presidential election occur by the deadline? | Institutional and legal event definition. |
| K10 | Kalshi | Will Ukrainian Temporary Protected Status end under the contract's definition? | Notices, effective dates and legal interpretation. |
| K11 | Kalshi | Will Seattle win the specified game against Kansas City? | **Retrospective in source.** A tie pays $0.50. |
| K12 | Kalshi | Will the specified Federal Reserve decision and dissent combination occur? | **Retrospective in source.** Joint institutional outcome. |
| K13 | Kalshi | Will initially published SOFR be at most 3.85%? | **Retrospective in source.** Rate date and publication convention. |

## Keep the supporting material separate

- **Question descriptions and outsider pipeline proposals:** [[source-outsider-prediction-market-examples]].
- **Subjective easiest-to-hardest ranking:** [[source-outsider-prediction-market-difficulty-ranking]]. No models were fitted or backtested to establish that ordering. Its rain/CPI/sports pilot preference is not ours.
- **Suggested data links, formulas and ten synthetic Python pipelines:** [[source-outsider-prediction-market-data-and-model-suggestions]]. The attachment is not application source or a verified forecasting engine. It expects precomputed inputs and uses fictional demonstration data.

## Possible use without accepting a solution

These examples could later help ask whether a candidate representation distinguishes a physical outcome from its measurement/publication and settlement, handles observation vintages and shared uncertainty, and permits an honest unresolved answer. They are candidate evaluation prompts, not proof that any particular schema or model is necessary or sufficient.

Choosing a workflow remains open in [[question-first-build-scope-and-success]]; its evidence and scoring requirements belong in [[question-evaluation-and-reference-evidence]]. Forecasting a payout does not imply a profitable trading strategy. No model, contract, dataset, provider or implementation was selected by this import.
