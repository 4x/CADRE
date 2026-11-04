"""Independent oracle recomputation for CFA-L3 bundles.

Safe AST evaluator (no eval): supports numbers, names, lists via sum(),
+ - * / ** and unary +/-. Compares each reference oracle against the
record expression with the record's own tolerance. Read-only.
"""

import ast
import glob
import json
import operator
import sys

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate(node, env):
    if isinstance(node, ast.Expression):
        return evaluate(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise KeyError(f"missing input {node.id}")
        return env[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](evaluate(node.left, env), evaluate(node.right, env))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](evaluate(node.operand, env))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == "sum" and len(node.args) == 1 and not node.keywords:
            val = evaluate(node.args[0], env)
            if not isinstance(val, list):
                raise TypeError("sum() over non-list")
            return float(sum(val))
        raise ValueError(f"unsupported call {node.func.id}")
    raise ValueError(f"unsupported node {type(node).__name__}")


def check_bundle(path):
    with open(path, encoding="utf-8") as fh:
        bundle = json.load(fh)
    results = []
    for model in bundle["models"]:
        expr = model["relationship"]["expression"]
        try:
            tree = ast.parse(expr, mode="eval")
        except SyntaxError as exc:
            results.append((model["id"], "EXPR-PARSE-FAIL", str(exc)))
            continue
        for ref in model["references"]:
            env = {}
            for key, val in ref["inputs"].items():
                env[key] = [float(x) for x in val] if isinstance(val, list) else float(val)
            try:
                got = evaluate(tree, env)
            except Exception as exc:  # noqa: BLE001 - reported, not hidden
                results.append((model["id"], ref["id"], f"EVAL-FAIL: {exc}"))
                continue
            want = float(ref["expected"])
            tol = float(ref["tolerance"])
            if isinstance(got, list) or abs(got - want) > tol:
                results.append(
                    (model["id"], ref["id"], f"MISMATCH got={got} want={want} tol={tol}")
                )
            else:
                results.append((model["id"], ref["id"], "ok"))
    return bundle["batch_id"], results


def main():
    paths = sorted(glob.glob("from-offline-curation-workers/financial-analysis-cfa-l3-*/bundle.json"))
    total_ok = 0
    total_bad = 0
    for path in paths:
        batch, results = check_bundle(path)
        bad = [r for r in results if r[2] != "ok"]
        total_ok += len(results) - len(bad)
        total_bad += len(bad)
        print(f"{batch}: {len(results) - len(bad)}/{len(results)} ok")
        for model_id, ref_id, msg in bad:
            print(f"  BAD {model_id} :: {ref_id} :: {msg}")
    print(f"TOTAL ok={total_ok} bad={total_bad}")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
