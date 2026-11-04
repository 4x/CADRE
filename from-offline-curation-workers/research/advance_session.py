import json
from datetime import datetime, timezone
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "SESSION.json"
session = json.loads(path.read_text(encoding="utf-8"))
stamp = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
session["last_checkpoint_utc"] = stamp
session["cumulative_useful_work_minutes"] = round((datetime.fromisoformat(stamp.replace("Z", "+00:00")) - datetime.fromisoformat(session["started_utc"].replace("Z", "+00:00"))).total_seconds()/60, 3)
session["next_queue"] = [
    "BSA de-indexing of GFR: NIDDK reference-area unit convention, preserve canonical expression without a doubled 1.73 factor",
    "Waist-to-height ratio: NICE/NHS formula, worked example, population restrictions and measurement basis",
    "Waist-to-hip ratio: WHO report, measurement landmarks and pure definition versus risk predictions",
    "Neonatal ponderal index: source definition, unit convention, validated scope and duplicate check against density",
    "Mosteller and Boyd BSA: exact sourced deferrals under assignment, no approximate or executable root forms",
    "Equal daily total allocation: document missing integer-count guard rather than silently accepting fractional administration counts",
    "Reconstitution arithmetic: final volume versus added diluent, powder displacement, distinctness from liquid-dose identity",
    "Clinical dilution conservation: directly inspect nursing source and compare with liquid-dose/density relationships",
    "Weight change fraction/body-size indices: inspect clinical definition and signed versus magnitude scope",
    "Continuous infusion drug-mass arithmetic: reject composed dose-to-pump scenario as a new atomic model; retain distinct source definitions only",
    "Serum anion gap: assess assignment scope and primary electrolyte-convention evidence before a candidate",
    "Audit completed records: source fidelity, unit base invariance, qualified inverse notes, numerical rounding and rights; make fresh revisions if needed"
]
session["exact_next_action"] = "Research first four remaining body-size/renal-normalization definitions; checkpoint b03 after up to four defensible records or 15 measured minutes, preserve all b01/b02 files and continue until the 60-minute useful-work gate."
session["blockers"] = ["No assignment-wide blocker. Original PDF screenshot tools return image placeholders without accessible pixels; use unambiguous extracted text or direct HTML and disclose original visual-inspection gaps."]
session["superseded_revisions"] = [{"model_id":"clinical-arithmetic--weight-based-prescribed-mass","old":"r1","preferred":"r2","reason":"Clarifies body_mass as actual measured mass, excluding ideal/adjusted weight constructs; same expression and checks."}]
path.write_text(json.dumps(session, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"checkpoint_utc":stamp,"useful_active_session_minutes":session["cumulative_useful_work_minutes"],"completed_batches":len(session["completed_batches"]),"queue":len(session["next_queue"])}))
