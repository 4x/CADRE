---
id: source-m2d-acceptance-exercise
type: source
title: M2-D Acceptance Exercise Evidence
summary: 'Recorded M2 acceptance run: stored-model compositions, version reuse, input revision, compatible
  substitution, inverse cases, missing-input and incompatible-binding outcomes, deterministic replays
  and per-phase inference evidence.'
status: active
created: '2026-10-31'
updated: '2026-10-31'
topics:
- benchmarks
- reliability
confidence: medium
relations:
- type: relates-to
  target: note-mvp-build-sequence-and-extension-triggers
- type: relates-to
  target: question-evaluation-and-reference-evidence
- type: relates-to
  target: source-mvp-heating-and-meta-evidence
- type: relates-to
  target: source-mechanics-independent-audit
---

# M2-D acceptance exercise evidence

Recorded 2026-10-31 on the reviewed subset of seven eligible registry models (five heating/finance, two mechanics `r1.runtime1` projections). Each case below was executed and its run replayed with the read-only `replay` command, which re-executes the saved graph against the run's pinned models/admissions and compares status, error and outputs exactly. All twelve replayed runs matched. No inference was spent during M2-D; the ledger is unchanged at 29 settled calls, $0.274631 conservatively, with no outstanding reservations.

## Cases and runs

| Case | Run | Outcome | Replay |
| --- | --- | --- | --- |
| Stored-model composition (live question) | `69144a1b-58f1-4aa8-bf99-6dae8fe946f9` | NPV $8,532.16 | matched |
| Second question reusing versions (live) | `786887da-b522-436c-b67e-dea5712adfe4` | $3,000/$1,200 costs, $1,800 savings | matched |
| Input revision (scenario) | `f3b9370d-13c3-4982-8e54-b6e5b3df7872` revises `69144a1b` | perf 3→2.5; savings $2,400→$2,160, NPV →$6,678.95 | matched |
| Input revision (fixture) | `517c5993-495b-4f36-9251-4ee6c8150d65` revises `513d4550` | perf 3→2, investment $10k→$12k; savings →$1,800, NPV →$1,899.12 | matched |
| Inverse: discounted payback (live) | `fb880a63-2725-4bee-a4f1-69cf205b0dc0` | first year-end crossing at 5 | matched |
| Inverse: seasonal performance (live) | `d25902f1-6fec-4ed9-ba2a-1299a86b6a8d` | recovers 3 | matched |
| Inverse: electricity use (live) | `4553f3a2-6f92-422f-88dd-4004b3349773` | recovers 4000 kWh | matched |
| Missing input (live) | `d4500890-724c-4fa8-9910-ae20274cead6` | `needs-input`, four questions, no graph | n/a (no graph) |
| Incompatible binding | `47b104bf-6b4d-4cf9-9004-51296ebaab38` revises `513d4550` | rejected: missing/extra inputs | matched (same rejection) |
| H1 returned-model two-phase chain | `e0f9d9c3-0197-4a6b-b0db-560434159da2` | v=144.56 m/s, x=1445.6 m | matched |
| H2 version reuse (auditor reference) | `4e926235-6eed-4e24-ac39-0302b9e2da37` | v=10.0 m/s, reproduces `airplane-70ms-decel` | matched |
| H3 returned-path inverse | `6d0b3d6e-05b0-474e-8bd9-228fe2225d13` | solves a=-1.5 m/s² | matched |
| Returned-path revision | `5eefffa1-8df9-4cec-8e24-97b1436c482f` revises H1 | coast t 10→20 s; x 1445.6→2891.2 m, v delta 0 | matched |

Compatible substitution is proven by the committed `test_revise_scenario_model_substitution` (verified second revision admitted under test review, outputs equal, diff recorded). The live registry holds a single revision per model, so no live substitution was selectable; manufacturing a second live revision for the exercise would have polluted reviewed state. Unknown-revision errors list available keys (committed `test_revise_rejects_bad_targets`).

