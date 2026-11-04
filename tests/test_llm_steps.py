"""Partially grounded composition: reviewed models with bounded LLM-filled gaps."""

import json
import os
import unittest
from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from unittest import mock

from connected_models import revisions
from connected_models.contracts import (
    Composition,
    LLMStep,
    Model,
    ModelError,
    Node,
    Port,
    Reference,
    Value,
)
from connected_models.runtime import MAX_LLM_STEPS, compile_graph, execute, save_run
from connected_models.serialization import composition_from_dict
from connected_models.workflows import LLM_STEPS_ENV_VAR, llm_steps_enabled

CONTEXT = "test-only energy flow"


def energy_port() -> Port:
    """Return the shared test port every fixture binding targets."""
    return Port("electricity_consumption", "kWh", CONTEXT)


def doubling_model() -> Model:
    """Return a fixture model that doubles its electricity input."""
    return Model(
        "test-double",
        "r1",
        {"x": energy_port()},
        energy_port(),
        "x + x",
        (),
        "Synthetic test model.",
        ("Synthetic test.",),
    )


def quadrupling_model() -> Model:
    """Return a fixture model that doubles its electricity input again."""
    return Model(
        "test-quadruple",
        "r1",
        {"z": energy_port()},
        energy_port(),
        "z + z",
        (),
        "Synthetic test model.",
        ("Synthetic test.",),
    )


def triple_step(upstream: str) -> LLMStep:
    """Return a step tripling the bound upstream electricity amount."""
    return LLMStep(
        "s1",
        {"y": energy_port()},
        {"y": Reference(upstream)},
        energy_port(),
        "Triple the bound electricity amount.",
    )


def hybrid_graph() -> tuple[Composition, dict[str, Model]]:
    """Build fact to model to step to model coverage over one chain."""
    fact = Value(5.0, energy_port(), "user-scenario", "Synthetic test fact.")
    node_a = Node("nA", "test-double@r1", {"x": fact})
    node_b = Node("nB", "test-quadruple@r1", {"z": Reference("s1")})
    composition = Composition(
        "hybrid-test", (node_a, node_b), ("nB",), "fixture", (triple_step("nA"),)
    )
    catalog = {
        "test-double@r1": doubling_model(),
        "test-quadruple@r1": quadrupling_model(),
    }
    return composition, catalog


def triple_stub(step: LLMStep, values: dict[str, Value]) -> tuple[float, str]:
    """Deterministically triple the bound input for offline tests."""
    return values["y"].amount * 3, "tripled for test"


