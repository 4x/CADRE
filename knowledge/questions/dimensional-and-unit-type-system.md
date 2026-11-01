---
id: question-dimensional-and-unit-type-system
type: question
title: Dimensional and Unit Type System
summary: How should Connected Models represent physical/economic dimensions, unit systems, state-dependent conversions, and higher-order tensor/distribution shapes?
status: active
created: '2026-10-24'
updated: '2026-10-31'
topics:
  - representation
  - typing
  - ontology
confidence: high
relations:
  - type: relates-to
    target: concept-end-state-vision
  - type: relates-to
    target: hypothesis-global-variable-namespace-compatibility
  - type: relates-to
    target: question-model-node-ast-and-schema-representation
  - type: relates-to
    target: investigation-model-variable-quantity-representation
---

# Dimensional and Unit Type System

## Question

How should Connected Models formally represent physical and economic dimensions, unit systems, conversion mechanics (linear, affine, and state-dependent), and higher-order data shapes (scalars, vectors, tensors, and probability distributions) to guarantee compile-time type safety across graph edges?

## Why it matters

A foundational value proposition of Connected Models is eliminating error-prone manual ETL and ensuring that composed models are dimensionally sound. If edge bindings rely on naive string matching of units (as was prototyped in 2025 via the `unit` table), catastrophic failure modes emerge:
- **Unit mismatch**: Connecting an acceleration in $m/s^2$ to an input expecting $km/h^2$ produces silent, disastrous numerical errors.
- **Dimensional incompatibility**: Attempting to connect a cost in $USD$ directly into an energy demand variable in $MWh$.
- **Tensor / Shape mismatch**: Passing an ensemble vector ($10{,}000$ Monte Carlo samples) or geospatial raster into a node designed for a scalar point estimate.

The system requires a formal dimensional type system that catches errors at graph compilation time while automatically synthesizing valid unit conversion adapters.

## Current partial answer

### Bounded mechanics extension — 2026-10-31

Runtime 0.3 uses four physical/currency dimension axes (mass, length, time, currency) and profile `cm-vocabulary/mechanics-1`. It retains all previous kWh/Wh/USD/tariff numerical scales. The numerical basis is kWh, metre, second and USD; its derived mass base is 3,600,000 kg, so a kg has scale 1/3,600,000 and a joule also has scale 1/3,600,000. Thus mass × velocity² and force × displacement close dimensionally and numerically without rewriting old expressions or conversion constants. Dimension vectors changed representation; this is explicitly versioned rather than interpreting historical two-axis manifests as the new profile.

The finite built-in vocabulary adds mass, position/displacement, duration, speed/velocity, acceleration, force and qualified mechanical energies, with a small set of ratio units/lexical aliases. Exact quantity and per-port context checks still prevent automatic speed/velocity, frame, work/heat/electricity bindings. Dimensionful powers required bounded literal integer exponents until runtime 0.16.0 (2026-11-01), which extended the grammar to bounded exact-rational exponents over `Fraction` dimension vectors per [[decision-rational-exponent-engine-extension]]; general roots as functions, affine temperatures and new physical dimensions remain unsupported. Vocabulary additions are code-reviewed, tested profile releases, not arbitrary query-time mutations or a universal ontology.

Separately reviewed constant-acceleration records are projected through generic `connected_models.integration` into distinct `r1.runtime1` versions, preserving original research, full review, guards, expression, contexts and profile/digests. [[source-mechanics-independent-audit]] records scientific dispositions and integration evidence. Three legacy saved heating runs replay with unchanged outputs and unchanged original bytes. This demonstrates a bounded additive extension; it does not resolve the general type-system question.

- **Dimensional Algebra**: A useful physical-unit subset uses powers of base dimensions (with a declared dimension system; some derived-unit systems need rational exponents). The earlier illustrative formula below adds currency as a project-level modeling convenience, **not a claim that all money has a fixed SI-like conversion or that dimensions determine semantic kinds**:
  $$[Q] = [L]^\alpha \cdot [M]^\beta \cdot [T]^\gamma \cdot [I]^\delta \cdot [\Theta]^\epsilon \cdot [N]^\zeta \cdot [J]^\eta \cdot [\text{Currency}]^\theta$$
