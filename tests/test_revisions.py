"""Saved-run revision: revised inputs or model revisions rerun with history preserved."""

from dataclasses import asdict, replace
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from uuid import uuid4

from connected_models.contracts import ModelError, Value
from connected_models.demo import catalog, composition
from connected_models.registry import Registry
from connected_models.reports import write_report
from connected_models.revisions import revise_run
from connected_models.runtime import execute, save_run
from connected_models.workflows import curate, load_packet, PACKET_PATH, reference_check, seed_candidates
from test_support import scratch_directory


def approve_test_catalog(registry: Registry) -> None:
    """Admit scratch-only supporting definitions and a mocked extracted model."""
    packet = load_packet(PACKET_PATH)
    model = catalog()["uniform-present-value@1"]
    symbols = {"annual": "A0", "rate": "d", "years": "t", "output": "PV"}
    extraction = {"content": {"expression": model.expression, "guards": list(model.guards),
        "assumptions": list(model.assumptions), "unresolved": [], "limitations": ["No zero-rate execution in this profile."],
        "source_map": [{"symbol": name, "source_symbol": source, "location": packet["location"]}
                       for name, source in symbols.items()]}, "audit": {"model": "test-double", "call_id": "offline-test"}}
    ids = seed_candidates(registry)
    with patch("connected_models.workflows.live_request", return_value=extraction):
        ids.append(curate(registry))
    for candidate_id in ids:
        registry.review(candidate_id, "test-reviewer", "Test-only admission, not scientific validation.")


def scenario_graph(operation: str = "investment"):
    """Build a scenario-purpose graph with operator-sourced inputs from fixtures."""
    base = composition(operation=operation)
    profile_version = load_packet(PACKET_PATH)["profile"]["version"]
    nodes = []
    for node in base.nodes:
        model = f"uniform-present-value@{profile_version}" if node.model == "uniform-present-value@1" else node.model
        bindings = {name: replace(value, origin="user-scenario") if isinstance(value, Value) else value
                    for name, value in node.bindings.items()}
        nodes.append(replace(node, model=model, bindings=bindings))
    return replace(base, purpose="scenario", nodes=tuple(nodes))


