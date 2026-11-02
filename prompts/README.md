# Editable LLM prompts

The three system prompts the application sends to the model live here as plain Markdown files, so you can read and tune them without touching code. The scripts load them at request time through `connected_models.inference.load_prompt`.

| File | Used by | Request name |
| --- | --- | --- |
| `parse-query-inputs.md` | `answer`, first call | ParseQueryInputs |
| `compose-grounded-models.md` | `answer`, second call | ComposeQueryGroundedModels |
| `offline-model-extraction.md` | `curate` | OfflineModelExtraction |

Each file holds exactly one prompt: the whole file (minus leading/trailing blank lines) becomes the system message. Blank lines separate paragraphs; do not hard-wrap inside a paragraph, since every line break is sent to the model.

The structured-output schemas and the user messages (the question, the model catalog, the source packet) stay in code in `connected_models/workflows.py` and `connected_models/query_inputs.py`; they are data contracts, not prose.

## Editing rules

- Keep the response contract: the parser must still return facts/issues, the composer a status/graph/reason/clarifications object, the curator an expression/guards/assumptions/source-map object. The code validates the shape and rejects anything else.
- Stay within 32 KiB per file; larger files are refused.
- Files must be UTF-8, non-empty, and named `*.md` directly in this directory. Missing or unreadable files fail the request with an error instead of a silent fallback prompt.
- Prompt edits take effect on the next request. Saved runs keep the model outputs and bindings they were executed with; rerunning an old question after an edit may compose a different graph.
