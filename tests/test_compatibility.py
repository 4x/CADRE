"""Offline chain-compatibility audit: edges, near misses, and isolates."""

import unittest

from connected_models.compatibility import audit_pairs
from connected_models.contracts import Model, Port


def _model(key: str, inputs: dict[str, Port], output: Port) -> Model:
    """Build a minimal structural model for audit-shape testing."""
    return Model(id=key.split("@")[0], version="r1.runtime1", inputs=inputs,
                 output=output, expression="x", guards=(), source="test",
                 assumptions=("test",), status="fixture", families={})


class CompatibilityAuditTests(unittest.TestCase):
    """Edges need exact meaning/context pairs; near misses name the gap."""

    def test_edges_and_near_misses(self) -> None:
        """Matching ports connect; same-meaning context splits are reported."""
        first = Port("mass", "kg", "same sample")
        models = {
            "a@r1": _model("a@r1", {"x": Port("length", "m", "same rod")}, first),
            "b@r1": _model("b@r1", {"m": Port("mass", "g", "same sample")},
                           Port("volume", "m3", "same sample")),
            "c@r1": _model("c@r1", {"m": Port("mass", "kg", "other sample")},
                           Port("volume", "m3", "other sample")),
        }
        report = audit_pairs(models)
        self.assertEqual(report["models"], 3)
        forwards = [edge for edge in report["edges"] if edge["view"] == "forward"]
        self.assertEqual(len(forwards), 1)
        self.assertEqual(forwards[0]["from"], "a@r1")
        self.assertEqual(forwards[0]["to"], "b@r1")
        self.assertEqual(report["near_miss_count"], 2)
        miss = next(item for item in report["near_misses"]
                    if item["from_context"] == "same sample")
        self.assertEqual(miss["meaning"], "mass")
        self.assertIn("a@r1[forward]->c@r1.m", miss["pairs"])
        self.assertEqual(report["isolates"], [])
        self.assertIn("structural only", report["limits"])

    def test_isolates_and_inverse_views(self) -> None:
        """Unconnected models are listed; inverse views add structural edges."""
        models = {
            "a@r1": _model("a@r1", {"x": Port("length", "m", "same rod")},
                           Port("mass", "kg", "same sample")),
            "b@r1": _model("b@r1", {"x": Port("length", "m", "same rod")},
                           Port("volume", "m3", "same vat")),
        }
        report = audit_pairs(models)
        views = {(edge["from"], edge["view"], edge["to"]) for edge in report["edges"]}
        self.assertIn(("a@r1", "solve_for:x", "b@r1"), views)
        self.assertNotIn(("a@r1", "forward", "b@r1"), views)
        self.assertEqual(report["isolates"], [])
