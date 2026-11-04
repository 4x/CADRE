"""Model Context Protocol server over newline-delimited stdio, stdlib only.

Any MCP client can register `connected-models mcp` as a stdio server and call
the same workflows as the CLI: answer questions, inspect evidence, revise
scenarios, replay runs, export reports, and browse units and admissions.
Stdout carries only JSON-RPC; diagnostics go to stderr via logging.
"""

from __future__ import annotations

import json
import logging
import sys
from collections.abc import Callable
from typing import Any, TextIO

from . import __version__
from .contracts import ModelError, describe_units
from .query_inputs import MAX_QUERY_CHARS
from .registry import Registry
from .reports import write_report
from .revisions import replay_run, revise_run
from .serve import HttpError, ServerConfig, load_run
from .workflows import answer

LOGGER = logging.getLogger("connected_models.mcp")
SERVER_NAME = "connected-models"
PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")

ANSWER_KEYS = (
    "run_id",
    "status",
    "outputs",
    "assumptions",
    "clarifications",
    "solve_diagnostic",
    "error",
    "saved_path",
)
REVISE_KEYS = (
    "run_id",
    "status",
    "revised_from",
    "revision",
    "outputs",
    "diff",
    "error",
    "saved_path",
)


class ToolError(Exception):
    """A tool failure reported inside a result, never as a protocol error."""


def _tool_text(payload: Any) -> str:
    """Serialize one tool payload to the text of a content block."""
    return json.dumps(payload, indent=2, allow_nan=False)


def _call_answer(arguments: dict[str, Any], config: ServerConfig) -> str:
    """Answer one self-contained question through the normal workflow."""
    question = arguments.get("question")
    if not isinstance(question, str) or not question.strip():
        raise ToolError("Provide a question.")
    if len(question) > MAX_QUERY_CHARS:
        raise ToolError("Question exceeds the supported length.")
    fill_in = arguments.get("fill_in_assumptions", False)
    if not isinstance(fill_in, bool):
        raise ToolError("fill_in_assumptions must be true or false.")
    registry = Registry(config.registry_path)
    record = answer(registry, question.strip(), fill_in)
    return _tool_text({key: record.get(key) for key in ANSWER_KEYS})


def _call_inspect(arguments: dict[str, Any], config: ServerConfig) -> str:
    """Return one saved run's complete manifest."""
    run_id = arguments.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ToolError("Provide a run_id.")
    try:
        return _tool_text(load_run(run_id.strip(), config.runs_dir))
    except HttpError as exc:
        raise ToolError(str(exc)) from None


def _call_revise(arguments: dict[str, Any], config: ServerConfig) -> str:
    """Revise one saved run's inputs or model revisions, offline."""
    run_id = arguments.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ToolError("Provide a run_id.")
    sets = arguments.get("sets", [])
    models = arguments.get("models", [])
    if (
        not isinstance(sets, list)
        or not all(isinstance(item, str) for item in sets)
        or not isinstance(models, list)
        or not all(isinstance(item, str) for item in models)
    ):
        raise ToolError("sets and models must be arrays of strings.")
    try:
        load_run(run_id.strip(), config.runs_dir)
        registry = Registry(config.registry_path)
        record = revise_run(run_id.strip(), sets, models, registry, config.runs_dir)
    except HttpError as exc:
        raise ToolError(str(exc)) from None
    return _tool_text({key: record.get(key) for key in REVISE_KEYS})


def _call_replay(arguments: dict[str, Any], config: ServerConfig) -> str:
    """Re-execute one saved run against its pinned models; saves nothing."""
    run_id = arguments.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ToolError("Provide a run_id.")
    try:
        load_run(run_id.strip(), config.runs_dir)
        return _tool_text(replay_run(run_id.strip(), config.runs_dir))
    except HttpError as exc:
        raise ToolError(str(exc)) from None


