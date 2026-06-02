# Feature Specification: Durable Agent Execution Runtime

**Feature Branch**: `004-durable-agent-execution-runtime`
**Created**: 2026-06-01
**Status**: Draft
**Input**: Goal 002 from `docs/goals/002-durable-agent-execution-runtime.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Durable Runtime Selection Is Evidence-Based (Priority: P1)

As an agent maintainer, I can inspect why the first durable runtime was selected and which alternatives remain open.

**Why this priority**: Durable runtime work should not turn the DBOS smoke into an unreviewed final platform choice.

**Independent Test**: Inspect the durable selection note, requirements matrix, and Beads comments; confirm DBOS is
selected only for the next proof and alternatives remain visible.

**Acceptance Scenarios**:

1. **Given** the durable runtime options, **When** the selection evidence is reviewed, **Then** DBOS, Prefect, Restate,
   Temporal, and Hatchet are scored against local setup, operator burden, recovery behavior, and scale path.
2. **Given** DBOS is selected for the next proof, **When** matrix scoring is updated, **Then** final-solution promotion
   remains blocked until retry, review wait, production storage, workers, and recovery are proven.

---

### User Story 2 - Durable Smoke Proves Failure Recovery (Priority: P1)

As an operator, I can run one local smoke that proves retry, resume, and side-effect safety for the tested Pydantic AI
candidate lane.

**Why this priority**: The system needs recoverable execution evidence, not only successful fixture runs.

**Independent Test**: Run the durable smoke command and inspect the repo-local evidence artifact for retry count,
resume identity, one side-effect record, Pydantic AI run id, trace id, and evaluation id.

**Acceptance Scenarios**:

1. **Given** a controlled transient failure, **When** the durable smoke runs, **Then** the workflow retries and completes
   without losing run identity.
2. **Given** a process restart after a completed side-effect step, **When** the workflow resumes, **Then** the side
   effect is not duplicated.

---

### User Story 3 - Durable Review Wait Is Review-Safe (Priority: P1)

As an automation operator, I can pause a durable agent workflow for review and resume it only after reviewer acceptance
is recorded in repo state.

**Why this priority**: Scheduled agents must not bypass review gates while trying to be durable.

**Independent Test**: Run a fixture-safe review-wait smoke and confirm the waiting state, reviewer acceptance artifact,
resume event, and final run artifact are linked.

**Acceptance Scenarios**:

1. **Given** a durable workflow reaches a review wait, **When** no acceptance artifact exists, **Then** the workflow
   records a waiting state and does not continue side effects.
2. **Given** an independent reviewer acceptance exists, **When** the workflow resumes, **Then** it continues with the
   same durable run id and links the acceptance evidence.

## Requirements *(mandatory)*

- **FR-001**: The durable runtime selection MUST compare DBOS, Prefect, Restate, Temporal, and Hatchet.
- **FR-002**: The first implementation MAY deepen the existing Pydantic AI plus DBOS lane, but MUST keep final platform
  selection blocked until the full durable evidence exists.
- **FR-003**: Durable evidence MUST prove retry after controlled failure.
- **FR-004**: Durable evidence MUST prove resume after process interruption.
- **FR-005**: Durable evidence MUST prove side-effect idempotency across retry or resume.
- **FR-006**: Durable evidence MUST prove a review wait that resumes only after durable reviewer acceptance exists.
- **FR-007**: Durable run artifacts MUST link durable run id, Pydantic AI run id, trace id, eval id, and Beads evidence.
- **FR-008**: Runtime setup docs MUST describe local startup, storage, reset, recovery, and troubleshooting.
- **FR-009**: Deterministic fixture validation MUST pass without hosted services, external model providers, or cloud
  credentials.
- **FR-010**: Follow-up Beads tickets MUST capture production storage, worker scaling, and recovery gaps that remain
  after the local proof.

### Key Entities

- **Durable Runtime**: The selected workflow engine or library used to retry, resume, wait, and protect side effects.
- **Durable Run Artifact**: Repo-local JSON evidence for durable execution, linked to trace, eval, and Beads evidence.
- **Review Wait**: A durable pause that requires an independent reviewer acceptance artifact before resuming.
- **Side-Effect Record**: An idempotency proof that a durable step ran exactly once despite retry or resume.

## Success Criteria *(mandatory)*

- **SC-001**: A reviewer can identify the selected runtime and see why alternatives were not chosen for this proof.
- **SC-002**: The durable smoke artifact proves retry, resume, review wait, and side-effect idempotency.
- **SC-003**: Durable run evidence is correlated with observability and evaluation artifacts.
- **SC-004**: Another agent can reproduce the local durable runtime setup from repo docs.
- **SC-005**: Requirements scoring distinguishes local smoke evidence from production-ready durable operations.

## Assumptions

- DBOS remains the first proof path because T024/T025 already selected and smoke-tested it for the Pydantic AI lane.
- Production storage, distributed workers, and recovery rehearsal can be follow-up work if the local proof is complete.
- Independent reviewer acceptance is sufficient for goal evidence unless the user explicitly reserves a decision.
