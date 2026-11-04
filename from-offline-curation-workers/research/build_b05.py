"""Weight-change definitions, conventional renal ratio, and a conservative empirical-scope correction."""
import copy
import json
from build_b01 import ROOT, DAY, variable as v, source, reference as ref, rejection as reject, record
from build_b02 import UNKNOWN_RIGHTS, SHORT_REDIST

GIBSON = "https://nutritionalassessment.org/bodysize/"
GIBSON_VERSION = "Gibson RS and Meredith-Jones K, Principles of Nutritional Assessment: Body Size, 3rd edition, July 2024; live HTML"
GIBSON_LIC = "Chapter opening identifies CC BY 4.0 and links https://creativecommons.org/licenses/by/4.0/; both chapter and CC deed inspected 2026-11-03. No source images are used."
GIBSON_REDIST = "Attribution: Gibson RS and Meredith-Jones K, Principles of Nutritional Assessment: Body Size, 3rd ed., July 2024, CC BY 4.0. Changes: local symbols, coherent units, signed mathematical interpretation and added synthetic checks; no endorsement. Retain author/source/license links and change notice."

def gs(id, locator, evidence):
    return source(id, "Gibson and Meredith-Jones: Nutritional Assessment of Body Size", GIBSON,
                  GIBSON_VERSION, locator, evidence, GIBSON_LIC, GIBSON_REDIST)

