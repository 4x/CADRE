"""Standalone inspection reports preserve run evidence without executing content."""

from pathlib import Path
import unittest

from connected_models.demo import catalog, composition
from connected_models.reports import read_run, write_report
from connected_models.runtime import execute, save_run
from connected_models.contracts import Composition, Node, Value
from connected_models.solving import OUTPUT_BINDING
from test_support import scratch_directory


class ReportTests(unittest.TestCase):
    """Verify reports are offline, escaped views of recorded calculations."""

    def test_report_results_and_untrusted_text(self) -> None:
        """Stored model text must remain inert even when it contains HTML or unsafe URLs."""
        run = execute(composition(), catalog())
        run["question"] = '<script>alert("injection")</script>'
        run["query_inputs"] = {"facts": [{"name": "test input", "value": "3", "unit": "1", "value_type": "number", "quote": '<script>3</script>'}]}
        run["models"]["heat-to-electricity@1"]["source"] = "javascript:alert('bad')"
        with scratch_directory() as folder:
            directory = Path(folder)
            save_run(run, directory)
            path = write_report([run["run_id"]], directory)
            html = path.read_text(encoding="utf-8")
            self.assertIn("8,532.16 USD", html)
            self.assertIn("&lt;script&gt;", html)
            self.assertNotIn("<script>", html)
            self.assertNotIn('href="javascript:', html)
            self.assertIn("Follow the calculation", html)
            self.assertIn("baseline-energy", html)
            self.assertIn("Inputs read from your question", html)

    def test_blocked_report_and_restricted_path(self) -> None:
        """An unresolved answer is inspectable without permitting arbitrary file reads."""
        run = execute(composition(performance=0), catalog())
        with scratch_directory() as folder:
            directory = Path(folder)
            save_run(run, directory)
            html = write_report([run["run_id"]], directory).read_text(encoding="utf-8")
            self.assertIn("domain condition failed", html)
            with self.assertRaises(ValueError):
                read_run("../credential-file", directory)

    def test_inverse_report_exposes_original_model_and_solver_domain(self) -> None:
        """An inverse report must distinguish a target value from a calculated source output."""
        model = catalog()["uniform-present-value@1"]
        node = Node("payback", model.key, {
            "annual": Value(2400, model.inputs["annual"], "fixture", "known annual savings"),
            "rate": Value(0.05, model.inputs["rate"], "fixture", "known discount rate"),
            OUTPUT_BINDING: Value(10000, model.output, "fixture", "requested threshold")}, "years", "at_least")
        run = execute(Composition("payback-report", (node,), (node.id,)), {model.key: model})
        with scratch_directory() as folder:
            directory = Path(folder)
            save_run(run, directory)
            html = write_report([run["run_id"]], directory).read_text(encoding="utf-8")
            self.assertIn("Solved for years", html)
            self.assertIn("Solver checks and domain", html)
            self.assertIn("Requested original-output target", html)
            self.assertIn("5.00 years", html)
