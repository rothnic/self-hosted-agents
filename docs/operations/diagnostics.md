# Health, Logs, Traces, And Diagnostics Runbook

Status: added for Goal 005 T010
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

This runbook defines the diagnostic path for the selected Pydantic AI plus Langfuse and DBOS deployment profiles. It
covers the evidence another agent needs when app behavior, observability ingestion, durable runtime state, or storage
health is unclear.

This is a runbook and inspection checkpoint. T012 records the clean-path rehearsal after the remaining operations
runbooks are complete.

## Diagnostic Surfaces

| Surface | Local profile evidence | Service-backed evidence | First command |
| --- | --- | --- | --- |
| Workflow control plane | `.beads/issues.jsonl`, `.agent-runs/claims/`, `.agent-runs/reports/` | same repo paths on controlled host | `uv run awf ready-work --json` |
| Pydantic AI app | run artifact, trace artifact, evaluation artifact | same artifacts plus service env presence | `uv run awf deployment-smoke --profile local --write --json` |
| Local trace export | `.trace.json` files with `trace_id` | repo trace artifact plus Langfuse trace visibility | `find .agent-runs -name '*.trace.json' -print` |
| Pydantic Evals | `.evaluation.json` files with `evaluation_id` | same repo-local artifact | `find .agent-runs -name '*.evaluation.json' -print` |
| DBOS durable runtime | durable smoke JSON and transient `/tmp` state | DBOS database health and smoke artifact | `uv run python apps/pydantic-ai/durable_smoke.py --help` |
| Langfuse observability | absent by default, credential-free proof should pass | Docker Compose services, OTLP endpoint, trace API | `docker compose ps` |
| Langfuse storage | not required locally | Postgres, ClickHouse, Redis or Valkey, object storage | `docker compose logs --tail=200` |

## Health Checks

### Local Profile

Use local checks first because they must remain credential-free:

```bash
uv run awf deployment-readiness --profile local --json
uv run awf deployment-smoke --profile local --write --json
uv run awf verify --profile health --json
```

Expected evidence:

- readiness reports no required hosted credentials
- smoke writes a repo-local `awf.deployment-smoke.v1` artifact
- smoke includes `run_id`, `trace_id`, `evaluation_id`, and DBOS durable workflow evidence
- health verification reports failed checks as workflow issues instead of continuing hidden failures

### Development-Server Or Production-Like Profile

Run profile checks with an env file outside git:

```bash
uv run awf deployment-readiness --profile development-server --env-file /path/outside/git/development.env --json
uv run awf deployment-smoke --profile development-server --env-file /path/outside/git/development.env --write --json
```

Expected evidence:

- missing service configuration is reported by variable name only
- secret values are not printed
- service-backed smoke either records trace and durable evidence or fails fast with the missing self-hosted prerequisite
- repo-local evidence remains the review surface even when the service runs on `vps-dev` or `vps-gw`

## Log Collection

### Repo And Workflow Logs

Capture the workflow state before inspecting service logs:

```bash
git status --short --branch
uv run awf context-index --json
uv run awf ready-work --json
find .agent-runs/claims -maxdepth 2 -name '*.json' -print
find .agent-runs/reports .agent-runs/verifications -maxdepth 3 -type f -print
```

Expected evidence:

- active claims are named
- relevant report, verification, trace, eval, and durable artifact paths are listed
- the diagnostic note identifies whether the repo was clean before service inspection

### Langfuse Service Logs

For a Docker Compose Langfuse deployment, inspect service status and recent logs from the controlled host:

```bash
cd ~/data/projects/langfuse
docker compose ps
docker compose logs --tail=200 langfuse
docker compose logs --tail=200 postgres
docker compose logs --tail=200 clickhouse
docker compose logs --tail=200 redis
```

If the Compose service names differ, record the actual service names from `docker compose ps` and use those names in the
diagnostic evidence.

Expected evidence:

- Compose project path or equivalent service path
- service names and status
- bounded log tail output or a copied log bundle path outside git
- explicit gap when Langfuse is not running for the current profile

## Trace Inspection

### Repo-Local Trace Evidence

