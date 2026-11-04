# Waves and optics curation session

Curator: codex. Started 2026-11-03T02:42:07Z; completed 2026-11-03T03:42:11Z. Measured active-session wall time: 60.08 minutes, exceeding the assigned 60-minute minimum. No sleeps, background workers or prior-session time counted. Tool latency and active research/authoring/review are included; this is wall-clock measurement, not a CPU-time estimate.

Returned 8 validated data ZIPs containing 22 serialized revision records. Preferred coverage is 18 nonduplicate relationships, with one additional local ID flagged as an existing-catalog overlap. Three r2 records preserve correction history; original files and archives remain intact. Toolkit version: 2026-10-31.6; schema: cm-curation-batch/1.

## Completed ZIPs

Every ZIP contains exactly bundle.json and manifest.json. JSON and packed-ZIP validation reports are saved in its matching batch folder.

| Data ZIP | Records | Numerical checks | Rejection checks | JSON / ZIP |
| --- | ---: | ---: | ---: | --- |
| [waves-and-optics-codex-b01-return.zip](waves-and-optics-codex-b01-return.zip) | 4 | 12 | 10 | Passed / passed |
| [waves-and-optics-codex-b02-return.zip](waves-and-optics-codex-b02-return.zip) | 4 | 10 | 8 | Passed / passed |
| [waves-and-optics-codex-b03-return.zip](waves-and-optics-codex-b03-return.zip) | 4 | 11 | 6 | Passed / passed |
| [waves-and-optics-codex-b04-return.zip](waves-and-optics-codex-b04-return.zip) | 4 | 10 | 8 | Passed / passed |
| [waves-and-optics-codex-b05-return.zip](waves-and-optics-codex-b05-return.zip) | 3 | 7 | 6 | Passed / passed |
| [waves-and-optics-codex-b06-return.zip](waves-and-optics-codex-b06-return.zip) | 1 | 6 | 3 | Passed / passed |
| [waves-and-optics-codex-b07-return.zip](waves-and-optics-codex-b07-return.zip) | 1 | 3 | 2 | Passed / passed |
| [waves-and-optics-codex-b08-return.zip](waves-and-optics-codex-b08-return.zip) | 1 | 4 | 3 | Passed / passed |

## Preferred relationship coverage

Expressions use coherent base units; variable conditions, sign conventions, source locators, numerical evidence and inverse exclusions are in each bundle. The table is an index, not an alternative interface specification.

| Relationship | Forward expression | Preferred batch/revision |
| --- | --- | --- |
| Periodic traveling-wave phase speed | `v = f * lam` | b01, r1 |
| Thin-lens and paraxial spherical-mirror imaging | `d_i = f * d_o / (d_o - f)` | b01, r1 |
| Signed transverse magnification from conjugate distances | `m_t = -d_i / d_o` | b01, r1 |
| Collinear acoustic Doppler frequency on the forward-crossing branch | `f_o = f_s * (v + u_o) / (v - u_s)` | b06, r2 |
| Light phase speed and refractive index | `v = 299792458 / n` | b02, r1 |
| Thin-lens focal length from refractive indices and curvatures | `f = 1 / ((n_l / n_m - 1) * (C_1 - C_2))` | b02, r1 |
| Paraxial imaging at one spherical or plane refracting interface | `d_i = n_2 * d_o / ((n_2 - n_1) * C * d_o - n_1)` | b08, r2 |
| Optical power as inverse focal length | `P = 1 / f` | b03, r1 |
| Combined power of coaxial thin lenses in contact | `P_total = sum(powers)` | b03, r1 |
| Paraxial spherical-mirror focal length and radius | `f = R / 2` | b03, r1 |
| Geometric optical path length of a homogeneous ray segment | `opl = n * s` | b03, r1 |
| Signed angular magnification of a Keplerian telescope | `M = -f_o / f_e` | b04, r1 |
| Simple-magnifier angular magnification at finite viewing distance | `M = N / L * (1 + (L - ell) / f)` | b04, r1 |
| Mach number from medium-relative object speed | `M_a = u / v` | b04, r1 |
| One-way acoustic range from stationary round-trip echo time | `r = v_p * tau / 2` | b04, r1 |
| Acoustic beat frequency with explicitly ordered component frequencies | `f_b = f_hi - f_lo` | b05, r1 |
| Frequency continuity across a stationary optical transmission boundary | `f_t = f_i` | b05, r1 |
| Paraxial imaging-system f-number at infinite conjugates | `N_f = f / D_ep` | b05, r1 |

## Revision and overlap instructions

- Prefer b06 Doppler r2 to b01 r1. It removes an unsupported observer upper-speed cap and explicitly distinguishes the wave-comoving zero-crossing-rate limit from the forbidden sonic-source denominator singularity.
- Prefer b08 interface-imaging r2 to b02 r1. It uses signed curvature C=1/R and includes the separately sourced near-normal plane-interface apparent-depth limit at C=0. A zero radius is not a plane, and axial apparent depth is not transverse image height.
- b07 period-frequency r2 flags computer-science--clock-cycle-time@r1 as an equivalent relationship. Do not import either local period revision as new scientific coverage. No existing curator's record was changed.
- b06's historical count of nineteen distinct relationships predates the b07 overlap finding. This report and SESSION.json give the corrected eighteen nonduplicate count. Earlier archived statements remain preserved as history.

