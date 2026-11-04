# Slice A — building-energy + classical-mechanics ingestion report

Reviewer: `ingest-energy-mech`. Date: 2026-11-04. All commands offline (`--no-env-file`); no `.env` access; no worker scripts run; no commits/branches (parent commits).

## Counts

- Zips in slice: 6. Records total: 23.
- Validate: 6/6 `valid-data-awaiting-review`, all `requires-extension`, 2-3 arithmetic + 1-2 rejection checks each.
- Import: 5/6 staged (`staged-not-published`, 19 candidates); 1/6 blocked (see muse-b01).
- New admissions: 0. Already admitted (verified, untouched): 16 records across 16 eligible projections. Rejected with documented reasons: 7 (3 staged r1s + 4 unstaged muse r1s).
- Registry `review` writes: 0 — the tool refuses model-less r1 candidates (see surprise 1), and re-reviewing admitted projections would clobber historical attribution. All verdicts below are the recorded decisions.
- Lock-retry incidents: 0. No `database is locked` encountered on any write.

## Batch results

### building-energy-a-b01 (batch 06c0f260..., curator buffy) — staged, 2 verified + 2 rejected

- `constant-power-electricity-consumption@r1` (a2ac0204) — VERIFIED ADMITTED. Eligible via `@r2.runtime1` (revAR recommend-admit, dev-intake 2026-11-03, replay passed). This r1 won the contested ID over muse-b01 (record SHA a217751e vs muse 63033a6f).
- `sensible-heat-no-phase-change@r1` (6675bc92) — VERIFIED ADMITTED. Eligible `@r1.runtime1` (reviewer-V recommend-admit, dev-intake 2026-11-02, replay passed).
- `steady-conduction-plane-slab-rate@r1` (99fc8be9) — REJECTED. Science verified offline by recomputation: P=kA dT/L, oracles 46.55 W (exp 46.6, tol 0.1) and 13.30 W (exp 13.3, tol 0.05) both in tolerance, inverse dT=35 exact, dimensions/guards/rejections/scope pass. Blocker: UP2 source license claims CC BY 4.0 with commercial reuse, contradicted by independent live-preface inspections (reviewer V, 2026-11-01) finding CC BY-NC-SA 4.0. r1 is immutable; needs curator r2 with corrected license + refreshed version label.
- `plane-layer-thermal-resistance@r1` (64bb20b4) — REJECTED. Same verdict pattern: R=L/k, oracles 0.003125 (exp 0.00313, tol 1e-5) and 0.00113636 (exp 0.00114, tol 1e-5) in tolerance; same UP2 CC BY vs BY-NC-SA rights block; needs curator r2.

### building-energy-a-b02 (batch 76bfcd9e...) — staged, 3 verified + 1 rejected

- `heat-pump-coefficient-of-performance@r1`, `seasonal-heating-performance-hspf@r1`, `mass-from-density-volume@r1` — VERIFIED ADMITTED (`@r1.runtime1` eligible; reviewer-W recommend-admit).
- `absolute-thermal-resistance-layer@r1` (8a3cb4b6) — REJECTED. Rth=L/(kA), oracles 39.8089 (exp 39.81, tol 0.05) and 14.4760 (exp 14.48, tol 0.05) recomputed in tolerance; dims K/W close; same UP2 license block (reviewer W live-inspected BY-NC-SA); needs curator r2.

### building-energy-a-b03 (batch f541a8ec...) — staged, 3 verified

- `latent-heat-phase-change`, `refrigerator-coefficient-of-performance`, `carnot-heating-cop-limit` — all VERIFIED ADMITTED (`@r1.runtime1`; reviewer-W recommend-admit).

### building-energy-a-b04 (batch 33649ddc...) — staged, 3 verified

- `series-thermal-resistance-sum`, `carnot-cooling-cop-limit` — VERIFIED ADMITTED (`@r1.runtime1`; reviewer-X recommend-admit).
- `net-radiative-exchange-gray-surface@r1` — VERIFIED ADMITTED via `@r2.runtime1` (revAR recommend-admit; r2 carries the sigma-input fix).

### building-energy-muse-b01 (curator muse-spark, kit .1) — NOT staged, 4 rejected

