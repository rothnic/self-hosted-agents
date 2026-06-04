# Goal 004 T004 Candidate Scoring

Date: 2026-06-04

Presenter: codex-goal004-t004

Work item: `awf-yka`

Objective: `agentic-development-foundation`

Spec: `005-candidate-platform-decision-product-baseline`

Task: T004, score candidates against infrastructure ownership, observability, evaluation, durable execution,
scalability, and operating effort.

Acceptance command: `uv run awf workflow-fixture-test`

## Presenter Evidence

T004 updated `docs/requirements-matrix.md` with a Goal 004 candidate scorecard grounded in the accepted T001-T003
evidence.

Scores recorded:

- LangGraph Python plus Langfuse: `2/2/2/1/2/2` across infrastructure ownership, observability, evaluation, durable
  execution, scalability, and operating effort. It remains a partial Python comparison slice.
- Pydantic AI plus Langfuse/DBOS: `3/4/3/4/2/2` across the same criteria. It is the strongest
  implementation-backed candidate slice, with production hardening blockers preserved.
- Mastra TypeScript plus shared contracts: `N/S` for all implementation criteria because the runnable contrast slice is
  deferred and current repo state lacks implementation evidence.

Decision boundary:

- T004 records the scorecard and leading evidence-backed candidate.
- T004 does not record the platform decision ADR; that remains T005.
- The scorecard does not rely on cloud-only services. Pydantic AI observability evidence remains backed by repo-local
  trace artifacts plus self-hosted Langfuse proof, and deterministic fixture validation remains credential-free.

Evidence sources:

- `docs/evaluation-criteria.md`
- `docs/comparison-evidence.md`
- `docs/requirements-matrix.md`
- `.agent-runs/reports/goal-004-t001-candidate-evidence-audit-20260602.md`
- `.agent-runs/reports/goal-004-t002-mastra-contrast-decision-20260602.md`
- `.agent-runs/reports/goal-004-t003-evidence-normalization-20260603.md`
- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.json`
- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json`
- `.agent-runs/verifications/verify-langfuse-t027-20260531.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t010-20260602.json`

## Validation

Validation passed:

- `git diff --check`
- `uv run awf spec-lint --json`
- `uv run awf review-gate --json` with `human_required_count=0`
- `uv run awf repo-hygiene --json` with `checked_files=257`
- `uv run awf workflow-state-lint --json`
- `uv run awf workflow-fixture-test --json` with `45/45` passed
- `uv run awf verify --profile ticket --json`

## Independent Reviewer Acceptance

Reviewer agent path: `019e9001-20ee-7053-a49d-4eb4ae79041c`

Outcome: `accepted`

Reviewer findings:

- No findings.
- The T004 scorecard stays within scope for `awf-yka`.
- The scorecard covers the required criteria, keeps Mastra unscored as `N/S`, preserves the self-hosted and
  no-cloud-only validation constraint, and does not record the T005 ADR decision.

Evidence checked:

- `docs/requirements-matrix.md`
- `.agent-runs/reports/goal-004-t004-candidate-scoring-20260604.md`
- `git diff --check`
- `uv run awf spec-lint --json`
- `uv run awf repo-hygiene --json`
- `uv run awf workflow-fixture-test --json`

Required follow-up tickets:

- None for T004.
