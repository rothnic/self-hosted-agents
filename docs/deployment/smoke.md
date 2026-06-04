# Deployment Smoke

Status: captured through Goal 005 T008
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

This page defines the representative selected-stack smoke command for the reference profile. The smoke command runs the
Pydantic AI fixture app and DBOS durable proof, then correlates readiness, startup, health, run, trace, evaluation, and
durable evidence in one repo-local result.

## Local Smoke Command

Use the local profile for deterministic ticket validation:

```bash
uv run awf deployment-smoke --profile local --write --json
```

When the local profile is ready, the command writes a per-smoke evidence bundle under
`.agent-runs/reports/goal-005/<smoke-id>/`. The top-level artifact uses schema `awf.deployment-smoke.v1` and includes:

- deployment readiness and startup health checks
- Pydantic AI run id, trace id, evaluation id, and artifact paths
- DBOS durable workflow id and runtime summary
- repo-local observability availability
- deterministic validation flags showing no hosted credentials, external model provider, or network is required
- explicit gaps for self-hosted Langfuse service-backed ingestion and production DBOS storage proof

## Captured Local Evidence

T007 captured the first committed local smoke artifact:

- `.agent-runs/reports/goal-005/deployment-smoke-local-20260604T045610Z/deployment-smoke.json`
- `.agent-runs/reports/goal-005/t007-deployment-smoke-evidence-20260604.md`

The artifact correlates the local profile health checks with the Pydantic AI run id, trace id, evaluation id, DBOS
durable run id, and credential-free deterministic validation flags. Self-hosted Langfuse remains the selected
observability service boundary, but it is not required for the local fixture profile.

The same evidence bundle includes the durable child artifacts referenced by the smoke result:

- `pydantic-ai-run.json`
- `pydantic-ai-run.trace.json`
- `pydantic-ai-run.evaluation.json`
- `pydantic-ai-durable-smoke.json`

## Credential-Free Fallback Proof

T008 adds a focused fallback proof command:

```bash
uv run awf deployment-fallback-proof --write --json
```

The command writes `awf.deployment-credential-free-fallback.v1` evidence under
`.agent-runs/reports/goal-005/<proof-id>/`. The committed T008 proof is:

- `.agent-runs/reports/goal-005/deployment-credential-free-fallback-20260604T051344Z/credential-free-fallback.json`
- `.agent-runs/reports/goal-005/t008-credential-free-fallback-20260604.md`

The proof uses an empty environment to show that the local deterministic profile passes without Langfuse, Logfire,
DBOS database, model-provider, or cloud credentials. It also shows that `development-server` and `production-like`
profiles fail fast on missing self-hosted configuration without running candidate or durable service work.

## Service-Backed Boundary

The local smoke proves the selected stack can run without hosted services. It does not claim that Langfuse ingestion or
production DBOS storage is available. For service-backed proof, start self-hosted Langfuse through the documented
equivalent in `docs/deployment/startup.md`, provide host-local env values outside git, and rerun smoke/readiness against
the controlled profile:

```bash
uv run awf deployment-smoke --profile development-server --env-file /path/outside/git/development.env --write --json
```

Development-server and production-like smoke should fail fast when required self-hosted service configuration is absent.
The output reports missing variable names and redacted presence only, never secret values.

## Boundaries

- T006 adds the smoke command and local driver contract.
- T007 captures committed repo-local smoke evidence with full correlation.
- T008 proves deterministic validation remains credential-free when service-backed deployment services or secrets are
  absent.
- Startup remains separate from smoke: `deployment-startup` records the startup plan, while `deployment-smoke` runs the
  selected workflow.
