# Water-use lane brief: flow accumulation, per-capita use, cost, harvest, intensity (brief 23)

To: curation review (batch water-hydraulics-use-b01, 5 new records)
From: deep-lane brief author (22-25), 2026-11-04
Status: proposed (prescription only — no bundle authored, no registry touched; all reviews stand)

## What this lane adds

Five atomic records seeding the empty `water-hydraulics` domain on the
demand/accounting side: volume from flow and duration, per-capita daily use,
water cost from volume and tariff, rainwater harvest volume, and process
water intensity. The lane parallels the environmental-accounting
per-capita and intensity shapes without relabeling them.

All endpoint vocabulary was surveyed read-only (`.registry/models.sqlite3`,
`mode=ro`, all 262 admitted models; never staged, reviewed, admitted, or
otherwise touched). No admitted model carries a water-use meaning (only
clinical fluid volumes with clinical contexts, which are out of scope).
All five lane IDs are absent (no collisions). Every port carries a
per-record context, so the lane binds no existing chain and forms no
in-lane legs (the brief-19 shape).

## Do-not-resubmit boundaries (wave-2 drift guard)

- Clinical fluid arithmetic stays clinical:
  `clinical-arithmetic--mean-volumetric-infusion-rate`,
  `--gravity-infusion-mean-drop-rate`, `--infusion-constituent-mass-rate`
  and the prescribed-volume records. No relabel of infusion/dosing volumes
  or rates under water-use names.
- Waste per-capita stays waste:
  `environmental-accounting--per-capita-generation-from-total-and-population`
  (`Mt / P`, t/person). Record 2 is the water analogue with its own
  meanings and unit — the admitted record is the mirrored shape precedent,
  not a reusable identity.
- Emission intensity stays emissions:
  `environmental-accounting--emission-intensity-from-mass-and-output`
  (`E / Q`, kg/unit). Record 5 is the water analogue with its own meanings
  and unit, same precedent treatment.
- Counts-only money unit rate: `economics--money-unit-rate@r1` (`T / Q`,
  `counted_unit_quantity` input). Cubic meters are physical measures and
  must NOT be submitted as `counted_unit_quantity`. Record 3 carries its
  own tariff meaning and unit.
- Electricity cost: `electricity-cost@1` (`energy * tariff`, kWh basis).
  Record 3 shares the value-times-price shape but is NOT an electricity
  relabel: distinct input/output meanings and a volumetric tariff unit.
- Mass-density-volume: `building-energy--mass-from-density-volume@r1`. No
  water-mass-from-volume record in this lane (that composition is left to
  the solver over the admitted record).
- Inverse doctrine: `Q = V / t`, `t = V / Q`, `P = V / q`, `A = V / (d*e)`
  and all other rearrangements of records 1-5 are solver-derived and are
  NOT prescribed.

## Oracle inventory (all numbers verified 2026-11-04 unless flagged)

- USGS Circular 1441 (Dieter et al., Estimated Use of Water in the United
  States in 2015): domestic per-capita 82 gpcd in 2015, 88 gpcd in 2010.
  Metric: 82 gal = 0.3104 m3; 88 gal = 0.3331 m3 per person per day.
- EPA WaterSense Statistics and Facts (`epa.gov/watersense/statistics-and-facts`):
  82 gal/person/day at home (citing USGS 2015); average family over 300
  gal/day at home (~70% indoors); over $1,000/yr in water costs; over
  $380/yr saveable with WaterSense/ENERGY STAR. Cross-arithmetic: 300 gpd x
  365 = 109,500 gal/yr = 414.5 m3/yr; $1,000 / 414.5 m3 = $2.41/m3 implied.
- UC Agriculture and Natural Resources (rainwater capture): 1 inch of rain
  on 1,000 sq ft yields about 623 gal before collection losses
  (volume = area x depth x 0.623). Metric closure: 92.903 m2 x 0.0254 m
  = 2.3597 m3 = 623.4 gal.
- Texas Water Newsroom / Texas A&M AgriLife: 0.623 gal per sq ft per inch;
  1,000 sq ft x 32 in/yr x 0.623 x 80% efficiency = 15,949 gal/yr
  (about 16,000 gal/yr, pool-filling scale). Independent publisher of the
  same rule plus a worked efficiency case.
- NCSU Extension (Pamlico): 1 inch over 1,000 sq ft produces 623 gal.
  Third publisher of the rule (corroboration, not the formula authority).
- Process intensity figure: VERIFY AT AUTHOR TIME — the curator pins one
  published corporate water-intensity figure (e.g. a beverage maker's
  water-use ratio from its audited sustainability report, or an Intel
  Corporate Responsibility figure) with accessed date; the brief does not
  pin a number it has not seen. Boundary (W = 0) and guard-scope cases
  ship regardless.

Every record carries 2+ references plus boundary/guard-scope checks;
provenance labels distinguish published oracles, cross-family worked
arithmetic, and curator boundary checks (the brief-20 convention).

## Registry orphan survey (all 262 admitted models, 2026-11-04, mode=ro)

All 12 lane meanings are absent from `MEANINGS` (verified); all 3 new units
below are absent from `UNITS`. `water-hydraulics` currently holds zero
admitted models: this lane seeds the domain. Meaning-sharing:

