---
id: decision-representation-contract-v0
type: decision
title: First Representation Contract — v0 Review Draft
summary: "Provisional cm-repr/0.1 draft with an appended critical review: retain layered identity/provenance boundaries, but revise single-context semantics, meaning-unit constraints, vocabulary evolution and candidate handling; simplify staged implementation before acceptance. No runtime exists."
status: provisional
created: '2026-10-28'
updated: '2026-10-28'
topics:
  - representation
  - architecture
  - lifecycle
confidence: medium
relations:
  - type: derived-from
    target: concept-layered-model-representation
  - type: derived-from
    target: investigation-model-variable-quantity-representation
  - type: relates-to
    target: note-mvp-build-sequence-and-extension-triggers
  - type: addresses
    target: question-model-node-ast-and-schema-representation
  - type: addresses
    target: question-registry-storage-and-versioning
  - type: addresses
    target: question-dimensional-and-unit-type-system
  - type: addresses
    target: question-semantic-variable-disambiguation
  - type: relates-to
    target: question-curation-evidence-and-approval
  - type: relates-to
    target: question-first-build-scope-and-success
  - type: relates-to
    target: question-evaluation-and-reference-evidence
---

# First Representation Contract — v0 Review Draft

## 1. Status, purpose, and boundary

**Proposed contract: `cm-repr/0.1`, executable profile `scalar-algebra/0.1`.** The normative wording below describes what an implementation would have to do **if this draft is accepted**; it is not evidence of approval or implementation. This record owns the concrete v0 shapes and rules; [[concept-layered-model-representation]] owns the broader concept, and [[note-mvp-build-sequence-and-extension-triggers]] owns delivery sequencing. Application language, storage engine, unit library, validator and Meta access remain unselected.

This is the smallest reviewable contract intended to support: fixture catalog → deterministic graph execution and saved run → real offline source extraction/review/publication → query-time composition → inspector and substitution. One local application, one numerical evaluator, one persistence backend. The six logical record kinds below need not be six tables, services, or files.

### Preflight and scope choices

- **Known:** offline dedicated agent curation; query-time consumption; model-first resolution; source/evidence, meaning and unit checks; pinned lineage. These stay intact.
- **Retired/paused:** old sole-engine browser/RPC architecture and social features. No new distributed/plugin framework or graph database is implied.
- **Unresolved:** first anchor, milestone/resources, API feasibility, and permanent ban versus last-resort inline curation. This draft disables inline curation for v0; it does not decide the permanent policy.
- **Possibly stale:** broad historic compilation/caching claims and old plan details are not requirements to reproduce those mechanisms. The MVP note explicitly permits full recompilation/recomputation; no performance measurements justify a cache yet.
- **Delta:** choose concrete fields, supported semantics, failure outcomes and an internally complete fixture. No fresh standards survey or product implementation is needed for this step.

### Proposed executable subset

Finite binary64 real **scalars**, explicit algebra, model-local symbols, exact semantic-spec matching, pinned linear ratio-unit conversions, and a finite acyclic graph of model instances. Every instance executes at most once per run. Scenario comparison means separate runs/compositions; arrays, loops and statistical propagation are not required to compare scalar results.

Scalar-only deliberately narrows the earlier optional short-array suggestion. If the selected anchor needs dated arrays, add and review that extension before its implementation; never flatten arrays into unlabeled scalars silently. A physical quantity at an instant or over a declared interval can still have a scalar value; that does not imply an array engine.

## 2. General serialization and identity rules

- JSON is the interchange form. YAML examples outside the JSON fixture are explanatory only. Implementation may store the records in documents or relational rows without changing their meaning.
- Every record has `schema: "cm-repr/0.1"`, `kind`, and `id`. Every versioned reusable record additionally has `revision`, a nonempty opaque string. `Ref = {id: string, revision: string}`. References never resolve `latest` during compilation/execution.
- Versioned kinds are `vocabulary`, `model`, `value`, and `composition`. `review` and `run` use globally unique event IDs and are append-only. Revision uniqueness is enforced on `(kind,id,revision)`; a different payload at an existing revision is rejected. Local symbol/node names are unique only inside their owning revision.
- JSON object key order has no semantic meaning; expression `args` order **does**. Reject duplicate JSON keys, unknown core fields, dangling references and unsupported schema/profile versions. An optional `annotations` object may hold inert namespaced display metadata; no executable or eligibility-relevant rule may be hidden there.
- Meaning/unit references inside a model/value are local keys in its pinned vocabulary. The complete identity is `(vocabulary Ref, key)`, not the key spelling. A v0 graph uses one vocabulary revision; semantic crosswalks between revisions/vocabularies are deferred.
- Decimal scalar magnitudes/literals are strings matching `^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$`. No NaN/Infinity/null/coercion. This lexical rule applies to source values and constants, not to arbitrary IDs. Computed magnitudes use the shortest decimal string that round-trips to the evaluated binary64 value, with zero serialized as `"0"`. Preserve the source string; convert once with round-to-nearest, ties-to-even into binary64, rejecting overflow and nonzero input that underflows to zero. Arithmetic overflow/nonfinite results and division by either signed zero fail. Each primitive arithmetic step rounds to binary64; no fused multiply-add or extended-precision reassociation is implied. Normalize computed zero to positive zero. This is not exact decimal accounting.
- Require retained immutable record contents, not merely a URL/hash. A future digest is over explicitly identified bytes/encoding; this draft does not invent a semantic hash or require canonical JSON hashing. Run event uniqueness does not imply deterministic IDs.
- Source `locator`s and external vocabulary links are citations, not permission to fetch/execute. Compilation/execution use only resolved local records. No remote schema/context/import resolution is required.

Notation below: `?` means optional; `[]` means list; maps are keyed by stable local strings. Shapes are closed: fields listed as required are required unless a variant says otherwise. There is no implied default numeric input, unit, context, approval, or uncertainty.

## 3. Six record kinds

### 3.1 Vocabulary: small, local, versioned meanings and units

```text
Vocabulary = {schema, kind:"vocabulary", id, revision,
  meanings: {key: Meaning}, units: {key: Unit}}
Meaning = {definition: string, entity_kind: string,
  temporal_basis: "static"|"instant"|"interval",
  qualifiers: {key: string}, external_refs: string[]}
Unit = {definition: string, dimension: {base: integer},
  scale: decimal-string, external_refs: string[]}
```

`dimension` has only nonzero integer exponents; `{}` is dimensionless. `scale > 0` converts to a local coherent reference scale for that dimension; its interpretation and base names must be fixed in the vocabulary definitions. v0 has ratio units only. Every vocabulary MUST contain unit key `one` with dimension `{}` and scale `"1"`. A model's used vocabulary must be human-reviewed as part of its review target (§3.5); units and meanings are not accepted because an agent typed them.

Meanings include applicable method/accounting convention, sign/orientation, currency/price basis, stock/flow/aggregation and other distinctions in `qualifiers`; the bounded domain must define which keys are required **before analyst-use approval**. Required meaning is not inferred from dimensions. Omitting a required qualifier blocks approval. Unknown meanings/units may remain in a source-only candidate, but cannot execute. Free strings define local controlled terms; exact key/value comparison is conservative and does not assert universal ontology coverage. Source-facing labels/notation remain in model symbols.

