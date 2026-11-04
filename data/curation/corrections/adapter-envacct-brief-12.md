# Adapter brief: envacct factor → GWP100 → two-gas-total chain bridges (brief 12)

To: curation review (batch environmental-accounting-adapters-b01, 3 new records)
From: envacct bridge curator (native compat-curation subagent), 2026-11-04
Status: proposed (mechanical — no admitted record is revised; all reviews stand)

## What happened

Two links of the environmental-accounting chain

`emission-mass-from-activity-and-factor` → `co2-equivalent-from-gas-mass-and-gwp`
→ `total-co2e-from-two-gas-components`

fail fail-closed under `Port.require_compatible` (`connected_models/contracts.py`:
exact `(meaning, context)` equality; units already match at `kg`). All endpoint
records stand as reviewed; nothing was modified and the registry was read
read-only throughout (`.registry/models.sqlite3`, `mode=ro`; never staged,
reviewed, or admitted here).

Link 1 — meaning AND context differ. Producer output
(`environmental-accounting--emission-mass-from-activity-and-factor@r1.runtime1`,
symbol `E`):

- `emission_mass`, `kg`,
  `same emitting source, gas, Scope boundary, accounting period and EF applicability as inputs`

Consumer input
(`environmental-accounting--co2-equivalent-from-gas-mass-and-gwp@r1.runtime1`,
symbol `Mgas`; the registry holds r1 only — no r2 exists):

- `greenhouse_gas_mass`, `kg`,
  `same emitted gas, 100-year horizon and assessment vintage (AR6 values used in references) as Mco2e`

Link 2 — same meaning, different contexts (the brief-7–9 near-miss shape, but
see below). Producer output (co2-equivalent record above, symbol `Mco2e`):

- `carbon_dioxide_equivalent`, `kg`,
  `same stated gas, 100-year horizon, vintage, Scope boundary and period as inputs`

Consumer inputs
(`environmental-accounting--total-co2e-from-two-gas-components@r1.runtime1`):

- `Ma`: `carbon_dioxide_equivalent`, `kg`,
  `same horizon (GWP100), vintage, Scope boundary and period as Mb and Mtot`
- `Mb`: `carbon_dioxide_equivalent`, `kg`,
  `same horizon (GWP100), vintage, Scope boundary and period as Ma and Mtot`

## Registry survey (all 235 admitted models, 2026-11-04)

`emission_mass` (`kg`) — 1 producer, 3 consumers, zero working edges:

| side | record@rev | port | context |
|---|---|---|---|
| OUT | emission-mass-from-activity-and-factor@r1 | `E` | `same emitting source, gas, Scope boundary, accounting period and EF applicability as inputs` |
| IN | emission-intensity-from-mass-and-output@r1 | `E` | `same Scope boundary, gas/CO2e basis and annual period as Q and I` |
| IN | revenue-intensity-from-emissions-and-revenue@r1 | `E` | `same Scope boundary, gas/CO2e basis and annual period as R and I` |
| FAM | pooled-intensity-from-site-families@r1 | `E` | `same Scope boundary, gas/CO2e basis and period across all pooled sites as Q and I` |

`greenhouse_gas_mass` (`kg`) — 0 producers, 2 consumers:

| side | record@rev | port | context |
|---|---|---|---|
| IN | co2-equivalent-from-gas-mass-and-gwp@r1 | `Mgas` | `same emitted gas, 100-year horizon and assessment vintage (AR6 values used in references) as Mco2e` |
| IN | co2-equivalent-gwp20-from-gas-mass@r1 | `Mgas` | `same stated gas, 20-year horizon and assessment vintage (AR6 values used in references) as Mco2e` |

`carbon_dioxide_equivalent` (`kg`) — 4 producers, 3 consumer faces, zero working edges:

| side | record@rev | port | context |
|---|---|---|---|
| OUT | co2-equivalent-from-gas-mass-and-gwp@r1 | `Mco2e` | `same stated gas, 100-year horizon, vintage, Scope boundary and period as inputs` |
| OUT | co2-equivalent-gwp20-from-gas-mass@r1 | `Mco2e` | `same stated gas, 20-year horizon, vintage, Scope boundary and period as inputs` |
| OUT | total-co2e-from-gas-family-sum@r1 | `Mtot` | `same horizon, vintage, Scope boundary and period as the G elements` |
| OUT | total-co2e-from-two-gas-components@r1 | `Mtot` | `same horizon, vintage, Scope boundary and period as inputs` |
| IN | total-co2e-from-two-gas-components@r1 | `Ma` | `same horizon (GWP100), vintage, Scope boundary and period as Mb and Mtot` |
| IN | total-co2e-from-two-gas-components@r1 | `Mb` | `same horizon (GWP100), vintage, Scope boundary and period as Ma and Mtot` |
| FAM | total-co2e-from-gas-family-sum@r1 | `G` | `same horizon (GWP100), vintage, Scope boundary and period as Mtot` |

