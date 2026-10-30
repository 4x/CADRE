---
id: investigation-model-variable-quantity-representation
type: investigation
title: Model, Variable, and Quantity Representation
summary: Completed desk investigation comparing representation standards and approaches; recommends a provisional layered contract separating semantic quantities, local symbols, values, model versions, implementations, composition, evidence, and runs. No interoperability trials performed.
status: completed
created: '2026-10-28'
updated: '2026-10-28'
topics:
  - representation
  - ontology
  - architecture
confidence: medium
relations:
  - type: addresses
    target: question-model-node-ast-and-schema-representation
  - type: addresses
    target: question-dimensional-and-unit-type-system
  - type: addresses
    target: question-semantic-variable-disambiguation
  - type: addresses
    target: question-registry-storage-and-versioning
  - type: relates-to
    target: question-temporal-and-spatial-data-alignment
  - type: relates-to
    target: question-uncertainty-and-epistemic-bounds-serialization
  - type: relates-to
    target: question-graph-topology-and-feedback-cycles
  - type: relates-to
    target: concept-specialized-model-curation-agents
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: investigation-prototype-2025-mathjs-supabase
  - type: uses
    target: source-mathematical-model-representation-standards
  - type: uses
    target: source-quantity-semantics-and-unit-standards
  - type: uses
    target: source-model-data-provenance-and-packaging-standards
  - type: produces
    target: concept-layered-model-representation
---

# Model, Variable, and Quantity Representation

## 1. Executive conclusion

**Recommend a layered representation, not a universal variable table, a universal expression AST, or a graph of untyped equations.** The repository should standardize identity, interfaces, quantity semantics, evidence, and versioning, while admitting distinct mathematical formalisms and execution payloads behind those contracts.

The most important separations are:

1. **Semantic concept / quantity kind:** what sort of thing is being represented.
2. **Contextual quantity specification:** whose property, under which convention, over what support.
3. **Local symbol declaration / port:** how that quantity appears in one particular model.
4. **Value assertion:** a particular observed, projected, hypothetical, or generated value with context and provenance.
5. **Mathematical model definition/version:** relations, assumptions, applicability, and local declarations.
6. **Implementation and execution capability:** how a particular artifact can evaluate/simulate/solve that model.
7. **Composition, experiment, and actual run:** selected instances/bindings, requested operation/settings, then actual execution and results.
8. **Evidence/review/mapping claims:** attributable, scoped claims, not properties made true by successful schema validation.

A canonical **boundary and curation contract** is useful; one canonical mathematical normal form for everything is not a defensible prerequisite. Start with a deliberately small algebraic profile and an allowlisted structural expression representation. Preserve richer source models as declared, potentially non-executable records until a supported adapter exists. The exact JSON Schema, unit engine, storage technology, semantic vocabulary subset, and adapter stack still require trials.

**Status:** completed desk investigation, medium confidence in the overall project recommendation, not an accepted architecture. No dependency installation, model curation run, benchmark, executable schema, import/export roundtrip, security test, or empirical model validation was performed. Strong confidence in the need for the distinctions above; lower confidence in the cost and sufficiency of the proposed first profile.

## 2. Charter, preflight, and method

User request, 2026-10-28: comprehensively investigate representation of models, variables, and other quantities; how others do it; alternatives, tradeoffs, and best fit for Connected Models. This record was initialized as active **before** external research, following PROJECT_STATE, pmem search/context, and overlap review. It was completed after evidence synthesis; linked platform questions remain active.

### Already known

- Dedicated Meta/Muse curators primarily or exclusively work offline from scientific papers, textbooks, and other sources, turning models into reusable repository components. Query-time answering consumes eligible existing versions. Inline curation is forbidden or last-resort-only; the permanent exception policy is not selected.
- Source fidelity, meaning, units, applicability, evidence, unknown uncertainty, and versioned run lineage matter. Repeated gap-filling must not become trusted knowledge by repetition.
- The 2025 prototype demonstrated a useful hierarchical algebraic composition pattern. Its one-table graph design is provisional, not a universal ontology.

### Rejected/paused, unresolved, and possibly stale

- Standalone Math.js as the **sole** execution architecture is retired; social/marketplace work remains paused. Neither is reopened by this research.
- Envelope/payload separation and compositional semantics were promising hypotheses, not researched decisions. Model identity, variable scope, values, canonicalization, supported formalisms, and storage ownership were unsettled.
- Older statements that strings cannot represent ODEs/AD, Math.js has no matrix support, or large ontologies are necessarily brittle were too categorical. Distinguish a prototype's capabilities from a library's facilities and from a language's expressiveness. See §14 for corrections.

### Method and source boundaries

Four focused research streams read primary specifications, official documentation, and original papers: mathematical formalisms/interfaces; quantity semantics/units/context; data/provenance/packaging; additional statistical/optimization/semantic precedents. Evidence digests:

- [[source-mathematical-model-representation-standards]]
- [[source-quantity-semantics-and-unit-standards]]
- [[source-model-data-provenance-and-packaging-standards]]

Version anchors identify documents reviewed, not newest-version claims. Exact URLs and retrieval limitations are preserved in those source records. Criteria: fidelity and expressiveness; safe composition; offline extraction; semantic scope; values/shapes/time/space; uncertainty and evidence; reproducibility; security; adoption burden; extensibility and lock-in. Comparisons below are qualitative engineering judgments, not measured scores or performance results.

## 3. What are we actually representing?

### 3.1 A variable is not a globally unique real-world quantity

