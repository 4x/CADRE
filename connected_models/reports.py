"""Standalone, offline HTML reports of executed evidence; no inference or recomputation."""

from html import escape
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from uuid import UUID, uuid4

from .contracts import ModelError
from .solving import OUTPUT_BINDING


def read_run(run_id: str, directory: Path = Path(".runs")) -> dict[str, Any]:
    """Read only an explicitly identified saved run, never arbitrary local paths."""
    identifier = str(UUID(run_id))
    return json.loads((directory / f"{identifier}.json").read_text(encoding="utf-8"))


def label(value: Any) -> str:
    """Escape all stored model/proposal content before inserting it into HTML."""
    return escape(str(value), quote=True)


def amount(value: dict[str, Any]) -> str:
    """Format an executed value and its actual unit without changing the calculation."""
    unit = value["port"]["unit"]
    if value["port"]["meaning"] == "period_count" and value["port"]["context"] == "annual-period-count" and unit == "1":
        unit = "years (annual periods)"
    if "amounts" in value:
        joined = "; ".join(f"{float(item):,.2f}" for item in value["amounts"])
        return f"{joined} {label(unit)} (branch: all)"
    return f"{float(value['amount']):,.2f} {label(unit)}"


def source_link(source: str) -> str:
    """Enable links only for public HTTP(S) references; render other provenance as text."""
    if urlsplit(source).scheme in {"http", "https"}:
        return f'<a href="{label(source)}" rel="noreferrer">{label(source)}</a>'
    return label(source)