Local trace evidence is required even when Langfuse is unavailable:

```bash
find .agent-runs/reports .agent-runs/verifications -name '*.trace.json' -print
find .agent-runs/reports .agent-runs/verifications -name '*.evaluation.json' -print
```

For a deployment smoke bundle, inspect the top-level smoke artifact and child paths:

```bash
uv run python -m json.tool .agent-runs/reports/goal-005/<smoke-id>/deployment-smoke.json
```

Expected evidence:

- trace artifact path
- `trace_id` matched to the Pydantic AI run artifact
- `evaluation_id` matched to the deterministic evaluation artifact
- DBOS durable workflow id or explicit durable smoke failure

### Self-Hosted Langfuse Trace Evidence

When a self-hosted Langfuse profile is running, verify ingestion from the controlled endpoint without relying on hosted
SaaS:

```bash
curl -fsS "$LANGFUSE_BASE_URL/api/public/health"
curl -fsS "$LANGFUSE_BASE_URL/api/public/otel/v1/traces" || true
```

The OTLP traces endpoint may reject a bare GET request. That is acceptable when health succeeds and the smoke artifact
records whether ingestion was attempted, skipped, or failed.

Expected evidence:

- redacted `LANGFUSE_BASE_URL` host
- Langfuse health result
- repo-local trace artifact path
- Langfuse trace URL, trace id, or explicit ingestion gap

## Durable Runtime Diagnostics

For local proof, inspect the DBOS durable smoke artifact rather than treating disposable `/tmp` SQLite files as durable
review evidence:

```bash
uv run python apps/pydantic-ai/durable_smoke.py --output /tmp/pydantic-ai-durable-smoke.json --pretty
find .agent-runs/reports .agent-runs/verifications -name '*durable-smoke*.json' -print
```

For service-backed DBOS storage, inspect database connectivity and then run a smoke or health check:

```bash
psql "$DBOS_DATABASE_URL" -c 'select current_database();'
uv run awf deployment-smoke --profile development-server --env-file /path/outside/git/development.env --write --json
```

Expected evidence:

- local durable smoke artifact or service-backed database name
- durable workflow id
- retry, resume, or review-wait summary when present
- explicit gap when production DBOS storage is not configured

## Storage Diagnostics

Langfuse storage is private service state. Diagnose it from the controlled host:

```bash
cd ~/data/projects/langfuse
docker compose ps postgres clickhouse redis
docker compose exec postgres pg_isready -U postgres
docker compose exec clickhouse clickhouse-client --query "SELECT 1"
```

If object storage is configured, inspect it with the deployment-specific command and record the exact command:

```bash
docker compose ps
```

Expected evidence:

- Postgres readiness result
- ClickHouse query result
- Redis or Valkey service status
- object storage status or explicit gap
- no secret values in copied output

## Incident Triage Procedure

1. Capture `git status --short --branch` and active claim paths.
2. Run `uv run awf deployment-readiness --profile local --json`.
3. Run `uv run awf deployment-smoke --profile local --write --json` when local evidence is needed.
4. For service-backed profiles, run readiness with the external env file and collect bounded service logs.
5. Match `run_id`, `trace_id`, `evaluation_id`, and durable workflow id across the repo-local artifacts.
6. Record missing self-hosted service prerequisites as gaps, not as hosted-service workarounds.
7. Log durable workflow failures with `uv run awf issue-log --write` when a scheduled health loop finds them.

## T010 Evidence Expectations

An acceptable T010 report names:

- app health command and result
- Langfuse health or explicit service-backed gap
- DBOS diagnostics command and local proof artifact or storage gap
- storage diagnostics command and result or explicit gap
- log bundle path or bounded log commands inspected
- trace correlation path with `run_id`, `trace_id`, and `evaluation_id`
- incident triage command sequence another agent can repeat

## Current Gaps

- T010 documents diagnostics but does not rehearse the full clean-path incident response.
- Production DBOS storage diagnostics still require controlled service-backed storage proof.
- Langfuse service-backed trace visibility still requires host-local self-hosted configuration outside git.
- T012 must record a clean-path or fresh setup rehearsal with commands, evidence, and remaining gaps.
