"""Broaden the same interface-imaging law to include its evidenced plane limit."""

import copy
import json

from curation_support import RETURN_ROOT, reference, rejection, variable, write_batch

prior = json.loads((RETURN_ROOT / "waves-and-optics-codex-b02" / "bundle.json").read_text(encoding="utf-8"))
record = copy.deepcopy(next(item for item in prior["models"] if item["id"].endswith("--spherical-interface-imaging")))
record["revision"] = "r2"
record["title"] = "Paraxial imaging at one spherical or plane refracting interface"
record["summary"] = "Broadens b02 spherical-interface-imaging@r1 under the same ID using signed curvature C=1/R and the separately evidenced C=0 plane-interface apparent-depth limit. This is a scope/parameterization revision, not another independent model or a renamed apparent-depth clone."
context = "Same single spherical or plane interface, optical axis and surface vertex/reference plane, incident medium 1 and transmitted semi-infinite medium 2, common optical frequency and specified material states. Real-is-positive convention: real object d_o>0, real transmitted image d_i>0, virtual image d_i<0. Signed curvature C>0 has center on outgoing side (convex toward real object), C<0 concave toward it; C=0 is a plane, not a zero-radius surface."
record["relationship"].update(
    expression="n_2 * d_o / ((n_2 - n_1) * C * d_o - n_1)",
    original_equation="n_1/d_o+n_2/d_i=(n_2-n_1)/R (Eq. 2.11); plane normal-view apparent depth h_i=(n_2/n_1)*h_o (Eq. 2.10)",
    locator="University Physics 3 section 2.3 Eqs. 2.10 and 2.11, plane normal-view paragraph and single-surface sign convention",
    translation_notes="Introduce signed geometric surface curvature C=1/R for finite nonzero spherical radius, with C=0 representing the plane boundary. Solve the unchanged Eq. 2.11 for d_i in curvature coordinates. Eq. 2.10 independently supports the plane limit: source apparent depth h_i is a positive distance on the incident side, so local d_i=-h_i and d_o=h_o; C=0 gives d_i=-(n_2/n_1)*d_o. Source h_i here is axial apparent depth, not the transverse image height used in magnification; do not bind those quantities by shared symbol. The old R!=0 exclusion becomes exclusion of infinite C (all scalar inputs must be finite), not C!=0. Thus admitting C=0 does not silently restore the original forbidden R=0. Dimensions: numerator L, denominator (1)*(L^-1)*L-1=1, output L. m and coherent research 1/m avoid inlined unit conversion. Normal-view/paraxial source approximations remain explicit; no new approximation of a forbidden angle law is authored."
)
record["variables"] = [
    {**port, "context": context} if port["symbol"] != "R" else
    variable("C", "Introduced C=1/R for a sphere; C=0 is plane boundary evidenced by Eq. 2.10", "input", "signed_optical_surface_curvature", "Signed inverse spherical radius, positive with curvature center on outgoing side; zero for a plane refracting interface.", "1/m", "L^-1 (m^-1)", context, "Any finite signed curvature, including zero; finite C excludes the source's zero-radius singular surface.")
    for port in record["variables"]
]
record["guards"] = ["n_1 >= 1", "n_2 >= 1", "d_o > 0", "((n_2 - n_1) * C * d_o - n_1) ** 2 > 0"]
record["assumptions"] = [
    "Source assumption: one refracting interface and paraxial rays; for a plane boundary, the apparent-depth relation is the near-normal viewing approximation, not arbitrary oblique viewing.",
    "Source geometry: medium 2 continues without a subsequent refracting interface; both supplied phase indices correspond to the same optical frequency and declared medium states.",
    "Source/profile convention: real-is-positive conjugates and a finite real object d_o>0; signed surface curvature follows the outgoing-center-positive convention.",
    "Application profile: ordinary transparent real-index media n_1,n_2>=1. Equal indices and zero curvature are explicitly admitted no-refraction/plane limits; no default material values."
]
record["limitations"] = [
    "No second surface or complete thick-lens/sphere system is included; a later interface needs separate modeling.",
    "An object at the curved-interface first focus produces parallel transmitted rays and no finite d_i.",
    "Plane-interface apparent depth depends on viewing angle outside the near-normal/paraxial regime; Eq. 2.10 is not asserted as exact at arbitrary angles.",
    "No image intensity, transmission fraction, group delay, diffraction or polarization prediction is provided."
]
record["sources"][0]["locator"] += "; r2 additionally inspects plane-interface Eq. 2.10 and preceding normal-view approximation paragraph"
record["sources"][0]["evidence"] = "Section 2.3 supplies both the index-weighted spherical conjugate law and the near-normal plane apparent-depth law. Signed curvature extends the same conjugate relationship to the plane limit, after converting the positive axial apparent depth to a negative virtual-image distance. The source's h_i in the plane passage is an axial depth, not transverse image height."
for item in record["references"]:
    radius = item["inputs"].pop("R")
    item["inputs"]["C"] = 1 / radius
    item["method"] += " For r2 the same physical radius is supplied as introduced curvature C=1/R; expected and tolerance are unchanged."
