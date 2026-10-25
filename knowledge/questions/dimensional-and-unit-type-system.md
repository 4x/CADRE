---
id: question-dimensional-and-unit-type-system
type: question
title: Dimensional and Unit Type System
summary: How should Connected Models represent physical/economic dimensions, unit systems, state-dependent conversions, and higher-order tensor/distribution shapes?
status: active
created: '2026-10-24'
updated: '2026-10-24'
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

- **Dimensional Algebra**: Quantities can be decomposed into integer powers of fundamental base dimensions:
  $$[Q] = [L]^\alpha \cdot [M]^\beta \cdot [T]^\gamma \cdot [I]^\delta \cdot [\Theta]^\epsilon \cdot [N]^\zeta \cdot [J]^\eta \cdot [\text{Currency}]^\theta$$
- **Unit Standards**:
  - **QUDT (Quantity, Unit, Dimension, and Type)**: Comprehensive RDF-based ontology defining units, dimensions, and conversion multipliers.
  - **UCUM (Unified Code for Units of Measure)**: Unambiguous algorithmic syntax for physical quantities used widely in healthcare and scientific instrumentation.
- **Conversion Classes**:
  1. *Linear conversions*: $y = k \cdot x$ (e.g., $m \to km$, $MW \to kW$).
  2. *Affine conversions*: $y = k \cdot x + c$ (e.g., $^\circ\text{C} \to \text{K}$).
  3. *State-dependent / Dynamic conversions*: Non-static conversions that require an intermediate model or empirical feed (e.g., converting $USD \to EUR$ via an FX rate node, or converting barrels of oil to $GJ$ via a crude density and caloric model).

## What would resolve it?

1. Selecting or adapting an existing open unit ontology (e.g., QUDT or UCUM) versus defining a lightweight native schema.
2. Formulating how the graph compiler automatically injects unit-conversion adapter nodes along edges when dimensions match but units differ.
3. Specifying how higher-order tensor shapes and probability distribution types are declared in the variable signature.

## Linked context

- `[[concept-end-state-vision]]`: Establishes strongly-typed execution pipes as a non-negotiable invariant.
- `[[hypothesis-global-variable-namespace-compatibility]]`: Hypothesizes that models can link organically through shared dimensional typing.
- `[[question-model-node-ast-and-schema-representation]]`: Node AST signatures must embed these dimensional types.
