"""Storage, review, source extraction and separate query-composition regressions."""

from dataclasses import asdict, replace
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from connected_models.contracts import ModelError, Value
from connected_models.demo import catalog, composition
from connected_models.registry import Registry
from connected_models.runtime import execute
from connected_models.workflows import answer, curate, load_packet, PACKET_PATH, seed_candidates, scenario_inputs
from test_support import scratch_directory


class RegistryTests(unittest.TestCase):
    """Use only scratch registries and fake model responses; never live credentials."""

    def extraction(self) -> dict:
        """Return a test double explicitly distinct from real offline inference."""
        packet = load_packet(PACKET_PATH)
        model = catalog()["uniform-present-value@1"]
        symbols = {"annual": "A0", "rate": "d", "years": "t", "output": "PV"}
        return {"content": {"expression": model.expression, "guards": list(model.guards),
            "assumptions": list(model.assumptions), "unresolved": [], "limitations": ["No zero-rate execution in this profile."],
            "source_map": [{"symbol": name, "source_symbol": source, "location": packet["location"]}
                           for name, source in symbols.items()]}, "audit": {"model": "test-double", "call_id": "offline-test"}}

    def approve_test_catalog(self, registry: Registry) -> None:
        """Admit scratch-only supporting definitions and a mocked extracted model."""
        ids = seed_candidates(registry)
        with patch("connected_models.workflows.live_request", return_value=self.extraction()):
            ids.append(curate(registry))
        for candidate_id in ids:
            self.assertFalse(registry.candidate(candidate_id)["diagnostics"])
            registry.review(candidate_id, "test-reviewer", "Test-only admission, not scientific validation.")

    def test_partial_candidate_not_eligible(self) -> None:
        """Incomplete knowledge is retained without acquiring execution authority."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            candidate = registry.propose({"model": {"id": "partial"}, "evidence": "unresolved unit"})
            self.assertTrue(registry.candidate(candidate)["diagnostics"])
            self.assertEqual(registry.snapshot(), ({}, {}))
            with self.assertRaises(ModelError):
                registry.review(candidate, "owner", "This incomplete model must not publish.")

    def test_claimed_pass_is_recomputed(self) -> None:
        """A curator-provided passed flag cannot disguise a wrong independent reference."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            raw = json.loads(json.dumps(asdict(catalog()["annual-saving@1"])))
            candidate = registry.propose({"model": raw, "evidence": "test only", "checks": [{"passed": True,
                "reference": {"inputs": {"baseline": 20, "alternative": 5}, "expected": 999}}]})
            self.assertTrue(registry.candidate(candidate)["diagnostics"])
            with self.assertRaisesRegex(ModelError, "blocking diagnostics"):
                registry.review(candidate, "owner", "Failing arithmetic must not be admitted.")

    def test_reopen_withdraw_and_old_snapshot(self) -> None:
        """Withdrawal affects new snapshots while old run evidence stays available."""
        with scratch_directory() as folder:
            path = Path(folder) / "registry.sqlite3"
            registry = Registry(path)
            self.approve_test_catalog(registry)
            models, admissions = Registry(path).snapshot()
            self.assertEqual(len(models), 5)
            target = admissions["annual-saving@1"]["candidate"]
            registry.review(target, "owner", "Withdrawn in test", "withdrawn")
            self.assertNotIn("annual-saving@1", registry.snapshot()[0])
            self.assertIn("annual-saving@1", models)
            self.assertIn("review_id", admissions["annual-saving@1"])
            self.assertEqual(seed_candidates(registry), seed_candidates(registry))

    def test_failed_extraction_reference_retained(self) -> None:
        """Numerically wrong source extraction cannot be published even with valid units."""
        response = self.extraction()
        response["content"]["expression"] = "annual * years"
        with scratch_directory() as folder, patch("connected_models.workflows.live_request", return_value=response):
            registry = Registry(Path(folder) / "registry.sqlite3")
            candidate = curate(registry)
            self.assertTrue(registry.candidate(candidate)["diagnostics"])
            with self.assertRaisesRegex(ModelError, "blocking diagnostics"):
                registry.review(candidate, "owner", "Must not admit a wrong reference.")

    def test_in_scope_ambiguity_stays_blocking(self) -> None:
        """A separate limitations field must never erase true unresolved semantics."""
        response = self.extraction()
        response["content"]["unresolved"] = ["Cannot identify the source discount rate convention."]
        with scratch_directory() as folder, patch("connected_models.workflows.live_request", return_value=response):
            registry = Registry(Path(folder) / "registry.sqlite3")
            candidate = registry.candidate(curate(registry))
            self.assertTrue(candidate["diagnostics"])
            self.assertTrue(candidate["evidence"]["extraction"]["unresolved"])
            self.assertEqual(registry.snapshot(), ({}, {}))

    def test_immutable_revision_and_forged_status(self) -> None:
        """A label cannot replace reviewed admission; changed definitions need a new revision."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            self.approve_test_catalog(registry)
            models, admissions = registry.snapshot()
            original = models["annual-saving@1"]
            changed = replace(original, expression="baseline + alternative")
            models[original.key] = changed
            base = composition()
            graph = replace(base, purpose="scenario", nodes=tuple(replace(node,
                bindings={name: replace(value, origin="user-scenario") if isinstance(value, Value) else value
                          for name, value in node.bindings.items()}) for node in base.nodes))
            rejected = execute(graph, models, admissions)
            self.assertIn("admission", rejected["error"])
            payload = json.loads(json.dumps(asdict(changed)))
            from connected_models.workflows import reference_check
            candidate = registry.propose({"model": payload, "evidence": "changed model", "checks": [reference_check(payload,
                {"inputs": {"baseline": 20, "alternative": 5}, "expected": 25})]})
            with self.assertRaisesRegex(ModelError, "immutable"):
                registry.review(candidate, "owner", "Cannot overwrite an existing revision.")

    def test_separate_composition_reuses_eligible_versions(self) -> None:
        """Query-time proposals use stored versions and the same executor, without curation."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            self.approve_test_catalog(registry)
            values = {item["id"]: {key: value for key, value in item.items() if key != "id"}
                      for item in scenario_inputs(3, 10000, 0.3)}
            for operation in ("operating-cost", "investment"):
                graph = composition(operation=operation)
                nodes = []
                for node in graph.nodes:
                    raw = asdict(node)
                    if node.model == "uniform-present-value@1":
                        raw["model"] = "uniform-present-value@" + load_packet(PACKET_PATH)["profile"]["version"]
                    for name, binding in node.bindings.items():
                        if isinstance(binding, Value):
                            raw["bindings"][name] = values[f"{node.id}.{name}"]
                    nodes.append(raw)
                response = {"content": {"status": "proposed", "graph_json": json.dumps({"id": operation, "nodes": nodes,
                            "outputs": list(graph.outputs)}), "reason": "Test-only composition."}, "audit": {"model": "test-double"}}
                with patch("connected_models.workflows.live_request", return_value=response) as inference, patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"):
                    result = answer(registry, "Compare the conditional heating scenario", 3, 10000, 0.3)
                self.assertEqual(result["status"], "completed", result.get("error"))
                self.assertEqual(result["outputs"]["annual-savings"]["amount"], 2400)
                self.assertEqual(inference.call_count, 1)
                self.assertTrue(result["admissions"])

    def test_no_match_is_saved_without_curation(self) -> None:
        """An uncovered question remains blocked and inspectable, with no inline extraction."""
        with scratch_directory() as folder:
            registry = Registry(Path(folder) / "registry.sqlite3")
            self.approve_test_catalog(registry)
            response = {"content": {"status": "unresolved", "graph_json": "", "reason": "No forecast model in this registry."}, "audit": {}}
            with patch("connected_models.workflows.live_request", return_value=response), patch("connected_models.workflows.RUNS_PATH", Path(folder) / "runs"):
                result = answer(registry, "Forecast a market price", 3, 10000, 0.3)
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(Path(result["saved_path"]).is_file())
