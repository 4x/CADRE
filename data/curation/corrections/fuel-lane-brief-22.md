# Fuel/energy lane brief: vehicle fuel use, fuel energy, conversion efficiency (brief 22)

To: curation review (batch environmental-accounting-fuel-b01, 6 new records)
From: deep-lane brief author (22-25), 2026-11-04
Status: proposed (prescription only — no bundle authored, no registry touched; all reviews stand)

## What this lane adds

Six atomic records covering vehicle fuel consumption and fuel-energy
accounting: measured fuel economy, trip fuel cost, fuel chemical energy from
mass and heating value, thermal conversion efficiency, rated driving range,
and fuel cost per distance. The lane is measurement- and planning-facing; it
does not touch combustion chemistry, emissions, or mass balances, which are
covered elsewhere.

All endpoint vocabulary was surveyed read-only (`.registry/models.sqlite3`,
`mode=ro`, all 262 admitted models; never staged, reviewed, admitted, or
otherwise touched). All six lane IDs are absent (no collisions). Every port
carries a per-record context, so the lane binds no existing chain and forms
no in-lane legs: all meaning-sharings below are context-mismatched
near-misses by construction (the brief-19 shape).

## Do-not-resubmit boundaries (wave-2 drift guard)

The following covered relationships must NOT be re-curated under fuel-lane
labels. Each names the admitted record that already owns the relationship:

- Fuel mass balance: `environmental-accounting--fuel-burned-from-purchase-and-inventory@r1`
  (`FuelP + FuelST - FuelSE`). No purchase/inventory/burned variants.
- Feedstock exclusion: `environmental-accounting--combustion-fuel-after-feedstock-exclusion@r1`
  (`FuelP - FuelF`). No further fuel-mass partitions.
- Activity-times-factor emissions: `environmental-accounting--emission-mass-from-activity-and-factor@r1`
  (`A * EF`, kg basis). In particular this lane prescribes NO volumetric
  emission-factor record (`V * EFvol`); a kg/gal-factor variant would be a
  re-curation of `A * EF` with relabeled ports.
- Mass-density-volume and its inverses: `building-energy--mass-from-density-volume@r1`
  (`rho * V`). `V = m / rho` and `rho = m / V` are solver-derived; never
  prescribed as records.
- Electricity analogues: `building-energy--constant-power-electricity-consumption@r2`
  (`P * t`), `electricity-cost@1` (`energy * tariff`), `heat-to-electricity@1`.
  No kWh/tariff relabels under fuel names.
