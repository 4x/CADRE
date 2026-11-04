# CVP lane brief: lane-B models + identity adapters (brief 20)

To: curation review (batch economics-cvp-b01, 6 new records)
From: CVP lane curator (native compat-curation subagent), 2026-11-04
Status: proposed (mechanical + new-record curation — no admitted record is revised; all reviews stand)

## Prescription (6 new records, r1, exactly as delegated)

Lane B of the economics domain, economics batch `economics-cvp-b01`:

1. `economics--contribution-margin-per-unit`: P (selling_price_per_unit, USD/unit),
   V (variable_cost_per_unit, USD/unit) -> C (contribution_margin_per_unit, USD/unit),
   expr `P - V`, guards `P>=0`, `V>=0`.
2. `economics--contribution-margin-income`: Q (units_sold_or_produced, unit),
   C (contribution_margin_per_unit, USD/unit) -> CM (contribution_margin_income, USD),
   expr `Q * C`, guards `Q>=0`, `C>=0`.
3. `economics--break-even-units`: FIX (fixed_operating_cost, USD),
   C (contribution_margin_per_unit, USD/unit) -> QB (break_even_unit_quantity, unit),
   expr `FIX / C`, guards `FIX>=0`, `C>0`.
4. `economics--target-profit-units`: FIX, PI (target_operating_profit, USD), C ->
   QT (required_unit_sales_for_target_profit, unit), expr `(FIX + PI) / C`,
   guards `FIX>=0`, `PI>=0`, `C>0`.
5. `economics--operating-cost-as-fixed-operating-cost`: identity adapter,
   OC (operating_cost, USD, relevant-range CVP face) -> FIX (fixed_operating_cost, USD),
   expr `OC`, guard `OC>=0`.
6. `economics--operating-leverage-as-price-elasticity`: identity adapter,
   DOL (operating_leverage_ratio, 1) -> E (price_elasticity_of_demand, 1),
   expr `DOL`, guard `DOL>=0`.

## Shared context family (verbatim everywhere — design note)

Every port of all 6 records carries one single byte-identical string:

> same CVP analysis, relevant range, currency, price/cost basis and period as P, V, C, Q, FIX, PI, OC and DOL

The delegation requires the family template verbatim everywhere AND a
chain-connectivity proof that the margin->income->break-even legs bind. Those
two requirements jointly force a single batch-wide instantiation: per-record
co-input subsets (e.g. `as P and V` on record 1 vs `as Q and C` on record 2)
would leave every in-batch leg a context near-miss and nothing would bind.
The roster is therefore the lane-B CVP input family (all 8 input symbols),
naming the shared analysis whose conditions the value belongs to; each
record's translation notes state it consumes/emits its own subset.

Brief-8 consideration: brief 8 rejects stamping a context that asserts
record-foreign provenance (EF applicability, GWP vintage, formulation symbols)
onto a record. This roster is the weaker sibling shape — it names the shared
analysis's own sibling inputs, not foreign physics — and the value on every
port genuinely belongs to a CVP analysis with those inputs. The trade is
explicit: one shared string buys all five in-batch legs (three C legs, two FIX
legs) with zero revisions and zero orphans (survey below). Review may still
reject the roster design on its own terms; the fallback is per-record contexts
plus brief-10-style face adapters, at the cost of 5 more records.

## Oracle inventory (all numbers verified 2026-11-04)

- AccountingTools, unit contribution margin (Bragg, 2026-08-02): P=$50, V=$30
  -> C=$20; FIX=$10,000 -> BE 500 units.
- AccountingTools, contribution per unit (Bragg, 2026-09-09): FIX=$10,000,
  C=$5 -> BE 2,000 units; ABC International: $20,000 revenue, $14,000 variable
  costs, $6,000 total over 500 widgets -> $12/unit.
- AccountingTools, CVP components (Bragg, 2026-09-27): FIX=$50,000/month,
  C=$50 -> BE 1,000 units; PI=$20,000 -> (50,000+20,000)/50 = 1,400 units;
  +$10,000 fixed -> (70,000+10,000)/50 = 1,600 units/month.
- AccountingTools, breakeven point (Bragg, 2026-05-10): unit formula
  FIX / average C; stable-price/cost/mix scope; ignores demand/achievability.
- CFI, Break-Even Analysis: book P=$100, V=$5 -> C=$95; Company A water
  bottles FIX=$100,000, P=$12, V=$2 -> C=$10 -> BE 10,000 units ($120,000
  revenue, $20,000 variable cost at that point).
- Lumen, Accounting for Managers Module 8, Target Profit Analysis: kayaks
  P=$500, V=$225 -> C=$275, FIX=$7,700 -> BE 28 kayaks; PI=$30,000 ->
  $37,700/$275 = 137.0909... rounded UP to 138 (137 yields only $29,975).
- HBS, Cost-Volume Profit Models (Hawkins/Narayanan/Cohen/Jurgens): verified
  by the hbs.edu listing abstract only (full note paywalled, not inspected);
  cited for scope agreement, never for equations or numbers.
- BLS Handbook of Methods Ch. 17 (CPI), Calculation: preliminary C-CPI-U uses
  the constant-elasticity-of-substitution formula with a dimensionless
  elasticity parameter; average prices per normalized quantity/period. Cited
  on the adapters for the dimensionless-elasticity and price-basis/period
  measurement scope only.

Every record carries 2+ references with independent recomputation (22 total);
provenance labels distinguish published oracles, cross-family worked
arithmetic, and curator boundary/guard-scope checks.

## Registry orphan survey (all 251 admitted models, 2026-11-04, mode=ro)

