import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_governance", ROOT / "tools/validate_governance.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(validator)


class GovernanceValidatorTests(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def approved_risk(self, domain, destination):
        record = self.load("risk/RISK-example-blocked.json")
        annex = {"clínico": "clinical.md", "financeiro": "financial.md", "físico": "physical.md"}[domain]
        record["domain"] = domain
        record["destination"] = destination
        record["required_documents"]["annex"] = f"domain-annexes/{annex}"
        record["required_documents"]["annex_status"] = "approved-by-competent-human"
        record["status"] = "aprovado-para-destino"
        record["decision"]["action"] = {
            "simulador": "allow-simulator",
            "pacote-de-evidência": "allow-evidence-package",
        }.get(destination, "allow-destination")
        if destination in {"produção", "canário-shadow", "sandbox"}:
            record["external_controls"] = [{
                "control_id": "CTRL-1", "kind": "gateway-or-interlock",
                "enforcement_system": "control-plane", "evidence_ref": "external://control/1",
                "evidence_revision": "a" * 40, "valid_until": "2026-09-01T00:00:00Z",
                "status": "verified", "provider": None,
            }]
        return record

    def test_repository_contract_is_valid(self):
        self.assertEqual([], validator.validate_repo(ROOT))

    def test_regression_result_cannot_claim_unobserved_humans(self):
        result = self.load("validation/regression-results-P1.06.json")
        result["observed_humans"] = 1
        errors = validator.validate_regression(result, "regression")
        self.assertTrue(any("não alegue participação humana" in error for error in errors))

    def test_regression_result_requires_complete_cross_product(self):
        result = self.load("validation/regression-results-P1.06.json")
        result["runs"][-1] = copy.deepcopy(result["runs"][0])
        errors = validator.validate_regression(result, "regression")
        self.assertTrue(any("matriz cenário/perfil incompleta" in error for error in errors))

    def test_simulated_fixture_is_valid(self):
        record = self.load("evidence/EV-P1.04-example.json")
        self.assertEqual([], validator.validate_evidence(record, "fixture"))

    def test_reviewed_execution_is_valid(self):
        record = self.load("validation/fixtures/evidence/validated-valid.json")
        self.assertEqual([], validator.validate_evidence(record, "record"))

    def test_fixture_cannot_claim_execution(self):
        record = self.load("validation/fixtures/evidence/fixture-executed-invalid.json")
        errors = validator.validate_evidence(record, "fixture")
        self.assertTrue(any("fixture só pode" in error for error in errors))

    def test_validated_requires_review(self):
        record = self.load("validation/fixtures/evidence/validated-no-review-invalid.json")
        errors = validator.validate_evidence(record, "record")
        self.assertTrue(any("revisão reproduzível" in error for error in errors))

    def test_missing_field_is_actionable(self):
        record = self.load("evidence/EV-P1.04-example.json")
        del record["provenance"]
        errors = validator.validate_evidence(record, "record")
        self.assertIn("record.provenance: campo obrigatório ausente", errors)

    def test_each_provenance_field_is_required(self):
        base = self.load("evidence/EV-P1.04-example.json")
        for field in sorted(validator.PROVENANCE_REQUIRED):
            record = copy.deepcopy(base)
            del record["provenance"][field]
            errors = validator.validate_evidence(record, "record")
            self.assertTrue(any(field in error and "obrigatório ausente" in error for error in errors))

    def test_null_is_not_an_evidence_record(self):
        errors = validator.validate_evidence(None, "record")
        self.assertIn("record: deve ser um objeto JSON", errors)

    def test_validated_commits_must_match(self):
        record = self.load("validation/fixtures/evidence/validated-no-review-invalid.json")
        record["review"] = {
            "reviewer": "reviewer@example",
            "reviewed_at": "2026-08-26T16:45:00-03:00",
            "review_commit": "b" * 40,
            "result": "accepted",
        }
        errors = validator.validate_evidence(record, "record")
        self.assertTrue(any("mesmo commit" in error for error in errors))

    def test_route_expected_overlays(self):
        self.assertEqual([], validator.validate_route(ROOT, ROOT / "validation/fixtures/routing/valid.json"))

    def test_missing_route_fact_is_actionable(self):
        manifest = self.load("overlays.json")
        record = self.load("validation/fixtures/routing/valid.json")
        del record["facts"]["risco"]
        errors, _ = validator.validate_facts(manifest, record["facts"], "route")
        self.assertIn("route.facts.risco: fato obrigatório ausente", errors)

    def test_broken_canonical_path_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            temporary = Path(folder)
            config = {"schema_version": 1, "canonical_paths": ["missing.md"], "evidence_globs": [], "overlay_manifest": "overlays.json"}
            (temporary / "governance.validation.json").write_text(json.dumps(config), encoding="utf-8")
            (temporary / "overlays.json").write_text('{"overlays": []}', encoding="utf-8")
            docs = temporary / "docs"
            docs.mkdir()
            (docs / "evidence-record.schema.json").write_text('{}', encoding="utf-8")
            (docs / "context-manifest.schema.json").write_text('{}', encoding="utf-8")
            errors = validator.validate_repo(temporary)
            self.assertTrue(any("caminho quebrado" in error for error in errors))

    def test_only_validated_can_satisfy_acceptance(self):
        base = self.load("evidence/EV-P1.04-example.json")
        for classification in ("simulado", "estimado", "executado"):
            record = copy.deepcopy(base)
            record["classification"] = classification
            record["acceptance_satisfied"] = True
            errors = validator.validate_evidence(record, classification)
            self.assertTrue(any("somente 'validado'" in error for error in errors))

    def test_high_risk_domain_destination_matrix(self):
        for domain in ("clínico", "financeiro", "físico"):
            for destination in ("produção", "sandbox", "simulador"):
                record = self.approved_risk(domain, destination)
                self.assertEqual([], validator.validate_risk(record, f"{domain}-{destination}", ROOT))

    def test_operational_destination_requires_external_control(self):
        record = self.approved_risk("financeiro", "produção")
        record["external_controls"] = []
        errors = validator.validate_risk(record, "risk", ROOT)
        self.assertTrue(any("permanece bloqueado" in error for error in errors))

    def test_documentation_is_not_enforcement(self):
        record = self.approved_risk("físico", "sandbox")
        record["external_controls"][0]["enforcement_system"] = "markdown"
        errors = validator.validate_risk(record, "risk", ROOT)
        self.assertTrue(any("não é enforcement" in error for error in errors))

    def test_cumulative_drift_reopens_risk(self):
        record = self.approved_risk("clínico", "simulador")
        record["change"]["cumulative_delta"] = record["change"]["threshold"]
        record["change"]["threshold_exceeded"] = True
        record["change"]["risk_reopened"] = False
        errors = validator.validate_risk(record, "risk", ROOT)
        self.assertTrue(any("reabre o risco" in error for error in errors))

    def test_changed_destination_requires_human_record(self):
        record = self.approved_risk("financeiro", "simulador")
        record["destination_basis"] = "changed"
        errors = validator.validate_risk(record, "risk", ROOT)
        self.assertTrue(any("rebaixamento exige" in error for error in errors))

    def test_provider_control_requires_reattestation(self):
        record = self.approved_risk("financeiro", "produção")
        record["external_controls"][0]["provider"] = "payments-provider"
        errors = validator.validate_risk(record, "risk", ROOT)
        self.assertTrue(any("sem reatestado" in error for error in errors))
        record["provider_attestations"] = [{
            "provider": "payments-provider", "attested_at": "2026-08-26T00:00:00Z",
            "valid_until": "2026-09-01T00:00:00Z", "evidence_ref": "external://provider/attestation",
        }]
        self.assertEqual([], validator.validate_risk(record, "risk", ROOT))


if __name__ == "__main__":
    unittest.main()