Different meaning keys are not direct-compatible even if their definition text/units look similar. No vector search, ontology reasoner, QUDT-to-UCUM engine, dynamic FX conversion or external service is needed in v0. External references preserve alignment possibilities without claiming a verified crosswalk.

### 3.2 Model: reusable definition plus embedded implementation artifact

```text
Model = {schema, kind:"model", id, revision, title, vocabulary:Ref,
  sources: SourceFragment[], authorship: Authorship,
  assumptions: string[], applicability: string, limitations: string[],
  symbols: {local-name: Symbol}, implementation: Implementation}
SourceFragment = {id:string, locator:string, version:string, location:string,
  excerpt:string, license_note:string, origin:"external"|"fixture"}
Authorship = {mode:"manual-fixture"|"offline-agent"|"manual-source",
  actor:string, at:UTC-timestamp,
  agent_model?:string, trace_locator?:string}
Symbol = {notation:string, definition:string,
  role:"input"|"parameter"|"constant"|"derived"|"output",
  meaning:string, unit:string, source_refs:string[], value?:decimal-string}
Implementation =
  {kind:"algebra-ir", version:"0.1",
   assignments:[{target:local-name, expr:Expr, source_refs:string[]}],
   predicates:[{id:string, expr:Predicate, source_refs:string[]}]} |
  {kind:"source-only", format:string, locator:string, reason:string}
```

`parameter` is an externally bound run-fixed scalar; `input` is an externally bound scalar, not a time-stepped signal. `constant` MUST have `value`; other roles MUST NOT. Constants retain meaning/unit/source information; literal algebraic numbers use §4. `derived` and `output` MUST each have exactly one assignment; `input`, `parameter`, and `constant` MUST have none. At least one output is required for algebra execution. Every symbol definition and implementation assignment/predicate has nonempty, resolvable local source-fragment references. Source map locations need not mean the source used our chosen direction of computation; document an extracted rearrangement in assumptions/limitations and review it.

For `offline-agent`, `agent_model` and `trace_locator` are required, identifying the actual model/access version as available and a retained extraction trace. Source records preserve exact document/equation/table and notation context, with license/access limitations, not just a generic paper URL. `manual-fixture` requires only fixture-origin fragments. Sources are evidence links; excerpts/locations and claims must be reviewed, not treated as true automatically.

Implementation is embedded to avoid a separate artifact/plugin registry: **the pinned model revision identifies its expression payload**, while the run records the evaluator build separately. A changed expression means a new revision. Multiple implementations, executable downloads, arbitrary code and external solver artifacts are deferred. A source-only record can retain any formalism but is never executable/approvable for this profile. Unsupported local declarations can remain in excerpts/native artifacts instead of pretending to encode them as scalar roles.

### 3.3 Value: contextual scalar assertion, not a global variable slot

```text
Value = {schema, kind:"value", id, revision, vocabulary:Ref,
  meaning:string, unit:string, context:Context,
  magnitude:decimal-string, origin:Origin,
  uncertainty:{kind:"unknown", reason:string}}
Context = {entity:string, entity_kind:string, scenario:string, support:Support}
Support = {kind:"static", reason:string} |
          {kind:"instant", at:UTC-timestamp} |
          {kind:"interval", start:UTC-timestamp, end:UTC-timestamp}
Origin = {kind:"fixture"|"observation"|"model-output"|"user-scenario"|"meta-estimate",
  actor:string, at:UTC-timestamp, evidence:string[],
  run_id?:string, output?:string,
  agent_model?:string, trace_locator?:string, reason?:string}
```

All UTC timestamps use `YYYY-MM-DDTHH:mm:ss[.fraction]Z`, valid Gregorian dates, no leap seconds; intervals are half-open `[start,end)` with start < end. Support kind must match meaning temporal basis; entity_kind must match the meaning. `entity` and `scenario` are explicit opaque IDs, not labels inferred from prose. The complete context must equal the consuming instance context in v0. Static does not mean unknown time; it means declared non-temporal support. Unknown time/entity/method cannot be disguised as static or "not applicable" to make a binding pass.

`meta-estimate` requires `agent_model`, `trace_locator`, and `reason`; `model-output` requires `run_id` and `output` (a graph output key). An observation requires nonempty evidence identifying source version, exact location and the information's publication/availability vintage; fixture/user-scenario can have `evidence:[]`. `origin.at` is assertion creation time, not necessarily observation/publication time. Historical as-of decision queries are unsupported in v0 unless a later explicit profile can enforce availability cutoffs; do not claim leakage-free backtesting from this metadata alone. Model-output evidence is its producing retained successful run/lineage. Meta evidence may be empty but must say why in `reason`. None of these fields constitutes calibrated uncertainty.

For `model-output`, validate that the referenced successful run output matches magnitude (by binary64 roundtrip), vocabulary, meaning, unit and context exactly; do not accept arbitrary pasted numbers with a run ID. Preserve transitive fixture and meta-estimate origin from that run, including the original estimate revisions, when importing its result. A computed value cannot launder synthetic/generated input into an observation or clear its disclosure/authorization requirements. Cyclic provenance is rejected. The first implementation may instead reject imported prior-run values and use within-composition edges until it implements these checks; that supported restriction must be explicit.

Only unknown uncertainty executes in v0; this explicitly means **no probability/interval propagation**, not zero uncertainty. New uncertainty types require an explicit profile extension. A run-specific Meta input estimate may be used only when §3.4 authorizes it. It does not curate a model or change its definition; invented equations/relationships remain prohibited during answering.

### 3.4 Composition: explicit instances/bindings and requested outputs

```text
Composition = {schema, kind:"composition", id, revision, vocabulary:Ref,
  purpose:"fixture"|"analyst", review_ids:string[],
  allow_meta_estimates:boolean, nodes:{node-id:Node},
  outputs:{output-key:{node:string, symbol:string}}}
Node = {model:Ref, context:Context, bindings:{input-or-parameter:Binding}}
Binding = {value:Ref} | {node:string, symbol:string}
```

All model/value vocabulary revisions must equal the composition's. Every required input/parameter has exactly one binding, including unused declared inputs (unused declarations should normally be cleaned up in review). Constants cannot be rebound. An edge references only an `output` symbol on another node. Nodes of the same model have independent local slots and contexts. No value is found implicitly by semantic identity. All nodes participate in at least one requested-output ancestry; reject dead nodes so irrelevant failures/cost cannot hide in the graph. Nonempty nodes/outputs, no cycles and no recursive composite-model payloads in v0. Reuse means new model instances or another composition, not bespoke evaluator code.

`purpose:"fixture"` permits fixture-only reviews and values and MUST be labeled synthetic in results. `purpose:"analyst"` rejects manual-fixture models, any fixture-origin model sources, and values with direct or transitive fixture origin, and requires eligible analyst-use reviews. Setting purpose to fixture cannot produce an analyst-use claim. A composition author cannot grant model approval by listing a review ID (§3.5).

