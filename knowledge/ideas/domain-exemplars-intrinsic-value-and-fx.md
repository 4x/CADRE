---
id: idea-domain-exemplars-intrinsic-value-and-fx
type: idea
title: "Domain Exemplars: Intrinsic Valuation and Foreign Exchange"
summary: Candidate finance questions spanning intrinsic value, future share price, EUR/USD and bond price; historical model sketches and outsider schema suggestions remain unvalidated, non-prescriptive alternatives.
status: provisional
created: '2026-10-24'
updated: '2026-10-29'
topics:
  - benchmarks
  - finance
  - exemplars
confidence: medium
relations:
  - type: relates-to
    target: concept-connected-models-thesis
  - type: addresses
    target: question-initial-domain-beachhead
  - type: derived-from
    target: source-historical-problem-statement-and-initial-thoughts
  - type: derived-from
    target: source-historical-connected-models-slides-2020
  - type: relates-to
    target: source-outsider-financial-forecasting-and-schema-suggestions
  - type: relates-to
    target: idea-prediction-market-question-catalog
  - type: relates-to
    target: question-evaluation-and-reference-evidence
---

# Domain Exemplars: Intrinsic Valuation and Foreign Exchange

## Idea

Preserve two historical finance sketches as **candidate** exemplars for future representation and runtime evaluation. Neither is an adopted benchmark suite, validated forecast, selected first workflow, or required model inventory. The original proposal to adopt them remains provisional; this organization does not accept it. The following summarizes the legacy sketches, not prescriptive solutions:

### 1. Intrinsic Equity Valuation
A multi-tier financial valuation graph linking:
- **Cost of Equity / CAPM**: Connecting 10Y US Treasury spot rates, Svensson yield curves, TIPS spreads, market equity risk premia (investor surveys, bond default spreads, Fama-French factors), and company beta.
- **Cash Flow Projections**: Connecting Net Borrowing, Cash Flow from Operations (CFO), and Fixed Capital Investment (FCI) into Free Cash Flow to Equity (FCFE).
- **Dividend Growth**: Connecting Return on Equity (ROE) and Earnings Retention Rate (ERR) into Dividend Growth Rate (DGR), feeding the Gordon Growth Model (GGM) and Dividend Discount Model (DDM).
- **Consolidation (unvalidated proposal)**: The historical sketch connects DCF, DDM, and FCFE estimates to Intrinsic Value. Any weighting, overlap, equity-versus-firm boundary, or double-counting must be independently justified; this is not an endorsed aggregation rule.

### 2. Foreign Exchange Forecasting (EUR/USD)
A macroeconomic currency model linking four complementary economic and statistical models:
- Covered Interest Rate Parity (CIP).
- Uncovered Interest Rate Parity (UIP).
- Relative Purchasing Power Parity (PPP).
- Time-series econometric models (ARIMA / GARCH).

## Additional imported questions — not their proposed solutions

The outsider document [[source-outsider-financial-forecasting-and-schema-suggestions]] adds three candidate questions:

1. **Equity:** What is the distribution of a specified share's observable price one year from now, distinguished from its intrinsic value and investor total return?
2. **FX:** What is the distribution of USD per EUR at a specified one-year horizon, with the quote direction and observation convention explicit?
3. **Fixed income:** What will the clean price of a specified fixed-rate Treasury bond be in one year, distinguished from dirty price, coupons and holding-period return?

These are question ideas, not claims that a defensible forecast is currently available. The source's forecasting recipes, schemas, model interfaces, Python examples and proposed three-instrument first implementation are **outsider suggestions, NOT project requirements**. They do not expand the scalar v0 contract, choose a runtime or data provider, or amend the offline-curation boundary.

The original financial document is kept intact: forecasting discussion in original lines 1–1350; financial data schemas/model interfaces from original line 1351 onward. Its fictional examples are not observations. No proposed pipeline, pricing-to-forecast bridge, data access or predictive performance was verified during import.

## Why it may matter

- Concrete financial questions could expose meaning, unit, timing and valuation/forecast distinctions without requiring every proposed model or schema.
- The proposed sketches span accounting relationships, statistical models, yield curves and external data, but coverage and suitability for a bounded runtime remain to be evaluated ([[question-execution-runtime-for-heterogeneous-models]]). Independent references and tolerances belong in [[question-evaluation-and-reference-evidence]].

## What would make it worth pursuing?

- If a finance question is selected through [[question-first-build-scope-and-success]], define a bounded reference case and evidence before treating it as a benchmark. Intrinsic Valuation is a candidate, not the default first test.
- Evaluate whether stored, qualified models can answer the selected question with available point-in-time data; preserve competing methods and no-match outcomes rather than adopting the outsider's component list.

## Legacy provenance

Reconstructed from the Mermaid valuation graph in [[source-historical-problem-statement-and-initial-thoughts]] (original payload lines 101–192) and the FX parity model list in [[source-historical-connected-models-slides-2020]] (original payload lines 116–124). The outsider financial commentary was imported on 2026-10-29 from the former Queue document; its author and original generation date are unknown. Prediction-market examples have their own question-only catalog: [[idea-prediction-market-question-catalog]].
