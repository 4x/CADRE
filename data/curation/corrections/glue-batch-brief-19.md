# Glue batch brief: economics arithmetic glue — sum, scaler, difference, payback, unit-rate (brief 19)

To: curation review (batch economics-glue-b01, 5 new records)
From: glue batch curator (native compat-curation subagent), 2026-11-04
Status: proposed (new records — no admitted record is revised; all reviews stand)

## What happened

The delegation assigns a 5-model arithmetic-glue batch in the economics domain. Its numbered
specification pins four records exactly (total-of-two-money-amounts, scaled-money-amount,
money-difference-first-minus-second, simple-payback-periods, with fixed ports, expressions and
guards, and no SUM variants), while the batch size (5-model), the reference pools (BLS
Handbook / CBP Informed Compliance for unit-rate), the rejection-case list (UNIT-RATE
gallon-quantity rejection + SUM-orientation test) and the unit-rate decision clause all require
a fifth record: a conservative counts-only money unit rate. This brief authors exactly those
five records — no extras, no SUM variants — and documents the unit-rate resolution below.

All endpoint vocabulary was surveyed read-only (`.registry/models.sqlite3`, `mode=ro`; never
staged, reviewed, admitted, or otherwise touched). The batch binds no existing chain: every
glue output slot is producer-free or context-mismatched against all current consumers.

## Registry survey (all 251 admitted models, 2026-11-04)

All five batch IDs are absent (no collisions). Meaning-level survey for every port meaning
the batch uses:

| meaning | producers | consumers | working edges |
|---|---|---|---|
| `named_money_amount` (new) | 0 | 0 | 0 |
| `sum_of_money` | 0 | 0 | 0 |
| `plain_multiplier` (new) | 0 | 0 | 0 |
| `scaled_money` | 0 | 0 | 0 |
| `difference_of_money` | 0 | 0 | 0 |
| `upfront_cost` | 0 | 1 (`net-present-value@1` investment, home-A context) | 0 |
| `annual_saving` | 1 (`annual-saving@1`, home-A context) | 1 (`uniform-present-value@source-3`, home-A context) | 1 (home-A leg, untouched) |
| `payback_period_count` | 0 | 0 | 0 |
| `counted_unit_quantity` (new) | 0 | 0 | 0 |
| `unit_price` | 0 | 6 (elasticity x3, contribution-margin-ratio, break-even, contribution-margin) | 0 |

Zero-edge verification (asserted in `author_bundle.py` at author time): the payback
`annual_saving` input context (payback scope) differs from the home-A producer context, so it
forms no edge with `annual-saving@1`; the unit-rate `unit_price` output context (lot scope)
differs from all 6 `unit_price` consumer contexts, so it binds no existing consumer; the three
money-glue output meanings have no producers or consumers at all. The batch therefore orphans
zero chains and creates zero accidental edges by construction.

Near-duplicate analysis (all read-only; `duplicate_of` stays empty with documented
distinctions): `economics--average-total-production-cost@r1` (TC/Q, production scope, units
produced — explicitly not units sold) differs from the unit-rate record (transaction-lot scope,
transacted counts, `unit_price` output); its TC>=0/Q>0 guard shape is the admitted precedent
this batch mirrors. `economics--unit-contribution-margin@r1` (price minus unit variable cost)
is specific contribution semantics, not a generic named difference.
`economics--identical-product-mean-transaction-price@r1` is a family-weighted mean over
transaction vectors, not a single-lot scalar rate. No existing record computes a generic
two-input money sum, money scaling, ordered money difference, or simple payback.

## SUM-orientation: input and output meanings stay distinct (proof)

The batch keeps `named_money_amount` (inputs) and `sum_of_money` (output) as different
meanings by validity and by inverse semantics.

Validity (forward direction): the engine binds ports only on exact `(meaning, context)`
equality (`Port.require_compatible`). Because the meanings differ as strings, a
`sum_of_money` output can never satisfy a `named_money_amount` input port: sums cannot
re-enter as named components, so no iterated sum-of-sums chain can form. The author script
asserts input/output-meaning disjointness for all five records, and the SUM missing-input
rejection case plus the unit-rate missing-total case document the fail-closed behavior.