`allow_meta_estimates` is mandatory; a UI may initialize it to false but omission is invalid. When meta estimates occur directly or transitively, it MUST be true and an eligible review event must approve this exact composition revision and the specific original meta-estimate value revisions. Merely setting true without any estimates does not require a composition review. Until authorized, return an unresolved planning diagnostic, not an evaluated number. Unknown/private/indefensible missing facts stay unresolved; permission to estimate does not justify fabricating evidence. This scalar permission does not allow query-time model creation/publication. A change to bindings/context/policy means a new composition revision and renewed authorization where needed.

### 3.5 Review: append-only human authority, scoped to exact versions/use

```text
Review = {schema, kind:"review", id,
  target:{kind:"model"|"composition", ref:Ref},
  vocabulary:Ref, use:"fixture"|"analyst",
  decision:"approve"|"reject"|"withdraw", supersedes:string|null,
  reviewer:string, at:UTC-timestamp, rationale:string,
  checks:[{name:string, outcome:"passed"|"failed"|"blocked"|"untested",
           evidence:string[]}],
  authorized_values:Ref[]}
```

The single project owner is the initial authority; a locally configured reviewer identity is validated by the application, **not trusted because a JSON record says `reviewer:"owner"`**. Query-time agents cannot write authoritative reviews. A source extraction agent cannot self-approve. Every review binds the model's/composition's vocabulary revision as well as its exact target; source, semantic/unit or implementation edits require new targets/review. `authorized_values` is empty for model reviews; a composition review uses it only for the exact permitted meta values. This is local authority, not public-key signing or multi-user RBAC.

For model approval require recorded `passed` checks with evidence for `structure`, `source-fidelity`, `meaning-units`, `reference-cases`, and `declared-use`. Empirical validation is separately recorded as `empirical-adequacy` with its actual outcome; `untested` is allowed only with stated limitations and a non-production declared use. Arithmetic/source reproduction is not empirical validation. Exact domain reference tolerances/oracles must be set before analyst-use approval, not invented by the agent/runtime. A fixture-only review checks synthetic internal consistency and must not masquerade as scientific source fidelity.

For composition approval require `passed` `structure`, `binding-compatibility`, and `declared-use`; meta authorization additionally requires `passed` `provisional-input-policy` citing every authorized value and why estimation is defensible. Meta authorization is not calibrated truth. These checks do not replace compiler/runtime validation.

Review check names are unique; approval must include all required checks above, and any failed/blocked applicable required check precludes approval. `reject`/`withdraw` retain honest check outcomes but need not claim those approval checks passed. The fixture bundle's expected approval records are explanatory only and MUST NOT be bulk-imported as authoritative approval merely because their fields are well-formed; the local owner must admit them through the actual review operation.

First review for a `(target,use)` has `supersedes:null`; later reviews cite the latest event and form a linear chain. Persist with compare-and-append; stale/conflicting heads block eligibility until owner reconciliation, never last-write-wins. `withdraw`/`reject` makes that target/use ineligible. Compilation resolves current heads from authoritative local review history, not only the IDs offered by a caller, and rechecks immediately before execution. Runs retain the exact heads used; later withdrawal prevents new runs but does not edit old evidence/results. No distributed synchronization is required.

### 3.6 Run: actual evidence, separate from reusable composition

```text
Run = {schema, kind:"run", id, composition:Ref, vocabulary:Ref,
  purpose:"fixture"|"analyst", evaluator:{id:string, build:string,
    profile:"scalar-algebra/0.1", limits:Limits},
  resolved:{models:Ref[], values:Ref[], reviews:string[]},
  started_at:UTC-timestamp, ended_at:UTC-timestamp,
  status:"succeeded"|"failed"|"blocked"|"cancelled",
  plan:[node-id], conversions:Conversion[],
  node_results:{node-id:{output-symbol:decimal-string}},
  checks:[{stage:string, outcome:"passed"|"failed"|"blocked", detail:string}],
  outputs:{output-key:{magnitude:decimal-string, unit:string, meaning:string,
    context:Context, uncertainty:{kind:"unknown", reason:string},
    upstream_values:Ref[], meta_values:Ref[]}},
  diagnostics:Diagnostic[]}
Limits = {max_nodes:integer, max_expression_nodes:integer,
  max_expression_depth:integer, max_run_ms:integer}
Conversion = {at:string, from_unit:string, to_unit:string,
  input:decimal-string, output:decimal-string}
Diagnostic = {code:string, stage:string, path:string, message:string,
  related_refs:Ref[]}
```

Manifest references must resolve to retained immutable content, including embedded source/implementation and review evidence. Store diagnostic/artifact evidence locally or retain precise immutable locators; no claim of replay from disappearing web pages. `plan` is derived and may be saved, not trusted as a caller-provided execution schedule. `resolved` lists every unique model/value and authoritative review event actually used; the vocabulary is pinned separately. Output `upstream_values` is the transitive set of original bound value revisions affecting it; `meta_values` identifies the original meta-estimate value revisions affecting the result, expanded through retained prior-run provenance where supported. Predicate-dependent input values count as reliance even when they do not occur in the output's assignment expression. Constants/model/source lineage is available through the pinned models. Different outputs can have different reliance sets; do not disclose all graph estimates as if all outputs depend on them.

`node_results` stores declared output symbols only; intermediate slots can remain transient. Successful run outputs MUST correspond to the executed expressions and declared bindings. `succeeded` requires all nodes and requested outputs to complete with current eligibility and passed validation. Other statuses have `outputs:{}`; partial node results may be retained for diagnosis, never presented as a complete answer. `blocked` means unresolved/unsupported/unauthorized before numeric execution; `failed` means an arithmetic/domain/execution error after starting numeric work. A review withdrawal after numeric work starts produces `cancelled` with no final outputs, not `blocked`. Preflight-invalid values are blocked. Cancellation is not success. Missing-input planning may remain a draft proposal outside this strict composition shape; never persist an invalid composition as executable.

Record complete runs as immutable terminal events; a process crash may leave a separate local pending job marker, which is not a succeeded Run. End-to-end Meta usage/latency and attempt traces belong to the curation/planning activities and can be linked via origin trace/review evidence; this numeric Run does not falsely include offline curation in query-execution time. Before real inference, metering/budgets remain requirements of the first-build contract, not solved by this record.

## 4. Algebra and type rules — exact supported operations

```text
Expr = {var:local-name} | {num:decimal-string, unit:unit-key} |
       {op:"neg", args:[Expr]} |
       {op:"add"|"sub"|"mul"|"div", args:[Expr,Expr]} |
       {op:"pow-int", arg:Expr, exponent:integer}
Predicate = {op:"gt"|"ge"|"lt"|"le"|"eq"|"ne", args:[Expr,Expr]}
```

Only these tags/arity execute; no text evaluation, function lookup, arbitrary code, strings-as-expressions, implicit array broadcasting, general powers, roots, transcendental functions, loops, randomness or network calls. `pow-int` exponent is in [-8,8]; `0^0` and zero to a negative power fail; power uses left-associated repeated multiplication, followed by reciprocal for negative exponents. Exponent zero on nonzero finite input yields dimensionless one. No algebraic reassociation or simplification changes operation order.

