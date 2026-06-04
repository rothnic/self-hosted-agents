# Goal 004 T009 Product Baseline BDD Contract

Date: 2026-06-04
Spec: `005-candidate-platform-decision-product-baseline`
Task: T009
Beads issue: `awf-e04`
Worker: `codex-goal004-t009`

## Scope

T009 adds implementation-agnostic product-level BDD contracts for the baseline workflow defined by T008. It does not add
setup notes, runnable product code, candidate-lane archive notes, production hardening tickets, or final Goal 004
acceptance.

## Presenter Evidence

Added `tests/workflow/features/product_baseline_work_order.feature`.

The contract covers the first product baseline as a review-gated implementation work order. It defines:

- actors: project owner, implementer, reviewer, and operator;
- product behavior: one executable work order from a repo-local goal, spec, or ready ticket;
- acceptance command: `uv run awf workflow-fixture-test`;
- operational observations: trace, evaluation, durable state, review gate, evidence paths, and hosted-service gaps;
- review boundary: completion waits for independent reviewer acceptance;
- deterministic boundary: fixture validation does not require hosted observability credentials.

Updated driver-boundary notes in `tests/workflow/drivers/README.md` so future concrete drivers know which observable
actions must satisfy the product-baseline contract.

Updated links:

- `docs/product-baseline/pydantic-ai-review-gated-work-order.md`
- `docs/goals/004-candidate-platform-decision-product-baseline.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `docs/roadmap.md`

## Boundary

The feature file does not name Pydantic AI, Langfuse, DBOS internals, hosted credentials, database APIs, queues, or
framework-specific tool calls. Those details belong in future implementation drivers and app code.

T010 remains responsible for setup and operating notes. T011 and T012 remain responsible for non-selected candidate
lane transition. T013 remains responsible for follow-up production hardening tickets. T014 remains responsible for
final Goal 004 increment verification and reviewer-accepted completion evidence.

## Validation

- `git diff --check`: passed.
- `uv run awf bdd-lint --json`: passed and included `Product baseline work order`.
- `uv run awf bdd-run --driver fixture --json`: passed and executed `Product baseline work order`.
- `uv run awf workflow-fixture-test --json`: passed `45/45`.
- `uv run awf verify --profile ticket --json`: passed all checks, including acceptance
  `uv run awf workflow-fixture-test`.

## Independent Review

Reviewer agent: `019e9036-a010-73f2-a9a4-a7755a3fcdc3`
Outcome: accepted

Findings:

- No findings.
- No required follow-up tickets for T009 closure.
- T010, T011, T012, T013, and T014 remain planned Goal 004 work, but they are not blockers for accepting T009.

Evidence checked by reviewer:

- `tests/workflow/features/product_baseline_work_order.feature` defines actors and operational behavior.
- The contract covers work-order output, review gating, and fixture validation without hosted services.
- `tests/workflow/drivers/README.md` documents the driver boundary without framework internals.
- `docs/product-baseline/pydantic-ai-review-gated-work-order.md` links the BDD contract and preserves repo-local
  deterministic validation.
- Goal, spec, and roadmap updates align T009 with Goal 004 product-baseline scope.
- This presenter report accurately records scope and validation.

Validation rerun by reviewer:

- `git diff --check`: passed.
- `uv run awf bdd-lint --json`: passed and included `Product baseline work order`.
- `uv run awf bdd-run --driver fixture --json`: passed and executed `product_baseline_work_order.feature`.
- `uv run awf workflow-fixture-test --json`: passed `45/45`.
- `uv run awf verify --profile ticket --json`: passed with no failures and acceptance command
  `uv run awf workflow-fixture-test`.
