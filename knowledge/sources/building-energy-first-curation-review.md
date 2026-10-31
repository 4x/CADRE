---
id: source-building-energy-first-curation-review
type: source
title: Review of the First Building-Energy Curation Return
summary: Four submitted research records pass v1 mechanical checks; source review identifies rights metadata errors, interface overclaims, scope issues and reference/inverse improvements that inform the revised curator instructions.
status: active
created: '2026-10-31'
updated: '2026-10-31'
topics:
  - agents
  - lifecycle
  - interoperability
confidence: medium
relations:
  - type: relates-to
    target: note-offline-curation-agent-kit
  - type: relates-to
    target: note-offline-curator-instructions
  - type: relates-to
    target: concept-specialized-model-curation-agents
---

# Review of building-energy-muse-b01

Reviewed 2026-10-31 at the owner's request. Original artifact: `from-offline-curation-workers/building-energy-muse-b01-return.zip`, batch `building-energy-muse-b01`, curator label `muse-spark`, kit `2026-10-31.1`, schema `cm-curation-batch/1`. This review does not modify, import, admit or replace the submitted records. The owner supplied the artifact; source claims inside it remain claims until checked. This is an agent technical/source review, not a scientific expert certification or legal opinion.

Original ZIP SHA-256: `3c783e9ea8c86436fe60f5e2e8965111dc9dc810b936b31c12f8a05f1b458bdd`.

## Outcome

The ZIP checksum/schema pass, with eight passing forward reference cases and four passing rejection cases. The four equations are sensible candidate relationships: constant-power electricity consumption, sensible heat, steady slab conduction rate, and absolute slab thermal resistance. All four correctly retain physical units and `requires-extension` status, with no executable runtime projection. The original signed/heating scope, inverse limitations, explicit constants, and distinction between absolute and area-normalized resistance are useful evidence. New runtime vocabulary is still required.

The sources checked support the underlying formula families and worked examples. Return for revision before approval: a valid JSON/arithmetic artifact is not a verified model card. The important corrections are below. The original return should remain unchanged; a curator can issue revised records with new revisions.

## Review findings and requested corrections

| Priority | Finding in the submitted artifact | Correction |
| --- | --- | --- |
| High | The first two source records say the accessed OpenStax preface states CC BY 4.0. The current page instead states CC BY-NC-SA 4.0 and includes additional use notices | Correct the observed terms/version and include the exact terms-page URL/locator and date. Record unresolved intended-use questions rather than claiming clearance or assuming older publisher terms apply |
| High | `handoff.connections[0]` says resistance feeds the conduction-rate model, but that model's inputs are conductivity, area, temperature difference and thickness; there is no resistance input | Remove the claimed implemented edge or label it hypothetical with the missing qualified relationship/adapter. Equivalent algebra in prose does not add a graph port |
| Medium | The second sample question requests a single water-heating event through a seasonal-performance model “whose scope matches this single heating event” | Use a single-model test question or name the missing event-specific performance relationship. An annual/seasonal model cannot be made event-specific by a matching-scope assertion |
| Medium | Electrical energy is called purchased energy although the equation measures device consumption; a 3-hours/day annual oracle is paired with wording excluding duty cycling inside the interval | State the metering/supply assumption separately. Define duration as total energized time at the same power if using that oracle, with excluded/off-period consumption explicit; otherwise use a continuous-interval oracle |
| Medium | The conduction `inverse_notes` require all geometry/property/difference quantities to be nonzero for both discussed directions | Write exclusions per target. Solving temperature difference at zero heat rate is valid when conductivity and area are positive; the unknown temperature difference need not already be nonzero. Check an inverse zero case by substitution |
| Medium | Sensible-heat `expected: 62790` is labeled a published oracle even though the source reports 62.8 kJ. Resistance `expected: 39.81` is first recomputed from the same candidate expression, then cross-checked with a rounded published rate | Keep the reported 62800 J as the published sensible-heat oracle, or label 62790 as a separate arithmetic derivation. For resistance, construct a clearly identified source-derived oracle from reported quantities, and document rounding propagation. Do not let a zero boundary be the only structurally independent case |
| Medium | Heating-only restrictions are explicit but narrower than the source's signed heat relation; the card proposes separate cooling records. `specific_heat` also needs a process/material-state qualification | Preserve signed source scope when appropriate, distinguish an application profile from a different law, and document the appropriate heat-capacity convention. This is a reuse improvement, not a claim that the declared heating-only arithmetic is wrong |
| Medium | Zero thickness/area are accepted as selected ideal boundaries without consistently distinguishing a limiting extension from a physical slab | Label these as ideal/limiting extensions if retained; otherwise use physical positive geometry and a different boundary case. Do not manufacture zero-domain inclusion simply to satisfy the test format |
| Low | `R_abs` is listed as a source symbol although the translation introduces it from an area-normalized source quantity | Mark it as introduced and retain the explicit derivation. The existing transformation explanation is valuable; improve attribution precision |
| Low | A prose COP definition was deferred partly because it has no symbolic equation. Some simple signed/difference/area-normalized relationships were deferred to maintain an application chain/coherent-unit preference | A faithful formalization of precise prose is allowed. The missing seasonal weighting evidence remains a legitimate blocker. Unit variants are conversions, not separate models; area-normalized versus absolute resistance are genuinely different quantities. Do not require a chain to select useful atomic definitions |

