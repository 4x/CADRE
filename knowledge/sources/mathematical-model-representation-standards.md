---
id: source-mathematical-model-representation-standards
type: source
title: Mathematical Model Languages and Execution Interfaces — Research Evidence
summary: Primary-source evidence on MathML, OpenMath, CellML, SBML, Modelica, FMI, BMI, symbolic expressions, statistical/optimization programs, and compiler/workflow boundaries; not an interoperability test.
status: active
created: '2026-10-28'
updated: '2026-10-28'
topics:
  - representation
  - architecture
  - interoperability
confidence: medium
relations:
  - type: supports
    target: investigation-model-variable-quantity-representation
---

# Mathematical Model Languages and Execution Interfaces — Research Evidence

## Provenance and scope

Primary specifications and official documentation read on 2026-10-28 by research agents for [[investigation-model-variable-quantity-representation]]. CellML was additionally inspected directly. This is a curated evidence digest, not a complete copy of each specification or verified interoperability. Version numbers below identify the evidence read, **not a claim to have selected or surveyed the newest release**. Unversioned/live documentation must be pinned before implementation. No dependency was installed and no parser, simulator, or adapter was exercised.

## Mathematical expressions versus notation

### MathML

- [MathML 3.0, second edition: Presentation](https://www.w3.org/TR/MathML/chapter3.html) describes layout/notation structures; [Content MathML](https://www.w3.org/TR/MathML/chapter4.html) represents mathematical expression structure and operators. Presentation is not uniquely invertible into mathematical meaning.
- Content MathML is an expression language, not by itself a complete source/evidence, parameter, initialization, simulation, and solver contract.
- MathML 4 retrieval failed during the research; no claims here depend on its current status or contents.

### OpenMath

- [OpenMath 2.0 revision 2, July 2019](https://openmath.org/standard/om20-2019-07-01/omstd20.html) represents mathematical objects, including application and binding structures. Symbol identity includes content dictionary and symbol name, with a base URI where applicable.
- Content dictionaries supply symbol semantics. The standard does not prescribe evaluation/simplification or a general model execution mechanism.
- Implication: semantic operator identifiers are useful; referencing a dictionary is not an executable implementation or proof of scientific adequacy.

### Symbolic libraries and safety

- [SymPy parsing documentation](https://docs.sympy.org/latest/modules/parsing.html) and [core documentation](https://docs.sympy.org/latest/modules/core.html), read as 1.14.0 documentation, describe symbolic expression structures and evaluation behavior. `parse_expr` and `sympify` carry explicit warnings about `eval` and unsanitized inputs. `evaluate=False` affects normalization/order; structural equality is not general mathematical equivalence.
- [Math.js function reference](https://mathjs.org/docs/reference/functions.html), [expression syntax](https://mathjs.org/docs/expressions/syntax.html), and [derivative](https://mathjs.org/docs/reference/functions/derivative.html) establish matrix operations and symbolic differentiation of supported expressions. They do not establish a universal CAS, general symbolic matrix calculus, or a complete heterogeneous simulation framework.
- Correction to earlier project prose: limitations observed in the 2025 prototype are not proof that Math.js lacks matrices or any symbolic differentiation. An expression string can encode rich mathematics if an appropriate language/parser exists; the issue is specified semantics, validation, safety, and execution support, not strings as a storage medium.

## Domain model languages

### CellML 2.0

- [Official specification entry](https://www.cellml.org/specifications/cellml_2.0) and [normative-text HTML rendering](https://www.cellml.org/cellml/2.0) describe components, units, variables, imports, variable mappings, encapsulation, MathML mathematics, and resets. Variables and numeric constants in supported mathematics have unit requirements.
- The HTML rendering says it is not the official normative artifact and links the official PDF; this review used that rendering and the official entry, not a complete PDF conformance analysis.
- A model is not a simulation experiment/solver selection. [CellML simulation metadata](https://www.cellml.org/specifications/metadata/simulations) points toward separate SED-ML work.
- Useful precedent for reusable components, explicit local variables, mathematical semantics, and units; importing a biological modeling standard wholesale would still require cross-domain context/evidence extensions.

### SBML

- [Specifications overview](https://sbml.org/documents/specifications/) and [Level 3 Version 2 page](https://sbml.org/documents/specifications/level-3/version-2/) identify Core and optional packages; the latter lists Level 3 Version 2 Core Release 2.
- Detailed constructs were read in the [Level 3 Version 1 Core specification text](https://pmc.ncbi.nlm.nih.gov/articles/PMC5451324/): species, compartments, parameters, rules, reactions, initial assignments, constraints, and events. Parameter scope can be global or reaction-local. Do not treat this as a full L3V2 semantic verification.
- [Hierarchical Model Composition package](https://sbml.org/documents/specifications/level-3/version-1/comp/) separately describes composing models/fragments; the page lists Version 1 Release 1, 2013.
- The specification overview warns that a schema captures syntax, not all semantic conformance. Domain constructs are useful precedents, not neutral names for every finance/engineering quantity.

### Modelica 3.6

- [Equations](https://specification.modelica.org/maint/3.6/equations.html) are constraints, not ordered assignments. Initial equations, conditions, and `when` equations affect semantics.
- [Connectors/connections](https://specification.modelica.org/maint/3.6/connectors-and-connections.html) generate equations; connection is not always output-to-input copying.
- [Declarations](https://specification.modelica.org/maint/3.6/class-predefined-types-and-declarations.html) distinguish constants, parameters, ordinary variables, and visibility. Parameters are constant during a simulation, not necessarily the same in every experiment.
- [Annotations](https://specification.modelica.org/maint/3.6/annotations.html) and the full language contain more than expression trees. Solver-generated causal order is distinct from the acausal source formulation.
- Counterexample to a universal DAG: simultaneous constraints and dynamic state require mathematical/initialization semantics, even if a compiler eventually emits ordered code.

## Exchange interfaces rather than universal source models

### FMI 3.0

- [FMI 3.0 specification](https://fmi-standard.org/docs/3.0/), dated 2022-05-10 in the source read: an FMU packages XML metadata, binary/source implementation, and resources with a C interface.
- Model Exchange leaves numerical integration to the importer; Co-Simulation generally carries its own solver; Scheduled Execution exposes partitions to an external scheduler.
- Exposed variables include type/units and causality/variability metadata. This is not necessarily all internal source mathematics. ME exposes an ODE state-space interface, not arbitrary DAEs directly, though an FMU may internally solve algebraic systems.
- Best read as a future simulation-adapter boundary, not as a scientific knowledge/provenance schema or automatic safe execution guarantee.

### CSDMS BMI 2.0

- [Specification](https://bmi-spec.readthedocs.io/en/latest/bmi.spec.html), [control functions](https://bmi.csdms.io/en/stable/bmi.control_funcs.html), [variable functions](https://bmi.csdms.io/en/stable/bmi.var_funcs.html), [grid functions](https://bmi.csdms.io/en/stable/bmi.grid_funcs.html), and [time functions](https://bmi.csdms.io/en/stable/bmi.time_funcs.html) define initialize/update/finalize and exchange metadata: names, types, units, sizes, grids, locations, values, and model time.
- [Best practices](https://bmi.csdms.io/en/stable/bmi.best_practices.html) map external Standard Names to internal symbols rather than requiring source renaming.
- [CSDMS Standard Names](https://csdms.colorado.edu/wiki/CSDMS_Standard_Names), listing version 0.8.3, use object/quantity names. [Naming motivation](https://csdms.colorado.edu/wiki/CSN_Motivation) and [coupling metadata](https://csdms.colorado.edu/wiki/CSN_Metadata_Names) place assumptions and other qualifiers outside names themselves.
- BMI is not a universal equation, validity, evidence, or coupling-appropriateness representation.

## Statistical and optimization formalisms

### Stan

- [Program blocks](https://mc-stan.org/docs/reference-manual/blocks.html), [statements](https://mc-stan.org/docs/reference-manual/statements.html), [types](https://mc-stan.org/docs/reference-manual/types.html), and [normal distribution](https://mc-stan.org/docs/functions-reference/unbounded_continuous_distributions.html), current unversioned reference pages read during the investigation.
- Data, parameters, transformed parameters, model, and generated quantities have distinct roles. A distribution statement contributes to log density, not necessarily a random draw. Observed data may occur in a likelihood; latent unknowns are different from observed data.
- Distribution family alone is insufficient: normal scale is standard deviation, not variance or precision. Parameterization and latent/observed roles must survive translation.
- No exact Stan release was verified. A representation should not reduce a statistical program to arbitrary assignments plus an unlabeled distribution name.

### Pyomo

- [Variables](https://pyomo.readthedocs.io/en/stable/explanation/modeling/math_programming/variables.html), [constraints](https://pyomo.readthedocs.io/en/stable/explanation/modeling/math_programming/constraints.html), and [objectives](https://pyomo.readthedocs.io/en/stable/explanation/modeling/math_programming/objectives.html), read as 6.10.1 documentation.
- Decision variables have domains/bounds and indexing; constraints and minimization/maximization objectives are distinct model constructs. A solver assigns variable values. An expression DAG alone omits the optimization task semantics.

## Compiler and workflow boundaries

- [ONNX IR](https://onnx.ai/onnx/repo-docs/IR.html), read as 1.24.0 documentation: typed operator graphs useful for portable computation/inference; training semantics are stateful. Not a source-paper semantic quantity or cross-domain provenance standard.
- [MLIR language reference](https://mlir.llvm.org/docs/LangRef/): extensible operations, values, blocks, regions, and dialects. A compiler framework is not a ready-made universal model ontology.
- [CWL Workflow 1.2](https://www.commonwl.org/v1.2/Workflow.html) and [CommandLineTool 1.2](https://www.commonwl.org/v1.2/CommandLineTool.html): portable tool/workflow descriptions, not governing scientific equations or a sufficient actual-run provenance record.

## Evidence boundary

This source supports distinguishing math expression, mathematical model, semantic annotation, execution interface, compiler IR, workflow, and experiment/run. It does not empirically establish the cost, adoption, fidelity, security, or performance of a Connected Models adapter. Specific import/export subsets must be tested before promising interoperability.