Evaluate expression operands after conversion to coherent dimension scale: multiply magnitude by its unit scale in binary64. `add/sub` and comparisons require equal dimension vectors; multiplication adds exponent vectors; division subtracts them; negation preserves dimension; power multiplies exponents by its exponent. Numeric literals have declared units; no assumed dimensionless bare numbers. Expression dimensions must match their assignment target; divide the coherent result by the target unit scale for the stored output magnitude. Unit conversion records identify each changed-scale symbol/literal load and output store by node/expression path; identity scale operations need no conversion record. Underflow during arithmetic may produce binary64 subnormals/zero, recorded as such; input parse underflow-to-zero is rejected as above. No hidden quantization or per-operation decimal rounding.

Unit algebra validates **dimensions**, not the scientific meaning of a derived expression. Meaning/source-fidelity of `voltage * current -> power`, for example, is an attributable reviewed claim. A compiler must not infer an arbitrary output meaning just from dimension arithmetic. Boundary bindings (§5) check exact declared meaning/context.

Assignments may reference inputs/parameters/constants and earlier/later assigned symbols if the local dependency graph is acyclic; compile its topological order. Resolve ties by ascending local symbol ID; model-instance ties by ascending node ID. References are local, not graph-global. Predicates can reference only inputs/parameters/constants and are all evaluated before that model's assignments; this avoids uncomputed-output guards. A predicate arithmetic error is a domain failure, not a successful false/true default. Comparisons are exact binary64 comparisons; tolerance is used only for declared reference tests, never implicitly to make preconditions pass. Real-world applicability prose requires declared-use review and disclosure even when not executable as a predicate.

Proposed default ceilings for the small local trial: 128 graph nodes, 4096 total expression/predicate tree nodes across instances, depth 64, numeric string length 128 characters and exponent magnitude 308, 1 MiB per record, 5 seconds numeric run timeout. Node/tree/depth bounds and record/numeric size limits apply before evaluation; all configurable Limits fields must be positive integers. The numeric run limit is recorded in `Limits`; the fixed lexical/record limits are part of this profile. These are conservative engineering guardrails, **not measured performance targets**; raise them only as an explicit reviewed local configuration change and capture effective run limits/build. No automatic retry of failed math or missing data.

## 5. Binding, compilation, failure and revision rules

Compiler stages, in order:

1. Parse closed shapes and versions; resolve references locally; reject conflicting revisions and unsupported implementations. Check resource bounds.
2. Resolve authoritative review heads for purpose/use and the pinned vocabulary. A fixture graph must have fixture-use eligibility; an analyst graph needs analyst-use. Analyst-use approval may serve a fixture run only if the graph still declares fixture purpose; never the reverse. A composition itself needs owner review only to authorize meta inputs, not to hand-author every query graph.
3. Check local symbol/assignment/source references, role cardinalities, dimension rules, predicates, bound-input completeness, requested outputs, absence of dead nodes, local/graph cycles.
4. Validate that every used symbol meaning's entity_kind/temporal_basis agrees with its instance Context; then for each binding compare full semantic identity, entity kind, exact instance/value or producer/consumer context, and scalar profile. Mismatch is rejected even for equal dimensions. Unit keys may differ only with equal dimensions and approved ratio scales; conversion uses §4. Different scenario/entity/support cannot be silently aligned or used as causal evidence.
5. Check available value origins and policy: fixtures only in fixture purpose; known values only; direct/transitive meta estimates require exact composition/value authorization and direct/transitive fixture provenance remains fixture-only. No silent numerical defaults. Missing/unknown/out-of-policy values yield a blocked/unresolved diagnostic and optionally an offline coverage need.
6. Derive the deterministic execution plan, pin manifest contents, recheck review heads, then evaluate each instance once; evaluate its predicates before assignments and check every arithmetic/output result. Compose only through declared output bindings. Plan/registry changes during execution do not retarget references; an authoritative withdrawal observed before a new instance starts blocks a not-yet-started numeric run or cancels one already in progress, rather than claiming full success. Recheck again before publishing success.

Required diagnostic codes: `INVALID_RECORD`, `UNRESOLVED_REF`, `REVISION_CONFLICT`, `UNSUPPORTED_PROFILE`, `UNSUPPORTED_PAYLOAD`, `REVIEW_REQUIRED`, `INELIGIBLE`, `REVIEW_CONFLICT`, `MISSING_BINDING`, `SEMANTIC_MISMATCH`, `CONTEXT_MISMATCH`, `UNIT_MISMATCH`, `CYCLE`, `DEAD_NODE`, `ORIGIN_POLICY`, `META_AUTH_REQUIRED`, `PRECONDITION_FAILED`, `NUMERIC_DOMAIN`, `NONFINITE`, `RESOURCE_LIMIT`, `CANCELLED`. Every diagnostic has a stage, record/JSON-pointer-like path and actionable message; no catch-and-return-zero behavior. `PRECONDITION_FAILED` and numeric errors occur during numeric execution and fail the run; preflight errors block it.

**Recompile/recompute by default.** Changing any model/input/graph/vocabulary/authorization creates a new revision/event and new run. No cross-run caching, dirty timestamp propagation, selective recomputation, or compile-on-save trigger is required. Evaluate each node once within a run to avoid duplicate traversal. Original runs/manifests stay inspectable. Changing a source-only/native record does not make it executable or inherit review. Adding an operation/unit/semantic mapping changes the applicable payload/vocabulary/profile and requires affected review, not an untracked evaluator patch.

## 6. Complete synthetic fixture — two models, two compositions, independent instances

This is a self-contained **fixture bundle**, not a sourced electrical model, source-faithful agent extraction, or approved scientific evidence. The outer array is a packaging convenience, not a seventh record kind. All identities/authority are local fixtures. `owner` is assumed locally configured for the fixture exercise, not authenticated by this file. Evidence locators beginning `fixture:` are in-bundle references to source-fragment definitions, review checks or the hand oracle stated below; they are not network locations. The fixture's supplied reviews describe **expected approvals in a future fixture import exercise**, not checks an implementation has actually passed.

