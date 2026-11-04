"""Validate, pack and log a curator-owned batch without touching toolkit source."""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def run(*args):
    result = subprocess.run([sys.executable, "-m", "connected_models.curation", *args], cwd=ROOT,
                            text=True, capture_output=True, encoding="utf-8")
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)
    return json.loads(result.stdout)

def main():
    batch_id = sys.argv[1]
    folder = ROOT / "returns" / batch_id
    bundle = folder / "bundle.json"
    archive = ROOT / "returns" / (batch_id + "-return.zip")
    if archive.exists():
        raise SystemExit("Archive already exists; preserve it and use a new batch/revision for corrections.")
    first = run("validate", str(bundle))
    data = json.loads(bundle.read_text(encoding="utf-8"))
    counts = {"models":len(data["models"]),
              "numerical":sum(len(m["references"]) for m in data["models"]),
              "rejection":sum(len(m["rejection_cases"]) for m in data["models"])}
    data["handoff"]["review_notes"] = data["handoff"]["review_notes"].replace(
        "JSON/ZIP validation will be recorded after execution in the checkpoint log; handoff must be updated with actual results before packing.",
        f"JSON validation executed successfully using installed kit {data['kit_version']}: {counts['models']} records, {counts['numerical']} reference and {counts['rejection']} rejection cases. Final JSON revalidation and packed ZIP validation are recorded in the external checkpoint log.")
    bundle.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    final = run("validate", str(bundle))
    packed = run("pack", str(bundle), str(archive))
    zipped = run("validate", str(archive))
    timestamp = now()
    log = dict(batch_id=batch_id, checkpoint_utc=timestamp, counts=counts,
               commands=[f"uv --cache-dir .uv-cache run --no-env-file --offline -m connected_models.curation validate returns/{batch_id}/bundle.json",
                         f"uv --cache-dir .uv-cache run --no-env-file --offline -m connected_models.curation pack returns/{batch_id}/bundle.json returns/{batch_id}-return.zip",
                         f"uv --cache-dir .uv-cache run --no-env-file --offline -m connected_models.curation validate returns/{batch_id}-return.zip"],
               execution="The checkpoint helper runs the same module commands through the current uv-selected Python interpreter with no environment-file loading; commands above are exact standalone equivalents.",
               initial_json_validation=first, final_json_validation=final, packing=packed, zip_validation=zipped,
               scientific_review="Pending; validation does not certify source fidelity, dimensions, population applicability or rights.")
    (folder / "checkpoint.json").write_text(json.dumps(log, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    session_path = ROOT / "returns/SESSION.json"
    session = json.loads(session_path.read_text(encoding="utf-8"))
    session["last_checkpoint_utc"] = timestamp
    elapsed = (datetime.fromisoformat(timestamp.replace("Z", "+00:00")) - datetime.fromisoformat(session["started_utc"].replace("Z", "+00:00"))).total_seconds()/60
    session["cumulative_useful_work_minutes"] = round(elapsed, 3)
    session["measurement"] = "Measured UTC active-session wall time including research/tool latency; no intentional idle waits. This is not a CPU-time measurement. No interruption observed so far."
    session["completed_batches"].append(dict(batch_id=batch_id, bundle=str(bundle.relative_to(ROOT)).replace("\\", "/"), zip=str(archive.relative_to(ROOT)).replace("\\", "/"), counts=counts, validated_utc=timestamp))
    for model in data["models"]:
        session["model_revisions"].append(model["id"]+"@"+model["revision"])
        for var in model["variables"]:
            entry = {k:var[k] for k in ("quantity_id", "definition", "unit", "dimensions")}
            if entry not in session["quantity_inventory"]:
                session["quantity_inventory"].append(entry)
    session["attempted_deferred"].extend(data["deferred"])
    session_path.write_text(json.dumps(session, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(batch_id=batch_id, archive=str(archive), counts=counts, elapsed_active_session_minutes=round(elapsed,3), status=zipped["status"]), indent=2))

if __name__ == "__main__":
    main()