def value_bindings(run: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    """Index direct value bindings by node and input; upstream references are excluded."""
    bindings: dict[tuple[str, str], dict[str, Any]] = {}
    for node in run.get("composition", {}).get("nodes", []) or []:
        if not isinstance(node, dict):
            continue
        for name, binding in (node.get("bindings", {}) or {}).items():
            if isinstance(binding, dict) and "amount" in binding:
                bindings[(node.get("id", "?"), name)] = binding
    return bindings


def diff_runs(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """Compare status, outputs, value bindings and node models between two saved runs."""
    old_outputs = old.get("outputs", {}) or {}
    new_outputs = new.get("outputs", {}) or {}
    outputs: dict[str, Any] = {}
    for name in sorted(set(old_outputs) | set(new_outputs)):
        before = old_outputs.get(name)
        after = new_outputs.get(name)
        delta = None
        if (isinstance(before, dict) and isinstance(after, dict)
                and before.get("port", {}).get("unit") == after.get("port", {}).get("unit")
                and isinstance(before.get("amount"), (int, float)) and isinstance(after.get("amount"), (int, float))):
            delta = after["amount"] - before["amount"]
        outputs[name] = {"old": before, "new": after, "delta": delta}
    old_bindings, new_bindings = value_bindings(old), value_bindings(new)
    inputs = []
    for key in sorted(set(old_bindings) | set(new_bindings)):
        before, after = old_bindings.get(key), new_bindings.get(key)
        if before == after:
            continue
        node_id, name = key
        inputs.append({"node": node_id, "input": name,
                       "old": {"amount": before.get("amount"), "unit": before.get("port", {}).get("unit")} if before else None,
                       "new": {"amount": after.get("amount"), "unit": after.get("port", {}).get("unit")} if after else None})
    old_models = {node.get("id"): node.get("model") for node in old.get("composition", {}).get("nodes", []) or [] if isinstance(node, dict)}
    new_models = {node.get("id"): node.get("model") for node in new.get("composition", {}).get("nodes", []) or [] if isinstance(node, dict)}
    models = [{"node": node_id, "old": old_models.get(node_id), "new": new_models.get(node_id)}
              for node_id in sorted(set(old_models) | set(new_models)) if old_models.get(node_id) != new_models.get(node_id)]
    return {"base_run": old.get("run_id"), "new_run": new.get("run_id"),
            "status": {"old": old.get("status"), "new": new.get("status")},
            "outputs": outputs, "inputs": inputs, "models": models}


def comparison_section(runs: list[dict[str, Any]]) -> str:
    """Render what changed in each listed run relative to the first listed run."""
    blocks = []
    for run in runs[1:]:
        diff = diff_runs(runs[0], run)
        status = diff["status"]
        rows = []
        for name, change in diff["outputs"].items():
            before = amount(change["old"]) if change["old"] else "—"
            after = amount(change["new"]) if change["new"] else "—"
            delta = f'{change["delta"]:+,.2f}' if change["delta"] is not None else "—"
            rows.append(f"<tr><td>{label(name)}</td><td>{before}</td><td>{after}</td><td>{label(delta)}</td></tr>")
        output_table = ("<table><thead><tr><th>Output</th><th>Before</th><th>After</th><th>Change</th></tr></thead>"
                        f"<tbody>{''.join(rows)}</tbody></table>") if rows else "<p>No outputs in either run.</p>"
        def recorded(entry: dict[str, Any] | None) -> str:
            """Format a recorded input amount and unit without recalculating it."""
            if not entry:
                return "—"
            return f"{label(entry.get('amount'))} {label(entry.get('unit'))}"

        input_rows = "".join(
            f"<tr><td>{label(change['node'])}.{label(change['input'])}</td>"
            f"<td>{recorded(change['old'])}</td>"
            f"<td>{recorded(change['new'])}</td></tr>" for change in diff["inputs"])
        input_table = ("<h4>Changed inputs</h4><table><thead><tr><th>Binding</th><th>Before</th><th>After</th></tr></thead>"
                       f"<tbody>{input_rows}</tbody></table>") if input_rows else ""
        model_rows = "".join(
            f"<tr><td>{label(change['node'])}</td><td>{label(change['old'])}</td><td>{label(change['new'])}</td></tr>"
            for change in diff["models"])
        model_table = ("<h4>Changed models</h4><table><thead><tr><th>Node</th><th>Before</th><th>After</th></tr></thead>"
                       f"<tbody>{model_rows}</tbody></table>") if model_rows else ""
        blocks.append(
            f"<h3>{label(run.get('run_id', '?'))} versus {label(runs[0].get('run_id', '?'))}</h3>"
            f"<p class=\"muted\">Status: {label(status['old'])} → {label(status['new'])}."
            + (f" Revised from {label(run['revised_from'])}." if run.get("revised_from") else "")
            + f"</p>{output_table}{input_table}{model_table}")
    return (f"<section><div class=\"eyebrow\">Comparison · {len(runs)} runs</div><h2>What changed</h2>"
            f"<p class=\"muted\">Each run below is compared with the first listed run. Amounts use executed units; inputs show raw recorded values.</p>"
            f"{''.join(blocks)}</section>")


def run_section(run: dict[str, Any]) -> str:
    """Show requested results, actual dependencies, model evidence and input origins."""
    outputs = "".join(f'<div class="metric"><span>{label(name)}</span><strong>{amount(value)}</strong>'
                      f'<small>{label(value["port"]["meaning"])} · {label(value["port"]["context"])}</small></div>'
                      for name, value in run.get("outputs", {}).items())
    node_map = {node["id"]: node for node in run.get("composition", {}).get("nodes", [])}
    steps = {step["node"]: step for step in run.get("steps", [])}
    cards = []
    for index, step in enumerate(steps.values(), start=1):
        model = run["models"][step["model"]]
        rows = []
        for name, binding in node_map[step["node"]]["bindings"].items():
            elements = [(f"{name}[{index}]", element) for index, element in enumerate(binding)] if isinstance(binding, list) else [(name, binding)]
            for element_name, element in elements:
                if "node" in element:
                    value = steps[element["node"]]["result"]
                    origin = f'Calculated by {label(element["node"])}'
                else:
                    value = element
                    origin = f'{label(value["origin"])} — {label(value["evidence"])}'
                input_label = "Requested original-output target" if element_name == OUTPUT_BINDING else element_name
                rows.append(f'<tr><td>{label(input_label)}</td><td>{amount(value)}</td><td>{origin}</td></tr>')
        assumptions = "".join(f"<li>{label(item)}</li>" for item in model["assumptions"])
        review = run.get("admissions", {}).get(step["model"], {})
        review_note = f'Review: {label(review.get("reviewer", "fixture / no admission"))}. {label(review.get("notes", ""))}'
        operation = ""
        if step.get("solve"):
            evidence = step["solve"]
            operation = (f'<p><b>Solved for {label(evidence["solve_for"])}</b> using {label(evidence["method"])} '
                         f'({label(evidence["relation"])}). The original relationship and review are retained.</p>'
                         f'<details><summary>Solver checks and domain</summary><pre>{label(json.dumps(evidence, indent=2))}</pre></details>')
        cards.append(f'<details><summary><span>{index}. {label(step["node"])}</span><b>{amount(step["result"])}</b></summary>'
                     f'<p class="muted">{label(step["model"])}</p><code>{label(model["expression"])}</code>{operation}'
                     '<table><thead><tr><th>Input</th><th>Value</th><th>Origin</th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table><p>Source: {source_link(model["source"])}</p>'
                     f'<ul>{assumptions}</ul><p class="muted">{review_note}</p></details>')
    limits = "".join(f"<li>{label(item)}</li>" for item in run.get("limitations", []))
    error = f'<p class="error">{label(run["error"])}</p>' if run.get("error") else ""
    questions = "".join(f"<li>{label(item)}</li>" for item in run.get("clarifications", []))
    clarification_section = f"<h3>What needs clarification</h3><ul>{questions}</ul>" if questions else ""
    def fact_type(fact: dict[str, Any]) -> str:
        """Mark assumption-filled facts so the report shows what was supplied, not quoted."""
        if fact.get("assumed"):
            return f"{fact['value_type']} (assumed: {fact.get('assumption', '')})"
        return str(fact["value_type"])
    fact_rows = "".join(f'<tr><td>{label(fact["name"])}</td><td>{label(fact["value"])} {label(fact["unit"])}</td>'
                        f'<td>{label(fact_type(fact))}</td><td>{label(fact["quote"])}</td></tr>'
                        for fact in run.get("query_inputs", {}).get("facts", []))
    input_section = ('<h3>Inputs read from your question</h3><table><thead><tr><th>Input</th><th>Value</th><th>Type</th><th>Exact source text</th></tr></thead>'
                     f'<tbody>{fact_rows}</tbody></table>') if fact_rows else ""
    revised = (f'<p class="muted">Revised from {label(run["revised_from"])}; the original run is preserved.</p>'
               if run.get("revised_from") else "")
    return (f'<section><div class="eyebrow">{label(run.get("status", "unknown"))} · {label(run["run_id"])}</div>'
            f'<h2>{label(run.get("question", run.get("composition", {}).get("id", "Saved run")))}</h2>'
            f'<p class="muted">{label(run.get("created", ""))}</p>{revised}{error}{clarification_section}<div class="metrics">{outputs}</div>{input_section}'
            f'<h3>What this answer assumes</h3><ul>{limits}</ul>'
            f'<h3>Follow the calculation</h3><p class="muted">Expand a step to inspect its inputs, model, sources and review.</p>{"".join(cards)}'
            f'<details><summary>Full saved evidence</summary><pre>{label(json.dumps(run, indent=2))}</pre></details></section>')


def write_report(run_ids: list[str], directory: Path = Path(".runs")) -> Path:
    """Export one or more runs into a self-contained report without paid operations."""
    if not 0 < len(run_ids) <= 8:
        raise ModelError("Choose between one and eight saved runs for a report.")
    runs = [read_run(identifier, directory) for identifier in run_ids]
    comparison = comparison_section(runs) if len(runs) > 1 else ""
    style = """
    :root { color-scheme: light; font-family: Segoe UI,system-ui,sans-serif; color:#152c37; background:#edf2f3 }
    * { box-sizing:border-box } body { margin:0 } header { padding:36px max(5vw,20px); background:#143744; color:#fff }
    header p { max-width:850px; color:#cbdde2 } h1 { font-weight:600; font-size:36px; margin:8px 0 }
    main { max-width:1200px; margin:28px auto; padding:0 20px } section { background:#fff; border:1px solid #d7e2e5; border-radius:16px; padding:28px; margin-bottom:24px }
    h2 { font-size:23px; line-height:1.4 } h3 { margin-top:30px } a { color:#17657d; overflow-wrap:anywhere }
    .eyebrow { font-size:12px; text-transform:uppercase; letter-spacing:.08em; overflow-wrap:anywhere }
    .muted, small { color:#526d79 } .metrics { display:flex; flex-wrap:wrap; gap:12px; margin:24px 0 }
    .metric { flex:1 1 220px; padding:18px; background:#eff7f5; border-left:4px solid #3b8d77; border-radius:8px }
    .metric span,.metric strong,.metric small { display:block; overflow-wrap:anywhere } .metric strong { font-size:27px; margin:10px 0 }
    details { border:1px solid #d8e4e7; border-radius:8px; padding:16px; margin:12px 0; overflow-wrap:anywhere }
    summary { cursor:pointer; font-weight:600 } summary b { float:right; padding-left:12px } code,pre { background:#f3f6f8; padding:10px; border-radius:6px }
    code { display:block } pre { white-space:pre-wrap; max-height:600px; overflow:auto; font-size:12px } table { width:100%; margin:18px 0; border-collapse:collapse; font-size:14px }
    th,td { padding:10px; text-align:left; border-bottom:1px solid #e1e8eb; vertical-align:top } li { margin:8px 0; line-height:1.5 } .error { background:#fff1ed; padding:16px; color:#8b3324 }
    @media(max-width:640px) { section { padding:18px } summary b { float:none; display:block; padding:8px 0 } table { font-size:12px } }
    """
    html = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Connected Models — run evidence</title>'
            f'<style>{style}</style><header><div class="eyebrow">Connected Models / Prototype</div><h1>Inspect the answer</h1>'
            '<p>Inspect the inputs and assumptions recorded with each question, then expand the calculations to see what each answer relies on. No inference or calculation runs when opening this report.</p></header>'
            f'<main>{comparison}{"".join(run_section(run) for run in runs)}</main></html>')
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"report-{uuid4()}.html"
    with path.open("x", encoding="utf-8") as handle:
        handle.write(html)
    return path
