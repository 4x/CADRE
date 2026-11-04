"""Independent dimensional and base-scale audit of curator data, separate from toolkit validation."""
import ast
import json
from decimal import Decimal, getcontext
from datetime import datetime, timezone
from pathlib import Path

getcontext().prec = 55
ROOT = Path(__file__).resolve().parents[2]
D = Decimal
ZERO = (D(0), D(0), D(0))
M = (D(1), D(0), D(0))
L = (D(0), D(1), D(0))
T = (D(0), D(0), D(1))
kg_scale = D(1)/D(3600000)
# Proposed coherent units are audited mathematically; this does not register them.
UNITS = {
    "1":(ZERO,D(1)), "years":(ZERO,D(1)), "kg":(M,kg_scale),
    "m":(L,D(1)), "s":(T,D(1)),
    "m^2":((D(0),D(2),D(0)),D(1)),
    "m^3":((D(0),D(3),D(0)),D(1)),
    "kg/m^2":((D(1),D(-2),D(0)),kg_scale),
    "kg/m^3":((D(1),D(-3),D(0)),kg_scale),
    "m^3/s":((D(0),D(3),D(-1)),D(1)),
    "m/s":((D(0),D(1),D(-1)),D(1)),
    "kg/s":((D(1),D(0),D(-1)),kg_scale),
    "drops/m^3":((D(0),D(-3),D(0)),D(1)),
    "drops/s":((D(0),D(0),D(-1)),D(1)),
}

def evaluate(node, values, dimensions, constant_dimensions):
    if isinstance(node, ast.Expression):
        return evaluate(node.body, values, dimensions, constant_dimensions)
    if isinstance(node, ast.Name):
        return values[node.id], dimensions[node.id]
    if isinstance(node, ast.Constant) and type(node.value) in (int,float):
        value = D(str(node.value))
        return value, constant_dimensions.get(value,ZERO)
    if isinstance(node, ast.UnaryOp):
        x,dx = evaluate(node.operand,values,dimensions,constant_dimensions)
        if isinstance(node.op,ast.USub):
            return -x,dx
        if isinstance(node.op,ast.UAdd):
            return x,dx
    if isinstance(node, ast.BinOp):
        x,dx = evaluate(node.left,values,dimensions,constant_dimensions)
        y,dy = evaluate(node.right,values,dimensions,constant_dimensions)
        if isinstance(node.op,(ast.Add,ast.Sub)):
            if dx != dy:
                raise ValueError("Incompatible dimensions in sum/difference")
            return (x+y if isinstance(node.op,ast.Add) else x-y),dx
        if isinstance(node.op,ast.Mult):
            return x*y,tuple(a+b for a,b in zip(dx,dy))
        if isinstance(node.op,ast.Div):
            return x/y,tuple(a-b for a,b in zip(dx,dy))
        if isinstance(node.op,ast.Pow):
            if dy != ZERO:
                raise ValueError("Dimensional exponent")
            return x**y,tuple(a*y for a in dx)
    raise ValueError(f"Unexpected AST form in these scalar records: {type(node).__name__}")

def main():
    snapshot = json.loads((ROOT/"data/curation/runtime-vocabulary.json").read_text(encoding="utf-8"))
    if snapshot["numerical_basis"] != "kWh, m, s, USD; mass base = 3600000 kg":
        raise ValueError("Audit's expected numerical basis differs from snapshot")
    results = []
    latest = {}
    for path in sorted((ROOT/"returns").glob("clinical-arithmetic-codex-b*/bundle.json")):
        batch = json.loads(path.read_text(encoding="utf-8"),parse_float=D)
        for model in batch["models"]:
            latest[model["id"]] = model
            variables = {x["symbol"]:x for x in model["variables"]}
            output = variables[model["relationship"]["output_symbol"]]
            inputs = {k:x for k,x in variables.items() if x["role"]=="input"}
            dims = {k:UNITS[x["unit"]][0] for k,x in inputs.items()}
            out_dim,out_scale = UNITS[output["unit"]]
            const_dims = {D(432000000000):T} if model["id"].endswith("--cockcroft-gault-creatinine-clearance") else {}
            expression = ast.parse(model["relationship"]["expression"],mode="eval")
            max_relative_tolerance_fraction = D(0)
            for case in model["references"]:
                values = {k:D(str(x))*UNITS[inputs[k]["unit"]][1] for k,x in case["inputs"].items()}
                canonical, inferred_dim = evaluate(expression,values,dims,const_dims)
                if inferred_dim != out_dim:
                    raise ValueError(model["id"]+": output dimensional mismatch")
                declared_result = canonical/out_scale
                error = abs(declared_result-D(str(case["expected"])))
                tolerance = D(str(case["tolerance"]))
                if error > tolerance:
                    raise ValueError(model["id"]+"/"+case["id"]+": canonical base-scale replay fails")
                max_relative_tolerance_fraction = max(max_relative_tolerance_fraction,error/tolerance)
            results.append(dict(identity=model["id"]+"@"+model["revision"],batch_id=batch["batch_id"],
                                output_unit=output["unit"],inferred_dimensions=[str(x) for x in out_dim],
                                canonical_reference_cases=len(model["references"]),
                                largest_fraction_of_allowed_absolute_tolerance=float(max_relative_tolerance_fraction),
                                status="dimension-and-base-scale-consistent"))
    audit = dict(audited_utc=datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z"),
                 method="Independent Decimal/AST dimensional algebra and canonical-scale evaluation; no toolkit expression evaluator or runtime model is used. Existing snapshot base checked; proposed coherent units remain unregistered.",
                 dimension_axes=["physical mass","length","time"],
                 special_coefficient="Cockcroft–Gault denominator432000000000 has dimension time, per normalized source coefficient; age years is the snapshot dimensionless year-index convention.",
                 quantity_semantics="Dimensional equality is insufficient for binding; this audit does not equate BMI/areal density, ponderal index/bulk density, constituent concentration/bulk density, GFR density/speed or body-mass/infused-constituent rates.",
                 limitations=["No source fidelity, clinical applicability, empirical error or licensing validation is performed by this arithmetic audit.",
                              "It validates consistency of the declared/proposed coherent units with the current non-SI mass base, not an installed runtime projection.",
                              "Blocked scientific candidates can be dimensionally consistent; Cockcroft–Gault r2 remains blocked."],
                 record_revisions=len(results),distinct_relationships=len(latest),
                 all_revision_reference_cases=sum(x["canonical_reference_cases"] for x in results),
                 latest_reference_cases=sum(len(x["references"]) for x in latest.values()),
                 latest_status_counts={status:sum(x["integration"]["status"]==status for x in latest.values()) for status in ["runtime-ready","requires-extension","blocked"]},
                 records=results)
    (ROOT/"returns/unit-audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:audit[k] for k in ["audited_utc","record_revisions","distinct_relationships","all_revision_reference_cases","latest_reference_cases","latest_status_counts"]},indent=2))

if __name__=="__main__":
    main()
