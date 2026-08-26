# Neocortex Project Memory

## Purpose

This repository is a portable, non-UI governance architecture for turning a project conversation into shared, executable direction for mixed-seniority teams and multiple LLM providers.

## Canonical direction

- Preserve **ALVO, PRAZO, DESTINO, ACEITE** and the approved cut rule.
- Use two to six project keywords to connect every task to one required outcome and integration point.
- Planning depth must be proportional to duration, risk and coordination cost.
- Human error is treated as a system condition: redirect ambiguous or divergent work instead of relying on perfect prompts or perfect people.
- Decisions that change target, deadline, destination, acceptance, risk, data scope or irreversible effects require recorded human approval.
- Claims are not evidence. Validation requires a reproducible result tied to the same revision that is reviewed and delivered.

## Required reading

Start at `docs/overlay-router.md` and follow its canonical order. Do not maintain a second reading list here. The router deterministically adds `profiles/high-extreme.md` and `RUNBOOK.md` whenever risk is high or extreme.

## Architecture mode

- Mode: `non-UI`
- Graphical interface: none
- Own database: none
- Own API: none
- Primary surfaces: Markdown files in the repository root, `docs/` and `profiles/`

The fixed Neocortex stages `arch-design-system`, `arch-ux-design`, `arch-database` and `arch-api-contracts` do not apply to this repository and must not be run. Useful concerns from skipped stages belong in the PRD or architecture document rather than separate fictional artifacts.

## Existing evidence

- Instance intake template: `PRD.md`
- Product requirements for this governance repository: `docs/architecture/prd.md`
- Operational directive: `PROJECT_CHARTER.md`
- Agent steering: `AGENTS.md`, `CONTEXT.md`, `docs/steering.md`
- Governance and recovery: `GOVERNANCE.md`, `RUNBOOK.md`, `profiles/high-extreme.md`
- Execution and collaboration: `TEAM.md`, `docs/execution-plan.md`, `docs/tasks.md`, `docs/task-template.md`, `docs/handoff.md`
- Context snapshots: `docs/context-registry.md`, `docs/context-manifest.schema.json`, `contexts/`
- Decisions and dependencies: `docs/decisions.md`, `docs/dependencies.md`, `docs/api-contract.md`
- Evidence and known gaps: `docs/validation-matrix.md`, `docs/simulation-report-10-projects.md`, `docs/regression-report-10-projects.md`

## Current architecture objective

Consolidate the repository into a coherent universal core plus conditional overlays, so people and LLMs can enter at different skill levels, share one verified context, work in bounded branches and converge on the same result without excessive process.

## Architecture artifacts

- Product requirements and measurable outcomes: `docs/architecture/prd.md`
- Component architecture, states, overlays and fitness functions: `docs/architecture/architecture.md`
- Consolidated review and quality gate: `docs/architecture/review-consolidation.md`

## Active epic

- `P1` — Arquitetura universal convergente: `docs/epics/epic-P1.md`
- Stories `P1.01`–`P1.06` cover overlays, context snapshots, task/handoff lifecycle, evidence checks, high/extreme boundaries and regression validation.
- `P1.01` passed QA and was physically merged as `fb1e77c` on 2026-08-26.
- `P1.02` passed its local QA gate on 2026-08-26; `P1.03` follows after physical merge.

## Known gaps to resolve

- Handoffs lack expiry, escalation, contract version and formal receiver acceptance.
- Data outputs do not universally require source, collection time, coverage and age.
- Multi-LLM identity and context are recorded, but an independence group remains a declaration rather than proof of independent evidence or incentives.
- High/extreme gates remain documentary and require domain-specific technical enforcement outside this repository.
- Regression reports contain recommendations that have not all migrated into canonical templates and rules.

## Architecture decision and next gate

The non-UI architecture is **approved with conditions**. Its core model is accepted: a small universal core, deterministic conditional overlays, a versioned context manifest, a work graph, an evidence ledger, an integration gate, accepted/expiring handoffs, external risk boundaries and portable fitness functions.

Story `P1.01` resolved the four C0 conditions from `docs/architecture/review-consolidation.md`:

1. the canonical entry is `docs/overlay-router.md` across README, agents and memory;
2. the evidence vocabulary is `simulado`, `estimado`, `executado`, `validado`;
3. root `PRD.md` is the instance template and `docs/architecture/prd.md` is this product's PRD;
4. `overlays.json` plus the confirmed charter facts implement the minimum deterministic overlay router.

Its QA evidence covers six nominal scenarios, 13,824 routing combinations with zero divergence, twelve typed facts, five overlay contracts and six risk-floor cases. The generic npm server test is `[N/A]` because this repository has no application runtime; portable executable fitness functions remain scoped to `P1.04`.

Story `P1.02` adds a portable JSON Schema, task-bound context registry, generic human/LLM identity, data/autonomy gate and selective invalidation. Its QA evidence includes two provider interpretations, nine negative contract cases, 1,000 generated valid manifests, all 16 root-required fields, seven LLM identity fields and 1,000 selective invalidation cases. The generic npm server test is `[N/A]`; persistent executable lint remains P1.04.

Stories `P1.03`–`P1.04` next implement accepted handoffs, provenance and structural checks. Story `P1.05` defines high/extreme external-control contracts without authorizing operations. Story `P1.06` re-runs multi-LLM and human validation only after the rules are canonical and executable.

## Neocortex architecture trail

The focused non-UI architecture path is complete: `init`, `arch-prd`, `create-epic`, `arch-architecture`, `arch-review` and `update-memory` were executed on 2026-08-26. The review result remains approved with conditions until P1.03–P1.04 implement the remaining operational contracts; P1.01's C0 gate and P1.02's context gate are complete.

The fixed plan's API contracts, Pact generation, API integrations, database, design system and UX stages are `[N/A]`. Security, performance, testing and infrastructure concerns were absorbed into `docs/architecture/architecture.md`; fitness functions are specified there and their portable implementation belongs to story `P1.04`. This closes the unused branches deliberately and prevents future sessions from generating fictional artifacts.
