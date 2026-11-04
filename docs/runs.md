# Revise, replay and solve

## Revise a saved run and compare results

Any saved run with an executable graph can be revised without inference: change direct inputs, substitute a model revision on a node, or both. The original run file is never modified; the revision is saved as a new run linked with `revised_from`. Scenario (`answer`) runs re-execute against the registry's current eligible snapshot, so `--model` selects among reviewed revisions. Amounts use the model's declared port unit, shown by `inspect`.

```powershell
uv run --no-env-file connected-models revise RUN_ID --set upgrade-energy.performance=2 --set investment-npv.investment=12000
uv run --no-env-file connected-models revise RUN_ID --model upgrade-energy=heat-to-electricity@2
uv run --no-env-file connected-models report RUN_ID REVISED_RUN_ID
```

Only direct value inputs can be revised; calculated upstream bindings are rejected with an explanation, as are unknown nodes, undeclared inputs and unavailable model revisions (the error lists what is available). A revision that violates model guards or interface checks is saved as a rejected run with diagnostics, preserving the failure evidence. Listing two or more runs in `report` adds a "What changed" comparison of outputs with deltas, changed inputs and changed models, each run compared against the first listed.

To verify deterministic reproduction without creating a new run, `replay RUN_ID` re-executes the saved graph against its pinned models and admissions and reports whether status, error and outputs match exactly. It saves nothing and exits nonzero on any mismatch.

## Explore what-if scenarios in plain language

`scenarios RUN_ID 'request'` asks Meta to design up to five named what-if variations of a completed run, then executes every proposal through the same revision machinery as `revise`. The model sees only the request plus the run's revisable inputs (node, input, unit, current amount) and executed outputs; it never computes results. Each scenario is accepted with executed engine figures or rejected with the exact machine error (unknown node, undeclared input, calculated binding, guard failure), and the exploration record preserves the proposal, the inference audit, and every per-scenario run id.

```powershell
uv run --env-file .env connected-models scenarios RUN_ID 'What if the heat pump underperforms and the quote was optimistic?'
```

Use `--max N` (1 to 5, default 3) to bound the proposal count. Proposed figures are never trusted: an accepted scenario's numbers come from deterministic execution, so `replay` and `report` verify them like any other run.

## Solve for another quantity in an existing relationship

Directional solve views answer rearranged questions without separate scientific models for every rearrangement. A model revision retains its equation, source, interface meanings, guards and review. A run may select a declared input as `solve_for`, supply all other inputs and the known original output through the reserved `__output__` binding, and return the selected variable using its original unit/context. The composer creates these views through the same question-only interface. It never generates or executes a new formula as an agent-authored model.

```powershell
uv run --env-file .env connected-models answer 'A heating system supplies 12000 kWh of delivered heat over a representative year and consumes 4000 kWh of electricity over that same year, with auxiliaries and losses included. What effective seasonal performance does this imply?'
uv run --env-file .env connected-models answer 'My annual electricity operating cost is 1200 USD with a flat tariff of 0.30 USD/kWh in constant real prices. Fixed charges are unchanged, and maintenance and cooling benefits are excluded. What annual electricity consumption corresponds to that cost?'
uv run --env-file .env connected-models answer 'I am considering replacing my resistance heating with a $10000 heat pump. When would this pay off, assuming a 5% real discount rate? Annual delivered heat demand is 12000 kWh. Baseline resistance heating has seasonal performance 1 and the proposed heat pump has seasonal performance 3. Electricity has a flat tariff of 0.30 USD/kWh'
```

Payback applies the original present-value model's constant-real, uniform year-end savings assumptions conditionally; it does not infer actual equipment life or different maintenance/replacement costs. Its 1–100 year search domain comes from the model guards, not an invented user horizon.

The first algebra profile substitutes known canonical-unit values into restricted rational arithmetic, forms an exact rational-coefficient polynomial, and solves degree one or two over real numbers. Unknown-dependent powers are restricted to integer magnitude at most two; intermediate degree and coefficient-size limits are explicit. Candidates are re-evaluated in the unmodified original expression with every source guard and type constraint; denominator exclusions survive rearrangement. Residual tolerances are recorded (1e-9 relative and absolute). Multiple admissible roots remain an explicit ambiguity with candidates, not a guessed positive branch. Unsupported forms, numerical limits, undefined domains, underdetermination and no admissible root are distinguished. Fixed literals are not free variables. The unitless E=m*c² fixture tests algebra only; this does not add a curated physics model or SI mass/speed vocabulary.

For integer period-count targets, a non-polynomial equality can use finite enumeration when original guards supply both bounds. A requested earliest threshold uses `relation=at_least`, checks each admissible integer in ascending order, and returns the first crossing without assuming monotonicity. At most 1,000 candidate integers are evaluated. Failure means no crossing within that declared domain, not no possible crossing anywhere. Fractional-time payback, general continuous root finding, systems of unknowns, higher-degree/transcendental symbolic solving and user-selected branches outside model guards remain unsupported. Algebraic reversal does not establish causal reversal or a scientifically valid inverse of a statistical/calibrated model.

Curators remain responsible for source relationships, scientific scope, variable roles/constants and domain constraints. The solver is a separate deterministic facility. Future derived implementations can be cached/indexed against a pinned source revision and solver profile without multiplying canonical model identities. Independently estimated inverse models or changed scientific assumptions would need their own linked evidence/review.

Local runtime artifacts are stored in `.registry/`, `.runs/` and `.usage/`, all excluded from version control. Preserve the registry and spend ledger when continuing the prototype.

The canonical delivery plan is [MVP milestones](../knowledge/notes/mvp-build-sequence-and-extension-triggers.md); current project context is in [PROJECT_STATE.md](../PROJECT_STATE.md). Source/evidence records and design decisions live in Project Memory under `knowledge/`.