`r` could be interest rate, radius, resistance, or a local residual. Even two occurrences of `revenue` may have different accounting rules, entity boundaries, periods, and information vintages. Conversely, `Q`, `flow`, and `discharge` may denote compatible quantities with different spellings.

Use stable, **model-local symbol identity**, retaining original notation and an explicit semantic mapping. Do not globally merge symbols because their names, dimensions, or embeddings match. Bound variables in sums/integrals have lexical scope; renaming must avoid capture. An array index is not necessarily a physical measured quantity. A time variable can be an independent coordinate, not a model output.

Three identities that must not collapse:

- `concept:revenue`: a reusable semantic concept, potentially qualified by a taxonomy/methodology.
- `model-A@revision#revenue`: a local declaration with a type, role, assumptions, and semantic specification.
- `value-X`: a specific assertion about company C's revenue for interval P under convention M, sourced as of information vintage V.

A contextual specification can be shared if genuinely identical; it need not be a separately minted global node for every record. Stable references matter more than forcing an object explosion.

### 3.2 Kinds, dimensions, units, and meanings differ

- **Dimension:** physical exponent structure in a specified dimension system; useful for algebra, insufficient for meaning.
- **Unit:** a measurement scale/code and conversion semantics, not the property itself.
- **Quantity kind:** energy, torque, length, revenue, etc. Kinds may share dimensions.
- **Contextual property:** pressure of blood in the aorta; revenue of a consolidated company over a reporting period under a particular convention.
- **Value:** magnitude or structured result assigned/asserted in context.

QUDT directly motivates the first distinctions; SOSA/SSN, SemSim, CF, and XBRL demonstrate contextual information that a unit cannot supply. Physical scalar dimensions are not an exhaustive type system: booleans, counts, categories, entities, dates, matrices, distributions, functions, and symbolic expressions need their own types.

Do not model all dimensionless quantities as one interchangeable type: probability, percentage, angle, efficiency, count, leverage, and annual effective rate have different constraints or operations. Currency is not simply another universally fixed-convertible SI base dimension. A financial flow can be a currency amount accumulated over an interval, not necessarily currency/time in its stored representation.

### 3.3 Roles are relative to model and operation

Separate axes rather than use one overloaded `variable_kind` enum:

- **Mathematical role:** independent coordinate, unknown, state, derivative, algebraic variable, index/binder, latent variable, decision variable, derived quantity.
- **Interface role:** input/output/internal under a selected evaluator or adapter. An acausal equation may not have fixed input/output roles until an operation is selected.
- **Variability:** invariant constant, run-fixed parameter, time-varying state/input, discrete event-updated quantity.
- **Statistical/epistemic role:** observed, calibrated/fitted, predicted, scenario-chosen, Meta-generated, unresolved. This often belongs to a particular value/assertion, not the reusable symbol.

`parameter` does not mean observed or immutable forever. A coefficient can be inferred in one experiment and supplied as an input in another. A number fixed within one run is not necessarily a physical universal constant. `pi`, a source-defined coefficient, a measured physical constant, and a calibration estimate deserve different provenance and exactness.

### 3.4 A model is not its code or its experiment

A source scientific model can have multiple implementations, numerical approximations, calibrations, validity regimes, and solver settings. A paper/code pair may describe the same model, not two independent corroborations. Two algebraically equivalent formulas may not have identical floating-point behavior. Solver selection can change results without changing governing equations.

A definition needs mathematical formalism, assumptions, declarations, relationships, domain/applicability, and evidence. Implementations reference the definition revision and declare fidelity/unsupported features and computational capabilities. Experiments select operations, inputs, calibration, horizon/initial conditions, and settings. Runs record what actually happened. This follows complementary precedents in CellML/SBML/Modelica, FMI/BMI, SED-ML, and PROV rather than demanding one format do all jobs.

## 4. How others do it: what to borrow, what not to expect

| Family / examples | What it primarily represents | Good fit here | Important boundary |
| --- | --- | --- | --- |
| Presentation math / LaTeX, Presentation MathML | Source notation and display | Preserve original notation; human review | Ambiguous meaning; not authoritative executable semantics |
| Content math / Content MathML, OpenMath | Structured math objects, operators, binders; OpenMath dictionaries identify symbol meanings | Expression import/export, operator vocabulary, explicit scoped references | Not a complete model, evidence ledger, solver, or universal canonical form |
| Symbolic systems / SymPy, Math.js expression nodes | Manipulable expression trees, supported numerical/symbolic operations | Internal algebra backend, differentiation where supported | Backend-specific semantics and unsafe string parser paths; not the repository ontology |
| Component math languages / CellML, SBML + comp | Domain-oriented components, variables, math, units, rules/events/composition | Learn source-backed component structure and preserve native payloads | Domain choices and import subset matter; XML schema alone is not semantic conformance |
| Equation-based modeling / Modelica | Acausal equations, component connections, parameters/state/events/initialization | Preserve simultaneous systems rather than force fake dataflow | Solver/causalization and domain extensions cannot be replaced by topological sorting |
| Execution exchange / FMI, BMI | Callable interface, values, state/time/grids/metadata/capabilities | Future simulator adapter boundary | May hide internal math; does not prove empirical validity or safe arbitrary coupling |
| Statistical programs / Stan | Probability density, data/latent/parameter roles, constrained domains, generated quantities | Preserve likelihood versus draw and distribution parameterization | Not just deterministic assignments with error bars attached |
| Optimization / Pyomo | Decision variables/domains, constraints, objectives and solve task | Optimization payload later | Expression graph omits objective sense, feasible domain, solution status |
| Semantic quantities / QUDT, UCUM, OM | Kinds, units, dimensions, scales, unit syntax/conversions | Reuse established concepts/codes with a bounded profile | Same units/dimensions do not prove same property/context; crosswalks need testing |
| Domain context / SOSA/SSN, SemSim, CF, XBRL | Property/bearer/procedure, observation/fact context, axes and aggregation | Compositional semantics with source-local qualifiers | No single ontology here is sufficient for every domain or proves equivalence |
| Linked knowledge / RDF, JSON-LD, SKOS, OWL, SHACL | Identity, relations, mappings, inference, graph constraints | Semantic links, attributable mappings, graph projection | Syntax/shape/reasoner success is not scientific truth; unknown is not compatible |
| Typed array/tabular data / xarray, CF/NetCDF, Arrow, Zarr/HDF5 | Named axes/coordinates or physical array/table storage | Rich data contracts without putting large tensors in a graph DB | Data model, disk encoding, and scientific meaning are distinct layers |
| Experiment/provenance/package / SED-ML, PROV, OMEX | Experiment description, lineage, bundle contents | Separate experiment/run/source/evidence artifacts | A package or provenance edge does not prove reproducibility/validity |
| Compiler/workflow IR / ONNX, MLIR, CWL | Computation operators, compiler transformations, or executable workflows | Specialized lowering/export where justified later | Not a universal source-model semantics or quantity ontology |

