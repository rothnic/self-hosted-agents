# Tasks: Automated Increment Orchestration

**Input**: `specs/003-automated-increment-orchestration/spec.md`
**Acceptance**: `uv run awf verify --profile increment --json`

## Phase 1: Contract And State Model

- [X] T001 [US1] Add the automated increment orchestration BDD contract
- [X] T002 [US2] Document the increment ledger and verification artifact storage paths

## Phase 2: Verification And Status Commands

- [X] T003 [US1] Add `uv run awf verify` profiles for ticket, increment, health, and pre-merge
- [X] T004 [US2] Add increment status and plan commands for phase-level state

## Phase 3: Scheduled Role Loops

- [X] T005 [US3] Add automation loop roles for PM/review, orchestrator, worker, integrator, and health
- [X] T006 [US3] Define blocked-work, stale-claim, and human-review handoff behavior

## Phase 4: Codex Automation Rollout

- [X] T007 [US3] Draft Codex app automation prompts for the five scheduled roles
- [X] T008 [US3] Run one manual worktree dry run before scheduling background automations