- **Unit Standards**:
  - **QUDT (Quantity, Unit, Dimension, and Type)**: Comprehensive RDF-based ontology defining units, dimensions, and conversion multipliers.
  - **UCUM (Unified Code for Units of Measure)**: Unambiguous algorithmic syntax for physical quantities used widely in healthcare and scientific instrumentation.
- **Conversion Classes**:
  1. *Linear conversions*: $y = k \cdot x$ (e.g., $m \to km$, $MW \to kW$).
  2. *Affine conversions*: $y = k \cdot x + c$ (e.g., $^\circ\text{C} \to \text{K}$).
  3. *State-dependent / Dynamic conversions*: Non-static conversions that require an intermediate model or empirical feed (e.g., converting $USD \to EUR$ via an FX rate node, or converting barrels of oil to $GJ$ via a crude density and caloric model).

## Investigation result — 2026-10-28

[[investigation-model-variable-quantity-representation]] and [[source-quantity-semantics-and-unit-standards]] distinguish dimensions, units/scales, quantity kinds, contextual quantities, and values. QUDT supplies kind/unit vocabulary; UCUM supplies machine-readable unit syntax/semantics. They are complementary, not interchangeable encodings; a bounded crosswalk and actual engine behavior still need tests. Energy and torque share dimensions but not meaning. Dimensionless probability, angle, count, ratio, and rate convention must not collapse into one interchangeable type.

Recommend explicit ratio/point/delta/log/arbitrary/contextual treatment, with tested linear/appropriate affine conversions only where meaning is preserved. FX, price-year rebasing, density-dependent conversions and time aggregation require declared data/model transforms. Shape requires named axes/support, not just lengths; numeric dtype/precision and source lexical values need explicit policy. Static checks and checks of actual bound values are separate; no universal compile-time safety claim is established by this desk investigation.

No unit library, ontology subset, conversion implementation, or complete numeric/shape schema is selected. The report proposes temperature point/delta, energy/torque, wrong-axis, finance-context and unknown-unit trials; none was run. [[concept-layered-model-representation]] summarizes the provisional contract.

## Minimum answer for the first build

**B — before automatic edge binding/conversion** ([[question-build-readiness]]). Choose a supported quantity/unit encoding and shape system, a canonical serialization for numbers, and clear compile-time versus bound-input runtime checks. Which conversions are safe linear/affine adapters, and which require an explicit model/data dependency (e.g., FX and price-year conversion)? Distinguish a temperature level from a temperature difference, percentage from fraction, scalar from series/ensemble, and currency/date scope where relevant.

Existing standards and libraries are candidates for research, not selected dependencies. A small declared unit subset may suffice; unsupported units/shapes/conversions must fail explicitly rather than be guessed by Meta. Define conversion provenance and precision/tolerance behavior, and cover one valid conversion plus incompatible dimensions, affine misuse, and shape mismatch in acceptance examples.

This question owns physical/numeric compatibility; [[question-semantic-variable-disambiguation]] owns meaning and [[question-temporal-and-spatial-data-alignment]] owns scope transforms. The universal unit ontology is not a prerequisite for an initial supported contract.

## What would resolve it?

1. Selecting or adapting an existing open unit ontology (e.g., QUDT or UCUM) versus defining a lightweight native schema.
2. Formulating how the graph compiler automatically injects unit-conversion adapter nodes along edges when dimensions match but units differ.
3. Specifying how higher-order tensor shapes and probability distribution types are declared in the variable signature.

## Linked context

- `[[concept-end-state-vision]]`: Establishes strongly-typed execution pipes as a non-negotiable invariant.
- `[[hypothesis-global-variable-namespace-compatibility]]`: Hypothesizes that models can link organically through shared dimensional typing.
- `[[question-model-node-ast-and-schema-representation]]`: Node AST signatures must embed these dimensional types.
