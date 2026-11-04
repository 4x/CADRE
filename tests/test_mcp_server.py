"""MCP server: handshake, tool surface, and offline calls without a client."""

import io
import json
import os
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from connected_models.demo_seed import seed_demo
from connected_models.mcp_server import PROTOCOL_VERSIONS, handle_message, run_stdio
from connected_models.registry import Registry
from connected_models.serve import ServerConfig

from .support import scratch_directory


def seed_workspace(workspace: str) -> tuple[ServerConfig, dict[str, Any]]:
    """Seed demo state under scratch and point a server config at it."""
    runs = Path(workspace)
    registry = Registry(runs / "models.sqlite3")
    seeded = seed_demo(registry, runs)
    return ServerConfig(runs / "models.sqlite3", runs), seeded


def call_tool(
    config: ServerConfig, name: str, arguments: dict[str, Any], identifier: int = 1
) -> dict[str, Any]:
    """Invoke one MCP tool and return its unwrapped result object."""
    reply = handle_message(
        {
            "jsonrpc": "2.0",
            "id": identifier,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
        config,
    )
    assert reply is not None
    return reply["result"]  # type: ignore[no-any-return]


def result_text(result: dict[str, Any]) -> str:
    """Read the single text block of a tool result."""
    return str(result["content"][0]["text"])


class McpServerTests(unittest.TestCase):
    """The stdio server speaks JSON-RPC and honors offline tool semantics."""

    def test_initialize_negotiates_and_announces_tools(self) -> None:
        """Known versions echo; unknown versions fall back to the newest."""
        with scratch_directory() as workspace:
            config, _ = seed_workspace(workspace)
            reply = handle_message(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {"protocolVersion": "2025-03-26"},
                },
                config,
            )
            assert reply is not None
            self.assertEqual(reply["result"]["protocolVersion"], "2025-03-26")
            self.assertEqual(reply["result"]["serverInfo"]["name"], "connected-models")
            self.assertIn("tools", reply["result"]["capabilities"])
            fallback = handle_message(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "initialize",
                    "params": {"protocolVersion": "9999-99-99"},
                },
                config,
            )
            assert fallback is not None
            self.assertEqual(
                fallback["result"]["protocolVersion"], PROTOCOL_VERSIONS[0]
            )

    def test_tools_list_exposes_seven_schemas(self) -> None:
        """Every tool carries a name, description, and input schema."""
        with scratch_directory() as workspace:
            config, _ = seed_workspace(workspace)
            reply = handle_message(
                {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
                config,
            )
            assert reply is not None
            tools = reply["result"]["tools"]
            self.assertEqual(
                {tool["name"] for tool in tools},
                {
                    "answer",
                    "inspect",
                    "revise",
                    "replay",
                    "report",
                    "units",
                    "registry_list",
                },
            )
            for tool in tools:
                self.assertTrue(tool["description"])
                self.assertEqual(tool["inputSchema"]["type"], "object")

    def test_protocol_errors_and_notifications(self) -> None:
        """Malformed traffic errors; notifications and ping behave."""
        with scratch_directory() as workspace:
            config, _ = seed_workspace(workspace)
            self.assertIsNone(
                handle_message(
                    {
                        "jsonrpc": "2.0",
                        "method": "notifications/initialized",
                        "params": {},
                    },
                    config,
                )
            )
            unknown = handle_message(
                {"jsonrpc": "2.0", "id": 7, "method": "resources/list", "params": {}},
                config,
            )
            assert unknown is not None
            self.assertEqual(unknown["error"]["code"], -32601)
            shape = handle_message(["not", "an", "object"], config)
            assert shape is not None
            self.assertEqual(shape["error"]["code"], -32600)
            ping = handle_message(
                {"jsonrpc": "2.0", "id": 8, "method": "ping", "params": {}}, config
            )
            assert ping is not None
            self.assertEqual(ping["result"], {})

    def test_offline_tools_read_and_revise_seed(self) -> None:
        """Units, registry, inspect, revise, replay, and report all work offline."""
        with scratch_directory() as workspace:
            config, seeded = seed_workspace(workspace)
            units = call_tool(config, "units", {"filter": "kWh"})
            self.assertNotIn("isError", units)
            self.assertIn("kWh", result_text(units))
            admissions = json.loads(result_text(call_tool(config, "registry_list", {})))
            self.assertEqual(len(admissions), 5)
            self.assertEqual(
                admissions["heat-to-electricity@1"]["reviewer"], "demo-seed"
            )
            run_id = seeded["runs"]["operating-cost"]["run_id"]
            manifest = json.loads(
                result_text(call_tool(config, "inspect", {"run_id": run_id}))
            )
            self.assertEqual(manifest["run_id"], run_id)
            revised = json.loads(
                result_text(
                    call_tool(
                        config,
                        "revise",
                        {"run_id": run_id, "sets": ["upgrade-energy.performance=2"]},
                    )
                )
            )
            self.assertEqual(revised["status"], "completed")
            self.assertEqual(revised["outputs"]["upgrade-cost"]["amount"], 1800)
            replayed = json.loads(
                result_text(call_tool(config, "replay", {"run_id": run_id}))
            )
            self.assertTrue(replayed["matched"])
            reported = json.loads(
                result_text(call_tool(config, "report", {"run_ids": [run_id]}))
            )
            self.assertTrue(Path(reported["report"]).is_file())

    def test_tool_failures_stay_inside_results(self) -> None:
        """Unknown tools and bad runs report isError, not protocol errors."""
        with scratch_directory() as workspace:
            config, _ = seed_workspace(workspace)
            unknown = call_tool(config, "teleport", {})
            self.assertTrue(unknown.get("isError"))
            missing = call_tool(
                config,
                "inspect",
                {"run_id": "00000000-0000-0000-0000-000000000000"},
            )
            self.assertTrue(missing.get("isError"))

    def test_answer_without_key_blocks_without_network(self) -> None:
        """A missing key yields a blocked record, saved under scratch only."""
        with scratch_directory() as workspace:
            config, _ = seed_workspace(workspace)
            runs = Path(workspace)
            with (
                mock.patch("connected_models.workflows.RUNS_PATH", runs),
                mock.patch.dict(os.environ, clear=False),
            ):
                os.environ.pop("META_API_KEY", None)
                result = call_tool(
                    config, "answer", {"question": "What is 1 kWh in USD?"}
                )
            record = json.loads(result_text(result))
            self.assertEqual(record["status"], "blocked")
            self.assertIn("META_API_KEY", record["error"])

    def test_stdio_loop_answers_until_eof(self) -> None:
        """The stdio loop replies per line, skips notifications, ends on EOF."""
        with scratch_directory() as workspace:
            config, _ = seed_workspace(workspace)
            reader = io.StringIO(
                '{"jsonrpc": "2.0", "id": 1, "method": "initialize", '
                '"params": {"protocolVersion": "2025-06-18"}}\n'
                '{"jsonrpc": "2.0", "method": "notifications/initialized"}\n'
                '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}\n'
                "{oops\n"
            )
            writer = io.StringIO()
            run_stdio(config, reader, writer)
            replies = [json.loads(line) for line in writer.getvalue().splitlines()]
            self.assertEqual([reply.get("id") for reply in replies], [1, 2, None])
            self.assertEqual(replies[2]["error"]["code"], -32700)
