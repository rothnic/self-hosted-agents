# Deployment Startup

Status: updated through Goal 005 T006
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

This page defines the startup surface for the selected self-hosted profiles without turning startup into the deployment
smoke workflow. T005 proves another agent can start or inspect the profile boundary. The T006 smoke command is
documented in `docs/deployment/smoke.md`.

## Local One-Command Startup

Use the local profile for deterministic development and ticket validation:

```bash
uv run awf deployment-startup --profile local --write --json
```

The command runs the local readiness checks and writes a startup manifest under `.agent-runs/manifests/` when readiness
passes. The manifest records the local profile, target machine, startup mode, component commands, service-boundary docs,
environment-readiness docs, and the next smoke scope.

The local profile does not start a daemon. Pydantic AI and DBOS are repo CLI entrypoints:

- Pydantic AI candidate app: `uv run python apps/pydantic-ai/run.py ...`
- DBOS durable runtime proof: `uv run python apps/pydantic-ai/durable_smoke.py ...`

Those commands are listed in the startup manifest for deployment smoke evidence. They are not executed by
`deployment-startup`, so startup validation remains fast and credential-free.

## Langfuse Service Equivalent

Self-hosted Langfuse is a multi-service Docker Compose profile, not a safe one-command repo-local fixture. Use the
documented equivalent when service-backed proof is required:

```bash
git clone https://github.com/langfuse/langfuse.git ~/data/projects/langfuse
cd ~/data/projects/langfuse
docker compose up -d
```

Then run readiness from this repository with host-local secrets stored outside git:

```bash
uv run awf deployment-readiness --profile development-server --env-file /path/outside/git/development.env --json
```

Detailed Langfuse setup, headless initialization, reset, and troubleshooting live in
`docs/orchestration/self-hosted-langfuse.md`.

## Profile Behavior

| Profile | Startup mode | Command |
| --- | --- | --- |
| `local` | one-command local manifest | `uv run awf deployment-startup --profile local --write --json` |
| `development-server` | documented service equivalent | `uv run awf deployment-startup --profile development-server --env-file <host-env> --json` |
| `production-like` | documented service equivalent | `uv run awf deployment-startup --profile production-like --env-file <host-env> --json` |

Development-server and production-like startup readiness should fail until the required self-hosted service config is
present in the operator environment or an untracked env file. The output reports variable names and redacted presence,
not values.

## Boundaries

- Startup checks readiness and records the startup plan.
- Startup does not run the representative selected-stack workflow; that is T006.
- Startup does not require hosted Logfire, model-provider credentials, or cloud services.
- Startup may reference self-hosted Langfuse, but deterministic fixture validation must pass when Langfuse is absent.
