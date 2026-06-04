# Implementation Plan: Self-Hosted Deployment And Operations Reference

**Branch**: `006-self-hosted-deployment-operations-reference` | **Date**: 2026-06-04 |
**Spec**: `specs/006-self-hosted-deployment-operations-reference/spec.md`

## Summary

Turn the selected Pydantic AI plus Langfuse/DBOS product baseline into a reproducible self-hosted deployment reference.
The work starts by defining deployment profiles and BDD contracts, then proves a representative workflow with
repo-local evidence, then records operations runbooks and reviewer-accepted Goal 005 evidence.

## Technical Context

**Language/Version**: Python 3.14 for workflow tooling and Pydantic AI app code; shell scripts for service operations.
**Primary Dependencies**: Existing `awf` CLI, Beads, Pydantic AI app, Langfuse OTLP proof path, DBOS durable proof path,
Docker or equivalent service runtime where selected by the profile.
**Storage**: `docs/deployment/`, `docs/operations/`, `.agent-runs/reports/`, `.agent-runs/verifications/`,
`.beads/issues.jsonl`, environment templates, and selected app artifacts.
**Testing**: `uv run awf workflow-fixture-test`, `uv run awf verify --profile health --json`,
`uv run awf verify --profile increment --json`, `uv run awf repo-hygiene`, and deployment smoke commands added by this
spec.
**Target Platform**: Local development on the MacBook, heavier development on `vps-dev`, and production-like management
on `vps-gw` when appropriate.
**Project Type**: Workflow and selected-stack deployment reference for a self-hosted agent system.
**Constraints**: Do not require third-party hosted services for core behavior. Do not commit secrets. Keep deterministic
fixture validation credential-free. Keep deployment evidence repo-local or on controlled infrastructure.

## Constitution Check

- Repository artifacts are the source of truth: PASS.
- Human-only pause is not required for goal evidence: PASS; presenter and independent reviewer evidence are required.
- Testable behavior comes before implementation depth: PASS through a deployment BDD contract and smoke evidence.
- Small slices and traceable tickets: PASS through Beads tasks generated from this spec.
- Alpha means no compatibility debt: PASS; deployment scripts and docs can evolve directly.

## Project Structure

```text
docs/
├── deployment/          # profile, topology, ports, volumes, env templates, startup
├── operations/          # backup, restore, reset, health, logs, traces, recovery
└── goals/

apps/
└── pydantic-ai/         # selected product-baseline lane and deployment smoke entrypoints

tests/
└── workflow/
    └── features/        # deployment operations BDD contract

.agent-runs/
├── reports/             # presenter/reviewer evidence
└── verifications/       # deployment smoke and increment verification artifacts
```

## Phased Plan

1. Define implementation-agnostic BDD coverage for self-hosted deployment operations.
2. Document local, development-server, and production-like profiles with service boundaries, ports, volumes, secrets,
   storage, target machines, and one-engineer operating constraints.
3. Add safe environment templates and readiness checks that report missing prerequisites without exposing secrets.
4. Add or document a one-command local startup path for the selected stack where practical.
5. Prove a representative selected-stack workflow against the reference profile with repo-local run, trace, eval,
   durable, and health evidence.
6. Add backup, restore, reset, health, log, trace, rollback, recovery, resource, and cost runbooks.
7. Rehearse a clean setup or fresh-path operation and record evidence and gaps.
8. Present Goal 005 evidence and have an independent reviewer accept or reject it.

## Complexity Tracking

- Multi-service deployment reference: needed because the selected stack includes app, observability, durable runtime, and
  storage concerns. Local fixture-only proof would not satisfy self-hosted operations.
- Controlled infrastructure evidence before final solution: needed because the roadmap needs operations proof before
  every production hardening gap is closed. Calling the stack final from local proof would violate promotion gates.
