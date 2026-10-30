---
id: source-outsider-end-state-question-commentary
type: source
title: "Outsider Commentary on Twelve End-State Questions"
summary: "Imported duplicate of the twelve-question gallery plus outsider model, pipeline, and interface suggestions; non-prescriptive and unverified."
status: provisional
created: '2026-10-29'
updated: '2026-10-29'
topics:
  - exemplars
  - decision-support
  - representation
confidence: null
relations:
  - type: relates-to
    target: idea-end-state-question-gallery
  - type: relates-to
    target: question-model-node-ast-and-schema-representation
  - type: relates-to
    target: question-assumption-resolution-and-fallback-policy
---

# Outsider Commentary on Twelve End-State Questions

## Provenance and interpretation

The opening twelve questions duplicate [[idea-end-state-question-gallery]]. The subsequent proposed answer pipelines, architecture, equations, model choices, and closing suggested next steps are an outsider's commentary, NOT project requirements or accepted solutions.

- Imported on 2026-10-29 from `Queue/DozenQuestions.md`.
- Created/updated metadata dates describe this source record, not the original document.
- Original payload SHA-256 (including original line endings): `d9455a860dbd09042be269bc9b02fd6afd3a5db3cc1d74d9486a67a1e0b67347`.
- The original payload follows unchanged after the marker; line references to the original are relative to that payload.
- User clarification, 2026-10-29: Queue contains candidate questions and outsider thoughts, NOT prescriptive solutions. The outsider's identity, generation process, and full conversation provenance are not supplied; no author or model is inferred.

## Original document (verbatim)

<!-- ORIGINAL DOCUMENT:BEGIN -->

# Questions
1. Home / everyday optimization: Is it cheaper to keep my apartment at a constant temperature or heat it only when I am home, without making it less comfortable?
2. Life planning / personal trade-offs: Where should I live if I want more time with friends, better long-term health, and more disposable income—not simply a higher salary?
3. Personal finance / inverse planning: How much less could I work now if I were willing to retire three years later?
4. Manufacturing / constrained improvement: What single change to this factory would reduce both costs and emissions most, without increasing delivery failures?
5. Valuation / technological disruption: What is this company worth if AI makes its product ten times cheaper to deliver but also makes it much easier for competitors to copy?
6.Geopolitics / systemic shock: If Taiwan's semiconductor exports stopped for six months, which shortages would reach my business first, and what would happen to prices and employment?
7. Public health / distributional policy: Would this city save more lives by planting trees, installing reflective roofs, or subsidizing air-conditioning—and who would actually benefit?
8. Ecology / unexpected consequences: Could reintroducing a predator increase a region's carbon storage, and would the gains outweigh the costs to local farmers?
9. Engineering / design selection: Which battery chemistry should we use for delivery drones operating in cold weather if we also want to avoid fragile mineral supply chains?
10. Science / value of information: Which experiment should we run next to distinguish two competing explanations of a disease, given our budget and the cost of being wrong?
11. Society / general-equilibrium counterfactual: If a country moved to a four-day working week, what would happen to productivity, health, energy demand, housing, and tax revenue over ten years?
12. Model introspection / non-obvious exposure: Which seemingly unrelated event elsewhere in the world is the biggest hidden threat to my retirement portfolio—and which missing piece of knowledge could most change that answer?

# How answer the 12 questions
The common pattern is to turn each question into a **decision**, connect models across the relevant domains, and report both the recommended action and what could change it.

These are not questions that can be answered reliably from a single model. A building model does not know whether an apartment is comfortable; a financial model does not know which semiconductor a supplier uses; and an ecological model does not automatically know who bears the economic costs of reintroducing a predator.

I would design each answer around five objects:

1. **Decision and alternatives:** What can the user actually choose?
2. **Counterfactual:** What would happen without the proposed change?
3. **Connected model pipeline:** How does each model’s output become another model’s input?
4. **Decision rule:** What is being optimized, subject to which constraints?
5. **Uncertainty and information:** Which unknowns matter, and can another model or measurement resolve them?

Where the user has not supplied the necessary facts, the platform should produce a **conditional answer**, not invented numbers. Below, I describe the pipelines, inputs, outputs, and the assumptions I would try to replace with another identifiable model before asking the user to accept them.

---

## A general architecture for ConnectedModels

### A. Build a typed causal graph, not just a chain of answers

Each model should expose:

- **Inputs and outputs**, with units, geography, time resolution, and population or system boundaries.
- **Model identity:** equations, implementation and version, calibration data, applicable domain, and validation record.
- **Uncertainty:** parameter distributions, correlations, structural alternatives, and known missing mechanisms.
- **Causal status:** whether an output is an observed correlation, a forecast, or an estimated response to an intervention.
- **Constraints:** where the model is not valid and what downstream calculations should not infer from it.

