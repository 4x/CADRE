"""Validate and package the bounded correction, then update public handoff."""
import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

folder = Path(__file__).resolve().parent
root = folder.parents[1]
batch_path = folder/'bundle.json'
batch_id = folder.name
archive = root/'returns'/f'{batch_id}-return.zip'
if archive.exists():
    raise SystemExit('Preserving existing archive; do not overwrite completed corrections.')
batch = json.loads(batch_path.read_text(encoding='utf-8'))
batch['handoff']['review_notes'] += ' Completed engine-dimension regression: old expression[0,3,0,0], corrected expression/output[0,3,-1,0]; all6 guards dimension-check and all3 canonical-scale cases pass. Final JSON and packed ZIP validation commands/results are logged beside the bundle. Runtime contract remains unchecked against clinical-2.'
batch_path.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
commands = [
    [sys.executable,'-m','connected_models.curation','validate',str(batch_path)],
    [sys.executable,'-m','connected_models.curation','pack',str(batch_path),str(archive)],
    [sys.executable,'-m','connected_models.curation','validate',str(archive)],
]
logs = []
for command in commands:
    result = subprocess.run(command,cwd=root,text=True,capture_output=True,encoding='utf-8')
    logs.append(dict(command=command,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
    if result.returncode:
        (folder/'validation.json').write_text(json.dumps(logs,indent=2)+'\n',encoding='utf-8')
        raise SystemExit(result.stdout+result.stderr)
with zipfile.ZipFile(archive) as zipped:
    assert sorted(zipped.namelist()) == ['bundle.json','manifest.json']
    assert json.loads(zipped.read('bundle.json')) == batch
stamp = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
report = dict(validated_utc=stamp,batch_id=batch_id,status='valid-data-awaiting-review',
              model='clinical-arithmetic--cockcroft-gault-creatinine-clearance@r3',
              counts=dict(models=1,numerical_cases=3,rejection_cases=5),
              dimension_regression='dimension-check.json; unmodified engine checker; explicit declared dimension map, not installed clinical-2 verification',
              commands=logs,zip_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
              zip_members=['bundle.json','manifest.json'])
(folder/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
session_path = root/'returns/SESSION.json'
session = json.loads(session_path.read_text(encoding='utf-8'))
snapshot = folder/'SESSION-before-b07.json'
if not snapshot.exists():
    snapshot.write_bytes(session_path.read_bytes())
minutes = (datetime.fromisoformat(stamp.replace('Z','+00:00'))-datetime.fromisoformat('2026-11-03T08:50:53+00:00')).total_seconds()/60
activity = dict(session_id='clinical-arithmetic-codex-correction-r3-20261103',status='completed',
                assignment='Correction-only user request: one r3 superseding b02/r1 and b05/r2; 60-minute research minimum does not apply.',
                curator='codex',started_utc='2026-11-03T08:50:53Z',finished_utc=stamp,
                measured_active_wall_minutes=round(minutes,3),measurement='UTC active-session wall time including tool latency; no intentional waits.',
                batch_id=batch_id,bundle=str(batch_path.relative_to(root)).replace('\\','/'),
                zip=str(archive.relative_to(root)).replace('\\','/'),model_id=batch['models'][0]['id'],revision='r3',
                scientific_status='Unreviewed restricted empirical candidate; explicit calibrated-domain limitation replaces blanket sCr>0 applicability claim.',
                integration_status='requires-extension (stale local snapshot; central clinical-2 reported by owner, not locally verified)',
                next_action='Owner/reviewer to re-review r3 and verify clinical-2 divisor meaning/projection. No further research or publication authorized by this correction-only request.')
session.setdefault('correction_sessions',[]).append(activity)
session['latest_activity'] = activity
session['latest_checkpoint_utc'] = stamp
session['exact_next_action'] = activity['next_action']
session.setdefault('model_revisions',[]).append(activity['model_id']+'@r3')
for record in session.get('superseded_revisions',[]):
    if record['model_id'] == activity['model_id']:
        record.update(preferred='r3',reason='User-directed r3 replaces both older revisions; calibrated-domain limitation and dimensional empirical divisor corrected. Pending re-review.')
session.setdefault('superseded_revisions',[]).append(dict(model_id=activity['model_id'],old='r2',preferred='r3',reason='b07 correction; no prior revision admitted.'))
session.setdefault('quantity_inventory',[]).append(dict(quantity_id='cockcroft_gault_divisor',definition=batch['models'][0]['variables'][4]['definition'],unit='s',dimensions='T'))
session_path.write_text(json.dumps(session,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(folder/'SESSION.json').write_text(json.dumps(activity,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inventory = dict(updated_utc=stamp,scope='Correction-only local inventory. Prior artifact files absent; historical IDs retained in SESSION.json.',
                 latest_corrected_model=dict(id=activity['model_id'],revision='r3',supersedes=['b02/r1','b05/r2'],batch=batch_id),
                 quantities=batch['models'][0]['variables'],archive=activity['zip'],sha256=report['zip_sha256'])
(folder/'INVENTORY.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['status','batch_id','model','counts','zip_sha256']},indent=2))
