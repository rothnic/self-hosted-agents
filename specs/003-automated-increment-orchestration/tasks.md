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

## Phase 5: Goal 003 Scheduled Delivery Baseline

- [X] T009 [US2] Audit current PM, orchestrator, worker, integrator, and health automation-loop behavior
- [X] T010 [US2] Define the minimum safe scheduled loop for one active increment
- [X] T011 [US3] Add stale-claim status and handoff guidance for abandoned active work
- [X] T012 [US3] Add blocker rerouting so unrelated ready work can continue
- [X] T013 [US3] Add deterministic worker branch naming and worktree setup guidance

## Phase 6: Goal 003 Handoff And Recovery Surfaces

- [X] T014 [US1] Add compact verification artifacts for ticket and increment profiles
- [X] T015 [US3] Add integrator verification of worker branches without merging to `main`
- [ ] T016 [US3] Add review-agent invocation guidance before PR and increment handoffs
- [ ] T017 [US3] Add health-loop issue logging for recurring workflow failures
- [ ] T018 [US3] Add dry-run fixtures for role transitions and blocked-state recovery

## Phase 7: Goal 003 Operator Visibility And Acceptance

- [ ] T019 [US3] Add compact active-work summaries for claims, ready work, blockers, and stale work
- [ ] T020 [US3] Add cleanup commands for obsolete active claims and old worktree pointers
- [ ] T021 [US3] Run a manual end-to-end increment rehearsal and record reviewer-accepted evidence
