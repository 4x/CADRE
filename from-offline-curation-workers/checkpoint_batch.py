"""Record this curator's checkpoint metadata after external validator success."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from curation_support import RETURN_ROOT, checkpoint


def main() -> None:
    """Refresh the public session from this curator's own completed bundles."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", type=int)
    args = parser.parse_args()
    session_path = RETURN_ROOT / "SESSION.json"
    session = json.loads(session_path.read_text(encoding="utf-8"))
    batch_id = f"waves-and-optics-codex-b{args.number:02d}"
    batch_path = RETURN_ROOT / batch_id / "bundle.json"
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    archive = RETURN_ROOT / f"{batch_id}-return.zip"
    if not archive.is_file():
        raise FileNotFoundError(f"Checkpoint requires the completed data archive: {archive}")
    entries = [entry for entry in session["completed_batches"] if entry["batch_id"] != batch_id]
    entries.append(dict(batch_id=batch_id, bundle=str(batch_path.relative_to(RETURN_ROOT.parent)),
                        zip=str(archive.relative_to(RETURN_ROOT.parent)),
                        model_count=len(batch["models"]),
                        validation="JSON and packed ZIP valid-data-awaiting-review; see validation logs beside bundle"))
    inventory: list[dict[str, Any]] = []
    quantities: dict[str, dict[str, str]] = {}
    for entry in entries:
        completed = json.loads((RETURN_ROOT.parent / entry["bundle"]).read_text(encoding="utf-8"))
        for record in completed["models"]:
            inventory.append(dict(id=record["id"], revision=record["revision"], batch_id=entry["batch_id"],
                                  expression=record["relationship"]["expression"]))
            for port in record["variables"]:
                quantities.setdefault(port["quantity_id"], dict(quantity_id=port["quantity_id"], unit=port["unit"],
                                                              dimensions=port["dimensions"], definition=port["definition"]))
    deferred = session["attempted_or_deferred"]
    for discovery in batch["deferred"]:
        if not any(item.get("title") == discovery["title"] for item in deferred):
            deferred.append(dict(batch_id=batch_id, **discovery))
    checkpoint(completed_batches=entries, model_inventory=inventory,
               quantity_inventory=list(quantities.values()), attempted_or_deferred=deferred,
               exact_next_action="Continue the next unresolved item in next_queue; preserve all packed batches. Research and validate a fresh batch, at most 12 records; do not stop at this checkpoint.")
    print(f"Checkpoint saved: {batch_id}; {len(inventory)} cumulative records")


if __name__ == "__main__":
    main()
