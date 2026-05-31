# Tasks: Solution Comparison Roadmap

**Input**: `specs/002-solution-comparison-roadmap/spec.md`
**Acceptance**: `uv run awf workflow-fixture-test`

## Phase 1: Requirements And Research

- [X] T001 [US2] Create `docs/requirements-matrix.md` mapping high-level needs to candidate solution fit
- [X] T002 [US2] Expand `docs/research/llm-observability-solution-space.md` with candidate-specific integration notes
- [X] T003 [US2] Define evaluation criteria for observability, evaluation, scalability, and operating effort

## Phase 2: Shared Comparison Harness

- [X] T004 [US3] Define shared behavior contract for the first comparable agent workflow
- [X] T005 [US3] Define shared trace and evaluation evidence expected from each candidate app
- [X] T006 [US3] Document where shared packages, fixtures, and app-local implementation code belong

## Phase 3: Candidate App Planning

- [X] T007 [US3] Propose the first Python-first candidate app slice based on the requirement matrix
- [X] T008 [US3] Propose the second comparison candidate and explain why it provides useful contrast
- [X] T009 [US3] Define the minimum demo needed to compare candidate implementations

## Phase 4: Roadmap Review

- [X] T010 [US1] Produce a CEO-level roadmap review with recommendation, options, and targeted questions
- [X] T011 [US1] Record the human roadmap decision in the objective, spec, and Beads backlog
- [X] T012 [US1] Sync approved implementation tasks into Beads only after roadmap approval

## Phase 5: Approved First Candidate Implementation

- [X] T013 [US3] Define the `langgraph-python` functional-needs mapping and implementation slice plan
- [X] T014 [US3] Scaffold the runnable `apps/langgraph-python/` comparable workflow with deterministic fixture support
- [X] T015 [US3] Add Langfuse or OpenTelemetry trace evidence capture for the LangGraph Python slice
- [X] T016 [US3] Add evaluation output and run artifact capture for the LangGraph Python slice
- [X] T017 [US3] Update the requirements matrix with LangGraph Python evidence, scores, and gaps
- [X] T018 [US3] Research Pydantic AI plus Logfire/OpenTelemetry against the functional needs map

## Phase 6: Approved Pydantic AI And Durable Execution Evaluation

- [X] T019 [US2] Update comparison criteria for hosted observability and durable execution requirements
- [X] T020 [US3] Define the `pydantic-ai` implementation slice plan with Logfire evidence
- [X] T021 [US3] Scaffold the runnable `apps/pydantic-ai/` comparable workflow with deterministic fixture support
- [X] T022 [US3] Add self-hosted-compatible OpenTelemetry trace evidence capture for the Pydantic AI slice
- [ ] T027 [US3] Prove self-hosted Langfuse ingestion for the Pydantic AI trace path
- [ ] T023 [US3] Add Pydantic Evals output and run artifact capture for the Pydantic AI slice
- [ ] T024 [US3] Compare durable execution options for Pydantic AI and Python workflow candidates
- [ ] T025 [US3] Add a durable execution smoke path for the lowest-complexity selected option
- [ ] T026 [US3] Update the requirements matrix with Pydantic AI evidence, scores, and promotion gaps
