"""Build the self-contained CFA external-curator pack.

Produces data/curation/cfa/external-pack/: root AGENTS.md, assignment,
source brief, manifest template, an empty sources/ drop folder, and the
extracted kit (validator, schema, vocabulary, inventory) with returns/.
The owner copies that folder to the external worker location, drops the
purchased PDFs into sources/, and dispatches one sentence per PDF.

Run from the repo root:
    uv run --no-env-file --offline data/curation/cfa/build_external_pack.py [--force]
"""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from connected_models.curation import build_kit, encoded, inventory_returns

ROOT = Path(__file__).resolve().parent.parent.parent.parent

CFA = ROOT / "data" / "curation" / "cfa"
PACK = CFA / "external-pack"

SOURCES_README = """# sources/

The owner drops the purchased CFA PDFs here after copying this pack to the
worker location. Curators: read only the PDF named in your dispatch; never
rename, copy, or redistribute these files. Manifest the PDF (see AGENTS.md
Step 0) before the first batch.
"""

RETURNS_README = """# returns/

Curators: packed `*-return.zip` files go here (one per batch, never
overwritten), created with the kit `pack` command. Hand every ZIP back to
the owner with the consolidated session report.
"""


def build_pack(force: bool = False) -> dict[str, object]:
    """Assemble the external pack; refuse to overwrite without --force."""
    if PACK.exists():
        if not force:
            raise SystemExit(f"Refuse to overwrite existing {PACK}; rerun with --force.")
        shutil.rmtree(PACK)
    PACK.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as scratch:
        scratch_path = Path(scratch)
        inventory_path = scratch_path / "fleet-inventory.json"
        inventory_path.write_bytes(encoded(inventory_returns(ROOT / "from-offline-curation-workers")))
        kit_zip = scratch_path / "kit.zip"
        kit_info = build_kit(kit_zip, domain="financial-analysis", inventory=inventory_path)
        kit_dir = PACK / "kit"
        kit_dir.mkdir()
        with zipfile.ZipFile(kit_zip) as archive:
            archive.extractall(kit_dir)
    shutil.copy(CFA / "pack-AGENTS.md", PACK / "AGENTS.md")
    assignments = json.loads((ROOT / "data" / "curation" / "assignments.json").read_text(encoding="utf-8"))
    assignment = next(item for item in assignments if item["domain"] == "financial-analysis")
    (PACK / "assignment.json").write_text(json.dumps(assignment, indent=2) + "\n", encoding="utf-8")
    shutil.copy(CFA / "cfa-source-brief-direct-pdf.md", PACK / "cfa-source-brief.md")
    shutil.copy(CFA / "source-manifest.pack-template.json", PACK / "source-manifest.template.json")
    sources = PACK / "sources"
    sources.mkdir()
    (sources / "README.md").write_text(SOURCES_README, encoding="utf-8")
    returns = kit_dir / "returns"
    returns.mkdir()
    (returns / "README.md").write_text(RETURNS_README, encoding="utf-8")
    files = sorted(path.relative_to(PACK).as_posix() for path in PACK.rglob("*") if path.is_file())
    return {"pack": str(PACK), "kit_version": kit_info["kit_version"], "files": len(files), "listing": files}


def main() -> None:
    """Parse flags and build the pack."""
    parser = argparse.ArgumentParser(description="Build the CFA external-curator pack.")
    parser.add_argument("--force", action="store_true", help="Rebuild over an existing pack.")
    args = parser.parse_args()
    result = build_pack(force=args.force)
    print(f"pack: {result['pack']}")
    print(f"kit: {result['kit_version']} ({result['files']} files)")


if __name__ == "__main__":
    main()
