"""Prepare only this requested correction; preserve all earlier artifacts."""
import json
from pathlib import Path
from datetime import datetime, timezone

folder = Path(__file__).resolve().parent
path = folder / 'bundle.json'
batch = json.loads(path.read_text(encoding='utf-8'))
faq = 'https://www.kidney.org/sites/default/files/441-8491_2202_faqs_aboutgfr_v5.pdf'
nkf = 'https://www.kidney.org/professionals/kdoqi/cockcroft-gault-equation-estimating-creatinine-clearance'
pub = 'https://pubmed.ncbi.nlm.nih.gov/1244564/'
expr = '(1 - 0.15 * z) * (140 - a) * w / (K * sCr)'
context = 'same adult assessment; source-era assay basis and independently established historical applicability; coefficient matched to this formula version'

def variable(symbol, source_symbol, role, meaning, definition, unit, dimensions, domain):
    return dict(symbol=symbol, source_symbol=source_symbol, role=role, quantity_id=meaning,
                definition=definition, unit=unit, dimensions=dimensions, context=context, domain=domain)

variables = [
    variable('a', 'age', 'input', 'chronological_age_year_index', 'Numerical chronological age in years, not elapsed seconds.', 'years', '1 (year index)', '18 <= a <= 92; derivation age coverage, not universal validation.'),
    variable('w', 'weight', 'input', 'body_mass', 'Actual measured total body mass; ideal/adjusted substitutes are outside this record.', 'kg', 'M', 'Positive finite mass.'),
    variable('sCr', 'SCr', 'input', 'serum_creatinine_mass_concentration', 'Serum creatinine mass per serum volume on the historical assay basis; no rounding-up or modern-assay correction is applied.', 'kg/m^3', 'M L^-3', 'Positive for algebra only. No validated serum-creatinine interval is established here; independent applicability confirmation is required.'),
    variable('z', 'introduced indicator: source multiplier 0.85 if female, otherwise 1', 'input', 'cockcroft_gault_female_branch_indicator', 'Historical formula branch: 0 male, 1 female; female branch is an estimated adjustment, not a validated female calibration.', '1', '1', 'Exactly 0 or 1; no inference of sex or gender.'),
    variable('K', 'introduced dimensional parameter: source denominator coefficient 72 normalized from kg*min*dL/(mg*mL) into seconds', 'input', 'cockcroft_gault_divisor', 'Version-specific empirical denominator parameter, supplied with provenance. For the unmodified historical 72-form K=432000000000 s. It is not a patient elapsed time or a universal constant.', 's', 'T', 'Positive finite parameter; this historical profile requires independently supplied K=432000000000 s. Other values require separately evidenced calibration and are not validated by this record.'),
    variable('C', 'eClcr', 'output', 'creatinine_clearance', 'Historical algebraic estimate of non-indexed creatinine clearance, an effective serum volume per time; not GFR.', 'm^3/s', 'L^3 T^-1', 'Positive under guards. Calculability alone does not establish empirical applicability.'),
]

