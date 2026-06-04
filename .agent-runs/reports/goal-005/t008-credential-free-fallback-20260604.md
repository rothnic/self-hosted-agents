# Goal 005 T008 Credential-Free Fallback Evidence

Date: 2026-06-04
Ticket: `awf-rgf`
Task: `specs/006-self-hosted-deployment-operations-reference/tasks.md#T008`
Acceptance: `uv run awf workflow-fixture-test`

## Evidence

T008 captured credential-free fallback proof at
`.agent-runs/reports/goal-005/deployment-credential-free-fallback-20260604T051344Z/credential-free-fallback.json`.

The proof command is:

```bash
uv run awf deployment-fallback-proof --write --json
```

The artifact uses schema `awf.deployment-credential-free-fallback.v1` and records:

- proof id: `deployment-credential-free-fallback-20260604T051344Z`
- absent environment mode: `empty-env`
- local profile readiness: `true`
- local profile smoke: `true`
- hosted credentials required: `false`
- external model required: `false`
- network required: `false`
- service-backed profiles fail fast without secrets: `true`

The local profile bundle keeps the directly inspectable child artifacts:

- `.agent-runs/reports/goal-005/deployment-credential-free-fallback-20260604T051344Z/pydantic-ai-run.json`
- `.agent-runs/reports/goal-005/deployment-credential-free-fallback-20260604T051344Z/pydantic-ai-run.trace.json`
- `.agent-runs/reports/goal-005/deployment-credential-free-fallback-20260604T051344Z/pydantic-ai-run.evaluation.json`
- `.agent-runs/reports/goal-005/deployment-credential-free-fallback-20260604T051344Z/pydantic-ai-durable-smoke.json`

## Service Absence Behavior

The proof intentionally runs the readiness and smoke checks with an empty environment:

- `local` passes readiness and smoke with no Langfuse, Logfire, DBOS database, model-provider, or cloud credentials.
- `development-server` fails readiness and smoke without running candidate or durable service work because
  `LANGFUSE_BASE_URL`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_PROJECT_ID` are absent.
- `production-like` fails readiness and smoke without running candidate or durable service work because the Langfuse
  variables and `DBOS_DATABASE_URL` are absent.

This proves absent deployment services or secrets do not become a hidden dependency for deterministic validation. The
missing service-backed configuration is preserved as explicit follow-up gap evidence instead of silently requiring
hosted services.

## Remaining Boundary

This evidence does not claim that service-backed Langfuse or production DBOS storage is available. It proves the
credential-free fallback and fail-fast absence behavior required before later operations runbooks and service-backed
proofs can rely on the same deployment surface.
