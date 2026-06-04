# Tasks: Operator Workbench And Review UX

**Input**: `specs/007-operator-workbench-review-ux/spec.md`
**Acceptance**: `uv run awf workflow-fixture-test`

## Goal 006 Phase 1: Information Architecture And Contracts

- [X] T001 [US1] Research and define the minimum operator views in `docs/workbench/`
- [X] T002 [US1] Add an operator workbench BDD contract for status, evidence, review decisions, and handoffs
- [X] T003 [US1] Define the generated artifact schema for workbench status and decision summaries

## Goal 006 Phase 2: Repo-Backed Status Surfaces

- [X] T004 [US1] Add a consolidated operator status report from goals, specs, Beads, claims, blockers, and validation
- [X] T005 [US1] Add a long-horizon goal dashboard with current phase and accepted evidence links
- [X] T006 [US1] Add an increment dashboard for tickets, claims, blockers, active workers, and validation state
- [X] T007 [US1] Add an evidence view linking run artifacts, traces, evals, Beads comments, branches, and PRs

## Goal 006 Phase 3: Review Actions And Handoffs

- [ ] T008 [US2] Add durable review-gate actions for approve, request changes, defer, and ask questions
- [ ] T009 [US2] Add reviewer decision records with verdict, evidence checked, findings, and follow-up routing
- [ ] T010 [US2] Add branch and PR status integration with repo-local fallback when GitHub access is unavailable
- [ ] T011 [US2] Add trace and eval deep links for self-hosted Langfuse-backed and repo-local evidence
- [ ] T012 [US2] Add concise daily or session handoff summaries for scheduled agents and local sessions

## Goal 006 Phase 4: Interface Decision And Implementation

- [ ] T013 [US3] Decide whether the workbench remains CLI/static or becomes a local UI
- [ ] T014 [US3] Implement the selected interface with restrained operating-tool design
- [ ] T015 [US3] Add accessibility and small-screen review checks if a UI is built, or document why CLI/static remains selected
- [ ] T016 [US3] Document how scheduled agents use the workbench artifacts without a fragile UI dependency

## Goal 006 Phase 5: Acceptance

- [ ] T017 [US3] Present Goal 006 workbench evidence and record independent reviewer acceptance or rejection
