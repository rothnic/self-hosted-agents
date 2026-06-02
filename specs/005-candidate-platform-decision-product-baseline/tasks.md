# Tasks: Candidate Platform Decision And Product Baseline

**Input**: `specs/005-candidate-platform-decision-product-baseline/spec.md`
**Acceptance**: `uv run awf workflow-fixture-test`

## Phase 1: Goal 004 Evidence Audit

- [ ] T001 [US1] Audit current LangGraph Python, Pydantic AI, and Mastra TypeScript evidence against `docs/comparison-evidence.md`
- [ ] T002 [US1] Decide whether Mastra TypeScript needs a runnable contrast slice before platform selection
- [ ] T003 [US1] Normalize candidate run, trace, evaluation, setup, durable, and gap evidence in `docs/requirements-matrix.md`

## Phase 2: Goal 004 Platform Decision

- [ ] T004 [US2] Score candidates against infrastructure ownership, observability, evaluation, durable execution, scalability, and operating effort
- [ ] T005 [US2] Record the platform decision ADR with selected stack, rejected alternatives, rationale, and promotion blockers
- [ ] T006 [US2] Update roadmap, goal, objective, requirements matrix, and Beads state with the selected primary stack
- [ ] T007 [US2] Present platform decision evidence and record independent reviewer acceptance or rejection

## Phase 3: Goal 004 Product Baseline Definition

- [ ] T008 [US3] Define the first product baseline workflow for the selected stack beyond the comparison demo
- [ ] T009 [US3] Add product-level BDD contracts for the baseline workflow
- [ ] T010 [US3] Add setup and operating notes for the selected stack product baseline

## Phase 4: Goal 004 Candidate Lane Transition

- [ ] T011 [US3] Freeze or archive non-selected candidates as comparison references with explicit tradeoffs
- [ ] T012 [US3] Add migration notes for reusable code, fixtures, or evidence from non-selected lanes
- [ ] T013 [US2] Create follow-up Beads tasks for production hardening gaps that remain after platform selection

## Phase 5: Goal 004 Acceptance

- [ ] T014 [US2] Run Goal 004 increment verification and record reviewer-accepted completion evidence