| meaning | producers | consumers | note |
|---|---|---|---|
| selling_price_per_unit | 0 | 0 | new |
| variable_cost_per_unit | 0 | 0 | new |
| contribution_margin_per_unit | 0 | 0 | new; binds only in-batch |
| units_sold_or_produced | 0 | 0 | new |
| contribution_margin_income | 0 | 0 | new |
| fixed_operating_cost | 0 | 0 | new; binds only in-batch |
| break_even_unit_quantity | 0 | 0 | new |
| target_operating_profit | 0 | 0 | new |
| required_unit_sales_for_target_profit | 0 | 0 | new |
| operating_leverage_ratio | 0 | 0 | new |
| price_elasticity_of_demand | 0 | 0 | new |
| operating_cost | 1 | 2 | electricity-cost@1 OUT + annual-saving@1 IN x2, all in `home-A:representative-year:constant-real-prices` — a different context that binds neither bridge face |

Lane-A near-miss vocabulary (`unit_price`, `unit_variable_cost`,
`unit_contribution_margin`, `fixed_cost`, `break_even_quantity`,
`degree_operating_leverage`, `signed_point_price_elasticity`, ...) carries
different meanings by construction, so no edge to or from lane A exists. All 6
lane IDs are absent from the registry (no collisions). The batch therefore
orphans zero chains and breaks zero working edges.

## Rejection mapping (as delegated)

- Margin: nonnegative-guard admission (zero-boundary reference P=V=0 -> 0
  admitted) + negative-margin guard-scope case (P=30, V=50 -> -20 admitted,
  because no guard constrains C itself) + domain rejection of negative P and
  a missing-input case. Downstream C>=0/C>0 guards reject the shortfall.
- Break-even: fractional admission (10,000/12 = 833.333... admitted exactly;
  whole-unit round-up downstream per Lumen) + C=0 rejection (guard and
  division) + negative-FIX rejection + missing-input case.
- Target-profit: worked arithmetic on all three references (1,400; 137.0909...
  with the source's round-up-to-138 rule; re-based 1,600) + declining-returns
  scope in assumptions (post-range parameter drift excluded) + C=0,
  negative-PI, and missing-input rejections.
- Adapters: domain (negative input) + missing-input cases each; orphan survey
  above covers the CVP terms.

## Records authored (batch economics-cvp-b01)

All 6 are `definition`-kind, runtime-ready, with the verbatim shared context.

1. Margin (R1): 5 references (AT 50-30, CFI book 100-5, Lumen kayak 500-225,
   zero boundary, negative-margin admission), 2 rejection cases.
2. Income (R2): 4 references (ABC 500x12; CFI/AT/Lumen at-break-even volumes
   reproducing each family's FIX — chain closure), 2 rejection cases.
3. Break-even (R3): 4 references (AT 500, CFI 10,000, AT-CVP 1,000, fractional
   admission), 3 rejection cases.
4. Target-profit (R4): 3 references (AT-CVP 1,400, Lumen 137.0909..., AT
   added-fixed 1,600), 3 rejection cases.
5. Cost adapter (R5): IN OC = relevant-range operating_cost face, OUT FIX =
   shared in-batch consumer face, expr `OC`, guard `OC>=0`. Honest scoped
   claim: the identity holds under the stated all-fixed precondition (zero
   variable portion in range). 3 references (CFI $100,000 and AT $10,000
   carried totals rechecked against the published figures, zero boundary),
   2 rejection cases. One output feeds both FIX legs (the brief-7 shape).
6. Leverage adapter (R6): IN DOL, OUT E, expr `DOL`, guard `DOL>=0`. The
   relabel is an ASSERTED delegated prescription with no derived economic
   equivalence; the record's assumptions say so explicitly and review must
   accept or reject it on its own terms. 3 references (CFI-worked DOL=3 at
   Q=15,000, DOL=1 no-fixed boundary, DOL=0 boundary), 2 rejection cases.

Engine vocabulary: the 11 new lane meanings were added to `MEANINGS` in
`connected_models/contracts.py` (per-unit money as MONEY per the lane-A
convention; counts and ratios dimensionless), following the per-batch comment
convention. Full repo suite: 178 tests OK.

## Chain-connectivity proof (prove_chain.py, packed artifact, registry ro)

- `margin.OUT C -> income.C`, `margin.OUT C -> break-even.C`,
  `margin.OUT C -> target.C`: all BIND via `Port.require_compatible`.
- `cost-adapter.OUT FIX -> break-even.FIX`,
  `cost-adapter.OUT FIX -> target.FIX`: both BIND.
- Numerical closure through the packed expressions: income(QB,C)=FIX exactly
  for CFI (100,000), AT (10,000) and Lumen (7,700); target(PI=0)=QB in all
  three families.
- Income->break-even is closure, not port binding (meanings differ by design);
  no silent equivalence is asserted.

## Resubmission

Batch `economics-cvp-b01` is validated and packed in
`.runs/compat-curation/cvp/` (bundle + return ZIP as usual) for review per
protocol:

- `validate` JSON -> `valid-data-awaiting-review` (6/6 runtime-ready,
  22 arithmetic + 14 rejection checks).
- `pack` -> `economics-cvp-b01-return.zip`, sha256
  `16af22529525496baaed3e120643bab0251835b8b39f3679fa764cb96689b70d`.
- `validate` ZIP -> `valid-data-awaiting-review`.

It was never staged or imported; the registry is untouched. Deferred:
multi-product weighted-average CM, CM-ratio/sales-dollar forms, and a signed
price-elasticity convention record (see batch `deferred`).
