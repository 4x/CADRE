"""Offline chain-compatibility audit over eligible models.

A directed edge A -> B exists when an output view of A satisfies
``Port.require_compatible`` against an input port of B: identical meaning
and context, with ratio-unit conversion allowed (currency excluded). Views
cover the forward output plus every inverse view (``solve_for`` each input);
inverse edges are structural only, since the audit does not solve.

Near misses drive curation: same meaning with different contexts wants a
context-alignment revision, while identical contexts with different
same-dimension meanings wants a scoped adapter record.
"""

from __future__ import annotations

from typing import Any

from .contracts import Model, ModelError, Port


def _views(model: Model) -> dict[str, Port]:
    """Map view names to their output ports without changing the model."""
    views = {"forward": model.output}
    for name, port in model.inputs.items():
        views[f"solve_for:{name}"] = port
    return views


def audit_pairs(models: dict[str, Model]) -> dict[str, Any]:
    """Pair every output view against every input port and report edges."""
    views: dict[str, dict[str, Port]] = {key: _views(model) for key, model in models.items()}
    inputs: dict[str, dict[str, Port]] = {key: dict(model.inputs) for key, model in models.items()}
    edges: list[dict[str, str]] = []
    same_meaning: dict[tuple[str, str, str], set[str]] = {}
    for source_key, source_views in views.items():
        for view, port in source_views.items():
            for target_key, target_inputs in inputs.items():
                for name, target in target_inputs.items():
                    try:
                        port.require_compatible(target)
                    except ModelError:
                        if port.meaning == target.meaning and port.context != target.context:
                            same_meaning.setdefault(
                                (port.meaning, port.context, target.context), set()).add(
                                f"{source_key}[{view}]->{target_key}.{name}")
                        continue
                    edges.append({"from": source_key, "view": view,
                                  "to": target_key, "input": name, "meaning": port.meaning})
    near_misses = [{"meaning": meaning, "from_context": first, "to_context": second,
                    "pairs": sorted(pairs)}
                   for (meaning, first, second), pairs in sorted(same_meaning.items())]
    connected = {edge["from"] for edge in edges} | {edge["to"] for edge in edges}
    isolates = sorted(set(models) - connected)
    domains: dict[str, dict[str, int]] = {}
    for edge in edges:
        for key in (edge["from"], edge["to"]):
            domain = key.split("--", 1)[0]
            domains.setdefault(domain, {"out_edges": 0, "in_edges": 0})
        domains[edge["from"].split("--", 1)[0]]["out_edges"] += 1
        domains[edge["to"].split("--", 1)[0]]["in_edges"] += 1
    return {"models": len(models),
            "views": sum(len(item) for item in views.values()),
            "inputs": sum(len(item) for item in inputs.values()),
            "edges": edges, "edge_count": len(edges),
            "near_misses": near_misses, "near_miss_count": len(near_misses),
            "isolates": isolates, "isolate_count": len(isolates),
            "domains": domains,
            "limits": ("Forward edges compile today; inverse-view edges are structural only, "
                       "since the audit does not solve. Units convert through registry scales; "
                       "currency never converts implicitly.")}