Source references and versions are in the three evidence digests. This is a comparison of roles, not a ranking by popularity or a recommendation to integrate every standard.

## 5. Major architectural approaches and tradeoffs

### A. Formula strings plus variable/unit metadata

**Pros:** simple extraction, readable, low authoring overhead, preserves familiar notation. **Cons:** spelling/scoping ambiguity, unspecified grammar and operator behavior, weak semantic checks, code injection if executed indiscriminately, divergence between displayed math and executable code.

A string in a specified language is not inherently weak; a well-defined textual DSL can be rich and safe. The bad choice is treating arbitrary LaTeX/Python-like text as an executable universal contract. Keep source text, but parse/validate a supported language before execution. Good source-preservation layer, insufficient by itself as the interchange contract.

### B. One universal symbolic AST / CAS internal representation

**Pros:** structural validation, symbolic manipulation, binders, code generation, shared subexpressions. **Cons:** simultaneous equations, stochastic inference, optimizers, events, grids, and black-box oracles need more than expressions. Backend semantics leak into the registry; unsupported content is easily flattened incorrectly. General equivalence cannot be assumed decidable/automatically canonicalizable across arbitrary executable models.

Recommend a **small expression IR for a declared subset**, not an ambition to invent a full universal CAS before building. Semantic function IDs and explicit assumptions leave room to export/import richer math later.

### C. Adopt one scientific modeling standard as the entire canonical format

**Pros:** established precise constructs, domain tool compatibility, less home-grown math design. **Cons:** imposing biological/physical/statistical structures on unrelated models, difficult agent extraction, missing project-specific evidence/review and epistemic metadata, toolchain/import constraints. CellML is a serious precedent, not a universal answer simply because it already has variables and units.

Good if the first selected domain strongly aligns; otherwise preserve native artifacts plus an envelope. Interchange fidelity must be checked format by format. Do not promise lossless conversion between unrelated formalisms.

### D. Everything as a semantic knowledge graph / RDF/OWL

**Pros:** stable identifiers, cross-source linkage, reusable vocabularies, provenance/mapping relationships, extensible semantic queries. **Cons:** verbose expression/value storage, open-world reasoning does not enforce required record completeness, ontological equality can be too strong, execution/solver semantics still required. Creating full-world ontology governance could dominate the project.

Useful **semantic and evidence layer**, not a reason to store every numeric array element as a graph vertex or to buy/select a graph database. Domain ontologies can be valuable; blanket dismissal as brittle is unjustified. Prefer scoped terms/mappings with ambiguity preserved.

### E. Opaque code/function/container registry

**Pros:** expressive and reuses real scientific software; manageable callable interface. **Cons:** poor internal inspectability, hidden state/data/units, security and environment burden, differentiation/assumption discovery not guaranteed. A wrapper cannot manufacture semantic completeness.

Needed eventually for some real-world models; make transparency/capabilities explicit. Not the first-build default for unreviewed arbitrary downloads. Cataloging an opaque artifact does not make it executable or trusted.

### F. One global variable namespace and automatic wiring

**Pros:** appealing discovery and reuse; fewer repeated semantic descriptions. **Cons:** symbol collisions, context-dependent meaning, excessive equality claims, unclear version governance, massive contextual combinatorics. Even identical quantity specifications can refer to independent scenarios/realizations and must not share one mutable value slot.

Use shared **concepts** plus **local symbols and contextual specifications**, not global mutable variables. Map source-local terms without requiring authors to rewrite notation. A mapping is a scoped claim, not automatic merge authority.

### G. Layered common contract plus specialized payloads — recommended

**Pros:** consistent curation/indexing/interface validation, faithful native formalisms, gradual implementation, scalable offline review; avoids mistaking syntactic uniformity for mathematical uniformity. **Cons:** explicit adapter and mapping work, potential envelope/payload divergence, more entity distinctions, need extension/profile governance and loss reports.

Mitigate with small mandatory core, operation-specific profiles, deterministic cross-checks, pinned extensions, and executable acceptance cases. Do not standardize a dozen backend payloads before one works. This recommendation strengthens the existing envelope/payload candidate but adds semantic/value/evidence/run distinctions; it is not approval of the historical one-table graph schema.

## 6. Proposed logical entity and relationship model