- Import fails atomically: `constant-power-electricity-consumption@r1: changed content under an existing revision` (known fleet collision; a-b01 holds the ID). Nothing from this batch staged — confirmed by absence from the registry review report.
- All 4 records independently REJECTED on substance too (reviewer V: 5/6 checks passed, rights-provenance failed on the same UP2 CC BY misstatement; `auditing validate` confirms the V review binds this exact zip):
  - `constant-power-electricity-consumption@r1` — same science as the admitted r2 lineage; contributes nothing new.
  - `sensible-heat-demand@r1` (m*c*dT) — duplicates admitted `sensible-heat-no-phase-change`.
  - `steady-conduction-heat-rate@r1` (kA dT/d) — duplicates pending `steady-conduction-plane-slab-rate@r1`.
  - `conduction-thermal-resistance@r1` (d/(kA)) — duplicates pending `absolute-thermal-resistance-layer@r1`.
- Net: zero new lanes; do-not-resubmit stands. If a canonical choice is ever revisited, V's note applies: muse-b01 rests on one primary + one published oracle vs a-b01's two primaries + two oracles.

### classical-mechanics-a-b01 (batch e9b3abfe...) — staged, 5 verified

- All 5 (`translational-kinetic-energy`, `constant-acceleration-displacement`, `velocity-after-constant-acceleration`, `gravitational-potential-energy-difference`, `collinear-constant-force-work`) VERIFIED ADMITTED (`@r1.runtime1`; reviewer-X 5/5 recommend-admit, dev-intake, replay passed). Note: the canonical codex review says needs-revision on kinetic/grav-pe/work, but admission followed the X review — a prior dev decision, not revisited here.

## Prior-review checks performed

- `auditing validate` passes for all 6 zips against committed `data/curation/reviews/*-review.json` (V, W, X, codex, plus mech review-x) — prior reviews cryptographically bind these exact zips.
- Worker audit artifacts (`QUALITY-AUDIT.json`, `NUMERICAL-REVIEW.json`, `QUANTITY-REVIEW.json`, `MODEL-DETAILS.md`, `FORMULA-INDEX.md`) contain ZERO coverage of building-energy/classical-mechanics — they serve other slices. Noted, not used.
- No `integration` runs: all integration-eligible records are already admitted (re-running risks duplicate projection writes); rejected records are not recommend-admit so integration is inapplicable. No `auditing packet` written: no separate reviewer handoff needed; prior reviews already bind.

## Surprises and dead ends

1. `connected-models review --decision rejected` cannot record decisions on requires-extension r1 candidates: `review()` validates `candidate.model` for every decision, and r1s carry `model: null` (`Invalid object fields; required: assumptions, expression, guards, id, inputs, output, source, version` — confirmed in `src/connected_models/registry.py` review()). So r1 rejections are report-only by tool design; r2s arrive as new candidates unaffected. Same limitation would hit `withdrawn`.
2. Slice was 16/23 pre-admitted (registry at 282 eligible). Real work was the 7 rejections + verification, not new admissions.
3. `$env:TEMP` did not persist across shell calls (sandbox); workdir `ingest-notes/slice-a-work/` holds reglist.json, validation receipts, and the review-bundle pointer instead.

## Unresolved / for parent

- Curator r2s needed for: steady-conduction-plane-slab-rate, plane-layer-thermal-resistance, absolute-thermal-resistance-layer (license-only fixes). No r2 brief exists yet for these three (nbe-c01 covered only constant-power + net-radiative).
- muse-b01 reconciliation: batch can never import under current IDs (1 hard conflict + 3 same-science overlaps). Suggest explicit do-not-resubmit closure rather than a correction brief, since all four overlap admitted/pending lineages.
- Tool gap (optional): allow `review --decision rejected` on model-less candidates so r1 rejections are registry-recorded, not just report-recorded.

---

# PIVOT — zip slice halted, CFA-L3 assignment (parent order, 2026-11-04)

Zip-slice work above is complete as far as the tools allow and is preserved unchanged. Already imported from the zip slice: be-a-b01, be-a-b02, be-a-b03, be-a-b04, classical-mechanics-a-b01 (19 candidates, staged-not-published); muse-b01 import blocked on the known r1 ID collision (nothing staged). No further zip-slice commands run after the pivot.

