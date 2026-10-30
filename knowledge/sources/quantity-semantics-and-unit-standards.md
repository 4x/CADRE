---
id: source-quantity-semantics-and-unit-standards
type: source
title: Quantity Semantics, Units, Observations, and Context — Research Evidence
summary: Primary-source evidence from QUDT, UCUM, SOSA/SSN, SemSim, CF, XBRL, SKOS, SHACL/OWL, and unit libraries; dimensions and names cannot establish semantic substitutability.
status: active
created: '2026-10-28'
updated: '2026-10-28'
topics:
  - representation
  - ontology
  - typing
confidence: medium
relations:
  - type: supports
    target: investigation-model-variable-quantity-representation
  - type: relates-to
    target: question-dimensional-and-unit-type-system
  - type: relates-to
    target: question-semantic-variable-disambiguation
---

# Quantity Semantics, Units, Observations, and Context — Research Evidence

## Provenance

Research agents read the linked primary specifications, first-party papers, and official documentation on 2026-10-28; UCUM was also inspected directly. Version anchors describe sources read, not a latest-version or implementation-support claim. No unit engine, ontology reasoner, compatibility matcher, or import pipeline was tested. Application implications are explicitly distinguished from standard requirements.

## QUDT and OM: distinguish kind, quantity, value, unit, and dimension