These are **logical distinctions**, not a requirement for one table/file/class per row. An initial document can embed local declarations, facets, and evidence references; shared identities and pinned references matter where reuse/versioning matters.

| Object | Meaning / representative fields | Key non-equivalence |
| --- | --- | --- |
| SourceArtifact / SourceFragment | document/code version, location/hash where retainable, page/equation/table, source notation, license/access | Citation is not a model version or proof |
| SemanticConcept / QuantityKind | stable IRI/local ID, definition, aliases, external vocabulary version/mappings | Concept is not a source-local variable or a value |
| QuantitySpecification | concept/property, bearer/entity selector, measurement/accounting convention, temporal/spatial support, aggregation, price/currency basis, conditions | Same specification does not identify one realization/scenario |
| UnitDefinition / Scale | code/IRI, vocabulary version, dimension system/vector, scale/conversion rules, point/delta/log distinctions | Unit/dimension does not determine meaning |
| ModelDefinitionVersion | stable family ID + immutable revision; formalism, declarations/relations, assumptions, validity, source/evidence links | Model family/version/implementation are separate identities |
| SymbolDeclaration / Port | ID local to revision/component; original symbol, semantic spec ref, data type/shape/unit, mathematical role, variability, optional interface role | Input/output is operation-dependent, not a global property |
| ImplementationArtifact | artifact identity/hash, language/format/version, model revision, backend contract, environment/dependencies, capabilities, fidelity/limits | Runnable code is not automatically faithful or approved |
| Calibration / ParameterSet | model/implementation scope, parameter values, estimation procedure/data, date/population, uncertainty/evidence | A fitted coefficient is not a universal constant |
| ValueAssertion / DatasetVersion | value or artifact reference, spec/context, origin, as-of/phenomenon time, units, precision/missingness/uncertainty, provenance | Data/calculation/scenario/Meta estimate must stay distinguishable |
| Mapping / CompatibilityClaim | source/target, exact/projection/transform/incompatible/unknown, scope, assumptions, evidence, author/review/version | Semantic relation is not universal identity |
| CompositionDefinition | reusable component refs, instances, port bindings, explicit adapters, exposed interface | A composition definition is not its execution schedule |
| ModelInstance / Binding | instance ID, pinned revision/implementation, parameter/input refs, scoped entity/time/scenario substitutions | Two uses of the same model can have independent state/inputs |
| ExperimentSpecification | operation, target outputs, inputs, initial/boundary conditions, horizon/grid/settings, solver/seed policy as relevant | Model does not prescribe every experiment |
| Run / CompiledPlan / Result | resolved manifests, actual artifacts/settings, checks, status, output assertions, logs, timings/usage | Plan is derived; result requires actual execution |
| Evidence / ReviewClaim | claim kind, target revision/use, checks/evidence, author/reviewer, dissent, passed/failed/blocked/untested details | One `verified` flag is not enough |

### Identity and version policy

- Stable repository IDs for model families and semantic concepts; immutable revision IDs for definitions, implementations, datasets, mappings, and experiments used in runs. Human-friendly mutable aliases may resolve at planning time but must become pinned references in the manifest.
- Local symbol IDs are scoped by model revision/component. A source symbol and its normalized ID/notation are recorded together. The same model can be instantiated twice without accidental variable aliasing.
- Content digests establish byte integrity. They are not stable semantic identity, scientific equivalence, review evidence, or a complete cache key. Serialization schema/normalization policy must be versioned before claiming stable hashes across serializers.
- A review targets a specific artifact/revision and declared use/profile. Source/implementation changes do not automatically inherit approval. Withdrawing eligibility affects future selection but does not erase prior run lineage.
- Curation, review, transformation, and execution are separate activities with used/generated artifacts and responsible agents, aligned with PROV concepts. Keep source locations and claim-level extraction provenance, not merely a bibliography on the model card.
- Provenance/evidence, semantic relationships, model/component incidence, and a compiled execution dependency graph are different graph projections. None dictates the physical database.

## 7. Recommended canonical layers and first-build profile

### Layer 1 — semantic contract and curation record

Typed JSON-compatible records with explicit schema/profile versions; stable identifiers and original source notation; required interfaces, assumptions/applicability, source/evidence and AI contribution metadata. Reference selected established quantity/unit terms, plus local concepts with scoped mappings when needed. Definition fields may be unknown, but unknown must be explicit and not count as approval.

Recommend evaluating **JSON Schema 2020-12** for structural validation. This is a research-backed design recommendation, not an installed dependency or completed schema. Add semantic/type/domain/reference validators; JSON Schema alone is insufficient. A JSON-LD/RDF projection can follow if needed, with controlled contexts and roundtrip rules. Do not require an ontology reasoner in the first numerical executor solely to validate mandatory fields.

### Layer 2 — mathematical content with declared formalism

Use a discriminated payload kind and versioned capabilities, e.g. `explicit-algebra`, `equation-system`, `ode-dae`, `probabilistic-program`, `optimization`, `simulator-interface`, `external-oracle`, `composite`. These names are illustrative, not adopted schema identifiers. Catalog-only support is distinct from executable support. Unknown kinds are rejected by the executor, not reinterpreted as formulas.

For the first algebraic profile: an allowlisted structural expression tree with symbol references, typed numeric literals, supported operations/functions, output assignments, and explicit predicates. Preserve source equations/LaTeX alongside it. No `eval`, arbitrary source-code imports, or implicit runtime library names. Define operator semantics: power/domain rules, divide-by-zero, reductions, real/complex support, ordering, scalar broadcasting, missingness, and numeric precision. Unsupported symbols/operators/binders must fail rather than be guessed by Meta.

