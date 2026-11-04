"""Local web demo over the standard library only: ask, animate, revise.

The server exposes saved runs and the offline revision machinery as JSON,
plus one live endpoint that runs the normal `answer` workflow. No third-party
packages, no external requests, no inference on page load.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from pathlib import Path
from typing import Any, cast
from urllib.parse import unquote, urlsplit
from uuid import UUID

from .contracts import ModelError
from .demo_seed import DEMO_QUESTIONS
from .query_inputs import MAX_QUERY_CHARS
from .registry import Registry
from .reports import read_run, write_report
from .revisions import revise_run
from .workflows import answer

LOGGER = logging.getLogger("connected_models.serve")
MAX_BODY_BYTES = 65536
MAX_RUNS_LISTED = 20
TITLE_CHARS = 90

DEMO_COMPOSITIONS = {
    "heating-operating-cost": "operating-cost",
    "heating-investment": "investment",
}


@dataclass(frozen=True)
class ServerConfig:
    """Working-state locations the demo server reads and writes."""

    registry_path: Path
    runs_dir: Path


class HttpError(Exception):
    """A failure with the status code the demo server should report."""

    def __init__(self, status: int, message: str) -> None:
        """Keep the public message free of paths and secrets."""
        super().__init__(message)
        self.status = status


def load_page() -> str:
    """Read the bundled single-file demo page."""
    try:
        return (
            files("connected_models")
            .joinpath("web")
            .joinpath("index.html")
            .read_text(encoding="utf-8")
        )
    except OSError as exc:
        raise ModelError("Demo page is not installed.") from exc


def run_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    """Project one manifest to the compact card the run list shows."""
    question = manifest.get("question")
    composition = manifest.get("composition") or {}
    title = (
        question[:TITLE_CHARS]
        if isinstance(question, str) and question
        else str(composition.get("id") or manifest.get("run_id"))
    )
    outputs = {}
    for name, value in (manifest.get("outputs") or {}).items():
        if isinstance(value, dict) and isinstance(value.get("port"), dict):
            outputs[name] = {
                "amount": value.get("amount"),
                "unit": value["port"].get("unit"),
                "meaning": value["port"].get("meaning"),
            }
    return {
        "run_id": manifest.get("run_id"),
        "created": manifest.get("created"),
        "status": manifest.get("status"),
        "title": title,
        "outputs": outputs,
    }


def list_runs(directory: Path) -> list[dict[str, Any]]:
    """List saved run summaries, newest first; skip files that are not runs."""
    summaries: list[dict[str, Any]] = []
    if not directory.is_dir():
        return summaries
    for path in directory.glob("*.json"):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            LOGGER.debug(f"Skipping unreadable run file {path.name}.")
            continue
        if (
            not isinstance(manifest, dict)
            or not manifest.get("run_id")
            or not manifest.get("status")
        ):
            continue
        summaries.append(run_summary(manifest))
    summaries.sort(key=lambda item: str(item.get("created") or ""), reverse=True)
    return summaries[:MAX_RUNS_LISTED]


def latest_demo_runs(directory: Path) -> dict[str, dict[str, Any] | None]:
    """Find the newest saved run per scripted demo scenario, if any exist."""
    found: dict[str, dict[str, Any]] = {}
    if directory.is_dir():
        manifests = []
        for path in directory.glob("*.json"):
            try:
                manifest = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(manifest, dict) and manifest.get("status") == "completed":
                manifests.append(manifest)
        manifests.sort(key=lambda item: str(item.get("created") or ""))
        for manifest in manifests:
            composition = manifest.get("composition") or {}
            name = DEMO_COMPOSITIONS.get(str(composition.get("id") or ""))
            if name:
                found[name] = run_summary(manifest)
    return {name: found.get(name) for name in DEMO_QUESTIONS}


def load_run(run_id: str, directory: Path) -> dict[str, Any]:
    """Read one saved run or raise the HTTP error the handler should report."""
    try:
        UUID(run_id)
    except ValueError:
        raise HttpError(400, "That run id is not valid.") from None
    try:
        return read_run(run_id, directory)
    except FileNotFoundError:
        raise HttpError(404, "No saved run has that id.") from None
    except (OSError, ValueError) as exc:
        LOGGER.error(f"Unreadable run {run_id}: {exc.__class__.__name__}.")
        raise HttpError(500, "That saved run cannot be read.") from None


class DemoServer(ThreadingHTTPServer):
    """Threaded demo server carrying its working-state configuration."""

    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], config: ServerConfig) -> None:
        """Bind the address; `config` selects the registry and runs directory."""
        self.config = config
        super().__init__(server_address, DemoHandler)


class DemoHandler(BaseHTTPRequestHandler):
    """Serve the demo page plus a small JSON API over runs and revisions."""

    server_version = "ConnectedModelsDemo/1"

    @property
    def config(self) -> ServerConfig:
        """Read the server-owned working-state configuration."""
        return cast("DemoServer", self.server).config

    def log_message(self, format: str, *args: Any) -> None:
        """Route request logs through logging instead of stderr writes."""
        LOGGER.info(format % args)

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        """Serialize one JSON response with explicit UTF-8 bytes."""
        body = json.dumps(payload, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, payload: str, status: int = 200) -> None:
        """Serve one HTML document with explicit UTF-8 bytes."""
        body = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        """Parse a bounded JSON request body or raise the error to report."""
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            raise HttpError(400, "Content-Length is not valid.") from None
        if length > MAX_BODY_BYTES:
            raise HttpError(413, "Request body is too large.")
        try:
            raw = self.rfile.read(length) if length else b""
            parsed = json.loads(raw or b"null")
        except ValueError:
            raise HttpError(400, "Request body is not valid JSON.") from None
        if not isinstance(parsed, dict):
            raise HttpError(400, "Request body must be a JSON object.")
        return parsed

    def do_GET(self) -> None:
        """Route page, run, demo, and report reads."""
        try:
            path = urlsplit(self.path).path
            if path in {"/", "/index.html"}:
                self._send_html(load_page())
            elif path == "/api/demo":
                self._send_json(
                    {
                        "questions": DEMO_QUESTIONS,
                        "runs": latest_demo_runs(self.config.runs_dir),
                    }
                )
            elif path == "/api/runs":
                self._send_json({"runs": list_runs(self.config.runs_dir)})
            elif path.startswith("/api/run/"):
                run_id = unquote(path[len("/api/run/") :])
                self._send_json(load_run(run_id, self.config.runs_dir))
            elif path.startswith("/api/report/"):
                run_id = unquote(path[len("/api/report/") :])
                load_run(run_id, self.config.runs_dir)
                report = write_report([run_id], self.config.runs_dir)
                self._send_html(report.read_text(encoding="utf-8"))
            else:
                self._send_json({"error": "Unknown demo route."}, 404)
        except HttpError as exc:
            self._send_json({"error": str(exc)}, exc.status)
        except (ModelError, OSError) as exc:
            LOGGER.error(f"Demo GET failed: {exc.__class__.__name__}.")
            self._send_json({"error": str(exc)}, 400)

    def do_POST(self) -> None:
        """Route live answers and offline revisions."""
        try:
            path = urlsplit(self.path).path
            if path == "/api/answer":
                self._send_json(self._answer(self._read_json()))
            elif path == "/api/revise":
                self._send_json(self._revise(self._read_json()))
            else:
                self._send_json({"error": "Unknown demo route."}, 404)
        except HttpError as exc:
            self._send_json({"error": str(exc)}, exc.status)
        except ModelError as exc:
            self._send_json({"error": str(exc)}, 400)
        except Exception as exc:  # Live inference can fail in provider-specific ways.
            LOGGER.error(f"Demo POST failed with {exc.__class__.__name__}.")
            self._send_json({"error": "The request failed; check the server log."}, 502)

    def _answer(self, body: dict[str, Any]) -> dict[str, Any]:
        """Run the normal answer workflow for one posted question."""
        question = body.get("question")
        if not isinstance(question, str) or not question.strip():
            raise HttpError(400, "Provide a question.")
        if len(question) > MAX_QUERY_CHARS:
            raise HttpError(400, "Question exceeds the supported length.")
        fill_in = body.get("fill_in_assumptions", False)
        if not isinstance(fill_in, bool):
            raise HttpError(400, "fill_in_assumptions must be true or false.")
        registry = Registry(self.config.registry_path)
        return answer(registry, question.strip(), fill_in)

    def _revise(self, body: dict[str, Any]) -> dict[str, Any]:
        """Revise one saved run's inputs or model revisions, offline."""
        run_id = body.get("run_id")
        if not isinstance(run_id, str) or not run_id.strip():
            raise HttpError(400, "Provide a run_id.")
        sets = body.get("sets", [])
        models = body.get("models", [])
        if (
            not isinstance(sets, list)
            or not all(isinstance(item, str) for item in sets)
            or not isinstance(models, list)
            or not all(isinstance(item, str) for item in models)
        ):
            raise HttpError(400, "sets and models must be arrays of strings.")
        load_run(run_id.strip(), self.config.runs_dir)
        registry = Registry(self.config.registry_path)
        return revise_run(run_id.strip(), sets, models, registry, self.config.runs_dir)


def create_server(
    config: ServerConfig, host: str = "127.0.0.1", port: int = 8000
) -> DemoServer:
    """Bind the demo server without serving yet, so tests can drive it."""
    return DemoServer((host, port), config)


def serve(config: ServerConfig, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Serve the demo page until interrupted."""
    server = create_server(config, host, port)
    print(
        f"Connected Models demo: open http://{host}:{server.server_port}/ in a browser."
    )
    print("Press Ctrl+C to stop; runs save under .runs/ as usual.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")