record["references"].append(reference(
    "independent-plane-apparent-depth", {"n_1": 1.5, "n_2": 1, "C": 0, "d_o": 0.3}, -0.2, 1e-12,
    "Independent synthetic near-normal ray construction: object depth 0.300 m in index 1.5, plane interface, outgoing medium index 1. At lateral surface intercept 0.001 m the incident slope magnitude is 0.001/0.300=1/300; the source's paraxial boundary geometry gives outgoing slope 1.5/300=0.005. Back-projecting 0.001/0.005 gives positive apparent depth 0.200 m on the incident side, hence signed d_i=-0.200 m. This uses the plane ray/apparent-depth construction, not serialized curved-conjugate replay; tolerance covers exact synthetic decimal arithmetic.",
    record["sources"][0]["url"] + "# Eq. 2.10 / Fig. 2.14, independent normal-view plane construction"))
record["rejection_cases"] = [
    rejection({"n_1": 1, "n_2": 1.5, "C": 10, "d_o": 0.2}, "At the curved-interface first object focus, transmitted rays are parallel and the finite-image denominator vanishes."),
    rejection({"n_1": 1.5, "n_2": 1, "C": 0, "d_o": 0}, "A real object on the interface is excluded by the original finite-conjugate real-object domain; C=0 alone is valid and is not rejected."),
    rejection({"n_1": 1.5, "n_2": 1, "d_o": 0.3}, "Surface curvature is required; do not silently assume a plane when the geometry is unspecified.", "missing-input")
]
record["inverse_notes"] = (
    "Solve d_o=n_1*d_i/[(n_2-n_1)*C*d_i-n_2] given n_1,n_2>=1, finite C and d_i!=0; require displayed denominator!=0, reconstructed d_o>0 and original forward guards. Solve C=(n_1*d_i+n_2*d_o)/[(n_2-n_1)*d_o*d_i] given d_o>0,d_i!=0,n_1,n_2>=1,n_2!=n_1; C=0 is individually admissible, and original finite-image guard must hold. Example (n_1,n_2,C,d_o,d_i)=(1,1.5,10,0.4,0.6) reconstructs d_o=0.4 and C=10; original reciprocal equation gives 2.5+2.5=5. Plane example (1.5,1,0,0.3,-0.2) reconstructs C=0 and d_o=0.3; forward gives -0.2. If n_1=n_2 and d_i=-d_o, every finite C (including plane C=0) is compatible and curvature is underdetermined; other conjugates inconsistent. A zero image distance is unavailable for a finite nonzero real object. Recovering a finite spherical R=1/C additionally requires C!=0; plane C=0 means R infinite, not R=0. All non-singular mentioned inverses have one root; refractive-index inversions not separately assessed."
)
record["integration"]["gaps"] = [
    "Add/use signed_optical_surface_curvature and coherent 1/m (same sign convention as b02 thin-lens-maker); use the proposed phase_refractive_index and conjugate-distance meanings. Units m and 1 exist; 1/m remains a research extension.",
    "Revision r2 replaces finite R input with C=1/R and supports C=0. Existing instances need explicit radius-to-curvature mapping; zero radius must never map to zero curvature. Preserve plane near-normal viewing and distinguish axial apparent depth from transverse image height."
]
path = write_batch(8, [record], [
    dict(title="Separate apparent-depth model copy",
         reason="Plane Eq. 2.10 is now explicitly supported as C=0 within spherical-interface-imaging@r2, after mapping positive apparent depth h_i=-d_i. No new model ID is minted for this qualified special case; source h_i must not be confused with transverse image height.", source_urls=[record["sources"][0]["url"]])
], "Scope revision only: spherical-interface-imaging@r2 uses curvature to include the separately sourced plane apparent-depth boundary while preserving both curved signs, index matching and finite-image singularities. Eighteen nonduplicate scientific relationships remain; no extra model coverage is counted for a special case.",
"Updates our b02 spherical-interface-imaging@r1; original record and ZIP preserved. Re-inspected official OpenStax University Physics 3 section 2.3 Eqs. 2.10/2.11 and normal-view condition on 2026-11-03. New plane case checked by an independent ray/apparent-depth construction and inverse substitution; original curved reference expected values/tolerances retained with input C=1/R. This source-backed parameterization avoids excluding planes merely because finite radius cannot serialize infinity. b06 Doppler r2 and b07 period-overlap r2 remain preferred over their r1 histories. Initial numerical validation results appended after execution; source/scientific/rights review pending.")
print(path)