Before inventing a large AST, test whether a restricted Content MathML/OpenMath-compatible shape or a vetted parser node format plus a stable interchange view meets requirements. A tiny native JSON expression profile may be easiest for agents and validation, at the cost of owning semantics and export tooling. The investigation recommends the **restricted profile**, not an untested exact AST syntax. Native payloads remain first-class for richer source formats; no universal lossless lowering claim.

### Layer 3 — typed values and data artifacts

Scalar/tensor/tabular/distribution/symbolic/categorical types with explicitly supported profiles. A tensor contract needs dtype, named axes, length/labels/coordinates and bounds, units and semantic spec, ordering and missingness. Equal shape is not equal axes. Do not silently align, broadcast, interpolate, sort, change calendars, or drop coordinates.

Small values can be inline; large data can be referenced with hash, format/version, shape/dtype, coordinate schema, and storage encoding. xarray-like named-axis semantics are useful independently of whether Python/xarray is selected. Choose NetCDF/Zarr/HDF5/Arrow only after workload/roundtrip tests; no format winner or performance claim here.

For initial numeric execution, recommend finite real scalar values and narrowly specified short dated arrays only if the chosen anchor needs them. Explicit float64 evaluation is a practical trial candidate, not exact financial accounting. Retain decimal lexical source values and physical units; use tagged exact integers/rationals/decimals or symbolic constants when needed, with deterministic conversion/rounding policy before float evaluation. Do not promise that arbitrary JSON numbers preserve all precision or that all domains can use float64.

### Layer 4 — composition and execution profile

Versioned instances and explicit bindings; validate declarations and actual bound values separately. Recommended first executable subset: reviewed deterministic explicit algebra, declared functions/transforms, and an acyclic inter-model dataflow plan. Algebraic constraints/dynamics can be cataloged honestly as non-executable, not silently oriented or delayed to fit the profile.

A future solver can treat an implicit equation block as a unit with declared unknowns, residuals, initialization, solution branches and solver requirements; a simulator can expose state/time/events through an adapter. Preserving mathematical structure prevents the outer DAG from pretending that everything inside is a pure function. A DAG run plan is an execution profile, not a claim about all scientific models.

### Layer 5 — evidence, provenance, and run manifest

Per-claim source fidelity, dimensional/semantic checking, reference reproduction, empirical evidence, and use eligibility are separate. Use PROV-aligned entities/activities/agents with a small project profile; no need to implement every PROV term. Run manifests pin model/implementation/data/calibration/adapter/mapping versions, scenario context, settings, actual validations/results and failures. Record seed and solver/numeric environment where relevant. Reproducibility limits for external services/inference remain explicit.

### What to standardize now, reuse, defer

| Now (minimum canonical profile) | Reuse as references/precedents | Defer until needed |
| --- | --- | --- |
| Identity/version/scoping; source spans; local symbols/roles; semantic/context contract; units; typed values; explicit algebra; applicability; instances/bindings; evidence/review; run manifest | JSON Schema structure; QUDT kinds/units; bounded UCUM codes with tested crosswalk; SemSim/SOSA contextual distinctions; CF/XBRL examples; PROV lineage | Full RDF/OWL reasoning, universal ontology, general CAS, comprehensive CellML/SBML import, Modelica/FMI/BMI execution, probabilistic/optimization solvers, large tensor store, distributed registry |

This is compatible with offline agents producing rich candidate records before an implementation supports execution. A source-backed mathematical model may be worth storing even if the first executor cannot run it. Do not conflate `cataloged`, `well-formed`, `source-faithful`, `executable`, `reproduced`, `empirically supported`, and `eligible-for-this-use`.

## 8. Safe connection is a checked contract, not a name match

Recommended compatibility outcomes:

1. **Direct compatible binding** under the selected profile and context.
2. **Compatible through an explicit adapter/model**, with declared assumptions and provenance.
3. **Review required / unresolved**, because required semantics or evidence are unknown.
4. **Incompatible or unsupported**, with a reason; no automatic numerical answer from that binding.

Check stages:

- Reference integrity, pinned revisions, supported profiles, execution eligibility/capabilities.
- Mathematical type, dtype/precision, shape/axes and allowed broadcasting.
- Quantity kind/property and bearer/entity/context compatibility; known scoped mappings, not just similar labels.
- Unit scale/dimensions and point/delta/log behavior. Unit convertibility is necessary for some connections, not sufficient for scientific substitutability.
- Temporal support, spatial support/CRS/grids, entity boundary, aggregation, convention, sign/orientation, price/currency basis, calibration/applicability.
- Actual inputs and domain predicates; knowledge available as of the experiment; missing/stale/revised values; uncertainty/dependence policy.
- Visible explanation of adapter assumptions and any generated input reliance.

Some checks can be performed statically; value ranges, predicates, unknown axes, and external data context require binding/runtime checks. Shape validation cannot establish model validity. An LLM can propose semantic mappings offline or a query plan, but cannot certify them through confidence alone.

**Automatic adapters:** begin only with validated linear unit conversions and carefully typed point/delta conversions that preserve meaning. FX, inflation rebasing, time aggregation, coordinate interpolation, density-dependent conversions, method changes, causal re-interpretation, and entity consolidation require declared transformations or domain models, not arbitrary unit-engine context magic.

## 9. Worked representation cases (hand analysis, not executed tests)

### Case A — the same symbol, different quantities; the same concept, different values

Two papers use `r` for radius and annual return. Give each declaration a local ID, retain `r` as notation, and attach different semantic/type specs. Two instances of the same return model can share a quantity specification but refer to different companies/scenarios. They must not share a mutable global `r` slot.

