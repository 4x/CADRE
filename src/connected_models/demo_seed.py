"""Offline demo seeding: fixture admissions plus scripted runs for demos and video.

Everything here is deterministic and spends nothing: it admits the synthetic
heating fixtures as explicitly labeled demo models and executes two scripted
scenarios. Demo admissions illustrate the review flow; they are not
scientific approval and never mix with curated registries silently.
"""

from __future__ import annotations

import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from .contracts import Model
from .demo import catalog, composition
from .registry import Registry
from .runtime import execute, save_run
from .workflows import reference_check

DEMO_REVIEWER = "demo-seed"
DEMO_NOTES = "Demo fixture admission; illustrates the flow, not scientific approval."

REFERENCES: dict[str, dict[str, Any]] = {
    "heat-to-electricity": {
        "inputs": {"heat": 120, "performance": 3},
        "expected": 40,
    },
    "electricity-cost": {
        "inputs": {"energy": 20, "tariff": 0.25},
        "expected": 5,
    },
    "annual-saving": {
        "inputs": {"baseline": 20, "alternative": 5},
        "expected": 15,
    },
    "uniform-present-value": {
        "inputs": {"annual": 100, "rate": 0.03, "years": 5},
        "expected": 457.97,
    },
    "net-present-value": {
        "inputs": {"benefit": 20, "investment": 5},
        "expected": 15,
    },
}

DEMO_QUESTIONS: dict[str, str] = {
    "operating-cost": (
        "Delivered heat is 12000 kWh. Heat pump seasonal performance is 3. "
        "Tariff is 0.30 USD/kWh. What is the annual operating cost?"
    ),
    "investment": (
        "Delivered heat is 12000 kWh per year. Baseline resistance heating has "
        "seasonal performance 1 and the proposed heat pump has seasonal "
        "performance 3. Tariff is 0.30 USD/kWh. The heat pump costs 10000 USD "
        "with a 5% real discount rate over 10 years. What is the net present value?"
    ),
}


def model_payload(model: Model) -> dict[str, Any]:
    """Serialize one fixture model into plain JSON-safe data."""
    payload: dict[str, Any] = json.loads(json.dumps(asdict(model)))
    return payload


def seed_demo_registry(registry: Registry) -> dict[str, str]:
    """Admit every heating fixture missing from the registry as a labeled demo model."""
    eligible, _ = registry.snapshot()
    admissions: dict[str, str] = {}
    for model in catalog().values():
        if model.key in eligible:
            admissions[model.key] = "already-eligible"
            continue
        payload = model_payload(model)
        candidate_id = registry.propose(
            {
                "model": payload,
                "evidence": {
                    "kind": "demo-fixture",
                    "source": model.source,
                    "notes": DEMO_NOTES,
                },
                "checks": [reference_check(payload, REFERENCES[model.id])],
            }
        )
        admissions[model.key] = registry.review(
            candidate_id, DEMO_REVIEWER, DEMO_NOTES, "accepted"
        )
    return admissions


def seed_demo_runs(
    models: dict[str, Model], directory: Path
) -> dict[str, dict[str, Any]]:
    """Execute the scripted demo scenarios offline and save each run manifest."""
    fixtures = {key: replace(model, status="fixture") for key, model in models.items()}
    scenarios = {
        "operating-cost": composition(operation="operating-cost"),
        "investment": composition(operation="investment"),
    }
    runs: dict[str, dict[str, Any]] = {}
    for name, scenario in scenarios.items():
        manifest = execute(scenario, fixtures)
        path = save_run(manifest, directory)
        runs[name] = {
            "run_id": manifest["run_id"],
            "status": manifest["status"],
            "outputs": manifest.get("outputs", {}),
            "saved_path": str(path),
        }
    return runs


def seed_demo(registry: Registry, directory: Path) -> dict[str, Any]:
    """Seed demo admissions and scripted runs; returns everything the demo needs."""
    admissions = seed_demo_registry(registry)
    models, _ = registry.snapshot()
    return {
        "admissions": admissions,
        "runs": seed_demo_runs(models, directory),
        "questions": DEMO_QUESTIONS,
    }