- [QUDT schema 2.1.29](https://www.qudt.org/doc/2023/07/DOC_SCHEMA-QUDT-v2.1.html) distinguishes quantity kinds, quantities, quantity values, units, and dimension vectors. A kind describes a category; a particular quantity concerns a particular thing; a value expresses its magnitude using a unit.
- QUDT has unit conversion multiplier/offset properties and logarithmic-unit concepts. These do not certify arbitrary conversion code or model compatibility.
- [Energy](https://qudt.org/vocab/quantitykind/Energy) and [Torque](https://qudt.org/vocab/quantitykind/Torque) are distinct kinds sharing the SI dimension vector L^2 M T^-2. Dimensional equality cannot justify treating them as interchangeable model ports.
- [OM 2 project](https://github.com/HajoRijgersberg/OM) offers another OWL vocabulary of quantities, measures, units, and dimensions, including a distinction between temperature scales and differences. This review did not verify a full QUDT/OM equivalence mapping or select both vocabularies.
- Project implication: reuse stable unit/kind references where they fit; retain a project/domain concept and context when the external kind is too broad. Do not treat one external IRI as a complete quantity identity or assume that each unit identifies exactly one kind.

## UCUM 2.2: unit communication, not domain semantics

- [UCUM specification](https://ucum.org/ucum), version 2.2 dated 2024-06-17, defines machine-readable unit atoms/expressions and semantics. Full conformance compares unit expressions semantically; limited conformance may compare literals.
- UCUM includes special units on non-ratio scales with forward/inverse transformations, including interval and logarithmic scales. They are not ordinary multiplicative units. Arbitrary/procedure-defined units have no general dimension or general commensurability.
- Curly-brace annotations do not contribute unit semantics and are discarded by a fully conformant parser. A tag in a UCUM expression cannot safely substitute for a typed analyte/entity/domain qualifier.
- Project implication: distinguish ratio, affine point, delta, logarithmic, arbitrary/procedure-specific, and contextual quantities. Unit normalization must not erase the original source notation or scientific meaning. UCUM syntax and QUDT IRIs can complement one another, but a tested crosswalk/profile is necessary; they are not interchangeable serializations by default.

## Observations: SOSA/SSN

- [W3C SOSA/SSN Recommendation](https://www.w3.org/TR/vocab-ssn/) separates observation, observable property, feature of interest, procedure, result, and temporal context. The property definition is not an observation activity and the result is not the whole observation.
- This provides a precedent for distinguishing river discharge as a property from a measured/estimated value for a particular river, procedure, and time. A unit/kind describes part of the result; it does not supply the rest of the observation.
- Project implication: observations, model predictions, and hypothetical scenarios should be distinct contextual assertions even when their numeric result shape is identical. Reusing SOSA ideas does not imply that every finance projection is literally a sensor observation.

## Composite semantic annotations: SemSim

- [SemSim composite annotation paper, 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2797541/) and [model reuse/merging paper, 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989341/) explain physical property plus bearer and location/part relationships, e.g. pressure of blood in the aorta.
- [SemSim library OPB API](https://sys-bio.github.io/libsemsim-docs/cppapi/opb.html), [entity API](https://sys-bio.github.io/libsemsim-docs/cppapi/entity.html), [entity-descriptor API](https://sys-bio.github.io/libsemsim-docs/cppapi/entity_descriptor.html), and [qualifiers](https://sys-bio.github.io/libsemsim-docs/cppapi/biomodels_qualifiers.html) were read as v0.1.0 API documentation. OPB means Ontology of Physics for Biology. These pages are not evidence of a current universal ontology release or production equivalence solver.
- Composite annotation supports disambiguation and candidate matching; the papers do not establish that annotation equality proves mathematical, numerical, or domain substitutability.
- Project implication: a property-plus-bearer/context design has concrete precedents. It is more defensible than minting a global variable ID for each spelling or requiring a single huge enumerated dictionary of all combinations.

## Climate/forecast data: CF

- [CF 1.7 specification](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/cf-conventions.html) was the version read; this is not a claim that it is latest.
- [Standard names](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/build/ch03s03.html) supply definitions and canonical units; actual units must be physically compatible, accounting for applicable modifiers/cell methods. Names may express qualifiers/sign conventions, not just a label.
- [Coordinate types](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/build/ch04.html) and [cell methods](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/build/ch07s03.html) distinguish locations, bounds, and how values represent a cell: point, sum, mean, maximum, variance, etc.
- Accumulated precipitation and precipitation rate differ; a mean rate over an interval differs from an instantaneous rate even when units coincide.
- Project implication: shape alone is inadequate. Keep coordinate values, bounds/support, calendar/time zone where relevant, and aggregation methods. Array alignment/resampling is a scientific transformation, not a benign rename.

## Financial facts: XBRL

- [XBRL 2.1 Recommendation with 2013 errata](https://www.xbrl.org/specification/xbrl-2.1/rec-2003-12-31/xbrl-2.1-rec-2003-12-31+corrected-errata-2013-02-20.html) distinguishes taxonomy concepts, facts, contexts, and units. Numeric facts refer to a context and unit. Concepts have instant/duration period types; contexts identify reporting entity and period and support additional reporting circumstances.
- [SEC XBRL glossary](https://www.sec.gov/data-research/structured-data/inline-xbrl/xbrl-glossary-terms) explains axes, domains, members, entity/reporting context, and monetary/share units. This research used it for dimensional-context explanation; it did not completely review the separate XBRL Dimensions specification.
- A cash balance at a date and revenue over a quarter can both be USD, but stock versus duration flow and concept identity differ. Taxonomy naming also does not erase GAAP/IFRS/entity/consolidation differences.
- Project implication: a monetary amount needs currency and applicable date/period, price basis where relevant, reporting entity/boundary, convention, and information vintage. FX direction/rate/date and inflation base-year changes are explicit contextual transformations, not fixed SI-like conversions.

## Mapping and validation: SKOS, OWL, SHACL

- [SKOS Reference](https://www.w3.org/TR/skos-reference/) and [namespace schema](https://www.w3.org/2004/02/skos/core) define mapping strengths. `closeMatch` is symmetric; `exactMatch` is symmetric/transitive and stronger. Neither is a casual permission to collapse all source records or all runtime contexts. `owl:sameAs` is an identity assertion, not a fuzzy synonym edge.
- [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/) explains open-world reasoning: absent facts can remain unknown. Lack of contradiction is not proof that all required metadata is explicitly supplied.
- [SHACL Recommendation](https://www.w3.org/TR/shacl/) describes graph validation against shapes: cardinality, types, patterns, and other constraints. SHACL-SPARQL extends expressiveness; Core-only tools need not implement every extension.
- Project implication: graph reasoning, record validation, numerical/type checking, scientific applicability, and evidence verification are different obligations. Passing a shape is not empirical validation. An unknown meaning should block automatic certification of a binding rather than silently count as compatible.

## Unit libraries as operational examples, not selected dependencies

- [Pint temperatures](https://pint.readthedocs.io/en/stable/user/nonmult.html) distinguishes offset temperatures and delta temperatures; subtraction of points yields a delta, while adding offset points is ambiguous and rejected by default.
- [Pint contexts](https://pint.readthedocs.io/en/stable/user/contexts.html) enables named, parameterized transformations such as wavelength/frequency. A contextual transformation may cross dimensions and is not ordinary universal unit conversion.
- [UDUNITS guide](https://docs.unidata.ucar.edu/udunits/current/udunits2prog.html) describes numeric conversion of compatible units. CF uses UDUNITS-style unit strings in relevant metadata. Unit libraries do not decide energy versus torque, GAAP versus IFRS, or observation versus forecast.
- Exact library/version/license/runtime suitability and required edge-case behavior remain untested. This investigation selects no unit-engine dependency.

## Evidence boundary

The external evidence strongly supports separating dimensions, unit scale, quantity kind, contextual property, local declaration, and measured/model-generated value. It does not prove universal automated matching, a complete ontology, or a specific project's safe conversion implementation. Those require scoped validation and domain evidence.