Every port on both links currently matches nothing, so any bridge orphans zero
working chains by construction.

## Decision per link: adapters (both links)

The brief-7–9 convention picks the minimal honest side that orphans nothing.
A context-r2 must keep the record's meaning and science intact while the shared
string truthfully describes the linked value on both sides. Neither link admits
such a move:

Link 1 → adapter (meanings differ, so no contexts-only r2 can bind at all).
A meaning-changing r2 is rejected on both sides: stamping the consumer's
`greenhouse_gas_mass` + GWP-horizon/vintage context onto the factor-accounting
output would assert a 100-year horizon, an AR6 vintage, and the symbol `Mco2e`
— all undefined in that horizon-independent record (the brief-8 reverse-move
objection); stamping the producer's `emission_mass` + EF-applicability context
onto `Mgas` would feed generic emission mass into a conversion that requires a
GHG and would assert EF conditions undefined in the GWP record. The adapter is
1 new record, 0 revisions, and honest: the producer's own output definition
already scopes `E` to "mass of stated greenhouse gas", so the relabel asserts
no new physics — the GWP100/vintage scope it carries is stated in assumptions.

Link 2 → two adapters, one per leg (a context-r2 cannot honestly bind here
despite the near-miss shape). Consumer-side r2 would stamp the producer
context — `same stated gas, ... as inputs` — onto `Ma`/`Mb`, whose own
contexts deliberately omit gas identity because the two components are
DIFFERENT gases (the record's application profile: "methane-route and
nitrous-oxide-route subtotals"); asserting same-gas across the sum contradicts
that profile. Producer-side r2 is worse: one output string cannot equal both
`Ma` and `Mb` contexts (`Ca ≠ Cb`), so it fixes at most one leg, and either
target references `Mb`/`Mtot`/`Ma` symbols undefined in the co2e record. Two
identity adapters (input face = producer output, output face = one consumer
input each, sibling leg named in assumptions) fix both legs with 0 revisions
and 0 orphans.

## Records authored (batch environmental-accounting-adapters-b01)

1. `environmental-accounting--emission-mass-as-greenhouse-gas-mass@r1`
   (link 1): IN `E` = producer-output face, OUT `Mgas` = consumer-input face,
   expression `E`, guard `E >= 0`.
2. `environmental-accounting--single-gas-co2e-as-component-a@r1`
   (link 2 leg A): IN `Mco2e` = producer-output face, OUT `Ma` = `Ma` face,
   expression `Mco2e`, guard `Mco2e >= 0`.
3. `environmental-accounting--single-gas-co2e-as-component-b@r1`
   (link 2 leg B): IN `Mco2e` = producer-output face, OUT `Mb` = `Mb` face,
   expression `Mco2e`, guard `Mco2e >= 0`.

All three are `definition`-kind identity records: the scope that the face
change implies (GHG-ness, GWP100/AR6 horizon-vintage, component-A/B roles,
sibling-leg sameness) is carried in assumptions, never in arithmetic. Faces
were embedded byte-exact by reading the registry read-only at author time.
Each record carries 2 numeric references (link-2 values mirror the upstream
reference outputs 300/546 to document chain intent), 1 domain + 1
missing-input rejection case, and a project-derivation source citing the
endpoint keys. Reference replay is exact substitution (`Registry.verify_reference`
passes identically).

Out of scope (deferred in the batch): GWP20-horizon legs (no GWP20 total
consumer exists; horizons never interchangeable), the family-sum `G` leg
(third consumer context, separate near-miss), and the three `emission_mass`
intensity-consumer legs (distinct contexts, separate near-misses).

## Resubmission

Batch `environmental-accounting-adapters-b01` is validated and packed in
`.runs/compat-curation/adapters-envacct/` (bundle + return ZIP as usual) for
re-review per protocol. It was never staged or imported; the registry is
untouched.
