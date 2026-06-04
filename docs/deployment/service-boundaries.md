# Deployment Service Boundaries

Status: updated through Goal 005 T009
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

This document names the service boundaries, ports, volumes, storage paths, secrets, and target machines for the
selected self-hosted stack. It extends `docs/deployment/profiles.md` and is paired with
`docs/deployment/environment-readiness.md` for environment templates and readiness checks,
`docs/deployment/startup.md` for startup commands and documented service equivalents, and
`docs/deployment/smoke.md` for the representative selected-stack smoke command, and
`docs/operations/backup-restore-reset.md` for backup, restore, and reset procedures.

## Boundary Rules

- Only the Langfuse UI and OTLP ingestion endpoint should be reachable by the candidate app during service-backed proof.
- Pydantic AI fixture and smoke commands are CLI entrypoints, not always-on HTTP services.
- DBOS durable evidence is local SQLite proof until a later ticket proves production storage.
- Internal observability storage services are private to the Langfuse deployment and are not public proof endpoints.
- Secret names may appear in docs and templates, but secret values must stay outside git.
- Repo-local artifacts remain the review surface even when service-backed evidence is collected on a VPS.

## Profile Targets

| Profile | Target machine | Repo path | Service-state root | Public ingress |
| --- | --- | --- | --- | --- |
| `local` | MacBook | `/Users/nroth/workspace/self-hosted-agents` | `/tmp` and repo `.agent-runs/` | none required |
| `development-server` | `vps-dev` | `~/data/projects/self-hosted-agents` | `~/data/projects` | SSH only by default |
| `production-like` | `vps-gw` | `~/data/projects/self-hosted-agents` | `~/data/projects` | operator-approved only |

The development-server profile is the preferred target for Docker-backed Langfuse and DBOS storage experiments. The
production-like profile is reserved for always-on operating proof after the lower-risk development-server boundary is
understood.

## Core Service Boundaries

| Boundary | Owner | Runtime | Port exposure | Required in fixture mode | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| Workflow control plane | repo | `uv run awf`, Beads, git | none | yes | `.beads/`, `.agent-runs/claims/`, `.agent-runs/increments/` |
| Pydantic AI app | `apps/pydantic-ai/` | repo `uv` Python CLI | none | yes | `.agent-runs/verifications/*.json` |
| Local trace export | `apps/pydantic-ai/` | JSON artifact writer | none | yes | `.agent-runs/verifications/*.trace.json` |
| Pydantic Evals export | `apps/pydantic-ai/` | deterministic eval runner | none | yes | `.agent-runs/verifications/*.evaluation.json` |
| Langfuse observability | self-hosted Langfuse checkout | Docker Compose or equivalent | `3000` to app only | no | Langfuse trace API plus repo trace artifact |
| Langfuse storage | Langfuse deployment | Postgres, ClickHouse, Redis or Valkey, object storage | private only | no | later backup and health evidence |
| DBOS durable runtime | `apps/pydantic-ai/durable_smoke.py` | repo `uv` Python process | none | yes for local proof | durable smoke JSON artifact |
| DBOS durable storage | DBOS runtime | SQLite now, production database later | private only | SQLite only | DBOS database path plus durable artifact |

## Ports

| Port or endpoint | Boundary | Profile | Exposure rule | Notes |
| --- | --- | --- | --- | --- |
| none | Pydantic AI app | all | no listener | Current app path is invoked by CLI commands. |
| none | local trace and eval export | all | no listener | Evidence is written as repo-local JSON files. |
| `3000` | Langfuse web and OTLP HTTP | development-server, production-like | reachable only by the app/operator | Endpoint path: `/api/public/otel/v1/traces`. |
| `127.0.0.1:13300` | SSH tunnel to Langfuse proof | local client to controlled host | localhost only | Existing proof used this as the local tunnel endpoint. |
| `127.0.0.1:3300 -> 3000` | Langfuse host mapping from prior proof | controlled host | host-local or tunnel-only | Existing evidence recorded this mapping; do not assume it is final. |
| `5432` | Postgres for Langfuse or future DBOS storage | service host only | private network or localhost | Do not expose as public ingress. |
| `6379` | Redis or Valkey for Langfuse | service host only | private network or localhost | Internal queue/cache service only. |
| `8123`, `9000` | ClickHouse for Langfuse | service host only | private network or localhost | Internal analytics storage only. |
| object storage ports | Langfuse blob storage | service host only | private network or localhost | Internal service; concrete port depends on the chosen deployment. |

Later startup and smoke tickets must verify the actual listening ports for the selected deployment instead of treating
this table as live service evidence.

## Storage Paths And Volumes

