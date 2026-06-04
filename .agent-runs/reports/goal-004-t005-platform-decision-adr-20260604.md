# Goal 004 T005 Platform Decision ADR

Date: 2026-06-04

Presenter: codex-goal004-t005

Work item: `awf-a31`

Objective: `agentic-development-foundation`

Spec: `005-candidate-platform-decision-product-baseline`

Task: T005, record the platform decision ADR with selected stack, rejected alternatives, rationale, and promotion
blockers.

Acceptance command: `uv run awf workflow-fixture-test`

## Presenter Evidence

T005 adds `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md` as the platform decision record.

Decision recorded:

- Selected primary stack: Pydantic AI plus Langfuse and DBOS.
- Decision type: product-baseline selection, not final-solution promotion.
- Rejected or deferred alternatives: LangGraph Python plus Langfuse, Mastra TypeScript plus shared contracts, and
  LangSmith baseline.
- Rationale: Pydantic AI plus Langfuse/DBOS is the only current candidate with repo-local run, trace, evaluation,
  setup, durable, and gap evidence.
- Self-hosted boundary: deterministic fixture validation remains credential-free; hosted-only trace inspection is not
  sufficient.
- Promotion blockers: Langfuse production operations, richer evaluation workflows, DBOS production storage, DBOS worker
  topology, recovery rehearsal, live model/tool trace coverage, and product-level BDD/setup work.

Task boundary:

- T005 records the decision ADR.
- T006 remains responsible for propagating the selected stack into roadmap, objective, requirements matrix, and Beads
  state.
- T007 remains responsible for presenting the full platform decision evidence to an independent reviewer for Goal 004
  decision acceptance.

## Validation

Validation passed:

- `git diff --check`
- `uv run awf spec-lint --json`
- `uv run awf review-gate --json` with `human_required_count=0`
- `uv run awf repo-hygiene --json` with `checked_files=260`
- `uv run awf workflow-state-lint --json`
- `uv run awf workflow-fixture-test --json` with `45/45` passed
- `uv run awf verify --profile ticket --json`

## Independent Reviewer Acceptance

Reviewer agent path: `019e9009-385c-7fb1-bf2d-50eb044caf98`

Outcome: `accepted`

Reviewer findings:

- No findings.
- The T005 ADR is within scope for `awf-a31`.
- The ADR records the selected stack, rejected or deferred alternatives, rationale, and promotion blockers.
- The ADR preserves the self-hosted constraint and does not complete T006 propagation or T007 final decision
  acceptance.

Evidence checked:

- `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md`
- `.agent-runs/reports/goal-004-t005-platform-decision-adr-20260604.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `specs/005-candidate-platform-decision-product-baseline/tasks.md`
- Accepted T001-T004 reports and scorecard basis
- `git diff --check`
- `uv run awf spec-lint --json`
- `uv run awf repo-hygiene --json`
- `uv run awf workflow-fixture-test --json`

Required follow-up tickets:

- None for T005.
