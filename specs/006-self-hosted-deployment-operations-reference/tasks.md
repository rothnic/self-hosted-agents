# Tasks: Self-Hosted Deployment And Operations Reference

**Input**: `specs/006-self-hosted-deployment-operations-reference/spec.md`
**Acceptance**: `uv run awf workflow-fixture-test`

## Goal 005 Phase 1: Deployment Contract And Profiles

- [X] T001 [US1] Add a self-hosted deployment operations BDD contract for profiles, smoke evidence, and recovery
- [X] T002 [US1] Define local, development-server, and production-like deployment profiles in `docs/deployment/`
- [X] T003 [US1] Document service boundaries, ports, volumes, secrets, storage paths, and target machines
- [X] T004 [US1] Add environment templates and readiness checks that do not commit credentials

## Goal 005 Phase 2: Reference Stack Startup And Smoke

- [X] T005 [US2] Add or document one-command local startup for the selected Pydantic AI, Langfuse, and DBOS profile
- [X] T006 [US2] Add deployment smoke command or driver for a representative selected-stack workflow
- [X] T007 [US2] Capture repo-local deployment smoke evidence with run, trace, eval, durable, and health correlation
- [X] T008 [US2] Prove deterministic validation remains credential-free when deployment services or secrets are absent

## Goal 005 Phase 3: Operations Runbooks

- [X] T009 [US3] Add backup, restore, and reset runbooks for databases, service state, and run evidence
- [X] T010 [US3] Add health, log, trace, and diagnostics runbooks for app, observability, durable runtime, and storage
- [X] T011 [US3] Add rollback, recovery, retention, resource, and cost notes for one-engineer operation
- [X] T012 [US3] Run a clean-path or fresh setup rehearsal and record evidence, gaps, and follow-up tickets

## Goal 005 Phase 4: Acceptance

- [ ] T013 [US3] Present Goal 005 deployment evidence and record independent reviewer acceptance or rejection