def _call_report(arguments: dict[str, Any], config: ServerConfig) -> str:
    """Export up to eight saved runs to one standalone HTML report."""
    run_ids = arguments.get("run_ids")
    if (
        not isinstance(run_ids, list)
        or not run_ids
        or not all(isinstance(item, str) for item in run_ids)
    ):
        raise ToolError("Provide run_ids as a non-empty array of strings.")
    try:
        for run_id in run_ids:
            load_run(run_id, config.runs_dir)
        report = write_report(run_ids, config.runs_dir)
    except HttpError as exc:
        raise ToolError(str(exc)) from None
    return _tool_text({"report": str(report), "runs": run_ids})


def _call_units(arguments: dict[str, Any], config: ServerConfig) -> str:
    """Describe canonical units with dimensions, scales, and aliases."""
    del config
    unit_filter = arguments.get("filter", "")
    if not isinstance(unit_filter, str):
        raise ToolError("filter must be a string.")
    return describe_units(unit_filter)


def _call_registry_list(arguments: dict[str, Any], config: ServerConfig) -> str:
    """List eligible model revisions with their review attribution."""
    del arguments
    _, admissions = Registry(config.registry_path).snapshot()
    return _tool_text(
        {
            key: {
                "reviewer": admission.get("reviewer"),
                "notes": admission.get("notes"),
                "reviewed": admission.get("reviewed"),
            }
            for key, admission in sorted(admissions.items())
        }
    )


_TOOL_CALLS: dict[str, Callable[[dict[str, Any], ServerConfig], str]] = {
    "answer": _call_answer,
    "inspect": _call_inspect,
    "revise": _call_revise,
    "replay": _call_replay,
    "report": _call_report,
    "units": _call_units,
    "registry_list": _call_registry_list,
}