- Counts-only money unit rate: `economics--money-unit-rate@r1` (`T / Q`,
  `counted_unit_quantity` input). Gallons are physical measures, so they
  must NOT be submitted as `counted_unit_quantity`. Record 6 below is the
  physical-measure sibling that brief 19 explicitly deferred ("would need
  its own meaning and record") — own input/output meanings, own unit.
- Cooling-cycle performance: heat-pump/refrigerator COP and Carnot-bound
  records. Record 4 is fuel-to-work efficiency only (`W / Q`, guarded
  `W <= Q`); no COP/Carnot restatement.
- Money glue: `economics--total-of-two-money-amounts`,
  `economics--scaled-money-amount`, `economics--money-difference-first-minus-second`.
  No money rescaling, summation, or differencing under fuel labels.
- Inverse doctrine: `V = D / e` and `D = e * V` with trip semantics are
  rearrangements of record 1 and are NOT prescribed (the solver derives
  them). Record 5 differs by input semantics (rated tank volume to rated
  range — planning, not measurement) and is prescribed once, with that
  distinction in its assumptions.

## Oracle inventory (all numbers verified 2026-11-04)

- fueleconomy.gov (EPA): 2024 Toyota Camry LE/SE — 28 city / 39 hwy /
  32 combined mpg (`Find.do?action=sbs&id=47090`); Camry Hybrid SE/XLE/XSE —
  44 / 47 / 46 combined (`id=47093`). Economy oracles use combined figures.
- EIA Gasoline and Diesel Fuel Update (`eia.gov/petroleum/gasdiesel/`):
  U.S. regular $4.153/gal week ending 11/02/26, $4.269/gal week ending
  10/26/26. Price oracles pin the week.
- EIA Monthly Energy Review Appendix A: gasoline blendstock 5.222 MMBtu/bbl
  = 124,340 Btu/gal (2007 forward). Cross-checks the GREET HHV row.
- Argonne GREET via the Hydrogen Analysis Resource Center heating-values
  table (conventional gasoline): LHV 116,090 Btu/gal, 18,679 Btu/lb,
  43.448 MJ/kg; HHV 124,340 Btu/gal; density 2,819 g/gal. Density closure:
  2.819 kg/gal x 43.448 MJ/kg = 122.48 MJ/gal against 116,090 Btu/gal x
  1055.06 J/Btu = 122.48 MJ/gal.
- EIA Electric Power Annual Table 8.1, 2025 operating heat rates
  (`eia.gov/electricity/annual/html/epa_08_01.html`): coal 10,647, petroleum
  10,969, natural gas 7,781, nuclear 10,443 Btu/kWh; perfect plant
  3,412 Btu/kWh. Efficiency oracles are curator inversions
  (eta = 3412 / heatrate): gas 0.4386, coal 0.3205, labeled cross-family
  arithmetic.
- AAA "Your Driving Costs" per-mile scope: cited for the cost-per-distance
  measurement scope only; the curator verifies the current edition's fuel
  cost-per-mile figure at author time and pins it, or ships EIA/EPA
  cross-arithmetic oracles only.

Every record carries 2+ references plus boundary/guard-scope checks;
provenance labels distinguish published oracles, cross-family worked
arithmetic, and curator boundary checks (the brief-20 convention).

## Registry orphan survey (all 262 admitted models, 2026-11-04, mode=ro)

All 13 lane meanings are absent from `MEANINGS` (verified); all 3 new units
below are absent from `UNITS`. In-lane meaning-sharing (all context-mismatched,
zero legs):

| meaning | shared by | edge? |
|---|---|---|
| `trip_distance` | r1 IN, r6 IN (both inputs) | no (inputs only, contexts differ) |
| `trip_fuel_volume` | r1 IN, r2 IN (both inputs) | no (inputs only, contexts differ) |
| `fuel_economy` | r1 OUT, r5 IN | no (contexts differ) |
| `trip_fuel_cost` | r2 OUT, r6 IN | no (contexts differ) |

No lane meaning appears in any admitted record, so the lane orphans zero
chains and breaks zero working edges. New units for the extension (or
requires-extension gaps): `mi/gal` (dims length-volume^-1^-style
`(0,-2,0,0,0,0,0)`, scale `METERS_PER_MILE/CUBIC_METERS_PER_GALLON`),
`USD/gal` (`(0,-3,0,1,0,0,0)`, scale `1/CUBIC_METERS_PER_GALLON`),
`USD/mi` (`(0,-1,0,1,0,0,0)`, scale `1/METERS_PER_MILE`).

## Records prescribed (batch environmental-accounting-fuel-b01)

All six are `definition`-kind, r1, with ordered ports where order matters
and substitution-checked inverse notes. Engine check: `+ - * /` only.

1. `environmental-accounting--vehicle-fuel-economy`: D (`trip_distance`,
   mi), V (`trip_fuel_volume`, gal) -> e (`fuel_economy`, mi/gal), expr
   `D / V`, guards `D >= 0`, `V > 0`. Context: same vehicle, fuel, trip
   and distance/volume basis as D, V and e. Rejections: V = 0 domain case
   plus missing-input case. References: 320 mi / 10 gal = 32 mpg (Camry
   combined); 460 mi / 10 gal = 46 mpg (Camry hybrid); D = 0 boundary.
2. `environmental-accounting--trip-fuel-cost`: V (`trip_fuel_volume`, gal),
   p (`fuel_unit_price`, USD/gal) -> C (`trip_fuel_cost`, USD), expr
   `V * p`, guards `V >= 0`, `p >= 0`. Rejections: negative-V domain case
   plus missing-input case. References: 10 gal x $4.153 = $41.53 (EIA week
   11/02/26); 15 gal x $4.269 = $64.04 (week 10/26/26); p = 0 boundary.
3. `environmental-accounting--fuel-energy-from-mass-and-heating-value`:
   m (`fuel_mass`, kg), LHV (`lower_heating_value`, J/kg) -> E
   (`fuel_chemical_energy`, J), expr `m * LHV`, guards `m >= 0`, `LHV > 0`.
   LHV-basis scope in assumptions (HHV figures must use the HHV row, not
   this record's LHV ports). References: 10 kg x 43.448 MJ/kg = 4.3448e8 J
   (GREET gasoline LHV); 18,679 Btu/lb = 43.448 MJ/kg unit-closure row;
   m = 0 boundary.
4. `environmental-accounting--thermal-conversion-efficiency`: W
   (`useful_work_output`, J), Q (`heat_input`, J) -> eta
   (`thermal_efficiency`, 1), expr `W / Q`, guards `W >= 0`, `Q > 0`,
   `W <= Q` (first-law fail-closed; mirrors the admitted `Md <= Mt`
   balance-guard shape). Rejections: Q = 0 domain case plus W > Q
   over-unity case. References: 3412/7781 = 0.4386 (EIA 2025 gas fleet);
   3412/10647 = 0.3205 (EIA 2025 coal fleet); W = Q = 1 perfect-engine
   limit identity.
5. `environmental-accounting--driving-range-from-economy-and-tank`: e
   (`fuel_economy`, mi/gal), Vt (`tank_fuel_volume`, gal) -> R
   (`vehicle_range`, mi), expr `e * Vt`, guards `e > 0`, `Vt >= 0`.
   Assumptions state the rated-planning scope (rated economy x usable tank),
   distinguishing record 1's measured-trip scope. Rejections: e = 0 domain
   case plus missing-input case. References: 32 mpg x 10 gal = 320 mi
   (stipulated partial fill on the EPA figure); 46 mpg x 10 gal = 460 mi;
   curator verifies the Camry tank specs (15.8 / 13.2 gal class) at author
   time for a rated-range oracle or ships stipulated-fill arithmetic only.
6. `environmental-accounting--driving-fuel-cost-per-distance`: C
   (`trip_fuel_cost`, USD), D (`trip_distance`, mi) -> c
   (`driving_fuel_cost_per_distance`, USD/mi), expr `C / D`, guards
   `C >= 0`, `D > 0`. The brief-19-deferred physical-measure sibling of
   the counts-only money unit rate; assumptions cite that boundary.
   Rejections: D = 0 domain case plus missing-input case. References:
   $41.53 / 320 mi = $0.1298/mi; $64.04 / 460 mi = $0.1392/mi
   (EIA weeks x EPA figures); C = 0 boundary.

## Resubmission shape (for the future curator; nothing submitted now)

Batch `environmental-accounting-fuel-b01` in `.runs/compat-curation/fuel/`:
`validate` on the bundle JSON -> `valid-data-awaiting-review` (6 models;
12+ arithmetic + 12 rejection checks; 3 records runtime-ready on
pre-provisioned units, 3 requires-extension on `mi/gal`, `USD/gal`,
`USD/mi` unless the vocabulary change ships with the batch); `pack` ->
return ZIP with sha256; `validate` on the return ZIP. Commands (central
package, offline): `uv --cache-dir .uv-cache run --no-env-file --offline
-m connected_models.curation validate|pack ...`. The batch must never be
staged or imported by the curator; the registry stays untouched.

Deferred (not prescribed): volumetric emission factors (covered-shape
exclusion), L/100km consumption (reciprocal of record 1 — solver-derived),
annual fuel cost (money scaling — glue-owned), tank-refill mass balances
(fuel-burned-owned), time-varying fuel prices (series, not scalar).