class HybridCompositionTests(unittest.TestCase):
    """Reviewed models keep their receipts when a step fills one gap."""

    def test_hybrid_chain_is_partial_with_exact_amounts(self) -> None:
        """A fact to model to step to model chain completes partially grounded."""
        composition, catalog = hybrid_graph()
        outcome = execute(composition, catalog, None, triple_stub)
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual(outcome["outputs"]["nB"]["amount"], 60.0)
        self.assertEqual(outcome["grounding"], "partial")
        self.assertEqual(len(outcome["llm_steps"]), 1)
        self.assertFalse(outcome["llm_steps"][0]["carried"])
        step_record = next(
            record for record in outcome["steps"] if record.get("llm_step")
        )
        self.assertEqual(step_record["result"]["origin"], "llm-computed")
        self.assertEqual(step_record["result"]["amount"], 30.0)
        origins = [entry.get("origin") for entry in outcome["steps"][-1]["relies_on"]]
        self.assertIn("llm-computed", origins)

    def test_steps_without_adapter_or_values_are_rejected(self) -> None:
        """Missing computation help fails closed with the flag named."""
        composition, catalog = hybrid_graph()
        outcome = execute(composition, catalog)
        self.assertEqual(outcome["status"], "rejected")
        self.assertIn("CADRE_ALLOW_LLM_STEPS", outcome["error"])

    def test_replay_carries_recorded_values_without_adapter(self) -> None:
        """Replay reuses recorded step amounts instead of re-querying."""
        composition, catalog = hybrid_graph()

        def forbidden(step: LLMStep, values: dict[str, Value]) -> tuple[float, str]:
            """Fail if replay calls back into any step computation."""
            raise AssertionError("replay must not call the adapter")

        outcome = execute(composition, catalog, None, forbidden, {"s1": 30.0})
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual(outcome["outputs"]["nB"]["amount"], 60.0)
        step_record = next(
            record for record in outcome["steps"] if record.get("llm_step")
        )
        self.assertTrue(step_record["llm"]["carried"])
        self.assertIn("Carried recorded", step_record["result"]["evidence"])

    def test_composition_round_trip_preserves_steps(self) -> None:
        """Saved manifests rebuild the same bounded steps."""
        composition, _ = hybrid_graph()
        rebuilt = composition_from_dict(json.loads(json.dumps(asdict(composition))))
        self.assertEqual([step.id for step in rebuilt.llm_steps], ["s1"])
        self.assertEqual(
            rebuilt.llm_steps[0].instruction, "Triple the bound electricity amount."
        )
        self.assertEqual(rebuilt.llm_steps[0].output.meaning, "electricity_consumption")

    def test_compile_refuses_malformed_steps(self) -> None:
        """Caps, identifiers, references, and scalar bindings are enforced."""
        composition, catalog = hybrid_graph()
        tuple_binding: dict[str, Any] = {"y": (Reference("nA"),)}
        cases: list[LLMStep] = [
            LLMStep(
                "s1",
                {"y": energy_port()},
                {"y": Reference("missing")},
                energy_port(),
                "Triple it.",
            ),
            LLMStep(
                "",
                {"y": energy_port()},
                {"y": Reference("nA")},
                energy_port(),
                "Triple it.",
            ),
            LLMStep(
                "s1", {"y": energy_port()}, tuple_binding, energy_port(), "Triple it."
            ),
            LLMStep(
                "s1", {"y": energy_port()}, {"y": Reference("nA")}, energy_port(), "  "
            ),
        ]
        for index, broken in enumerate(cases):
            with self.subTest(case=index):
                patched = Composition(
                    composition.id,
                    composition.nodes,
                    composition.outputs,
                    composition.purpose,
                    (broken,),
                )
                with self.assertRaises(ModelError):
                    compile_graph(patched, catalog)
        dup = (
            triple_step("nA"),
            triple_step("nA"),
        )
        doubled = Composition(
            composition.id, composition.nodes, ("nB",), composition.purpose, dup
        )
        with self.assertRaises(ModelError):
            compile_graph(doubled, catalog)
        many = tuple(
            LLMStep(
                f"s{i}",
                {"y": energy_port()},
                {"y": Reference("nA")},
                energy_port(),
                "Triple it.",
            )
            for i in range(MAX_LLM_STEPS + 1)
        )
        crowded = Composition(
            composition.id, composition.nodes, ("nA",), composition.purpose, many
        )
        with self.assertRaises(ModelError):
            compile_graph(crowded, catalog)

    def test_step_outputs_are_validated(self) -> None:
        """Non-numeric step results reject the run instead of propagating."""

        def bad_nan(step: LLMStep, values: dict[str, Value]) -> tuple[Any, str]:
            """Return a non-finite amount the engine must refuse."""
            return float("nan"), "not a number"

        def bad_text(step: LLMStep, values: dict[str, Value]) -> tuple[Any, str]:
            """Return a non-numeric amount the engine must refuse."""
            return "about thirty", "not a number"

        composition, catalog = hybrid_graph()
        for stub in (bad_nan, bad_text):
            with self.subTest(stub=stub.__name__):
                outcome = execute(composition, catalog, None, stub)
                self.assertEqual(outcome["status"], "rejected")
                self.assertIn("s1", outcome["error"])

    def test_env_flag_parsing(self) -> None:
        """The environment toggle accepts the documented truthy spellings."""
        for truthy in ("1", "true", "TRUE", "yes", "on"):
            self.assertTrue(llm_steps_enabled({"CADRE_ALLOW_LLM_STEPS": truthy}))
        for falsy in ("", "0", "false", "off"):
            self.assertFalse(llm_steps_enabled({"CADRE_ALLOW_LLM_STEPS": falsy}))
        self.assertFalse(llm_steps_enabled({}))

    def test_model_only_graphs_stay_fully_grounded(self) -> None:
        """Graphs without steps keep the default full-grounding record."""
        fact = Value(5.0, energy_port(), "user-scenario", "Synthetic test fact.")
        composition = Composition(
            "plain-test",
            (Node("nA", "test-double@r1", {"x": fact}),),
            ("nA",),
            "fixture",
        )
        outcome = execute(composition, {"test-double@r1": doubling_model()})
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual(outcome["outputs"]["nA"]["amount"], 10.0)
        self.assertEqual(outcome["grounding"], "full")
        self.assertEqual(outcome["llm_steps"], [])


class ReviseStepTests(unittest.TestCase):
    """Revision recomputes bounded steps instead of carrying stale amounts."""

    def test_revise_requeries_steps_with_fresh_inputs(self) -> None:
        """A revised direct input flows through a recomputed step."""
        composition, catalog = hybrid_graph()
        parent = execute(composition, catalog, None, triple_stub)
        seen: list[float] = []

        def recompute(
            step: LLMStep, values: dict[str, Value], inference_model: str | None = None
        ) -> tuple[float, str]:
            """Record the fresh step input, then triple it deterministically."""
            seen.append(values["y"].amount)
            return values["y"].amount * 3, "recomputed for test"

        with TemporaryDirectory() as tmp:
            save_run(parent, Path(tmp))
            with mock.patch.dict(os.environ, {LLM_STEPS_ENV_VAR: "1"}):
                with mock.patch.object(
                    revisions, "compute_llm_step", side_effect=recompute
                ):
                    revised = revisions.revise_run(
                        parent["run_id"], ["nA.x=7"], [], directory=Path(tmp)
                    )
        self.assertEqual(revised["status"], "completed")
        self.assertEqual(seen, [14.0])
        self.assertEqual(revised["outputs"]["nB"]["amount"], 84.0)
        self.assertFalse(revised["llm_steps"][0]["carried"])
        self.assertEqual(revised["grounding"], "partial")

    def test_revise_without_flag_refuses_step_runs(self) -> None:
        """Revision of a step-bearing run fails closed when the flag is off."""
        composition, catalog = hybrid_graph()
        parent = execute(composition, catalog, None, triple_stub)
        with TemporaryDirectory() as tmp:
            save_run(parent, Path(tmp))
            with mock.patch.dict(os.environ, {LLM_STEPS_ENV_VAR: "0"}):
                with self.assertRaises(ModelError) as raised:
                    revisions.revise_run(
                        parent["run_id"], ["nA.x=7"], [], directory=Path(tmp)
                    )
        self.assertIn(LLM_STEPS_ENV_VAR, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