## CFA-L3 scope

28 dirs `from-offline-curation-workers/financial-analysis-cfa-l3-*` (v1-b01..b08, v2-b01..b07, v3-b01..b06, v4-b01..b07), curator buffy, kit 2026-10-31.9, 115 records, all r1. Each dir holds bundle.json ONLY — no validation-log.json exists (parent expected them; discrepancy noted). No committed reviews exist; this is first review. pmem preflight: no prior financial-analysis curation knowledge. Registry namespace clean (no `financial-analysis--` IDs eligible yet).

## Counts

- Validate: 28/28 `valid-data-awaiting-review`; 114 requires-extension + 1 blocked (see below).
- Import: 28/28 `staged-not-published`, 115 candidates, zero ID conflicts, zero locks.
- Independent oracle recomputation (own AST evaluator, `slice-a-work/recompute_cfa.py`): 232/232 in tolerance, 0 mismatches.
- Full read-through: all 115 record cores (expression, original equation, translation notes, oracles, guards, rejections, inverses, assumptions).
- Reviews authored: 28 review JSONs as `ingest-energy-mech` (`slice-a-work/reviews/*-review-ingest-energy-mech.json`); `auditing validate` 28/28 pass.
- Verdicts: 0 recommend-admit (offline: no live source access, honestly not-checked), 3 needs-revision (specific curator defects), 112 blocked (111 clean pending live verification + 1 with defects).
- Registry `review` writes: 0 — tool refuses model-less candidates (demonstrated live, same gate as zip slice). Integration: refused live with "Scientific reviewer did not recommend this record for admission" (correct — no recommend-admit issued). No admission-track writes exist for this material yet.

## Per-batch verdicts

v1-b01: 4 blocked (Grinold-Kroner, RE long-run, RE finite-horizon, mean-variance utility — all canonical forms matched, 8/8 oracles recomputed). v1-b02: 4 blocked (Singer-Terhaar blend, CAPM beta, building-block FI, saving-investment identity). v1-b03: 4 blocked (ST integrated, ST segmented, pension surplus, funding ratio). v1-b04: 4 blocked (surplus objective, safety-first, ARCH(1), risk parity). v1-b05: 4 blocked (Taylor rule, 120-age, 1/N, shrinkage). v1-b06: 4 blocked (SML, corridor lo/hi, surplus return). v1-b07: 3 blocked (credit spread, 100-age, ARCH unconditional). v1-b08: 5 blocked (FX building-block Eq9, after-tax return/vol/range/account-value). v2-b01: 5 blocked (HHI, effective-N, current yield, rolldown, rolling yield). v2-b02: 5 blocked (duration-convexity, spread-convexity, FI E(R) build, levered return, repo interest). v2-b03: 5 blocked (5 after-tax FVIF siblings). v2-b04: 4 blocked + 1 blocked-with-defects (tax drag, human capital, balance-sheet pair clean; domestic-currency-return-compounding blocked, see below). v2-b05: 5 blocked (bank Eqs 3/4/7/8/9). v2-b06: 3 blocked (quoted/effective spreads). v2-b07: 3 blocked (VWAP, VWAP cost, avg effective spread). v3-b01: 5 blocked (portfolio sum, BHB alloc/alloc-total/select/select-total). v3-b02: 5 blocked (BHB interact/interact-total, BF alloc, Carhart, excess). v3-b03: 4 blocked (Sortino, semivariance, up/down capture). v3-b04: 5 blocked (capture ratio, gain-to-offset, max DD, style, active). v3-b05: 4 blocked (fee leg, net active, fee kink, monthly net). v3-b06: 4 blocked (subperiod TWR, linked TWR, Dietz, composite). v4-b01: 5 blocked (covered-call pair, bull-spread triple). v4-b02: 2 blocked + 1 needs-revision (bear breakeven/max-loss clean; collar-flat-region-profit needs-revision). v4-b03: 3 blocked + 2 needs-revision (swap notional, BPVP, BPVT clean; bpv-futures-hedge-count and equity-futures-count needs-revision). v4-b04: 4 blocked (domestic-currency-return WITH corroboration, invoice, risk-free-asset risk, two-asset variance). v4-b05: 3 blocked (TRS pair, partial-hedge blend). v4-b06: 2 blocked (FX quote, semiannual accrual). v4-b07: 3 blocked (implied FFE, hike probability, locked rate).

