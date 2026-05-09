# Feature Specification: Agent Workflow Foundation

**Feature Branch**: `001-workflow-foundation`
**Created**: 2026-05-09
**Status**: Draft
**Input**: User description: "Establish the agent workflow foundation using Spec Kit-managed artifacts"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agent Starts From Maintained Context (Priority: P1)

As a coding agent, I can start in a fresh local, CI, Codex, or cloud environment and discover the current project state,
required tools, objectives, tickets, specs, checks, and next safe action from repo artifacts.

**Why this priority**: Every recurring or delegated agent run depends on a reliable startup path.

**Independent Test**: Run bootstrap, context index, and health status from a fresh checkout and confirm they report the
project state without requiring hidden local context.

**Acceptance Scenarios**:

1. **Given** a fresh checkout, **When** an agent runs `tools/agent-workflow/bootstrap-dev.sh --install-tools`,
   **Then** required tools, hooks, Beads Rust, Spec Kit substrate, and the `awf` CLI are available or clearly reported.
2. **Given** an initialized environment, **When** an agent runs `uv run awf context-index`,
   **Then** objectives, Spec Kit features, BDD contracts, tickets, blockers, ADRs, research, and recent runs are summarized.
3. **Given** a healthy harness, **When** an agent runs `uv run awf health-status --deep`,
   **Then** the command reports the next safe action and includes workflow, Spec Kit, BDD, review-gate, and repo hygiene checks.

---

### User Story 2 - Planner Keeps Work Aligned (Priority: P1)

As a PM-like agent, I can review objectives, specs, tickets, checks, recent runs, and learnings, then produce planning
output or stop for human review when intent is unclear.

**Why this priority**: The workflow must prevent drift before agents perform implementation work.

**Independent Test**: Run a planning workflow against the isolated fixture and confirm stale or ambiguous state blocks
unsafe continuation.

**Acceptance Scenarios**:

1. **Given** maintained objectives and run artifacts, **When** the planner runs `uv run awf workflow-run --mode plan`,
   **Then** the report includes context, risks, next action, and whether a human gate is required.
2. **Given** unresolved questions or blocked-state files, **When** `uv run awf review-gate` runs,
   **Then** it exits non-zero and reports the blocked artifacts.
3. **Given** a health issue, **When** `uv run awf issue-log --write` runs,
   **Then** it records a durable health artifact and creates a Beads task when `br` is available.

---

### User Story 3 - Worker Executes One Verified Slice (Priority: P2)

As an implementation agent, I can claim one ready item, make the smallest coherent change, run the required acceptance
checks, and leave follow-up work as tickets instead of hidden context.

**Why this priority**: Recurring agents need safe work separation before product implementation starts.

**Independent Test**: Run the worker cron tick against ready work and confirm it claims at most one unclaimed task.

**Acceptance Scenarios**:

1. **Given** ready Beads work, **When** a worker runs `uv run awf claim-work --worker-id worker-1 --write`,
   **Then** one claim is recorded under `.agent-runs/claims/`.
2. **Given** no ready or safe work, **When** a worker runs `uv run awf cron-tick --role worker --worker-id worker-1`,
   **Then** it exits without making product changes.
3. **Given** a discovered follow-up, **When** the worker cannot complete it safely,
   **Then** it logs the issue through the normal workflow rather than silently skipping it.

---

### User Story 4 - Behavior Contracts Stay Implementation-Agnostic (Priority: P2)

As a reviewer or test steward, I can express expected end-to-end behavior through BDD contracts and run a driver that
verifies actor outcomes plus operational evidence without coupling to Mastra, LangGraph, frontend, or cloud services.

**Why this priority**: The future product will compare multiple framework implementations against the same behavior.

**Independent Test**: Run BDD lint and the fixture driver and confirm contracts include actors, operational assertions,
and a driver boundary.

**Acceptance Scenarios**:

