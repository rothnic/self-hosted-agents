# Feature Specification: Operator Workbench And Review UX

**Feature Branch**: `007-operator-workbench-review-ux`
**Created**: 2026-06-04
**Status**: Draft
**Input**: Goal 006 from `docs/goals/006-operator-workbench-review-ux.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decision Status Is Inspectable (Priority: P1)

As the project owner, I can inspect one concise operator surface and see the active objective, ordered goals, current
spec, Beads work, claims, blockers, validation state, traces, evals, PRs, and next decision without assembling raw CLI
output by hand.

**Why this priority**: The roadmap is now broad enough that context bloat and raw artifact spelunking slow down product
direction. Goal 006 must make the system operator-visible before adding deeper product workflows.

**Independent Test**: Run the operator status command or regenerate the workbench artifact; confirm it links goals,
specs, tickets, claims, blockers, run evidence, traces, evals, branches, PRs, and the next action from repo state.

**Acceptance Scenarios**:

1. **Given** the repo has accepted goals, active specs, Beads issues, run evidence, and a draft PR, **When** the operator
   surface is generated, **Then** it shows the current roadmap phase and next decision with links to source artifacts.
2. **Given** there are no ready worker tickets, **When** the operator surface is generated, **Then** it routes to planning
   or backlog sync instead of presenting a false implementation task.

---

### User Story 2 - Review Decisions Are Durable (Priority: P1)

As an agent operator, I can approve, request changes, defer, or ask a question on goal or increment evidence, and the
decision is recorded in durable repo artifacts that another agent can inspect.

**Why this priority**: Human review should not be a hidden chat dependency. The project standard is presenter evidence
plus independent reviewer acceptance or rejection, with human escalation only for explicitly reserved or contradictory
decisions.

**Independent Test**: Exercise the review-gate action flow or fixture driver; confirm decisions are written to repo-local
artifacts, linked to the relevant goal/spec/ticket/run evidence, and visible through workflow status.

**Acceptance Scenarios**:

1. **Given** presenter evidence exists for a ticket, increment, or goal, **When** a reviewer accepts or rejects it,
   **Then** the workbench records reviewer id, verdict, evidence checked, findings, and follow-up routing.
2. **Given** a reviewer asks a question or defers, **When** status is regenerated, **Then** the unresolved decision is
   visible without requiring prior chat context.

---

### User Story 3 - The Workbench Stays Self-Hosted And Automation-Compatible (Priority: P2)

As a maintainer, I can evolve the workbench from CLI/static reports to a local UI only when the evidence shows that
the interface improves operations without hiding repo source-of-truth artifacts.

**Why this priority**: A UI can help, but an early fragile product surface would create maintenance cost and could
encourage agents to bypass CLI and repo-backed workflows.

**Independent Test**: Inspect the interface decision record, docs, and fixture coverage; confirm scheduled agents can
still operate through CLI artifacts and the selected interface can be regenerated from repo state.

**Acceptance Scenarios**:

1. **Given** the workbench interface decision is reviewed, **When** CLI/static and local UI options are compared, **Then**
   the decision records operating burden, self-hosting requirements, accessibility, small-screen review, and automation
   compatibility.
2. **Given** scheduled agents run PM, worker, integrator, or health loops, **When** they produce handoffs, **Then** those
   handoffs are visible through the workbench artifacts without relying on a hosted service.

## Requirements *(mandatory)*

- **FR-001**: Goal 006 MUST define the operator information architecture for objectives, goals, specs, Beads issues,
  claims, blockers, validations, review gates, traces, evals, branches, and PRs.
- **FR-002**: The workbench MUST be generated from repo state and workflow commands, not hidden chat context.
- **FR-003**: The workbench MUST link Beads issues to run artifacts, trace views, eval reports, claims, reviewer
  decisions, and PR evidence when those artifacts exist.
- **FR-004**: The workbench MUST expose the current next action and explain whether the next owner is PM, planner,
  implementer, test steward, reviewer, integrator, or health steward.
- **FR-005**: Review actions MUST support approve, request changes, defer, and ask questions.
- **FR-006**: Review decisions MUST be durable, repo-local, reviewer-attributed, and inspectable by another agent.
- **FR-007**: Goal and increment evidence MUST use presenter evidence plus independent reviewer acceptance or rejection;
  human review MUST NOT block progress unless a decision is explicitly reserved, missing, or contradicted.
- **FR-008**: Deterministic fixture validation MUST remain valid without hosted services, cloud credentials, or GitHub
  access.
- **FR-009**: GitHub branch and PR status SHOULD be integrated when available, but absent GitHub access MUST degrade to
  explicit repo-local status rather than blocking validation.
- **FR-010**: Trace and eval links SHOULD prefer self-hosted Langfuse-backed views when available and MUST preserve
  repo-local fallback artifact links.
- **FR-011**: Session and scheduled-agent handoff summaries MUST be concise enough to reduce context bloat while keeping
  exact artifact handles.
- **FR-012**: Any local UI decision MUST preserve CLI/static workflows for automation and testability.
- **FR-013**: If a UI is built, accessibility and small-screen review checks MUST be added before goal acceptance.
- **FR-014**: Goal 006 completion evidence MUST be presented by one agent and accepted or rejected by an independent
  reviewer agent.

### Key Entities

- **Operator Workbench**: A CLI report, static artifact, local UI, or selected combination that summarizes workflow
  state and decision options from repo artifacts.
- **Operator View**: A focused status slice for roadmap, increment, evidence, review gate, traces/evals, PRs, or
  handoffs.
- **Review Decision**: A durable approval, rejection, defer, or question record attributed to a reviewer and linked to
  evidence.
- **Evidence Link**: A repo-relative or self-hosted URL pointing to run reports, traces, evals, Beads comments, PRs, or
  validation artifacts.
- **Handoff Summary**: A compact session or scheduled-agent artifact that names current state, exact next work, validation
  evidence, and risks.

## Success Criteria *(mandatory)*

- **SC-001**: Another agent can regenerate a decision-ready operator status surface from repo state.
- **SC-002**: The project owner can identify what is happening, what is blocked, and what decision is needed without
  reading raw workflow dumps.
- **SC-003**: Review decisions are durable, reviewer-attributed, evidence-linked, and visible through status.
- **SC-004**: Trace, eval, run, ticket, branch, and PR evidence are connected where available, with credential-free
  repo-local fallback links.
- **SC-005**: Scheduled agents can continue operating through CLI and repo artifacts even if no UI is running.

## Assumptions

- The first Goal 006 implementation should favor CLI/static artifacts until a reviewed interface decision justifies a
  local UI.
- The selected product baseline remains Pydantic AI plus self-hosted-compatible Langfuse and DBOS.
- GitHub access is useful for PR status but is not required for deterministic validation.
