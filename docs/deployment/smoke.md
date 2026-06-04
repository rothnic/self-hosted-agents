# Deployment Smoke

Status: initialized for Goal 005 T006
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

When the local profile is ready, the command writes a smoke artifact under `.agent-runs/verifications/`. The artifact
uses schema `awf.deployment-smoke.v1` and includes:

- deployment readiness and startup health checks
- Pydantic AI run id, trace id, evaluation id, and artifact paths
- DBOS durable workflow id and runtime summary
- repo-local observability availability
- deterministic validation flags showing no hosted credentials, external model provider, or network is required
- explicit gaps for self-hosted Langfuse service-backed ingestion and production DBOS storage proof

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