| Boundary | Local profile path | Development-server path | Production-like path | Git policy |
| --- | --- | --- | --- | --- |
| Repo checkout | `/Users/nroth/workspace/self-hosted-agents` | `~/data/projects/self-hosted-agents` | `~/data/projects/self-hosted-agents` | tracked source only |
| Run evidence | `.agent-runs/verifications/` | repo `.agent-runs/verifications/` | repo `.agent-runs/verifications/` | commit selected proof artifacts |
| Reports and reviews | `.agent-runs/reports/`, `.agent-runs/reviews/` | same repo paths | same repo paths | commit durable acceptance evidence |
| Beads state | `.beads/issues.jsonl` | same repo path | same repo path | commit ticket state changes |
| DBOS SQLite proof | `/tmp/pydantic-ai-dbos-*.sqlite` | `/tmp` or documented service path | not final until storage proof | do not commit SQLite files |
| DBOS side-effect logs | `/tmp/pydantic-ai-dbos-*.jsonl` | `/tmp` or documented service path | not final until storage proof | do not commit transient logs |
| Langfuse checkout | optional `~/data/projects/langfuse` | `~/data/projects/langfuse` | `~/data/projects/langfuse` or documented equivalent | do not vendor upstream checkout |
| Langfuse database volumes | Docker-managed or documented local paths | under Langfuse deployment root or Docker volumes | documented persistent volume paths | do not commit service data |
| Langfuse object storage | Docker-managed or documented local paths | under Langfuse deployment root or Docker volumes | documented persistent volume paths | do not commit object data |
| Backup targets | `/tmp/self-hosted-agents-backups` | host-local backup path under operator control | host-local or operator-approved backup target | commit runbook, not backups |

## Secret Names

These names are the allowed configuration surface for the current deployment reference. Values must be injected through
the operator shell, local service environment, or a host secret store outside this repository.

### Observability

- `LANGFUSE_BASE_URL`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PROJECT_ID`
- `LANGFUSE_INIT_ORG_ID`
- `LANGFUSE_INIT_ORG_NAME`
- `LANGFUSE_INIT_PROJECT_ID`
- `LANGFUSE_INIT_PROJECT_NAME`
- `LANGFUSE_INIT_PROJECT_PUBLIC_KEY`
- `LANGFUSE_INIT_PROJECT_SECRET_KEY`
- `LANGFUSE_INIT_USER_EMAIL`
- `LANGFUSE_INIT_USER_NAME`
- `LANGFUSE_INIT_USER_PASSWORD`
- `LOGFIRE_TOKEN`

`LOGFIRE_TOKEN` is named only as an optional operator-provided export surface. It is not accepted as required evidence
for this self-hosted assessment.

### Durable Runtime And Storage

- `DBOS_DATABASE_URL`
- database username, password, database, and host variables selected by the later environment template

### Model Providers

- model-provider API keys for explicit live-model proof tickets only

Fixture validation must pass when all observability, durable storage, and model-provider secrets are unset.

## Profile-Specific Boundary Notes

### Local

- Runs `uv run python apps/pydantic-ai/run.py` and `uv run python apps/pydantic-ai/durable_smoke.py` from the repo.
- Requires no listening service and no hosted credentials.
- Writes durable review evidence under `.agent-runs/` and transient DBOS state under `/tmp`.
- May connect to Langfuse through `127.0.0.1:13300` only when a ticket explicitly requests service-backed proof.

### Development Server

- Uses `vps-dev` for Docker-backed Langfuse, heavier smoke commands, or DBOS storage experiments.
- Keeps the repo checkout under `~/data/projects/self-hosted-agents`.
- Keeps service checkouts and state under `~/data/projects`, with exact paths recorded in the relevant evidence.
- Should prefer SSH tunnels or private networking over public ports for proof work.

### Production-Like

- Uses `vps-gw` for controlled always-on operating proof after the development-server profile is understood.
- Must not be called production-ready until backup, restore, reset, health, trace, recovery, retention, and rehearsal
  evidence is accepted.
- Must keep service ports private unless an operator explicitly documents a public ingress decision.
- Must record persistent volume and backup target paths before final Goal 005 acceptance.

## Deferred Work

- T004 added environment templates and readiness checks for these names and paths.
- T005 added or documented startup for the selected profile.
- T006 added the selected-stack smoke command.
- T007 captured committed local smoke evidence across the app, observability, durable runtime, and health boundaries.
- T008 captured credential-free fallback proof for absent deployment services or secrets.
- T009 added backup, restore, and reset runbooks for database, service state, and run evidence.
- T010-T012 add diagnostics, recovery, operating burden, and rehearsal evidence.
- T013 presents final Goal 005 evidence to an independent reviewer.
