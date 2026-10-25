---
id: question-temporal-and-spatial-data-alignment
type: question
title: Temporal and Spatial Data Alignment Across Models
summary: How should the graph reconcile mismatching temporal and spatial resolutions when connecting continuous time-series, periodic averages, and static projections?
status: active
created: '2026-10-24'
updated: '2026-10-24'
topics:
  - ontology
  - representation
  - data-alignment
confidence: high
relations:
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: question-semantic-variable-disambiguation
  - type: relates-to
    target: question-model-node-ast-and-schema-representation
---

# Temporal and Spatial Data Alignment Across Models

## Question

How should the Connected Models representation and execution runtime formally reconcile mismatching temporal frequencies (continuous streams vs. daily vs. monthly vs. annualized) and spatial resolutions (raster grids vs. regional basins vs. corporate legal entities) when chaining cross-domain models?

## Why it matters

In real-world multi-tier modeling cascades (such as the flagship cascade in `[[concept-end-state-vision]]`), models naturally operate at completely different scales:
- **Physical earth systems**: Emit continuous time-series, hourly weather observations, and gridded spatial rasters (e.g., $0.25^\circ \times 0.25^\circ$ latitude/longitude cells).
- **Infrastructure & agriculture**: Operate on monthly or seasonal aggregates bounded by administrative or watershed polygons (e.g., *acre-feet per irrigation season across the Central Valley*).
- **Supply chain & operations**: Operate on quarterly production schedules, monthly batch runs, and weekly freight dispatch rates.
- **Financial markets & valuation**: Operate on trailing-twelve-month (TTM) financial reports, annualized discount rates, and multi-year terminal projections.

If edge connections cannot natively express temporal aggregation, resampling, and spatial re-zoning, modelers are forced back into writing fragile, bespoke ETL scripts—destroying the core promise of zero-ETL composability.

## Current partial answer

- **First-Class Spatio-Temporal Typing**: Variables must declare their temporal frequency (`continuous`, `hourly`, `daily`, `monthly`, `annual`, `static-point`) and spatial domain (`global`, `polygon-id`, `point(lat, lon)`, `entity-id`).
- **Declarative Edge Transform Operators**: Edges between models with mismatched temporal/spatial types must incorporate formal transform adapters synthesized at compile time:
  - *Temporal transforms*: `AggregateMean(window)`, `CumulativeSum(season)`, `Resample(frequency, method=spline)`, `DiscountToPresent(rate)`.
  - *Spatial transforms*: `AreaWeightedSum(boundary_polygon)`, `PointExtract(lat, lon)`, `ZonalStatistics(raster, zones)`.
- If an edge attempts to bind a daily time-series to an annualized input without an explicit or inferrable aggregation operator, the graph compiler flags a compile-time resolution error.

## What would resolve it?

1. Specifying the formal syntax for spatio-temporal edge adapters within the graph compilation lifecycle.
2. Implementing a reference test case tracing daily precipitation data down to an annualized crop yield input without manual data wrangling.

## Linked context

- `[[concept-end-state-vision]]`: The multi-tier cascade requires seamless linking from physical earth systems to annualized financial models.
- `[[question-semantic-variable-disambiguation]]`: Temporal framing is a fundamental component of variable semantic identity.
