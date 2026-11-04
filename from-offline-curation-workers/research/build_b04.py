"""Solution and infusion arithmetic plus a signed postpartum body-mass definition."""
import json
from build_b01 import ROOT, DAY, variable as v, source, reference as ref, rejection as reject, record
from build_b02 import UNKNOWN_RIGHTS, SHORT_REDIST
from build_b03 import SACN_PDF

NOTTINGHAM = "https://www.nottingham.ac.uk/medicine/documents/gem-documents/gem-science-workbook.pdf"
NOTT_VERSION = "Medical Sciences & Graduate Entry Medicine Basic Science Workbook, cover September 2022–23; 92 PDF pages"
NOTT_LICENSE = ("No reusable-content license established; terms unknown. Printed p7 notes Maths for Medicine reproduced with permission of Dr J Koenig; "
                "that statement does not authorize this curator to redistribute the source. Full workbook, images and copied explanatory passages are excluded.")

def ns(id, locator, evidence):
    return source(id, "University of Nottingham School of Medicine: Basic Science Workbook", NOTTINGHAM,
                  NOTT_VERSION, locator, evidence, NOTT_LICENSE, SHORT_REDIST)

def main():
    path = ROOT / "returns/clinical-arithmetic-codex-b04/bundle.json"
    batch = json.loads(path.read_text(encoding="utf-8"))
    batch["created"] = DAY
    models = []
    ctx = ("Same identified active constituent and homogeneous liquid formulation sample, final sample volume, temperature and composition state. "
           "Clinical application is a supplied drug formulation on a consistent active-moiety basis. This is a concentration definition without patient-population calibration or administration advice.")
    models.append(record(
        "constituent-mass-concentration", "Mass concentration of a constituent in a liquid formulation",
        "Defines active-constituent mass per total final formulation volume. This is partial mass concentration, not total bulk liquid density. In the clinical profile the constituent is the specified active drug.",
        "definition", "C", "m / V", "C = D / V (concentration = drug amount / solution volume)", "nott-concentration", "Topic 1, 2.d, printed p18 (PDF index17), answer to practice question 3, explicit C=D/V; concentration discussion in 2.b",
        "Source D denotes drug amount; introduced m renames it to a constituent mass independent of an ordered dose. Preserve source C and V. "
        "m is kg and V is final solution m^3, making C kg/m^3; dimensions M/L^3=M L^-3. The same kg base scale appears in m and C, so m/V is canonical without a conversion literal. "
        "C is an independently meaningful scientific quantity and can normalize the H/Q stock-strength pair in b02, but the present record is a definition rather than an extra multiplication operator split from that model. "
        "The generic building-energy density record counts the substance's total mass per occupied sample volume; here the numerator counts one constituent while the denominator is the full mixture volume. A unit match does not prove equivalence.",
        [v("m", "Introduced m maps to drug amount D in C=D/V", "input", "constituent_mass", "Mass of the identified constituent contained in the entire specified formulation sample, not total mixture mass.", "kg", "M", ctx, "Finite nonnegative; zero represents a blank carrier sample with no selected constituent."),
         v("V", "V", "input", "solution_volume", "Total final volume of the same homogeneous liquid formulation, including constituent and carrier effects.", "m^3", "L^3", ctx, "Finite strictly positive; not merely solvent volume added before dissolution."),
         v("C", "C", "output", "mass_concentration", "Mass of one identified constituent divided by total final solution volume.", "kg/m^3", "M L^-3", ctx, "Finite nonnegative; active-moiety definition, phase and formulation conditions must be specified.")],
        ["m >= 0", "V > 0"],
        ["Source definition: the medical arithmetic workbook explicitly gives C=D/V for drug mass and solution volume.",
         "Application profile: one homogeneous liquid formulation, defined constituent/active moiety and final volume. No clinical age, pregnancy or disease validation is supplied by a concentration identity."],
        ["Bulk density, mass fraction, molarity and pharmacological potency are distinct quantities; no unit-only substitution is authorized.",
         "Does not establish solubility, stability, product identity or whether a formulation is suitable for a patient. Reconstitution diluent volume may differ from final volume."],
        [ns("nott-concentration", "Topic 1, 2.b concentration units; 2.d answer 3, printed p18/PDF index17", "Explicitly defines C as drug amount divided by final volume and supplies a 380 mg, 152 mL, 2.5 mg/mL worked set.")],
        [ref("published-worked-set-reversed", {"m":0.00038,"V":0.000152}, 2.5, 1e-10,
             "Value derived from published worked data: the example states concentration 2.5 mg/mL and computes 152 mL for 380 mg. Use the independently reported concentration as expected (2.5 kg/m^3), rather than calling this a measured sample. Inputs and result are exact pedagogical numbers; tolerance covers arithmetic representation only.", "Nottingham workbook, Topic1 2.d answer 3, printed p18, PDF index17."),
         ref("independent-aliquot-count", {"m":0.000125,"V":5e-6}, 25, 1e-10,
             "Independent synthetic partition: five equal 1 mL portions sharing 125 mg contain 25 mg each, hence 25 mg/mL =25 kg/m^3. This checks the constituent-per-total-volume meaning and scale; it is not an empirical concentration validation.", "Curator-created aliquot-count example."),
         ref("blank-sample", {"m":0,"V":5e-6}, 0, 1e-20,
             "Definitional blank-carrier boundary: positive sample volume with no selected constituent has zero mass concentration.", "Curator limiting identity.")],
        [reject({"m":0.000125,"V":0}, "A zero-volume sample cannot define this concentration."),
         reject({"V":5e-6}, "Selected constituent mass is missing.", "missing-input")],
        "Target m: known C>=0,V>0 give m=C*V uniquely. Check C=25 kg/m^3,V=5e-6 m^3 gives m=0.000125 kg and forward C=25. C=0 gives m=0 uniquely. Target V: known m>0,C>0 give V=m/C>0. With m=C=0, every V>0 fits, so V is not identified; m>0 with C=0 has no finite positive-volume solution; m=0,C>0 would require V=0 and is excluded. Retain original constituent/final-volume context; inversion does not authorize a formulation change.",
        ["Need constituent_mass, solution_volume and mass_concentration meanings and m^3/kg/m^3 units with matching kg scale; kg already exists.",
         "Possible alias of b02 labeled_active_drug_reference_mass/volume is conditional on actual constituent and final-stock semantics. It is not an automatic binding; inventory mass_density describes a different numerator support."]
    ))

    ctx = ("Same identified conserved solute/active moiety, initial liquid aliquot and final diluted liquid mixture at specified conditions. "
           "Final volume is supplied as a final measured/defined value, not assumed from additive ingredient volumes. Clinical use requires an independently authorized compatible diluent/formulation; no patient-population calibration is claimed.")
    models.append(record(
        "solute-conserving-dilution", "Mass concentration after solute-conserving dilution",
        "Maps initial concentration and aliquot volume to final concentration when only solute-free diluent is added and the selected solute mass is conserved. It does not choose a drug, dilution target or preparation procedure.",
        "theoretical", "C2", "C1 * V1 / V2", "C1 V1 = C2 V2 for unchanged solute amount during dilution", "openstax-dilution", "Chemistry 2e, section 3.3 Molarity, Dilution of Solutions, general concentration-volume form and unchanged-solute explanation",
        "Source general C and V notation is preserved with initial/final subscripts serialized as C1,V1,C2,V2. Source explains conservation for amount concentration and explicitly allows other mutually consistent concentration/volume units. "
        "This record uses mass concentration of one conserved solute; C1*V1 and C2*V2 are its mass. Both C values are kg/m^3 and volumes are m^3, so C2 is kg/m^3 and the runtime mass scale cancels consistently. Dimensions: (M L^-3)*L^3/L^3=M L^-3. "
        "No assumption of additive solution volumes is needed because V2 is the final supplied volume. V2>=V1 declares the dilution/no-change profile, excluding concentration by evaporation. "
        "Unlike the b02 desired-over-have definition, two states of one conserved solute are related here; no independent prescription amount is a port.",
        [v("C1", "C1, initial concentration", "input", "mass_concentration", "Mass concentration of the identified conserved solute in the starting aliquot.", "kg/m^3", "M L^-3", ctx, "Finite nonnegative. Zero is the blank-solute limit; no solute is introduced by the diluent."),
         v("V1", "V1, initial volume", "input", "solution_volume", "Positive volume of the initial homogeneous aliquot actually transferred into the dilution.", "m^3", "L^3", ctx, "Finite strictly positive; not total bottle volume if only an aliquot is transferred."),
         v("V2", "V2, final volume", "input", "solution_volume", "Total final diluted formulation volume after mixing, supplied independently.", "m^3", "L^3", ctx, "Finite and at least V1; positive follows from V1>0. Equality is the no-dilution identity boundary."),
         v("C2", "C2, final concentration", "output", "mass_concentration", "Mass concentration of the same conserved solute in the final homogeneous mixture.", "kg/m^3", "M L^-3", ctx, "Finite nonnegative and no greater than C1 in the declared dilution profile.")],
        ["C1 >= 0", "V1 > 0", "V2 > 0", "V2 >= V1"],
        ["Source assumption: dilution preserves the chosen solute amount; its concentration-volume products are equal before and after adding solute-free solvent.",
         "Application profile: selected solute is neither added, lost, reacted, precipitated nor selectively adsorbed; the initial aliquot and final mixture are homogeneous on the specified sampling supports.",
         "Clinical profile: authorized compatible formulation and final volume are external; this is conservation arithmetic without a therapeutic validation population."],
        ["Not applicable to adding another active-solute solution, chemical conversion, losses, incomplete transfer or a concentration-by-solvent-removal process.",
         "Does not calculate final volume by adding solvent and solution volumes; no drug compatibility, stability, sterility or preparation recommendation follows."],
        [source("openstax-dilution", "OpenStax: Chemistry 2e, 3.3 Molarity", "https://openstax.org/books/chemistry-2e/pages/3-3-molarity", "Chemistry 2e, live HTML inspected 2026-11-03; footer licensing on accessed version applies", "Dilution of Solutions; general C1 V1 = C2 V2 form following solute conservation", "Relates initial and final concentration-volume products when dilution leaves the solute amount unchanged and permits consistent alternative concentration units.", "Accessed section Citation/Attribution states CC BY-NC-SA 4.0 and additional restrictions on ingestion/use in AI offerings without written permission; same-page licensing section inspected 2026-11-03. No inference of downstream AI/commercial redistribution permission is made.", "Only an independently written mathematical/conservation formalization and original short paraphrase are returned; no textbook pages/images/long passages. Applicable source-content restrictions remain explicit and downstream clearance is not claimed."),
         ns("nott-dilution-examples", "Topic 1, 2.c printed p16/PDF index15, 5 g/L tenfold example; 2.d printed p18/PDF index17 answer 4", "Provides a tenfold mass-concentration dilution and a 25 to 2.5 mg/mL worked clinical stock example.")],
        [ref("published-mass-stock-example", {"C1":25,"V1":1e-5,"V2":0.0001}, 2.5, 1e-10,
             "Published result 2.5 mg/mL becomes 2.5 kg/m^3; 25 mg/mL stock, 10 mL aliquot and 100 mL final volume are normalized to coherent units. Treat stated teaching values as exact; tolerance is arithmetic only, not preparation uncertainty.", "Nottingham workbook Topic1 2.d, answer4, printed p18/PDF index17."),
         ref("independent-conserved-mass", {"C1":8,"V1":0.000025,"V2":0.0001}, 2, 1e-10,
             "Independent synthetic mass-balance check: 25 mL at 8 mg/mL contains 200 mg; sharing that unchanged mass among one hundred 1 mL portions gives 2 mg/mL=2 kg/m^3. No additive-volume assumption is used.", "Curator-created count of conserved solute mass and final aliquots."),
         ref("no-dilution-boundary", {"C1":8,"V1":0.000025,"V2":0.000025}, 8, 1e-10,
             "Identity at unchanged positive final volume: the same solute mass and volume retain concentration 8 kg/m^3.", "Curator limiting identity, not an empirical mixture measurement.")],
        [reject({"C1":25,"V1":1e-5,"V2":0}, "Final zero volume is undefined."),
         reject({"C1":25,"V1":1e-5,"V2":5e-6}, "Final volume below initial aliquot volume is outside the declared dilution profile; no concentration process is silently substituted.")],
        "Target C1: known C2>=0,V1>0,V2>=V1 give C1=C2*V2/V1 uniquely; C2=0 gives C1=0. Target V1: C1>0,C2>0,V2>0 give V1=C2*V2/C1 and require V1<=V2. Target V2: C1>0,V1>0,C2>0 give V2=C1*V1/C2 and require V2>=V1. Check C2=2.5,V1=1e-5,V2=0.0001 gives C1=25 kg/m^3 and forward C2=2.5. With C1=C2=0, any positive volumes satisfying V2>=V1 fit; neither volume is identified. One zero concentration and the other positive has no solution with finite positive volumes. Retain original conservation/context assumptions in every direction; do not infer clinical preparation authorization.",
        ["Reuses proposed mass_concentration and solution_volume meanings from this batch, with distinct initial/final state context; need kg/m^3 and m^3 units. No runtime projection.",
         "Source-content licensing limits and independent final-volume measurement remain explicit integration/review gaps."]
    ))

    ctx = ("Same identified active drug/moiety, homogeneous infusion solution, delivery boundary and interval. "
           "Concentration is constant; q and r are interval means, also instantaneous values only for a constant-rate application. "
           "Rates/formulation are supplied for qualified arithmetic; source is medical education without a drug-specific patient validation population.")
    models.append(record(
        "infusion-constituent-mass-rate", "Infused drug mass rate from concentration and fluid flow",
        "Concentration times volumetric flow gives the selected constituent's mass delivery rate at the same boundary. This single transport relationship is distinct from a composed weight-to-pump dosing scenario.",
        "theoretical", "r", "C * q", "Infusion mass rate = concentration x infusion flow rate", "nott-infusion", "Topic 1, 3a Infusions, printed page20 (PDF index19), main displayed relation and 10 mg/mL, 1 mL/min example",
        "Introduced q maps to the source infusion flow rate (also V in its example); introduced r maps to source infusion mass rate, while C remains concentration. "
        "Use C in kg/m^3, q in m^3/s and r in kg/s. Dimensions: (M L^-3)*(L^3 T^-1)=M T^-1. The kg mass scale appears equally in C and r, so expression C*q is canonical without a mg/min or hour conversion literal. "
        "For fixed C, the relation also connects interval means exactly because constituent mass in every fluid portion is proportional to volume. That temporal interpretation is an explicit source-backed constant-concentration extension, not a claim about varying C. "
        "No weight-based amount, drug-selection rule or concentration-to-dose chain is built into this atomic transport relationship.",
        [v("C", "C", "input", "mass_concentration", "Mass concentration of the selected active constituent in the infused homogeneous solution.", "kg/m^3", "M L^-3", ctx, "Finite nonnegative and constant over the interval at the delivery boundary; zero is a blank-carrier limit, not a drug recommendation."),
         v("q", "Introduced q maps to infusion flow rate; source example also calls it V", "input", "mean_volumetric_infusion_rate", "Nonnegative fluid volume delivered per elapsed time at the same boundary and interval.", "m^3/s", "L^3 T^-1", ctx, "Finite nonnegative; zero denotes no flow. Constant rate is needed only to identify the mean with a fixed instantaneous setting."),
         v("r", "Introduced r maps to Infusion mass rate", "output", "mean_constituent_mass_infusion_rate", "Mass of the selected active constituent delivered per elapsed time at the specified boundary.", "kg/s", "M T^-1", ctx, "Finite nonnegative; delivered at boundary, not absorbed amount, systemic concentration or effect.")],
        ["C >= 0", "q >= 0"],
        ["Source relationship: medical workbook distinguishes fluid volume flow from constituent mass flow and multiplies concentration by volumetric rate.",
         "Application profile: selected-constituent concentration is homogeneous and constant; rates use the same time aggregation and boundary. No patient-specific clinical validation is asserted by this transport identity."],
        ["If concentration varies in time, a product of separate interval means is generally insufficient; a matched integral or aligned subinterval model is required.",
         "Does not include drug absorption, distribution, clearance, pump accuracy, line dead volume or therapeutic suitability. No dose or flow setting is recommended."],
        [ns("nott-infusion", "Topic1 3a Infusions, printed p20/PDF index19; next-page inverse example", "Separates volumetric and drug-mass rates, gives their concentration relation, and reports 10 mg/min for 10 mg/mL at 1 mL/min.")],
        [ref("published-ten-mg-per-minute", {"C":10,"q":1.6666666666666667e-8}, 1.6666666666666668e-7, 1e-18,
             "Published 10 mg/min converted to kg/s; 10 mg/mL becomes 10 kg/m^3 and 1 mL/min becomes 1.6666666666666667e-8 m^3/s. Preserve the source's exact teaching result; tolerance is representation only.", "Nottingham 3a first worked example, printed p20/PDF index19."),
         ref("independent-portion-count-per-hour", {"C":4,"q":3.3333333333333334e-8}, 1.3333333333333334e-7, 1e-18,
             "Independent synthetic interval count: 120 one-mL portions in one hour, each containing 4 mg, deliver 480 mg/h, equal to 8 mg/min and the declared kg/s value. This is independently counted mass transport, not pharmacological validation.", "Curator-created equal-portion and equal-time argument; values also match the workbook's next setup, but no unprinted answer is claimed as a published oracle."),
         ref("no-flow-boundary", {"C":10,"q":0}, 0, 1e-20,
             "No solution volume crosses the boundary in the interval, so no selected constituent mass crosses it at finite concentration.", "Conservation/no-flow identity.")],
        [reject({"C":-1,"q":1e-8}, "Mass concentration of the identified constituent cannot be negative."),
         reject({"C":10}, "Volumetric flow rate is missing.", "missing-input")],
        "Target q: known r>=0,C>0 give q=r/C uniquely; target C: known r>=0,q>0 give C=r/q uniquely. Retain source concentration, boundary and temporal assumptions. Check r=1.6666666666666668e-7 kg/s,C=10 kg/m^3 gives q=1.6666666666666667e-8 m^3/s and forward r matches. r=0,C>0 gives q=0; r=0,q>0 gives C=0, both admitted arithmetic boundaries. When C=r=0, any q>=0 fits; when q=r=0, any C>=0 fits. A positive r with a zero known multiplier has no solution. Algebraic inversion does not authorize choosing a clinical flow or formulation.",
        ["Need mean_constituent_mass_infusion_rate meaning and kg/s unit; reuse mass_concentration and b01 mean_volumetric_infusion_rate with matching constant-concentration interval context. kg/s must have the same kg mass scale as kg/m^3.",
         "No runtime projection. No composed dosing/infusion scenario or unverified connection is proposed."]
    ))

    ctx = ("Same person following a childbirth event, body mass at a specified postpartum assessment and an explicitly identified pre-pregnancy or early-pregnancy baseline. "
           "Both are actual measured body masses on comparable measurement bases. Source glossary is in a maternal nutrition report; the difference is definitional, not a calibrated clinical risk or treatment model.")
    models.append(record(
        "postpartum-weight-retention", "Signed postpartum body-mass retention relative to a baseline",
        "Postpartum mass minus early- or pre-pregnancy baseline mass. Positive values mean retained mass relative to that baseline; negative values remain signed differences rather than being clamped to zero.",
        "definition", "delta", "wp - w0", "Postpartum weight retention is the difference between body weight at a given postpartum time and early- or pre-pregnancy body weight", "sacn-retention", "Chapter 13 Glossary, Postpartum weight retention, printed p165 (PDF index164)",
        "Introduced wp,w0,delta map to source postpartum body weight, early/pre-pregnancy weight and their difference. Use actual mass in kg rather than force; dimensions M-M=M. "
        "The expression remains unchanged in the snapshot mass base because all three mass quantities share the kg unit scale. No percentage or elapsed-time rate is computed. "
        "A specified baseline is essential: early-pregnancy and pre-pregnancy measurements cannot silently be pooled. The source prose says difference; retain its signed mathematical meaning rather than creating a nonnegative-only profile. "
        "The report focuses on pregnancy and up to 24 months after delivery; the glossary definition supplies no fitted time coefficient or universal clinical cutoff.",
        [v("wp", "Introduced wp maps to body weight at a given time postpartum", "input", "body_mass", "Actual body mass at the identified postpartum assessment following the specified childbirth event.", "kg", "M", ctx, "Finite strictly positive measured body mass; assessment timing recorded externally."),
         v("w0", "Introduced w0 maps to early or pre-pregnancy body weight", "input", "body_mass", "Actual measured body mass at the declared pre-pregnancy or early-pregnancy baseline for the same pregnancy.", "kg", "M", ctx, "Finite strictly positive; baseline type/date and comparability must be documented, not imputed as a default."),
         v("delta", "Introduced delta maps to Postpartum weight retention", "output", "postpartum_body_mass_retention", "Signed postpartum mass difference relative to the specified baseline.", "kg", "M", ctx, "Finite real, including zero and negative values. Sign describes arithmetic relative mass only.")],
        ["wp > 0", "w0 > 0"],
        ["Source definition: the SACN glossary compares body weight at a specified postpartum time with early- or pre-pregnancy weight.",
         "Application profile: same person/pregnancy, explicit baseline type and comparable measurement conditions. The source report concerns girls/women of childbearing age and maternal outcomes; no age-specific prediction validity or new physiological relationship is claimed.",
         "This is a signed mass-accounting definition without diagnosis, treatment selection or monitoring instructions."],
        ["Does not separate fat, lean mass, fluid changes or effects of measurement timing; it is not a body-fat or energy-balance estimate.",
         "No missing baseline imputation, recommended weight trajectory, pregnancy treatment or clinical risk threshold is supplied. Different baseline types are not interchangeable."],
        [source("sacn-retention", "Scientific Advisory Committee on Nutrition: Nutrition and maternal weight outcomes, full report", SACN_PDF, "Published February 3, 2026; 178-page full report, publication landing page https://www.gov.uk/government/publications/nutrition-and-maternal-weight-outcomes-sacn-report", "Chapter13 Glossary, Postpartum weight retention, printed p165/PDF index164", "Defines retention as a postpartum weight difference from an early- or pre-pregnancy baseline.", "Publication landing page inspected 2026-11-03 states Open Government Licence v3.0 except where otherwise stated and links https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/. Detailed OGL-page retrieval returned 403, so no claim of inspecting its full text or clearing third-party material.", "Source: SACN/Office for Health Improvement and Disparities (2026), maternal-weight report glossary; original brief paraphrase and signed equation formalization with synthetic checks. Retain attribution/OGL link; no endorsement. No full report pages or figures included.")],
        [ref("independent-positive-retention", {"wp":69.5,"w0":64}, 5.5, 1e-10,
             "Independent synthetic difference check: adding five whole kg and one half kg to 64 kg reaches 69.5 kg, hence signed retention is +5.5 kg. Tolerance is floating arithmetic only.", "Curator-created mass-difference example, not observed maternal data."),
         ref("below-baseline-signed-case", {"wp":57,"w0":60}, -3, 1e-10,
             "Independent signed subtraction: current mass is three kg below the declared baseline, so the difference is -3 kg. This rejects silent clamping while retaining two positive body masses.", "Curator-constructed materially different signed case."),
         ref("equal-mass-boundary", {"wp":64,"w0":64}, 0, 1e-10,
             "Identical positive body masses have zero difference; this is an admissible equality boundary, not a zero-mass body.", "Definitional identity.")],
        [reject({"wp":69.5,"w0":0}, "A zero-body-mass baseline is not admissible."),
         reject({"wp":69.5}, "Baseline mass is missing; it cannot be inferred from postpartum mass.", "missing-input")],
        "Target wp: known delta and w0>0 give wp=delta+w0, with wp>0 requiring delta>-w0. Target w0: known wp>0 and delta give w0=wp-delta, with w0>0 requiring delta<wp. No denominators or multiple roots occur. Check delta=5.5,w0=64 gives wp=69.5 kg and forward delta=5.5; delta=-3,w0=60 gives wp=57 and forward -3. At delta=0, each known positive mass uniquely determines the equal other mass, so there is no zero-difference ambiguity when one mass is known. Without either mass, delta alone leaves infinitely many pairs. Retain same-pregnancy baseline context; inversion is accounting rather than causation.",
        ["Need postpartum_body_mass_retention meaning; body_mass and kg already exist. Source-specific time and baseline contexts must remain explicit. No runtime projection."]
    ))
    batch["models"] = models
    batch["deferred"] = [
        dict(title="Reconstitution powder-displacement arithmetic", reason="Directly inspected Langham Chapter13 separates 75 mL added liquid from 100 mL final volume in one example, but its printed dose equation is reversed; another exercise similarly swaps mass/volume units. The label transcriptions are useful facts, but no universal additive-volume or powder-displacement law is established. Keep this as a future product-specific definition/label-evidence task; do not set final volume equal to diluent volume or manufacture a general displacement parameter.", source_urls=["https://opentextbc.ca/nursingnumeracy/chapter/reconstituting-medications/"]),
        dict(title="Weight-based coefficient plus stock concentration to pump flow", reason="This combines independent weight-based amount/rate scaling with concentration-to-volume transport. Do not mint an end-to-end scenario formula merely to connect records. Distinct source identities are retained separately; no source-model inverse is a new model.", source_urls=[NOTTINGHAM]),
        dict(title="IUPAC independent mass-concentration terminology evidence", reason="Gold Book M03713 discovery describes constituent mass per mixture volume, but direct HTML/PDF retrieval returned 403. Not used as direct supporting evidence. Nottingham's directly inspected C=D/V and explicit drug mass/volume units ground the candidate; original terminology cross-check remains a review priority.", source_urls=["https://goldbook.iupac.org/terms/view/M03713","https://goldbook.iupac.org/terms/view/M03713/PDF"]),
        dict(title="Open Government Licence full-text access", reason="SACN publication landing page directly identifies OGL v3.0 except where stated, but the linked National Archives licence page returned 403. Exact source license label and URL are recorded; full legal terms were not claimed as read, and no general rights clearance is inferred.", source_urls=["https://www.gov.uk/government/publications/nutrition-and-maternal-weight-outcomes-sacn-report","https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"])
    ]
    batch["handoff"] = dict(
        summary="Fourth checkpoint: constituent mass concentration, solute-conserving dilution, constituent mass infusion rate and signed postpartum mass retention. New concentration meaning is independently useful; no composed dose-to-pump scenario is offered. No clinical decisions are encoded.",
        gaps=["New solution/constituent meanings and coherent kg/m^3, kg/s and m^3 units require extension. Preserve kg's mass scale on all mass-derived units.",
              "Duplicate checks limited to supplied inventory and own b01–b04. Bulk density and constituent mass concentration have different numerator supports; a future scientific reviewer should confirm any broader catalog harmonization.",
              "Nottingham workbook is directly hosted by its medical school and explicitly credits permission for reproduced maths; that is not a redistribution license. OpenStax live licensing restrictions are recorded. No broad downstream clearance is claimed.",
              "Root/inverse assignment deferrals from prior batches remain active; final-volume assumptions and temporal concentration constancy must be retained."],
        connections=[], queries=[],
        review_notes="Direct source prose/equations and numerical examples inspected in the 2022–23 Nottingham workbook; printed-page versus PDF-index locators recorded. OpenStax general conservation/dilution passage inspected, with exact accessed-version restrictions. SACN glossary inspected directly for signed postpartum definition. Original arithmetic, dimensional algebra, domain guards and inverse zero cases reviewed; empirical patient validation is not asserted by these definitions. Prior ZIPs remain intact and weight-based mass r2 remains preferred. JSON/ZIP validation will be recorded after execution in the checkpoint log; handoff must be updated with actual results before packing. Source-content rights and scientific review remain pending.")
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
