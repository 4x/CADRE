"""Lexical retrieval: ranking, field weights, expansion, caps, determinism."""

import unittest

from connected_models.contracts import Model, Port
from connected_models.retrieval import (
    RETRIEVAL_VERSION,
    build_index,
    neighbors_from_audit,
    retrieve,
    tokenize,
)


def toy_model(
    id: str,
    inputs: dict[str, Port],
    output: Port,
    assumptions: tuple[str, ...] = (),
    guards: tuple[str, ...] = (),
) -> Model:
    """Build a minimal catalog model with distinctive vocabulary per field."""
    return Model(id, "1", inputs, output, "x + 1", guards, "Test-only.", assumptions)


ALPHA = toy_model(
    "alpha--heat-flow",
    {"hot": Port("temperature", "K", "alpha furnace context")},
    Port("heat", "J", "alpha furnace context"),
    ("Conduction moves heat downhill.",),
)
BETA = toy_model(
    "beta--cold-flow",
    {"cold": Port("temperature", "K", "beta cryostat context")},
    Port("coldness", "J", "beta cryostat context"),
    ("Heat flow language appears here repeatedly without endorsement.",),
)
GAMMA = toy_model(
    "gamma--pump",
    {"work": Port("heat", "J", "gamma pump context")},
    Port("pressure", "Pa", "gamma pump context"),
    ("Unrelated test filler.",),
)


class RetrievalTests(unittest.TestCase):
    """Retrieval is a pure deterministic function of question, models and edges."""

    def test_id_and_output_meaning_outweigh_assumption_mentions(self) -> None:
        """Field weights beat raw mention counts: id x3, output meaning x3, assumptions x0.5."""
        index = build_index({"a": ALPHA, "b": BETA})
        result = retrieve("heat flow", index, k=2)
        self.assertEqual(result.keys[0], "a")
        self.assertEqual(result.version, RETRIEVAL_VERSION)

    def test_output_meaning_beats_input_meaning(self) -> None:
        """A model producing heat outranks one merely consuming it."""
        index = build_index({"consumer": GAMMA, "producer": ALPHA})
        result = retrieve("heat", index, k=2)
        self.assertEqual(result.keys[0], "producer")

    def test_ties_break_by_key_deterministically(self) -> None:
        """Equal scores order by model key; repeats are identical."""
        twin = toy_model(
            "alpha--heat-flow",
            {"hot": Port("temperature", "K", "alpha furnace context")},
            Port("heat", "J", "alpha furnace context"),
            ("Conduction moves heat downhill.",),
        )
        index = build_index({"b-key": ALPHA, "a-key": twin})
        first = retrieve("heat flow furnace", index, k=2)
        second = retrieve("heat flow furnace", index, k=2)
        self.assertEqual(first.keys, ("a-key", "b-key"))
        self.assertEqual(first, second)

    def test_expansion_reaches_zero_overlap_neighbors(self) -> None:
        """A neighbor with no shared vocabulary joins via edges; strangers stay out."""
        index = build_index({"a": ALPHA, "b": BETA, "c": GAMMA})
        neighbors = {"a": {"c"}, "c": {"a"}, "b": set()}
        result = retrieve("furnace conduction", index, neighbors, k=1)
        self.assertEqual(result.seeds, ("a",))
        self.assertIn("c", result.keys)
        self.assertNotIn("b", result.keys)
        self.assertEqual(result.expanded, ("c",))

    def test_cap_trims_expansion_never_seeds(self) -> None:
        """Overflow drops the lowest-scoring expanded models first."""
        index = build_index({"a": ALPHA, "b": BETA, "c": GAMMA})
        neighbors = {"a": {"b", "c"}, "b": {"a"}, "c": {"a"}}
        result = retrieve("furnace", index, neighbors, k=1, cap=2)
        self.assertEqual(result.seeds, ("a",))
        self.assertEqual(len(result.keys), 2)
        self.assertEqual(len(result.dropped), 1)
        self.assertIn(result.dropped[0], ("b", "c"))

    def test_empty_question_is_deterministic_key_order(self) -> None:
        """No tokens still yields a stable subset, ordered by key."""
        index = build_index({"b": BETA, "a": ALPHA, "c": GAMMA})
        first = retrieve("", index, k=2)
        self.assertEqual(first.keys, ("a", "b"))
        self.assertEqual(first, retrieve("", index, k=2))
        self.assertEqual(retrieve("   ", index, k=2).keys, ("a", "b"))

    def test_tokenizer_drops_stopwords_and_singles(self) -> None:
        """Indexing keeps content tokens; 'what is the Q' leaves Q-like words."""
        self.assertEqual(tokenize("What is the heat flow?"), ["heat", "flow"])
        self.assertEqual(tokenize("a b c dd"), ["dd"])
        self.assertEqual(tokenize(""), [])

    def test_neighbors_reduce_audit_edges(self) -> None:
        """Audit from/to pairs become undirected neighbor sets."""
        audit = {"edges": [{"from": "a", "to": "b"}, {"from": "b", "to": "c"}]}
        self.assertEqual(
            neighbors_from_audit(audit), {"a": {"b"}, "b": {"a", "c"}, "c": {"b"}}
        )
        self.assertEqual(neighbors_from_audit({}), {})
