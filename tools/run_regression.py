#!/usr/bin/env python3
"""Run the declared structural simulation; never represents live humans or LLM calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DECISIONS = {
    "scope-creep": "redirect-or-swap",
    "checkpoint-overrun": "cut-or-fallback",
    "false-evidence": "reject-claim",
    "ambiguous-input": "clarify-minimum",
    "missing-provenance": "reject-claim",
    "broken-canonical": "block-integration",
    "expired-handoff": "escalate-handoff",
    "late-joiner": "guided-reentry",
    "high-risk-no-control": "block-operation",
    "provider-drift": "reopen-risk",
    "concurrent-contract": "stop-integration",
    "scope-drift": "reopen-risk",
}


def run_suite(spec: dict) -> dict:
    if spec.get("evidence_class") != "simulado" or spec.get("live_llm_calls") != 0 or spec.get("observed_humans") != 0:
        raise ValueError("suite must declare simulated evidence, zero live LLM calls and zero observed humans")
    profiles, scenarios = spec.get("profiles", []), spec.get("scenarios", [])
    if len(profiles) != 3 or {p.get("id") for p in profiles} != {"simples", "intermediária", "forte"}:
        raise ValueError("exactly three declared simulated LLM profiles are required")
    if len(scenarios) != 10 or len({s.get("id") for s in scenarios}) != 10:
        raise ValueError("exactly ten unique scenarios are required")

    runs = []
    for scenario in scenarios:
        calculated = [DECISIONS.get(injection, "unmapped") for injection in scenario.get("injections", [])]
        expected = scenario.get("expected_decisions", [])
        if calculated != expected:
            raise ValueError(f"{scenario.get('id')}: expected decisions diverge from canonical mapping")
        for profile in profiles:
            high_risk_safe = True
            if scenario.get("risk") in {"alto", "extremo"} and scenario.get("destination") in {"produção", "sandbox"}:
                high_risk_safe = "block-operation" in calculated or "reopen-risk" in calculated
            runs.append({
                "scenario_id": scenario["id"],
                "profile": profile["id"],
                "profile_behavior": profile["behavior"],
                "evidence_class": "simulado",
                "decisions": calculated,
                "direction_preserved": "unmapped" not in calculated,
                "risk_preserved": high_risk_safe,
                "simulated_onboarding_seconds": profile["simulated_onboarding_seconds"],
                "onboarding_human_observed": False,
                "safe_learning_destination": scenario["safe_learning_destination"],
            })
    converged = all(run["direction_preserved"] and run["risk_preserved"] for run in runs)
    return {
        "schema_version": 1,
        "evidence_class": "simulado",
        "method": "deterministic structural personas; no live provider inference",
        "live_llm_calls": 0,
        "observed_humans": 0,
        "human_onboarding_claim": "not-observed",
        "scenario_count": len(scenarios),
        "profile_count": len(profiles),
        "run_count": len(runs),
        "converged_runs": sum(1 for run in runs if run["direction_preserved"] and run["risk_preserved"]),
        "all_simulated_onboarding_under_10_minutes": all(run["simulated_onboarding_seconds"] <= 600 for run in runs),
        "human_onboarding_under_10_minutes": None,
        "suite_pass": converged,
        "runs": runs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=Path("validation/regression-scenarios-P1.06.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_suite(json.loads(args.spec.read_text(encoding="utf-8")))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if result["suite_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
