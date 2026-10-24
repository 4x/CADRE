---
id: idea-domain-exemplars-intrinsic-value-and-fx
type: idea
title: "Domain Exemplars: Intrinsic Valuation and Foreign Exchange"
summary: Preserve the Intrinsic Value model (CAPM/DDM/DCF) and EUR/USD FX parity model (CIP/UIP/PPP/ARIMA) from legacy notes as canonical benchmark suites.
status: provisional
created: '2026-10-24'
updated: '2026-10-24'
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
---

# Domain Exemplars: Intrinsic Valuation and Foreign Exchange

## Idea

Adopt two detailed multi-model reference graphs from legacy materials as canonical benchmark exemplars to evaluate future representation schemas, ontological frameworks, and runtime execution engines:

### 1. Intrinsic Equity Valuation
A multi-tier financial valuation graph linking:
- **Cost of Equity / CAPM**: Connecting 10Y US Treasury spot rates, Svensson yield curves, TIPS spreads, market equity risk premia (investor surveys, bond default spreads, Fama-French factors), and company beta.
- **Cash Flow Projections**: Connecting Net Borrowing, Cash Flow from Operations (CFO), and Fixed Capital Investment (FCI) into Free Cash Flow to Equity (FCFE).
- **Dividend Growth**: Connecting Return on Equity (ROE) and Earnings Retention Rate (ERR) into Dividend Growth Rate (DGR), feeding the Gordon Growth Model (GGM) and Dividend Discount Model (DDM).
- **Consolidation**: Weighing DCF, DDM, and FCFE into a composite Intrinsic Value point estimate with sensitivity ranges.

### 2. Foreign Exchange Forecasting (EUR/USD)
A macroeconomic currency model linking four complementary economic and statistical models:
- Covered Interest Rate Parity (CIP).
- Uncovered Interest Rate Parity (UIP).
- Relative Purchasing Power Parity (PPP).
- Time-series econometric models (ARIMA / GARCH).

## Why it may matter

- Grounding future architectural research in concrete, mathematically rigorous reference cases prevents abstract over-engineering.
- These exemplars span closed-form accounting formulas, statistical market regressions, term structure yield curve fits, and external database lookups—serving as a comprehensive stress test for any candidate runtime ([[question-execution-runtime-for-heterogeneous-models]]).

## What would make it worth pursuing?

- When designing the formal model representation and ontology, using Intrinsic Valuation as the first end-to-end test case.
- Evaluating whether an AI agent can assemble this graph and execute it using external market data APIs.

## Legacy provenance

Reconstructed from the Mermaid valuation graph in `Legacy/ProblemStatementInitialThoughts.md` (lines 101–192) and the FX parity model list in `Legacy/Slides2020.md` (lines 116–124).
