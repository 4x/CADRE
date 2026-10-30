"""Standalone, offline HTML reports of executed evidence; no inference or recomputation."""

from html import escape
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from uuid import UUID, uuid4

from .contracts import ModelError


def read_run(run_id: str, directory: Path = Path(".runs")) -> dict[str, Any]:
    """Read only an explicitly identified saved run, never arbitrary local paths."""
    identifier = str(UUID(run_id))
    return json.loads((directory / f"{identifier}.json").read_text(encoding="utf-8"))


def label(value: Any) -> str:
    """Escape all stored model/proposal content before inserting it into HTML."""
    return escape(str(value), quote=True)


def amount(value: dict[str, Any]) -> str:
    """Format an executed value and its actual unit without changing the calculation."""
    return f"{float(value['amount']):,.2f} {label(value['port']['unit'])}"


def source_link(source: str) -> str:
    """Enable links only for public HTTP(S) references; render other provenance as text."""
    if urlsplit(source).scheme in {"http", "https"}:
        return f'<a href="{label(source)}" rel="noreferrer">{label(source)}</a>'
    return label(source)


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
            if "node" in binding:
                value = steps[binding["node"]]["result"]
                origin = f'Calculated by {label(binding["node"])}'
            else:
                value = binding
                origin = f'{label(value["origin"])} — {label(value["evidence"])}'
            rows.append(f'<tr><td>{label(name)}</td><td>{amount(value)}</td><td>{origin}</td></tr>')
        assumptions = "".join(f"<li>{label(item)}</li>" for item in model["assumptions"])
        review = run.get("admissions", {}).get(step["model"], {})
        review_note = f'Review: {label(review.get("reviewer", "fixture / no admission"))}. {label(review.get("notes", ""))}'
        cards.append(f'<details><summary><span>{index}. {label(step["node"])}</span><b>{amount(step["result"])}</b></summary>'
                     f'<p class="muted">{label(step["model"])}</p><code>{label(model["expression"])}</code>'
                     '<table><thead><tr><th>Input</th><th>Value</th><th>Origin</th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table><p>Source: {source_link(model["source"])}</p>'
                     f'<ul>{assumptions}</ul><p class="muted">{review_note}</p></details>')
    limits = "".join(f"<li>{label(item)}</li>" for item in run.get("limitations", []))
    error = f'<p class="error">{label(run["error"])}</p>' if run.get("error") else ""
    return (f'<section><div class="eyebrow">{label(run.get("status", "unknown"))} · {label(run["run_id"])}</div>'
            f'<h2>{label(run.get("question", run.get("composition", {}).get("id", "Saved run")))}</h2>'
            f'<p class="muted">{label(run.get("created", ""))}</p>{error}<div class="metrics">{outputs}</div>'
            f'<h3>What this answer assumes</h3><ul>{limits}</ul>'
            f'<h3>Follow the calculation</h3><p class="muted">Expand a step to inspect its inputs, model, sources and review.</p>{"".join(cards)}'
            f'<details><summary>Full saved evidence</summary><pre>{label(json.dumps(run, indent=2))}</pre></details></section>')


def write_report(run_ids: list[str], directory: Path = Path(".runs")) -> Path:
    """Export one or more runs into a self-contained report without paid operations."""
    if not 0 < len(run_ids) <= 8:
        raise ModelError("Choose between one and eight saved runs for a report.")
    runs = [read_run(identifier, directory) for identifier in run_ids]
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
            '<p>These are conditional heating scenarios using illustrative inputs. Compare the saved results and expand the calculations to see what each answer relies on. No inference or calculation runs when opening this report.</p></header>'
            f'<main>{"".join(run_section(run) for run in runs)}</main></html>')
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"report-{uuid4()}.html"
    with path.open("x", encoding="utf-8") as handle:
        handle.write(html)
    return path
