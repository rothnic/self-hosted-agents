# Feature Specification: Candidate Platform Decision And Product Baseline

**Feature Branch**: `005-candidate-platform-decision-product-baseline`
**Created**: 2026-06-02
**Status**: Draft
**Input**: Goal 004 from `docs/goals/004-candidate-platform-decision-product-baseline.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decision-Ready Candidate Evidence (Priority: P1)

As the project owner, I can inspect normalized implementation evidence for the current candidate stacks and understand
which evidence is strong enough for a platform decision.

**Why this priority**: The project cannot choose a primary stack from preference or stale research; the decision needs
run, trace, evaluation, setup, durable, and gap evidence from comparable slices.

**Independent Test**: Inspect the Goal 004 evidence audit and comparison matrix updates; confirm every scored candidate
links to implementation evidence or is explicitly marked as deferred, missing, or not comparable.

**Acceptance Scenarios**:

1. **Given** completed Goal 001 through Goal 003 evidence, **When** Goal 004 starts, **Then** the agent audits
   LangGraph Python, Pydantic AI, and Mastra TypeScript evidence against the same checklist.
2. **Given** a candidate lacks runnable evidence, **When** the matrix is updated, **Then** the candidate is not scored
   as implementation-proven and the missing evidence is recorded as a blocker or explicit deferral.

---

### User Story 2 - Evidence-Based Platform Decision (Priority: P1)

As an agent maintainer, I can see the selected primary stack, the rejected alternatives, and the review evidence that
accepted the decision.

**Why this priority**: Future work should stop re-litigating the framework choice and should deepen one selected stack
unless new evidence invalidates the decision.

**Independent Test**: Inspect the platform decision record, requirements matrix, roadmap, Beads comments, and reviewer
report; confirm the selected stack is based on implementation evidence and has explicit promotion gaps.

**Acceptance Scenarios**:

1. **Given** normalized candidate evidence, **When** the platform decision is recorded, **Then** the selected stack,
   rejected or deferred candidates, rationale, and remaining promotion blockers are all linked.
2. **Given** the presenter records decision evidence, **When** an independent reviewer evaluates it, **Then** the
   reviewer records acceptance or rejection in a durable artifact before the goal is considered accepted.

---

### User Story 3 - Product Baseline Workflow (Priority: P2)

As an implementation agent, I can start product work from a baseline workflow that is more than the comparison demo and
has BDD contracts, setup notes, and acceptance checks.

**Why this priority**: A platform decision only matters if it produces a product direction agents can build on without
renaming the comparison fixture as the product.

**Independent Test**: Run the product-baseline BDD and fixture validation; confirm the selected stack has a documented
workflow boundary, contract, operating notes, and follow-up backlog.

**Acceptance Scenarios**:

1. **Given** a selected stack, **When** the product baseline is defined, **Then** the baseline workflow names the user
   job, inputs, outputs, review gates, observability expectations, eval expectations, durable expectations, and
   acceptance command.
2. **Given** non-selected candidate code remains in the repo, **When** product work starts, **Then** those candidates are
   frozen or archived as comparison references with migration notes for any reusable assets.

## Requirements *(mandatory)*

- **FR-001**: Goal 004 MUST audit LangGraph Python, Pydantic AI, and Mastra TypeScript against the same evidence
  checklist before platform selection.
- **FR-002**: The audit MUST distinguish implementation evidence from research, planning, or directional fit.
- **FR-003**: The audit MUST decide whether Mastra TypeScript needs a runnable contrast slice before selection or can be
  explicitly deferred with evidence-based rationale.
- **FR-004**: Candidate scoring MUST cover infrastructure ownership, observability, evaluation, durable execution,
  scalability, and operating effort.
- **FR-005**: The selected primary stack MUST have repo-local run, trace, evaluation, setup, durable, and gap evidence.
- **FR-006**: Deterministic fixture validation MUST remain valid without hosted credentials or cloud services.
- **FR-007**: The platform decision MUST record rejected or deferred candidates with evidence-based reasons.
- **FR-008**: The decision MUST be accepted or rejected by an independent reviewer agent before Goal 004 acceptance.
- **FR-009**: The first product baseline workflow MUST be distinct from the comparison demo and must name product
  behavior, not only candidate comparison behavior.
- **FR-010**: Product baseline BDD contracts MUST define actor, operational observation, driver boundary, and acceptance
  command before implementation deepens.
- **FR-011**: The roadmap, requirements matrix, objective state, spec tasks, and Beads backlog MUST agree after the
  decision is recorded.
- **FR-012**: Follow-up tickets MUST capture production hardening gaps that remain after the platform decision.

### Key Entities

- **Candidate Evidence Audit**: A durable report mapping each candidate to run, trace, evaluation, setup, durable, and
  gap evidence.
- **Platform Decision Record**: The chosen primary stack, alternatives, rationale, promotion blockers, and reviewer
  acceptance evidence.
- **Product Baseline Workflow**: The first product-oriented workflow for the selected stack, separate from the shared
  comparison demo. T008 defines this as the review-gated implementation work-order workflow in
  `docs/product-baseline/pydantic-ai-review-gated-work-order.md`. T009 adds the implementation-agnostic BDD contract
  in `tests/workflow/features/product_baseline_work_order.feature`. T010 adds setup and operating notes in
  `docs/product-baseline/pydantic-ai-setup-operating-notes.md`.
- **Frozen Candidate Reference**: A non-selected candidate retained for comparison history and reusable lessons. T011
  records the freeze policy, dispositions, and tradeoffs in
  `docs/candidate-references/frozen-non-selected-candidates.md`. T012 records migration notes for reusable code,
  fixtures, and evidence in `docs/candidate-references/non-selected-candidate-migration-notes.md`.
- **Production Hardening Follow-up Backlog**: Beads epics that keep product-baseline promotion blockers visible after
  platform selection. T013 records `awf-4x7`, `awf-6zf`, and `awf-7ck` for the runnable work-order app, live model/tool
  trace coverage, and product tool/context approval boundaries.

## Success Criteria *(mandatory)*

- **SC-001**: A reviewer can trace every platform decision claim to implementation evidence or an explicit deferral.
- **SC-002**: The selected stack has higher evidence-backed fit than alternatives for the current product baseline.
- **SC-003**: The first product baseline workflow has BDD coverage and a deterministic acceptance command.
- **SC-004**: Future implementers can identify the selected stack and next Beads task without reading prior chat.
- **SC-005**: Non-selected candidates remain documented references rather than active product lanes.

## Assumptions

- Goals 001 through 003 are accepted and provide the starting evidence base.
- Pydantic AI is the strongest tested slice today, but Goal 004 must still prove or reject that conclusion from current
  evidence.
- Mastra TypeScript is a contrast candidate, not a default requirement; it should receive a runnable slice only if the
  audit finds the platform decision would otherwise be under-supported.
- Independent reviewer acceptance is sufficient for Goal 004 evidence unless the user explicitly reserves a decision.
