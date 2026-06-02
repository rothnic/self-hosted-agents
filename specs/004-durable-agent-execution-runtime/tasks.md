# Tasks: Durable Agent Execution Runtime

**Input**: `specs/004-durable-agent-execution-runtime/spec.md`
**Acceptance**: `uv run awf workflow-fixture-test`

## Phase 1: Durable Contract And Review Model

- [X] T001 [US1] Add a durable execution BDD contract for retry, resume, wait, and side-effect evidence
- [X] T002 [US1] Update DBOS selection scoring and final-promotion blockers in `docs/requirements-matrix.md`
- [X] T003 [US1] Document local DBOS setup, storage reset, recovery, and troubleshooting for another agent

## Phase 2: Failure Recovery Smoke

- [X] T004 [US2] Extend the Pydantic AI DBOS smoke with a controlled retry proof
- [X] T005 [US2] Harden the restart/resume smoke so run identity survives process interruption
- [X] T006 [US2] Record side-effect idempotency evidence across retry and resume in the durable artifact

## Phase 3: Review-Safe Review Wait

- [X] T007 [US3] Add a fixture-safe review wait that stops without reviewer acceptance evidence
- [ ] T008 [US3] Add durable resume from independent reviewer acceptance evidence
- [ ] T009 [US3] Link wait, reviewer, resume, trace, eval, and Beads ids in the durable run artifact

## Phase 4: Promotion Evidence And Follow-Ups

- [ ] T010 [US1] Add workflow fixture assertions for the durable evidence shape
- [ ] T011 [US1] Update roadmap, requirements, and promotion gates with the durable proof result
- [ ] T012 [US1] Record reviewer acceptance and follow-up tickets for production hardening gaps
