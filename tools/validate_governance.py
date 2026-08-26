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
    else:
        resolved = args.path if args.path.is_absolute() else root / args.path
        errors = validate_route(root, resolved)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"FAIL errors={len(errors)}")
        return 1
    print(f"PASS command={args.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
