from __future__ import annotations

import json
import unittest
from pathlib import Path

from validation.engine import ValidationInputError, load_json, run_suite


ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = ROOT / "validation" / "cases" / "runtime_integrity_cases.json"
MODEL_PATH = ROOT / "models" / "governance-state-model.json"
EQUATION_REGISTRY = ROOT / "registry" / "EQ_BIBLE_OMEGA.md"

LOCKED_EQUATIONS = [
    "Ψ = Consciousness Anchor",
    "ΩR = Root Declaration",
    "ΔR(t) = ||Ω_obs - ΩR||",
    "II(t) = Σ ωᵢ·Iᵢ(t)",
    "Pe(t) = ∫ L(t) dt",
    "Re(t) = -dPe/dt",
    "Φ = ∇(1 - II)",
    "Vc(t) = d/dt(1 - ΔR)",
]


class ValidationEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.suite = load_json(SUITE_PATH)
        self.model = load_json(MODEL_PATH)

    def test_reference_suite_matches_all_expected_outcomes(self) -> None:
        report = run_suite(self.suite, self.model)
        self.assertEqual(report["summary"]["total_cases"], 8)
        self.assertEqual(report["summary"]["expectations_matched"], 8)
        self.assertEqual(report["summary"]["expectation_mismatches"], 0)
        self.assertTrue(report["summary"]["suite_passed"])

    def test_model_must_remain_provisional_and_noncanonical(self) -> None:
        promoted = dict(self.model)
        promoted["canonical"] = True
        with self.assertRaises(ValidationInputError):
            run_suite(self.suite, promoted)

    def test_each_fixture_is_explicitly_noncanonical(self) -> None:
        for case in self.suite["cases"]:
            self.assertEqual(case["classification"], "NON_CANONICAL_SYNTHETIC_FIXTURE")

    def test_locked_equation_transcriptions_remain_present_exactly(self) -> None:
        registry = EQUATION_REGISTRY.read_text(encoding="utf-8")
        for equation in LOCKED_EQUATIONS:
            self.assertIn(equation, registry)
            self.assertEqual(registry.count(equation), 1)

    def test_case_identifiers_are_unique(self) -> None:
        identifiers = [case["case_id"] for case in self.suite["cases"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))


if __name__ == "__main__":
    unittest.main()
