# Data-center TCO lane brief: xUE efficiency, overhead, downtime cost, depreciation (brief 25)

To: curation review (batch computer-science-dctco-b01, 6 new records)
From: deep-lane brief author (22-25), 2026-11-04
Status: proposed (prescription only — no bundle authored, no registry touched; all reviews stand)

## What this lane adds

Six atomic records for data-center total cost of ownership: the Green Grid
xUE efficiency trio (PUE, WUE, CUE), facility overhead energy, annual
downtime cost from downtime hours and an outage cost rate, and straight-line
annual depreciation. The lane consumes the admitted availability/downtime
vocabulary by meaning (never re-deriving it) and adds the cost and
sustainability layer on top.

All endpoint vocabulary was surveyed read-only (`.registry/models.sqlite3`,
`mode=ro`, all 262 admitted models; never staged, reviewed, admitted, or
otherwise touched). All six lane IDs are absent (no collisions). Every port
carries a per-record DC-TCO context; the one reused meaning
(`annual_downtime`) is context-mismatched against its producer, so the lane
binds no existing chain and forms no in-lane legs (the brief-19 shape).

## Do-not-resubmit boundaries (wave-2 drift guard)

- Availability family (all owned): series/parallel/n-identical/three-leg
  availability, inherent/operational/uptime-ratio availability, MTBF/MTTR/
  MDT pairs, MTBF reciprocal, unavailability complement and the scope
  adapters. No reliability recomputation under TCO labels.
- Annual downtime: `computer-science--annual-downtime-hours@r2` (`U * H`,
  `annual_downtime` [h]). Record 5 CONSUMES `annual_downtime` as an input
  meaning with a new cost-basis context (documented near-miss, no edge);
  it never re-derives `U * H`.
- Electricity cost: `electricity-cost@1` (`energy * tariff`). NO
  data-center-energy-cost record (`E * tariff` with relabeled ports) — that
  composition is left to the solver over the admitted record.
- Cost per server routes through glue: `economics--money-unit-rate@r1`
  (`T / Q`, `counted_unit_quantity` -> `unit_price`) already covers
  TCO-per-server exactly. No per-server/per-rack unit-rate record is
  prescribed; the curator notes the routing.
- TCO summation routes through glue: `economics--total-of-two-money-amounts`
  owns two-input money addition. No `capex + opex` sum record is
  prescribed; future relabel adapters to `named_money_amount` are deferred,
  not prescribed.
- National-accounts depreciation is NOT asset depreciation:
  `economics--current-price-net-domestic-product@r1` (`GDP - CFC`, NIPA
  current-cost CFC) and `economics--constant-price-fixed-capital-stock-balance@r1`
  (`K0 + I - D - O`, Laspeyres economic depreciation) both carry audited
  permitted-use clauses excluding book/tax depreciation binding. Record 6
  is straight-line book depreciation of one asset population with its own
  meanings — distinguished, never bound to CFC/D.
- Money glue otherwise: scaled-money, money-difference, simple-payback
  (`C / A`), NPV (`benefit - investment`). No money restatement.
- Inverse doctrine: `Eit = Et / PUE`, `Et = O + Eit` rearrangements, and
  declining-balance/MACRS-table depreciation (tables/schedules, not one
  scalar relationship) are NOT prescribed.

## Oracle inventory (all numbers verified 2026-11-04 unless flagged)

- The Green Grid: PUE = total facility energy / IT equipment energy
  (2007; now ISO/IEC 30134-2); CUE = CO2e caused by total data-center
  energy / IT equipment energy (Belady et al. 2010, kg/kWh); WUE = annual
  site water / IT equipment energy (Patterson/Belady/Pouchet 2011, L/kWh).
  Ideal values: PUE 1, WUE/CUE 0.
