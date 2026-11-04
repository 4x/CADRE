"""Preserve the first return and correct the acoustic observer branch as r2."""

import copy
import json

from curation_support import RETURN_ROOT, reference, rejection, source, write_batch

prior_path = RETURN_ROOT / "waves-and-optics-codex-b01" / "bundle.json"
prior = json.loads(prior_path.read_text(encoding="utf-8"))
record = copy.deepcopy(next(item for item in prior["models"] if item["id"].endswith("--collinear-acoustic-doppler")))
record["revision"] = "r2"
record["title"] = "Collinear acoustic Doppler frequency on the forward-crossing branch"
record["summary"] = "Corrects b01 collinear-acoustic-doppler@r1: removes an unnecessarily subsonic observer upper bound and admits the explicitly labeled zero-crossing-rate limit. Source remains subsonic, and the same canonical relationship/ID and medium-frame sign mapping are retained. No new coverage is counted for this revision."
context = "Same constant-frequency acoustic source and ideal passive observer on one propagation line, homogeneous medium at rest in the stated frame, fixed medium composition/phase/temperature/pressure and constant prescribed collinear endpoint velocities. Source is subsonic. Positive u_s is toward observer; positive u_o is toward source, so comoving endpoints have u_o=-u_s. Forward-crossing branch u_o>=-v; u_o=-v is the zero-crossing-rate limit. Source/observer ordering remains unchanged over the modeled interval."
for port in record["variables"]:
    port["context"] = context
    if port["symbol"] == "u_o":
        port["domain"] = "Finite u_o>=-v on the declared forward wave-crossing branch. No subsonic upper bound for approach is imposed; classical kinematics and ideal passive-observer conditions still apply."
    if port["symbol"] == "f_o":
        port["definition"] = "Nonnegative rate of acoustic phase crossings at the observer on the declared branch; zero denotes a wave-comoving static phase pattern, not a zero emitted carrier frequency."
        port["domain"] = "Finite nonnegative. Positive for u_o>-v; zero at u_o=-v as an explicitly admitted limiting identity. Shift f_o-f_s may be positive, negative or zero."
record["guards"] = ["f_s > 0", "v > 0", "u_s > -v", "u_s < v", "u_o >= -v", "v - u_s > 0"]
record["relationship"]["translation_notes"] = (
    "Introduce signed u_s=+v_s for source approach and -v_s for recession, and u_o=+v_o for observer approach and -v_o for recession, all relative to the medium. Source Eq. 17.19 follows from lambda=(v+u_o)*T_o on the approach branch: positive approach has no u_o<v requirement. Source's subsonic-source restriction stays -v<u_s<v with nonzero v-u_s. r1 imposed an unnecessary symmetric subsonic observer profile; r2 uses u_o>=-v to retain nonnegative crossing orientation, with no upper observer speed bound except classical/passive-probe applicability. At u_o=-v the observed phase is static: f_o=0 is an admitted zero-crossing-rate limit, with no finite observed period. Negative crossing orientation u_o<-v would need a separate qualified magnitude/branch treatment, not negative heard frequency. Hz*(m/s)/(m/s)=Hz; no unit scales or physical constants inlined. Relativistic light Doppler is not this law."
)
record["assumptions"] = [
    "Source assumption: constant source frequency, homogeneous acoustic medium at rest, and collinear endpoint velocities in that same medium frame; no source/observer crossing in the chosen interval.",
    "Source restriction: source speed is subsonic (-v<u_s<v), so emitted forward wavefronts remain ordered and v-u_s>0.",
    "Application branch: observer u_o>=-v gives nonnegative forward phase-crossing rate; equality is an explicitly admitted static-phase/zero-arrival-rate limit, not a repeating observed oscillation.",
    "Kinematic idealization: observer is a passive probe of the prescribed acoustic field; self-generated disturbances/wakes are not computed. Observer approaching faster than sound is not rejected solely by an unsupported symmetric speed guard.",
    "Source scope: classical acoustics, common time coordinate, no relativistic electromagnetic Doppler or noncollinear geometry."
]
record["limitations"] = [
    "For u_o=-v, no successive phase arrivals occur; a finite observed period or arrival-spacing inverse is unavailable even though the limiting crossing rate is zero.",
    "For u_o<-v the oriented crossing rate changes sign; nonnegative physical-frequency magnitudes and their inverses need a separately evidenced branch/magnitude treatment. That branch is outside this record, not a claim that the motion is impossible.",
    "Changing line-of-sight orientation, endpoint crossing, source supersonic/shock regimes or an observer's disturbance of the medium require more modeling.",
    "No energy, intensity, loudness, audibility or perceptual-pitch relation is supplied; rounded textbook frequency examples are pedagogical arithmetic, not empirical calibration."
]
record["sources"][0]["locator"] += "; r2 specifically rechecks observer derivation before Eq. 17.19 and the approaching-observer column in Table 17.4"
record["sources"][0]["evidence"] = "The observer approach derivation adds the observer and wave travel distances over an arrival interval and does not impose a subsonic observer upper bound. The signed general law retains the source's subsonic wavefront ordering; the zero numerator has a static-phase limiting interpretation, distinguished from the sonic-source denominator singularity."
record["sources"].append(source(1, "16-2-mathematics-of-waves", "16.2 Mathematics of Waves",
                               "Phase expression kx-omega*t, Eq. 16.5, and constant-phase tracking explanation",
                               "Following a phase point at the propagation velocity keeps its phase constant. An observer moving with the passing wave therefore has zero temporal phase-crossing rate; this is a kinematic limiting inference, not a claim of a finite zero-frequency period."))
