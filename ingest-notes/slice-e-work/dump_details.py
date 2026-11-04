"""Dump condensed review sheets for slice E bundles (read-only)."""

import json
from pathlib import Path

ROOT = Path("from-offline-curation-workers")

out = []
for n in range(1, 51):
    batch = f"financial-analysis-cfa-l1-b3-b{n:02d}"
    bundle = json.loads((ROOT / batch / "bundle.json").read_text(encoding="utf-8"))
    out.append("=" * 100)
    out.append(f"BATCH {batch} curator={bundle['curator']} kit={bundle['kit_version']} "
               f"deferred={json.dumps(bundle.get('deferred', []))}")
    out.append(f"  handoff.summary: {bundle.get('handoff', {}).get('summary', '')}")
    out.append(f"  handoff.review_notes: {bundle.get('handoff', {}).get('review_notes', '')}")
    try:
        vlog = json.loads((ROOT / batch / "validation-log.json").read_text(encoding="utf-8"))
        cmds = "; ".join(f"{c.get('command', '?')[:70]}->exit{c.get('exit_code')}" for c in vlog)
        out.append(f"  validation-log: {cmds}")
    except OSError:
        out.append("  validation-log: MISSING")
    for m in bundle["models"]:
        r = m["relationship"]
        out.append("-" * 100)
        out.append(f"{m['id']}@{m['revision']} :: {m['title']}")
        out.append(f"  kind={m['kind']} expr={r['output_symbol']} = {r['expression']}")
        out.append(f"  original: {r['original_equation']}")
        out.append(f"  source_id={r['source_id']} locator={r['locator']}")
        out.append(f"  translation: {r.get('translation_notes', '')}")
        for v in m["variables"]:
            out.append(f"  var {v['symbol']:<12} role={v['role']:<7} qty={v['quantity_id']:<55} "
                       f"unit={v['unit']:<8} dims={v.get('dimensions', ''):<13} domain={v.get('domain', '')}")
            out.append(f"      def: {v.get('definition', '')}")
        out.append(f"  guards: {m['guards']}")
        out.append(f"  assumptions: {m['assumptions']}")
        out.append(f"  limitations: {m['limitations']}")
        out.append(f"  unresolved: {m.get('unresolved', [])}")
        for s in m["sources"]:
            out.append(f"  src [{s['kind']}] {s['id']}: {s.get('title', '')}")
            out.append(f"      url={s.get('url')} accessed={s.get('accessed')}")
            out.append(f"      locator={s.get('locator')}")
            out.append(f"      evidence={s.get('evidence', '')}")
            out.append(f"      license={s.get('license', '')}")
        for ref in m["references"]:
            out.append(f"  ref {ref['id']}: {json.dumps(ref['inputs'])} -> {ref['expected']} "
                       f"(tol {ref.get('tolerance')})")
            out.append(f"      method={ref.get('method', '')}")
            out.append(f"      provenance={ref.get('provenance', '')}")
        for rej in m["rejection_cases"]:
            out.append(f"  rej [{rej['kind']}]: {json.dumps(rej['inputs'])} :: {rej.get('reason', '')}")
        out.append(f"  inverse_notes: {m.get('inverse_notes', '')}")
        out.append(f"  integration: {json.dumps(m.get('integration', {}))}")

Path("ingest-notes/slice-e-work/details.txt").write_text("\n".join(out), encoding="utf-8")
print(f"batches=50 records={sum(1 for l in out if l.startswith('financial-analysis--'))} "
      f"lines={len(out)}")