| meaning | shared by | edge? |
|---|---|---|
| `water_volume` | r1 OUT, r3 IN, r5 IN | no (all three contexts differ) |

No lane meaning appears in any admitted record, so the lane orphans zero
chains and breaks zero working edges. New units for the extension (or
requires-extension gaps): `m3/person` (dims `(0,3,0,0,0,0,0)`, scale 1.0 —
person is dimensionless, mirroring the admitted `t/person` pattern),
`USD/m3` (`(0,-3,0,1,0,0,0)`, scale 1.0), `m3/unit`
(`(0,3,0,0,0,0,0)`, scale 1.0, mirroring the admitted `kg/unit` intensity
pattern).

## Records prescribed (batch water-hydraulics-use-b01)

All five are `definition`-kind, r1, with ordered ports where order matters
and substitution-checked inverse notes. Engine check: `+ - * /` only; no
offset-temperature (no water-temperature records in this lane).

1. `water-hydraulics--water-volume-from-flow-and-duration`: Q
   (`volumetric_flow`, m^3/s), t (`flow_duration`, s) -> V (`water_volume`,
   m3), expr `Q * t`, guards `Q >= 0`, `t >= 0`. Context: same conveyance,
   flow regime and interval as Q, t and V. Rejections: negative-Q domain
   case plus missing-input case. References: 0.05 m3/s x 3,600 s = 180 m3
   (stipulated municipal-pump rating, curator pins a published pump/EPA
   figure at author time); 100 gpm x 2 h = 12,000 gal = 45.42 m3
   (unit-closure row); Q = 0 boundary.
2. `water-hydraulics--per-capita-daily-water-use`: V (`water_volume`, m3),
   P (`served_population`, person) -> q (`per_capita_daily_water_use`,
   m3/person), expr `V / P`, guards `V >= 0`, `P > 0`. Context: same
   served population, day and delivery boundary as V, P and q. Mirrors the
   admitted waste per-capita shape with water meanings. Rejections: P = 0
   domain case plus missing-input case. References: 0.3104 m3 / 1 =
   0.3104 m3/person (USGS 2015, 82 gpcd); 0.3331 m3 / 1 (USGS 2010,
   88 gpcd, vintage-independent recomputation); V = 0 boundary.
3. `water-hydraulics--water-cost-from-volume-and-tariff`: V
   (`water_volume`, m3), p (`water_tariff`, USD/m3) -> C (`water_cost`,
   USD), expr `V * p`, guards `V >= 0`, `p >= 0`. Context: same account,
   billing interval and tariff schedule as V, p and C. Rejections:
   negative-V domain case plus missing-input case. References: 414.5 m3 x
   $2.41/m3 = $999.00 (EPA WaterSense family cross-arithmetic, labeled as
   such); curator pins one published utility volumetric tariff at author
   time for the second oracle; V = 0 boundary.
4. `water-hydraulics--rainwater-harvest-volume`: A (`catchment_area`, m2),
   d (`rainfall_depth`, m), e (`collection_efficiency`, 1) -> V
   (`harvested_rainwater`, m3), expr `A * d * e`, guards `A >= 0`,
   `d >= 0`, `e >= 0`, `e <= 1`. Context: same catchment, storm/event and
   collection system as A, d, e and V. Rejections: e > 1 guard-scope case
   plus missing-input case. References: 92.903 m2 x 0.0254 m x 1 =
   2.3597 m3 (UC ANR 0.623 rule); 92.903 x 0.8128 (32 in) x 0.8 =
   60.41 m3 = 15,959 gal (Texas Water 80% case); e = 0 boundary (no
   capture).
5. `water-hydraulics--process-water-intensity`: W (`water_volume`, m3), Q
   (`product_output`, unit) -> I (`water_intensity`, m3/unit), expr
   `W / Q`, guards `W >= 0`, `Q > 0`. Context: same facility, process,
   accounting interval and output counting basis as W, Q and I. Mirrors
   the admitted emission-intensity shape with water meanings. Rejections:
   Q = 0 domain case plus missing-input case. References: curator-pinned
   published corporate intensity figure (verify at author time, see
   oracle inventory); second published figure or industry-benchmark
   cross-check; W = 0 boundary (dry process).

## Resubmission shape (for the future curator; nothing submitted now)

Batch `water-hydraulics-use-b01` in `.runs/compat-curation/water/`:
`validate` on the bundle JSON -> `valid-data-awaiting-review` (5 models;
10+ arithmetic + 10 rejection checks; record 1 runtime-ready on
pre-provisioned vocabulary, 4 requires-extension on `m3/person`, `USD/m3`,
`m3/unit` unless the vocabulary change ships with the batch); `pack` ->
return ZIP with sha256; `validate` on the return ZIP. Commands (central
package, offline): `uv --cache-dir .uv-cache run --no-env-file --offline
-m connected_models.curation validate|pack ...`. The batch must never be
staged or imported by the curator; the registry stays untouched.

Deferred (not prescribed): water mass from volume (solver composes the
admitted density record), fixture/shower event volumes (same `Q * t` shape
as record 1 — no second record for one shape), leak-loss volumes (same
shape), storage-tank balances (mass-balance family, future lane), water
temperature mixing (offset-temperature risk — excluded by lane rule),
time-varying tariffs (series, not scalar).
