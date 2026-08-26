#!/usr/bin/env python3
"""Portable structural validator for Universal Project Governance."""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path
from typing import Any

REVISION = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
EVIDENCE_REQUIRED = {
    "schema_version", "evidence_id", "task_id", "classification", "subject",
    "provenance", "execution", "review", "delivery_commit", "acceptance_satisfied",
}
PROVENANCE_REQUIRED = {
    "source_kind", "source_ref", "collected_at", "coverage", "age_at_validation",
    "transformations", "limitations",
}
CLASSES = {"simulado", "estimado", "executado", "validado"}
SOURCE_KINDS = {"fixture", "repository", "external-system", "human-observation", "calculation"}
RISK_REQUIRED = {
    "schema_version", "assessment_id", "risk_level", "domain", "destination", "destination_basis", "status",
    "required_documents", "authority", "change", "external_controls", "provider_attestations",
    "recovery", "destination_change", "decision",
}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def read_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        errors.append(f"{path}: arquivo ausente")
    except json.JSONDecodeError as exc:
        errors.append(f"{path}:{exc.lineno}:{exc.colno}: JSON inválido: {exc.msg}")
    return None


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_fields(data: Any, required: set[str], label: str, errors: list[str]) -> bool:
    if not isinstance(data, dict):
        errors.append(f"{label}: deve ser um objeto JSON")
        return False
    for field in sorted(required - set(data)):
        errors.append(f"{label}.{field}: campo obrigatório ausente")
    return required.issubset(data)


def validate_evidence(data: Any, label: str) -> list[str]:
    errors: list[str] = []
    if not require_fields(data, EVIDENCE_REQUIRED, label, errors):
        return errors

    extra = set(data) - EVIDENCE_REQUIRED
    for field in sorted(extra):
        errors.append(f"{label}.{field}: campo não reconhecido")

    if data["schema_version"] != 1:
        errors.append(f"{label}.schema_version: esperado 1")
    if not nonempty(data["evidence_id"]) or not data["evidence_id"].startswith("EV-"):
        errors.append(f"{label}.evidence_id: use EV-<identificador>")
    for field in ("task_id", "subject"):
        if not nonempty(data[field]):
            errors.append(f"{label}.{field}: texto não vazio obrigatório")

    classification = data["classification"]
    if classification not in CLASSES:
        errors.append(f"{label}.classification: use {sorted(CLASSES)}")

    provenance = data["provenance"]
    if require_fields(provenance, PROVENANCE_REQUIRED, f"{label}.provenance", errors):
        for field in sorted(set(provenance) - PROVENANCE_REQUIRED):
            errors.append(f"{label}.provenance.{field}: campo não reconhecido")
        if provenance["source_kind"] not in SOURCE_KINDS:
            errors.append(f"{label}.provenance.source_kind: valor inválido")
        for field in ("source_ref", "collected_at", "coverage", "age_at_validation"):
            if not nonempty(provenance[field]):
                errors.append(f"{label}.provenance.{field}: texto não vazio obrigatório")
        if not isinstance(provenance["transformations"], list):
            errors.append(f"{label}.provenance.transformations: lista obrigatória")
        if not isinstance(provenance["limitations"], list) or not provenance["limitations"]:
            errors.append(f"{label}.provenance.limitations: informe ao menos uma limitação")

    execution = data["execution"]
    review = data["review"]
    delivery = data["delivery_commit"]
    acceptance = data["acceptance_satisfied"]
    source_kind = provenance.get("source_kind") if isinstance(provenance, dict) else None

    if source_kind == "fixture" and classification != "simulado":
        errors.append(f"{label}.classification: fixture só pode ser 'simulado'")
    if classification != "validado" and acceptance is not False:
        errors.append(f"{label}.acceptance_satisfied: somente 'validado' pode satisfazer aceite")

    if classification in {"executado", "validado"}:
        if not isinstance(execution, dict):
            errors.append(f"{label}.execution: obrigatório para {classification}")
        else:
            for field in ("environment", "command_or_case", "result"):
                if not nonempty(execution.get(field)):
                    errors.append(f"{label}.execution.{field}: texto não vazio obrigatório")
            if not REVISION.fullmatch(str(execution.get("commit", ""))):
                errors.append(f"{label}.execution.commit: revisão Git de 40 ou 64 hex obrigatória")
            if execution.get("reproducible") is not True:
                errors.append(f"{label}.execution.reproducible: deve ser true")

    if classification == "validado":
        if source_kind == "fixture":
            errors.append(f"{label}.provenance.source_kind: fixture não pode ser validada como execução")
        if not isinstance(review, dict):
            errors.append(f"{label}.review: revisão reproduzível obrigatória para 'validado'")
        else:
            if not nonempty(review.get("reviewer")) or not nonempty(review.get("reviewed_at")):
                errors.append(f"{label}.review: reviewer e reviewed_at são obrigatórios")
            if review.get("result") != "accepted":
                errors.append(f"{label}.review.result: deve ser 'accepted'")
        exec_commit = execution.get("commit") if isinstance(execution, dict) else None
        review_commit = review.get("review_commit") if isinstance(review, dict) else None
        if not REVISION.fullmatch(str(delivery or "")):
            errors.append(f"{label}.delivery_commit: revisão Git obrigatória para 'validado'")
        if not (exec_commit == review_commit == delivery and exec_commit is not None):
            errors.append(f"{label}: execução, revisão e entrega devem apontar para o mesmo commit")
        if acceptance is not True:
            errors.append(f"{label}.acceptance_satisfied: 'validado' deve registrar true")

    return errors


