"""Close this authorized session only after its measured minimum work duration."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from curation_support import RETURN_ROOT, checkpoint


def read_json(path: Path) -> dict[str, Any]:
    """Read one public JSON artifact, accepting PowerShell's optional UTF-8 BOM."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    """Check completed checkpoint evidence and save the consolidated handoff."""
    session = read_json(RETURN_ROOT / "SESSION.json")
    now = datetime.now(UTC)
    elapsed = (now - datetime.fromisoformat(session["started_utc"])).total_seconds() / 60
    if elapsed < session["minimum_work_minutes"]:
        raise ValueError(f"Session remains active: {elapsed:.4f} measured minutes; continue useful assigned work.")
    numerical = read_json(RETURN_ROOT / "NUMERICAL-REVIEW.json")
    source_review = read_json(RETURN_ROOT / "SOURCE-REVIEW.json")
    quantity_review = read_json(RETURN_ROOT / "QUANTITY-REVIEW.json")
    completed = session["completed_batches"]
    if len(numerical["archives"]) != len(completed):
        raise ValueError("Archive audit does not cover all completed batches.")
    preferred: dict[str, tuple[dict[str, Any], str]] = {}
    archive_rows = []
    all_references = 0
    all_rejections = 0
    total_records = 0
    source_urls: set[str] = set()
    for entry in completed:
        bundle_path = RETURN_ROOT.parent / entry["bundle"]
        batch = read_json(bundle_path)
        json_report = read_json(bundle_path.parent / "validation-json.json")
        zip_report = read_json(bundle_path.parent / "validation-zip.json")
        if any(report["status"] != "valid-data-awaiting-review" or report["batch_id"] != batch["batch_id"]
               for report in (json_report, zip_report)):
            raise ValueError(f"Unsuccessful validation or mismatched report: {batch['batch_id']}")
        references = sum(item["arithmetic_checks"] for item in zip_report["checks"])
        rejections = sum(item["rejection_checks"] for item in zip_report["checks"])
        if references != sum(len(item["references"]) for item in batch["models"]):
            raise ValueError(f"Reference-count mismatch: {batch['batch_id']}")
        if rejections != sum(len(item["rejection_cases"]) for item in batch["models"]):
            raise ValueError(f"Rejection-count mismatch: {batch['batch_id']}")
        all_references += references
        all_rejections += rejections
        total_records += len(batch["models"])
        filename = Path(entry["zip"]).name
        archive_rows.append(f"| [{filename}]({filename}) | {len(batch['models'])} | {references} | {rejections} | Passed / passed |")
        for record in batch["models"]:
            preferred[record["id"]] = (record, batch["batch_id"])
            source_urls.update(source["url"] for source in record["sources"])
    new = [(record, batch) for record, batch in preferred.values() if not record["integration"]["duplicate_of"]]
    rows = [f"| {record['title']} | `{record['relationship']['output_symbol']} = {record['relationship']['expression']}` | {batch[-3:]}, {record['revision']} |"
            for record, batch in new]
    summaries = session["coverage_summary"]
    if (summaries["all_revision_reference_checks"], summaries["all_revision_rejection_checks"]) != (all_references, all_rejections):
        raise ValueError("Consolidated coverage totals are stale.")
    end_text = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    lines = [
        "# Waves and optics curation session", "",
        f"Curator: codex. Started {session['started_utc']}; completed {end_text}. Measured active-session wall time: {elapsed:.2f} minutes, exceeding the assigned {session['minimum_work_minutes']}-minute minimum. No sleeps, background workers or prior-session time counted. Tool latency and active research/authoring/review are included; this is wall-clock measurement, not a CPU-time estimate.", "",
        f"Returned {len(completed)} validated data ZIPs containing {total_records} serialized revision records. Preferred coverage is {len(new)} nonduplicate relationships, with one additional local ID flagged as an existing-catalog overlap. Three r2 records preserve correction history; original files and archives remain intact. Toolkit version: 2026-10-31.6; schema: cm-curation-batch/1.", "",
        "## Completed ZIPs", "",
        "Every ZIP contains exactly bundle.json and manifest.json. JSON and packed-ZIP validation reports are saved in its matching batch folder.", "",
        "| Data ZIP | Records | Numerical checks | Rejection checks | JSON / ZIP |",
        "| --- | ---: | ---: | ---: | --- |", *archive_rows, "",
        "## Preferred relationship coverage", "",
        "Expressions use coherent base units; variable conditions, sign conventions, source locators, numerical evidence and inverse exclusions are in each bundle. The table is an index, not an alternative interface specification.", "",
        "| Relationship | Forward expression | Preferred batch/revision |", "| --- | --- | --- |", *rows, "",
        "## Revision and overlap instructions", "",
        "- Prefer b06 Doppler r2 to b01 r1. It removes an unsupported observer upper-speed cap and explicitly distinguishes the wave-comoving zero-crossing-rate limit from the forbidden sonic-source denominator singularity.",
        "- Prefer b08 interface-imaging r2 to b02 r1. It uses signed curvature C=1/R and includes the separately sourced near-normal plane-interface apparent-depth limit at C=0. A zero radius is not a plane, and axial apparent depth is not transverse image height.",
        "- b07 period-frequency r2 flags computer-science--clock-cycle-time@r1 as an equivalent relationship. Do not import either local period revision as new scientific coverage. No existing curator's record was changed.",
        "- b06's historical count of nineteen distinct relationships predates the b07 overlap finding. This report and SESSION.json give the corrected eighteen nonduplicate count. Earlier archived statements remain preserved as history.", "",
        "## Verification and limits", "",
        f"All serialized revisions passed {all_references} numerical reference checks and {all_rejections} domain/missing-input checks. Preferred nonduplicate revisions account for {summaries['preferred_nonduplicate_reference_checks']} numerical and {summaries['preferred_nonduplicate_rejection_checks']} rejection checks. Published rounded expected values remain as reported, with documented unit conversions and tolerances.", "",
        source_review["numerical_audit"] + " See [NUMERICAL-REVIEW.json](NUMERICAL-REVIEW.json).", "",
        f"The [quantity review](QUANTITY-REVIEW.json) retains {len(quantity_review['quantities'])} proposed quantity interfaces and their context/domain variants. It separates phase speed from pulse timing speed, optical power from watts, angular from transverse magnification, mirror from transmitted-surface sign conventions, and effective from back focal length. The session quantity index uses preferred revisions rather than first-seen historical definitions.", "",
        f"Sources include {len(source_urls)} distinct directly inspected source URLs across completed records. Full bibliographic/access/terms evidence is in the bundles. Completed models rely on official HTML; no completed equation depends on ambiguous PDF extraction. [SOURCE-REVIEW.json](SOURCE-REVIEW.json) records source prose/sign mistakes avoided and deferred PDF limitations.", "",
        "All preferred candidates remain requires-extension with runtime_model null: proposed wave/optics meanings and coherent inverse-length notation need integration. This work did not change a runtime registry, publish models, instantiate a composition or establish scientific approval. Duplicate screening was limited to the supplied dated 218-record inventory, runtime snapshot and this curator's returns; no global uniqueness claim is made.", "",
        source_review["rights"], "",
        "## Artifact navigation and replay", "",
        "SESSION.json contains the batch inventory, preferred revisions, measured start/end/checkpoint times, quantity definitions, attempted/deferred work and exact next action. SOURCE-REVIEW.json and QUANTITY-REVIEW.json preserve review details outside the two-member data ZIPs. Historical author_batch scripts generate local research JSON and should not be rerun over completed checkpoint folders. Use fresh folders and batch IDs for future research or corrections.", "",
        "From the kit root, a reviewer can replay a saved archive's toolkit checks without regenerating the research:", "",
        "```powershell",
        "uv --cache-dir .uv-cache run --no-env-file -m connected_models.curation validate returns/waves-and-optics-codex-b08-return.zip",
        "```", "",
        "The same command accepts any of the eight archives. Research helpers numerical_review.py and quantity_review.py inspect this curator's saved records; their conclusions retain the review limits described above. No source PDFs, screenshots, executables, toolkit or credentials are included in the data archives.", "",
        "## Attempted and deferred coverage", "",
        f"SESSION.json retains {len(session['attempted_or_deferred'])} attempted/deferred entries with source URLs and reasons. Coverage includes all assignment seeds, adjacent kinematic definitions, finite-conjugate optics and instrument geometry. Source-backed special cases were kept with their canonical relationships instead of counted as new models.", "",
        "Deferred categories include exact Snell/critical/Malus/Mach-angle and logarithmic sound-level forms excluded by the assignment; physical-optics interference/diffraction/polarization; unordered beat absolute values; virtual-object/Galilean profiles awaiting broader sign evidence; general optical-path integrals/Fermat stationarity; wave-field partial derivatives; and coupled ray-transfer matrices/principal planes. PDF screenshot adapters exposed only text placeholders, so no visual-equation verification is claimed. Isolated source access failures were recorded and alternative candidates pursued.", "",
        "The [unfinished separated-lens follow-up](SEPARATED-LENS-FOLLOWUP.json) saves a newly located author-textbook source and two exact paraxial ray constructions. Reversing the example lens order preserves 0.08 m effective focal length while changing the back focal distance from 0.04 m to 0.06 m. This illustrates why those metre-valued quantities need different references. It is a continuation lead, excluded from completed model counts and the 271-case completed-record audit.", "",
        "## Priorities for a separately authorized continuation", "",
        *[f"- {item}" for item in session["next_queue"]], "",
        "The assigned sustained session is complete. These priorities are a saved backlog, not an ongoing background mandate. Resume from SESSION.json and preferred revisions if a continuation is requested.", ""
    ]
    (RETURN_ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    checkpoint(status="completed-session-awaiting-review", ended_utc=end_text,
               completed_at_measured_minutes=round(elapsed, 4), time_gate_verified=True,
               blockers=[],
               downstream_review=["Runtime vocabulary extension", "Independent scientific/source review", "Source-specific rights and downstream-use review"],
               exact_next_action="Session complete. Owner reviews returns/README.md and preferred records; on an explicitly requested continuation, resume the saved next_queue without resubmitting existing relationships.",
               final_report="returns/README.md")
    print(json.dumps(dict(status="completed-session-awaiting-review", measured_minutes=round(elapsed, 4),
                          zip_count=len(completed), revision_records=total_records,
                          nonduplicate_relationships=len(new), numerical_checks=all_references,
                          rejection_checks=all_rejections, report="returns/README.md"), indent=2))


if __name__ == "__main__":
    main()
