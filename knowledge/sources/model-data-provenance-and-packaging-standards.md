---
id: source-model-data-provenance-and-packaging-standards
type: source
title: Model Data, Provenance, Validation, and Packaging — Research Evidence
summary: Primary-source evidence on JSON Schema/JSON-LD/SHACL, PROV, xarray/Arrow/NetCDF/HDF5/Zarr, SED-ML/OMEX, and uncertainty descriptors; no implementation or interoperability claims.
status: active
created: '2026-10-28'
updated: '2026-10-28'
topics:
  - representation
  - lifecycle
  - uncertainty
confidence: medium
relations:
  - type: supports
    target: investigation-model-variable-quantity-representation
  - type: relates-to
    target: question-registry-storage-and-versioning
  - type: relates-to
    target: question-uncertainty-and-epistemic-bounds-serialization
---

# Model Data, Provenance, Validation, and Packaging — Research Evidence

## Provenance and limits

Official specifications/documentation and first-party papers read by research agents on 2026-10-28; PROV-O was additionally inspected directly. Version anchors describe evidence reviewed, not a latest-version guarantee. This is desk research, not a storage benchmark, schema implementation, archive conformance test, or reproducibility experiment. Recommendations derived from it belong in [[investigation-model-variable-quantity-representation]].

## Structural validation versus semantic graphs

