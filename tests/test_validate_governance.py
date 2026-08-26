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

    def test_repository_contract_is_valid(self):
        self.assertEqual([], validator.validate_repo(ROOT))

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


if __name__ == "__main__":
    unittest.main()
