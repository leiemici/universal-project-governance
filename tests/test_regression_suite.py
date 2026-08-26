import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_regression", ROOT / "tools/run_regression.py")
runner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(runner)


class RegressionSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = json.loads((ROOT / "validation/regression-scenarios-P1.06.json").read_text(encoding="utf-8"))
        cls.spec = spec
        cls.result = runner.run_suite(spec)

    def test_ten_scenarios_three_profiles(self):
        self.assertEqual(10, self.result["scenario_count"])
        self.assertEqual(3, self.result["profile_count"])
        self.assertEqual(30, self.result["run_count"])

    def test_all_runs_converge(self):
        self.assertTrue(self.result["suite_pass"])
        self.assertEqual(30, self.result["converged_runs"])

    def test_simulation_is_not_misrepresented(self):
        self.assertEqual("simulado", self.result["evidence_class"])
        self.assertEqual(0, self.result["live_llm_calls"])
        self.assertEqual(0, self.result["observed_humans"])
        self.assertIsNone(self.result["human_onboarding_under_10_minutes"])
        self.assertTrue(all(not run["onboarding_human_observed"] for run in self.result["runs"]))

    def test_high_extreme_never_silently_operates(self):
        protected = [run for run in self.result["runs"] if run["scenario_id"] in {"S05", "S07", "S08", "S09", "S10"}]
        self.assertTrue(all(run["risk_preserved"] for run in protected))

    def test_simulated_onboarding_budget_is_not_human_evidence(self):
        self.assertTrue(self.result["all_simulated_onboarding_under_10_minutes"])
        self.assertEqual("not-observed", self.result["human_onboarding_claim"])

    def test_every_injection_has_a_canonical_decision(self):
        for scenario in self.spec["scenarios"]:
            self.assertEqual(
                scenario["expected_decisions"],
                [runner.DECISIONS[injection] for injection in scenario["injections"]],
            )

    def test_cross_product_has_no_duplicate_or_missing_pair(self):
        pairs = {(run["scenario_id"], run["profile"]) for run in self.result["runs"]}
        self.assertEqual(30, len(pairs))

    def test_false_claims_are_rejected(self):
        for field, value in (("evidence_class", "validado"), ("live_llm_calls", 1), ("observed_humans", 1)):
            changed = copy.deepcopy(self.spec)
            changed[field] = value
            with self.assertRaises(ValueError):
                runner.run_suite(changed)

    def test_missing_or_duplicate_scenario_is_rejected(self):
        missing = copy.deepcopy(self.spec)
        missing["scenarios"].pop()
        with self.assertRaises(ValueError):
            runner.run_suite(missing)
        duplicate = copy.deepcopy(self.spec)
        duplicate["scenarios"][-1]["id"] = duplicate["scenarios"][0]["id"]
        with self.assertRaises(ValueError):
            runner.run_suite(duplicate)

    def test_unknown_error_injection_is_rejected(self):
        changed = copy.deepcopy(self.spec)
        changed["scenarios"][0]["injections"][0] = "unknown-human-error"
        with self.assertRaises(ValueError):
            runner.run_suite(changed)


if __name__ == "__main__":
    unittest.main()
