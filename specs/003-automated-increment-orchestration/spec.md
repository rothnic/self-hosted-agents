# Feature Specification: Automated Increment Orchestration

**Feature Branch**: `003-automated-increment-orchestration`
**Created**: 2026-05-10
**Status**: Draft
**Input**: User direction: "Create a repo-native orchestration layer so Codex automations can keep work moving without
manual hand holding, with centralized planning, decentralized execution, and review at increment boundaries."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One Verification Surface (Priority: P1)

As an agent running manually or on a schedule, I can run one command for the current context and receive the checks,
evidence summary, failure details, and next safe action.

**Why this priority**: Agents should not need to remember long hand-built validation checklists.

**Independent Test**: Run `uv run awf verify --profile health --json` and
`uv run awf verify --profile increment --json`; confirm each response includes checks, git state, Beads readiness,
review-gate status, failures, and one `next_action`.

**Acceptance Scenarios**:

1. **Given** a scheduled agent is checking health, **When** it runs the health profile, **Then** it receives the
   lightweight workflow checks and the next safe action.
2. **Given** an increment is being prepared for review, **When** the increment profile runs, **Then** the full workflow
   gate is summarized without requiring the agent to assemble commands.

---

### User Story 2 - Increment State Tracks Decentralized Work (Priority: P1)

As an orchestrator, I can read phase-level increment state and see objective/spec context, child work, worker branches,
claims, blockers, stale claims, validation evidence, and review status.

**Why this priority**: Decentralized workers need shared state that survives session boundaries.

**Independent Test**: Run `uv run awf increment-status --json` and confirm it reports active phase child tickets,
claims, blockers, review status, and a safe next action.

**Acceptance Scenarios**:

1. **Given** a spec phase with open child work, **When** increment status is requested, **Then** the output identifies
   whether PM/review, orchestration, worker, integration, or reviewer acceptance should happen next.
2. **Given** a claim is old or work is blocked, **When** increment status is requested, **Then** stale and blocked work
   remain visible instead of stopping the whole increment silently.

---

### User Story 3 - Scheduled Roles Move Work Without Merging To Main (Priority: P2)

As the project owner, I can allow scheduled roles to plan, assign, implement, verify, and integrate work on feature
branches while independent reviewer acceptance remains at the increment evidence boundary.

**Why this priority**: The project should keep moving without turning every worker step into a manual decision.

**Independent Test**: Run each automation loop in dry form and confirm roles return a bounded action without merging to
`main` or crossing review gates.

**Acceptance Scenarios**:

1. **Given** ready unblocked work exists, **When** the orchestrator loop runs, **Then** it claims one safe item and
   assigns a worker branch.
2. **Given** an increment is complete, **When** the integrator loop verifies it, **Then** it presents evidence for
   independent reviewer acceptance rather than merging to `main`.
3. **Given** a worker hits a blocker, **When** the automation loop reports status, **Then** the blocker is visible to
   the PM/review loop and unblocked work can continue.

## Requirements *(mandatory)*

- **FR-001**: The CLI MUST provide `uv run awf verify --profile <ticket|increment|health|pre-merge> --json`.
- **FR-002**: `verify` MUST run the context-appropriate workflow checks and return a single `next_action`.
- **FR-003**: `verify --write` MUST store compact handoff evidence under `.agent-runs/verifications/`.
- **FR-004**: Increment state MUST be represented as `.agent-runs/increments/<increment-id>.json`.
- **FR-005**: Increment state MUST include objective, spec, phase, feature branch, child tickets, active claims,
  blockers, stale claims, validation evidence, review status, and learning proposals when present.
- **FR-006**: Increment membership SHOULD use normal Beads epics, dependencies, comments, and labels instead of a
  custom Beads schema.
- **FR-007**: Automation MUST split PM/review, orchestrator, worker, integrator, and health concerns.
- **FR-008**: Workers MUST act on one claimed ticket and must not close it without passing verification evidence.
- **FR-009**: Blocked work MUST be recorded and visible; one blocker MUST NOT idle the whole increment unless it blocks
  all remaining work through dependencies.
- **FR-010**: Integrators and scheduled workers MUST NOT merge to `main`.
- **FR-011**: Increment evidence MUST be accepted or rejected by an independent reviewer agent unless the user has
  explicitly reserved the decision.
- **FR-012**: The workflow fixture MUST cover verification, backlog creation behavior, work selection, evidence
  recording, reviewer acceptance routing, and blocker rerouting.
- **FR-013**: The automation loops MUST expose stale active claims with enough age, worker, branch, and issue context
  for another agent to resume, reassign, or archive them.
- **FR-014**: Worker branch and worktree guidance MUST be deterministic from issue metadata so scheduled workers do not
  depend on hidden local branch naming conventions.
- **FR-015**: Integrator output MUST verify worker branches and prepare reviewer-facing evidence without merging to
  `main` or bypassing the draft PR review boundary.
- **FR-016**: Health loops MUST create actionable repo-local issue evidence for recurring workflow failures instead of
  only printing transient command output.
- **FR-017**: Operators MUST be able to inspect active claims, stale claims, blockers, ready work, and next actions from
  one compact status surface.
- **FR-018**: Cleanup behavior MUST preserve historical evidence while removing obsolete active claims and worktree
  pointers that would misroute future scheduled workers.

### Key Entities

- **Increment Ledger**: Phase-level state file under `.agent-runs/increments/`.
- **Verification Artifact**: Compact run output under `.agent-runs/verifications/`.
- **Automation Role**: One scheduled concern: PM/review, orchestrator, worker, integrator, or health.
- **Worker Branch**: Focused branch for one claimed ticket, normally targeting the increment feature branch.
- **Review Gate**: A boundary for reviewer acceptance or unresolved product, architecture, priority, or scope.

## Success Criteria *(mandatory)*

- **SC-001**: Agents can run one verification command for ticket, increment, health, and pre-merge contexts.
- **SC-002**: Increment status answers what should happen next from repo state without human CLI operation.
- **SC-003**: Scheduled loops can return safe next actions for PM/review, orchestrator, worker, integrator, and health.
- **SC-004**: The workflow fixture validates that automation routes increment evidence to review instead of merging to
  `main`.
- **SC-005**: Blocked and stale work are visible to planning loops, while unrelated unblocked work can continue.

## Assumptions

- Codex app automations are the initial scheduler, using worktrees where useful.
- Repo state, Beads, and `.agent-runs/` remain authoritative over any specific runner.
- Subagents may help with read-heavy review or research but are not required for orchestration.
- Actual scheduling of Codex app automations happens after this repo-native command surface passes manual validation.

## Goal 003 Product Iteration Alignment

The first eight tasks established the orchestration command surface. Goal 003 now reopens this feature for the next
product iteration: making the scheduled PM, orchestrator, worker, integrator, and health loops reliable enough for real
cross-session delivery on controlled infrastructure.

This iteration is complete only when the repo can prove:

- a scheduled worker can claim, verify, and hand off one ticket from a deterministic worker branch/worktree path;
- stale and blocked work stay visible while unrelated ready work can continue;
- integrator output prepares independent reviewer evidence without merging to `main`;
- health automation records durable, actionable issue evidence for recurring failures;
- another agent can inspect compact active-work status and resume without hidden local context;
- the workflow fixture covers the key role transitions and blocked-state recovery paths.

The remaining Goal 003 work is decomposed in `specs/003-automated-increment-orchestration/tasks.md` beginning at T009.
