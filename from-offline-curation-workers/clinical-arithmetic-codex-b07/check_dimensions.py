"""Regression for the reported staging failure, without changing vocabulary."""
import json
import sys
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from connected_models.expressions import dimensions, parse, guard_dimensions, evaluate, check_guard

folder = Path(__file__).resolve().parent
model = json.loads((folder / 'bundle.json').read_text(encoding='utf-8'))['models'][0]
def dim(*axes):
    return tuple(F(x) for x in axes)

unit_dims = {'years':dim(0,0,0,0), '1':dim(0,0,0,0), 'kg':dim(1,0,0,0),
             'kg/m^3':dim(1,-3,0,0), 's':dim(0,0,1,0), 'm^3/s':dim(0,3,-1,0)}
names = {v['symbol']:unit_dims[v['unit']] for v in model['variables'] if v['role']=='input'}
expected_dims = unit_dims['m^3/s']
old = '(1 - 0.15 * z) * (140 - a) * w / (432000000000 * sCr)'
old_dims = dimensions(parse(old), {k:v for k,v in names.items() if k!='K'})
new_dims = dimensions(parse(model['relationship']['expression']), names)
assert old_dims == dim(0,3,0,0) and old_dims != expected_dims
assert new_dims == expected_dims
for text in model['guards']:
    guard_dimensions(parse(text), names)

snapshot = json.loads((folder.parents[1] / 'data/curation/runtime-vocabulary.json').read_text(encoding='utf-8'))
mass_scale = snapshot['units']['kg']['scale']
scales = {'a':1, 'z':1, 'w':mass_scale, 'sCr':mass_scale, 'K':1}
cases = []
for ref in model['references']:
    x = ref['inputs']
    canonical = {k:value*scales[k] for k,value in x.items()}
    assert all(check_guard(parse(g), canonical) for g in model['guards'])
    actual = evaluate(parse(model['relationship']['expression']), canonical)
    # Independent source-unit route using exact rational arithmetic.
    scr_mg_dl = F(str(x['sCr'])) * 100
    ml_min = ((140-F(str(x['a'])))*F(str(x['w']))/(72*scr_mg_dl)) * (1-F(15,100)*x['z'])
    oracle = ml_min/F(60000000)
    assert abs(F(str(ref['expected']))-oracle) <= F(str(ref['tolerance']))
    assert abs(actual-ref['expected']) <= ref['tolerance']
    cases.append(dict(id=ref['id'],canonical_result=actual,source_unit_oracle=str(oracle),status='pass'))

report = dict(checked_utc=datetime.now(timezone.utc).isoformat(), status='pass',
              method='Unmodified engine dimensions/guard_dimensions functions with explicit declared unit-dimension map; no registry mutation or invented installed clinical-2 profile.',
              old_expression_dimensions=[int(v) for v in old_dims],
              corrected_expression_dimensions=[int(v) for v in new_dims],
              expected_output_dimensions=[int(v) for v in expected_dims],
              numerical_basis=snapshot['numerical_basis'], references=cases,
              limits='This isolates the staging defect and canonical numeric scaling. Full clinical-2 port/meaning validation is unavailable locally; scientific applicability and approval are not established.')
(folder/'dimension-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
