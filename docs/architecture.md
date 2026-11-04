# Architecture

## How models are represented

All representation contracts live in `src/connected_models/contracts.py` as frozen dataclasses:

- A **Model** is one revisioned scalar relationship: an id, a version, named input **Ports**, one output Port, an expression string, guard strings, a source, and assumption strings. Revisions are immutable; the `id@version` key is the only way to reference one.
- A **Port** is a meaning, a ratio unit, and an exact context string (for example `delivered_heat` in `kWh` for `home-A:representative-year:constant-real-prices`). Binding requires an exact meaning/context match; units convert only through the registry scales, and currency units never convert implicitly.
- **Dimensions** are exact seven-axis rational vectors: mass, length, time, currency, temperature, current, amount. The `UNITS` table maps each unit string to dimensions plus a scale against the canonical basis (kWh, m, s, USD, K, A, mol); the `MEANINGS` table maps each meaning to its dimensions, so a port's meaning and unit are checked against each other. Lexical spellings (`dollars`, `meters`, `m/s²`) resolve through a validated `UNIT_ALIASES` table next to `UNITS`, with canonical case winning (`S` is siemens, `s` is seconds). Inspect the whole registry with `connected-models units [filter]`.
- **Expressions** use scalar arithmetic (`+ - * / **`), comparisons in guards, and the allowlisted calls `log`, `log10`, `exp`, `sqrt`, `sum`, `prod`, `len`. Powers carry bounded exact-rational exponents; expressions are capped at 2048 characters and 128 AST nodes. Anything else is rejected before evaluation.
- Universal physical constants live in a versioned registry (`pi`, `stefan_boltzmann`, `gravitational_constant`, `avogadro`) and are named in expressions instead of inlined; the engine converts them through the registry unit scales. Case-specific fitted values stay input variables, and conversion factors live in unit scales, never in expressions (see the canonical-expressions decision in Project Memory).
- A **Composition** is a bounded scenario: nodes plus requested outputs. Each **Node** instantiates one model revision, binding every input to a **Value** (an amount with a port, an origin, and evidence) or a **Reference** to an upstream node. Index-family inputs take bounded tuples (at most 256 elements) for summation-style models.

## How models execute

Execution (`src/connected_models/runtime.py`) is deterministic and has no inference inside it:

1. **Compile** the composition: topologically sort nodes, reject cycles, and check every binding against its model's ports (meaning/context match, guard domains, scenario input origins).
2. **Normalize** each input to canonical units by multiplying with its unit scale.
3. **Check guards** against the normalized inputs, then **evaluate** the expression (or run the bounded solver for a `solve_for` view).
4. **Denormalize** the result into the output port unit and record the step: normalized inputs, result, evidence, and everything it relied on.

The run manifest pins the exact model definitions (with a snapshot hash), the vocabulary, and the admissions in force, so `replay RUN_ID` can re-execute later and report whether status, error and outputs match exactly. `revise` never modifies a saved run; it writes a new run linked with `revised_from`.

## How the LLM is used

`answer` makes structured-output calls (`AnswerQuestionGrounded`) and nothing else: one to parse the question into typed facts with exact quotes and compose a graph from those facts in the same response, plus up to two repair rounds when the runtime rejects a proposal. Each repair sees the prior proposal and its exact machine error. Planning works backward from the requested output: find models producing it, check assumptions, and recursively satisfy each input from a fact or an upstream model. The model cannot emit numeric literals; the runtime validates every fact (exact quote in the question, unique IDs), validates the graph shape, checks every binding, and executes it. Contradictory questions and missing inputs yield `needs-input` with clarification questions; a clarification may propose a specific assumed value with justification for the user to confirm or replace, but estimates never fill graph bindings silently. The one exception is the explicit opt-in `--fill-in-assumptions` (or `FILL_IN_ASSUMPTIONS=True` in the environment): then the composer may supply question-implied values as assumed facts, and every assumed binding is executed and recorded on the run under `assumptions`, shown in CLI output and the HTML report. Unsupported coverage yields `blocked`.

The system prompt lives as an editable file, `src/connected_models/prompts/answer-question.md`, and loads on every request; when assumption filling is enabled, `src/connected_models/prompts/answer-fill-in-assumptions.md` is appended, and repair rounds append `src/connected_models/prompts/answer-repair.md`. See [prompts.md](prompts.md) for the editing rules. The JSON schema and the user message (question, solver profile, model catalog) stay in code in `src/connected_models/workflows.py`. Each catalog entry carries only composition signal — input/output ports, assumptions, and guards when non-empty; identity, version, status, source, and expression stay in the database. A second prompt, `src/connected_models/prompts/offline-model-extraction.md`, serves the `curate` command, which extracts one NIST source relationship into an unapproved candidate. Every call accrues through the spend ledger described in [setup.md](setup.md). The call currently receives the full eligible catalog; catalog retrieval is future work.
