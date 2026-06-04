# Goal 004 T007 Platform Decision Acceptance

Date: 2026-06-04
Spec: `005-candidate-platform-decision-product-baseline`
Task: T007
Beads issue: `awf-zi9`
Presenter: `codex-goal004-t007`

## Scope

T007 presents the platform decision evidence to an independent reviewer agent and records acceptance or rejection. It
does not define the first product baseline workflow, freeze non-selected candidate lanes, create production-hardening
follow-up tickets, or accept Goal 004 as complete.

## Decision Presented

ADR 0005 selects Pydantic AI plus Langfuse and DBOS as the first product-baseline stack.

The selection is based on implementation evidence:

- Pydantic AI provides the Python-first agent application boundary.
- Langfuse provides self-hosted-compatible LLM observability.
- Repo-local OpenTelemetry artifacts preserve deterministic trace inspection without hosted credentials.
- Pydantic Evals provides deterministic evaluation artifacts tied to run and trace identity.
- DBOS provides local durable proof for retry, resume, review wait, side-effect idempotency, and evidence correlation.

This is a product-baseline decision, not final-solution promotion.

## Evidence Presented

- `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md`
- `docs/requirements-matrix.md`
- `objectives/current.md`
- `docs/goals/004-candidate-platform-decision-product-baseline.md`
- `docs/roadmap.md`
- `.agent-runs/reports/goal-004-t001-candidate-evidence-audit-20260602.md`
- `.agent-runs/reports/goal-004-t002-mastra-contrast-decision-20260602.md`
- `.agent-runs/reports/goal-004-t003-evidence-normalization-20260603.md`
- `.agent-runs/reports/goal-004-t004-candidate-scoring-20260604.md`
- `.agent-runs/reports/goal-004-t005-platform-decision-adr-20260604.md`
- `.agent-runs/reports/goal-004-t006-selected-stack-propagation-20260604.md`
- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.json`
- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json`
- `.agent-runs/verifications/verify-langfuse-t027-20260531.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t010-20260602.json`
- `.beads/issues.jsonl`

## Alternatives Presented

- LangGraph Python plus Langfuse remains a comparison reference because durable execution proof, self-hosted Langfuse
  ingestion, product trace depth, and committed verification artifacts are incomplete.
- Mastra TypeScript remains a deferred TypeScript reference because it has no runnable implementation evidence for the
  current platform decision.
- LangSmith remains an external feature benchmark because self-hosted access cannot be assumed and hosted-only trace
  inspection does not satisfy the project constraint.

## Boundary Presented

Deterministic fixture validation must remain valid without hosted credentials or cloud services. Service-backed
observability proof supplements repo-local artifacts; it does not replace them.

The selected stack cannot be called the final solution until follow-up work proves:

- Langfuse production operations.
- Richer evaluation workflows.
- DBOS production storage.
- DBOS worker topology and queue behavior.
- Recovery rehearsal, retention, and cleanup.
- Live model/tool trace coverage or explicit simulated equivalents.
- Product-level BDD contracts and setup notes for a baseline workflow distinct from the comparison demo.

## Validation

- `git diff --check`: passed.
- `uv run awf spec-lint --json`: passed.
- `uv run awf review-gate --json`: passed with no human-required gates.
- `uv run awf repo-hygiene --json`: passed with `checked_files=264`.
- `uv run awf workflow-state-lint --json`: passed.
- `uv run awf verify --profile ticket --json`: passed all checks, including acceptance
  `uv run awf workflow-fixture-test`.

## Independent Review

Reviewer agent: `019e901f-b8f9-7f90-a8c0-c27601d8d736`
Outcome: accepted

Findings:

- No blocking findings.
- No required follow-up tickets for T007 acceptance.
- Existing Goal 004 tasks T008-T014 remain open for product baseline definition, product BDD contracts, setup notes,
  candidate lane transition, production hardening follow-up tickets, and final Goal 004 increment acceptance.

Evidence checked by reviewer:

- This T007 packet presents the decision and scope without claiming Goal 004 completion.
- ADR 0005 selects Pydantic AI plus Langfuse and DBOS, records rejected or deferred alternatives, and preserves
  promotion blockers.
- Requirements matrix, objective, Goal 004, and roadmap agree that this is product-baseline selection, not
  final-solution promotion.
- Spec and task state keep product baseline, transition, hardening, and final Goal 004 acceptance open.
- Prior accepted T001-T006 reports support the selection.
- Cited Pydantic AI run, trace, Langfuse proof, eval, and DBOS durable smoke artifacts exist.
- Read-only checks passed: `git diff --check`, `spec-lint`, `review-gate`, `repo-hygiene`, `workflow-state-lint`,
  `verify --profile ticket`, and `workflow-fixture-test` with 45/45 passing.
