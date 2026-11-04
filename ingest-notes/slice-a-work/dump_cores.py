"""Dump compact record cores per volume, ASCII-sanitized. Read-only."""

import glob
import json
import os


def clean(text):
    return "".join(ch if 32 <= ord(ch) < 127 or ch in "\n\t" else "?" for ch in str(text))


def dump_volume(volume, out_path):
    paths = sorted(glob.glob(
        f"from-offline-curation-workers/financial-analysis-cfa-l3-{volume}-*/bundle.json"))
    lines = []
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as fh:
            bundle = json.load(fh)
        lines.append(f"##### BATCH {bundle['batch_id']}")
        for model in bundle["models"]:
            rel = model["relationship"]
            lines.append(f"##### {model['id']} rev={model['revision']} kind={model['kind']}")
            lines.append(f"EXPR: {rel['expression']}")
            lines.append(f"ORIG: {rel['original_equation']}")
            lines.append(f"NOTES: {rel['translation_notes']}")
            for ref in model["references"]:
                lines.append(
                    f"REF {ref['id']}: exp={ref['expected']} tol={ref['tolerance']} "
                    f"method=[{ref['method']}] prov=[{ref['provenance']}]")
            for case in model["rejection_cases"]:
                lines.append(f"REJ {case['kind']}: inputs={json.dumps(case['inputs'])} -- {case['reason']}")
            lines.append(f"GUARDS: {' | '.join(model['guards'])}")
            lines.append("VARS: " + " ; ".join(
                f"{v['symbol']}/{v['role']}/{v['unit']}/{v['dimensions']} def=[{v['definition']}]"
                for v in model["variables"]))
            lines.append(f"ASSUME: {' | '.join(model['assumptions'])}")
            lines.append(f"LIMIT: {' | '.join(model['limitations'])}")
            lines.append(f"INV: {model['inverse_notes']}")
            lines.append(f"UNRES: {' | '.join(model['unresolved'])}")
            lines.append("")
    with open(out_path, "w", encoding="ascii", errors="replace") as fh:
        fh.write(clean("\n".join(lines)))
    print(f"{volume}: {out_path} ({os.path.getsize(out_path)} bytes)")


for volume in ("v1", "v2", "v3", "v4"):
    dump_volume(volume, f"ingest-notes/slice-a-work/core-{volume}.txt")
