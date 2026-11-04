"""Final bounded pair: supplied-area prescription arithmetic and arm-geometry index."""
import json
from build_b01 import ROOT, DAY, variable as v, source, reference as ref, rejection as reject, record
from build_b02 import UNKNOWN_RIGHTS, SHORT_REDIST

def main():
    path = ROOT/"returns/clinical-arithmetic-codex-b06/bundle.json"
    batch = json.loads(path.read_text(encoding="utf-8"))
    batch["created"] = DAY
    models = []
    ctx = ("Same patient, independently supplied body surface area and already authorized active-drug mass per body surface area for one administration. "
           "No BSA is calculated from height or mass. Source discusses pediatric and other clinical uses, but this amount identity does not establish drug-specific clinical validation for any population.")
    models.append(record(
        "surface-area-based-prescribed-mass", "Prescribed drug mass from a supplied body-surface-area basis",
        "Multiplies a supplied body surface area by an independently authorized mass-per-area amount for one administration. This does not compute a root-based body-area estimate or select a regimen.",
        "definition", "D", "d * A", "Client size (body surface area) x Order (mass per area) = Dose (mass)", "openstax-area-dose", "Pharmacology for Nurses, 2.4 Dosage Calculations, Body Surface Area Method, example step3 and final displayed Client size x Order = Dose",
        "Introduced A,d,D map to supplied client BSA, ordered mass per area, and resulting mass. Use A in m^2, d in kg/m^2 and D in kg; dimensions (M L^-2)*L^2=M. "
        "Input d and output D share kg's runtime scale, so d*A is canonical without a mg conversion factor. The earlier square-root BSA step is excluded entirely; A is an external quantity with its own provenance. "
        "Use only the source's step3 mass result1.34 mg from2 mg/m^2 and already reported0.67 m^2. Its later dimensional-analysis line incorrectly labels the mass product as mL; that line is not the authority. "
        "This area-normalized prescription has a different normalization quantity/dimensions from mass-per-body-mass prescription; a kg-to-m^2 unit conversion cannot turn one into the other.",
        [v("d", "Introduced d maps to Order, in mg/m^2", "input", "prescribed_drug_mass_per_body_surface_area", "Already authorized active-drug mass per patient body surface area for one administration, normalized to kg/m^2.", "kg/m^2", "M L^-2", ctx, "Finite nonnegative; drug, moiety, route, age and clinical eligibility must be established externally. Zero is only a no-amount arithmetic boundary."),
         v("A", "Introduced A maps to Client size/BSA", "input", "body_surface_area", "Independently supplied BSA of the same patient, with measurement/estimation method and assessment state documented.", "m^2", "L^2", ctx, "Finite strictly positive. No root formula, default area, cap or height/mass inference is supplied."),
         v("D", "Introduced D maps to Dose in mass units", "output", "prescribed_drug_mass_per_administration", "Active-drug mass corresponding to the authorized per-area amount and supplied patient area for one administration.", "kg", "M", ctx, "Finite nonnegative arithmetic amount, without therapeutic appropriateness or rounding policy.")],
        ["d >= 0", "A > 0"],
        ["Source arithmetic: multiply patient area by the ordered mass-per-area amount; example step3 explicitly gives a mass result.",
         "Application profile: A is supplied independently and the per-administration coefficient is already clinically qualified for the patient. This definition is not drug-specific population validation.",
         "Assignment scope: root-based BSA estimation remains deferred. The model does not reconstruct A or infer a dose coefficient."],
        ["Does not establish drug selection, per-day frequency, dose limits, rounded tablet quantities, renal adjustment or BSA method validity.",
         "A percentage of an adult reference dose, a per-weight amount and a mass-per-area prescription are distinct conventions and cannot be substituted by a unit label.",
         "The source's numerical regimen is pedagogical only; it is not promoted to a reusable recommendation or default."],
        [source("openstax-area-dose", "OpenStax: Pharmacology for Nurses, 2.4 Dosage Calculations", "https://openstax.org/books/pharmacology/pages/2-4-dosage-calculations", "Tina Barbour-Taylor et al.; publication May29,2024; live accessed-version licensing inspected2026-11-03", "Body Surface Area Method, example step3; final displayed size-times-order relationship; Citation/Attribution", "Provides a per-area mass multiplication and a1.34 mg worked intermediate from supplied0.67 m^2 and2 mg/m^2.", "Same-page licensing states CC BY-NC-SA4.0, attribution/share-alike and AI-use/commercial restrictions. Accessed2026-11-03; no inference that downstream AI/commercial source-content use is cleared.", "Only an original short mathematical formalization, evidence paraphrase and attributed numeric fact are returned. No textbook images, full passages or clinical regimen recommendation; source-content restrictions remain explicit.")],
        [ref("published-area-mass-intermediate", {"d":2e-6,"A":0.67}, 1.34e-6, 5e-9,
             "Published step3 mass result1.34 mg is preserved as1.34e-6 kg; input2 mg/m^2 becomes2e-6 kg/m^2 and already reported BSA0.67 m^2 is used directly. Half the printed0.01 mg increment explains5e-9 kg tolerance. No height/mass root is evaluated and no accuracy claim is made for the rounded BSA or regimen.", "OpenStax Pharmacology for Nurses2.4, Body Surface Area Method, worked example step3 only."),
         ref("independent-equal-area-portions", {"d":0.00035,"A":1.6}, 0.00056, 1e-12,
             "Independent synthetic partition: eight area portions of0.2 m^2 at350 mg/m^2 correspond to70 mg each, totaling560 mg. This is prescription arithmetic only; neither value is recommended. Tolerance is representation only.", "Curator-created equal-area count."),
         ref("zero-coefficient-boundary", {"d":0,"A":1.6}, 0, 1e-20,
             "A supplied zero amount per area corresponds to zero total amount at a positive area; this is a no-amount identity, not a treatment instruction.", "Definitional boundary.")],
        [reject({"d":2e-6,"A":0}, "Zero patient surface does not describe an eligible body-area input."),
         reject({"d":2e-6}, "BSA is missing and must not be inferred by an excluded root form.", "missing-input")],
        "Target d: D>=0,A>0 give d=D/A uniquely. Target A: D>0,d>0 give A=D/d>0. Retain original clinical/area provenance conditions. Check D=0.00056 kg,A=1.6 m^2 gives d=0.00035 kg/m^2 and forward D matches. D=0,A>0 uniquely gives d=0. If d=D=0 and A is unknown, every A>0 fits; d=0,D>0 has no solution; D=0,d>0 would require A=0 and is excluded. These are proportional-amount inversions, not BSA-from-height roots or clearance inversions.",
        ["Need prescribed_drug_mass_per_body_surface_area meaning; reuse body_surface_area from b03 and prescribed_drug_mass_per_administration from b01/r2. Need m^2/kg/m^2 with consistent kg scale.",
         "Despite kg/m^2 unit equality, a per-area prescription coefficient is not BMI. No runtime projection or forced link to deferred BSA formulas."]
    ))

    ctx = ("Same human mid-upper arm, assessment side/site and measurement state; paired MUAC and triceps skinfold thickness. "
           "Conditional circular-section/uniform-fat-rim geometry; a positive nondegenerate inner muscle-and-bone core is required. "
           "This geometric anthropometric proxy has no universal age/sex/ethnic clinical validation or percentile mapping in this record.")
    models.append(record(
        "mid-upper-arm-muscle-circumference", "Calculated mid-upper-arm muscle circumference under circular geometry",
        "Subtracts pi times triceps skinfold thickness from total upper-arm circumference to estimate the inner muscle-core circumference under a circular, uniform-rim model. No total muscle mass, sarcopenia diagnosis or risk threshold is inferred.",
        "theoretical", "M", "C - 3.141592653589793 * T", "MUAMC = MUAC - (pi x TSK)", "gibson-arm", "Principles of Nutritional Assessment: Body Composition,11.2.2, Calculation of mid-upper-arm-muscle circumference; shared geometric assumptions in11.1.4",
        "Introduced C,T,M map to MUAC,TSK,MUAMC. Both measurements and output use metres, so cm/mm scales cancel without an inline conversion factor. Dimensions L-(1*L)=L. "
        "Source pi is serialized as3.141592653589793, a local floating-point approximation to the mathematical constant, not a fitted clinical parameter. "
        "The source derives the inner-circle circumference by subtracting the diameter decrement represented by a doubled fat-layer skinfold. Under this geometry C>pi*T ensures positive inner diameter, hence the feasibility guard; it is not a clinical cutoff. "
        "The source's model ignores variable skinfold compressibility and fat nonuniformity. Its central bone core is enclosed, not removed. BAPEN's3.14 coefficient is a rounded alternative source view of the same relationship, not another model.",
        [v("C", "Introduced C maps to MUAC", "input", "mid_upper_arm_circumference", "Total measured circumference at the declared mid-upper-arm site.", "m", "L", ctx, "Finite strictly positive and greater than pi*T for the model's nondegenerate inner core."),
         v("T", "Introduced T maps to TSK, triceps skinfold", "input", "triceps_skinfold_thickness", "Measured doubled skin/fat fold thickness at the matching upper-arm site, treated as the diameter decrement under the source geometric approximation.", "m", "L", ctx, "Finite strictly positive measured fold; compressibility/method metadata external. No universal sample value or clinical normal range is supplied."),
         v("M", "Introduced M maps to MUAMC", "output", "calculated_mid_upper_arm_muscle_circumference", "Calculated inner muscle-core boundary circumference, enclosing central bone, under the circular/uniform-rim geometric model.", "m", "L", ctx, "Finite strictly positive proxy within geometric feasibility; not a direct muscle-mass measurement.")],
        ["C > 0", "T > 0", "C - 3.141592653589793 * T > 0"],
        ["Source geometric assumptions: circular/cylindrical limb approximation, uniform surrounding fat rim, doubled-fold representation, and ignored variation in skinfold compressibility.",
         "Application profile: same arm/site/state measurements and a nondegenerate positive inner core. The definition is conditional geometry, not a population-fitted muscle-mass prediction.",
         "Source notes historical/community and elderly proxy uses; those uses do not establish universal clinical classification validity for this record."],
        ["Nonuniform fat, noncircular shape, skinfold compressibility and individual humerus proportion can bias the proxy; these are not corrected here.",
         "One-dimensional circumference is not muscle area or volume and can be insensitive to small muscle-mass changes. No percentage, percentile, diagnosis or intervention is returned.",
         "Zero fold thickness is not admitted as a measured human fold in this profile; an ideal zero-rim limit is mathematically M=C but is not claimed as a valid clinical observation."],
        [source("gibson-arm", "Rosalind S Gibson: Nutritional Assessment of Body Composition", "https://nutritionalassessment.org/bodycomposition/", "Principles of Nutritional Assessment,3rd edition,July2024; author-hosted HTML", "11.2.2 Calculation of mid-upper-arm-muscle circumference;11.1.4 geometric assumptions; source limitations following equation", "Derives the circumference difference from paired arm/skinfold measures and describes the circular geometry and compressibility limitations.", "Chapter header identifies CC BY4.0 and links https://creativecommons.org/licenses/by/4.0/; chapter and deed inspected2026-11-03.", "Attribution: Gibson RS, Principles of Nutritional Assessment: Body Composition,3rd ed.,July2024,CC BY4.0. Changes: symbols, coherent units, explicit feasibility guard and added numerical checks. No images or full paragraphs redistributed; retain attribution/license/change notice; no endorsement."),
         source("bapen-arm", "BAPEN: Nutritional Assessment", "https://www.bapen.org.uk/education/nutrition-support/assessment-planning/nutritional-assessment/", "Live HTML inspected2026-11-03; page revision date not established", "Anthropometry table, Mid arm muscle circumference (MAMC) row", "Shows the same index with3.14 as the rounded pi coefficient and same-unit centimetre inputs.", UNKNOWN_RIGHTS, SHORT_REDIST)],
        [ref("alternate-rounded-pi-source-check", {"C":0.3,"T":0.012}, 0.26232, 0.00006,
             "Value independently derived from BAPEN's published rounded coefficient:30 cm-3.14*1.2 cm=26.232 cm=0.26232 m. It is not labeled a published patient result. A coefficient rounded to0.01 has half-increment0.005; multiplied by0.012 m this gives absolute6e-5 m comparison tolerance. Difference from the fuller-pi model is coefficient approximation, not clinical uncertainty.", "Independent arithmetic from BAPEN alternate rounded-pi form; original source facts are distinct from the model's fuller-pi serialization."),
         ref("independent-concentric-circle", {"C":0.3141592653589793,"T":0.02}, 0.25132741228718347, 1e-14,
             "Independent ideal geometry: outer diameter0.10 m has circumference pi*0.10; a0.02 m doubled-rim decrement leaves diameter0.08 m and circumference pi*0.08=0.25132741228718347 m. This checks the source geometric derivation, not empirical accuracy in a real arm. Tolerance covers decimal representation only.", "Curator-constructed concentric-circle model with nonzero fold.")],
        [reject({"C":0.1,"T":0.04}, "Under the declared circular uniform-rim geometry, the fold decrement would exceed the outer diameter and leave no positive inner core."),
         reject({"C":0.3}, "Matching triceps skinfold thickness is missing.", "missing-input")],
        "Target C: known M>0,T>0 give C=M+pi*T>0 and automatically satisfy inner-core feasibility. Target T: known C>0,M>0 with C>M give T=(C-M)/pi>0; pi is fixed positive, not a freely solvable input. Retain source geometry and measurement context. Check M=0.25132741228718347 m,T=0.02 m gives C=0.3141592653589793 m and forward M matches; solving T from that C,M gives0.02 m. If M=C, T=0 would follow but is outside this measured-fold profile; M>C would require negative fold. M=0 would be a degenerate inner core and violates the declared feasibility guard. No muscle-mass or biological causal inversion is asserted.",
        ["Need mid_upper_arm_circumference,triceps_skinfold_thickness and calculated_mid_upper_arm_muscle_circumference meanings; m already exists. New contexts must preserve arm/site/method and geometric eligibility. No runtime projection.",
         "No arm-muscle-area or total-body-muscle-mass conversion is asserted; those require distinct relationships and validation scope."],
        constants=[dict(literal=3.141592653589793,meaning="Local floating-point approximation to source mathematical pi; not a fitted clinical coefficient",unit="1",source_id="gibson-arm",locator="11.2.2, source MUAMC=MUAC-(pi*TSK)")]
    ))
    batch["models"] = models
    batch["deferred"] = [
        dict(title="Root-based BSA estimate in the same dosing source", reason="OpenStax2.4 also supplies a height/mass square-root BSA form, but the assignment requires it deferred. Completed per-area prescription arithmetic accepts BSA as an independently supplied input and extracts only the subsequent mass multiplication. It does not evaluate, approximate or recurate the root form.", source_urls=["https://openstax.org/books/pharmacology/pages/2-4-dosage-calculations"]),
        dict(title="Arm fat/muscle areas and corrected muscle-mass predictions", reason="Author body-composition chapter provides additional area formulae and validation-specific corrections. Retain as next-session priorities rather than rush incomplete population/parameter review at the session boundary. Each proposed area or corrected empirical predictor requires its own scope, source locators, independent oracles and duplicate check; no generic conversion from circumference to true muscle mass is implied.", source_urls=["https://nutritionalassessment.org/bodycomposition/"]),
        dict(title="OpenStax per-area example's mL label", reason="Direct HTML inspected: Body Surface Area Method example step3 yields1.34 mg from0.67 m^2 times2 mg/m^2, while a later dimensional-analysis line labels that same product1.34 mL. The latter has incompatible units and is not used. The completed record uses the dimensionally coherent mass step and discloses that the illustrative regimen is not a reusable default.", source_urls=["https://openstax.org/books/pharmacology/pages/2-4-dosage-calculations"])
    ]
    batch["handoff"] = dict(
        summary="Sixth bounded checkpoint: two additional independent relationships, supplied-area prescribed mass and conditional circular-arm muscle circumference. Root-based BSA calculation stays deferred; clinical decisions and muscle-mass predictions are excluded.",
        gaps=["New clinical meanings require extension; units must preserve kg scale for per-area mass. Source-content licensing and clinical applicability remain subject to review.",
              "Per-area and per-body-mass prescriptions have physically different normalization quantities, not a unit conversion. The arm proxy is conditional geometry, not empirically validated true muscle mass.",
              "Original/source errors and incomplete adjacent area-model review are retained as deferred work. Prior CG r2 remains blocked; dose-mass r2 remains preferred.",
              "Duplicate search limited to supplied catalog/vocabulary and own six batches; no global uniqueness or scientific approval claim."],
        connections=[],queries=[],
        review_notes="Primary author-hosted body-composition derivation and assumptions inspected directly; BAPEN rounded-pi alternative checked. OpenStax2.4 direct HTML inspected for coherent step3 mass result and final per-area relation, with later unit typo excluded. All ordinary/domain/missing-input and direction-specific inverse notes reviewed. This smaller two-model batch checkpoints bounded useful work near the session endpoint rather than expanding unreviewed area/calibration records for a quota. JSON/ZIP validation will be recorded after execution in the checkpoint log; handoff must be updated with actual results before packing. No clinical/scientific approval.")
    path.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