**Distinguishes:** symbol versus concept versus contextual value versus instance. **Failure exposed:** global variable namespace aliasing.

### Case B — small canonical algebra example

The following is an **illustrative design sketch**, not an executable schema, scientifically curated model, exact QUDT mapping, or implementation artifact. `demo:` references denote local illustrative identifiers; review metadata is deliberately not invented. Ohm's relation is used only to make entity boundaries concrete.

```yaml
schema_profile: illustrative-algebra-v0
model:
  id: demo:ohmic-relation
  revision: demo:revision-1
  formalism: explicit-algebra
  source_refs: [demo:source-equation-ref]
  validity:
    description: Ohmic element in the declared operating regime
    predicates:
      - {op: greater-than, args: [{symbol: resistance}, {literal: '0', unit: ohm}]}
  symbols:
    voltage:
      source_symbol: V
      mathematical_role: supplied-quantity
      interface_role: input
      quantity_spec: demo:voltage-across-element
      type: {kind: real-scalar, evaluation_dtype: float64}
      unit: volt
    resistance:
      source_symbol: R
      mathematical_role: supplied-quantity
      interface_role: input
      variability: run-fixed
      quantity_spec: demo:resistance-of-element
      type: {kind: real-scalar, evaluation_dtype: float64}
      unit: ohm
    current:
      source_symbol: I
      mathematical_role: derived-quantity
      interface_role: output
      quantity_spec: demo:current-through-element
      type: {kind: real-scalar, evaluation_dtype: float64}
      unit: ampere
  assignments:
    - target: current
      expression: {op: divide, args: [{symbol: voltage}, {symbol: resistance}]}
value_assertion:
  id: demo:scenario-voltage
  quantity_spec: demo:voltage-across-element
  context: {entity: demo:element-A, scenario: demo:scenario-1}
  value: {kind: decimal, lexical: '12.0', unit: volt}
  epistemic_origin: user-scenario
  uncertainty: {kind: unknown}
instance:
  id: demo:instance-A
  model_revision: demo:revision-1
  context_bindings: {element: demo:element-A, scenario: demo:scenario-1}
  input_bindings: {voltage: demo:scenario-voltage, resistance: demo:resistance-assertion}
```

What is canonical here is the separation and explicit contract, not these field names. A real record also needs exact source location/license, confirmed unit IDs and semantics, source-to-expression trace, implementation identity, review/evidence, parameter/binding completeness, and run configuration. A different evaluator could solve the relation for voltage instead; that must be an explicit supported operation, not arbitrary runtime equation rearrangement. Positive resistance is an assumed applicability choice in this sketch, not a universal rule for all electrical components.

### Case C — energy versus torque

Both have SI dimensions kg m^2 s^-2, and torque is often expressed as N m. Retain distinct quantity kinds. Joule/N m conversion alone cannot authorize routing torque into an energy-demand input. Work can be computed from torque and angular displacement through a declared physical relation with conventions/conditions.

**Outcome:** incompatible direct binding; a model-based transform may be meaningful. **Evidence:** QUDT kind records.

### Case D — temperature point versus temperature difference

A 20 °C temperature is a point; a 20 °C difference is a delta. A difference converts to the same numeric kelvin difference; a point requires an offset. Subtracting two temperature points yields a delta. Arbitrarily summing temperature points or multiplying offset-unit magnitudes is not ordinary ratio-unit arithmetic.

**Outcome:** typed conversion/operation rules, not one affine multiplier applied to every occurrence. **Evidence:** UCUM special units and Pint delta-temperature examples. Neither string suffix guessing nor dimension equality is enough.

### Case E — financial amount and growth/discount conventions

A cash balance at an instant and annual revenue can both be USD. Revenue requires entity/consolidation/accounting/period context; expected forward revenue is not historical reported revenue. Nominal USD of one price year is not real USD of another. FX conversion requires direction, dated rate and often averaging convention. A 5% continuously compounded annual rate is not a 5% annual effective return or a five-year cumulative return.

**Outcome:** inspect concept, instant/interval, method, currency/basis, origin and as-of context. Bind only with explicit supported mappings/transforms; do not infer missing conventions. XBRL provides a concrete precedent for concept/context/unit distinctions; compounding/price-basis additions here are project analysis, not claims that XBRL alone specifies them.

### Case F — arrays with equal dimensions but wrong time support

A length-12 array of monthly mean precipitation rates is not a length-12 array of monthly accumulated precipitation, nor necessarily the same twelve months/calendar. Annualizing a mean rate requires interval durations, coverage and missing-data policy; summing rates is not summing amounts. Mean of nonlinear model outputs need not equal model evaluated at mean input.

**Outcome:** named coordinates, bounds and cell methods; explicit aggregation/integration. Reject mismatches or missing required support. xarray-like labels help but automatic alignment is not scientific justification. **Evidence:** CF/xarray.

### Case G — same property, different bearer/procedure

Arterial pressure and pressure in a different compartment may share units and a broad pressure kind. Instantaneous peak, mean arterial pressure, and instrument-derived estimates differ. Physical property plus bearer/location/method/support makes the distinction explicit.

**Outcome:** scoped semantic mapping, not one global `pressure` variable. **Evidence:** SemSim/SOSA. This is not a recommendation to make a medical domain the first build.

### Case H — implicit system and state dynamics are not assignment cycles to break casually

