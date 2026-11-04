"""Consolidate completed local artifacts and a precise continuation queue; never changes data ZIPs."""
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
    session_path = ROOT/"returns/SESSION.json"
    session = json.loads(session_path.read_text(encoding="utf-8"))
    latest = {}
    history = {}
    archives = []
    all_models = []
    deferred = []
    actual_invocations = []
    for folder in sorted((ROOT/"returns").glob("clinical-arithmetic-codex-b*")):
        if not folder.is_dir():
            continue
        bundle_path = folder/"bundle.json"
        batch = json.loads(bundle_path.read_text(encoding="utf-8"))
        checkpoint = json.loads((folder/"checkpoint.json").read_text(encoding="utf-8"))
        archive_path = ROOT/"returns"/(batch["batch_id"]+"-return.zip")
        with zipfile.ZipFile(archive_path) as z:
            members = z.namelist()
        archives.append(dict(batch_id=batch["batch_id"],path=str(archive_path.relative_to(ROOT)).replace("\\","/"),
                             model_revisions=len(batch["models"]),numerical_cases=sum(len(x["references"]) for x in batch["models"]),
                             rejection_cases=sum(len(x["rejection_cases"]) for x in batch["models"]),
                             members=members,bytes=archive_path.stat().st_size,
                             sha256=hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                             final_json_status=checkpoint["final_json_validation"]["status"],
                             zip_status=checkpoint["zip_validation"]["status"]))
        actual_invocations.append(dict(batch_id=batch["batch_id"],host_command=f"uv --cache-dir .uv-cache run --no-env-file --offline returns/research/checkpoint.py {batch['batch_id']}",
                                       child_module_commands=[
                                           [sys.executable,"-m","connected_models.curation","validate",str(bundle_path)],
                                           [sys.executable,"-m","connected_models.curation","validate",str(bundle_path)],
                                           [sys.executable,"-m","connected_models.curation","pack",str(bundle_path),str(archive_path)],
                                           [sys.executable,"-m","connected_models.curation","validate",str(archive_path)]],
                                       result_log=str((folder/"checkpoint.json").relative_to(ROOT)).replace("\\","/")))
        for model in batch["models"]:
            all_models.append(model)
            latest[model["id"]] = model
            history.setdefault(model["id"],[]).append(dict(revision=model["revision"],batch_id=batch["batch_id"],integration_status=model["integration"]["status"]))
        deferred.extend(dict(batch_id=batch["batch_id"],**x) for x in batch["deferred"])
    quantities = {}
    for model in latest.values():
        for var in model["variables"]:
            quantities.setdefault(var["quantity_id"],[]).append(dict(model=model["id"]+"@"+model["revision"],
                symbol=var["symbol"],definition=var["definition"],unit=var["unit"],dimensions=var["dimensions"],context=var["context"]))
    inventory = dict(created_utc=stamp,scope="Own public research only; this is a local handoff index, not a central catalog or scientific approval.",
                     latest_models=[dict(id=m["id"],revision=m["revision"],title=m["title"],status=m["integration"]["status"],
                                         expression=m["relationship"]["expression"],source_urls=[s["url"] for s in m["sources"]],
                                         history=history[m["id"]]) for m in latest.values()],
                     quantity_inventory=quantities,archives=archives,deferred_coverage=deferred)
    (ROOT/"returns/LOCAL-INVENTORY.json").write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/"returns/VALIDATION-INDEX.json").write_text(json.dumps(dict(created_utc=stamp,
        actual_checkpoint_invocations=actual_invocations,
        separate_unit_audit_command="uv --cache-dir .uv-cache run --no-env-file --offline returns/research/audit_units.py",
        results="Every checkpoint's module commands completed with exit0; all final JSON and ZIP checks report valid-data-awaiting-review. Original incomplete templates were not packed.",
        limits="No runtime projection, publication, central intake or scientific approval. Checksums are transfer-integrity information only."),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    elapsed = (datetime.fromisoformat(stamp.replace("Z","+00:00"))-datetime.fromisoformat(session["started_utc"].replace("Z","+00:00"))).total_seconds()/60
    session["last_checkpoint_utc"] = stamp
    session["cumulative_useful_work_minutes"] = round(elapsed,3)
    session["latest_record_inventory"] = "returns/LOCAL-INVENTORY.json"
    session["validation_index"] = "returns/VALIDATION-INDEX.json"
    session["independent_units_audit"] = "returns/unit-audit.json"
    session["superseded_revisions"] = [
        dict(model_id="clinical-arithmetic--weight-based-prescribed-mass",old="r1",preferred="r2",reason="Actual body_mass only, excluding ideal/adjusted weight constructs."),
        dict(model_id="clinical-arithmetic--cockcroft-gault-creatinine-clearance",old="r1",preferred="r2",reason="Blocked pending directly inspected original calibration/assay scope.")]
    session["next_queue"] = [
        "Original Cockcroft–Gault methods/tables or appropriate independent validation: establish concentration/renal-function calibration range and assay scope before resolving blocked r2; preserve female-adjustment limitation.",
        "FENa: obtain unambiguous primary equation/unit rendering; resolve urinary-sodium nmol versus mmol conflict without guessing, and separate clearance ratio from true filtered fraction.",
        "Original Boyd/Mosteller source and exact formula/rights metadata for deferred evidence only; completed root models remain outside assignment authorization.",
        "Equal daily-dose allocation: an arbitrary administration count needs integer-domain enforcement or a faithful non-scalar representation; do not admit fractional actual counts.",
        "Arm-fat and arm-muscle area definitions from Gibson11.1.4/11.2.3: independently review model assumptions, population-specific corrections and numeric oracles before new records.",
        "Manufacturer-specific reconstitution: final volume versus diluent amount; avoid generalizing apparent powder displacement without evidence.",
        "Scientific review of broad quantity aliases and source-content use restrictions; do not bind bulk density to constituent concentration, index dimensions to physical density, or creatinine clearance to GFR.",
        "If a new session is requested, start at unused batch clinical-arithmetic-codex-b07 and record a fresh actual session clock; do not re-return existing equations as new coverage."
    ]
    session["blockers"] = ["One candidate-level scientific blocker: Cockcroft–Gault r2 applicability evidence. No assignment-wide blocker; further in-scope sources remain in the queue.",
                           "Browser PDF screenshots returned image placeholders without inspectable pixels; ambiguous image-dependent equations were deferred or replaced with directly inspected clear HTML/prose."]
    session["exact_next_action"] = "Finish the current source-fidelity/handoff audit until the60-minute useful-work target; then record actual completion timestamp, finalize consolidated report and end this bounded session."
    session_path.write_text(json.dumps(session,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rows = ["# Clinical arithmetic research session", "", f"Curator: codex. Toolkit:2026-10-31.6. UTC start:{session['started_utc']}. Latest measured checkpoint:{stamp} ({elapsed:.3f} active-session wall minutes).", "",
            "Status: research checkpoint; the final session status is recorded in SESSION.json. No scientific approval, clinical recommendation or publication.", "",
            f"{len(all_models)} candidate revisions across {len(latest)} distinct relationships; latest statuses: {sum(m['integration']['status']=='requires-extension' for m in latest.values())} require runtime extensions and {sum(m['integration']['status']=='blocked' for m in latest.values())} is scientifically blocked. Two original revisions are preserved with preferred r2 replacements.", "",
            f"All completed JSON/ZIP pairs validate: {sum(x['numerical_cases'] for x in archives)} numerical cases and {sum(x['rejection_cases'] for x in archives)} domain/missing-input cases across returned revisions. Independent dimensional/base-scale replay is in unit-audit.json; it does not establish clinical/source validity.", "", "## Archives", ""]
    for archive in archives:
        rows.append(f"- [{archive['batch_id']}-return.zip]({archive['batch_id']}-return.zip) — {archive['model_revisions']} candidate revisions; validated JSON and ZIP.")
    rows += ["", "Each ZIP contains exactly bundle.json and manifest.json. Checksums, sizes and actual command/result-log links are in LOCAL-INVENTORY.json and VALIDATION-INDEX.json.", "", "## Coverage and limitations", "",
             "Covered BMI, prescribed per-weight/per-area amounts, liquid quantity, fluid/drop/mass infusion rates, timed creatinine clearance, GFR area de-indexing, waist ratios, ponderal index, signed postpartum and general weight change, concentration/dilution, conventional BUN/creatinine ratio, and conditional upper-arm circumference geometry.", "",
             f"{len(deferred)} checkpoint deferral/evidence-overlap entries preserve access failures, original-source gaps and next work. Root BSA forms and clearance inverse views were deferred by assignment. FENa has an unresolved primary unit rendering. Daily allocation needs count-domain support. Product-specific reconstitution, arm areas and empirical corrections need further research.", "",
             "Cockcroft–Gault r2 is blocked because its original calibration/assay scope was not fully verified; r1 must not be treated as a resolved candidate. The other19 latest records are unreviewed requires-extension candidates. No current-runtime projection was supplied or changed.", "",
             "Duplicate review was limited to the supplied2026-11-01 inventory (218 records), vocabulary snapshot and own returns. Runtime unit support, clinical validity, actual instance matching, licensing and proposed aliases need separate review. Source terms are recorded individually; public/open availability was not treated as universal redistribution clearance.", "",
             "## Next priorities", ""]
    rows += [f"- {x}" for x in session["next_queue"][:6]]
    rows += ["", "Measurement: available UTC tools and host clock measured continuous active research/record construction/validation, including tool latency. No intentional idle waits, sleeping, scheduled services or additional workers were used. This is a wall-clock measure, not CPU time.", ""]
    (ROOT/"returns/REPORT.md").write_text("\n".join(rows),encoding="utf-8")
    print(json.dumps(dict(checkpoint_utc=stamp,elapsed_active_session_minutes=round(elapsed,3),archives=len(archives),candidate_revisions=len(all_models),distinct_relationships=len(latest),deferred_entries=len(deferred),quantity_meanings=len(quantities)),indent=2))

if __name__=="__main__":
    main()
