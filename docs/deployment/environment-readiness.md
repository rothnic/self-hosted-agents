# Environment And Readiness

Status: updated through Goal 005 T008
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

This page defines the credential-free environment templates and readiness check for the selected self-hosted profiles.
The templates name the required service configuration without committing secrets. The readiness command reports missing
runtimes, service configuration, secrets, storage prerequisites, and repo paths without printing secret values.

## Templates

| Profile | Template | Target |
| --- | --- | --- |
| `local` | `docs/deployment/env.local.template` | MacBook checkout |
| `development-server` | `docs/deployment/env.development-server.template` | `vps-dev` |
| `production-like` | `docs/deployment/env.production-like.template` | `vps-gw` |

Copy a template to an untracked host-local path before use. Do not edit tracked templates with real values.

## Readiness Command

```bash
uv run awf deployment-readiness --profile local --json
uv run awf deployment-readiness --profile development-server --env-file /path/outside/git/development.env --json
uv run awf deployment-readiness --profile production-like --env-file /path/outside/git/production-like.env --json
```

The command returns structured checks for:

- required local tools such as Python, Git, `uv`, and Docker where a service-backed profile needs it
- required repo paths for Pydantic AI, durable smoke, Beads, deployment docs, and run evidence
- writable evidence paths under `.agent-runs/verifications/` and `/tmp`
- required and optional env names, with every present value redacted
- template validation that fails when a tracked template assigns a non-placeholder secret value

## Credential Policy

The local profile is the deterministic closure lane. It must pass readiness and fixture validation with Langfuse, DBOS,
Logfire, and model-provider credentials unset. Service-backed Langfuse and production DBOS storage are stricter
development-server or production-like concerns and should report missing configuration until an operator provides
external host-local secrets.

`LOGFIRE_TOKEN` remains an optional operator-provided export name only. It is not required evidence for the self-hosted
assessment and must not make deterministic validation depend on hosted Logfire.

## Fallback Proof

T008 records the absence behavior with:

```bash
uv run awf deployment-fallback-proof --write --json
```

The proof runs with an empty environment. The `local` profile must pass readiness and smoke with no hosted credentials,
external model provider, network dependency, or service-backed deployment secrets. The `development-server` and
`production-like` profiles must report missing required self-hosted configuration and skip candidate/durable smoke work
instead of silently depending on hosted services.