```json
[
  {
    "schema":"cm-repr/0.1","kind":"vocabulary","id":"fixture:electrical","revision":"1",
    "meanings":{
      "voltage":{"definition":"Potential difference across an idealized element","entity_kind":"element","temporal_basis":"instant","qualifiers":{"method":"synthetic-dc","orientation":"passive-sign"},"external_refs":[]},
      "resistance":{"definition":"Positive resistance of that element at the specified instant","entity_kind":"element","temporal_basis":"instant","qualifiers":{"method":"synthetic-dc","regime":"ohmic"},"external_refs":[]},
      "current":{"definition":"Current through that element","entity_kind":"element","temporal_basis":"instant","qualifiers":{"method":"synthetic-dc","orientation":"passive-sign"},"external_refs":[]},
      "power":{"definition":"Electrical power absorbed by that element","entity_kind":"element","temporal_basis":"instant","qualifiers":{"method":"synthetic-dc","orientation":"passive-sign"},"external_refs":[]}
    },
    "units":{
      "one":{"definition":"Dimensionless unity; L/M/T/I are metre/kilogram/second/ampere bases","dimension":{},"scale":"1","external_refs":[]},
      "V":{"definition":"Volt","dimension":{"L":2,"M":1,"T":-3,"I":-1},"scale":"1","external_refs":[]},
      "ohm":{"definition":"Ohm","dimension":{"L":2,"M":1,"T":-3,"I":-2},"scale":"1","external_refs":[]},
      "A":{"definition":"Ampere","dimension":{"I":1},"scale":"1","external_refs":[]},
      "W":{"definition":"Watt","dimension":{"L":2,"M":1,"T":-3},"scale":"1","external_refs":[]}
    }
  },
  {
    "schema":"cm-repr/0.1","kind":"model","id":"fixture:current","revision":"1","title":"Synthetic current relation",
    "vocabulary":{"id":"fixture:electrical","revision":"1"},
    "sources":[{"id":"s1","locator":"fixture:current","version":"1","location":"relation 1","excerpt":"I = V / R; R > 0","license_note":"Project-authored synthetic fixture; not external evidence","origin":"fixture"}],
    "authorship":{"mode":"manual-fixture","actor":"owner","at":"2026-10-28T00:00:00Z"},
    "assumptions":["Synthetic ohmic DC element; passive sign convention"],"applicability":"Fixture-only arithmetic exercise","limitations":["No empirical electrical validation"],
    "symbols":{
      "v":{"notation":"V","definition":"Element voltage","role":"input","meaning":"voltage","unit":"V","source_refs":["s1"]},
      "r":{"notation":"R","definition":"Element resistance","role":"parameter","meaning":"resistance","unit":"ohm","source_refs":["s1"]},
      "i":{"notation":"I","definition":"Element current","role":"output","meaning":"current","unit":"A","source_refs":["s1"]}
    },
    "implementation":{"kind":"algebra-ir","version":"0.1","assignments":[{"target":"i","expr":{"op":"div","args":[{"var":"v"},{"var":"r"}]},"source_refs":["s1"]}],"predicates":[{"id":"positive-resistance","expr":{"op":"gt","args":[{"var":"r"},{"num":"0","unit":"ohm"}]},"source_refs":["s1"]}]}
  },
  {
    "schema":"cm-repr/0.1","kind":"model","id":"fixture:power","revision":"1","title":"Synthetic absorbed power",
    "vocabulary":{"id":"fixture:electrical","revision":"1"},
    "sources":[{"id":"s1","locator":"fixture:power","version":"1","location":"relation 1","excerpt":"P = V * I","license_note":"Project-authored synthetic fixture; not external evidence","origin":"fixture"}],
    "authorship":{"mode":"manual-fixture","actor":"owner","at":"2026-10-28T00:00:00Z"},
    "assumptions":["Synthetic DC element; passive sign convention"],"applicability":"Fixture-only arithmetic exercise","limitations":["No empirical electrical validation"],
    "symbols":{
      "v":{"notation":"V","definition":"Element voltage","role":"input","meaning":"voltage","unit":"V","source_refs":["s1"]},
      "i":{"notation":"I","definition":"Element current","role":"input","meaning":"current","unit":"A","source_refs":["s1"]},
      "p":{"notation":"P","definition":"Absorbed electrical power","role":"output","meaning":"power","unit":"W","source_refs":["s1"]}
    },
    "implementation":{"kind":"algebra-ir","version":"0.1","assignments":[{"target":"p","expr":{"op":"mul","args":[{"var":"v"},{"var":"i"}]},"source_refs":["s1"]}],"predicates":[]}
  },
  {
    "schema":"cm-repr/0.1","kind":"value","id":"fixture:v12","revision":"1","vocabulary":{"id":"fixture:electrical","revision":"1"},"meaning":"voltage","unit":"V",
    "context":{"entity":"element-A","entity_kind":"element","scenario":"baseline","support":{"kind":"instant","at":"2026-10-28T00:00:00Z"}},"magnitude":"12",
    "origin":{"kind":"fixture","actor":"owner","at":"2026-10-28T00:00:00Z","evidence":[]},"uncertainty":{"kind":"unknown","reason":"Synthetic point input; no probability claim"}
  },
  {
    "schema":"cm-repr/0.1","kind":"value","id":"fixture:r6","revision":"1","vocabulary":{"id":"fixture:electrical","revision":"1"},"meaning":"resistance","unit":"ohm",
    "context":{"entity":"element-A","entity_kind":"element","scenario":"baseline","support":{"kind":"instant","at":"2026-10-28T00:00:00Z"}},"magnitude":"6",
    "origin":{"kind":"fixture","actor":"owner","at":"2026-10-28T00:00:00Z","evidence":[]},"uncertainty":{"kind":"unknown","reason":"Synthetic point input; no probability claim"}
  },
  {
    "schema":"cm-repr/0.1","kind":"review","id":"fixture:review-current","target":{"kind":"model","ref":{"id":"fixture:current","revision":"1"}},"vocabulary":{"id":"fixture:electrical","revision":"1"},"use":"fixture","decision":"approve","supersedes":null,"reviewer":"owner","at":"2026-10-28T00:00:00Z","rationale":"Expected fixture-only admission after future checker review; no scientific validation",
    "checks":[
      {"name":"structure","outcome":"passed","evidence":["fixture:current#s1"]},
      {"name":"source-fidelity","outcome":"passed","evidence":["fixture:current#s1"]},
      {"name":"meaning-units","outcome":"passed","evidence":["fixture:electrical@1"]},
      {"name":"reference-cases","outcome":"passed","evidence":["fixture:oracle-current-2A"]},
      {"name":"declared-use","outcome":"passed","evidence":["fixture:current#s1"]},
      {"name":"empirical-adequacy","outcome":"untested","evidence":[]}
    ],"authorized_values":[]
  },
  {
    "schema":"cm-repr/0.1","kind":"review","id":"fixture:review-power","target":{"kind":"model","ref":{"id":"fixture:power","revision":"1"}},"vocabulary":{"id":"fixture:electrical","revision":"1"},"use":"fixture","decision":"approve","supersedes":null,"reviewer":"owner","at":"2026-10-28T00:00:00Z","rationale":"Expected fixture-only admission after future checker review; no scientific validation",
    "checks":[
      {"name":"structure","outcome":"passed","evidence":["fixture:power#s1"]},
      {"name":"source-fidelity","outcome":"passed","evidence":["fixture:power#s1"]},
      {"name":"meaning-units","outcome":"passed","evidence":["fixture:electrical@1"]},
      {"name":"reference-cases","outcome":"passed","evidence":["fixture:oracle-power-24W"]},
      {"name":"declared-use","outcome":"passed","evidence":["fixture:power#s1"]},
      {"name":"empirical-adequacy","outcome":"untested","evidence":[]}
    ],"authorized_values":[]
  },
  {
    "schema":"cm-repr/0.1","kind":"composition","id":"fixture:power-chain","revision":"1","vocabulary":{"id":"fixture:electrical","revision":"1"},"purpose":"fixture","review_ids":["fixture:review-current","fixture:review-power"],"allow_meta_estimates":false,
    "nodes":{
      "c":{"model":{"id":"fixture:current","revision":"1"},"context":{"entity":"element-A","entity_kind":"element","scenario":"baseline","support":{"kind":"instant","at":"2026-10-28T00:00:00Z"}},"bindings":{"v":{"value":{"id":"fixture:v12","revision":"1"}},"r":{"value":{"id":"fixture:r6","revision":"1"}}}},
      "p":{"model":{"id":"fixture:power","revision":"1"},"context":{"entity":"element-A","entity_kind":"element","scenario":"baseline","support":{"kind":"instant","at":"2026-10-28T00:00:00Z"}},"bindings":{"v":{"value":{"id":"fixture:v12","revision":"1"}},"i":{"node":"c","symbol":"i"}}}
    },"outputs":{"absorbed-power":{"node":"p","symbol":"p"}}
  },
  {
    "schema":"cm-repr/0.1","kind":"composition","id":"fixture:current-only","revision":"1","vocabulary":{"id":"fixture:electrical","revision":"1"},"purpose":"fixture","review_ids":["fixture:review-current"],"allow_meta_estimates":false,
    "nodes":{"c2":{"model":{"id":"fixture:current","revision":"1"},"context":{"entity":"element-A","entity_kind":"element","scenario":"baseline","support":{"kind":"instant","at":"2026-10-28T00:00:00Z"}},"bindings":{"v":{"value":{"id":"fixture:v12","revision":"1"}},"r":{"value":{"id":"fixture:r6","revision":"1"}}}}},
    "outputs":{"current":{"node":"c2","symbol":"i"}}
  }
]
```

