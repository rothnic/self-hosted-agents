# Tasks: Agent Workflow Foundation

**Input**: Design documents from `/specs/001-workflow-foundation/`
**Prerequisites**: `plan.md`, `spec.md`
**Tests**: Workflow fixture, BDD fixture driver, Spec Kit lint, repo hygiene, pre-commit hook.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel when files do not overlap.
- **[Story]**: User story from `spec.md`.
- Include exact file paths in descriptions.

## Phase 1: Spec Kit Substrate (Shared Infrastructure)

- [x] T001 [US1] Initialize Spec Kit substrate in `.specify/`
- [x] T002 [US1] Install Spec Kit Codex skills under `.agents/skills/speckit-*`
- [x] T003 [US1] Write project constitution in `.specify/memory/constitution.md`
- [x] T004 [US1] Remove custom non-native spec templates from `specs/`
- [x] T005 [US1] Add `uv run awf spec-kit-lint` for Spec Kit substrate validation

---

## Phase 2: Environment And CLI Foundation

- [x] T006 [US1] Create `tools/agent-workflow/bootstrap-dev.sh`
- [x] T007 [US1] Configure `uv`, `pyproject.toml`, and `awf` CLI entrypoint
- [x] T008 [US1] Install and initialize Beads Rust through bootstrap
- [x] T009 [US1] Add versioned git hook in `.githooks/pre-commit`
- [x] T010 [US1] Add repo hygiene policy in `.agents/project-policy.json`

---

## Phase 3: Planning And Human Gates

- [x] T011 [US2] Add `AGENTS.md` state machine and skill routing
- [x] T012 [US2] Add PM steward, review gatekeeper, reviewer, test steward, and retrospector skills
- [x] T013 [US2] Implement `uv run awf workflow-run --mode plan`
- [x] T014 [US2] Implement `uv run awf review-gate`
- [x] T015 [US2] Implement `uv run awf issue-log --write`

---

## Phase 4: Worker Orchestration

- [x] T016 [US3] Implement ready work discovery with Beads fallback behavior
- [x] T017 [US3] Implement claim files under `.agent-runs/claims/`
- [x] T018 [US3] Implement planner and worker cron ticks
- [x] T019 [US3] Document cron orchestration in `docs/orchestration/cron-workflow.md`

---

## Phase 5: Behavior Contracts And Fixture Validation

- [x] T020 [US4] Add BDD contract skill and driver boundary guidance
- [x] T021 [US4] Add `tests/workflow/features/agent_workflow_foundation.feature`
- [x] T022 [US4] Add fixture driver under `tests/workflow/drivers/`
- [x] T023 [US4] Add isolated fixture under `tests/workflow/fixtures/sample-project/`
- [x] T024 [US4] Implement `uv run awf workflow-fixture-test`

---

## Phase 6: Review Before Product Work

- [ ] T025 [P] [US1] Run `tools/agent-workflow/bootstrap-dev.sh`
- [ ] T026 [P] [US1] Run `uv run awf spec-kit-lint`
- [ ] T027 [P] [US4] Run `uv run awf bdd-lint && uv run awf bdd-run --driver fixture`
- [ ] T028 [P] [US2] Run `uv run awf review-gate`
- [ ] T029 [P] [US1] Run `uv run awf repo-hygiene`
- [ ] T030 [US4] Run `uv run awf workflow-fixture-test`
- [ ] T031 [US2] Human review of the foundation before product implementation

## Dependencies & Execution Order

- Phase 1 blocks all future specification work.
- Phase 2 blocks recurring agent execution.
- Phase 3 blocks autonomous planning and review gates.
- Phase 4 blocks cron-style workers.
- Phase 5 blocks product implementation.
- Phase 6 is the approval gate before LangGraph, Mastra, RAG, frontend, or product workflow work begins.