`x + y = a` and `x - y = b` define simultaneous unknowns. A solver could derive explicit outputs under appropriate assumptions, but the source formulation is not an ordered two-node function pipeline. An ODE `dx/dt = -k*x` additionally needs initial state and time/integration settings. A DAE, event reset, or coupled simulator adds further semantics.

**Outcome:** preserve formalism and declarations; first executor reports unsupported. Do not invent a delay, choose a solution branch, or wrap an unqualified fixed-point loop silently. **Evidence:** Modelica, CellML/SBML, FMI.

### Case I — uncertainty and latent quantities

`normal(mu, sigma)` and a source parameterized by variance/precision are not interchangeable without a declared transform. A posterior parameter, observed measurement, and future draw have different roles. Two sample arrays of equal length are not necessarily paired joint samples. If `y = x - x`, preserving shared realization gives zero; treating the two occurrences as independent uncertain inputs invents variance.

**Outcome:** family plus parameterization/support/units and dependence identity; unknown uncertainty stays unknown. Interval bounds versus confidence intervals versus scenario ranges need distinct tags and interpretation. No generic promise that particles pass through every model: validity constraints, state, discontinuities, solver failure, and computational cost still matter. **Evidence:** Stan, ProbOnto, data-model docs; dependence example is hand reasoning.

### Case J — Meta fallback and later curated replacement

A query lacks an input. A permitted provisional input estimate becomes a run-specific value assertion with origin, reason, unknown uncertainty, and downstream reliance. It is not a new eligible repository model. Offline curators later extract/check a sourced provider, producing a new version and review evidence. A new run binds it; the old run retains its original estimate and versions.

**Outcome:** clean offline/query separation and replaceability. New on-the-fly relationships/submodels must not escape the unresolved forbidden-versus-last-resort policy. This requirement comes from the user, not an external standard.

## 10. Offline curation implications

The canonical target must support **partial, contested, and non-executable knowledge**; otherwise agents are pressured to invent missing semantics to make validation pass.

Recommended extraction sequence, performed separately from answering:

1. Retain source identity/version/license and exact fragments, notation and context. Treat documents/code as untrusted inputs.
2. Identify the model/formalism and local symbols, lexical scope, domains, constants, parameters, units, assumptions and conditions. Do not turn every numeric literal into a global constant or every mentioned quantity into an exposed port.
3. Propose semantic specs and external mappings. Preserve unrecognized terms as local defined concepts and record uncertainty/conflicts; lack of a global vocabulary entry must not prevent cataloging a model.
4. Build the supported mathematical payload or retain a native artifact. Record extraction/normalization steps and any losses/unsupported constructs.
5. Check structural integrity, symbol/reference resolution, units/roles, source fidelity, applicability, then reference reproduction where executable. Separate deterministic validation from agent judgment and scientific empirical evidence.
6. Review/publish a version for a declared use/profile. Keep incomplete candidates discoverable as candidates, not silently eligible. Preserve alternatives and disagreements.
7. Query-time agents select/compose eligible versions; new gaps feed a separate backlog. A query does not normally wait for steps 1–6.

A schema can require that an unknown field be explicitly tagged, not require that an agent invent a value. Catalog validation and execution eligibility are different profiles. Offline work allows more time for semantic review and cross-checks, but does not itself guarantee accuracy or independence of multiple agents.

## 11. Canonicalization: what it can and cannot mean

Distinguish:

- **Serialization normalization:** deterministic ordering/encoding, numeric lexical policy, schema version, hash rules. Useful for integrity/diffs, not semantics.
- **Syntactic/structural normalization:** resolve local references, alpha-renaming where scope-safe, normalize supported operator notation. Preserve source map.
- **Unit normalization:** convert using a validated scale/type rule, retain source values and conversion lineage. Not all units/concepts should be forced into one SI-like scalar.
- **Semantic alignment:** assert qualified concept/context mappings with evidence/review. Not automatic identity because normalized names coincide.
- **Mathematical transformation:** algebraic simplification/causalization subject to domains and numeric semantics. E.g. `x/x -> 1` requires `x != 0`; floating-point reassociation can change results. Original and transformed definitions/implementations remain traceable.

The goal is **consistent inspectable contracts and explicit transformations**, not one unique normal form for all models. Exact symbolic equality, mathematical equivalence under assumptions, observational similarity, executable equality within tolerance, and empirical adequacy are distinct claims.

## 12. Storage, serialization, extension, and safety tradeoffs

### Logical model does not select a database

- Versioned documents/files: easy audit, portability, Git diffs; harder concurrent atomic cross-record updates and large-scale queries.
- Relational storage with structured fields/JSON: references/transactions/indexes; migrations and graph traversal design still needed. A graph-shaped domain does not disqualify relational storage.
- Graph-oriented store: flexible typed relations/query paths; model numeric payloads/versioned transactional boundaries still need design.
- Binary array/object artifacts: keep bulk values out of metadata, but require reference integrity, formats/codecs and lifecycle management.

For a local single-operator trial, evaluate versioned structured documents with a rebuildable catalog/index before selecting infrastructure. This is a provisional storage approach, not a hosted database/service recommendation. Do not maintain unsynchronized canonical copies in JSON, SQL, and RDF; choose one source of truth and documented projections.

### Extension policy

Use explicit schema and **capability/profile versions**. Namespaced extensions may be retained, but unknown required semantics must prevent execution/approval. A reader can preserve an unsupported payload without claiming to understand it. A generic `metadata` bag is not a substitute for required semantics. Define migration and review invalidation rather than allowing silent upgrades of old runs.

### Safety

