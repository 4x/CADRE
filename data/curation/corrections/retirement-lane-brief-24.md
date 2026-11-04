# Retirement-planning lane brief: nest egg, withdrawals, benefits, distributions (brief 24)

To: curation review (batch engineering-finance-retire-b01, 6 new records)
From: deep-lane brief author (22-25), 2026-11-04
Status: proposed (prescription only — no bundle authored, no registry touched; all reviews stand)

## What this lane adds

Six atomic records for retirement planning that complement — never
duplicate — the admitted engineering-finance annuity/loan family: the
missing ordinary-annuity present value (end-of-period withdrawals), the
withdrawal-rate nest egg (Bengen rule shape), the income replacement ratio,
the Social Security delayed-retirement-credit benefit, the IRS required
minimum distribution, and the expense-coverage multiple. Record 1 reuses
the canonical annuity vocabulary with a retirement context; records 2-6
mint retirement-specific meanings.

All endpoint vocabulary was surveyed read-only (`.registry/models.sqlite3`,
`mode=ro`, all 262 admitted models; never staged, reviewed, admitted, or
otherwise touched). All six lane IDs are absent (no collisions). Every
port carries a retirement context that differs byte-wise from all existing
producer/consumer contexts on the reused meanings (table below), so the
lane binds no existing chain (the brief-19 shape).

## Do-not-resubmit boundaries (wave-2 drift guard)

The admitted engineering-finance family owns these relationships outright;
this lane prescribes NONE of them, not even with retirement labels:

- Capital recovery / level payment: `engineering-finance--level-loan-periodic-payment@r1`
  and `@r2` (`P*i*(1+i)**n/((1+i)**n - 1)`). An "annuity payment from nest
  egg" record would be this exact expression — NEVER resubmit.
- Accumulation: `engineering-finance--ordinary-annuity-future-value@r1`,
  `--annuity-due-future-value@r1`, `--lump-sum-future-value-discrete@r1`.
- Due-timing present value: `engineering-finance--annuity-due-present-value@r1`
  (`R*((1-(1+i)**(-n))/i)*(1+i)`, beginning-of-period). Record 1 differs by
  timing (end-of-period, no `(1+i)` factor) — a distinct relationship, not
  a relabel. The due record's context
  (`same-series:beginning-of-period-level-payments:fixed-rate`) and record
  1's context differ accordingly.
- Growing annuity: `engineering-finance--growing-annuity-present-value@r1`.
  No growing-withdrawal PV record in this lane.
- Rate conversions: `--effective-annual-rate-nominal`, `--periodic-rate-from-nominal`,
  `--fisher-real-rate`, `--effective-discount-rate`, `--real-rate-as-unit-frequency-nominal`,
  and the two periodic-rate schedule adapters. No rate restatement.
- Loan amortization splits: `--loan-payment-interest-portion`,
  `--loan-payment-principal-portion`, `--arithmetic-gradient-annual-equivalent`.
- Inverse doctrine (load-bearing for this lane): lump-sum present value
  (`F/(1+r/m)**(m*t)`), the sinking-fund payment (`F*i/((1+i)**n - 1)`),
  and any log-form term/rate solution are solver-derived inverses of
  covered records and are NOT prescribed — pure inverses are exactly the
  wave-2 drift pattern. Record 6 (`S / W`) is not an inverse of any
  covered record (no covered record divides two money stocks).
- Home-A annuity PV:
  `uniform-present-value@source-3`
  (`annual * ((1 + rate) ** years - 1) / (rate * (1 + rate) ** years)`).
  Record 1 shares the ordinary-annuity mathematics but is prescribed in
  the general eng-finance vocabulary, distinguished on all three inputs:

| port | UPV (home-A, covered) | record 1 (retirement, new) |
|---|---|---|
| payment | `annual_saving` [USD] | `periodic_payment` [USD] |
| rate | `discount_rate` [1] | `periodic_rate` [1] |
| term | `period_count` [1], guards 1..100 | `period_count` [periods] |
| context | `home-A:...` | `same-series:end-of-period-level-withdrawals:fixed-rate:retirement-horizon` |

  The UPV record stays the home-A energy-savings identity; record 1 is the
  general-series form. A numerical cross-check (UPV == record 1 on matched
  inputs) ships as labeled cross-record recomputation, never as equivalence.

## Oracle inventory (all numbers verified 2026-11-04 unless flagged)