class RevisionTests(unittest.TestCase):
    """Exercise revise controls offline against scratch registries and run directories."""

    def test_revise_fixture_inputs_preserves_parent(self) -> None:
        """A revised input reruns with new results while the original file is untouched."""
        with scratch_directory() as folder:
            directory = Path(folder)
            old = execute(composition(), catalog())
            path = save_run(old, directory)
            contents = path.read_bytes()
            new = revise_run(old["run_id"], ["upgrade-energy.performance=2"], [], None, directory)
            self.assertEqual(new["status"], "completed", new.get("error"))
            self.assertNotEqual(new["run_id"], old["run_id"])
            self.assertEqual(new["revised_from"], old["run_id"])
            self.assertEqual(new["revision"]["sets"], {"upgrade-energy.performance": {"amount": 2.0, "unit": "1"}})
            self.assertEqual(new["outputs"]["annual-savings"]["amount"], 1800)
            self.assertEqual(old["outputs"]["annual-savings"]["amount"], 2400)
            self.assertEqual(new["diff"]["outputs"]["annual-savings"]["delta"], -600)
            self.assertEqual(path.read_bytes(), contents)
            self.assertTrue(Path(new["saved_path"]).is_file())
            revised_binding = [node for node in new["composition"]["nodes"] if node["id"] == "upgrade-energy"][0]["bindings"]["performance"]
            self.assertEqual(revised_binding["origin"], "user-scenario")
            self.assertIn(old["run_id"], revised_binding["evidence"])

    def test_revise_fixture_incompatible_model_is_saved_rejection(self) -> None:
        """An incompatible substitution fails loudly as saved evidence, not a silent diff."""
        with scratch_directory() as folder:
            directory = Path(folder)
            old = execute(composition(), catalog())
            save_run(old, directory)
            new = revise_run(old["run_id"], [], ["upgrade-energy=annual-saving@1"], None, directory)
            self.assertEqual(new["status"], "rejected")
            self.assertIn("missing/extra inputs", new["error"])
            self.assertEqual(new["revision"]["models"],
                             {"upgrade-energy": {"old": "heat-to-electricity@1", "new": "annual-saving@1"}})
            self.assertEqual(new["revised_from"], old["run_id"])
            self.assertTrue(Path(new["saved_path"]).is_file())

    def test_revise_scenario_inputs_offline(self) -> None:
        """Scenario input revision re-executes against eligible versions with fresh provenance."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            approve_test_catalog(registry)
            models, admissions = registry.snapshot()
            old = execute(scenario_graph("operating-cost"), models, admissions)
            self.assertEqual(old["status"], "completed", old.get("error"))
            directory = Path(folder) / "runs"
            save_run(old, directory)
            new = revise_run(old["run_id"], ["baseline-cost.tariff=0.25", "upgrade-cost.tariff=0.25"], [], registry, directory)
            self.assertEqual(new["status"], "completed", new.get("error"))
            self.assertEqual(new["outputs"]["annual-savings"]["amount"], 2000)
            self.assertEqual(new["diff"]["status"], {"old": "completed", "new": "completed"})
            self.assertEqual(len(new["diff"]["inputs"]), 2)
            self.assertTrue(new["admissions"])

    def test_revise_scenario_model_substitution(self) -> None:
        """An operator can select a compatible reviewed revision for one node and rerun."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            approve_test_catalog(registry)
            payload = json.loads(json.dumps(asdict(catalog()["heat-to-electricity@1"])))
            payload["version"] = "2"
            payload["expression"] = "heat / performance * 1.0"
            candidate = registry.propose({"model": payload, "evidence": "test-only revision",
                "checks": [reference_check(payload, {"inputs": {"heat": 120, "performance": 3}, "expected": 40})]})
            self.assertFalse(registry.candidate(candidate)["diagnostics"])
            registry.review(candidate, "test-reviewer", "Test-only second revision.")
            models, admissions = registry.snapshot()
            self.assertIn("heat-to-electricity@2", models)
            old = execute(scenario_graph("operating-cost"), models, admissions)
            directory = Path(folder) / "runs"
            save_run(old, directory)
            new = revise_run(old["run_id"], [], ["upgrade-energy=heat-to-electricity@2"], registry, directory)
            self.assertEqual(new["status"], "completed", new.get("error"))
            self.assertEqual(new["outputs"]["annual-savings"]["amount"], old["outputs"]["annual-savings"]["amount"])
            self.assertEqual(new["revision"]["models"],
                             {"upgrade-energy": {"old": "heat-to-electricity@1", "new": "heat-to-electricity@2"}})
            self.assertEqual(new["diff"]["models"],
                             [{"node": "upgrade-energy", "old": "heat-to-electricity@1", "new": "heat-to-electricity@2"}])
            self.assertIn("heat-to-electricity@2", new["models"])

    def test_revise_rejects_bad_targets(self) -> None:
        """Unknown nodes, calculated bindings, bad amounts and unknown models fail clearly."""
        with scratch_directory() as folder:
            directory = Path(folder)
            old = execute(composition(), catalog())
            save_run(old, directory)
            with self.assertRaisesRegex(ModelError, "Unknown node"):
                revise_run(old["run_id"], ["missing.performance=2"], [], None, directory)
            with self.assertRaisesRegex(ModelError, "no input"):
                revise_run(old["run_id"], ["upgrade-energy.missing=2"], [], None, directory)
            with self.assertRaisesRegex(ModelError, "calculated from"):
                revise_run(old["run_id"], ["baseline-cost.energy=5"], [], None, directory)
            with self.assertRaisesRegex(ModelError, "must be a finite number"):
                revise_run(old["run_id"], ["upgrade-energy.performance=much"], [], None, directory)
            with self.assertRaisesRegex(ModelError, "finite"):
                revise_run(old["run_id"], ["upgrade-energy.performance=inf"], [], None, directory)
            with self.assertRaisesRegex(ModelError, "Unknown model revision.*available"):
                revise_run(old["run_id"], [], ["upgrade-energy=missing@9"], None, directory)
            with self.assertRaisesRegex(ModelError, "Nothing to revise"):
                revise_run(old["run_id"], [], [], None, directory)

    def test_revise_rejects_runs_without_graph(self) -> None:
        """A needs-input run has nothing to revise; the operator must ask a new question."""
        with scratch_directory() as folder:
            directory = Path(folder)
            record = {"run_id": str(uuid4()), "status": "needs-input",
                      "clarifications": ["What electricity price should be used?"]}
            save_run(record, directory)
            with self.assertRaisesRegex(ModelError, "no executable graph"):
                revise_run(record["run_id"], ["upgrade-energy.performance=2"], [], None, directory)

    def test_report_comparison_shows_revision(self) -> None:
        """A two-run report visibly compares revised outputs, inputs and models."""
        with scratch_directory() as folder:
            directory = Path(folder)
            old = execute(composition(), catalog())
            save_run(old, directory)
            new = revise_run(old["run_id"], ["upgrade-energy.performance=2"], [], None, directory)
            html = write_report([old["run_id"], new["run_id"]], directory).read_text(encoding="utf-8")
            self.assertIn("What changed", html)
            self.assertIn("Changed inputs", html)
            self.assertIn("upgrade-energy.performance", html)
            self.assertIn("-600.00", html)
            self.assertIn("Revised from", html)
            single = write_report([old["run_id"]], directory).read_text(encoding="utf-8")
            self.assertNotIn("What changed", single)


if __name__ == "__main__":
    unittest.main()
