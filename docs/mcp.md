# MCP server

Any MCP client can drive Connected Models as a stdio server — no SDK, no new
dependencies: the protocol is newline-delimited JSON-RPC over the standard
library. Seven tools mirror the CLI workflows:

| Tool | Effect |
| --- | --- |
| `answer` | Answer a question (live inference, writes a run) |
| `inspect` | Return a saved run's full manifest |
| `revise` | Revise inputs/models offline, saving a new run |
| `replay` | Re-execute a run against pinned models, saving nothing |
| `report` | Export runs to standalone HTML evidence |
| `units` | Browse canonical units, dimensions, aliases |
| `registry_list` | List eligible revisions with review attribution |

## Register the server

Run the client from the repo root (registry, runs, and `inference.toml`
resolve from the working directory) with this stdio command:

```powershell
uv run --env-file .env connected-models mcp
```

`--env-file .env` matters only for `answer`; the other six tools are offline.
Stdout carries only JSON-RPC — diagnostics go to stderr — so the command is
safe to embed in any client's `mcpServers` stdio entry with `cwd` set to the
checkout.

Tool failures arrive inside the result (`isError: true`) with the same
user-facing messages as the CLI; protocol errors use standard JSON-RPC codes.
`answer` returns the compact receipt (status, outputs, assumptions,
clarifications, error, `saved_path`); call `inspect` for the full manifest.

## Verify without a client

Pipe four lines and confirm three replies (the notification answers
nothing) plus a clean exit:

```powershell
@('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}', '{"jsonrpc":"2.0","method":"notifications/initialized"}', '{"jsonrpc":"2.0","id":2,"method":"tools/list"}', '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"units","arguments":{"filter":"USD"}}}') | uv run --no-env-file connected-models mcp 2>$null
```

`registry_list` shows what `answer` can compose; an empty map means seed or
curate first (see [demo.md](demo.md) for the offline `demo-seed`).