For example:

> Weather → building heat transfer → heating-system efficiency → tariff cost  
> Occupancy → room temperature during occupancy → comfort  
> Heating controls → recovery timing and electrical peak

Each arrow needs a defensible transformation. A monthly national electricity price, for instance, is not interchangeable with a household’s hourly tariff, and a sector-level semiconductor dependency is not a supplier-specific bill of materials.

### B. Resolve assumptions systematically

For every consequential assumption, the platform should try the following in order:

1. **Observe it:** use the user’s records, sensors, public statistics, experiments, or supplier evidence.
2. **Infer it with an identifiable model:** for example, estimate a building’s thermal response from temperature and energy readings rather than assuming insulation quality.
3. **Compare competing models:** use several defensible structures when the evidence does not select one.
4. **Elicit irreducible preferences:** comfort tolerance, acceptable delivery-failure risk, or how a person values time with friends are not facts a physical model can discover.
5. **Represent remaining unknowns as scenarios or ranges:** do not disguise a guess as a prediction.

This cannot eliminate all assumptions. Models themselves require structural assumptions, and some preferences, rare-event probabilities, and causal effects may be unidentifiable from available evidence. The answer should make those limitations visible.

### C. Run counterfactuals consistently

Compare alternatives using:

- The **same baseline**, accounting period, prices, and population or functional unit.
- The same sampled weather, economic conditions, and other shared drivers where appropriate.
- Explicit feedback loops, delays, capacity constraints, and behavior changes.
- Joint uncertainty distributions rather than independent draws where variables are correlated.
- Backtesting and out-of-sample checks where historical data permit.

For interventions, observational associations should not automatically be treated as causal. Use experiments, credible natural experiments, mechanistic evidence, or explicit sensitivity analyses for confounding.

### D. Return a decision, not just a simulation

A useful answer should distinguish:

- **Best estimated choice** under the stated decision rule.
- **Feasibility:** whether each hard constraint is satisfied.
- **Uncertainty:** ranges, probabilities where defensible, and alternative model results.
- **Distribution:** who gains, who loses, and when.
- **Sensitivity:** the conditions that would reverse the recommendation.
- **Value of information:** whether a measurement or experiment is worth its cost before deciding.

“Best” is not always uniquely defined. If two objectives conflict and no defensible exchange rate exists, the platform should show a **Pareto frontier** and request a preference rather than manufacture a universal score.

---

# 1. Apartment heating: constant temperature or heat only when home?

## Decision

Choose a thermostat schedule that minimizes heating cost **without violating an agreed comfort standard while the user is home**. Compare at least:

- A constant occupied-temperature setpoint.
- A setback when away, with preheating before arrival.
- Several setback depths and recovery times.

“Heating only when home” should not be interpreted literally if the apartment needs time to warm up before arrival.

## Model pipeline

**Weather and occupancy → apartment thermal model → HVAC performance → tariff and billing model → comfort-constrained schedule optimization**