Inverse semantics (single-output vs many-inputs): the sum output alone underdetermines its
inputs — infinitely many pairs sum to one total (S = 10500 admits both (9000, 1500) and
(10000, 500)), so no inverse view can recover *named* components from an anonymous sum. Each
input is recoverable only with the output *plus* the other input (A = S - B). The output is
therefore semantically poorer (one anonymous aggregate) than the input pair (two identified
components), which is exactly why the two sides need different meanings. Collapsing them
would assert that an aggregate is one of its own components — false — and would admit
silent sum-chaining. The same orientation holds across the batch: scaled, difference,
payback-count and unit-rate outputs never re-enter as named inputs.

## Unit-rate decision: conservative counts-only scope (evidence check documented)

Decision: `economics--money-unit-rate` admits dimensionless item counts only
(`counted_unit_quantity`); gallon, ounce, pound, kilowatthour and other physical-measure
quantities are excluded, with the gallon exclusion carried by the Q = 0 domain rejection
case (division undefined; volumes fail closed at composition on meaning/unit mismatch).

Evidence check (live, 2026-11-04): CFI defines unit cost over counts on three inspected
pages — cost-of-production ("total cost of production divided by the number of units
produced"), cost-driver ("Cost per unit of product A = Total cost/Number of units =
$120,000/300 = $400"), and variable-cost-plus-pricing Step 2 ("dividing the total cost by
the number of units produced"). Investopedia's worked commission example prices 100 shares
at $10 each (counted shares); Investopedia has no dedicated average-cost-per-unit term page
(`terms/a/averagecost.asp` and `terms/u/unit-economics.asp` both returned 404). Nothing in
the live CFI/Investopedia evidence contradicts the conservative interpretation, so per the
delegation it was adopted without asking. Cross-note: the BLS Handbook itself spans physical
measures (per-ounce flour, per-pound publication), so this record is deliberately narrower
than BLS practice; CBP customs quantities are unit counts throughout (19 CFR 152.103(e),
152.105), which supports the restriction. A physical-measure sibling would need its own
meaning and record (deferred).

## Oracle independence proof

Every record carries 3 references: 2+ from independent public publishers plus one
constructed boundary/limiting identity. Formula authorities (relationship sources) are never
Investopedia or CFI — asserted mechanically in `prove_oracles.py`:

| record | formula authority (relationship source) | oracle 1 | oracle 2 | boundary |
|---|---|---|---|---|
| total-of-two-money-amounts | GAAP ASC 230 sum-of-amounts (ASU 2016-18) | CFI textile $9,000+$1,500=$10,500 | Investopedia XYZ $50B+$120B=$170B | zero component |
| scaled-money-amount | GAAP ASC 830-30-45-3 rate scaling | CFI $9x1,000=$9,000 | Investopedia $1,000x0.025=$25 | unit factor |
| money-difference-first-minus-second | GAAP ASC 830-30-45-7 (FX 5-6) | PwC FX 5-6 $300-$264=$36 | CFI $20-$2=$18 | equal amounts |
| simple-payback-periods | DOE BECP methodology (formula+scope) | DOE Utah $4,606/$495=9.3 | DOE Texas $3,312/$381=8.7 | zero cost |
| money-unit-rate | BLS Handbook CPI average prices | BLS corn 69c/3=23c per can | CBP 152.105 $47,500/500=$95 | zero total |

Independence notes. Money models: CFI and Investopedia are independent commercial
publishers with distinct fact patterns; the PwC-guide GAAP oracles add a third publisher for
the difference record. GAAP access was indirect and is disclosed in every evidence field:
asc.fasb.org returned HTTP 403 and Viewpoint codification full text is premium-gated, so
ASC paragraphs were inspected via Viewpoint's open verbatim excerpts (FX 5.5: ASC
830-30-45-3/45-4/45-7, ASC 830-10-55-10/55-11; FSP 6.5: ASC 230 sum/change rules). Unit-rate:
BLS Handbook and the eCFR are independent federal publishers. Payback: Utah and Texas are
independently computed DOE state analyses (different climates, costs, savings) with
published one-decimal paybacks; tolerances (0.01) cover only the states' rounding
(|9.3051-9.3|=0.0051, |8.6929-8.7|=0.0071). The EIA Electric Power Monthly October 2026
release (data for August 2026; Table 5.3, e.g. residential 18.16 c/kWh) is the Pub 2026-10
pin and scopes the energy-price denomination of annual savings, not a payback oracle.
`prove_oracles.py` recomputes all 15 references under `Decimal` (independent of the
validator engine): ALL PASS (15 arithmetic + 10 rejection + 5 disjointness + 5 authority
checks).

