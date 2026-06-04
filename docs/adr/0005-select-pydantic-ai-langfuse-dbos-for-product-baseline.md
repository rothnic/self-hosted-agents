# ADR 0005: Select Pydantic AI Plus Langfuse And DBOS For The Product Baseline

Status: accepted

## Context

Goal 004 requires a platform decision based on implementation evidence, not provider preference or research notes.
The current comparison set is LangGraph Python plus Langfuse, Pydantic AI plus Langfuse/DBOS, and Mastra TypeScript
plus shared contracts.

The accepted T001-T004 Goal 004 evidence shows:

- Pydantic AI plus Langfuse/DBOS has repo-local run, trace, evaluation, setup, durable, and gap evidence.
- LangGraph Python plus Langfuse remains a partial Python comparison slice with no durable execution proof and weaker
  committed verification evidence.
- Mastra TypeScript remains a deferred TypeScript contrast reference with missing runnable implementation evidence.

The project also has a hard self-hosted constraint: deterministic fixture validation must not require hosted
credentials, third-party cloud trace access, or hidden service state.

## Decision

Select **Pydantic AI plus Langfuse and DBOS** as the primary stack for the first product baseline.

Use this stack for the next product-oriented workflow because it is the only current candidate with implementation
evidence across the required categories:

- Pydantic AI provides the Python-first agent application boundary.
- Langfuse provides the self-hosted-compatible LLM observability control plane.
- Repo-local OpenTelemetry trace artifacts preserve credential-free inspection.
- Pydantic Evals provides deterministic evaluation artifacts tied to run and trace identity.
- DBOS provides the first durable execution path, with local evidence for retry, resume, review wait, side-effect
  idempotency, and evidence correlation.

This is a product-baseline selection, not final-solution promotion. Final-solution language remains blocked until the
promotion blockers below are closed with repo-local or self-hosted evidence.

## Rejected Or Deferred Alternatives

### LangGraph Python Plus Langfuse

Disposition: comparison reference, not selected for the first product baseline.

Reasons:

- The current Goal 004 scorecard records weaker implementation-backed scores than Pydantic AI plus Langfuse/DBOS.
- Durable execution evidence is missing.
- Self-hosted Langfuse ingestion, product trace depth, and committed verification artifacts are incomplete.
- Keeping it as a reference preserves useful Python orchestration lessons without splitting product implementation.

### Mastra TypeScript Plus Shared Contracts

Disposition: deferred TypeScript contrast reference, not implementation-comparable for this decision.

Reasons:

- T002 explicitly deferred the runnable Mastra contrast slice before platform selection.
- T003 normalized Mastra run, trace, evaluation, durable, and operating evidence as missing or deferred.
- T004 did not assign implementation scores to Mastra.
- Reopening Mastra should require a future TypeScript need or evidence that the selected Python baseline cannot satisfy
  a product requirement.

### LangSmith Baseline

Disposition: external benchmark only, not selected.

Reasons:

- Self-hosted access cannot be assumed for this project.
- Hosted-only trace inspection does not satisfy the self-hosted agents assessment.
- LangSmith remains useful as a feature expectation baseline for LangChain/LangGraph-style observability.

## Promotion Blockers

The selected stack cannot be called the final solution until follow-up work proves:

- Langfuse production operations: retention, backup, reset, recovery, secret handling, and production-style deployment.
- Richer Langfuse or equivalent evaluation workflows beyond deterministic fixture assertions.
- DBOS production storage beyond SQLite development mode.
- DBOS worker topology, queue behavior, concurrency boundaries, stale-work handling, and operator diagnostics.
- DBOS recovery rehearsal, retention, cleanup, and another-agent recovery procedure.
- Live model/tool trace coverage or explicit simulated equivalents for tokens, cost, failures, and tool-call context.
- Product-level BDD contracts and setup notes for a baseline workflow that is distinct from the comparison demo.

Tracked follow-up epics include `awf-eas`, `awf-2du`, `awf-4t2`, `awf-lkr`, `awf-ygu`, and `awf-5ae`. Goal 004 later
tasks must add any missing product-baseline or production-hardening Beads items before final Goal 004 acceptance.

## Consequences

- Future product-baseline work should deepen `apps/pydantic-ai` rather than continue framework selection by default.
- LangGraph Python and Mastra TypeScript are frozen comparison references under
  `docs/candidate-references/frozen-non-selected-candidates.md`.
- Deterministic validation remains credential-free; service-backed observability proof supplements repo-local
  artifacts instead of replacing them.
- T006 must propagate this decision to roadmap, objective, requirements matrix, and Beads state.
- T007 must present the decision evidence to an independent reviewer agent for acceptance or rejection before Goal 004
  can be accepted.

## Evidence

- `docs/requirements-matrix.md`
- `.agent-runs/reports/goal-004-t001-candidate-evidence-audit-20260602.md`
- `.agent-runs/reports/goal-004-t002-mastra-contrast-decision-20260602.md`
- `.agent-runs/reports/goal-004-t003-evidence-normalization-20260603.md`
- `.agent-runs/reports/goal-004-t004-candidate-scoring-20260604.md`
- `.agent-runs/reports/goal-004-t005-platform-decision-adr-20260604.md`
- `.agent-runs/reports/goal-004-t006-selected-stack-propagation-20260604.md`
- `.agent-runs/reports/goal-004/t007-platform-decision-acceptance-20260604.md`
- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.json`
- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json`
- `.agent-runs/verifications/verify-langfuse-t027-20260531.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t010-20260602.json`
