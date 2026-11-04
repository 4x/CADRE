# Slice D — waves-and-optics-codex b01–b09 ingestion report

Reviewer: `ingest-optics`. Date: 2026-11-04. All commands offline (`--no-env-file`); no branches, commits, or stages; no worker scripts run or imported.

## Headline

Slice was already 22/23 ingested by a prior session (`dev-intake`, 2026-11-03): independent reviews (revAG/revAH/revAL) committed, projections staged, admissions recorded. This session validated all 9 zips, staged 23 intake candidates, validated all 9 review bindings, independently re-checked every record, and closed the one open item: b07 `period-frequency-reciprocal@r2` is now explicitly **rejected** (duplicate coverage), review `bf367493-1e71-427a-b992-c95b2f3a2a96`.

Counts: 9 zips validated, 9 imported (23 intake candidates staged), 9 review bindings valid, 1 projection staged, 1 CLI decision recorded (1 reject), 0 accepts (all admittable records already eligible), 0 lock incidents.

## Per-batch results

| Batch | Records | Validate | Import (intake candidates) | Review binding | Outcome |
|---|---|---|---|---|---|
| b01 | 4 (phase-speed, gaussian-imaging, magnification, doppler r1) | valid-data-awaiting-review | ee7e34a6, 4fa7a783, 537e3fea, 3861bb4b | revAG, 4x recommend-admit, valid | 3 eligible; doppler r1 withdrawn (superseded by r2) |
| b02 | 4 (period-freq r1, refr-index r1, lens-maker, sph-interface r1) | valid | c43029da, 2a3655cf, 82baeaef, c64cec8f | revAG, 4x recommend-admit, valid | 2 eligible; refr-index r1 never projected (inlined c literal, r2 admitted instead); sph-interface r1 withdrawn (superseded by r2) |
| b03 | 4 (optical-power, lens-power-sum, mirror-radius, OPL) | valid | 44728e58, 8b33b85f, 0968d417, c73bfe32 | revAG, 4x recommend-admit, valid | 4 eligible |
| b04 | 4 (telescope-M, magnifier-M, mach, echo-ranging) | valid | bdcbb20c, 3aabeec6, 1ec89081, e65531b3 | revAG, 4x recommend-admit, valid | 4 eligible |
| b05 | 3 (beat-freq, boundary-freq, f-number) | valid | 0a4d95da, 05593fb0, 6a751ed4 | revAH, 3x recommend-admit, valid | 3 eligible |
| b06 | 1 (doppler r2) | valid | c5ecf131 | revAH, recommend-admit, valid | eligible; r1 withdrawn as superseded |
| b07 | 1 (period-freq r2) | valid | 2eb2494a | revAH, recommend-admit (overlap-restricted), valid | **REJECTED by ingest-optics** (this session; see below) |
| b08 | 1 (sph-interface r2) | valid | 914e4dba | revAH, recommend-admit, valid | eligible; r1 withdrawn as superseded |
| b09 | 1 (refr-index r2, named speed_of_light) | valid | 54626a1d | revAL, recommend-admit, valid | eligible; r1 (inlined 299792458 literal) correctly never projected |

Final registry state for the slice: 19 eligible (16 `r1.runtime1` + 3 `r2.runtime1`), 2 withdrawn-superseded (`doppler@r1.runtime1`, `sph-interface@r1.runtime1`), 1 staged-never-projected (`refr-index@r1`), 1 rejected (`period-freq@r2.runtime1` projection candidate `5cbd679c-8ca6-49eb-b468-641357764269`).

## The one decision: b07 r2 rejected (duplicate coverage)

Projection staged cleanly (`integration ... --version r2.runtime1`, diagnostics empty, reference replay passed), then:

`review 5cbd679c... --decision rejected --reviewer ingest-optics`

Reasons: r2 math is byte-for-byte identical in meaning to eligible `r1.runtime1` (T=1/f, same vars/guards/refs); r2 only adds overlap documentation (`duplicate_of computer-science--clock-cycle-time@r1`, UVM overlap source, overlap limitation). Admitting it would duplicate the eligible catalog entry. Concurs with revAH's own permitted-use ("overlap/correction-evidence use only; do not import as a new scientific relationship") and the worker's NUMERICAL-REVIEW `preferred_candidates` (`new_coverage: false`). Checked source UP1 Sec 15.1 Eq 15.1 / Sec 16.1 via the revAH report; scenario scope periodic wave/oscillator full-cycle conversion with f>0; zero-frequency/aperture exclusions retained in r1.

## Independent re-checks performed (not rubber-stamped)

- Re-derived key algebra myself: spherical-interface r1 (R-form) vs r2 (C-form) are exactly equivalent under C=1/R, and r2 additionally admits the planar C=0 case; magnifier M=(N/L)(1+(L-ell)/f) reproduces both textbook limits (1+N/f at L=N, N/f relaxed eye); Gaussian d_i=f*d_o/(d_o-f) follows from 1/f=1/d_o+1/d_i; Doppler sign conventions consistent (toward-positive).
- Dimension-checked all 23 expressions against declared units (Hz/m/s/1/m/diopter-family); guards exclude every singularity the expressions admit (d_o=f, matched indices, u_s=v, f=0, zero radius).
- Confirmed the three supersessions were correct calls: doppler r2 loosens the unnecessary symmetric observer subsonic cap (450 m/s approaching case); refr-index r2 replaces the inlined `299792458` literal with named `speed_of_light` (the known "1 waves c" correction); sph-interface r2 replaces finite-R with curvature input.
- Prior-review signals consulted: NUMERICAL-REVIEW.json (b01-b08 archives, preferred-revision list, doppler/refraction/magnifier grid findings) supports the admitted set; QUALITY-AUDIT.json, MODEL-DETAILS.md, FORMULA-INDEX.md carry no optics-slice content (other workers/slices); b09 postdates the numerical audit but its record is trivially verifiable and revAL-reviewed.

## Skipped step with reason

`auditing packet` was not run: it produces a handoff artifact for a *separate* reviewer agent, and separate independent reviews already exist, validate against the exact zip SHAs, and are committed. There was no recipient. All 9 `auditing validate` bindings were run instead (all `valid-review-not-published`).

## No-op CLI decisions explained

No `review --decision accepted` was recorded by ingest-optics: every admittable record is already eligible under 2026-11-03 projection candidates. Re-recording was mechanically refused by design (verified in code): intake candidates carry `model: null` plus blocking `requires-extension` diagnostics, so `review` raises before any write; `review()` also refuses a second candidate claiming an admitted immutable revision. Nothing was forced around these guards.

## Lock-retry incidents

None. Zero "database is locked" events across 9 validates, 9 imports, 9 review-validations, 1 integration, 1 review, and several read-only sqlite probes.

## Surprises and dead ends

1. Slice 96% pre-ingested: the only real delta was b07 r2's undocumented non-admission, which turned out to be correct-but-unrecorded. Now recorded.
2. No `waves-and-optics-codex-b09/` extracted directory exists (only the zip); b09 bundle was read straight from the zip. No b09 row in README/NUMERICAL-REVIEW (packed after the worker's audit).
3. `gaussian-finite-conjugate-imaging@r2.runtime1` is eligible from another slice/worker and coexists with my slice's r1; left untouched.
4. `import` always mints fresh intake-candidate rows (no dup-key reuse); harmless here because the prior session projected straight from zip+review without importing, so no duplicate intake rows exist (verified: exactly 1 intake candidate per identity).