TOOLS: list[dict[str, Any]] = [
    {
        "name": "answer",
        "description": (
            "Answer a self-contained quantitative question by composing reviewed "
            "stored models and executing them deterministically. Put every number, "
            "unit, and assumption in the question text. Statuses: completed, "
            "needs-input (ask the listed clarifications), blocked (no model), "
            "rejected. Uses live inference and writes a saved run."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "fill_in_assumptions": {
                    "type": "boolean",
                    "description": (
                        "Explicit opt-in: let the composer supply question-implied "
                        "values as documented assumptions. Default false."
                    ),
                },
            },
            "required": ["question"],
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": True},
    },
    {
        "name": "inspect",
        "description": (
            "Return one saved run's complete manifest: composition, steps, "
            "outputs, pinned models, admissions, and provenance."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}},
            "required": ["run_id"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "revise",
        "description": (
            "Revise one saved run's direct inputs (node.input=amount in the "
            "declared unit) or substitute node model revisions, then rerun "
            "offline. The original run is preserved; the revision saves as a "
            "new run linked with revised_from."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string"},
                "sets": {"type": "array", "items": {"type": "string"}},
                "models": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["run_id"],
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": False},
    },
    {
        "name": "replay",
        "description": (
            "Re-execute one saved run's graph against its pinned models and "
            "compare status, error, and outputs exactly. Saves nothing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}},
            "required": ["run_id"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "report",
        "description": (
            "Export one to eight saved runs to a standalone HTML evidence "
            "report, including a what-changed comparison for multiple runs."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"run_ids": {"type": "array", "items": {"type": "string"}}},
            "required": ["run_ids"],
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": False},
    },
    {
        "name": "units",
        "description": (
            "List canonical units with dimensions, scales, and aliases, "
            "optionally filtered by substring."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"filter": {"type": "string"}},
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "registry_list",
        "description": (
            "List eligible model revisions with reviewer, notes, and review "
            "time. Shows what the answer tool can compose."
        ),
        "inputSchema": {"type": "object", "properties": {}},
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
]


def _error(identifier: Any, code: int, message: str) -> dict[str, Any]:
    """Build one JSON-RPC error response."""
    return {
        "jsonrpc": "2.0",
        "id": identifier,
        "error": {"code": code, "message": message},
    }


def _handle_initialize(params: dict[str, Any]) -> dict[str, Any]:
    """Negotiate the protocol version and announce tool capability."""
    requested = params.get("protocolVersion")
    negotiated = requested if requested in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0]
    return {
        "protocolVersion": negotiated,
        "capabilities": {"tools": {"listChanged": False}},
        "serverInfo": {"name": SERVER_NAME, "version": __version__},
    }


def _handle_tools_call(params: dict[str, Any], config: ServerConfig) -> dict[str, Any]:
    """Run one named tool; failures stay inside the result as isError."""
    name = params.get("name")
    arguments = params.get("arguments", {})
    if not isinstance(name, str) or not isinstance(arguments, dict):
        return {
            "content": [{"type": "text", "text": "name and arguments are required."}],
            "isError": True,
        }
    call = _TOOL_CALLS.get(name)
    if call is None:
        return {
            "content": [{"type": "text", "text": f"Unknown tool {name}."}],
            "isError": True,
        }
    try:
        return {"content": [{"type": "text", "text": call(arguments, config)}]}
    except ToolError as exc:
        return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
    except (ModelError, OSError, ValueError) as exc:
        LOGGER.error(f"Tool {name} failed with {exc.__class__.__name__}.")
        return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
    except Exception as exc:  # Live inference can fail in provider-specific ways.
        LOGGER.error(f"Tool {name} failed with {exc.__class__.__name__}.")
        return {
            "content": [
                {"type": "text", "text": "The request failed; check the server log."}
            ],
            "isError": True,
        }


def handle_message(message: Any, config: ServerConfig) -> dict[str, Any] | None:
    """Handle one parsed JSON-RPC message; None means notification, no reply."""
    if not isinstance(message, dict):
        return _error(None, -32600, "Message must be a JSON-RPC object.")
    if message.get("jsonrpc") != "2.0":
        return _error(message.get("id"), -32600, "Only JSON-RPC 2.0 is supported.")
    method = message.get("method")
    if not isinstance(method, str):
        return _error(message.get("id"), -32600, "Missing method.")
    if "id" not in message:
        return None  # Notifications, including notifications/initialized, get no reply.
    identifier = message.get("id")
    params = message.get("params", {})
    if not isinstance(params, dict):
        return _error(identifier, -32602, "params must be an object.")
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": identifier,
            "result": _handle_initialize(params),
        }
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": identifier, "result": {"tools": TOOLS}}
    if method == "tools/call":
        return {
            "jsonrpc": "2.0",
            "id": identifier,
            "result": _handle_tools_call(params, config),
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": identifier, "result": {}}
    return _error(identifier, -32601, f"Unknown method {method}.")


def _write(writer: TextIO, payload: Any) -> None:
    """Write one newline-delimited JSON-RPC message and flush it."""
    writer.write(json.dumps(payload, allow_nan=False) + "\n")
    writer.flush()


def run_stdio(
    config: ServerConfig,
    reader: TextIO | None = None,
    writer: TextIO | None = None,
) -> None:
    """Serve JSON-RPC over newline-delimited stdio until EOF."""
    inp = reader if reader is not None else sys.stdin
    out = writer if writer is not None else sys.stdout
    for stream in (inp, out):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue  # StringIO test doubles have no encoding to set.
        try:
            reconfigure(encoding="utf-8")
        except ValueError:
            continue  # Closed or detached streams stay as they are.
    LOGGER.info(f"{SERVER_NAME} MCP server {__version__} reading stdio.")
    for line in inp:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except ValueError:
            _write(
                out,
                _error(None, -32700, "Message is not valid JSON."),
            )
            continue
        if isinstance(message, list):
            replies = [
                reply
                for item in message
                if (reply := handle_message(item, config)) is not None
            ]
            if replies:
                _write(out, replies)
        else:
            reply = handle_message(message, config)
            if reply is not None:
                _write(out, reply)