H1 chains the two returned mechanics models: phase-1 velocity (v0=0, a=26, t=5.56 from reference `dragster-26ms2-556s`) feeds phase-2 displacement v0 with operator-scenario x0=0, a=0, t=10. Hand check: 26×5.56=144.56; 144.56×10=1445.6. H3 inverts the velocity model for `a` from the `airplane-70ms-decel` inputs (v0=70, t=40, target v=10). The runner is preserved at `.runs/m2d-acceptance-runner.py`; the acceptance comparison report is `.runs/report-f7c27b60-dc17-4533-9af6-b85d479eafe2.html`.

## Preserved lineage

Every run retains its composition, model definitions, pinned admissions with reviewer identity/notes, sources and input origins. The mechanics runs carry the `codex-technical-integrator` admissions citing the separate auditor report SHA-256 `428bfb4b…db76e7` and CC BY4 attribution. Revision runs link `revised_from` with byte-preserved parents.

## Per-phase inference evidence

| Phase | Call | Model | Conservative USD |
| --- | --- | --- | --- |
| Curation: NIST extraction (admitted) | `912a467f-b689-4ce7-a60a-2c077699a952` | muse-spark-1.3 | 0.007243 |
| Answer `69144a1b`: parse | `d049c80d-deab-44b6-af5b-f6e21c253adb` | muse-spark-1.3 | 0.011827 |
| Answer `69144a1b`: compose | `ffa8f80d-273a-4a04-97e0-4ba038fd7119` | muse-spark-1.3 | 0.011448 |
| Answer `786887da`: parse | `8f0f99d5-078f-4cbb-aa33-cff85bc06151` | muse-spark-1.3 | 0.006419 |
| Answer `786887da`: compose | `d0bb646d-3b0b-40cc-a5d2-ff85d2f8e121` | muse-spark-1.3 | 0.008901 |
| Answer `d4500890`: parse | `8a965691-65fc-45b6-9bb5-c12f317087f2` | muse-spark-1.3 | 0.007060 |
| Answer `d4500890`: compose | `f130a601-24dd-49fa-85b4-18374f507b16` | muse-spark-1.3 | 0.007255 |
| Answer `fb880a63`: parse | `e2967572-66a6-47ea-aa11-236512c17f74` | muse-spark-1.3 | 0.007249 |
| Answer `fb880a63`: compose | `03402efc-39c7-412e-bc7a-2f5377052cc5` | muse-spark-1.3 | 0.012972 |
| Answer `d25902f1`: parse | `07c47a64-50ab-42fd-b284-2b43ceeaffb9` | muse-spark-1.3 | 0.005965 |
| Answer `d25902f1`: compose | `4f365c09-bde2-41bd-97ff-d183d19b8f75` | muse-spark-1.3 | 0.007632 |
| Answer `4553f3a2`: parse | `3ef60779-18ce-4654-abe1-049ad790738c` | muse-spark-1.3 | 0.007717 |
| Answer `4553f3a2`: compose | `5babb66b-f2b8-42f6-b53e-94fef3f0f28a` | muse-spark-1.3 | 0.007646 |

Earlier blocked curation attempts and retained inference failures (malformed nested graph `d9c132cc`, failed generation) are recorded in [[source-mvp-heating-and-meta-evidence]]. No failures or reservations are outstanding; the ledger shows a `settled` group only.

## Elapsed time

Deterministic execution measured 0.3–0.7 ms per acceptance case (H1/H2/H3). CLI `replay` wall time is roughly 250–330 ms including interpreter startup. Historical live runs record creation time but no elapsed time; per-call latency was not captured.

## Reliability / limitations

- The returned-model path was exercised deterministically, not through a live composer call: the authorization question for one live mechanics answer timed out unanswered, so no new inference was spent. Agent-composed mechanics extensibility remains unproven.
- `.runs/` is gitignored local state; this record carries the durable case data (run IDs, inputs, outputs, references) for recovery.
- No new scientific claims were made: all references reused the separately audited findings in [[source-mechanics-independent-audit]] and prior NIST evidence. The auditor role was consumed, not re-dispatched.
