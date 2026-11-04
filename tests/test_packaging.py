"""Installed-package integrity: version, markers, and bundled resources."""

import unittest
from importlib.metadata import version
from importlib.resources import files

from connected_models import __version__


class PackagingTests(unittest.TestCase):
    """The distribution carries one version and its runtime resources."""

    def test_version_matches_distribution(self) -> None:
        """__version__ is single-sourced from the installed metadata."""
        self.assertEqual(__version__, version("connected-models"))

    def test_typed_marker_and_resources_ship(self) -> None:
        """Type marker, prompts, and source packet resolve inside the package."""
        root = files("connected_models")
        self.assertTrue(root.joinpath("py.typed").is_file())
        self.assertTrue(
            root.joinpath("prompts").joinpath("answer-question.md").is_file()
        )
        self.assertTrue(
            root.joinpath("data").joinpath("nist-uniform-present-value.json").is_file()
        )
