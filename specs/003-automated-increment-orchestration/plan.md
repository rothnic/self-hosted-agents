# Implementation Plan: Automated Increment Orchestration

**Branch**: `003-automated-increment-orchestration` | **Date**: 2026-05-10 |
**Spec**: `specs/003-automated-increment-orchestration/spec.md`

## Summary

Add a repo-native orchestration layer that gives agents one verification command, phase-level increment state, and
scheduled role loops for PM/review, orchestration, worker execution, integration, and health. Codex app automations can
run these commands later, but repo artifacts remain the durable state and review boundary.

## Technical Context

**Language/Version**: Python 3.14 for the `awf` CLI.
**Primary Dependencies**: Existing Typer/Rich/Pydantic CLI stack, Beads Rust `br`, Spec Kit artifacts.
**Storage**: `.agent-runs/increments/`, `.agent-runs/verifications/`, `.agent-runs/claims/`, `.beads/issues.jsonl`.
**Testing**: `uv run awf verify --profile increment --json`, BDD fixture driver, workflow fixture test.
**Target Platform**: Local Codex sessions, Codex app automations, CI-like runners, and worktree-backed agents.
**Project Type**: Workflow foundation repo with future product apps under `apps/`.
**Constraints**: Do not merge to `main` from scheduled roles. Do not fork Beads schema while labels and ledgers suffice.

## Constitution Check

- Repository artifacts are the source of truth: PASS.
- Human gates prevent drift: PASS; routine workers stop before `main`.
- Testable behavior comes before implementation: PASS through BDD and fixture coverage.
- Small slices and traceable tickets: PASS through Beads claims and increment child tickets.
- Alpha means no compatibility debt: PASS; new commands extend the current `awf` surface directly.

## Project Structure

```text
.agent-runs/
├── increments/
└── verifications/

docs/
└── orchestration/
    └── cron-workflow.md

specs/
└── 003-automated-increment-orchestration/

tests/
└── workflow/
    ├── drivers/
    └── features/

tools/
└── agent-workflow/
    └── src/agent_workflow/
```

## Phased Plan

1. Document the increment state machine and automation roles.
2. Add implementation-agnostic BDD contracts for scheduled orchestration.
3. Implement `awf verify` profiles and verification artifacts.
4. Implement increment status and plan commands for phase ledgers.
5. Implement automation loops for PM/review, orchestrator, worker, integrator, and health.
6. Run manual validation, then create Codex app automations in a separate scheduling slice.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| Multiple automation roles | Work needs independent cadence and failure handling | One loop would mix planning, claims, integration, and health concerns |
| Increment ledgers | Session and worktree state must survive agent restarts | Beads alone does not hold phase review state or validation summaries |
| Verification profiles | Agents need one safe command per context | Hand-maintained checklists caused manual orchestration friction |