record["references"].extend([
    reference("independent-fast-approaching-observer", {"f_s": 100, "v": 300, "u_s": 60, "u_o": 450}, 312.5, 1e-10,
              "Independent synthetic wavefront events with source at x=0 moving +60 m/s, observer initially x=30 m moving -450 m/s, waves +300 m/s. First front meets at t=0.040 s. Second is emitted t=0.010 at x=0.6 and meets when 0.6+300*(t-0.01)=30-450*t, giving t=0.0432 s. Arrival spacing 0.0032 s means 312.5 Hz. The endpoints have not crossed before these events. This catches r1's overrestrictive u_o<v guard; decimal floating-point tolerance only.", record["sources"][0]["url"] + "# observer approach distance-sum derivation; independent event construction"),
    reference("wave-comoving-zero-crossing-rate", {"f_s": 100, "v": 300, "u_s": 60, "u_o": -300}, 0, 1e-10,
              "Kinematic limiting identity: observer moves away at wave speed, so it stays at one phase of an already established train and sees no repeated phase crossings. It is not a case of two finite echo arrivals separated by zero time; observed period is unavailable. Expected zero follows constant-phase motion, independent of frequency-expression substitution. Numeric tolerance only.", record["sources"][1]["url"] + "# constant-phase tracking, combined with section 17.7 observer branch")
])
record["rejection_cases"].append(rejection({"f_s": 100, "v": 300, "u_s": 60, "u_o": -301}, "Observer overtakes forward wavefronts in reverse order; the stated nonnegative forward-crossing branch is violated. Motion is physically possible but needs a separately qualified magnitude/branch model."))
record["inverse_notes"] = (
    "Retain f_s>0,v>0,-v<u_s<v,u_o>=-v and the same classical medium-frame geometry. For f_s given f_o,v,u_s,u_o: f_s=f_o*(v-u_s)/(v+u_o), requiring u_o>-v and f_o>0; unique positive root. At u_o=-v,f_o=0 any positive f_s is compatible (underdetermined), while f_o>0 is inconsistent. For u_s given f_o,f_s,v,u_o: u_s=v-f_s*(v+u_o)/f_o, requiring f_o>0 and reconstructed -v<u_s<v; at f_o=0,u_o=-v every admissible u_s gives zero, so u_s is underdetermined. For u_o given f_o,f_s,v,u_s: u_o=f_o*(v-u_s)/f_s-v, requiring f_o>=0,f_s>0 and the reconstructed original guards; f_o=0 uniquely returns u_o=-v, no nonzero-f_o exclusion in this direction. For v given frequencies/velocities: v=(f_o*u_s+f_s*u_o)/(f_o-f_s), requiring f_o!=f_s, v>0,-v<u_s<v,u_o>=-v. If f_o=f_s then u_o=-u_s leaves all admissible v undetermined; otherwise inconsistent. Checks: f_o=312.5,f_s=100,v=300,u_o=450 -> u_s=60 and forward 312.5; inverse v=(312.5*60+100*450)/(312.5-100)=300. At f_o=0,f_s=100,u_s=60,u_o=-300 -> v=300; u_o inverse also gives -300. At zero endpoint motion, f_o=f_s=150, so shift is exactly zero with arbitrary admissible supplied v. Non-singular mentioned directions have one root; observed-frequency data alone do not establish causal identification."
)
record["integration"]["gaps"].append("Revision r2 supersedes the r1 observer-domain profile under the same scientific ID; integration must preserve the static-phase zero output and direction-specific zero/ambiguous inverse behavior, without treating it as an oscillating wave period.")

path = write_batch(6, [record], [
    dict(title="Reverse-order observer crossing branch",
         reason="For u_o<-v the signed source expression changes crossing orientation. A physical frequency magnitude would require explicit branch evidence and revised inverse roots; do not return a negative heard frequency or manufacture an abs workaround. r2 intentionally covers the nonnegative forward-crossing branch plus its zero-rate limit.", source_urls=[record["sources"][0]["url"]])
], "Self-review correction only: collinear-acoustic-doppler@r2 preserves the relationship and model ID, broadens the previously overrestricted observer domain, and correctly separates zero-crossing-rate and sonic-source singular limits. Nineteen distinct scientific relationships remain; this is not a twentieth new model.",
"Corrected prior record: waves-and-optics-codex-b01/bundle.json, waves-and-optics--collinear-acoustic-doppler@r1. Finding: the symmetric observer subsonic cap was an unnecessary curator profile that excluded source-supported approaching-observer crossing kinematics. Re-inspected official section 17.7 observer derivation and section 16.2 constant-phase tracking on 2026-11-03. Added independent two-wavefront 450 m/s observer case and a labeled wave-comoving zero-rate limit; rewrote all inverse denominator/zero cases. Original r1 and its archive remain unchanged; r2 should be the preferred candidate for review. Initial numerical validation results appended after execution. No central approval or publication inferred.")
print(path)
