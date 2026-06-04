# Goal 005 T007 Deployment Smoke Evidence

Date: 2026-06-04
Ticket: `awf-xei`
Task: `specs/006-self-hosted-deployment-operations-reference/tasks.md#T007`
Acceptance: `uv run awf workflow-fixture-test`

## Evidence

T007 captured repo-local deployment smoke evidence at
`.agent-runs/reports/goal-005/deployment-smoke-local-20260604T045610Z/deployment-smoke.json`.

The smoke command writes a per-smoke evidence bundle under `.agent-runs/reports/goal-005/` so the root verification
directory remains within repo-hygiene child-count policy.

The artifact uses schema `awf.deployment-smoke.v1` and records:

- profile: `local`
- smoke id: `deployment-smoke-local-20260604T045610Z`
- Pydantic AI run id: `run-e93c5940e04ff8cf99fe2e21`
- Pydantic AI trace id: `trace-f9cac59a8a238a726e8289e1`
- Pydantic AI evaluation id: `eval-65ca933b165e3794`
- DBOS durable run id: `dbos-workflow-a5c4cdb62d4f6f611dbb7a92`
- health checks: deployment readiness, deployment startup, Pydantic AI candidate app, DBOS durable runtime, and
  self-hosted Langfuse service boundary

The bundle also keeps the directly inspectable child artifacts:

- `.agent-runs/reports/goal-005/deployment-smoke-local-20260604T045610Z/pydantic-ai-run.json`
- `.agent-runs/reports/goal-005/deployment-smoke-local-20260604T045610Z/pydantic-ai-run.trace.json`
- `.agent-runs/reports/goal-005/deployment-smoke-local-20260604T045610Z/pydantic-ai-run.evaluation.json`
- `.agent-runs/reports/goal-005/deployment-smoke-local-20260604T045610Z/pydantic-ai-durable-smoke.json`

## Validation Meaning

The local profile smoke passed all required gates:

- readiness, startup, candidate app, durable runtime, run/trace/eval correlation, observability availability, durable
  availability, health correlation, and credential-free validation are all `true`.
- self-hosted Langfuse is present as the selected observability service boundary, but it is `required=false` for the
  local deterministic fixture path.
- deterministic validation records `hosted_credentials_required=false`, `external_model_required=false`, and
  `network_required=false`.

## Remaining Boundary

This evidence proves repo-local smoke correlation for the deterministic local profile. It does not claim service-backed
Langfuse ingestion or production DBOS storage. Those remain routed to later Goal 005 work.