- Ordinary-annuity PV table value: PVIFA(5%, 10) = 7.72173, i.e. $10,000/yr
  x 10 yr at 5% -> $77,217.35 end-of-period. The curator pins a public
  annuity-table or textbook source at author time (formula authority for
  the timing convention); the due-PV closure (duePV/(1+i)) and the UPV
  cross-check above ship regardless as labeled recomputation.
- Bengen, W. (1994), "Determining Withdrawal Rates Using Historical Data,"
  Journal of Financial Planning (October 1994): first-year 4% withdrawal
  with inflation-adjusted successors survives 30 years (SAFEMAX 4.15%).
  Worked: $40,000 / 0.04 = $1,000,000 (rule of 25). Trinity study (Cooley,
  Hubbard, Walz 1998): curator verifies the AAII Journal citation and a
  second worked pair (e.g. $25,000 / 0.04 = $625,000) at author time.
- SSA: benefits replace about 40% of pre-retirement earnings for the
  average/medium worker (long-standing SSA estimate; methodology debated
  in AEI Economics Working Paper 2023-12, cited for scope honesty).
  Worked: $30,000 / $75,000 = 0.40. Planning-need target (~70% of
  pre-retirement income): curator pins a published guidance source at
  author time.
- SSA delayed retirement credits (`ssa.gov` retirement planner):
  8% per year (2/3 of 1% per month) for birth years 1943+, through age 70;
  regulation 20 CFR 404.313. Worked: $2,000 PIA x 3 yr -> $2,480 (124%);
  $2,000 x 4 yr -> $2,640 (132%, FRA-66 cohort).
- IRS Publication 590-B, Table III (Uniform Lifetime Table): age 73 ->
  26.5; age 75 -> 24.6; age 80 -> 20.2. Worked: $500,000 / 26.5 =
  $18,867.92 (age 73); $600,000 / 24.6 = $24,390.24 (age 75).
- Expense coverage closures: $1,000,000 / $40,000 = 25 (rule-of-25 closure
  with the Bengen pair); $625,000 / $25,000 = 25 (Trinity-pair closure).
  Labeled cross-record arithmetic.

Every record carries 2+ references plus boundary/guard-scope checks;
provenance labels distinguish published oracles, cross-family worked
arithmetic, and curator boundary checks (the brief-20 convention).

## Registry orphan survey (all 262 admitted models, 2026-11-04, mode=ro)

Records 2-6 mint 15 new meanings (all absent from `MEANINGS`, verified).
Record 1 reuses four canonical meanings; every existing producer/consumer
context differs from the retirement context (verified full strings):

| meaning | producers | consumers | new record 1 ports bind? |
|---|---|---|---|
| `periodic_payment` | 3 (loan r1/r2, gradient; loan/gradient contexts) | 5 (OAFV, due-PV, due-FV, interest, principal) | no (context differs on all 8) |
| `periodic_rate` | 3 (r/m, 2 schedule adapters) | 12 (loan/annuity/gradient/growing/discount family) | no (context differs on all 15) |
| `period_count` | 0 | 11 (UPV + loan/annuity family) | no (context differs on all 11) |
| `present_value` | 4 (UPV home-A, Gordon, due-PV, growing-PV) | 4 (NPV home-A, lump-sum-FV, loan r1/r2) | no (context differs on all 8) |

The lane orphans zero chains and breaks zero working edges. No new units:
all ports use `USD`, `1`, `periods` (all pre-provisioned; `periods` is
dimensionless by the finance-1 design).

## Records prescribed (batch engineering-finance-retire-b01)

All six are `definition`-kind, r1, with ordered ports where order matters
and substitution-checked inverse notes. Engine check: `+ - * / **` on
dimensionless bases only (record 1 mirrors the admitted due-PV exponent
shape `(1+i)**(-n)`), plus one numeric literal (record 4).

1. `engineering-finance--ordinary-annuity-present-value`: A
   (`periodic_payment`, USD), i (`periodic_rate`, 1), n (`period_count`,
   periods) -> P (`present_value`, USD), expr
   `A*(1-(1+i)**(-n))/i`, guards `A >= 0`, `i > 0`, `n >= 1` (mirrors the
   admitted OAFV guard shape). Context on all ports:
   `same-series:end-of-period-level-withdrawals:fixed-rate:retirement-horizon`.
   Assumptions state end-of-period timing and exclude the i = 0 limit
   branch (`P = A*n`, separate expression per the OAFV precedent).
   Rejections: i = 0 domain case plus missing-input case. References:
   $10,000 x 7.72173 = $77,217.35 (pinned table); due-PV/(1+i) closure;
   n = 1 single-discount identity (`A/(1+i)`).