def validate_risk(data: Any, label: str, root: Path) -> list[str]:
    errors: list[str] = []
    if not require_fields(data, RISK_REQUIRED, label, errors):
        return errors
    for field in sorted(set(data) - RISK_REQUIRED):
        errors.append(f"{label}.{field}: campo não reconhecido")
    if data["schema_version"] != 1:
        errors.append(f"{label}.schema_version: esperado 1")
    if not nonempty(data["assessment_id"]) or not data["assessment_id"].startswith("RISK-"):
        errors.append(f"{label}.assessment_id: use RISK-<identificador>")
    if data["risk_level"] not in {"alto", "extremo"}:
        errors.append(f"{label}.risk_level: use alto ou extremo")
    if data["domain"] not in {"nenhum", "clínico", "financeiro", "físico"}:
        errors.append(f"{label}.domain: domínio inválido")
    destinations = {"produção", "canário-shadow", "sandbox", "simulador", "pacote-de-evidência"}
    if data["destination"] not in destinations:
        errors.append(f"{label}.destination: destino inválido")
    if data["destination_basis"] not in {"initial", "changed"}:
        errors.append(f"{label}.destination_basis: use initial ou changed")
    if data["status"] not in {"bloqueado", "pronto-para-revisão", "aprovado-para-destino", "expirado"}:
        errors.append(f"{label}.status: estado inválido")

    docs = data["required_documents"]
    if require_fields(docs, {"profile", "runbook", "annex", "annex_status"}, f"{label}.required_documents", errors):
        for key in ("profile", "runbook"):
            if not nonempty(docs[key]) or not (root / docs[key]).is_file():
                errors.append(f"{label}.required_documents.{key}: caminho obrigatório ausente")
        if data["domain"] != "nenhum":
            if not nonempty(docs["annex"]) or not (root / docs["annex"]).is_file():
                errors.append(f"{label}.required_documents.annex: anexo aplicável ausente")
            expected_annex = {"clínico": "clinical.md", "financeiro": "financial.md", "físico": "physical.md"}[data["domain"]]
            if Path(str(docs.get("annex", ""))).name != expected_annex:
                errors.append(f"{label}.required_documents.annex: anexo não corresponde ao domínio")
        if data["status"] == "aprovado-para-destino" and docs["annex_status"] != "approved-by-competent-human":
            errors.append(f"{label}.required_documents.annex_status: aprovação humana competente obrigatória")

    authority = data["authority"]
    if require_fields(authority, {"author", "reviewer", "approver", "approver_competence"}, f"{label}.authority", errors):
        identities = [authority.get(k) for k in ("author", "reviewer", "approver")]
        if not all(nonempty(v) for v in identities) or len(set(identities)) != 3:
            errors.append(f"{label}.authority: autor, revisor e aprovador devem ser distintos")
        if not nonempty(authority.get("approver_competence")):
            errors.append(f"{label}.authority.approver_competence: competência obrigatória")

    change = data["change"]
    change_required = {"baseline_revision", "cumulative_delta", "threshold", "unit", "threshold_exceeded", "risk_reopened", "reassessed_at"}
    if require_fields(change, change_required, f"{label}.change", errors):
        delta, threshold = change.get("cumulative_delta"), change.get("threshold")
        if not isinstance(delta, (int, float)) or isinstance(delta, bool) or delta < 0:
            errors.append(f"{label}.change.cumulative_delta: número não negativo obrigatório")
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or threshold <= 0:
            errors.append(f"{label}.change.threshold: número positivo obrigatório")
        calculated = isinstance(delta, (int, float)) and isinstance(threshold, (int, float)) and delta >= threshold
        if change.get("threshold_exceeded") is not calculated:
            errors.append(f"{label}.change.threshold_exceeded: deve refletir cumulative_delta >= threshold")
        if calculated and change.get("risk_reopened") is not True:
            errors.append(f"{label}.change.risk_reopened: drift acima do limiar reabre o risco")
        if calculated and data["status"] == "aprovado-para-destino" and not nonempty(change.get("reassessed_at")):
            errors.append(f"{label}.change.reassessed_at: reavaliação obrigatória após drift")

    controls = data["external_controls"]
    if not isinstance(controls, list):
        errors.append(f"{label}.external_controls: lista obrigatória")
        controls = []
    verified = []
    for index, control in enumerate(controls):
        prefix = f"{label}.external_controls[{index}]"
        needed = {"control_id", "kind", "enforcement_system", "evidence_ref", "evidence_revision", "valid_until", "status", "provider"}
        if not require_fields(control, needed, prefix, errors):
            continue
        system = str(control.get("enforcement_system", "")).strip().lower()
        if not system or system in {"markdown", "documentation", "documento", "repository", "prompt", "checklist"}:
            errors.append(f"{prefix}.enforcement_system: texto/repositório não é enforcement técnico")
        if not str(control.get("evidence_ref", "")).startswith("external://"):
            errors.append(f"{prefix}.evidence_ref: use referência sanitizada external://")
        if not REVISION.fullmatch(str(control.get("evidence_revision", ""))):
            errors.append(f"{prefix}.evidence_revision: revisão de 40 ou 64 hex obrigatória")
        if control.get("status") not in {"verified", "missing", "expired"}:
            errors.append(f"{prefix}.status: use verified, missing ou expired")
        if control.get("status") == "verified" and nonempty(control.get("valid_until")):
            verified.append(control)

    attestations = data["provider_attestations"]
    if not isinstance(attestations, list):
        errors.append(f"{label}.provider_attestations: lista obrigatória")
        attestations = []
    attested = {a.get("provider") for a in attestations if isinstance(a, dict) and nonempty(a.get("provider")) and nonempty(a.get("attested_at")) and nonempty(a.get("valid_until")) and str(a.get("evidence_ref", "")).startswith("external://")}
    for control in verified:
        provider = control.get("provider")
        if nonempty(provider) and provider not in attested:
            errors.append(f"{label}.provider_attestations: provedor {provider} sem reatestado externo vigente")

    recovery = data["recovery"]
    if require_fields(recovery, {"safe_state", "stop_mechanism", "rollback", "reconciliation"}, f"{label}.recovery", errors):
        for key in ("safe_state", "stop_mechanism", "rollback", "reconciliation"):
            if not nonempty(recovery.get(key)):
                errors.append(f"{label}.recovery.{key}: texto não vazio obrigatório")

    decision = data["decision"]
    if require_fields(decision, {"action", "approved_by", "approved_at", "decision_ref"}, f"{label}.decision", errors):
        for key in ("approved_by", "approved_at", "decision_ref"):
            if not nonempty(decision.get(key)):
                errors.append(f"{label}.decision.{key}: aprovação humana registrada obrigatória")
        if isinstance(authority, dict) and decision.get("approved_by") != authority.get("approver"):
            errors.append(f"{label}.decision.approved_by: deve coincidir com authority.approver")
        operational = data["destination"] in {"produção", "canário-shadow", "sandbox"}
        if data["status"] == "aprovado-para-destino":
            expected_action = {
                "simulador": "allow-simulator",
                "pacote-de-evidência": "allow-evidence-package",
            }.get(data["destination"], "allow-destination")
            if decision.get("action") != expected_action:
                errors.append(f"{label}.decision.action: esperado {expected_action}")
            if operational and not verified:
                errors.append(f"{label}.external_controls: destino operacional permanece bloqueado sem controle externo verificado")
        elif decision.get("action") != "bloquear":
            errors.append(f"{label}.decision.action: estado não aprovado exige bloquear")

    destination_change = data["destination_change"]
    if data["destination_basis"] == "changed" and destination_change is None:
        errors.append(f"{label}.destination_change: mudança/rebaixamento exige aprovação humana registrada")
    if data["destination_basis"] == "initial" and destination_change is not None:
        errors.append(f"{label}.destination_basis: use 'changed' quando houver destination_change")
    if destination_change is not None:
        required = {"previous", "current", "approved_by", "approved_at", "decision_ref"}
        if require_fields(destination_change, required, f"{label}.destination_change", errors):
            if destination_change.get("current") != data["destination"]:
                errors.append(f"{label}.destination_change.current: deve coincidir com destination")
            if destination_change.get("previous") == destination_change.get("current"):
                errors.append(f"{label}.destination_change: previous e current devem ser diferentes")
            for key in ("approved_by", "approved_at", "decision_ref"):
                if not nonempty(destination_change.get(key)):
                    errors.append(f"{label}.destination_change.{key}: rebaixamento exige aprovação humana")
            if isinstance(authority, dict) and destination_change.get("approved_by") != authority.get("approver"):
                errors.append(f"{label}.destination_change.approved_by: deve coincidir com authority.approver")
    return errors