Never let the source paper, model payload, schema reference, remote context, or archive instruct an agent to override permissions. Avoid eval-based parsing of untrusted text. Bound expression depth/size and computational cost even for pure formulas. Control schema/context/import resolution, XML entities, ZIP paths/expanded size, array codecs/external references, and native backend execution. Structural JSON is not automatically safe, and a scientific standard is not a sandbox.

## 13. Decisions recommended, alternatives retained, evidence still needed

### Recommend now (provisional, no user preference needed to establish technical facts)

- Separate concepts/specifications, local declarations, values, definitions/revisions, implementations, bindings/instances, experiments/runs and evidence claims.
- Shared envelope and semantic/value contracts with explicitly supported mathematical payloads, not a universal expression or global variable slot.
- Common stable semantic references where useful plus original symbols/local definitions and scoped mappings.
- Strict unknown/incompatible/adapter/direct outcomes and explicit contextual transformations; no embedding-certified equivalence.
- Offline curation publishes qualified reusable versions; answering consumes them. First implementation should not depend on inline curation.
- A first executable algebraic profile with structural allowlisting and deterministic validators, versioned manifests, origin/unknown uncertainty, and explicit unsupported-formalism behavior.

### Not selected by this investigation

Exact schema field names; graph database; application language; unit library; JSON Schema validator; complete operator grammar; full ontology; runtime engine; first domain; full uncertainty format; native model import/export coverage. Standards are evaluated, not dependencies installed.

### User/product choices that remain separate

- Anchor problem and milestone/resources still constrain the executable profile. They do not require the user to choose a low-level AST or unit engine from guesswork.
- Whether inline curation is forbidden permanently or last-resort-only remains open. Recommend disabled for the first build, without treating that as final user agreement.
- Risk tolerance/review authority for consequential use and acceptable catalog/UI breadth remain policy decisions informed by domain evidence.

### Falsification and validation trials — proposed, not performed

| Trial | Evidence required | Recommendation changes if… |
| --- | --- | --- |
| Source fidelity: offline extract 2–3 small models from actual accessible papers/textbooks | Exact source map; independent review of declarations/constants/units/assumptions and supported operators | Core distinctions cannot preserve source meaning without a huge unstructured escape hatch |
| Algebra profile: nested DuPont or other selected supported composition | Independent numeric references/tolerances; input/domain/shape failures; no registry bypass | Tiny expression profile is cumbersome or loses required mathematics versus a restricted existing format |
| Meaning/type cases: energy/torque, temperature point/delta, finance stock/flow/conventions, same-shape wrong axes | Direct/adapter/review/rejection results agreed before implementation | Mandatory facets fail to distinguish practical incompatible inputs or block ordinary valid bindings |
| Native richer model roundtrip: one CellML/SBML or Modelica example if licensing/access permits | Preserve local declarations/math/units/source; report unsupported native semantics; no fake executable claim | Envelope cannot faithfully describe an important existing native format without distorting it |
| Definition versus solver task: implicit equations/ODE, probabilistic, optimization fixtures | Honest representation and explicit unsupported-operation response in first executor | Discriminated payload boundary cannot express required model kind/capabilities |
| Lineage: repeated model instances, independent scenarios, revised source/data, provisional input replaced later | Old run intact; new versions and instances unambiguously pinned; review not inherited silently | Local identity/context binding is fragile or version manifests cannot reproduce selected cases |
| Uncertainty/dependence and missingness | Shared `x - x` sample lineage; parameterization mismatch; null/NaN/unknown origin distinctions | Proposed value contract encourages independent-draw or false-confidence errors |
| Security parser/adapter trial | Resource limits; no eval, unauthorized resolution/download or arbitrary execution | Selected representation/tool cannot be bounded safely in the intended host |

First three plus lineage are natural prerequisites for calling a bounded v0 contract ready; broader adapters only become build requirements if the chosen workflow needs them. Do not demand successful execution of every mathematical formalism before a first algebraic build. No latency/token/accuracy improvement or curation scalability is claimed without measurements.

## 14. Corrections and unresolved limits

- Formula **strings are not inherently incapable** of ODE/implicit math/AD; a specified grammar/parser plus model/solver semantics can express them. Arbitrary raw strings alone do not establish safe interpretable contracts.
- Math.js has matrices and a documented symbolic derivative API. Retiring the 2025 sole-engine architecture remains sensible given heterogeneous models, semantics and execution needs; it must not rest on categorical false capability claims.
- Domain ontologies have useful precedents; maintenance/governance/mapping cost is a tradeoff, not evidence that all large ontologies are brittle or unusable.
- Sample ensembles are not universally composable through arbitrary models: joint dependence, validity, state, discontinuities, unsupported operations and cost can defeat naive propagation.
- Only specified versions/primary pages were reviewed. MathML 4 and some uncertainty-source access failed; detailed SBML constructs were checked against L3V1 text, not fully against L3V2. Current ProbOnto maintenance and UncertML contents/status remain unverified. No newest-release comparison was needed or claimed.
- A complete ontology, universal equivalence checker, automatic causal inference, and full semantic interoperability are not established by this investigation. Needed scientific/methodological evidence cannot be replaced by structural validation.

## 15. Durable result and next move

The reusable recommendation is summarized in [[concept-layered-model-representation]]. Existing representation, unit, semantics, time/space, uncertainty, topology, registry and compatibility-hypothesis records retain their canonical ownership and link this investigation. They remain open because a desk investigation does not choose/validate an executable v0 schema.

**Next useful work:** review the recommended distinctions, then specify and hand-check a narrow v0 profile against actual source models and adversarial compatibility cases. That work should produce a scoped decision and trial evidence, not silently turn this recommendation into an accepted universal architecture.
