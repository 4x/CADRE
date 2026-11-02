---
id: finding-wave2-intake-axes-blocked
type: finding
title: 'Wave-2 intake: 8 admitted, thermal/circuits blocked on dimension axes'
summary: Reviewers V/W/X/Y cleared 31 wave-2 records (24 recommend-admit). Runtime 0.20.0 be-1 vocabulary
  admitted 8 (3 mechanics, 5 building-energy); registry 90->98; 7 legacy runs replay exact. Constant-power
  r1 failed projection (inlined /1000, briefed for r2). Two mech r1s are a byte-identical re-delivery of the M2 batch (same record SHAs), already admitted (staged,
  never published). Five thermal records (sensible-heat, carnot-heating, b04 x3) need a temperature
  axis; 8 circuits records need current (V/A/ohm/C/S) and one needs amount (mol); temperature-difference
  vs absolute-temperature semantics unresolved. Axis extension is now the binding constraint; see [[question-dimensional-and-unit-type-system]].
status: active
created: '2026-11-01'
updated: '2026-11-01'
topics:
- engine
- vocabulary
- lifecycle
confidence: null
relations: []
---

# Wave-2 intake: 8 admitted, thermal/circuits blocked on dimension axes

## Finding

Wave-2 review is nearly complete (31/37 records across V/W/X/Y; circuits b03/b04
still queued) and intake admitted everything the 4-axis engine can express: 8
new eligible models, registry 90 -> 98. The remaining 16 recommend-admit records
are all vocabulary-blocked on missing dimension axes, not on science:

- 5 thermal records need temperature (sensible-heat, carnot-heating,
  carnot-cooling, series-thermal-resistance, net-radiative-exchange).
- 8 circuits records need electric current (V, A, ohm, C, S units).
- 1 circuits record (carrier-density, b04, unreviewed) additionally needs
  amount-of-substance (mol).


## Basis

- Review JSONs in `data/curation/reviews/` (V: be-a-b01 + muse-b01; W: be-a-b02
  + be-a-b03; X: be-a-b04 + mech-a-b01; Y: circuits b01 + b02).
- Runtime 0.20.0 be-1 vocabulary (`W`, `Btu`, `Btu/Wh`, `m3`, `kg/m3`, `J/kg`;
  14 meanings) with `tests/test_runtime.py::test_building_energy_scales_close_algebra`.
- Staging transcripts: 10/11 projections staged; constant-power failed reference
  replay (canonical-expression violation, r2 briefed); 2 mech duplicates of
  wave-1 admissions left staged-not-published (registry guard forbids a second
  candidate review row for the same key).
- 7/7 legacy runs replay exact; 108/108 tests green.


## Implications

- Dimension-axis extension (temperature, current, amount) is the binding
  constraint for thermodynamics, materials-science, circuits, and thermal
  building-energy lanes. See [[question-dimensional-and-unit-type-system]].
- Temperature carries a semantic trap: absolute temperatures (K) vs differences
  (dT) need distinct handling; no silent remap onto existing axes.
- Curator-facing: `kg/m^3` (circuits b04) vs registry `kg/m3` unit-string
  mismatch needs an alias policy or r2.


## Limitations / uncertainty

- Axis migration approved and shipped, digest-safe (models hash strings, not
vectors): see [[decision-seven-axis-dimension-migration]]. 11 of the 16 queued
records admitted (registry 109); radiative needs a sigma-input r2,
average-current a duration-rename r2, constant-power r2 still owed,
carrier-density still unreviewed.