## Records authored (batch economics-glue-b01)

1. `economics--total-of-two-money-amounts@r1`: inputs A/B (`named_money_amount`, USD) ->
   S (`sum_of_money`, USD), expression `A + B`, no guards. Requires-extension (new input
   meaning). Rejections: unknown-meaning / no-zero-fill missing-input pair.
2. `economics--scaled-money-amount@r1`: inputs base (`named_money_amount`, USD), factor
   (`plain_multiplier`, 1) -> M (`scaled_money`, USD), expression `base * factor`, no
   guards. Requires-extension (two new input meanings). Rejections: decimal-factor
   missing-base case plus missing-factor case (no silent x1 default).
3. `economics--money-difference-first-minus-second@r1`: inputs first/second
   (`named_money_amount`, USD) -> D (`difference_of_money`, USD), expression
   `first - second`, no guards. Requires-extension (new input meaning). Rejections:
   reversed-order-sign missing-minuend case plus missing-subtrahend case.
4. `economics--simple-payback-periods@r1`: inputs C (`upfront_cost`, USD), A
   (`annual_saving`, USD) -> P (`payback_period_count`, 1), expression `C / A`, guards
   `C >= 0`, `A > 0`. Runtime-ready on pre-provisioned vocabulary with a full runtime
   projection and contract check. Rejections: A = 0 domain case (A <= 0) plus missing-A
   case.
5. `economics--money-unit-rate@r1`: inputs T (`named_money_amount`, USD), Q
   (`counted_unit_quantity`, unit) -> R (`unit_price`, USD/unit), expression `T / Q`,
   guards `T >= 0`, `Q > 0` (mirrors the admitted TC/Q precedent). Requires-extension
   (two new input meanings). Rejections: gallon-quantity Q = 0 domain case plus
   SUM-orientation missing-total case.

All five are `definition`-kind records with signed-where-applicable domains, ordered ports
where order matters, and substitution-checked inverse notes. Deferred (not authored): wider
sums (3+ inputs, families, running balances), physical-measure unit rates, and discounted
payback/NPV rules.

## Resubmission

Batch `economics-glue-b01` is validated and packed in `.runs/compat-curation/glue/`:

- `validate` on `economics-glue-b01-bundle.json` -> `valid-data-awaiting-review`
  (5 models; 15 arithmetic + 10 rejection checks; payback runtime-ready with contract
  check, 4 requires-extension).
- `pack` -> `economics-glue-b01-return.zip`, bundle
  sha256 `a1f7f0ef850feaebdff838dc90617e9d7aff7b3668afb3efb936893bc6d371bb`.
- `validate` on the return ZIP -> `valid-data-awaiting-review` (same checks).

Commands (central package, offline): `uv --cache-dir .uv-cache run --no-env-file --offline
-m connected_models.curation validate|pack ...`. The batch was never staged or imported;
the registry is untouched.

Out of scope (separate near-misses for other briefs): the `annual_saving` home-A producer
leg (different context, untouched working edge into `uniform-present-value`), the 6
`unit_price` consumer legs (distinct contexts, still unbound), any `upfront_cost`
production, and the family-sum / physical-rate / discounted-payback siblings in `deferred`.