assumptions = [
    'Source scope: White-men derivation, ages18–92; NKF attests measured creatinine-clearance coverage approximately30–130 mL/min and pre-standardization serum assays (FAQ Q16/Table3; original abstract).',
    'Calibrated-domain limitation: guards express algebraic admissibility only. Scientific interpretation requires independent confirmation of matching historical population, stable assessment and assay calibration; a positive sCr alone is insufficient.',
    'Parameter profile: caller supplies the evidenced historical K=432000000000 s; K is an explicit empirical parameter because literals carry no dimensions. It is not a freely selectable duration or an authorized recalibration.',
    'Application profile: this is forward arithmetic for qualified interpretation; it does not select treatment, drug dose or monitoring. Female-branch calculations are formal arithmetic only, without a validated female-population claim.',
]
limitations = [
    'No inspected source establishes serum-creatinine calibration endpoints. The approximately30–130 mL/min range concerns measured clearance, not sCr or a guard on the predicted output; no concentration interval is invented or inferred from it.',
    'The historical equation is not expressed for standardized creatinine. Modern IDMS-traceable measurements are not assumed interchangeable; no assay conversion is supplied. Broader-population and female validation are not established.',
    'Measured creatinine clearance and measured GFR differ. This output is not BSA-indexed, is not a GFR measurement, and must not be bound to GFR solely because units match.',
    'Original abstract reports correlation0.83 against mean paired24-hour clearances in236 patients; no individual error bound or confidence interval is asserted. Numerical checks validate transcription/unit handling, not clinical accuracy.',
    'K positivity does not enforce version matching; caller/reviewer must verify the coefficient provenance and all non-scalar applicability conditions. Inverse solving for K or patient inputs is excluded from this return.',
]
sources = [
    dict(id='nkf-faq-2022', kind='primary', title='National Kidney Foundation: Frequently Asked Questions About GFR Estimates', url=faq,
         version='Copyright2022; document441-8491_2202, v5 URL', accessed='2026-11-03',
         locator='Q16 begins printed7/PDF index6; equation/units printed8/PDF index7; Table3 printed7/PDF index6; Q40 printed15/PDF index14.',
         evidence='Official handbook directly inspected as extracted text: historical measured-clearance span about30–130 mL/min; unstandardized assay basis; White-men table; 72-form equation, age-years, kg, mg/dL and mL/min conventions. Clear text equation; screenshots yielded no inspectable pixels.',
         license='PDF copyright2022 NKF. Specific reuse license unknown; https://www.kidney.org/about/copyright attempted2026-11-03 but inaccessible. No clearance inferred.',
         redistribution='Only short original paraphrase and relationship metadata returned; PDF, screenshots and full text are excluded. Permission for broader reuse remains unestablished.'),
    dict(id='nkf-cg-limitations', kind='primary', title='Cockcroft-Gault Equation for Estimating Creatinine Clearance', url=nkf,
         version='Undated live NKF guidance, directly inspected2026-11-03', accessed='2026-11-03',
         locator='Limitations of the Cockcroft-Gault equation; Limitations of Practice Adaptations.',
         evidence='NKF describes249 White males, an estimated rather than quantified female adjustment, pre-standardization assays, and validation against measured clearance rather than GFR. It cautions about weight substitutions and empirical low-creatinine adjustments.',
         license='Specific terms unknown; no open-content license established on inspected page. NKF copyright endpoint inaccessible2026-11-03.',
         redistribution='Original concise paraphrase only; no webpage or clinical instructions redistributed; broader reuse rights unresolved.'),
    dict(id='cockcroft-gault-1976-abstract', kind='primary', title='Prediction of creatinine clearance from serum creatinine — Cockcroft DW, Gault MH', url=pub,
         version='Nephron1976;16(1):31–41; DOI10.1159/000180580; PubMed abstract inspected, full methods not inspected', accessed='2026-11-03',
         locator='PubMed Abstract, both paragraphs.',
         evidence='Original abstract reports249 derivation patients ages18–92,236 comparison patients with paired24-hour clearances, and correlation0.83. It does not supply serum-creatinine calibration limits or an individual prediction interval.',
         license='Article rights not established by PubMed indexing; original publisher terms not inspected. Bibliographic/abstract access is not a redistribution license.',
         redistribution='Bibliographic facts and short original paraphrase only; full article and abstract text not returned.'),
]

def ref(id, a, w, scr, z, expected, method):
    return dict(id=id, inputs=dict(a=a,w=w,sCr=scr,z=z,K=432000000000), expected=expected,
                tolerance=1e-18, method=method+' Absolute1e-18 m^3/s covers binary floating arithmetic, not empirical uncertainty.',
                provenance='Independent constructed arithmetic in the directly inspected NKF conventional-unit equation; synthetic inputs, not published patient results or clinical validation.')

