---
id: source-hydropower-investment-demo-reference
type: source
title: Hydropower and Incremental NPV Reference Sources
summary: 'Reference equations and limitations for a synthetic run-of-river turbine-upgrade scenario: net head, flow, electrical output, on-site load clipping, and discounted incremental cash flow.'
status: active
created: '2026-10-26'
updated: '2026-10-26'
topics:
  - exemplars
  - finance
confidence: medium
relations:
  - type: supports
    target: note-meta-hackathon-build-plan
  - type: relates-to
    target: concept-end-state-vision
---

# Hydropower and Incremental NPV Reference Sources

## Scope

Retrieved on **2026-10-26** to support a deliberately narrow, synthetic physical-to-financial example in [[note-meta-hackathon-build-plan]]. These sources support physical definitions and discounted cash-flow methodology, not the validity of a particular plant dataset or the commercial payoff of the proposed product.

The DOE glossary, Renewables First explanation, and OpenStax finance chapter were read directly through readable-page retrieval. Additional DOE/EIA/USGS pages were read during independent research. No actual site flow history, engineering curve, tariff contract, upgrade quote, or environmental permit was obtained.

## H1 — US Department of Energy: hydropower glossary

- Publisher: U.S. Department of Energy.
- URL: https://www.energy.gov/cmei/water/glossary-hydropower-terms
- Title: Glossary of Hydropower Terms.

Useful definitions:

- Flow is volume passing a point per unit time, expressed in cubic feet or cubic meters per second.
- Environmental flows include the quantity, timing, and quality of water needed downstream to protect ecosystems and human well-being.
- Installed/nameplate capacity is maximum generator output under manufacturer-specified conditions; it is not expected continuous generation.
- Net capacity factor compares actual output over a period with hypothetical continuous full-capacity output.
- Run-of-river facilities channel a portion of a waterway through a canal/penstock to exploit natural elevation decline.
- Practical resource incorporates environmental, economic, and regulatory constraints, not only theoretical physical energy.

**Implication:** water availability, electrical capacity, and operating constraints must be explicit. A universal bypass-subtraction rule cannot be inferred from this glossary; site-specific environmental requirements may be met through or around a turbine.

## H2 — Exact power equation: engineering practitioner explanation

- Publisher: Renewables First, a commercial engineering practitioner, not a government standard.
- Title: Performance and Financial Analysis.
- URL: https://renewablesfirst.co.uk/renewable-energy-technologies/hydropower/hydropower-learning-centre/performance-and-financial-analysis/
- Page credits Phil Davis and engineering-team review; page says reviewed June 2026.

The page gives:

> “P = m x g x Hnet x η”

Here P is power in W, m is mass flow in kg/s, g is approximately 9.81 m/s², Hnet is gross head less head losses, and eta is the product of turbine, drive, and generator efficiencies. With mass flow = water density × volumetric flow, this becomes P = rho × g × Q × Hnet × eta. At rho approximately 1,000 kg/m³, the convenient kW form is 9.81 × Q[m³/s] × Hnet[m] × eta.

The page distinguishes power (kW) from energy (kWh), notes 8,760 hours in a non-leap year, and describes annual-energy/capacity-factor calculations as approximations dependent on site-specific conditions. It distinguishes on-site offset value from export value and notes that demand/generation timing affects the fraction self-consumed.

**Do not inherit the page's illustrative prices, historical price trends, generic efficiency ranges, assumed head-loss percentage, or example capacity factor as measured inputs for this project.** The proposed demo uses explicit fictional inputs. Net head already reflects conveyance losses; do not subtract them again. Constant efficiency ignores real dependence on operating flow/head.

## H3 — OpenStax: net present value

- Publisher: OpenStax.
- Book: Principles of Finance, Section 16.2, Net Present Value (NPV) Method.
- URL: https://openstax.org/books/principles-finance/pages/16-2-net-present-value-npv-method

The chapter defines NPV as present value of cash inflows minus present value of cash outflows. Its worked examples discount each period's cash flow and subtract the initial investment. It shows how changing the discount rate changes NPV and the investment decision.

For the demo's incremental-upgrade comparison:

```text
NPV = -initial_upgrade_capex + sum(incremental_CF_y / (1+r)^y)
```

The project must explicitly declare initial capex timing, year-end cash-flow timing, horizon, and a consistent real/nominal price and discount-rate basis. A positive result is favorable under the specified model and inputs; it is not a complete investment recommendation.

## Additional sources read during research

### H4 — DOE efficiency-improvement examples

https://www.energy.gov/cmei/water/frequently-asked-questions-section-243-hydroelectric-efficiency-improvement-incentives

Supports the real context for efficiency upgrades and that performance changes depend on flow/head conditions. It does not establish the example's assumed 60%→80% total electrical-efficiency improvement or actual project economics.

### H5 — EIA hydropower explanation

https://www.eia.gov/energyexplained/hydropower/

Supports the run-of-river description and variability of hydropower availability with precipitation/seasonality. It is not a calibrated future-flow forecast.

### H6 — USGS flow-duration and low-flow statistics

https://pubs.usgs.gov/sir/2008/5126/section3.html

Explains flow-duration/exceedance statistics and notes that at least ten years of record is typically used for reliable probable-future-condition indicators in that context. A duration curve does not preserve calendar ordering or coincident demand. Four synthetic blocks are a demonstration fixture, not a hydrological record or empirical forecast.

## Project-specific modeling choices, not quotations from sources

The plan composes the references into an explicit screening model:

1. Subtract an assumed bypass flow from fictional river flow for this declared site layout; cap at design turbine flow.
2. Compute net electrical power using net head and total electrical efficiency, then cap at installed capacity.
3. Clip each time block's generation against coincident on-site demand before aggregating avoided kWh.
4. Credit only avoided volumetric grid purchases; no export revenue or avoided demand charges.
5. Calculate upgrade-minus-baseline energy and subtract incremental O&M before discounting incremental cash flows.

These are project-created assumptions. Source references do not turn them into site-specific engineering validation. The default fixture and independently sanity-checked numbers are preserved in the plan, not presented as observed data.

## Critical limitations

- Annual-mean flow × 8,760 can be misleading when generator/load caps or varying efficiency are present. Evaluate aligned blocks first, aggregate second.
- Lower flow can reduce total generation while increasing the *incremental* value of an efficiency upgrade under self-consumption caps; do not impose a false monotonic narrative.
- Environmental requirements, cut-in flow, water rights, downtime, efficiency curves, varying net head, infrastructure losses, taxes, financing, replacement, degradation, grants, and salvage require site-specific treatment. Most are excluded from the initial demo and must be visibly disclosed.
- No blanket confidence interval follows from low/base/high scenarios. A deterministic sensitivity sweep is not a probability model, variance decomposition, or calibrated risk forecast.
- No universal numerical minimum-flow requirement, official DOE webpage with the exact full power equation, or actual plant economics was verified. The exact equation is supported here by the identified practitioner source and standard dimensional reasoning, not falsely attributed to DOE.
