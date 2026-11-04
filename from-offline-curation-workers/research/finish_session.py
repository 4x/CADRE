"""Finalize public handoff metadata only, after the measured session gate."""
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[2]
session_path = root / 'returns/SESSION.json'
session = json.loads(session_path.read_text(encoding='utf-8'))
inventory = json.loads((root / 'returns/LOCAL-INVENTORY.json').read_text(encoding='utf-8'))
for archive in inventory['archives']:
    # Transfer integrity against the previously recorded handoff; no scientific retest.
    path = root / 'returns' / (archive['batch_id'] + '-return.zip')
    with zipfile.ZipFile(path) as packed:
        assert sorted(packed.namelist()) == ['bundle.json', 'manifest.json']
        on_disk = root / 'returns' / archive['batch_id'] / 'bundle.json'
        # The packer canonicalizes JSON formatting; compare parsed content.
        assert json.loads(packed.read('bundle.json')) == json.loads(on_disk.read_text(encoding='utf-8'))
now = datetime.now(timezone.utc)
start = datetime.fromisoformat(session['started_utc'].replace('Z', '+00:00'))
minutes = (now - start).total_seconds() / 60
if minutes < session['minimum_work_minutes']:
    raise SystemExit(f'Not complete: measured {minutes:.3f} minutes; useful work must continue.')
stamp = now.isoformat(timespec='seconds').replace('+00:00', 'Z')
session.update(
    status='completed',
    finished_utc=stamp,
    last_checkpoint_utc=stamp,
    cumulative_useful_work_minutes=round(minutes, 3),
    measurement='Measured continuous active-session UTC wall time, including research, record construction, validation and tool latency. No intentional idle waits. Not a CPU-time measurement.',
    source_audit='returns/SOURCE-AUDIT.md',
    exact_next_action='This bounded research session is complete. If the owner requests another session, start from the saved queue at unused batch clinical-arithmetic-codex-b07 with a fresh actual clock; prioritize Cockcroft–Gault calibration evidence and FENa unit ambiguity. Do not continue autonomously or treat candidates as approved.',
)
session['closing_source_findings'] = [
    {'title': 'Boyd / Mosteller late provenance audit',
     'source_urls': ['https://www.va.gov/vdl/documents/Clinical/CPRS-Clinical_Reminders/pxrm_2_22_mm.pdf', 'https://hero.epa.gov/reference/1061257/'],
     'accessed': '2026-11-03',
     'finding': 'VA July2012 printed36/PDF42 directly inspected as text. Boyd is explicitly secondary and LOG base unstated; original book not inspected. See SOURCE-AUDIT.md. Both BSA forms remain deferred by assignment.'}
]
session_path.write_text(json.dumps(session, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
report_path = root / 'returns/REPORT.md'
report = report_path.read_text(encoding='utf-8')
paragraphs = report.split('\n\n')
paragraphs[1] = f"Curator: codex. Toolkit:2026-10-31.6. UTC start:{session['started_utc']}. Completed:{stamp} ({minutes:.3f} measured active-session wall minutes)."
paragraphs[2] = 'Status: completed bounded research session. All candidates remain unreviewed; no scientific approval, clinical recommendation or publication.'
report = '\n\n'.join(paragraphs)
report += '\nClosing provenance findings and direct/indirect access distinctions are in [SOURCE-AUDIT.md](SOURCE-AUDIT.md). Latest-revision selection and exact resume instructions are in [SESSION.json](SESSION.json).\n'
report_path.write_text(report, encoding='utf-8')
print(json.dumps({'status': session['status'], 'finished_utc': stamp, 'measured_minutes': round(minutes, 3), 'archives': len(session['completed_batches'])}))
