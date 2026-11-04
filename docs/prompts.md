# Editable LLM prompts

The five system prompts the application sends to the model live as plain Markdown files in `src/connected_models/prompts/`, so you can read and tune them without touching code. They ship as package data and load at request time through `connected_models.inference.load_prompt`.

| File | Used by | Request name |
| --- | --- | --- |
| `answer-question.md` | `answer`, first attempt | AnswerQuestionGrounded |
| `answer-fill-in-assumptions.md` | `answer` with fill-in enabled, appended | AnswerQuestionGrounded |
| `answer-repair.md` | `answer` repair attempts, appended with the machine error | AnswerQuestionGrounded |
| `direct-answer.md` | `compare` direct route, plain text | DirectAnswer |
| `offline-model-extraction.md` | `curate` | OfflineModelExtraction |

Each file holds exactly one prompt: the whole file (minus leading/trailing blank lines) becomes the system message. Blank lines separate paragraphs; do not hard-wrap inside a paragraph, since every line break is sent to the model.

The structured-output schemas and the user messages (the question, the trimmed model catalog, the source packet) stay in code in `src/connected_models/workflows.py`; they are data contracts, not prose. Fact validation stays in `src/connected_models/query_inputs.py`.

## Editing rules

- Keep the response contract: the answer call must still return facts/issues plus a status/graph/reason/clarifications object, the curator an expression/guards/assumptions/source-map object. The code validates the shape and rejects anything else.
- Stay within 32 KiB per file; larger files are refused.
- Files must be UTF-8, non-empty, and named `*.md` directly in `src/connected_models/prompts/`. Missing or unreadable files fail the request with an error instead of a silent fallback prompt.
- Prompt edits take effect on the next request. Saved runs keep the model outputs and bindings they were executed with; rerunning an old question after an edit may compose a different graph.
