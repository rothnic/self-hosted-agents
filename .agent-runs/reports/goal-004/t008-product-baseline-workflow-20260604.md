# Goal 004 T008 Product Baseline Workflow Definition

Date: 2026-06-04
Spec: `005-candidate-platform-decision-product-baseline`
Task: T008
Beads issue: `awf-6kf`
Worker: `codex-goal004-t008`

## Scope

T008 defines the first product baseline workflow for the selected Pydantic AI plus Langfuse and DBOS stack. It does not
add BDD contracts, setup notes, runnable product code, candidate-lane archive notes, or final Goal 004 acceptance.

## Presenter Evidence

Added `docs/product-baseline/pydantic-ai-review-gated-work-order.md`.

The baseline workflow is a review-gated implementation work order. It is distinct from the comparison demo because it
does more than recommend a next slice for candidate scoring: it turns an approved roadmap, spec, or Beads request into
one implementation work order with behavior scope, acceptance command, trace expectations, evaluation expectations,
durable execution expectations, setup expectations, and independent reviewer handoff.

Updated links:

- `docs/goals/004-candidate-platform-decision-product-baseline.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `apps/pydantic-ai/README.md`

## Boundary

T009 remains responsible for implementation-agnostic product BDD contracts. T010 remains responsible for setup and
operating notes. Later implementation tickets remain responsible for runnable product code and production hardening.

## Validation

- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=267`.
- `uv run awf review-gate --json`: passed with no human-required gates.
- `uv run awf workflow-state-lint --json`: passed.
- `uv run awf verify --profile ticket --json`: passed all checks, including acceptance
  `uv run awf workflow-fixture-test`.

## Independent Review

Reviewer agent: `019e902b-3464-7c92-9d01-aa1fdd5978e6`
Outcome: accepted

Findings:

- No blocking findings.
- No required follow-up tickets for T008 closure.
- Existing T009, T010, and T011-T014 remain open for BDD contracts, setup and operating notes, candidate lane
  transition, hardening follow-ups, and final Goal 004 increment acceptance.

Evidence checked by reviewer:

- The product baseline defines the user job, inputs, outputs, acceptance command, review gate, observability
  expectations, evaluation expectations, durable expectations, setup boundary, and first product boundary.
- The workflow is distinct from the comparison demo and scopes a review-gated implementation work order.
- T008 does not claim T009 BDD contracts, T010 setup notes, runnable product code, or final Goal 004 acceptance.
- Spec, Goal 004, roadmap, Pydantic AI README, and implementation plan point to the workflow definition.
- ADR 0005 confirms the selected stack and keeps final-solution promotion blockers open.
- Read-only checks passed: `git diff --check`, `spec-lint`, `review-gate`, `repo-hygiene`, `workflow-state-lint`,
  `verify --profile ticket`, and `workflow-fixture-test` with 45/45 passing.