## Records needing curator action (4)

1. `collar-flat-region-profit@r1` (v4-b02) — NEEDS-REVISION. Cap-profit oracle method is an unreplaced placeholder ("Placeholder replaced below."). Arithmetic is right (17-12-1.46+1.44=4.98); only the method text is missing. Fix: write the substitution route, resubmit.
2. `bpv-futures-hedge-count@r1` (v4-b03) — NEEDS-REVISION. Domain rejection case cites guard `c != 0`, but the guards list is empty. Fix: declare the guard or reword the case, resubmit.
3. `equity-futures-count@r1` (v4-b03) — NEEDS-REVISION. Same defect class: cites `f != 0`, guards empty. Same fix.
4. `domestic-currency-return-compounding@r1` (v2-b04) — BLOCKED. Curator self-declared status=blocked with unresolved corroboration gap (PDF-only, no accessible corroboration found; honest). Additionally a same-science duplicate of v4-b04 `domestic-currency-return` (same RDC formula, which HAS accessible corroboration + 2 published oracles). Needs canonical-choice reconciliation at consolidation, not a silent merge. No curator dishonesty — the gap was disclosed.

Defect-class scans (placeholder markers; rejection cases citing undeclared guards) confirm these are the only instances across all 115.

## Observations (non-blocking)

- Rights hygiene is GOOD: CFA PDFs cited as project-derivation with "no redistribution", equation-shape-only use; 125 web sources honestly labeled "terms unknown" with no invented clearance; a few real licenses (CC BY-SA wikipedia, CC BY-NC-SA SUNY, US public domain Fed/CRS). No UP2-style overstatement anywhere. My rights-provenance is still not-checked (offline, live terms uninspected) — verification gap, not curator defect.
- Pack convention: money-denominated ports use unit `1`/dimensionless with currency prose ("unit 1 by pack convention"); a few records use USD. Documented and consistent math, but projection-time relabeling to currency units will be needed. Noted per-record in review evidence where present.
- 11 records state guards with only missing-input rejection cases (no domain case live-fires the guard); inverses still analyzed. Noted per-record, non-blocking per be precedent.
- HHI nasdaq oracle method text has a corrupted fragment ("0.38A?") from encoding; inputs/arithmetic exact (0.04+0.0004=0.0404). Cosmetic; suggest cleanup at next revision.
- Upside-capture guard (rb > 0) deliberately tightens the source's >= 0 (division by zero); documented. Fine.

## Lock incidents, unresolved, next steps

- Lock incidents: 0 across 28 imports + 2 probe refusals.
- Unresolved: (a) all 111 clean records need a NETWORKED reviewer to open the cited PDF passages/web pages and confirm source-fidelity + rights before any recommend-admit; my review JSONs are validated first-review evidence, not admission tickets. (b) 3 needs-revision r2s owed by curator. (c) Canonical choice: v2 compounding vs v4 domestic-currency-return. (d) Runtime vocabulary extension for finance quantities is the admission-track gate after review (all records requires-extension).
- Workdir files: `slice-a-work/reviews/` (28 review JSONs), `import-*.json` (28 receipts), `recompute_cfa.py` (232/232), `build_reviews.py`, `scan_defects.py`, `scan_coverage.py`, `dump_cores.py`, `core-v{1,2,3,4}.txt`, `cfa-expressions.txt`, `reglist.json`. Parent decides what (if anything) graduates to `data/curation/reviews/` — I did not touch `data/`.

## Parent placement note (2026-11-04)
The 28 review JSONs this report locates at ingest-notes/slice-a-work/reviews/ (*-review-ingest-energy-mech.json) were moved to data/curation/reviews/<batch-id>-review.json (filenames normalized, content untouched) with matching <batch-id>-bundle.json copies from from-offline-curation-workers/. Verified 181 review JSONs + 181 bundles, zero missing, before the single ingestion commit.