## Primary-source checks

[OpenStax §9.5](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) contains the integral energy definition and constant-rate case. Example 9.10 reports 21.90 kWh for the stated LED operating schedule. This supports the numerical reference, while the device/meter boundary and active-time interpretation still require clear model wording.

[OpenStax §1.4](https://openstax.org/books/university-physics-volume-2/pages/1-4-heat-transfer-specific-heat-and-calorimetry) contains equation 1.5 and Example 1.5, including the reported water result 62.8 kJ. It also distinguishes heat capacities under different constraints and later uses signed heat transfer in calorimetry. This supports the formula and motivates better process/sign metadata.

[OpenStax §1.6](https://openstax.org/books/university-physics-volume-2/pages/1-6-mechanisms-of-heat-transfer) contains equation 1.9 and Example 1.11, including the reported 41.3 °C junction, 1.47 W rate and area-normalized resistance values. The submitted absolute-resistance expression is a stated derivation, not a directly reported numerical resistance. Independently using the reported steel temperature drop and rate gives approximately 39.932 K/W; the candidate formula gives 39.809 K/W from its declared geometry. Their difference requires a rounding argument, not a claim that 39.81 was directly published. Interface and inverse critiques above follow from the submitted records' own declarations.

[OpenStax's current preface](https://openstax.org/books/university-physics-volume-2/pages/preface) explicitly lists CC BY-NC-SA 4.0; the submitted “CC BY 4.0 as observed” statement is not supported by the page retrieved for this review. The page also contains separate use notices. This review records that discrepancy and does not determine the legal status of mathematical facts, any particular generated record, or a future commercial product.

[UMD's heat-pump page](https://www.extension.umd.edu/resource/home-energy-heat-pump) does describe COP as a heat/electricity ratio in prose. The [DOE FEMP page](https://www.energy.gov/cmei/femp/purchasing-energy-efficient-residential-water-heaters) gives UEF figures and cites a test method. Neither reviewed passage supplies the missing seasonal whole-system weighting contract. Deferring a seasonal mapping is defensible; rejecting all precise prose formalization is not required.

## Changes to the instructions motivated by this return

The user's correction is adopted: each worker receives complete curator-only `AGENTS.md` and only its assignment, with operator instructions retained centrally. Curation targets atomic composable models for a large catalog, independently of future scenarios. Chains and example questions are optional and may be empty in the handoff. Definition/parameter/context/source distinctions, per-direction inverse checks, reported-oracle preservation, actual-port connection checks and license provenance are now explicit in [[note-offline-curator-instructions]]. No automated scientific review capability is implied by these instruction changes.

The existing runtime vocabularies, unit limits and canonical-equation inverse design remain intact. The old return version remains accepted by the transport validator; a revised kit must not strand work already assigned. Large-scale deduplication and ontology reconciliation will need a shared inventory and central integration process as the catalog grows, but forcing every worker to design a chain does not solve those problems.
