# Goal 004 T003 Evidence Normalization

Date: 2026-06-03

Presenter: codex-goal004-t003

Work item: `awf-dys`

Objective: `agentic-development-foundation`

Spec: `005-candidate-platform-decision-product-baseline`

Task: T003, normalize candidate run, trace, evaluation, setup, durable, and gap evidence in
`docs/requirements-matrix.md`.

Acceptance command: `uv run awf workflow-fixture-test`

## Presenter Evidence

T003 updated `docs/requirements-matrix.md` so Goal 004 scoring can use accepted T001 and T002 evidence without mixing
implementation evidence, research claims, and deferred contrast intent.

Changes made:

- Added a Goal 004 evidence normalization section.
- Listed the accepted T001 and T002 reports plus the app docs and committed Pydantic AI evidence artifacts used as
  sources.
- Normalized LangGraph Python plus Langfuse as `partial` for run, trace, evaluation, setup, and gap evidence, with
  durable evidence still `missing`.
- Normalized Pydantic AI plus Langfuse/DBOS as `proven` for tested candidate-slice run, trace, evaluation, setup,
  local durable, and gap evidence while preserving final-promotion blockers.
- Normalized Mastra TypeScript as `missing` for run, trace, evaluation, and durable implementation evidence, `partial`
  for setup intent, and `deferred-before-platform-selection` for Goal 004 scoring.
- Updated the top requirement score table so the Mastra column uses `Missing` or `Deferred` for implementation-dependent
  evidence rows instead of unqualified positive scores.

## Validation

Post-fix validation passed:

- `git diff --check`
- `uv run awf spec-lint --json`
- `uv run awf review-gate --json`
- `uv run awf repo-hygiene --json`
- `uv run awf workflow-state-lint --json`
- `uv run awf workflow-fixture-test --json` with `45/45` passed

Earlier ticket-profile validation also passed for the active `awf-dys` claim:

- `uv run awf verify --profile ticket --json`

## Independent Reviewer Acceptance

Reviewer agent id: `codex-independent-reviewer-goal004-t003`

Review agent path: `019e8ff5-acb5-7652-a6b8-7f94781f8043`

Outcome: `accepted`

Reviewer findings:

- No findings.
- The previous P1 was fixed by bounding `Deferred` and `Missing` as not implementation-backed evidence.
- The Mastra column now uses `Missing` or `Deferred` for implementation-dependent evidence rows.
- The matrix now aligns with the normalization rules and T003 closure criteria.

Evidence checked:

- `docs/requirements-matrix.md`
- Active `awf-dys` claim state
- `git diff --check`
- `uv run awf verify --profile ticket --json`
- `uv run awf workflow-fixture-test --json`

Required follow-up tickets:

- None for T003.