1. **Given** BDD feature files, **When** `uv run awf bdd-lint` runs,
   **Then** every feature includes an actor, operational assertion, and implementation driver boundary.
2. **Given** the fixture driver, **When** `uv run awf bdd-run --driver fixture` runs,
   **Then** it returns deterministic observations for the workflow foundation scenario.

### Edge Cases

- If `br` is unavailable, the workflow reports the missing tool and tells agents how to bootstrap it.
- If Spec Kit substrate is missing or a non-native folder is placed under `specs/`, validation fails.
- If a cron worker sees claimed, blocked, or ambiguous work, it exits after logging the issue.
- If a generated artifact or cache appears in the repo, repo hygiene fails before the task is considered complete.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide `AGENTS.md` as the minimal agent entrypoint with role routing and safety rules.
- **FR-002**: The system MUST use `.specify/` and Spec Kit-managed `specs/` for feature specifications.
- **FR-003**: The system MUST reject non-native spec folders under `specs/`.
- **FR-004**: The system MUST provide role/task skills for planning, specs, research, ticketing, implementation, review, tests, gates, and retrospectives.
- **FR-005**: The system MUST expose a single `uv run awf` CLI for bootstrap, context, health, Spec Kit lint, BDD lint/run, review gates, tickets, and reports.
- **FR-006**: The system MUST use Beads Rust as the local-first ticket backend when available.
- **FR-007**: The system MUST link implementation work to objectives, specs or Spec Kit feature artifacts, tickets, and acceptance checks.
- **FR-008**: The system MUST support dry-run behavior by default and require explicit `--write` for mutations.
- **FR-009**: The system MUST provide cron-safe planner, worker, and health modes.
- **FR-010**: The system MUST keep worker work separated through Beads ready work and `.agent-runs/claims/`.
- **FR-011**: The system MUST provide implementation-agnostic BDD contracts and driver boundaries.
- **FR-012**: The system MUST provide an isolated workflow fixture that proves the process without product implementation.
- **FR-013**: The system MUST enforce repo hygiene for root clutter, generated artifacts, directory size, and line length.
- **FR-014**: The system MUST maintain alpha policy: no shims, compatibility adapters, deprecated paths, duplicate APIs, or migration layers.

### Key Entities

- **Objective**: Durable statement of project intent, success criteria, constraints, and non-goals.
- **Spec Kit Feature**: Native `spec.md`, `plan.md`, and `tasks.md` artifacts under `specs/<number>-<short-name>/`.
- **Ticket**: Beads Rust work item with objective or feature context and acceptance evidence.
- **Run Manifest**: Durable record of trigger type, mode, context, changed artifacts, checks, and next action.
- **Health Issue**: Structured problem report that can become a Beads ticket.
- **BDD Contract**: Implementation-agnostic feature file with actor outcomes and operational assertions.
- **Claim**: Worker ownership record for one ready task.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `tools/agent-workflow/bootstrap-dev.sh` completes on a fresh environment and installs required local tooling.
- **SC-002**: `uv run awf health-status --deep` passes and reports the next safe action.
- **SC-003**: `uv run awf spec-kit-lint` passes only when `.specify/` and native Spec Kit artifacts are valid.
- **SC-004**: `uv run awf workflow-fixture-test` proves the isolated workflow fixture.
- **SC-005**: `.githooks/pre-commit` rejects repo hygiene violations before commit.
- **SC-006**: A dry-run `uv run awf spec-new workflow-foundation "<description>"` reports a Spec Kit feature path.

## Assumptions

- The first product implementation is deferred until this workflow foundation passes validation.
- The repo may run locally, in Codex, in CI, or in a cloud agent service.
- Repo artifacts are the durable state layer; runtime environments are replaceable.
- Spec Kit is the specification substrate, not a hosted dependency.
- Beads Rust is installed locally through bootstrap and stores tracked issue state in `.beads/issues.jsonl`.
