# Self-Hosted Deployment Profiles

Status: updated through Goal 005 T003
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`
BDD contract: `tests/workflow/features/self_hosted_deployment_operations.feature`

## Purpose

Define the three deployment profiles another agent can choose from without reading prior chat:

- `local`: deterministic development and fixture validation on the MacBook.
- `development-server`: heavier service-backed proof runs on `vps-dev`.
- `production-like`: controlled always-on management proof on `vps-gw`.

These profiles do not promote the stack as final production infrastructure. They define the operating surface that later
Goal 005 tickets harden with detailed ports, volumes, environment templates, startup, smoke, backup, recovery, and
fresh-setup evidence.

Detailed service boundaries, ports, volumes, storage paths, secret names, and machine ownership are in
`docs/deployment/service-boundaries.md`.

## Shared Principles

- Core behavior must run without required third-party hosted services.
- Secrets are named here but never committed.
- Service-backed Langfuse evidence is additive; repo-local trace artifacts remain required.
- DBOS SQLite remains acceptable for deterministic fixture validation, but production storage proof remains a blocker.
- Beads, `awf`, specs, BDD contracts, and `.agent-runs/` remain the source of truth for work state and evidence.
- A presenter agent records goal evidence, and a separate reviewer agent accepts or rejects it.

## Profile Summary

| Profile | Target | Primary use | Service-backed proof | Closure boundary |
| --- | --- | --- | --- | --- |
| `local` | MacBook checkout | ticket validation and development | optional only | credential-free fixtures |
| `development-server` | `vps-dev` | heavier Langfuse/DBOS proof | expected when needed | repo-local plus controlled VM evidence |
| `production-like` | `vps-gw` | always-on operations proof | expected before promotion | reviewer-accepted ops evidence |

## Local Profile

### Intent

The local profile is the default for agents implementing and closing ordinary tickets. It proves the selected stack can
produce deterministic run, trace, evaluation, durable, and workflow evidence without cloud services.

### Target Machine

- Machine: MacBook checkout under `/Users/nroth/workspace/self-hosted-agents`.
- Runtime: repo `uv` environment bootstrapped by `tools/agent-workflow/bootstrap-dev.sh --install-tools`.
- Persistence: repo-local artifacts under `.agent-runs/` plus disposable local paths under `/tmp`.

### Included Services

- `awf` workflow CLI and Beads local ticket state.
- `apps/pydantic-ai/` deterministic fixture runner.
- Repo-local OpenTelemetry-style trace artifact writer.
- Pydantic Evals deterministic evaluation artifact writer.
- DBOS durable smoke path using disposable SQLite and JSONL paths.

### Optional Services

- Local self-hosted Langfuse on `http://localhost:3000` when the ticket explicitly asks for service-backed proof.

### Secret Names

The local profile must pass when these are unset:

- `LANGFUSE_BASE_URL`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PROJECT_ID`
- `LOGFIRE_TOKEN`
- model-provider credentials

### Evidence Expectations

- `uv run awf workflow-fixture-test`
- `uv run awf verify --profile ticket --json`
- repo-local `.trace.json` and `.evaluation.json` artifacts when a Pydantic AI run is part of the slice
- explicit gaps when Langfuse, production DBOS storage, live model calls, or service-backed smoke evidence are absent

## Development-Server Profile

### Intent

The development-server profile moves heavier controlled proof work to `vps-dev`. Use it when local memory, Docker
capacity, or long-running smoke work would slow down the MacBook.

### Target Machine

- Machine: `vps-dev`.
- Project path: `~/data/projects/self-hosted-agents`.
- Runtime: repo `uv` environment, Git, Docker or equivalent service runtime, and Beads.
- Persistence: repo artifacts in the checkout plus service state under `~/data/projects` or documented service paths.

### Included Services

- Pydantic AI app and deterministic fixture runner.
- Self-hosted Langfuse service when observability proof requires a running trace UI.
- DBOS durable proof path, with future production-storage experiments when T003-T008 define the topology.
- Local or VM-hosted storage services required by Langfuse and DBOS proof work.

### Secret Names

The development-server profile may use these names, stored outside git:

- `LANGFUSE_BASE_URL`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PROJECT_ID`
- `DBOS_DATABASE_URL`
- model-provider credentials for later live-model proof tickets

### Evidence Expectations

- repo-local run, trace, evaluation, durable, and health artifacts copied or written into `.agent-runs/`
- service-backed Langfuse proof only when the ticket requires it
- commands and service state paths recorded in the relevant report or verification artifact
- deterministic fallback evidence showing fixture validation still passes without service credentials

## Production-Like Profile

### Intent

The production-like profile is the controlled always-on operations proof for one-engineer management. It should run only
after the development-server profile has enough evidence to make operating burden, backup, recovery, and retention
risks explicit.

### Target Machine

- Machine: `vps-gw`.
- Project path: `~/data/projects/self-hosted-agents`.
- Runtime: minimal always-on services for management, health checks, and evidence capture.
- Persistence: documented service volumes and backup targets defined by later Goal 005 tickets.

### Included Services

- Pydantic AI product-baseline lane or deployment smoke entrypoint.
- Self-hosted Langfuse or accepted self-hosted observability alternative.
- DBOS durable runtime with production storage once the DBOS production-storage proof closes.
- Health, log, trace, backup, restore, reset, and recovery surfaces defined by Goal 005 runbooks.

### Secret Names

The production-like profile must use externally managed secrets, never committed values:

- `LANGFUSE_BASE_URL`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PROJECT_ID`
- `DBOS_DATABASE_URL`
- database credentials for observability and durable runtime services
- backup target credentials when backup proof requires remote or object storage
- model-provider credentials only for explicit live-model proof tickets

### Evidence Expectations

- deployment smoke evidence that links run id, trace id, evaluation id, durable run id, service health, and Beads issue
- backup, restore, reset, health, log, trace, rollback, and recovery runbook evidence
- fresh setup or clean-path rehearsal report with gaps and follow-up tickets
- independent reviewer acceptance before Goal 005 can be called complete

## Current Gaps Routed To Later Goal 005 Tickets

- T003 documented detailed service boundaries, ports, volumes, storage paths, and target machine ownership.
- T004 adds environment templates and readiness checks that report missing prerequisites without exposing secrets.
- T005 adds or documents startup for the selected Pydantic AI, Langfuse, and DBOS profile.
- T006-T008 add deployment smoke and credential-free fallback evidence.
- T009-T012 add runbooks and fresh-setup rehearsal evidence.
- T013 presents final Goal 005 evidence to an independent reviewer.