- Uptime Institute Global Data Center Survey: industry-average PUE 1.58
  (2018 and 2023; 1.55-1.59 band since ~2020); 2025 survey 1.54. Worked:
  1.58 kWh / 1 kWh = 1.58; overhead 1.58 - 1 = 0.58 kWh per IT kWh.
  Hyperscale-fleet figure (~1.1): curator verifies a published operator
  figure (e.g. Google Environmental Report) at author time.
- Ponemon Institute / Emerson Network Power 2016 Cost of Data Center
  Outages (63 US organizations): average $8,851/min unplanned outage
  (= $531,060/hr); 2013 edition $7,908/min (= $474,480/hr); 2010 $5,617/min.
  Worked: 2 h x $531,060/hr = $1,062,120.
- EPA eGRID grid carbon intensity for the CUE worked figure (US average
  ~0.34-0.39 kg/kWh class): VERIFY AT AUTHOR TIME — the curator pins the
  current eGRID summary-table value with accessed date; the brief does not
  pin a number it has not seen. Boundary (G = 0) ships regardless.
- IRS Revenue Procedure 87-56, Asset Class 00.12 (Information Systems):
  computers 5-year property (GDS); IRS Publication 946 MACRS. Worked:
  ($10,000 - $0) / 5 = $2,000/yr straight-line. Second authority: GAAP
  ASC 360 systematic allocation via the brief-19 Viewpoint-excerpt
  protocol (asc.fasb.org gated; disclose indirect access).

Every record carries 2+ references plus boundary/guard-scope checks;
provenance labels distinguish published oracles, cross-family worked
arithmetic, and curator boundary checks (the brief-20 convention).

## Registry orphan survey (all 262 admitted models, 2026-11-04, mode=ro)

Records 1-4 and 6 mint 11 new meanings (all absent from `MEANINGS`,
verified). Record 5 reuses one meaning:

| meaning | producers | consumers | edge? |
|---|---|---|---|
| `annual_downtime` | 1 (`annual-downtime-hours@r2`: "same system, stated conditions and accounting year as U") | 0 | no (record 5 input context adds the outage-cost basis, so it differs; the brief-19 payback/`annual_saving` near-miss shape) |

All other lane meanings (`total_facility_energy`, `it_equipment_energy`
shared by records 1-4 as inputs/output with four distinct contexts) are
absent from admitted records. The lane orphans zero chains and breaks zero
working edges. New units for the extension (or requires-extension gaps):
`L/kWh` (dims `(-1,1,2,0,0,0,0)`, scale 0.001), `kg/kWh`
(`(0,-2,2,0,0,0,0)`, scale `1/JOULES_PER_KWH`), `USD/h`
(`(0,0,-1,1,0,0,0)`, scale `1/3600`).

## Records prescribed (batch computer-science-dctco-b01)

All six are `definition`-kind, r1, with ordered ports where order matters
and substitution-checked inverse notes. Engine check: `+ - * /` only.

1. `computer-science--power-usage-effectiveness`: Et
   (`total_facility_energy`, kWh), Eit (`it_equipment_energy`, kWh) -> PUE
   (`power_usage_effectiveness`, 1), expr `Et / Eit`, guards `Et >= 0`,
   `Eit > 0`, `Et >= Eit` (facility meter includes the IT meter; mirrors
   the admitted `Md <= Mt` balance-guard shape). Rejections: Eit = 0
   domain case plus Et < Eit guard-scope case. References: 1.58/1 = 1.58
   (Uptime 2023 average); 1.54/1 = 1.54 (Uptime 2025); Et = Eit ideal
   identity (PUE = 1).
2. `computer-science--water-usage-effectiveness`: W
   (`site_water_consumption`, L), Eit (`it_equipment_energy`, kWh) -> WUE
   (`water_usage_effectiveness`, L/kWh), expr `W / Eit`, guards `W >= 0`,
   `Eit > 0`. Annual site-water scope in assumptions (Green Grid WUE-1
   class; source-energy water excluded). Rejections: Eit = 0 domain case
   plus missing-input case. References: curator-pinned published operator
   site-WUE figure (verify at author time); second published figure or
   1.8 L/kWh worked illustration labeled curator arithmetic; W = 0 ideal
   boundary.