2. `engineering-finance--required-nest-egg-withdrawal-rate`: W
   (`annual_withdrawal`, USD), s (`safe_withdrawal_rate`, 1) -> N
   (`required_nest_egg`, USD), expr `W / s`, guards `W >= 0`, `s > 0`.
   Assumptions scope the Bengen rule (30-year horizon, inflation-adjusted
   successors, historical-US calibration — the record computes the
   division, it does not certify safety). Rejections: s = 0 domain case
   plus missing-input case. References: $40,000/0.04 = $1,000,000
   (Bengen); $25,000/0.04 = $625,000 (Trinity pair, citation verified at
   author time); s = 1 spend-it-all boundary (`N = W`).
3. `engineering-finance--income-replacement-ratio`: Yret
   (`retirement_income`, USD), Ypre (`preretirement_income`, USD) -> R
   (`replacement_ratio`, 1), expr `Yret / Ypre`, guards `Yret >= 0`,
   `Ypre > 0`. No upper guard: over-replacement (R > 1) is admitted, with
   a guard-scope admission case documenting it. Rejections: Ypre = 0
   domain case plus missing-input case. References: $30,000/$75,000 =
   0.40 (SSA medium worker); $52,500/$75,000 = 0.70 (pinned planning
   target); Yret = 0 boundary.
4. `engineering-finance--delayed-retirement-credit-benefit`: PIA
   (`primary_insurance_amount`, USD), y (`delayed_retirement_years`, 1)
   -> B (`delayed_benefit`, USD), expr `PIA*(1+0.08*y)`, guards `PIA >= 0`,
   `y >= 0`, `y <= 4`. The 0.08 literal is sourced to SSA/20 CFR 404.313
   in assumptions with the 1943+ birth-year and through-age-70 scope;
   cohort FRA (66 vs 67) caps the applicable y and is stated in the port
   contexts. Rejections: y > 4 guard-scope case plus y < 0 domain case.
   References: $2,000 x (1+0.24) = $2,480; $2,000 x (1+0.32) = $2,640;
   y = 0 identity (`B = PIA`).
5. `engineering-finance--required-minimum-distribution`: Bal
   (`prior_year_balance`, USD), L (`rmd_distribution_period`, 1) -> R
   (`required_minimum_distribution`, USD), expr `Bal / L`, guards
   `Bal >= 0`, `L > 0`. Assumptions scope Table III (most account owners;
   spouse-more-than-10-years-younger and beneficiary tables excluded) and
   the Dec-31-prior-year balance convention. Rejections: L = 0 domain
   case plus missing-input case. References: $500,000/26.5 = $18,867.92
   (age 73); $600,000/24.6 = $24,390.24 (age 75); Bal = 0 boundary.
6. `engineering-finance--expense-coverage-multiple`: S
   (`retirement_savings`, USD), W (`annual_expenses`, USD) -> T
   (`expense_coverage_multiple`, 1), expr `S / W`, guards `S >= 0`,
   `W > 0`. Dimensionless years-of-expenses multiple (no return, no
   inflation — assumptions say so). Rejections: W = 0 domain case plus
   missing-input case. References: $1,000,000/$40,000 = 25;
   $625,000/$25,000 = 25 (both labeled rule-of-25 closures); S = 0
   boundary.

## Resubmission shape (for the future curator; nothing submitted now)

Batch `engineering-finance-retire-b01` in `.runs/compat-curation/retire/`:
`validate` on the bundle JSON -> `valid-data-awaiting-review` (6 models;
12+ arithmetic + 12 rejection checks; record 1 runtime-ready on
pre-provisioned vocabulary, 5 requires-extension on new meanings unless
the vocabulary change ships with the batch); `pack` -> return ZIP with
sha256; `validate` on the return ZIP. Commands (central package, offline):
`uv --cache-dir .uv-cache run --no-env-file --offline
-m connected_models.curation validate|pack ...`. The batch must never be
staged or imported by the curator; the registry stays untouched.

Deferred (not prescribed): sinking-fund and lump-sum-PV inverses
(solver-derived), growing-withdrawal PV (growing-annuity-owned),
zero-rate branches (separate expressions per precedent), tax treatment of
distributions (jurisdiction tables, not scalar arithmetic), MACRS/DB
depreciation of retirement-property side topics (no), RMD Table I/II
variants (same division shape as record 5 — one record per shape).
