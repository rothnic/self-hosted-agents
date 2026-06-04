# Goal 004 T006 Selected Stack Propagation

Date: 2026-06-04
Spec: `005-candidate-platform-decision-product-baseline`
Task: T006
Beads issue: `awf-gal`
Worker: `codex-goal004-t006`

## Scope

T006 propagates the ADR 0005 platform decision into durable roadmap state. It does not complete T007 independent
platform-decision acceptance and does not accept Goal 004.

## Presenter Evidence

ADR 0005 selects Pydantic AI plus Langfuse and DBOS as the first product-baseline stack. This task updated:

- `objectives/current.md` to name the selected product-baseline stack and active follow-on work.
- `docs/goals/004-candidate-platform-decision-product-baseline.md` to add current decision state, preserve final-solution
  blockers, and clarify remaining Goal 004 work.
- `docs/roadmap.md` to make `apps/pydantic-ai/` the default product lane while keeping LangGraph and Mastra as
  comparison references.
- `docs/requirements-matrix.md` to update candidate dispositions and add a platform-decision section tied to ADR 0005.
- Beads issue `awf-gal` through the normal `complete-work` evidence path after validation and review.

## Boundary

The selected stack is a product baseline, not a final solution. Final-solution language remains blocked until production
Langfuse operations, richer evaluation workflows, DBOS production storage, worker topology, recovery rehearsal, and
live model/tool trace coverage have repo-local or self-hosted evidence.

## Validation

- `git diff --check`: passed.
- `uv run awf spec-lint --json`: passed.
- `uv run awf review-gate --json`: passed with no human-required gates.
- `uv run awf repo-hygiene --json`: passed after shortening long requirements-matrix rows.
- `uv run awf workflow-state-lint --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed, 45/45.
- `uv run awf verify --profile ticket --json`: passed all checks, including acceptance.

## Independent Review

Reviewer agent: `019e9015-de65-7f63-84c1-bfd6d6f72240`
Outcome: accepted

Findings:

- No blocking findings.
- No required follow-up tickets for T006 closure.
- Existing T007 remains the separate platform-decision acceptance task.

Evidence checked by reviewer:

- ADR 0005 selected stack and final-solution blockers.
- Objective, Goal 004, roadmap, and requirements-matrix propagation.
- Spec task split between T006 and T007.
- This report's T006-only scope.
- Read-only validation evidence: `git diff --check`, `spec-lint`, `review-gate`, `repo-hygiene`,
  `workflow-state-lint`, `verify --profile ticket`, and `workflow-fixture-test` with 45/45 passing.