3. `computer-science--carbon-usage-effectiveness`: G
   (`attributable_carbon_emissions`, kg), Eit (`it_equipment_energy`, kWh)
   -> CUE (`carbon_usage_effectiveness`, kg/kWh), expr `G / Eit`, guards
   `G >= 0`, `Eit > 0`. Scope-1+2-from-energy scope in assumptions.
   Rejections: Eit = 0 domain case plus missing-input case. References:
   curator-pinned eGRID-based worked figure (verify at author time);
   0.34 kg / 1 kWh = 0.34 labeled illustration pending the pin; G = 0
   boundary.
4. `computer-science--facility-overhead-energy`: Et
   (`total_facility_energy`, kWh), Eit (`it_equipment_energy`, kWh) -> O
   (`overhead_energy`, kWh), expr `Et - Eit`, guards `Et >= 0`, `Eit >= 0`,
   `Et >= Eit`. Energy (not money) difference — no covered record
   subtracts energies. Rejections: Et < Eit guard-scope case plus
   missing-input case. References: 1.58 - 1 = 0.58 kWh (Uptime closure);
   1.54 - 1 = 0.54 kWh; Et = Eit zero-overhead boundary.
5. `computer-science--annual-downtime-cost`: D (`annual_downtime`, h), c
   (`outage_cost_rate`, USD/h) -> C (`annual_downtime_cost`, USD), expr
   `D * c`, guards `D >= 0`, `c >= 0`. Input context adds the outage-cost
   basis to the downtime scope (recorded near-miss against the
   availability producer — no edge). Rejections: negative-D domain case
   plus missing-input case. References: 2 h x $531,060/hr = $1,062,120
   (Ponemon/Emerson 2016); 1 h x $474,480/hr (2013 edition); D = 0
   boundary.
6. `computer-science--straight-line-annual-depreciation`: C (`asset_cost`,
   USD), S (`salvage_value`, USD), n (`recovery_periods`, periods) -> Dep
   (`annual_depreciation`, USD), expr `(C - S) / n`, guards `C >= 0`,
   `S >= 0`, `C >= S`, `n >= 1` (mirrors the admitted balance-guard
   shapes). Straight-line book scope in assumptions; MACRS 200%-DB
   default and bonus depreciation explicitly excluded. Rejections: C < S
   guard-scope case plus n = 0 domain case. References: ($10,000 - $0)/5
   = $2,000 (5-yr computers, Rev. Proc. 87-56); ($12,000 - $2,000)/5 =
   $2,000 (salvage case); C = S zero-depreciation boundary.

## Resubmission shape (for the future curator; nothing submitted now)

Batch `computer-science-dctco-b01` in `.runs/compat-curation/dctco/`:
`validate` on the bundle JSON -> `valid-data-awaiting-review` (6 models;
12+ arithmetic + 12 rejection checks; record 6 runtime-ready on
pre-provisioned vocabulary, 5 requires-extension on `L/kWh`, `kg/kWh`,
`USD/h` unless the vocabulary change ships with the batch); `pack` ->
return ZIP with sha256; `validate` on the return ZIP. Commands (central
package, offline): `uv --cache-dir .uv-cache run --no-env-file --offline
-m connected_models.curation validate|pack ...`. The batch must never be
staged or imported by the curator; the registry stays untouched.

Deferred (not prescribed): data-center energy cost (electricity-cost-owned
composition), TCO summation (glue-owned; adapters deferred), per-server
unit rates (money-unit-rate-owned), PUE-partial / WUE-source-energy
variants (same shapes as records 1-2 — one record per shape), MACRS tables
(schedules, not scalar), carbon from facility energy (A x EF-owned).