**Hand oracle (not generated execution output):** `fixture:oracle-current-2A` is 12 V / 6 ohm = 2 A; `fixture:oracle-power-24W` is 12 V × 2 A = 24 W. All are exactly representable binary64 values. Expected plans are `["c","p"]` and `["c2"]`. Both outputs depend on v12 and r6, no meta values, no changed-scale conversions. A real Run must be created by the future evaluator, with actual build/times/checks, **not copied from this expected trace**. A reference runner test must still compare to the hand oracle; this draft is not its pass record.

The fixture shows model reuse in a second composition. Independent-instance isolation additionally needs a trial that duplicates the current instance, binds different value/context revisions, and proves no shared mutable slots; the table below makes that a release check rather than falsely claiming this fixture exercised it.

## 7. Review matrix: required outcomes, not tests claimed passed

| Case | Required result | MVP stage |
| --- | --- | --- |
| Two compositions above | Future run: 24 W and 2 A; same current model revision; no executor special case | 2: deterministic skeleton |
| Add mV ratio unit to a **new** vocabulary, repin/review fixtures, bind 12000 mV | 24 W with explicit load conversion, not a changed semantic meaning | 2 |
| A known voltage Value bound to a current input; or same meaning with incompatible dimension units | `SEMANTIC_MISMATCH` at binding; separately wrong dimensions yield `UNIT_MISMATCH`. Deliberately relabeling an unverified source value cannot be detected from numeric magnitude alone and requires provenance/source review. | 2 |
| Same meaning/unit but wrong entity, scenario or instant/interval | `CONTEXT_MISMATCH`, no auto alignment | 2 |
| R = 0 or negative | `PRECONDITION_FAILED` before division; no numeric answer | 2 |
| Missing/duplicate binding, dangling ref, cycle, dead node, unknown op/version | Specific blocked diagnostic; no guessed/default input or fallback code | 2 |
| Source-only ODE or array/distribution/offset-temperature payload | Explicit unsupported/profile error, not scalar reinterpretation | 2 |
| Two instances with separate contexts/values, changed input/model revision | Independent results/new runs; original manifest unchanged | 2 and 5 |
| Vocabulary/source/expression edit or stale/withdrawn/conflicting review | New revision/review required; cannot retain approval by ID reuse | 2 and 3 |
| Actual offline Meta extraction from an accessible source | Same Model structure with source map, variables/constants, actual trace; owner-scoped approval after checks; later query uses saved revision | 3: real curation |
| Meta scalar estimate | Block until exact composition/value authorization; then disclosed transitive reliance; no automatic model publication | 4: query composition |
| Missing model/private or indefensible fact | Conditional/unresolved planning result and separate curation need; no inline model invention | 4 |
| Known fixture presented as analyst use, directly or through prior-run output; forged owner JSON | Rejected by transitive origin/review/authority boundary, not trusted declaration | 3–4 |
| Inspector/substitution | Render actual run/model/value/source/approval lineage; new run for changes | 5 |

Nontrivial numeric references use predeclared `abs(actual-expected) <= atol + rtol*abs(expected)` with unit and finite-value checks. Tolerances are case-specific and must not be loosened after failures without justified changed requirements. Fixture exact values can use `atol=0, rtol=0`. Tests for cancellation/resource limits and parse safety become required before the actual evaluator is used with untrusted agent payloads; no such evaluator exists in this documentation task.

## 8. MVP alignment and extension triggers

| Build increment from the MVP note | Implement only these contract responsibilities |
| --- | --- |
| 1. Bound workflow and reference evidence | Pick a scalar-compatible anchor and required semantic qualifiers/units; independent oracles/tolerances and resource/access limits. This contract does not select the domain. |
| 2. Deterministic walking skeleton | Six record loaders/validators in one app; fixed vocabulary, hand fixture/owner review; local compiler/evaluator; saved manifest. Author composition by hand; no AI, search service, UI framework, public deployment or plugin discovery required. |
| 3. Real offline curation | Sequential explicit job writes candidate Model records; source map/trace and checks; owner review; later query reads the same stored versions. No mass autonomous ingestion or inline curation. |
| 4. Query composition/resolution | Agents propose existing references/bindings; validator remains authority; explicit meta-input authorization and unresolved gaps. No new implementation kinds. |
| 5. Inspector/reuse/substitution | Display saved lineage and failures; create new versions/runs; demonstrate another composition without a special computation path. |

Deferrals retain extension seams, not speculative implementations:

- Arrays/date series: add named-axis/coordinate/support and missingness profile only if the anchor/next accepted workflow requires it; never silently broadcast.
- Offset/log/arbitrary units and dynamic conversions: new tested unit/adapter profile when a needed quantity requires one; reject rather than shift blindly.
- Different semantic meanings/context transformations: add reviewed explicit adapter models and scoped context rules when a valid use cannot be represented by exact matching; no universal equivalence engine now.
- Non-algebra payloads, state/loops/solvers, multiple implementations: preserve catalog-only source and `implementation.kind`; extend only for a concrete workflow. No generic plugin framework now.
- Distribution/calibration datasets/large artifacts: new value/uncertainty or artifact profile on demonstrated need; no universal propagation/store now.
- Cross-run cache or selective invalidation: only after measured recomputation cost; current new-run/full-recompile policy is correct by construction, not a speed claim.
- Multi-user/distributed registry/auth/publication: replace the local-owner boundary before exposure, not by trusting reviewer fields remotely. Keep pinned refs and append-only evidence now.

Adding required semantics changes the schema/profile version. Preserve older records and declared evaluator build; migration is explicit and does not rewrite old results. Retain unsupported native artifacts without claiming to validate them. No migration-free/universal interoperability promise.

## 9. Review disposition and next evidence

### Recommended defaults proposed for acceptance