1. **Infer the apartment’s thermal dynamics.** Start with an energy-balance or resistance–capacitance model:

   \[
   C\frac{dT_{\text{in}}}{dt}
   = UA(T_{\text{out}}-T_{\text{in}})
   + Q_{\text{heat}}+Q_{\text{solar}}+Q_{\text{internal}}
   \]

   Estimate heat-loss coefficient \(UA\), effective thermal mass \(C\), and system response using indoor/outdoor temperatures and, ideally, heating-energy measurements. If sufficient building details exist, use a whole-building simulator such as [EnergyPlus](https://www.energy.gov/cmei/buildings/articles/energyplus).

2. **Model the heating system.** A resistance heater, boiler, district-heating system, and heat pump have different efficiencies, cycling behavior, and tariff structures. For a heat pump, estimate the coefficient of performance as a function of outside temperature and operating conditions; account for auxiliary resistance heat and defrost where relevant.

3. **Model cost.** Calculate energy at the time it is consumed using the actual tariff, including time-of-use rates and any demand charges. Distinguish apartment-level heat metering from rent-inclusive or building-wide heating charges: physical energy savings may not reduce the occupant’s bill.

4. **Model comfort.** Constrain temperature during occupied hours, including the arrival period and nighttime preferences. Include humidity, radiant temperature, drafts, or slow-warming surfaces if they materially affect the user. Standardized tools such as [ASHRAE Standard 55 comfort methods](https://www.ashrae.org/technical-resources/bookstore/standard-55-thermal-environmental-conditions-for-human-occupancy) can inform the assessment, but the occupant’s actual comfort is the final test.

5. **Optimize.** Search feasible schedules for the lowest expected cost over representative weather and occupancy scenarios, with a minimum-temperature constraint to avoid freezing or moisture problems.

## Answer and important caveat

For a simple heater with roughly constant efficiency and energy pricing, reducing indoor temperature while away usually reduces cumulative heat loss; reheating does not inherently erase those savings. But it is **not universally cheaper**: heat-pump efficiency, auxiliary heat, recovery timing, tariffs, and billing arrangements can reverse the result.

Report estimated annual savings and the probability that the apartment is comfortable on arrival, plus a practical test: run alternating schedules on comparable days and update the thermal model. If the result depends mostly on unknown preheat time, that measurement may be more valuable than a detailed simulation.

---

# 2. Where should I live for friendship, health, and disposable income?

## Decision

Compare feasible places to live, including staying put, over a specified horizon. The objective is not maximum salary; it is a personalized trade-off between **actual financial resources, opportunities for social connection, and long-term health**.

## Model pipeline

**Candidate locations and jobs → after-tax household budget → social-access and time model → health-exposure model → personalized multi-objective choice**

1. **Generate feasible alternatives.** Use housing availability, legal or immigration constraints, job locations, remote-work policies, household needs, and accessibility. An urban location-choice model such as [UrbanSim](https://cloud.urbansim.com/docs/general/documentation/urbansim.html) can inform the housing and accessibility side, but it cannot decide what the user values.

2. **Calculate disposable resources.** For each location, model salary *conditional on the jobs actually available*, taxes and benefits, housing, transport, insurance, healthcare, childcare, and moving costs. Use local tax-and-benefit rules rather than nominal tax rates.

3. **Estimate time with friends.** Use the locations of relevant friends, realistic travel times, schedules, and the probability that people are available. A simple interaction model might estimate:

   \[
   \mathbb{E}[\text{social hours per month}]
   = \sum_j P(\text{meeting }j \mid
   \text{travel time, schedules, relationship})
   \times \text{duration}_j
   \]

   Calibrate with the user’s current behavior if possible. Geographic proximity alone is not proof that a friendship will become more active.

4. **Estimate health effects.** Connect transport and activity patterns, air pollution, heat, injury risk, healthcare access, and relevant baseline health to exposure-response or health-state models. Research has linked land-use and transport microsimulation to physical activity, pollution, and traffic injury impacts; such models require local calibration and do not establish that every association is causal ([example](https://doi.org/10.1016/j.jth.2023.101707)).

5. **Combine outcomes without hiding trade-offs.** Show a Pareto frontier across disposable income, expected social time, and health outcomes. If the user supplies preferences, a multi-attribute utility model can select a preferred option. Alternatively, use constraints such as “at least two friend visits per month” and “no less than a specified annual savings amount.”

## Answer

Return a short list of locations, not just a winner: estimated disposable income, available social time, health indicators, one-time moving costs, and uncertainty for each. Show which locations are dominated and which trade-offs remain genuinely subjective.

**Likely decisive missing information:** whether friends will remain in those locations and how frequently they are willing and able to meet. A scenario based on actual conversations may outperform an elaborate proximity model.

---

# 3. How much less could I work now if I retire three years later?

## Decision

Compare the current plan with plans that reduce work now and retire three years later, while preserving an agreed retirement standard and acceptable financial risk.

The platform must clarify whether “less” means fewer hours each week, fewer working years before the delayed retirement, or lower-intensity work. Those have different benefit and earnings consequences.

## Model pipeline

**Work schedule → earnings and benefits → taxes and savings → retirement cash flows → market/longevity simulation → constrained inverse optimization**

1. **Project earnings under alternative hours.** Estimate the relation between hours and pay, including nonlinearities such as overtime, part-time pay rates, promotions, employer pension contributions, and loss of insurance. A simple proportional wage model is a starting point, not a default truth.

2. **Model household cash flows.** Apply current jurisdiction-specific tax, pension, benefit, and retirement-account rules. Include debts, partner income, dependent costs, healthcare, and any required minimum contributions.

3. **Project assets and retirement spending.**

   \[
   A_{t+1}=(A_t+S_t)(1+r_{t+1})-W_{t+1}
   \]

   Here \(S_t\) is net saving and \(W_t\) is withdrawal; the implementation must handle timing, taxes, account types, and inflation consistently. Simulate correlated returns, wage shocks, inflation, health costs, and longevity.

4. **Invert the plan.** Search for the largest feasible hours reduction, \(\Delta h\), such that the delayed-retirement plan meets the user’s chosen constraints—for example, a target spending level and a specified probability of avoiding depletion. Compare with the baseline under the **same scenarios**.

5. **Add lifecycle choices if needed.** A dynamic-programming framework can model work, saving, claiming, and retirement as decisions that adapt to future health and finances. [Rust’s retirement model](https://www.nber.org/papers/w2470) is a foundational example; it is not a turnkey personalized forecast.

## Answer

Report a range such as “under these assumptions, approximately X–Y fewer hours per week,” with effects on take-home pay, benefits, retirement date, and financial shortfall risk. Also show a stress case in which the user cannot work the extra three years.

**Most important unknowns to resolve:** employer part-time terms, benefit eligibility, retirement spending, and the actual pension formula. No numerical reduction is defensible without them.

---

# 4. Which single factory change best reduces cost and emissions without increasing delivery failures?

## Decision

Select **one implementable intervention** from an explicit candidate set. “Single change” must have a defined scope: replacing one machine, changing a setpoint, rescheduling a shift, or repairing a compressed-air leak are not necessarily comparable without capital and implementation boundaries.

## Model pipeline

**Process and orders → production/queueing model → energy and materials model → cost and emissions accounting → delivery-risk evaluation → constrained selection**

1. **Reconstruct the factory baseline.** Map the bill of materials, routing, machine cycle times, scrap, energy use, downtime, buffers, staffing, supplier reliability, and delivery deadlines.

2. **Model production and reliability.** Use a discrete-event simulation or a suitable queueing/production-line model to capture bottlenecks, maintenance, blocking, starvation, variability, and order priorities. For a simpler serial line, a [Bernoulli-reliability production model](https://www.nist.gov/publications/reducing-energy-consumption-serial-production-lines-bernoulli-reliability-machines) is one identifiable starting point, subject to its assumptions.

3. **Model interventions.** For each candidate, change only the relevant parameters: machine reliability, yield, energy intensity, cycle time, maintenance demand, etc. Include implementation downtime and transition risk.

4. **Calculate costs and emissions.** Include capital, maintenance, labor, materials, scrap, energy, and the appropriate time-varying emissions factors. State the emissions boundary—on-site, purchased energy, and/or upstream—and avoid counting shifted emissions as eliminated.

5. **Enforce the delivery constraint.** Compare the probability or rate of late or failed deliveries with the baseline under shared demand and disruption scenarios. A practical robust rule might require the upper confidence bound on the increase in failure rate to be no greater than an agreed tolerance. Exactly proving *zero* increase is generally impossible with finite data.

6. **Select the change.** First discard interventions that fail the delivery constraint or do not reduce both cost and emissions. Among the remainder, rank by a user-specified valuation of cost and emissions, or show the Pareto frontier if no trade-off has been agreed.

## Answer

Return the best feasible intervention, expected annual cost and emissions changes, delivery-risk impact, implementation cost, and conditions under which it stops being preferred.

**Key limitation:** “reduce both most” may not have a unique answer. One change may save more money while another saves more carbon. The platform must not invent a carbon price or silently prioritize one.

---

# 5. What is a company worth if AI cuts delivery cost tenfold but makes copying easier?

## Decision

Estimate enterprise and equity value under a specified technological and competitive scenario. A tenfold reduction in delivery cost is not a tenfold increase in value: prices, demand, competitor entry, switching costs, and reinvestment all matter.

## Model pipeline

**AI cost shock → customer demand and pricing → competitor entry and market-share dynamics → operating cash flows → valuation**

1. **Disaggregate the cost base.** Identify which cost per unit becomes one-tenth of its original level, which costs remain fixed, and what additional inference, training, quality assurance, security, or customer-support costs arise. “Ten times cheaper to deliver” should be applied only to the specified cost component.

2. **Model demand and pricing.** Estimate customer willingness to pay, price elasticity, substitution, and adoption. Explore whether cost savings are retained as margin, passed to customers, or expand the market.

3. **Model competition.** Use an industry-entry or differentiated-product pricing model, calibrated where possible from comparable disruptions and the company’s actual distribution, data, brand, contracts, regulation, and switching costs. Vary the rate at which excess margins fade; do not assume every competitor gains the same capabilities immediately.

4. **Forecast free cash flow.** Model revenue, operating costs, taxes, working capital, capital expenditure, and reinvestment by scenario. Account for implementation risks, cannibalization, and any changes to product quality.

5. **Value consistently.**

   \[
   EV=\sum_{t=1}^{T}\frac{\mathbb{E}[FCF_t]}{(1+r)^t}
   +\frac{TV_T}{(1+r)^T}
   \]

   Convert enterprise value to equity value using net debt and other relevant claims. Keep cash-flow risk and discount-rate treatment consistent; do not double-count downside by embedding the same risk in both severely reduced cash flows and an unjustifiably high discount rate. A multistage DCF with explicit fade of excess returns is a useful scaffold; NYU’s [valuation readings](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/eqread.htm) cover competitive-advantage duration.

6. **Check optionality.** If management can delay, expand, license, or abandon an investment, a real-options model may be informative—but only if its decisions and payoffs are not already captured in the DCF.

## Answer

Show valuations under at least: cost savings retained, savings largely competed away, and a larger market with lower prices. Decompose the change in value into cost, pricing, volume, and reinvestment effects.

**Most valuable evidence:** the fraction of costs truly affected and evidence about customer switching, distribution, and competitor entry. Without company financials and those inputs, the result is a framework—not a defensible valuation.

---

# 6. If Taiwan’s semiconductor exports stop for six months, what reaches my business first?

## Decision

Identify the first likely operational shortages, their timing, and the consequences for the business and relevant wider economy. Distinguish **a six-month export stop** from a six-month interruption of chip production, global chip supply, or semiconductor exports from elsewhere.

## Model pipeline

**Shock definition → chip-level supply network → inventories and lead times → production allocation and substitution → prices, output, and employment**

1. **Map exposure.** Link the business’s products and equipment to components, chip types, suppliers, fabrication and packaging locations, and alternative sources. Use bills of materials, supplier disclosures, customs records, and procurement data. OECD’s work on [semiconductor supply-chain vulnerabilities](https://www.oecd.org/en/publications/vulnerabilities-in-the-semiconductor-supply-chain_6bed616f-en.html) provides a starting point for network mapping.

2. **Model time to disruption.** For each critical component:

   \[
   \text{time to potential stockout}
   \approx
   \frac{\text{usable inventory}}{\text{net consumption rate}}
   \]

   Then refine for goods already in transit, contractual allocation, safety stocks held by suppliers, replacement qualification, and possible demand changes.

3. **Propagate through the network.** Use a dynamic, capacity-constrained production-network model that includes inventory depletion, bottlenecks, rationing, substitution, and delays. Sector-level [OECD inter-country input–output tables](https://www.oecd.org/en/data/datasets/inter-country-input-output-tables.html) can help identify indirect dependencies, but fixed-coefficient input–output analysis alone cannot reliably predict chip-specific shortages or prices.

4. **Estimate price responses.** Model constrained supply against demand, contractual pricing, spot exposure, and supplier bargaining. Price paths should be scenarios when elasticities and allocation rules are poorly known, not precise point forecasts.

5. **Estimate employment effects.** Translate production shortfalls into hours, overtime, furloughs, layoffs, and supplier effects using firm and sector labor-adjustment models. Differentiate temporary hours reductions from permanent job losses and allow for policy support.

6. **Simulate recovery.** Six months of interruption may cause a longer backlog. Model restart capacity, equipment and logistics constraints, order prioritization, and substitution that persists after exports resume.

## Answer

Present a timeline by component and business operation: earliest likely stockout, production at risk, alternative sources, and price exposure. Separately show wider industry price and employment scenarios.

**Highest-priority information:** the business’s multi-tier chip mapping and inventory. If supplier data are missing, the platform should show exposure as unknown—not infer a specific chip origin from a broad industry category.

---

# 7. Trees, reflective roofs, or air-conditioning subsidies: which saves more lives, and who benefits?

## Decision

Compare interventions against a common baseline, budget, geography, and time horizon. The policy packages must be operationally specified: for example, number and placement of trees, roof area and reflectivity, or subsidy eligibility and electricity support.

## Model pipeline

**Policy design → neighborhood heat and indoor exposure → population-specific health risks → deaths avoided → cost and distribution**

1. **Model implementation.** Estimate adoption, location, installation timing, maintenance, tree growth and survival, housing eligibility, and landlord or tenant participation.

2. **Model exposure.** Couple urban climate or heat-island models to building thermal models. Trees alter shade and, potentially, local temperatures; reflective roofs affect building and neighborhood heat; air-conditioning changes indoor exposure but consumes electricity and may increase outdoor waste heat. Local climate, building type, and grid conditions matter.

3. **Model health impacts.** Link hourly or daily exposure to locally calibrated heat–mortality relationships, including delayed effects where supported. Use age, baseline mortality, health status, and exposure vulnerability. An EPA-authored [heat-mortality assessment framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC6266381/) illustrates how to combine climate, population, and health-response uncertainty.

4. **Track distribution.** Report benefits by neighborhood, income, age, disability, housing tenure, baseline exposure, and intervention access. Estimate who pays energy bills, who can use a subsidy, and whether tree benefits arrive only after years of growth.

5. **Include system effects.** Model electricity demand, outages during heat waves, emissions, maintenance, water use, and possible winter heating penalties from reflective roofs. Avoid assuming that a subsidized unit is installed, powered, and used.

6. **Optimize under a fixed budget.** Compare deaths avoided over a stated period and, if appropriate, deaths avoided per public dollar. A spatial multi-objective model such as [City-HEAT](https://repository.library.noaa.gov/view/noaa/57567) illustrates the combination of intervention placement, health, costs, and equity.

## Answer

Return a citywide ranking **and** a map or table of distributional effects. The preferred choice may be different for immediate heat waves than for a 30-year horizon, and the best overall portfolio may combine approaches.

**Critical uncertainty:** indoor exposure and actual air-conditioner usage among high-risk people. A household survey or targeted pilot can materially change the ranking.

---

# 8. Could a predator increase carbon storage enough to outweigh costs to farmers?

## Decision

Compare reintroduction with a credible no-reintroduction baseline, accounting for ecological outcomes, carbon persistence, farmer losses, and the distribution of costs and benefits.

## Model pipeline

**Predator reintroduction → food-web dynamics → vegetation and carbon pools → climate valuation → farm and implementation economics**

1. **Model the food web.** Estimate predator population, prey abundance and behavior, livestock interactions, and vegetation response. Use field evidence and a dynamic food-web model, potentially [Ecopath with Ecosim or Rpath](https://noaa-edab.github.io/Rpath/), if appropriate to the ecosystem and data.

2. **Translate ecological change into carbon.** Model above- and below-ground biomass, soils, decomposition, fire, and land-use change. Track carbon stocks and fluxes explicitly. The proposed causal pathway—predator → prey behavior or abundance → vegetation → carbon—is plausible in some settings but not universal; the [sea otter–kelp case study](https://doi.org/10.1890/110176) is an illustration, not a transferable coefficient.

3. **Account for permanence and leakage.** Compare carbon changes with the no-predator baseline, incorporate fire or reversal risk, and consider whether displaced grazing or production increases emissions elsewhere. Convert carbon to CO₂-equivalent consistently, including relevant non-CO₂ gases where material.

4. **Model farmer costs.** Estimate livestock losses, guarding, fencing, veterinary costs, changes in grazing practices, insurance, and the effectiveness and cost of mitigation. Include public administration and monitoring costs.

5. **Evaluate welfare and distribution.** Compare discounted costs and benefits over the same horizon. If assigning a monetary value to carbon, show the chosen valuation and sensitivity to alternatives. Separately report benefits and costs to farmers, residents, government, and others: aggregate net benefit does not guarantee that farmers are compensated.

## Answer

Provide a probability distribution for additional durable carbon, the range of farm costs, and the conditions under which net benefits are positive. If the comparison depends on an uncertain trophic cascade, explicitly present a scenario in which the predator has little or even adverse carbon impact.

**Most useful next evidence:** local measurements of prey behavior and vegetation recovery, alongside a credible estimate of livestock losses and mitigation effectiveness.

---

# 9. Which battery chemistry suits cold-weather delivery drones without fragile mineral supply chains?

## Decision

Choose among **specific cells and pack designs**, not chemistry labels alone. The relevant functional unit is a successful delivery mission at the required payload and temperature, with adequate safety and service life.

## Model pipeline

**Mission profile → temperature-dependent cell and pack behavior → drone flight/thermal model → safety and lifetime → supply-chain stress → constrained choice**

1. **Define the mission.** Payload, distance, wind, altitude, reserve requirement, ambient temperature, turnaround time, charging access, and allowed battery mass.

2. **Model cold-weather cell performance.** Use manufacturer data and laboratory measurements for usable energy, internal resistance, power capability, charge limits, and degradation at relevant temperatures and states of charge. Couple an electrical and thermal cell model to propulsion and flight-energy requirements; include pack insulation or heating and the energy it consumes.

3. **Assess feasible missions.** Calculate whether each candidate can deliver the required power throughout the flight, land with reserve, and recharge safely. A high nominal energy density is not enough if cold-weather voltage sag or heating needs make the mission infeasible.

4. **Estimate lifetime and cost.** Model cycles, calendar aging, replacement frequency, charging infrastructure, and maintenance. [BLAST-Lite](https://github.com/NatLabRockies/BLAST-Lite) is one identifiable battery-aging tool, but its models have documented limits and do not by themselves establish cold-weather flight range or safety.

5. **Assess mineral and manufacturing exposure.** Map material requirements and actual supplier tiers, including refining and cell manufacturing—not merely mine locations. Stress geographic concentration, export restrictions, substitution, lead times, and supplier qualification. DOE’s [critical-materials assessment methodology](https://www.energy.gov/cmm/what-are-critical-minerals-and-materials) and [BLEECAM](https://www.nlr.gov/critical-minerals/bleecam) are relevant starting points.

6. **Evaluate environmental trade-offs.** If emissions are part of the choice, use a consistent lifecycle boundary and a tool such as [R&D GREET](https://www.energy.gov/cmei/rd-greet-life-cycle-assessment-model), with mission and pack lifetime reflected in the functional unit.

7. **Select with constraints.** Eliminate options that fail mission, safety, certification, or charging requirements. Compare remaining options on cost per successful delivery, lifetime, and supply-disruption risk; show a frontier if trade-offs remain.

## Answer

Return the best qualified cell/pack candidate, the temperatures and missions for which it works, supply-chain vulnerabilities, and laboratory tests needed before procurement.

**Do not select a chemistry from generic reputation alone.** A particular cell’s low-temperature power and the drone’s mass sensitivity may dominate its broad chemistry category.

---

# 10. Which experiment best distinguishes two disease explanations, given budget and cost of error?

## Decision

Choose an experiment—or choose not to run one—that maximizes expected improvement in the downstream decision, net of study and delay costs, subject to budget and ethical constraints.

Distinguishing explanations is useful only insofar as it improves a decision, unless scientific discrimination is itself the agreed objective.

## Model pipeline

**Competing disease models → predictions for possible experiments → posterior updating → downstream decision utility → expected value of sample information**

1. **Specify hypotheses and alternatives.** Define \(H_1\) and \(H_2\), their mechanisms, observable predictions, parameter uncertainty, and a model-checking plan. If neither hypothesis explains the data well, allow for an “other or misspecified” possibility rather than forcing certainty between two wrong explanations.

2. **Generate candidate designs.** Vary intervention, comparison group, measurements, sample size, duration, recruitment population, and randomization. Include confounding, measurement error, missingness, and feasible recruitment.

3. **Predict results and update beliefs.** For each design \(e\), simulate outcomes \(y\) under the competing models and update:

   \[
   P(H_i\mid y,e)
   \propto P(y\mid H_i,e)P(H_i)
   \]

4. **Connect to the actual decision.** Define actions—such as choosing a treatment, funding a program, or collecting more evidence—and their consequences under each possible disease state. Include the harm of incorrect action and the harm of waiting.

5. **Calculate expected value of sample information.** With utility \(U\), action \(a\), and unknown state \(\theta\):

   \[
   EVSI(e)=
   \mathbb{E}_{y\mid e}\left[
      \max_a \mathbb{E}[U(a,\theta)\mid y,e]
   \right]
   -\max_a \mathbb{E}[U(a,\theta)]
   \]

   Choose a feasible design that maximizes EVSI minus study costs and any decision-relevant delay costs not already included in \(U\). [NIST’s Bayesian optimal experimental design work](https://www.nist.gov/publications/optimal-bayesian-experimental-design) and this [EVSI methods review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9189720/) provide identifiable methodological starting points.

6. **Check robustness and ethics.** Vary priors, effect sizes, model misspecification, enrollment, adherence, and implementation of the study’s eventual recommendation. Require appropriate safeguards and approvals for human research.

## Answer

Return the recommended design, cost, expected decision improvement, chance of changing the decision, expected duration, and comparison with alternatives. A smaller study can beat a more statistically informative one if it is faster or addresses the decision more directly.

**If all net values are negative, recommend acting now or improving existing evidence rather than running an experiment.**

---

# 11. What happens over ten years if a country moves to a four-day working week?

## Decision

Evaluate a precisely specified policy against a no-policy baseline over ten years. The first distinction is essential:

- **Compressed schedule:** roughly the same weekly hours over four days.
- **Reduced hours:** fewer weekly hours, with or without the same weekly pay.

Coverage, implementation timing, exemptions, overtime, enforcement, and public-sector rules can change the result substantially.

## Model pipeline

**Policy design → firm and worker responses → economy-wide production and prices → household and health outcomes → energy, housing, and fiscal feedback**

1. **Estimate direct workplace effects.** Use causal evidence from comparable trials or natural experiments to estimate changes in output per hour, output per worker, absenteeism, turnover, staffing needs, and wages. Represent differences across sectors and jobs. Do not extrapolate volunteer-pilot results uncritically to every employer.

2. **Model labor and production adjustment.** Firms may reorganize tasks, hire additional workers, reduce output, change prices, or increase automation. Workers may take second jobs or change labor-force participation. A dynamic computable general equilibrium model can connect sectors, wages, trade, investment, and prices; the World Bank describes [CGE and MANAGE-WB frameworks](https://www.worldbank.org/en/programs/economicpolicy-macro-modeling/cge). Model closure and labor-market assumptions must be explicit.

3. **Connect household microsimulation.** Translate wages, hours, job changes, prices, taxes, and benefits to different households, including those not covered by the policy. CGE–microsimulation approaches can expose distributional effects that a representative household would hide ([example](https://euromod-web.jrc.ec.europa.eu/research/publications/keeping-best-two-worlds-linking-cge-and-microsimulation-models-policy)).

4. **Model health and time use.** Connect changes in work stress, sleep, physical activity, care work, income, and unemployment risk to health outcomes using the best available causal evidence. Account for possible adverse effects of compressed longer days.

5. **Model energy demand.** Feed commuting, workplace occupancy, home heating and cooling, leisure travel, production levels, and electricity demand into transport and building-energy models. A shorter workweek does not automatically mean lower total energy use.

6. **Model housing.** Use location choice, commuting frequency, household income, and housing supply constraints to estimate effects on rents, prices, and residential location. Housing adjusts slowly, so annual feedback with the wider model matters.

7. **Model public finances.** Recalculate income and payroll taxes, consumption and corporate taxes, transfers, healthcare spending, and public-sector staffing costs. State whether government spending, deficits, tax rates, or some combination adjusts: those are consequential model-closure choices.

8. **Iterate and test.** Reconcile prices, employment, demand, and fiscal responses across models; check convergence and preserve uncertainty about feedback strengths. Compare outcomes annually over the ten years.

## Answer

Report productivity **per hour and per worker**, employment and hours, health, energy demand, housing costs, tax revenue, and distributional outcomes under several plausible behavioral scenarios. Show transition effects separately from year-ten outcomes.

There is no defensible single forecast without the policy specification and country. If effects differ sharply between compressed and reduced hours, those should be presented as different policies, not as uncertainty around one policy.

---

# 12. What unrelated global event is my portfolio’s biggest hidden threat, and what missing knowledge could change that answer?

## Decision

Search for plausible, non-obvious events that could materially harm the user’s retirement plan, then identify which unresolved fact has the highest **decision-relevant value of information**.

“Biggest threat” must be defined: largest plausible loss, greatest expected loss, largest contribution to tail risk, or greatest chance of undermining retirement spending can produce different answers.

## Model pipeline

**Portfolio look-through → economic dependency network → event generation → shock transmission → portfolio and retirement-plan loss → information-value analysis**

1. **Look through the portfolio.** Identify underlying holdings in funds, issuer and sector exposures, geographic revenue, currencies, interest-rate duration, credit, liquidity, derivatives, and concentration. For retirement outcomes, include contributions, withdrawals, pensions, and other household exposures—not just the brokerage account.

2. **Build a dependency graph.** Connect holdings to supply chains, energy inputs, customers, insurers, transport routes, financing, and common factors. A global event can create hidden exposure through shared dependencies even when the portfolio appears diversified by sector or geography.

3. **Generate a structured event set.** Use historically informed and expert-designed scenarios: for example, a disruption in a critical shipping route, an energy shock, a concentrated supplier failure, or a sovereign funding stress. Use a production-network or macro model to map real-economy effects, then asset-pricing, credit, currency, and interest-rate models to map financial effects.

4. **Calculate portfolio and plan impact.** Revalue holdings under each scenario, including correlations, nonlinear instruments, liquidity, and possible hedges. Feed losses and recovery paths into the retirement cash-flow model in question 3. Use scenario loss, expected shortfall, or retirement shortfall risk as appropriate; [IMF stress-testing methods](https://www.elibrary.imf.org/display/book/9781484368589/9781484368589.xml) provide a useful methodological reference.

5. **Rank carefully.** A stress scenario shows conditional consequences; it does **not** establish how likely the event is. Rank by probability-weighted loss only where probabilities are credible, and separately show severe scenarios with poorly known probabilities. Do not claim the “biggest event in the world” has been found from a limited scenario library.

6. **Find the missing fact that matters most.** For uncertain facts—such as actual fund look-through, supplier concentration, revenue exposure, or the user’s pension guarantee—estimate how learning the fact would change the best protective action. Calculate expected value of information using the same principle as question 10, net of the cost of obtaining it.

## Answer

Return:

- The largest **identified** threat under the chosen risk measure and scenario set.
- Its causal path from event to holdings to retirement outcome.
- The exposures that make it non-obvious.
- The uncertainty in both the loss and event probability.
- The missing fact most likely to change the recommended action, and how to obtain it.

A variable can greatly change the estimated loss yet have little decision value if the recommended action would remain the same. Conversely, a modest uncertainty near a decision threshold can be worth investigating.

---

## What a complete ConnectedModels answer should look like

For any of these questions, I would make the final result inspectable at three levels:

1. **Decision summary:** recommended action, feasible alternatives, key trade-off, and confidence.
2. **Causal explanation:** a readable graph showing how inputs propagate across domains, when effects occur, and who is affected.
3. **Model audit:** data sources and dates; model versions; equations or documentation; calibration and validation; unresolved assumptions; sensitivity and value-of-information results.

The platform’s central promise should be **traceable conditional reasoning**, not the appearance of certainty. Its strongest answers will be those that can say both “this is the best choice under these conditions” and “here is the observation that would most likely make us change our minds.”

A useful next step would be to turn these examples into a common model-interface specification.