model = dict(
    id='clinical-arithmetic--cockcroft-gault-creatinine-clearance', revision='r3',
    title='Historical Cockcroft–Gault creatinine-clearance arithmetic with explicit dimensional divisor',
    summary='Correction superseding b02/r1 and b05/r2. Addresses reviewerAA by an explicit calibrated-domain limitation and NKF historical context, and mechanical staging failure by replacing the dimensional bare divisor with supplied empirical input K in seconds. No new serum-creatinine bounds or clinical validation are claimed.',
    kind='empirical',
    relationship=dict(output_symbol='C', expression=expr,
        original_equation='eClcr = ((140-age)*weight)/(72*SCr), multiplied by0.85 if female; eClcr[mL/min], age[years], weight[kg], SCr[mg/dL].',
        source_id='nkf-faq-2022', locator='Q16, printed8 / PDF index7; historical context begins printed7 / PDF index6.',
        translation_notes='Introduced a,w,sCr,C map to age,weight,SCr,eClcr; z encodes the stated branch, so1-0.15*z reproduces1 or0.85. Introduced K carries the source empirical72-form coefficient normalized into seconds: sCr[mg/dL]=100*sCr[kg/m^3] and1 mL/min=1e-6/60 m^3/s, hence K=72*100*60*1e6 s=432000000000 s. These are a derivation of a dimensional parameter value, not conversion factors in the executable expression. Dimensional check: (dimensionless)*M/(T*(M/L^3))=L^3/T; mass scale cancels under both coherent SI and the kit kWh-based mass convention. Pure1 is branch identity;140 is the source age-index intercept;0.15 is1-0.85. K is never solved for or inferred from the patient. Guards on K use positivity only, avoiding dimensionally invalid equality to a bare seconds literal.'),
    variables=variables,
    constants=[dict(literal=140, meaning='Historical age-index intercept; age is numerical years.', unit='years', source_id='nkf-faq-2022', locator='Q16 equation printed8/PDF7.'),
               dict(literal=0.15, meaning='Complement of source female multiplier0.85, used only for binary branch encoding.', unit='1', source_id='nkf-faq-2022', locator='Q16 equation printed8/PDF7.')],
    guards=['a >= 18','a <= 92','w > 0','sCr > 0','z * (z - 1) == 0','K > 0'],
    assumptions=assumptions, limitations=limitations, unresolved=[], sources=sources,
    references=[
        ref('ordinary-male-conventional-units',50,72,0.012,0,0.00000125,'Independent conventional-unit route:1.2 mg/dL; (140-50)*72/(72*1.2)=75 mL/min; converting the exact rational75/60000000 gives1.25e-6 m^3/s.'),
        ref('female-branch-arithmetic-only',50,72,0.012,1,0.0000010625,'Branch contrast: the same conventional-unit75 mL/min times0.85 is63.75 mL/min=1.0625e-6 m^3/s. This tests source branch encoding, not female calibration.'),
        ref('upper-age-boundary',92,60,0.01,0,40/60000000,'Age-boundary identity in conventional units:48*60/(72*1)=40 mL/min. Conversion uses the exact rational40/60000000. Age92 is an observed derivation boundary, not a singular limit.'),
    ],
    rejection_cases=[
        dict(kind='domain',inputs=dict(a=50,w=72,sCr=0,z=0,K=432000000000),reason='Zero concentration is outside the reciprocal algebraic domain; it is not an empirical lower calibration endpoint.'),
        dict(kind='domain',inputs=dict(a=50,w=72,sCr=0.012,z=0,K=0),reason='Zero empirical divisor is singular; no clearance can be computed.'),
        dict(kind='domain',inputs=dict(a=17,w=72,sCr=0.012,z=0,K=432000000000),reason='Outside the declared18–92 derivation-age profile; no pediatric extrapolation.'),
        dict(kind='domain',inputs=dict(a=50,w=72,sCr=0.012,z=0.5,K=432000000000),reason='The historical selector is binary; fractional branch mixing is not a source relationship.'),
        dict(kind='missing-input',inputs=dict(a=50,w=72,sCr=0.012,z=0),reason='The empirical divisor must be explicitly supplied with units/provenance; no hidden coefficient default.'),
    ],
    inverse_notes='Forward clearance evaluation only. All denominators require K>0 and sCr>0; other original guards and non-scalar scope conditions also apply. No clearance inversion, patient-input solve or coefficient fit is proposed or tested, consistent with the assignment. In particular K is an evidenced model parameter, never a target for free inverse solving.',
    integration=dict(status='requires-extension',runtime_model=None,
        gaps=['Local kit2026-10-31.6 snapshot profile mechanics-1+finance-2+economics-5+biology-3+cs-4 predates clinical-2. It lacks chronological_age_year_index, serum_creatinine_mass_concentration, cockcroft_gault_female_branch_indicator and creatinine_clearance, and units kg/m^3 and m^3/s. Owner reports central clinical-2 supplies these; no central access or local toolkit modification performed.',
              'Map/register cockcroft_gault_divisor with dimensionT and units as seconds if absent in clinical-2; do not alias it to patient duration. Its version/provenance must select the historical4.32e11 s coefficient. Full clinical-2 projection cannot be certified by this local snapshot.'],duplicate_of=[])
)
batch.update(created=datetime.now(timezone.utc).date().isoformat(),example_only=False,models=[model],deferred=[],handoff=dict(
    summary='One requested r3 correction to existing clinical-arithmetic--cockcroft-gault-creatinine-clearance; supersedes both b02/r1 and b05/r2. No new relationship coverage.',
    gaps=['Full clinical-2 runtime projection unavailable locally; dimensional regression and canonical-scale arithmetic are checked separately without altering the toolkit.',
          'Prior b02/b05 bundle/ZIP files referenced by retained SESSION.json are absent from the current workspace snapshot. Correction reconstructed from supplied review, retained public quantity definitions and newly inspected sources; no exact byte diff against absent originals is claimed.'],
    connections=[],queries=[],
    review_notes='User review: AA requires calibrated-domain context; Z recommended r1 science but staging rejected dimensional literal. r3 preserves the same72-form and restrictions, adds independently supplied K in seconds, removes the implicit dimensional literal, and explicitly limits empirical claims. Earlier records are superseded, not admitted. Existing historical SESSION and toolkit version are retained. Scope notes distinguish measured-clearance coverage from unknown serum-creatinine endpoints; no predicted-output guard substitutes for measured validation. See validation.json and dimension-check.json beside this bundle for actual checks. Reviewer must reassess r3; successful data validation is not approval.'
))
path.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(path)