def eval_condition(condition: dict[str, Any], facts: dict[str, Any]) -> bool:
    actual, operator, expected = facts.get(condition.get("field")), condition.get("operator"), condition.get("value")
    if operator == "equals":
        return actual == expected
    if operator == "not_equals":
        return actual != expected
    if operator == "in":
        return actual in expected
    if operator == "at_least":
        return isinstance(actual, (int, float)) and not isinstance(actual, bool) and actual >= expected
    raise ValueError(f"operador desconhecido: {operator}")


def validate_facts(manifest: dict[str, Any], facts: Any, label: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    if not isinstance(facts, dict):
        return [f"{label}: facts deve ser objeto"], []
    definitions = manifest.get("facts", {})
    for name, definition in definitions.items():
        if name not in facts:
            errors.append(f"{label}.facts.{name}: fato obrigatório ausente")
            continue
        value, kind = facts[name], definition.get("type")
        valid = True
        if kind == "enum":
            valid = value in definition.get("values", [])
        elif kind == "integer":
            valid = isinstance(value, int) and not isinstance(value, bool) and value >= definition.get("minimum", 0)
        elif kind == "boolean":
            valid = isinstance(value, bool)
        elif kind == "positive-number-or-literal":
            valid = value == definition.get("literal") or (isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0)
        if not valid:
            errors.append(f"{label}.facts.{name}: valor inválido para {kind}")

    active: list[str] = []
    if not errors:
        for overlay in manifest.get("overlays", []):
            activation = overlay.get("activation", {})
            any_ok = "any" not in activation or any(eval_condition(c, facts) for c in activation["any"])
            all_ok = "all" not in activation or all(eval_condition(c, facts) for c in activation["all"])
            if any_ok and all_ok:
                active.append(overlay["id"])
        floor_conditions = manifest.get("risk_floor", {}).get("on_any", [])
        risk_rank = {"baixo": 0, "médio": 1, "alto": 2, "extremo": 3}
        if any(eval_condition(c, facts) for c in floor_conditions) and risk_rank.get(facts.get("risco"), -1) < 2:
            errors.append(f"{label}.facts.risco: piso 'alto' exigido; roteamento permanece pendente")
    return errors, active


def validate_route(root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    manifest = read_json(root / "overlays.json", errors)
    record = read_json(path, errors)
    if not isinstance(manifest, dict):
        if manifest is None and not errors:
            errors.append(f"{root / 'overlays.json'}: deve ser um objeto JSON")
        return errors
    if not isinstance(record, dict):
        if record is None and not errors:
            errors.append(f"{path}: deve ser um objeto JSON")
        return errors
    route_errors, active = validate_facts(manifest, record.get("facts"), str(path))
    errors.extend(route_errors)
    expected = record.get("expected_active_overlays")
    if expected is not None and sorted(expected) != sorted(active):
        errors.append(f"{path}.expected_active_overlays: esperado {expected}, calculado {active}")
    return errors


def validate_repo(root: Path) -> list[str]:
    errors: list[str] = []
    config = read_json(root / "governance.validation.json", errors)
    if not isinstance(config, dict):
        if config is None and not errors:
            errors.append("governance.validation.json: deve ser um objeto JSON")
        return errors
    for relative in config.get("canonical_paths", []):
        if not (root / relative).is_file():
            errors.append(f"canonical_paths: caminho quebrado: {relative}")
    manifest = read_json(root / config.get("overlay_manifest", "overlays.json"), errors)
    if isinstance(manifest, dict):
        ids: set[str] = set()
        for overlay in manifest.get("overlays", []):
            oid = overlay.get("id")
            if not oid or oid in ids:
                errors.append(f"overlays.json: id ausente ou duplicado: {oid}")
            ids.add(oid)
            for relative in overlay.get("required_reading", []):
                if not (root / relative).is_file():
                    errors.append(f"overlays.json[{oid}].required_reading: caminho quebrado: {relative}")
    elif manifest is None and not errors:
        errors.append("overlays.json: deve ser um objeto JSON")
    read_json(root / "docs/evidence-record.schema.json", errors)
    read_json(root / "docs/risk-control-record.schema.json", errors)
    read_json(root / "docs/context-manifest.schema.json", errors)
    for pattern in config.get("evidence_globs", []):
        for filename in sorted(glob.glob(str(root / pattern))):
            path = Path(filename)
            previous = len(errors)
            data = read_json(path, errors)
            if data is not None:
                errors.extend(validate_evidence(data, str(path.relative_to(root))))
            elif len(errors) == previous:
                errors.append(f"{path.relative_to(root)}: deve ser um objeto JSON")
    for pattern in config.get("risk_globs", []):
        for filename in sorted(glob.glob(str(root / pattern))):
            path = Path(filename)
            previous = len(errors)
            data = read_json(path, errors)
            if data is not None:
                errors.extend(validate_risk(data, str(path.relative_to(root)), root))
            elif len(errors) == previous:
                errors.append(f"{path.relative_to(root)}: deve ser um objeto JSON")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("repo")
    evidence = sub.add_parser("evidence")
    evidence.add_argument("paths", nargs="+", type=Path)
    route = sub.add_parser("route")
    route.add_argument("path", type=Path)
    risk = sub.add_parser("risk")
    risk.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    errors: list[str] = []
    if args.command == "repo":
        errors = validate_repo(root)
    elif args.command == "evidence":
        for path in args.paths:
            resolved = path if path.is_absolute() else root / path
            previous = len(errors)
            data = read_json(resolved, errors)
            if data is not None:
                errors.extend(validate_evidence(data, str(path)))
            elif len(errors) == previous:
                errors.append(f"{path}: deve ser um objeto JSON")
    elif args.command == "route":
        resolved = args.path if args.path.is_absolute() else root / args.path
        errors = validate_route(root, resolved)
    else:
        for path in args.paths:
            resolved = path if path.is_absolute() else root / path
            previous = len(errors)
            data = read_json(resolved, errors)
            if data is not None:
                errors.extend(validate_risk(data, str(path), root))
            elif len(errors) == previous:
                errors.append(f"{path}: deve ser um objeto JSON")
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"FAIL errors={len(errors)}")
        return 1
    print(f"PASS command={args.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