- [JSON Schema specification index](https://json-schema.org/specification), [2020-12 Core](https://json-schema.org/draft/2020-12/json-schema-core), and [2020-12 Validation](https://json-schema.org/draft/2020-12/json-schema-validation) define dialects/vocabularies, references, assertions, and annotations over JSON instances. Assertions cover types, required properties, bounds, and array constraints. In the standard dialect, `format` is annotation by default; an optional assertion vocabulary changes behavior. A validator's actual configuration matters.
- JSON Schema's conceptual numbers allow arbitrary-precision decimals; host-language parsers may not. A JSON number does not itself guarantee exact monetary arithmetic or preservation of every lexical digit. Cross-record referential integrity, unit algebra, arbitrary dependent-shape checks, source fidelity, and scientific validity require additional mechanisms.
- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) maps JSON terms to IRIs and represents linked data/RDF graphs. It is not a replacement for application record validation. Remote contexts introduce resolution/version dependencies unless controlled.
- [SHACL](https://www.w3.org/TR/shacl/) validates RDF graphs using shapes; optional SPARQL-based constraints are distinct from Core support. Its graph constraints do not validate scientific binary array content or certify that a semantic assertion is true.
- Project implication: a local typed manifest can coexist with IRI-backed semantic links and a derived graph; adopting all RDF tooling at the outset is not mandated by the problem. Any claimed graph projection roundtrip must be explicitly specified and tested.

## Data models and payload formats

| Source read | Established behavior | Boundary for Connected Models |
| --- | --- | --- |
| [xarray data structures](https://docs.xarray.dev/en/latest/user-guide/data-structures.html) | DataArray associates values with named dimensions, optional coordinates, and attributes; Dataset groups arrays. xarray is a programming/data model, not a file format. Attributes are generally not interpreted as scientific meaning by the library. | Good conceptual precedent for named axes; does not establish unit/meaning correctness or safe arbitrary automatic alignment. |
| [Arrow columnar format](https://arrow.apache.org/docs/format/Columnar.html), [PyArrow data model](https://arrow.apache.org/docs/python/data.html) | Typed columns/arrays, record batches, tables, nested types, decimal/time types, and null validity. PyArrow normally distinguishes a valid NaN from null. | Useful tabular/columnar exchange; scientific coordinate support and context need a profile. Do not flatten N-D arrays without a declared coordinate mapping. |
| [NetCDF dataset components](https://docs.unidata.ucar.edu/nug/current/netcdf_data_set_components.html) | Named dimensions, typed variables with shapes, attributes; coordinate-variable conventions and enhanced NetCDF-4 groups/types. | A scientific array data model with conventions layered above it; names/dimensions alone do not prove semantic compatibility. |
| [HDF5 datasets](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_d__u_g.html), [NetCDF structure/performance](https://docs.unidata.ucar.edu/nug/current/file_structure_and_performance.html) | HDF5 dataset datatype, dataspace, attributes, chunking/compression/fill/resizing; NetCDF-4 uses HDF5 with its own data model. External dependencies are possible. | General storage is not a domain ontology; audit dependencies, filters, and resource use. No comparative performance measured. |
| [Zarr v3 core](https://zarr-specs.readthedocs.io/en/latest/v3/core/index.html) | N-D typed arrays with shape, chunks, codecs, fill values, optional dimension names, and extension/version rules. | Does not by itself give scientific coordinate, unit, observation, or provenance semantics. Pin codecs/extensions for archival use. |
| [xarray I/O](https://docs.xarray.dev/en/stable/user-guide/io.html) | Describes on-disk encodings and `_FillValue`/NaN transformations. | Storage missingness and scientific reasons for missingness are distinct; transformations can affect precision and interpretation. |

No large-data format is selected here. Choosing one should follow the actual workload, not an assumption that every model variable requires a tensor store. Inline small values and referenced large artifacts can share the same semantic contract.

## Provenance and version lineage

- [PROV-DM](https://www.w3.org/TR/prov-dm/) and [PROV-O](https://www.w3.org/TR/prov-o/), W3C Recommendations 2013, distinguish Entity, Activity, Agent and relations for use, generation, attribution, association, derivation, revision, and timing.
- PROV-O supports qualified relations, e.g. `qualifiedDerivation` with source entity and activity detail. A version-specific entity can be related to the more general thing it specializes; alternate/revision relations have their own semantics.
- A curated source/model/data artifact can be an entity; extraction, review, conversion, and execution activities; humans/software agents. This does not automatically record exact parameters, executable digest, environment, seed, source location, review eligibility, or scientific validity.
- Project implication: use a small PROV-aligned profile plus required project-specific fields. Provenance is evidence of origin/process, not a truth or quality guarantee. A content hash establishes byte identity, not mathematical or empirical equivalence.

## Models versus experiments versus archives

- [SED-ML official site](https://sed-ml.org/) identified Level 1 Version 5 as current when read. SED-ML describes simulation experiments using model references/changes, simulation settings, tasks, and outputs; it is separate from model encoding. A task associates model and simulation. This review did not implement or validate L1V5 files.
- [COMBINE standards](https://co.mbine.org/standards/), [OMEX specification description / original paper, 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4272562/), and [archive format page](https://github.com/combine-org/combine-specifications/blob/main/specifications/omex.md) describe packaging multiple model/experiment/data/metadata files in a ZIP-based archive.
- The original paper describes OMEX v1 with root `manifest.xml`, relative content locations and format identifiers, optional master flags, and optional RDF metadata. This is not a complete review of every later archive revision.
- A manifest path/format/master flag is not a persistent scientific identity, integrity digest, executable proof, or actual-run record. Offline interpretation requires retained artifacts, declared versions, and controlled references.
- Project implication: preserve ModelDefinition, ExperimentSpecification, and Run separately even if the first build stores them as simple JSON documents; do not make OMEX or SED-ML mandatory for elementary scalar models solely because they exist.

## Uncertainty descriptors

- [ProbOnto original paper, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5013898/) describes distribution families, parameterizations, and reparameterization relationships, including multivariate distributions. This supports naming the distribution **and parameterization**, not storing an ambiguous `sigma` value. The [official site](https://probonto.org/) was not fetchable; current maintenance, current release, and exact coverage remain unverified.
- [OGC UncertML document](https://portal.ogc.org/files/?artifact_id=33234) redirected to [a PDF](https://docs.ogc.org/dp/08-122r2/08-122r2/pdf) that the reader could not extract. Approval status, detailed constructs, correlation support, and applicability were **not verified**; treat it as an unverified candidate rather than adopted authority.
- Neither source establishes automatic universal uncertainty propagation. Parameter distributions need support, units, family/parameterization, origin, and dependence structure; independent marginal descriptors do not imply independence.
- Samples need joint draw identities/coupling, not just equal array length. Validity, numerical error, model disagreement, epistemic origin, scenario spread, and probability distributions are different concepts. These are project-level implications, not claims that a particular uncertainty standard already solves them.

## Security evidence and implications

- [OWASP XXE guidance](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html) describes external-entity/DTD risks and parser hardening. XML/model archives are untrusted inputs, not permissions to fetch arbitrary references or execute code.
- [ZIP path traversal guidance](https://developer.android.com/privacy-and-security/risks/zip-path-traversal) illustrates entries escaping an extraction destination. Apply controlled paths, expanded-size/count limits, and isolated extraction when importing OMEX-like packages.
- These guidance documents do not certify any parser/runtime used here; none was installed or tested. JSON references, JSON-LD contexts, XML imports, array external references, and execution artifacts require explicit allowlists/resolution policies.