1. Scalar-only explicit algebra v0, tiny structural IR, ratio units and exact meaning/context matching; arrays/solvers/semantic adapters require a justified extension.
2. Six logical record kinds; embed symbols/source maps and the sole algebra implementation rather than normalize into a large registry architecture.
3. Human owner approval, scoped model/use/vocabulary and exact meta-value authorization; no authoritative agent self-approval.
4. Decimal source strings with documented binary64 evaluation; unknown uncertainty only; pinned references and complete run lineage.
5. No inline curation, no caching, no arbitrary code/network calls in execution; fixtures can bootstrap but cannot count as real curation or analyst validation.

These are recommendations, not user choices already made. No need to ask the user to pick a JSON validator or database from untested alternatives.

### Still needed before implementation acceptance

- User review of the proposed restrictions and selected first workflow; exact anchor/reference sources, milestone/resource ceilings still come from the first-build scope.
- Derive executable structural schemas/validators from this contract, then run the matrix. Revisit unsupported required operators/types based on actual source models rather than widening speculatively.
- Select and verify evaluator/storage/Meta access against that workflow. Confirm actual numeric/timeout behavior; hand arithmetic is not a runtime test.
- Decide permanent inline-curation exception policy separately. v0 deliberately needs no exceptions.

**Verification of this documentation:** examples and cross-references can be checked for JSON syntax, arithmetic/reference consistency and Project Memory integrity. That is not validation of an executable schema, safe parser, source fidelity, review authentication or a working runtime. Record exact checks performed when presenting this draft.

## 10. Critical review — revise before acceptance

Review requested by the user on 2026-10-28. **Disposition: keep the architectural direction; do not accept the exact contract as written.** Sections 1–9 remain the original proposal, not silently corrected rules. Recommendations in this section identify revisions to make next; they do not themselves establish a replacement schema. This is a desk review with hand-traced counterexamples, not runtime test evidence or new external research.

### What is established, open, or potentially stale

- Established: dedicated offline curation, query-time consumption, explicit generated contributions, independent instances, source provenance and pinned lineage.
- Previously retired/paused: the sole-engine browser/RPC architecture and social features; nothing here reopens them.
- Open: anchor workflow, access/resources, executable profile and exact review policy. Scalar-only execution and per-composition Meta authorization are recommendations, not user mandates.
- Potentially stale: claims that the draft is the smallest aligned contract. Its stage-2 checklist pulls later governance work forward, and its context restrictions have not been checked against real source models. No performance result supports more elaborate scheduling/caching.

### R1 — Blocking: one Context for every symbol cannot express ordinary models

**Where:** §§3.3–3.4 and compiler step 4. Every used symbol's entity kind and temporal basis must match the node Context, and every input/edge must have that complete Context.

**Counterexamples:** `energy = power × duration` can combine interval-average power, a duration and interval energy; `present_value = cash_flow / (1 + rate)^n` combines interval cash flow, a rate with a compounding convention, an elapsed period count and a valuation-date output. Even a scalar supply-demand model can consume quantities for different entities. The electrical fixture hides this because every declared quantity belongs to one element at one instant. A declared static coefficient in an instant-context node also fails the temporal-basis check. Literals avoid this check only by losing the distinct contextual declaration, not by solving it.

**Consequence:** this is not merely an absent array feature. It blocks valid scalar cross-domain composition. The proposed future adapter models do not solve it while adapters must obey the same single-context rule.

**Recommend:** distinguish node defaults from per-symbol context requirements/bindings. Permit only explicitly declared relationships between an input's bearer/time support and an output's; reject unknown or unsupported transformations. The first anchor needs a small finite set of context roles, not a universal time/space ontology. Add one mixed-support or cross-entity scalar case before accepting the interface.

### R2 — Blocking: meaning does not constrain its permissible unit dimension

**Where:** Meaning in §3.1, Symbol/Value and §4 dimension rules. Meaning has no dimension/unit-type constraint; the compiler checks declared expression dimensions and matching boundary meanings separately.

**Counterexample:** a Value labeled `voltage` with unit `A` is structurally expressible. Binding it to a properly declared voltage-in-volts port will fail, but binding it to another wrongly declared `voltage`-in-amperes port can pass the specified identity and boundary-dimension checks. A dimensionally consistent identity assignment can preserve the error. Source review may catch it, but no explicit deterministic vocabulary rule does.

**Recommend:** each executable local quantity specification must constrain its allowed dimension/unit category, checked for literals where applicable, declarations and Values, independently of whether they are bound. Keep meaning identity distinct from dimensions: this rule must not collapse torque into energy. Reserve point/delta/affine categories for a needed extension; ratio-only remains a reasonable first profile.

### R3 — High: scenario equality confuses query context with a fact's origin

**Where:** Context and its exact-equality rule in §§3.3–3.4.

A reviewed observation used in both a baseline and an intervention scenario currently needs a scenario-matched copy or is rejected. A stable parameter cannot be reused over multiple supports without a similar maneuver. Blind copying risks making an assumed reuse look like an independently observed scenario-specific fact. Nor does placing two Values in the same named scenario prove either is valid there.

**Recommend:** explicitly record authorized reuse/assumption in the binding or scenario specification while retaining the original Value's evidence and support. For the first workflow, allow only declared invariant inputs and explicit overrides; do not remove scenario checks or invent general causal transfer. Hand-check a two-scenario comparison sharing one observation and changing one hypothetical input.

### R4 — High: the vocabulary is versioned too coarsely for ongoing offline curation

**Where:** §2 semantic identity and §3.4 single vocabulary revision.

Adding a previously unused `mV` unit or a new model meaning produces a new vocabulary revision. Even unchanged entries acquire different semantic identities because identity includes that entire revision. Old eligible models and newly curated ones then cannot compose without repinning models/values and renewing review. The draft's mV case explicitly demonstrates this churn; it is not just a hypothetical future-scale concern.

**Recommend:** pin semantic/unit definitions at an appropriate smaller granularity, or define a reviewed additive-extension compatibility rule that establishes unchanged entries remain identical. Choose one, not both mechanisms plus a crosswalk engine. Changed definitions must invalidate affected uses; unrelated additions should not invalidate every model. A frozen vocabulary is acceptable for the first fixture, not a credible default for the continuing curation loop.

### R5 — High: scalar algebra is a useful bootstrap, not yet an evidence-based MVP ceiling

**Where:** §§1, 4 and 8. Step 1 says to pick a scalar-compatible anchor, although the MVP sequence first bounds the useful question and references.

The grammar excludes clipping/branching, roots, general powers and dated arrays. The ±8 integer-power limit excludes a direct tenth-year discount factor; a variable horizon or a non-integer growth transform is not representable as that operation. Unrolling some computations into many mul/div assignments is possible, but that is a serialization workaround, not evidence of faithful or convenient curation. Common scalar models can fail before any advanced solver is needed.

**Recommend:** keep the tiny profile for the walking skeleton, then inventory operators and data shapes from the selected actual source models before freezing the complete MVP profile. Add only demonstrated needs with type/domain rules and independent cases. Do not add a universal function library, arbitrary code, or arrays merely for generality. Equally, do not choose a weak problem solely to preserve the current grammar.

### R6 — High: candidate knowledge is promised but has no adequate explicit validation variant

**Where:** general closed-shape/reference rules, §3.1 unknown semantics, Model and `source-only` in §3.2.

