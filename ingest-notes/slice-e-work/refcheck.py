"""Independent review checker for slice E (CFA L1 b3 b01-b50).

Recomputes every reference case with an independent restricted evaluator,
verifies reference inputs satisfy the record's own guards, and checks
rejection-case structure. Stdlib only. Read-only w.r.t. worker bundles.
Usage: uv run --no-env-file python ingest-notes/slice-e-work/refcheck.py
"""

import ast
import json
import math
import operator as op
from pathlib import Path

ROOT = Path("from-offline-curation-workers")
BINOPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod,
}
UNARY = {ast.UAdd: op.pos, ast.USub: op.neg}
CMP = {
    ast.Eq: op.eq, ast.NotEq: op.ne, ast.Lt: op.lt,
    ast.LtE: op.le, ast.Gt: op.gt, ast.GtE: op.ge,
}
FUNCS = {
    "log": math.log, "log10": math.log10, "exp": math.exp,
    "sqrt": math.sqrt, "sum": lambda *a: sum(a),
    "prod": lambda *a: math.prod(a), "abs": abs,
    "min": min, "max": max, "len": len,
}


def ev(node, env):
    """Evaluate a parsed expression node under env; no attribute/subscript/call abuse."""
    if isinstance(node, ast.Expression):
        return ev(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in BINOPS:
        return BINOPS[type(node.op)](ev(node.left, env), ev(node.right, env))
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY:
        return UNARY[type(node.op)](ev(node.operand, env))
    if isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in CMP:
        return CMP[type(node.ops[0])](ev(node.left, env), ev(node.comparators[0], env))
    if isinstance(node, ast.BoolOp):
        vals = [ev(v, env) for v in node.values]
        return all(vals) if isinstance(node.op, ast.And) else any(vals)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id not in FUNCS or node.keywords:
            raise ValueError(f"unsupported call {node.func.id}")
        return FUNCS[node.func.id](*[ev(a, env) for a in node.args])
    raise ValueError(f"unsupported node {type(node).__name__}")


def run():
    n_ref = n_ref_ok = n_guard_sat = n_guard_tot = 0
    problems = []
    for n in range(1, 51):
        batch = f"financial-analysis-cfa-l1-b3-b{n:02d}"
        bundle = json.loads((ROOT / batch / "bundle.json").read_text())
        for m in bundle["models"]:
            ident = f"{m['id']}@{m['revision']} ({batch})"
            inputs = {v["symbol"] for v in m["variables"] if v["role"] == "input"}
            expr = ast.parse(m["relationship"]["expression"], mode="eval")
            for ref in m["references"]:
                n_ref += 1
                try:
                    got = ev(expr, dict(ref["inputs"]))
                except Exception as exc:  # noqa: BLE001
                    problems.append(f"{ident} ref={ref['id']}: EVAL-ERROR {exc}")
                    continue
                tol = ref.get("tolerance", 0.0)
                if abs(got - ref["expected"]) <= tol + 1e-12:
                    n_ref_ok += 1
                else:
                    problems.append(
                        f"{ident} ref={ref['id']}: MISMATCH got={got!r} "
                        f"expected={ref['expected']!r} tol={tol}"
                    )
                for g in m["guards"]:
                    n_guard_tot += 1
                    try:
                        sat = ev(ast.parse(g, mode="eval"), dict(ref["inputs"]))
                    except Exception as exc:  # noqa: BLE001
                        problems.append(f"{ident} ref={ref['id']}: GUARD-EVAL-ERROR {g} {exc}")
                        continue
                    if sat is True or (isinstance(sat, (int, float)) and sat != 0):
                        n_guard_sat += 1
                    else:
                        problems.append(f"{ident} ref={ref['id']}: GUARD-VIOLATED {g}")
            for rej in m["rejection_cases"]:
                given = set(rej["inputs"])
                if rej["kind"] == "missing-input" and not (given < inputs):
                    problems.append(f"{ident}: REJ-STRUCT missing-input {sorted(given)} vs {sorted(inputs)}")
                if rej["kind"] not in ("missing-input", "guard-violation", "domain-error", "incompatible"):
                    problems.append(f"{ident}: REJ-KIND unknown {rej['kind']}")
    print(f"references: {n_ref_ok}/{n_ref} recomputed-in-tolerance")
    print(f"guard-sat on reference inputs: {n_guard_sat}/{n_guard_tot}")
    print(f"problems: {len(problems)}")
    for p in problems:
        print("  " + p)


if __name__ == "__main__":
    run()