def main():
    path = ROOT / "returns/clinical-arithmetic-codex-b05/bundle.json"
    batch = json.loads(path.read_text(encoding="utf-8"))
    batch["created"] = DAY
    models = []
    ctx = ("Same person, actual current body mass and an explicitly dated usual/baseline body mass on comparable measurement bases. "
           "Source covers human body-size assessment in adults and children; the ratio is arithmetic without validated disease-risk classification. "
           "The interval/baseline is specified externally, with no assumed three- or six-month aggregation.")
    models.append(record(
        "fractional-body-mass-decrease", "Signed fractional decrease from usual body mass",
        "Usual mass minus current mass, divided by usual mass. Positive values indicate relative decrease, negative values relative gain. The fraction is not a nutrition diagnosis or a prescribed weight target.",
        "definition", "f", "(w0 - w1) / w0", "% Wt. loss = (usual wt. - actual wt.) / usual wt. x 100%", "gibson-weight-fraction", "Body Size, section on weight changes, Box 10.4, second displayed equation and preceding paragraph",
        "Introduced w0,w1 map to usual and actual body weight; f is the source percentage expressed as a fraction in unit 1. The snapshot's percent unit has scale 0.01, so no factor 100 is inlined; a future percent display would convert f once. "
        "Use actual body masses in kg, not force; dimensions (M-M)/M=1 and mass scale cancels. Source preceding prose explicitly discusses weight loss or weight gain, supporting the signed form rather than clamping negative values. "
        "Usual/reference mass must be supplied with provenance and timing; it is not a model default. This normalized body-size definition is not equivalent to the postpartum absolute mass difference, which has a distinct baseline and dimensions M.",
        [v("w0", "Introduced w0 maps to usual wt.", "input", "body_mass", "Actual measured usual/baseline body mass at the declared reference assessment.", "kg", "M", ctx, "Finite strictly positive; baseline date, provenance and measurement comparability required externally."),
         v("w1", "Introduced w1 maps to actual wt.", "input", "body_mass", "Actual measured body mass at the current assessment for the same person.", "kg", "M", ctx, "Finite strictly positive; it may be above, equal to or below baseline."),
         v("f", "Introduced f maps to % Wt. loss in fractional units", "output", "fractional_body_mass_decrease", "Signed fraction of baseline body mass by which current mass is lower; negative values denote gain.", "1", "1", ctx, "Finite real less than 1 for positive masses; no arbitrary lower bound or clinical category is imposed.")],
        ["w0 > 0", "w1 > 0"],
        ["Source definition: Box10.4 normalizes usual-minus-actual mass by usual mass; surrounding prose includes loss and gain.",
         "Application profile: same individual and comparable actual-mass measurements, with a declared baseline and assessment interval. No clinical population calibration is needed for the arithmetic identity or claimed for risk prediction."],
        ["Body-mass change alone does not distinguish tissue, fluid, edema, dehydration or other components; the source cautions that these affect nutritional interpretation.",
         "No malnutrition threshold, desired change, intervention or monitoring schedule is encoded. A usual mass obtained by recall rather than measurement needs its own uncertainty metadata."],
        [gs("gibson-weight-fraction", "Weight changes; Box10.4, percentage weight-loss equation", "Defines fractional weight loss relative to usual weight and explicitly discusses weight gain as well as loss.")],
        [ref("independent-five-percent-decrease", {"w0":80,"w1":76}, 0.05, 1e-12,
             "Independent synthetic partition: 4 kg is one twentieth of the 80 kg baseline, so the decrease is 0.05 (5%). The fraction is stored directly; no percentage factor is part of the expression. Tolerance is numerical only.", "Curator-created ratio check, not an observed clinical result."),
         ref("independent-gain-sign", {"w0":60,"w1":63}, -0.05, 1e-12,
             "Current mass exceeds baseline by one twentieth of 60 kg; the signed decrease is -0.05, not zero or +0.05. Arithmetic-only tolerance.", "Curator-constructed materially different signed case."),
         ref("no-change-positive-masses", {"w0":60,"w1":60}, 0, 1e-12,
             "Equal positive masses give no relative change; neither body has zero mass.", "Definitional equality boundary.")],
        [reject({"w0":0,"w1":60}, "Zero reference body mass is inadmissible and makes the denominator zero."),
         reject({"w1":60}, "Baseline mass is missing.", "missing-input")],
        "Target w1: known w0>0 and f<1 give w1=w0*(1-f)>0, unique. Target w0: known w1>0,f<1 give w0=w1/(1-f)>0, unique; denominator exclusion is f!=1 and positivity strengthens it to f<1. Retain original contexts. Check f=0.05,w0=80 gives w1=76 kg and forward f=0.05; f=-0.05,w0=60 gives w1=63 and forward -0.05. At f=0, one known positive mass uniquely determines the equal other. f=1 would require zero current mass and is excluded; f alone without either mass leaves infinitely many positive pairs when f<1. No biological causal inverse is asserted.",
        ["Need fractional_body_mass_decrease meaning; body_mass, kg, 1 and percent already exist. Canonical expression returns fraction; a percent output must use the registry scale once.",
         "Other domains' population or capacity ratios share algebraic shape but not this human body-mass definition or context. No runtime projection."]
    ))

    ctx = ("Same person, two actual body-mass assessments on comparable measurement bases, and the positive continuous elapsed interval between them. "
           "Source human assessment includes adults and children; this endpoint mean is not a fitted growth curve or age-specific normal rate. "
           "Direction is later mass minus earlier mass; time is supplied in seconds, not visit count or a calendar-year default.")
    models.append(record(
        "mean-body-mass-change-rate", "Mean body-mass change rate between assessments",
        "Signed change in actual body mass divided by elapsed assessment time. A positive rate indicates endpoint gain and a negative rate endpoint loss, without assuming change was linear within the interval.",
        "definition", "r", "(w1 - w0) / t", "Rate of change = (body weight present - body weight initial) / (day present - day initial), in kg/day", "gibson-mass-rate", "Box10.4, third displayed equation, Rate of change",
        "Introduced w1 and w0 map to present and initial mass; introduced t is the positive elapsed interval corresponding to the source day difference, normalized to seconds. r is kg/s rather than kg/day; day conversion belongs to unit scales (86400 s for a continuous 24-hour day), not an inlined equation factor. "
        "Dimensions (M-M)/T=M T^-1; kg's numerical scale applies equally to the input masses and output rate, so the expression is canonical. "
        "The endpoint definition gives a time average; no constant instantaneous growth assumption is introduced. It is not a separately minted inverse of postpartum mass retention because it defines a generic time-normalized quantity with a supplied interval and no pregnancy-specific baseline.",
        [v("w0", "Introduced w0 maps to body weight initial", "input", "body_mass", "Actual measured body mass at the initial assessment.", "kg", "M", ctx, "Finite strictly positive measured mass."),
         v("w1", "Introduced w1 maps to body weight present", "input", "body_mass", "Actual measured body mass at the later assessment.", "kg", "M", ctx, "Finite strictly positive measured mass; gain, loss and equality all admitted."),
         v("t", "Introduced t maps to day present minus day initial, normalized to elapsed seconds", "input", "duration", "Continuous elapsed duration between these two mass assessments.", "s", "T", ctx, "Finite strictly positive elapsed interval; no source-supported minimum interval or rounding default is invented."),
         v("r", "Introduced r maps to Rate of change", "output", "mean_body_mass_change_rate", "Signed endpoint body-mass change per elapsed time over the stated interval.", "kg/s", "M T^-1", ctx, "Finite real, including zero and negative rates; no instant-by-instant trajectory is inferred.")],
        ["w0 > 0", "w1 > 0", "t > 0"],
        ["Source definition: the body-size text divides endpoint mass change by the matched difference of assessment days.",
         "Application profile: interpret time units as continuous elapsed duration and masses as comparable observations of the same person. Source addresses human body-size assessment, not a calibrated prediction of healthy growth."],
        ["Endpoint mean may hide nonlinear growth or fluctuation and does not separate tissue, water or measurement error.",
         "No interval adequacy, target gain, age-based threshold, feeding decision or monitoring protocol is supplied; measurement uncertainty can dominate small endpoint changes."],
        [gs("gibson-mass-rate", "Box10.4, Rate of change; surrounding weight-change discussion", "Defines an endpoint mass-change rate using the difference of assessment times.")],
        [ref("independent-twenty-day-gain", {"w0":60,"w1":62,"t":1728000}, 1.1574074074074074e-6, 1e-16,
             "Independent synthetic interval partition: a total 2 kg increase across 20 equal 24-hour days corresponds to 0.1 kg/day. Convert that counted mean once to kg/s; t=20*86400 s. This is an average, not a claimed daily trajectory. Tolerance is arithmetic only.", "Curator-constructed mean-rate example."),
         ref("independent-thirty-day-loss", {"w0":63,"w1":60,"t":2592000}, -1.1574074074074074e-6, 1e-16,
             "A signed 3 kg decrease over 30 equal days corresponds to -0.1 kg/day, normalized to kg/s. Materially different sign and interval; no linear within-interval loss assumed.", "Curator synthetic endpoint example."),
         ref("zero-net-change", {"w0":60,"w1":60,"t":86400}, 0, 1e-20,
             "Equal positive endpoint masses have zero net mean change over a positive day, without proving the instantaneous mass remained constant.", "Definitional endpoint identity.")],
        [reject({"w0":60,"w1":62,"t":0}, "Two endpoints with zero elapsed interval cannot define this mean rate."),
         reject({"w0":60,"w1":62}, "Elapsed interval is missing; visit count or nominal month is not substituted.", "missing-input")],
        "Target w1: known w0>0,t>0 and r give w1=w0+r*t, requiring w1>0. Target w0: known w1>0,t>0 and r give w0=w1-r*t>0. Target t: known endpoint masses and r!=0 give t=(w1-w0)/r; require t>0, so change and rate must have the same sign. Retain original guards/context. Check r=1.1574074074074074e-6 kg/s,w0=60,t=1728000 s gives w1=62 and forward r matches. For r=0 and w1=w0, any t>0 fits; for r=0 and unequal masses none fits. Equal masses with r!=0 would give t=0 and are excluded. These inverses do not establish a physiological causal law.",
        ["Need mean_body_mass_change_rate meaning and kg/s unit with kg's mass scale; body_mass, kg, duration and s already exist. No runtime projection.",
         "Unit match with infused constituent mass rate does not authorize semantic binding; a patient's net body-mass change is a different quantity/support."]
    ))

    ctx = ("Same adult assessment and paired serum BUN and serum creatinine measurements on the conventional mass-concentration basis. "
           "Numerator is nitrogen mass associated with urea, not total urea mass or urea amount concentration. "
           "This laboratory ratio is a definition, with no validated diagnostic interpretation or therapeutic action supplied.")
    models.append(record(
        "serum-bun-creatinine-mass-ratio", "Conventional serum BUN-to-creatinine mass-concentration ratio",
        "Serum urea-nitrogen mass concentration divided by serum creatinine mass concentration. The explicit mass basis prevents silently substituting an SI urea-to-creatinine molar ratio, which has a different numerical convention.",
        "definition", "R", "B / C", "BUN/Creatinine ratio = BUN divided by creatinine", "boston-ratio", "Test Code1013, Methodology; independently corroborated by ACL Calculations manual January2026, page1",
        "Introduced B,C,R map to serum BUN, serum creatinine and their ratio. Both inputs use kg/m^3, corresponding to the conventional mg/dL mass concentrations documented by MedlinePlus; identical scales cancel. Dimensions (M L^-3)/(M L^-3)=1. "
        "The numerator counts nitrogen in urea, whereas the denominator counts creatinine mass. Equal dimensions do not make their molecular/mass definitions interchangeable; no urea-to-nitrogen or molarity conversion is inlined. "
        "Source operator's prose describes serum; its preferred-specimen list names heparin plasma. This arithmetic record explicitly uses serum quantities and makes no claim to resolve the operator's specimen workflow or authorize plasma substitution. "
        "Normal ranges and diagnostic risk descriptions are not imported as guards; this is a ratio of two supplied laboratory quantities.",
        [v("B", "Introduced B maps to BUN", "input", "serum_urea_nitrogen_mass_concentration", "Nitrogen mass contained in serum urea per serum volume; conventional BUN analyte basis.", "kg/m^3", "M L^-3", ctx, "Finite nonnegative, with analyte/assay basis supplied. Do not substitute total urea mass or a bare molar urea number."),
         v("C", "Introduced C maps to Creatinine", "input", "serum_creatinine_mass_concentration", "Serum creatinine mass per serum volume at the same assessment.", "kg/m^3", "M L^-3", ctx, "Finite strictly positive, on the same volume unit basis as B; no flooring or clamping."),
         v("R", "Introduced R maps to BUN/Creatinine Ratio", "output", "serum_bun_creatinine_mass_ratio", "Dimensionless conventional BUN nitrogen-mass to creatinine-mass concentration ratio.", "1", "1", ctx, "Finite nonnegative ratio. No diagnostic category or molar-ratio equivalence is asserted.")],
        ["B >= 0", "C > 0"],
        ["Source definition: the test operator directly states BUN divided by creatinine; ACL's laboratory calculation reference independently lists the same relationship.",
         "Application profile: conventional serum mass-concentration basis, with both analyte definitions and same assessment established externally. This identity has no empirical patient-population calibration or diagnostic accuracy claim."],
        ["Total urea mass and molar urea/creatinine ratios are distinct inputs/conventions and cannot be bound by unit label alone.",
         "No ratio threshold, diagnosis or treatment is supplied; source operator specimen-list/prose differences remain a workflow review issue beyond this serum arithmetic profile."],
        [source("boston-ratio", "Boston Heart Diagnostics: BUN/Creatinine Ratio, Test1013", "https://bostonheartdiagnostics.com/test/bun-creatinine-ratio/", "Live HTML inspected 2026-11-03; page revision date not established", "Test Details, description and Methodology; preferred specimen noted separately", "Describes the serum BUN/creatinine calculation and explicitly specifies division.", "Page footer copyright Boston Heart Diagnostics; no redistribution terms established for this accessed page. Terms unknown; do not infer a license from public access.", SHORT_REDIST),
         source("acl-ratio", "ACL Laboratories: Calculations for Reference Manual", "https://referencemanual.aclab.com/wp-content/uploads/2026/01/Calculations-for-Reference-Manual_01.2026.pdf", "Revision January2026; 6-page PDF", "Page1 (PDF index0), BUN/Creatinine Ratio row", "Lists the ratio formula when both analytes are ordered.", UNKNOWN_RIGHTS, SHORT_REDIST),
         source("medline-units", "MedlinePlus Medical Encyclopedia: Basic metabolic panel", "https://medlineplus.gov/ency/article/003462.htm", "Review date May19,2025; A.D.A.M./Ebix material hosted by MedlinePlus", "Normal Results: BUN and creatinine unit entries; footer rights statement", "Uses mg/dL for conventional BUN and creatinine reporting, separately from SI amount-concentration values.", "Same-page footer inspected2026-11-03 states Ebix copyright and personal noncommercial viewing; other content uses require consent, with copying/derivative restrictions. No reuse permission or legal clearance for source content is inferred.", "Only independently authored mathematical facts and a very short original unit-convention paraphrase are returned; no reference ranges, source paragraphs, graphics or page copies. Downstream source-content rights remain unresolved.")],
        [ref("independent-twenty-to-one", {"B":0.2,"C":0.01}, 20, 1e-10,
             "Independent synthetic unit count: conventional 20 mg/dL of BUN nitrogen and 1 mg/dL of creatinine form twenty equal numerator units per denominator unit. Normalize both to kg/m^3:0.2 and0.01; the ratio stays20. Arithmetic-only tolerance.", "Curator-created mass-ratio example; not patient data or a diagnostic normal-range claim."),
         ref("independent-twelve-to-one", {"B":0.18,"C":0.015}, 12, 1e-10,
             "18 mg/dL divided into 1.5 mg/dL units gives twelve units, with independently normalized inputs0.18 and0.015 kg/m^3. This checks a different nonunit denominator and the same mass basis.", "Curator-constructed arithmetic evidence."),
         ref("zero-nitrogen-ideal-limit", {"B":0,"C":0.01}, 0, 1e-20,
             "Ideal no-urea-nitrogen mathematical limit at positive serum creatinine gives ratio zero. It is not a claimed clinical assay value.", "Definitional boundary.")],
        [reject({"B":0.2,"C":0}, "Zero serum creatinine makes this ratio undefined."),
         reject({"B":0.2}, "Serum creatinine is missing.", "missing-input")],
        "Target B: known R>=0,C>0 give B=R*C uniquely. Target C: known B>0,R>0 give C=B/R>0. Retain original serum/analyte contexts. Check R=12,C=0.015 kg/m^3 gives B=0.18 and forward R=12. At R=0,C>0, B=0 uniquely; if B=R=0 and C is unknown, any C>0 satisfies the definition. B>0,R=0 has no finite solution; B=0,R>0 would imply C=0 and violates the denominator domain. These are laboratory-ratio algebraic views, not clearance inversions or clinical inferences.",
        ["Need serum_urea_nitrogen_mass_concentration and serum_bun_creatinine_mass_ratio meanings; reuse serum_creatinine_mass_concentration from b02. kg/m^3 needs the same mass scale in numerator and denominator. No runtime projection.",
         "Explicit conventional mass basis and specimen matrix must accompany any actual binding; source operator's serum/plasma workflow difference is not resolved by this ratio record."]
    ))

    old = json.loads((ROOT / "returns/clinical-arithmetic-codex-b02/bundle.json").read_text(encoding="utf-8"))
    cg = copy.deepcopy(next(m for m in old["models"] if m["id"].endswith("--cockcroft-gault-creatinine-clearance")))
    cg["revision"] = "r2"
    cg["summary"] = ("Conservative self-audit correction of b02/r1: preserve the historical equation, numerical arithmetic and known cohort facts, "
                     "but mark the candidate blocked because original concentration/renal-function calibration endpoints and assay/method scope were not directly established. "
                     "Positive numeric inputs and age18–92 do not supply that missing empirical applicability evidence. No clinical approval or new validation is asserted.")
    cg["unresolved"] = ["Empirical applicability cannot be fully bounded from directly inspected evidence: original methods/tables and calibration concentration/renal-function range were not inspectable. The formula's meaning is clear, but which positive assay values constitute supported calibrated use remains a scientific review blocker. The source-stated female reduction also lacks equivalent validation; no unsupported interval is invented."]
    cg["integration"]["status"] = "blocked"
    cg["integration"]["gaps"].insert(0, "Scientific scope blocker: obtain original methods/calibration evidence or a directly inspected appropriate validation study before considering this candidate ready for scientific review as an applicable empirical mapping. Do not use r1's requires-extension status to imply the source gap was resolved.")
    models.append(cg)
    batch["models"] = models
    batch["deferred"] = [
        dict(title="Fractional sodium excretion from paired measurements", reason="Direct original study inspected: Schreuder et al., Nephron2017;136:221–225, DOI10.1159/000468547, https://pmc.ncbi.nlm.nih.gov/articles/PMC5516416/. Equation1 rendering labels urinary sodium nmol/L versus serum mmol/L while separately normalizing creatinine units. Do not silently correct that unit ambiguity. Study cohort is ages4–18, GFR>60 mL/min/1.73m^2,761 reliable collections; paper explicitly warns against a universal diagnostic cutoff. A faithful future record needs an unambiguous primary equation/unit source and a precise distinction between a creatinine-clearance-referenced ratio and a true filtered-sodium fraction. Device-manual alternative https://fcc.report/FCC-ID/ZLZ-EPM/4297304.pdf was discovery only; direct retrieval403. No candidate, diagnostic cutoff or approximate correction is returned.", source_urls=["https://pmc.ncbi.nlm.nih.gov/articles/PMC5516416/","https://fcc.report/FCC-ID/ZLZ-EPM/4297304.pdf"]),
        dict(title="Weight-loss formula from an ambiguous PDF rendering", reason="Health Hawke's Bay 2023 guidance, Appendix2 printed p41/PDF index43, was inspected as extracted text. The100 multiplier's fraction placement is visually ambiguous and screenshot pixels are unavailable, so it is not the equation authority. Completed weight-change definitions instead use Gibson/Meredith-Jones's directly inspected HTML Box10.4, which also explicitly discusses gain. No nutritional score, treatment or monitoring protocol is imported.", source_urls=["https://healthhb.co.nz/wp-content/uploads/2023/10/Diabetes-Care-for-Age-Related-Residential-Care-Facilities-in-Hawkes-Bay-2023-v2.pdf",GIBSON]),
        dict(title="Usual-weight percentage as another record", reason="Same two-weight normalization already represented by fractional-body-mass-decrease; percentage of usual mass is its complementary view (1-f) under the same baseline. Preserve as source evidence rather than minting a cosmetic complement. Time-normalized rate is a distinct quantity and is separately defined from the source's own equation.", source_urls=[GIBSON]),
        dict(title="Cockcroft-Gault empirical applicability", reason="Supersedes b02/r1's integration status with blocked r2 under the same model ID. Original files are preserved. Full methods/calibration-range evidence remains unavailable; a source-backed equation and passing arithmetic do not settle empirical scope. Continue only when a directly inspected original/validation source supplies the missing applicability facts; do not invent concentration endpoints or broaden the female validation claim.", source_urls=["https://pubmed.ncbi.nlm.nih.gov/1244564/","https://www.drugtnt.com/ref/RenalDosing/Cockcroft_1976.pdf"])
    ]
    batch["handoff"] = dict(
        summary="Fifth checkpoint: three new arithmetic definitions (signed fractional body-mass decrease, mean body-mass change rate, conventional serum BUN/creatinine mass ratio) and a blocked r2 revision of the historical Cockcroft–Gault candidate. Original r1 remains preserved; use r2's conservative scientific-blocker status.",
        gaps=["No clinical diagnoses, treatment choices, risk thresholds or monitoring instructions are returned. New definitions require quantity/unit extensions; no toolkit/registry changes.",
              "Cockcroft–Gault r2 is blocked on empirical applicability evidence; its passing numerical checks do not make it scientifically ready. Full original scope/assay evidence remains needed.",
              "FENa unit ambiguity, uninspected source images and source-specific usage rights remain explicitly deferred; no guessed equation correction is supplied.",
              "Duplicate search remains limited to the2026-11-01 inventory, vocabulary and own five batches. BMI/dose/flow/ratio/data-state meanings are compared semantically, not by expression spelling alone."],
        connections=[], queries=[],
        review_notes="Primary author-hosted 3rd-edition July2024 body-size chapter and CC-BY4.0 attribution inspected; explicit loss/gain and time-rate equations support both new body-change definitions. Boston Heart formula and ACL January2026 calculation row inspected directly; MedlinePlus unit convention and restrictive source footer recorded. Self-audit conservatively reclassifies CG as blocked because age/population facts alone do not supply its missing empirical calibration range. Earlier preferred weight-based dose is r2; other earlier records remain unreviewed requires-extension candidates. JSON/ZIP validation will be recorded after execution in the checkpoint log; handoff must be updated with actual results before packing. No central or scientific approval has occurred.")
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