The investigation requires partial, ambiguous and non-executable candidates. Yet the model still requires a vocabulary, source-linked typed Symbols and the common resolved-reference rules even when implementation is source-only. There is no explicit unknown/contested meaning or unit variant. Leaving symbols empty and placing everything in excerpts may retain a document, but loses the partially extracted declarations that the curator is meant to improve. Requiring invented resolved semantics to save a candidate would be worse.

**Recommend:** separate candidate/catalog structural validation from execution eligibility. Retain known local declarations, unresolved fields, competing interpretations and diagnostics without making them executable. A minimal candidate variant is enough; a second generic knowledge-base framework is not. Source-only is an execution-capability label, not a complete extraction/review lifecycle.

### R7 — Medium: sound governance goals are expanded into premature runtime machinery

**Where:** §3.5 linear review heads/compare-and-append and §5 per-instance withdrawal checks; §8 six loaders/review machinery in stage 2.

Keep attributable owner admission, version/use scoping and honest evidence. But a single-operator, seconds-long local evaluator need not implement concurrent review-head reconciliation and repeated revocation monitoring to demonstrate the skeleton. `Composition.review_ids` also duplicates authority that the compiler must independently resolve; its exact role is unclear.

**Recommend:** use one authoritative local admission operation and serialized registry/review updates, with a documented eligibility snapshot boundary. A simple lock can exclude withdrawal during the short execution if that is the chosen policy; do not claim live revocation without implementing it. Prevent new runs after withdrawal and retain old evidence. Resolve review heads once under that boundary and save them in the Run; remove caller review IDs or clearly mark them as expected preconditions. More elaborate concurrency/revocation semantics should follow an actual concurrent-use requirement.

Exact-composition Meta authorization is conservative, not an error: it prevents an agent from authorizing its own guesses. However, requiring renewed owner approval for every otherwise innocuous scenario edit makes interactive gap-filling human-gated. State that tradeoff plainly. Initial one-click, exact-value consent is sufficient; broader scoped permissions can be a separate later policy, not a reason to remove disclosure or approval.

### R8 — Medium: missing planning/result semantics and excessive numerical prescriptions

**Planning and blocked runs:** a strict Composition cannot omit an input or contain unresolved references, yet Run requires a valid Composition Ref even for `blocked`. A rejected proposal therefore has no clearly defined persisted identity/input artifact for the advertised failure inspection. Save the proposed request plus diagnostics separately from executable compositions, or define a minimal draft variant. Do not mark a malformed graph executable merely to log its rejection. No large workflow state machine is necessary.

**Question intent and applicability:** purpose currently distinguishes fixture/analyst, not evaluation/scenario comparison/forecast. Arbitrary applicability prose and reviewer labels are not runtime checks of all scientific assumptions. Pin the supported request/operation and selected scenario assumptions in run evidence; distinguish machine-checked predicates from human-reviewed and unresolved applicability conditions. Do not claim causal or predictive validity from successful DAG evaluation. Use the first anchor to decide which assumptions require executable guards. No universal causal calculus is needed.

**Uncertainty:** saying 'we do not propagate uncertainty' is appropriate; accepting only `unknown` makes it impossible to retain a source-reported interval as structured evidence without a new executable type. Preserve supplied uncertainty evidence even if only the point estimate executes; label outputs 'not propagated' rather than inventing bounds or presenting them as calibrated. A quote/citation can be enough initially. Separate data retention from computational capability.

**Numerics:** documented binary64, finite checks, bounded parsing and declared tolerances belong now. A custom repeated-multiplication power algorithm, mandated shortest-decimal output, forbidding FMA, exhaustive changed-scale load/store traces and special underflow rules are not established MVP needs. They can constrain engine reuse and create more conformance work than the algebra itself. Prefer a pinned engine/build, documented behavior and independent tolerance-based references unless bit-for-bit cross-engine replay is an actual requirement. Preserve source numeric text and essential conversion evidence; never silently change domains or swallow nonfinite results. Coherent-scale normalization also needs a range trial: a large finite source magnitude can overflow on normalization even where a dimensionless ratio could be finite. Treat that as a declared numeric limitation rather than a physical invalidity.

### What not to simplify away

The six logical kinds are not, by themselves, overengineering. Vocabulary, Model, Value, Composition, Review and Run answer distinct questions; collapsing them would risk recreating a global-variable table or treating generated assertions as reviewed models. Embed implementation/source maps, keep one backend and evaluator, retain immutable versions, explicit bindings and unknown uncertainty, and recompute conservatively. No graph database, plugins, cache, distribution engine, public identity system or arbitrary-code runtime is justified by this review.

Fixture/sourced evidence separation is also necessary. However, a run combining a real sourced model with a hypothetical input is a valid scenario calculation when labeled accordingly; it is not empirical verification of that model. Do not equate every synthetic/hypothetical input with a prohibited model fixture. Preserve the existing `user-scenario` distinction and disclose its reliance.

### Minimum revision and evidence sequence

| Stage from the MVP note | Do now | Do not make a prerequisite |
| --- | --- | --- |
| 1. Bound workflow | Inspect a few real source models and independent cases; determine required context roles, operators, unit meanings and intended question type | A universal ontology or choosing a domain solely to fit the draft |
| 2. Deterministic skeleton | Fixed fixture vocabulary; explicit instances/bindings; minimum structure/meaning/unit/context/domain validation; simple local admission; saved run and rejected-proposal evidence | Full concurrent review protocol, imported prior-run Values, elaborate numeric serialization/conversion tracing, production inspector |
| 3. Offline curation | Candidate-versus-executable validation, retained sources/trace, owner admission, additive vocabulary evolution and a real stored extraction | Autonomous fleets, general semantic crosswalks, arbitrary code |
| 4. Query composition | Bounded discovery, explicit unknowns, authorized disclosed estimates, scenario input reuse and request intent | Universal recursive resolution or automatic model publication |
| 5. Inspection/substitution | Show actual lineage/limitations; change input/model; demonstrate shared observation across scenarios and a second composition | Public hosting or graph-editor polish |

The first-stage fixture can remain narrow. The **complete MVP** must still demonstrate real offline curation followed by reuse, valid multi-model composition and revision—not just a beautifully validated electrical calculator.

Before accepting a revised contract, hand-review (then implement as focused checks): one mixed-context model; one meaning/unit contradiction; one additive vocabulary update with old/new model reuse; one partial candidate; and one shared-observation two-scenario comparison. Alongside these, retain the existing arithmetic, wrong-meaning, wrong-unit, domain, independent-instance and lineage cases. These are proposed checks, not checks run in this review. No need to execute all future solver/formalism trials to start the skeleton.

**Bottom line:** the draft spends too much precision on operational mechanics while underrepresenting the semantic relationships that make model composition useful. Fix those semantics and stage the mechanics; do not abandon the layered direction or weaken honest rejection/provenance.

## Provenance

Prepared at the user's request to make the representation investigation concrete and reviewable while aligning with [[note-mvp-build-sequence-and-extension-triggers]]. Derived from existing project research, not additional external research or model curation. Synthetic examples are clearly separated from external sources and actual test evidence. The draft does not resolve the universal representation question or authorize application deployment.
