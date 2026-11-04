"""Body-index and renal normalization definitions from directly inspected primary technical sources."""
import json
from build_b01 import ROOT, DAY, variable as v, source, reference as ref, rejection as reject, record
from build_b02 import UNKNOWN_RIGHTS, SHORT_REDIST

NIDDK_URL = "https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/ckd-drug-dosing-providers"
SACN_PDF = "https://assets.publishing.service.gov.uk/media/698087f0f0e5cf1ed2612dd3/nutrition-and-maternal-weight-outcomes_full-report.pdf"

def main():
    path = ROOT / "returns/clinical-arithmetic-codex-b03/bundle.json"
    batch = json.loads(path.read_text(encoding="utf-8"))
    batch["created"] = DAY
    models = []
    ctx = ("Same adult with CKD, same renal-estimate equation, time/assay state and supplied body surface area. "
           "Input g is GFR per square metre of body surface, converted from a laboratory result indexed to 1.73 m^2. "
           "This is normalization arithmetic, without choosing an estimating equation, deriving BSA or selecting a drug dose.")
    models.append(record(
        "gfr-body-surface-deindexing", "Absolute GFR from GFR per body surface area",
        "Removes reference-body-surface indexing from an already supplied adult GFR estimate. The input is a genuine per-area density in coherent units; the conventional 1.73 m^2 display scale must be handled once, not multiplied into the expression again.",
        "definition", "G", "g * A", "eGFR (mL/min) = reported eGFR (mL/min/1.73 m^2) x BSA / 1.73", "niddk-gfr", "Considerations for Body Surface Area, last paragraph and displayed expression",
        "Introduced A maps to BSA, G to absolute eGFR, and g to the reported reference-indexed result divided by its reference area. "
        "For a reported number E in mL/min per 1.73 m^2, g=E*(1e-6/60)/1.73 m/s. This is the port's unit normalization, not an extra scientific correction or a second expression conversion. "
        "Thus the canonical equation is G=g*A; do not store E as m/s or inline another /1.73. Dimensions: (L^3 T^-1 L^-2)*L^2=L^3 T^-1. "
        "A0=1.73 m^2 is a fixed reference area documented in constants, not a freely solvable input. Input A must be supplied independently; root-based BSA estimates are deferred under the assignment.",
        [v("g", "Introduced g maps to reported eGFR divided by its fixed reference BSA", "input", "glomerular_filtration_rate_per_body_surface_area", "GFR estimate per actual area unit, not the unconverted numerical value printed for a standard 1.73 m^2 body surface.", "m/s", "L T^-1", ctx, "Finite nonnegative density; estimation-equation population, assay and uncertainty metadata remain attached. Unit match with speed does not permit binding a speed."),
         v("A", "Introduced A maps to BSA", "input", "body_surface_area", "Supplied body surface area for the same adult and assessment, in square metres, with method/provenance specified.", "m^2", "L^2", ctx, "Finite strictly positive. No default 1.73 m^2 patient area and no BSA formula or approximation is supplied."),
         v("G", "Introduced G maps to absolute eGFR in mL/min, normalized to m^3/s", "output", "glomerular_filtration_rate", "Absolute glomerular filtration rate estimate for the individual, without reference-area indexing; distinct from creatinine clearance.", "m^3/s", "L^3 T^-1", ctx, "Finite nonnegative estimate; normalization preserves the underlying estimate's limitations rather than validating it.")],
        ["g >= 0", "A > 0"],
        ["Source scope: NIDDK's adult CKD technical guidance states removal of the standard 1.73 m^2 correction by multiplying by supplied BSA and dividing by that reference area.",
         "Derived definition: g is a per-square-metre density, so its unit conversion already includes the reference area exactly once.",
         "Application profile: underlying GFR estimate and area concern the same adult and condition. No therapeutic decision, BSA computation or new population validation is performed."],
        ["Cannot use a raw laboratory number such as 60 directly as g; it must first be normalized from its stated mL/min per 1.73 m^2 unit convention.",
         "Does not turn creatinine clearance into GFR, remove estimation error, establish renal stability, or extend the equation to children or pregnancy.",
         "No clearance inverse views are offered under this assignment; the normalization itself is retained as an independently meaningful definition."],
        [source("niddk-gfr", "NIDDK: Determining Drug Dosing in Adults with Chronic Kidney Disease", NIDDK_URL, "Last reviewed October 2024; live HTML inspected 2026-11-03", "Considerations for Body Surface Area", "Explains how the standard reference-area result is converted to an individual's absolute GFR using that person's BSA.", "https://www.niddk.nih.gov/copyright, inspected 2026-11-03: most information is copyright free, with third-party exceptions; attribution and no endorsement are required, and logos must be removed from edited content.", "Source: NIDDK. Available free at the linked page. Changes: original paraphrase and coherent per-area port normalization; no images/logos or treatment guidance reproduced. NIDDK/NIH do not endorse this record; third-party rights are not cleared by this attribution.")],
        [ref("independent-reference-area-ratio", {"g":5.780346820809249e-7,"A":2}, 1.1560693641618498e-6, 1e-17,
             "Independent source-convention arithmetic: a reported 60 mL/min per 1.73 m^2 scales by the area ratio 2/1.73 to 69.36416184971098 mL/min. Convert that value to m^3/s; separately normalize input density 60/1.73 to mL/min/m^2. This is a constructed normalization check, not a published patient result. Tolerance is arithmetic only.", "Curator synthetic example based on the NIDDK reference-area convention."),
         ref("reference-body-identity", {"g":5.780346820809249e-7,"A":1.73}, 1e-6, 1e-17,
             "Limiting normalization identity: at exactly the reference area, reported 60 mL/min per 1.73 m^2 corresponds to absolute 60 mL/min = 1e-6 m^3/s. This checks that the 1.73 reference is applied only once.", "Curator identity check of the source definition, not empirical renal validation."),
         ref("zero-filtration-limit", {"g":0,"A":1.8}, 0, 1e-20,
             "Ideal zero-filtration algebraic boundary for a positive surface area. No diagnosis or inference about urine output is made.", "Definitional limit; not a claimed laboratory measurement.")],
        [reject({"g":5e-7,"A":0}, "Zero body surface does not describe a patient and cannot supply this area normalization."),
         reject({"g":5e-7}, "Patient BSA is missing; the reference 1.73 must not be substituted as a patient default.", "missing-input")],
        "No inverse solve view is supplied: the assignment explicitly defers clearance inversions, so no inverse-target example is asserted. Forward normalization at g=0 is defined for every positive A; it does not identify an individual's area. Negative GFR density and zero patient surface are outside the declared forward domain. The source supports reference-area removal, not statistical or causal inference about body size.",
        ["Need glomerular_filtration_rate_per_body_surface_area, body_surface_area and glomerular_filtration_rate meanings, plus m^2 and m^3/s units. Existing m/s unit can represent the density dimension but speed meaning cannot be reused.",
         "Future indexed GFR unit scale must include 1/1.73 m^-2; no additional /1.73 may be inlined. BSA is an external supported input, not a forced connection to a deferred root model."],
        constants=[dict(literal=1.73,meaning="Fixed conventional reference body surface area used only in the source/reporting-unit normalization, not additionally in the expression",unit="m^2",source_id="niddk-gfr",locator="Considerations for Body Surface Area, reference-area paragraph")]
    ))

    ctx = ("Same person and assessment, waist circumference at the midpoint between lower ribs and top of hips and standing height in matching length units. "
           "Source use spans children aged at least 5 and adults; application excludes pregnancy, eating disorders and height-affecting growth conditions, "
           "and uses adults only below BMI 35 per BHF guidance. These eligibility conditions require external context verification.")
    models.append(record(
        "waist-height-ratio", "Waist-to-height ratio",
        "Waist circumference divided by standing height, with declared measurement context. Returns the arithmetic ratio only; no adiposity category, disease-risk prediction or treatment advice is included.",
        "definition", "R", "W / h", "waist-to-height ratio = waist measurement / height measurement, in the same units", "bhf-ratio", "How to work out your waist to height ratio, final step and 96.5 cm/170 cm example",
        "Introduced W, h and R map to waist measurement, height and their ratio. Both lengths use metres; source cm/cm or inch/inch factors cancel and must not be inlined. Dimensions L/L=1. "
        "The published 0.57 result is retained with its rounding tolerance, not replaced by 0.567647... . This is an arithmetic body-size index, not an empirical fat-fraction estimate. "
        "h reuses the standing_body_height definition from b01. W uses generic waist_circumference with this source's landmark in context. Adult BMI eligibility is not a numeric input to this two-length equation.",
        [v("W", "Introduced W maps to waist measurement", "input", "waist_circumference", "Measured circumference of the waist at the explicitly declared anatomical landmark and assessment condition.", "m", "L", ctx, "Finite strictly positive. Here the context requires the source midpoint landmark; differently located abdominal measurements require compatibility review."),
         v("h", "Introduced h maps to height", "input", "standing_body_height", "Measured standing height of the same person at the same assessment.", "m", "L", ctx, "Finite strictly positive; source calculator excludes conditions affecting height."),
         v("R", "Introduced R maps to waist to height ratio", "output", "waist_to_height_ratio", "Dimensionless ratio of measured waist circumference to standing height.", "1", "1", ctx, "Finite strictly positive ratio; no artificial upper bound of 1 is imposed.")],
        ["W > 0", "h > 0"],
        ["Source definition: BHF directly divides same-unit waist measurement by height and publishes a worked ratio. NHS calculator describes use from age 5 and lists eligibility exclusions.",
         "Application profile: BHF states adult use below BMI 35; NHS excludes adult BMI over 35. This record takes the stricter below-35 profile, without pretending that exactly 35 makes division undefined.",
         "The output is only a quantitative index. Source guidance on risk categories is outside this assignment and not encoded."],
        ["Numeric guards check positive measured lengths; they do not verify age, BMI, pregnancy, eating-disorder or growth-condition exclusions.",
         "Different waist landmarks, recumbent length or times are not automatically compatible with these ports.",
         "No clinical diagnostic, age-specific risk or intervention validity is asserted from a ratio calculation alone."],
        [source("bhf-ratio", "British Heart Foundation: Why your waist size matters", "https://www.bhf.org.uk/informationsupport/heart-matters-magazine/medical/measuring-your-waist", "Live HTML inspected 2026-11-03; publication/update date not established", "What's the best way to measure your waist?; How to work out your waist to height ratio", "Defines same-unit waist/height division and reports 0.57 for 96.5 cm and 170 cm; adult application is below BMI 35.", "BHF Website terms, https://www.bhf.org.uk/what-we-do/our-policies/terms-and-conditions, section 12, inspected 2026-11-03: site material is protected; personal/noncommercial copying is limited and public republication requires authorization. This record does not infer permission for wider source-content reuse.", SHORT_REDIST),
         source("nhs-scope", "NHS: Calculate your waist to height ratio", "https://www.nhs.uk/health-assessment-tools/calculate-your-waist-to-height-ratio", "Live HTML inspected 2026-11-03; no page revision date established", "Using this calculator; Who should not use this calculator", "Lists age under 5, pregnancy, eating disorders, height-affecting conditions and adult BMI over 35 as calculator exclusions.", "Specific NHS reuse terms for this accessed calculator were not established; terms unknown. No blanket permission inferred.", SHORT_REDIST)],
        [ref("published-bhf-ratio", {"W":0.965,"h":1.70}, 0.57, 0.005,
             "Published result 0.57 preserved; convert lengths 96.5 and 170 cm to metres. Half the printed hundredth increment explains the absolute tolerance 0.005. No disease-risk validity is tested.", "BHF worked example in How to work out your waist to height ratio."),
         ref("independent-half-height", {"W":0.84,"h":1.68}, 0.5, 1e-12,
             "Independent synthetic length partition: two equal 84 cm segments span 168 cm, so the first segment is one half of the height. Tolerance is floating arithmetic only; no category or recommendation follows from the equality.", "Curator-constructed equal-segment identity, using positive plausible body measurements.")],
        [reject({"W":0.9,"h":0}, "Positive standing height is required and the denominator cannot be zero."),
         reject({"h":1.7}, "Waist circumference is missing.", "missing-input")],
        "Target W: R>0 and h>0 give W=R*h, unique. Target h: W>0 and R>0 give h=W/R>0, unique; requested unknown height need not appear in a denominator guard before solving. Retain the source measurement and population context. Check R=0.5,h=1.68 gives W=0.84 m and forward R=0.5. R=0 would imply W=0 for finite positive height, violating the positive-person-measurement domain; there is no admissible zero-waist ambiguity here. R=1 is mathematically permitted when waist equals height and is not clamped or reclassified.",
        ["Need waist_circumference, standing_body_height and waist_to_height_ratio meanings; m and 1 already exist. Reuse standing_body_height from b01; source landmark must remain in context.",
         "Population and measurement-context eligibility are external preconditions; no risk category meaning or runtime projection is supplied."]
    ))

    ctx = ("Same adult and assessment, waist and hip circumference measured under an explicitly named compatible anthropometry protocol. "
           "Anatomical landmarks, clothing/posture and measurement state must be recorded externally; the MeSH definition itself does not prescribe a landmark. "
           "Adult men and women are discussed by the source; no pregnancy, pediatric or clinical-risk validation is asserted by the pure definition.")
    models.append(record(
        "waist-hip-ratio", "Waist-to-hip circumference ratio",
        "The waist circumference measurement divided by the hip circumference measurement. This is a measurement-ratio definition, without importing the source vocabulary's risk-threshold statements.",
        "definition", "R", "W / H", "Waist-Hip Ratio: waist circumference measurement divided by hip circumference measurement", "nlm-whr", "MeSH Descriptor D049629, 2026 data, Scope Note (first sentence)",
        "Introduced W,H,R map to waist circumference, hip circumference and their ratio; the source uses prose rather than algebraic symbols. Both circumferences use metres, so L/L=1 and no cm/inch conversion coefficient belongs in the expression. "
        "Source definition is formalized directly. The waist_circumference meaning is reused from b03's waist-height record, but common symbol/meaning is not proof that two measured instances share landmarks or timing. "
        "The mathematical definition is not a fitted predictor, and no source category cutoffs are treated as domain guards.",
        [v("W", "Introduced W: waist circumference measurement in source prose", "input", "waist_circumference", "Measured waist circumference at the declared protocol landmark for this assessment.", "m", "L", ctx, "Finite strictly positive, with the method and anatomical landmark specified externally."),
         v("H", "Introduced H: hip circumference measurement in source prose", "input", "hip_circumference", "Measured hip circumference at the declared protocol landmark for the same assessment.", "m", "L", ctx, "Finite strictly positive. Circumference is not hip breadth or diameter."),
         v("R", "Introduced R: Waist-Hip Ratio", "output", "waist_to_hip_ratio", "Dimensionless waist circumference divided by hip circumference.", "1", "1", ctx, "Finite strictly positive; values equal to or greater than 1 are mathematically admitted without interpretation.")],
        ["W > 0", "H > 0"],
        ["Source definition: MeSH explicitly defines the ratio by the two circumference measurements and discusses men and women.",
         "Application profile: restrict this record's interpretation context to adults using a declared measurement protocol; no age- or sex-specific risk mapping is provided.",
         "Source prose is translated into a ratio only; source disease-risk thresholds are neither transcribed nor validated by the arithmetic."],
        ["The source definition does not establish a particular waist/hip measurement protocol or a clinical validation population for risk prediction.",
         "No pregnancy/pediatric risk interpretation or therapeutic decision is supported by this definition. Different anatomical landmarks can produce different ratios."],
        [source("nlm-whr", "U.S. National Library of Medicine: Waist-Hip Ratio, MeSH Descriptor D049629", "https://meshb.nlm.nih.gov/record/ui?ui=D049629", "MeSH Descriptor Data 2026; also directly inspected NCBI rendering https://www.ncbi.nlm.nih.gov/mesh?Cmd=DetailsSearch&Term=%22Waist-Hip+Ratio", "Scope Note, first sentence; Descriptor UI D049629", "Defines the ratio of waist circumference to hip circumference.", "NLM MeSH Terms and Conditions, https://www.nlm.nih.gov/databases/download/terms_and_conditions_mesh.html, inspected 2026-11-03: freely provided data, NLM attribution and no endorsement, with current version maintained or distributed version identified; translation files excluded from those terms.", "Source: NLM MeSH 2026, descriptor D049629. This is an original equation formalization of the definition with synthetic checks, not the complete descriptor. NLM does not endorse this application. Version is identified; no guarantee of current data after access date.")],
        [ref("independent-length-ratio", {"W":0.81,"H":0.96}, 0.84375, 1e-12,
             "Independent exact integer-ratio arithmetic: waist 81 cm and hips 96 cm reduce to 27/32; 27 thirty-seconds equal 0.84375. Synthetic same-assessment lengths; floating arithmetic tolerance only.", "Curator-created definitional check, not a published patient result or clinical validation."),
         ref("equal-circumference-boundary", {"W":0.9,"H":0.9}, 1, 1e-12,
             "Identity at two equal positive circumferences: numerator and denominator represent the same length amount, giving ratio 1. This is physically admissible and does not require zero-size extrapolation.", "Curator boundary identity, not a source disease-risk threshold.")],
        [reject({"W":0.81,"H":0}, "Zero hip circumference does not describe a valid positive body measurement and divides by zero."),
         reject({"W":0.81}, "Hip circumference is missing.", "missing-input")],
        "Target W: known R>0,H>0 give W=R*H. Target H: W>0,R>0 give H=W/R>0. Retain original protocol/context conditions. Check R=0.84375,H=0.96 m gives W=0.81 m and forward R=0.84375; reversing W/R gives H=0.96. R=0 cannot be satisfied by positive finite W,H; it is not an admitted zero-body boundary. Equal positive circumferences give R=1 uniquely. No clinical or causal inverse interpretation is asserted.",
        ["Need hip_circumference and waist_to_hip_ratio meanings; reuse waist_circumference and existing m/1 units. No runtime projection.",
         "A generic measurement label does not establish actual instance compatibility. External context must identify landmarks and same assessment."]
    ))

    ctx = ("Same human body-mass and stature/recumbent-length assessment. The source glossary defines the human mass/height-cubed index and explicitly allows infant length. "
           "Use standing height for a standing-stature instance or recumbent crown-to-heel length for an infant instance; record the method and do not silently substitute one for another. "
           "This is an arithmetic index, not validated adiposity or nutrition classification.")
    models.append(record(
        "mass-height-cubed-index", "SI mass-to-height-cubed ponderal index",
        "Human body mass divided by the cube of height, using length for infants under the declared measurement method. The SI numerical convention is kg/m^3; this is not true body density because cubed stature is not measured body volume.",
        "definition", "PI", "w / L ** 3", "Ponderal index = weight (kg) divided by cubed height, or infant length, in m^3", "sacn-pi", "Nutrition and maternal weight outcomes, chapter 13 Glossary, Ponderal index, printed page 165 (PDF page 165, index 164)",
        "Introduced w,L,PI map to source weight, height/infant length and ponderal index. Dimensions M/L^3=M L^-3. The expression is homogeneous under the snapshot mass base; proposed kg/m^3 output must share kg's 1/3600000 scale. "
        "Literal 3 is the geometric cube operation, not an empirical coefficient. kg/m^3 here does not authorize a mass_density binding because the denominator is cubed linear body extent, not actual body volume. "
        "Use the exact SI convention defined in the government glossary. The Measurement Toolkit prose says cube root while its equation says cube; it is retained as conflicting discovery evidence, not the authority. "
        "The neonatal 100*w(g)/L(cm)^3 convention has numerical value one tenth of this SI kg/m^3 index; changing that unit convention alone must not create another model. No root inversion is offered.",
        [v("w", "Introduced w maps to weight (kg)", "input", "body_mass", "Actual measured human body mass for the same assessment as linear body extent.", "kg", "M", ctx, "Finite strictly positive actual mass. No ideal/adjusted mass substitution."),
         v("L", "Introduced L maps to height or length in infants", "input", "linear_body_extent", "Measured standing height or infant recumbent length, with method explicitly distinguished by context.", "m", "L", ctx, "Finite strictly positive; method must be appropriate to the individual and assessment. Not inferred from age or mass."),
         v("PI", "Ponderal index; introduced local PI", "output", "mass_height_cubed_index", "Body mass divided by the cube of the declared linear body extent, using the SI numerical convention.", "kg/m^3", "M L^-3", ctx, "Finite strictly positive quantitative index; not actual bulk body density or a body-fat fraction.")],
        ["w > 0", "L > 0"],
        ["Source definition: the SACN technical glossary uses mass over cubed height and explicitly includes infant length.",
         "Application profile: mass and body extent refer to the same individual/assessment with declared standing versus recumbent method. The pure definition has no fitted age/sex calibration or validated risk population.",
         "Permitted use is body-size arithmetic for qualified interpretation. No fetal-malnutrition, adiposity or treatment classification is supplied."],
        ["Not interchangeable with mass_density or with a differently scaled neonatal numerical index merely because units appear similar.",
         "No population percentile, clinical cutoff or diagnostic accuracy is established by the definition. Recumbent and standing length instances require method compatibility.",
         "Height/length inversion requires a cube root and is deferred under the assignment; no approximate root is substituted."],
        [source("sacn-pi", "Scientific Advisory Committee on Nutrition: Nutrition and maternal weight outcomes, full report", SACN_PDF, "Published February 3, 2026; 178-page full report linked from https://www.gov.uk/government/publications/nutrition-and-maternal-weight-outcomes-sacn-report", "Chapter 13 Glossary, Ponderal index, printed p165/PDF index164; unambiguous prose definition", "Defines the index using kg divided by cubed height or infant length in metres.", "Publication landing page, inspected 2026-11-03, footer states Open Government Licence v3.0 except where otherwise stated: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/. No separate PDF copyright statement found; third-party exclusions remain applicable.", "Source: SACN/Office for Health Improvement and Disparities, Nutrition and maternal weight outcomes (2026), glossary. Original paraphrase and formalization with synthetic checks; no report pages or figures redistributed. Retain attribution and OGL link; no endorsement or third-party clearance claimed.")],
        [ref("independent-neonatal-cube", {"w":3,"L":0.5}, 24, 1e-10,
             "Independent geometric arithmetic: a half-metre comparison cube occupies one eighth of a cubic metre, so 3 kg per comparison cube corresponds to 24 kg/m^3. The comparison cube is a normalization support, not the infant's actual volume. Synthetic index example; arithmetic-only tolerance.", "Curator-constructed newborn-size example; no observed patient or body-fat claim."),
         ref("independent-adult-cube", {"w":72.9,"L":1.8}, 12.5, 1e-10,
             "Independent hand arithmetic in rational units: 1.8^3 = 729/125 m^3, while mass is 729/10 kg, so their ratio is 125/10=12.5 kg/m^3. This verifies arithmetic and unit convention, not empirical adiposity validity.", "Curator-constructed adult-size example distinct from the infant example.")],
        [reject({"w":3,"L":0}, "Zero body extent is inadmissible and makes the denominator zero."),
         reject({"w":0,"L":0.5}, "A zero-mass body is not admitted as a valid measurement case."),
         reject({"L":0.5}, "Body mass is required.", "missing-input")],
        "Target w only: known PI>0 and L>0 give w=PI*L**3 uniquely, with original same-body/method context. Check PI=24 kg/m^3 and L=0.5 m gives w=3 kg, returning PI=24; PI=0 would imply w=0 and violates the body's positive-mass domain. Target L is a cube-root direction and is deferred by the assignment; no executable or approximate inverse is offered and no separate solve-direction model is minted.",
        ["Need linear_body_extent and mass_height_cubed_index meanings plus kg/m^3 with kg's base scale; body_mass already exists. Standing_body_height may be compatible only for a matching standing-method instance, not automatically for infant length.",
         "Known building-energy--mass-from-density-volume@r1 concerns actual sample volume; it is not the body-extent index and is not claimed as a duplicate. No runtime projection."]
    ))
    batch["models"] = models
    batch["deferred"] = [
        dict(title="Mosteller body surface area and all root-based body-size inverse forms", reason="Assignment explicitly defers root forms, even though this installed kit now supports sqrt/exact-rational powers. Mosteller relates BSA to the square root of height(cm)*mass(kg)/3600; no approximation, execution or derived candidate is supplied. Original Mosteller letter bibliographic record was inspected at PubMed (NEJM 1987;317(17):1098, DOI 10.1056/NEJM198710223171717); it has no abstract. NIDDK links the original and presents a BSA image, but accessible pixels were unavailable. Detailed validation scope remains uninspected. The cube-root inverse of the ponderal index and square-root height inverse of BMI are likewise excluded solve views.", source_urls=["https://pubmed.ncbi.nlm.nih.gov/3657876/",NIDDK_URL,"https://www.va.gov/vdl/documents/Clinical/CPRS-Clinical_Reminders/pxrm_2_22_mm.pdf"]),
        dict(title="Boyd body surface area", reason="Assignment-mandated deferral: retain the nonlinear log-dependent exponent relationship without approximating it or claiming current authorization to execute it. Official VA documentation discovered a height^0.3 and gram-mass^(0.7285-0.0188*LOG(mass)) form, but first attempted VA manual timed out; search rendering alone is not equation evidence. The VA search rendering itself says its author did not find Boyd's 1935 original and used another source. Verify exact log base, dimensionless normalization, calibration and original monograph before any future authorized record. Current engine capability is not the reason for the assignment exclusion.", source_urls=["https://www.va.gov/vdl/documents/Clinical/CPRS-Clinical_Reminders/pxrm_2_22_mm.pdf","https://www.va.gov/vdl/documents/Clinical/CPRS-Clinical_Reminders/pxrm_2_mm.pdf","https://hero.epa.gov/reference/1061257/"]),
        dict(title="Measurement Toolkit ponderal-index prose conflict", reason="Directly inspected https://www.measurement-toolkit.org/anthropometry/anthropometric-indices/ponderal says cubed height in its introduction and equation, but cube root in later prose. Do not silently reconcile that source. The completed SI definition instead uses the unambiguous SACN government glossary; diagnostic percentile and superiority claims are not imported.", source_urls=["https://www.measurement-toolkit.org/anthropometry/anthropometric-indices/ponderal",SACN_PDF]),
        dict(title="WHO waist/hip source and NICE waist/height source access", reason="WHO official publication landing page for 2008 expert consultation (published 2011) inspected; linked IRIS PDF returned 403/timeout. NICE NG246 section and official full PDF returned 403, so their search-rendered example is not claimed as direct equation evidence. BHF directly inspected formula/example and NHS eligibility support the waist-height record; NLM MeSH directly inspected definition supports waist-hip arithmetic. Exact WHO landmark protocol remains a future source priority.", source_urls=["https://www.who.int/publications/i/item/9789241501491","https://iris.who.int/bitstream/handle/10665/44583/9789241501491_eng.pdf?sequence=1","https://www.nice.org.uk/guidance/ng246/chapter/Identifying-and-assessing-overweight-obesity-and-central-adiposity","https://www.nice.org.uk/guidance/ng246/resources/overweight-and-obesity-management-pdf-66143959958725"])
    ]
    batch["handoff"] = dict(
        summary="Third checkpoint: four definitions for GFR surface de-indexing, waist-height ratio, waist-hip ratio and SI mass-height-cubed index. Definitions carry no risk categories or treatment recommendations. Root-based BSA models and specified inverse views are deferred with source/access details.",
        gaps=["All four records require meanings/units beyond the supplied snapshot. The GFR per-area input is already normalized from the reference 1.73 m^2 display convention, avoiding duplicate conversion factors.",
              "Duplicate checks limited to supplied inventory, vocabulary and own b01/b02/b03. Circumference ratios have different denominators/meanings; ponderal index is not actual body density.",
              "Clinical population/measurement eligibility is not verified by simple positive-input guards. No scientific validation of adiposity or drug dosing is asserted.",
              "Direct-source access failures and contradictory prose were retained in deferred notes. BHF source-material redistribution rights are limited; no blanket clearance claimed."],
        connections=[], queries=[],
        review_notes="Primary NIDDK HTML, BHF formula/example, NHS eligibility, NLM descriptor and SACN unambiguous glossary prose inspected directly. SACN publication landing page establishes 2026-02-03 date and links OGL; NLM MeSH terms inspected. No PDF visual check is claimed where only placeholders were available; no ambiguous formula is silently transcribed from an image. Previous preferred weight-based dose record is b02/r2; all prior original artifacts remain intact. Inverse limitations follow the explicit assignment exception for clearance/root forms. JSON/ZIP validation will be recorded after execution in the checkpoint log; handoff must be updated with actual results before packing. Scientific review remains pending.")
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
