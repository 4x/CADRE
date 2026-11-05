"""CLI .env defaults: a working-directory .env fills absent variables."""

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

from connected_models import __main__ as cli
from connected_models.__main__ import load_dotenv

from .support import scratch_directory


class DotenvTests(unittest.TestCase):
    """The CLI reads .env by default without overriding the real environment."""

    def test_missing_file_is_a_no_op(self) -> None:
        """No .env means nothing loads and nothing raises."""
        with scratch_directory() as workspace:
            with mock.patch.dict(os.environ, {}, clear=True):
                loaded = load_dotenv(Path(workspace) / ".env")
        self.assertEqual(loaded, {})
        self.assertNotIn("CADRE_ALLOW_LLM_STEPS", os.environ)

    def test_fills_absent_variables_only(self) -> None:
        """Comments, quotes, export prefix and blanks parse; exports win."""
        with scratch_directory() as workspace:
            env_file = Path(workspace) / ".env"
            env_file.write_text(
                "# comment line\n"
                "\n"
                "CADRE_ALLOW_LLM_STEPS=1\n"
                "FILL_IN_ASSUMPTIONS='yes'\n"
                'LLM="probe-model"\n'
                "export META_API_KEY=probe-key\n"
                "MALFORMED LINE WITHOUT EQUALS\n",
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {"FILL_IN_ASSUMPTIONS": "0"}, clear=True):
                loaded = load_dotenv(env_file)
                self.assertEqual(
                    loaded,
                    {
                        "CADRE_ALLOW_LLM_STEPS": "1",
                        "LLM": "probe-model",
                        "META_API_KEY": "probe-key",
                    },
                )
                self.assertEqual(os.environ["CADRE_ALLOW_LLM_STEPS"], "1")
                self.assertEqual(os.environ["LLM"], "probe-model")
                self.assertEqual(os.environ["FILL_IN_ASSUMPTIONS"], "0")
                self.assertNotIn("MALFORMED LINE WITHOUT EQUALS", os.environ)


class NoDotenvFlagTests(unittest.TestCase):
    """--no-dotenv restores the no-.env opt-out per invocation."""

    def run_main(self, argv: list[str]) -> tuple[int, mock.Mock]:
        """Run main against an invalid run id; fails fast with no side effects."""
        with (
            mock.patch.object(cli, "load_dotenv") as loader,
            mock.patch.object(sys, "argv", argv),
        ):
            code = cli.main()
        return code, loader

    def test_flag_skips_dotenv_loading(self) -> None:
        """--no-dotenv leaves the process environment exactly alone."""
        code, loader = self.run_main(
            ["connected-models", "--no-dotenv", "inspect", "not-a-uuid"]
        )
        self.assertEqual(code, 1)
        loader.assert_not_called()

    def test_default_loads_dotenv(self) -> None:
        """Without the flag the working-directory .env still loads."""
        code, loader = self.run_main(["connected-models", "inspect", "not-a-uuid"])
        self.assertEqual(code, 1)
        loader.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