## Verification and limits

All serialized revisions passed 63 numerical reference checks and 46 domain/missing-input checks. Preferred nonduplicate revisions account for 50 numerical and 38 rejection checks. Published rounded expected values remain as reported, with documented unit conversions and tolerances.

NUMERICAL-REVIEW.json: 22 revision-level dimensional checks, 271 exact rational inverse/source-residual grid cases, 8 two-member archives semantically matching local bundles; not scientific approval. See [NUMERICAL-REVIEW.json](NUMERICAL-REVIEW.json).

The [quantity review](QUANTITY-REVIEW.json) retains 30 proposed quantity interfaces and their context/domain variants. It separates phase speed from pulse timing speed, optical power from watts, angular from transverse magnification, mirror from transmitted-surface sign conventions, and effective from back focal length. The session quantity index uses preferred revisions rather than first-seen historical definitions.

Sources include 24 distinct directly inspected source URLs across completed records. Full bibliographic/access/terms evidence is in the bundles. Completed models rely on official HTML; no completed equation depends on ambiguous PDF extraction. [SOURCE-REVIEW.json](SOURCE-REVIEW.json) records source prose/sign mistakes avoided and deferred PDF limitations.

All preferred candidates remain requires-extension with runtime_model null: proposed wave/optics meanings and coherent inverse-length notation need integration. This work did not change a runtime registry, publish models, instantiate a composition or establish scientific approval. Duplicate screening was limited to the supplied dated 218-record inventory, runtime snapshot and this curator's returns; no global uniqueness claim is made.

Current accessed OpenStax versions identify CC BY-NC-SA and assert additional AI/LLM/commercial-use permission requirements. MIT OCW terms identify CC BY-NC-SA 4.0. Manufacturer articles do not establish open reuse grants; NOAA/NASA page-specific terms remain unknown. Only attributed mathematical facts/short original paraphrases/data are supplied; no downstream legal clearance inferred.

## Artifact navigation and replay

SESSION.json contains the batch inventory, preferred revisions, measured start/end/checkpoint times, quantity definitions, attempted/deferred work and exact next action. SOURCE-REVIEW.json and QUANTITY-REVIEW.json preserve review details outside the two-member data ZIPs. Historical author_batch scripts generate local research JSON and should not be rerun over completed checkpoint folders. Use fresh folders and batch IDs for future research or corrections.

From the kit root, a reviewer can replay a saved archive's toolkit checks without regenerating the research:

```powershell
uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation validate returns/waves-and-optics-codex-b08-return.zip
```

The same command accepts any of the eight archives. Research helpers numerical_review.py and quantity_review.py inspect this curator's saved records; their conclusions retain the review limits described above. No source PDFs, screenshots, executables, toolkit or credentials are included in the data archives.

## Attempted and deferred coverage

SESSION.json retains 30 attempted/deferred entries with source URLs and reasons. Coverage includes all assignment seeds, adjacent kinematic definitions, finite-conjugate optics and instrument geometry. Source-backed special cases were kept with their canonical relationships instead of counted as new models.

Deferred categories include exact Snell/critical/Malus/Mach-angle and logarithmic sound-level forms excluded by the assignment; physical-optics interference/diffraction/polarization; unordered beat absolute values; virtual-object/Galilean profiles awaiting broader sign evidence; general optical-path integrals/Fermat stationarity; wave-field partial derivatives; and coupled ray-transfer matrices/principal planes. PDF screenshot adapters exposed only text placeholders, so no visual-equation verification is claimed. Isolated source access failures were recorded and alternative candidates pursued.

The [unfinished separated-lens follow-up](SEPARATED-LENS-FOLLOWUP.json) saves a newly located author-textbook source and two exact paraxial ray constructions. Reversing the example lens order preserves 0.08 m effective focal length while changing the back focal distance from 0.04 m to 0.06 m. This illustrates why those metre-valued quantities need different references. It is a continuation lead, excluded from completed model counts and the 271-case completed-record audit.

## Priorities for a separately authorized continuation

- Piecewise-homogeneous optical-path aggregation: source explicitly permits summing completed segment optical lengths; assess independent scientific value and per-family-element domain enforcement before adding a record.
- Separated thin-lens effective power: clear author-textbook HTML now located in Wandell section 11.2 Eqs. 11.1/11.2 (SOURCE-REVIEW.json). Verify ambient-medium/sign scope and independent ray checks, distinguish EFL/BFL/FFL, and compare the existing contact-lens family; no contact-only clone.
- Broader virtual-object and Galilean telescope profiles: if source definitions/signs are unambiguous, revise existing IDs instead of creating renamed copies.
- Remaining scalar geometric instrument definitions require source/duplicate screening; energy, intensity, constitutive medium-speed laws, physical optics, log and trig angle models remain outside assignment.

The assigned sustained session is complete. These priorities are a saved backlog, not an ongoing background mandate. Resume from SESSION.json and preferred revisions if a continuation is requested.
