"""Demo server: page resource, run listing, and offline revision over HTTP."""

import json
import threading
import unittest
import urllib.error
import urllib.request
from importlib.resources import files
from pathlib import Path
from typing import Any

from connected_models.demo_seed import seed_demo
from connected_models.registry import Registry
from connected_models.serve import (
    ServerConfig,
    create_server,
    latest_demo_runs,
    list_runs,
    load_page,
)

from .support import scratch_directory


def read_json(url: str) -> Any:
    """GET one demo URL and decode its JSON body."""
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url: str, body: dict[str, Any]) -> Any:
    """POST one JSON body to the demo server and decode its JSON reply."""
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


class ServeTests(unittest.TestCase):
    """The demo server stays offline-safe and honest about missing runs."""

    def test_page_resource_ships_with_demo_hooks(self) -> None:
        """The bundled page carries the elements and endpoints the demo needs."""
        self.assertTrue(files("connected_models").joinpath("web/index.html").is_file())
        page = load_page()
        for hook in (
            'id="question"',
            'id="ask-btn"',
            'id="graph"',
            'id="revise"',
            "/api/answer",
            "/api/revise",
            "/api/run/",
        ):
            self.assertIn(hook, page)

    def test_list_runs_skips_non_run_files(self) -> None:
        """Stray JSON never appears in the run list or breaks its ordering."""
        with scratch_directory() as workspace:
            runs = Path(workspace)
            (runs / "notes.json").write_text('{"note": "not a run"}', encoding="utf-8")
            (runs / "broken.json").write_text("{oops", encoding="utf-8")
            registry = Registry(runs / "models.sqlite3")
            seed_demo(registry, runs)
            summaries = list_runs(runs)
            self.assertEqual(len(summaries), 2)
            self.assertTrue(all(item["run_id"] for item in summaries))
            demo = latest_demo_runs(runs)
            self.assertEqual(
                {name for name, item in demo.items() if item},
                {"operating-cost", "investment"},
            )

    def test_http_demo_and_offline_revise(self) -> None:
        """The served API lists, loads, and revises runs without inference."""
        with scratch_directory() as workspace:
            runs = Path(workspace)
            registry = Registry(runs / "models.sqlite3")
            seeded = seed_demo(registry, runs)
            server = create_server(
                ServerConfig(runs / "models.sqlite3", runs), "127.0.0.1", 0
            )
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_port}"
                with urllib.request.urlopen(base + "/", timeout=10) as response:
                    self.assertIn("Connected Models", response.read().decode("utf-8"))
                demo = read_json(base + "/api/demo")
                self.assertIn("operating-cost", demo["questions"])
                run_id = seeded["runs"]["operating-cost"]["run_id"]
                manifest = read_json(f"{base}/api/run/{run_id}")
                self.assertEqual(manifest["run_id"], run_id)
                revised = post_json(
                    f"{base}/api/revise",
                    {"run_id": run_id, "sets": ["upgrade-energy.performance=2"]},
                )
                self.assertEqual(revised["status"], "completed")
                self.assertNotEqual(revised["run_id"], run_id)
                self.assertEqual(revised["outputs"]["upgrade-cost"]["amount"], 1800)
            finally:
                server.shutdown()
                thread.join(timeout=10)
                server.server_close()

    def test_http_errors_are_explicit(self) -> None:
        """Bad ids, missing runs, and bad revisions report distinct statuses."""
        with scratch_directory() as workspace:
            runs = Path(workspace)
            Registry(runs / "models.sqlite3")
            server = create_server(
                ServerConfig(runs / "models.sqlite3", runs), "127.0.0.1", 0
            )
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_port}"
                with self.assertRaises(urllib.error.HTTPError) as invalid:
                    read_json(f"{base}/api/run/not-a-uuid")
                self.assertEqual(invalid.exception.code, 400)
                with self.assertRaises(urllib.error.HTTPError) as missing:
                    read_json(f"{base}/api/run/00000000-0000-0000-0000-000000000000")
                self.assertEqual(missing.exception.code, 404)
                with self.assertRaises(urllib.error.HTTPError) as bad_revise:
                    post_json(
                        f"{base}/api/revise",
                        {"run_id": "00000000-0000-0000-0000-000000000000"},
                    )
                self.assertIn(bad_revise.exception.code, (400, 404))
            finally:
                server.shutdown()
                thread.join(timeout=10)
                server.server_close()
