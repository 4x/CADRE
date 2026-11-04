"""System-prompt loading from editable files."""

import unittest

from connected_models.contracts import ModelError
from connected_models.inference import load_prompt


class PromptTests(unittest.TestCase):
    """Each shipped prompt loads with its load-bearing instructions intact."""

    def test_shipped_prompts_load_with_key_instructions(self) -> None:
        """Fail closed on drift that would silently change model behavior."""
        expectations = {
            "answer-question.md": (
                "backward chaining",
                "__output__",
                "EXACT numeric literal",
                "never fill a graph binding with an estimate silently",
                "fewest gaps",
                "match what the question asked for",
                'set branch to "all"',
                "bracketed bisection",
            ),
            "answer-fill-in-assumptions.md": (
                "assumed fact",
                "implying",
                "Never assume the requested unknown",
                "Prefer FEWER assumptions",
            ),
            "offline-model-extraction.md": (
                "offline model curator",
                "never suppress these",
            ),
            "answer-repair.md": (
                "Repair round",
                "machine_error",
                "complete fresh proposal",
                "do not repeat a failing graph",
                "never reinterpret",
            ),
            "direct-answer.md": ("directly", "no tools", "no catalog"),
        }
        for filename, phrases in expectations.items():
            with self.subTest(prompt=filename):
                content = load_prompt(filename)
                for phrase in phrases:
                    self.assertIn(phrase, content)

    def test_prompt_loader_rejects_bad_filenames(self) -> None:
        """Only plain Markdown filenames inside prompts/ are loadable."""
        for filename in ("../inference.toml", "subdir/prompt.md", "prompt.txt", ""):
            with self.subTest(filename=filename), self.assertRaises(ModelError):
                load_prompt(filename)
        with self.assertRaises(ModelError):
            load_prompt("no-such-prompt.md")
