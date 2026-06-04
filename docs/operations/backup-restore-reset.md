# Backup, Restore, And Reset Runbook

Status: added for Goal 005 T009
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

This runbook defines backup, restore, and reset procedures for the current reference deployment profiles. It covers the
state surfaces another agent must protect before Goal 005 can claim an operations-ready self-hosted stack:

- databases and durable runtime state
- self-hosted Langfuse service state
- repo-local run evidence, reviews, claims, increments, and Beads state

This is a runbook and inspection checkpoint. T012 records the clean-path rehearsal after the remaining operations
runbooks are complete.

## State Inventory

| State surface | Local profile | Development-server profile | Production-like profile | Git policy |
| --- | --- | --- | --- | --- |
| Beads issue state | `.beads/issues.jsonl` | repo `.beads/issues.jsonl` | repo `.beads/issues.jsonl` | commit after workflow mutation |
| Claims and increments | `.agent-runs/claims/`, `.agent-runs/increments/` | same repo paths | same repo paths | commit durable evidence |
| Run reports and reviews | `.agent-runs/reports/`, `.agent-runs/reviews/` | same repo paths | same repo paths | commit selected proof artifacts |
| Verification artifacts | `.agent-runs/verifications/` | same repo path | same repo path | commit selected proof artifacts |
| DBOS local proof state | disposable `/tmp/*.sqlite` and `/tmp/*.jsonl` | documented host path when used | production database later | do not commit raw DB files |
| Langfuse service state | optional local checkout | `~/data/projects/langfuse` or documented equivalent | documented persistent path | do not commit service data |
| Langfuse databases | Docker volumes or explicit host paths | host-local volumes | production-like volumes | backup outside git |
| Langfuse object storage | Docker volume or explicit host path | host-local volume | production-like volume | backup outside git |

## Backup Procedure

### 1. Freeze Workflow Mutations

Before taking a backup, stop scheduled workers or record that none are active:

```bash
uv run awf ready-work --json
find .agent-runs/claims -maxdepth 2 -name '*.json' -print
git status --short --branch
```

Expected evidence:

- no active claim is modifying the same profile state, or the active claim is recorded in the backup note
- git status is captured before backup

### 2. Backup Repo-Local Evidence

Create a host-local archive outside git:

```bash
mkdir -p /tmp/self-hosted-agents-backups
tar -czf /tmp/self-hosted-agents-backups/repo-evidence-$(date -u +%Y%m%dT%H%M%SZ).tgz \
  .beads \
  .agent-runs/claims \
  .agent-runs/increments \
  .agent-runs/reports \
  .agent-runs/verifications \
  specs \
  docs
```

If `.agent-runs/reviews` exists, include it in the archive as an additional repo-local evidence surface. If it does not
exist, record that reviewer acceptance is currently stored in Beads comments and committed reports, then continue with
the existing paths instead of failing the backup.

Expected evidence:

- archive path and byte size are recorded in the rehearsal report
- archive stays outside git
- selected proof artifacts remain committed separately when they are review evidence
- absent optional evidence directories are recorded as gaps or fixed runbook drift, not ignored

### 3. Backup DBOS State

For the local profile, DBOS state is disposable proof state under `/tmp`; the durable evidence is the committed JSON
artifact, not the SQLite file. Record the artifact instead of backing up the raw local SQLite file:

```bash
find .agent-runs/reports .agent-runs/verifications -name '*durable-smoke*.json' -print
```

For a service-backed DBOS profile, use the operator-provided `DBOS_DATABASE_URL` and write a database dump outside git:

```bash
mkdir -p /tmp/self-hosted-agents-backups
pg_dump "$DBOS_DATABASE_URL" \
  --format=custom \
  --file=/tmp/self-hosted-agents-backups/dbos-$(date -u +%Y%m%dT%H%M%SZ).dump
```

Expected evidence:

- local profile records durable JSON artifact paths
- service-backed profile records dump path, size, source profile, and redacted database URL presence

### 4. Backup Langfuse State

Langfuse service state is self-hosted and must be backed up from the controlled host, not from a hosted SaaS project.
When the profile uses Docker Compose, inspect the active Compose project and dump databases or copy volumes to a
host-local backup path:

```bash
cd ~/data/projects/langfuse
docker compose ps
docker compose exec postgres pg_dumpall -U postgres > /tmp/self-hosted-agents-backups/langfuse-postgres.sql
docker compose exec clickhouse clickhouse-client --query "BACKUP DATABASE default TO Disk('backups', 'langfuse')"
```

If object storage is configured as a local volume, copy that volume or use the configured self-hosted object-store
backup command. Record the exact command used because object storage differs by deployment.

Expected evidence:

- Compose project path or equivalent service path
- Postgres backup artifact
- ClickHouse backup artifact or explicit gap if the current profile has no ClickHouse backup target
- object storage backup artifact or explicit gap

## Restore Procedure

### 1. Restore Repo-Local Evidence

Restore into a clean checkout or temporary path first:

```bash
mkdir -p /tmp/self-hosted-agents-restore-check
tar -xzf /tmp/self-hosted-agents-backups/<repo-evidence>.tgz -C /tmp/self-hosted-agents-restore-check
```

Verify the restored evidence:

```bash
test -f /tmp/self-hosted-agents-restore-check/.beads/issues.jsonl
find /tmp/self-hosted-agents-restore-check/.agent-runs/reports -type f | head
```

Expected evidence:

- restored Beads file exists
- restored report and verification artifacts are inspectable
- restore target is not the live checkout until the operator decides to replace state

### 2. Restore DBOS State

For the local profile, rerun deterministic smoke instead of restoring disposable SQLite:

```bash
uv run awf deployment-smoke --profile local --write --json
```

For a service-backed DBOS profile, restore the database dump into a controlled database:

```bash
pg_restore --dbname "$DBOS_DATABASE_URL" --clean --if-exists /tmp/self-hosted-agents-backups/<dbos>.dump
```

Expected evidence:

- local profile records a new smoke artifact
- service-backed restore records dump path, target profile, and a post-restore smoke or health check

### 3. Restore Langfuse State

Stop ingestion before restoring service state:

```bash
cd ~/data/projects/langfuse
docker compose stop
```

Restore Postgres, ClickHouse, and object storage from the host-local backup artifacts, then restart:

```bash
docker compose up -d
uv run awf deployment-readiness --profile development-server --env-file /path/outside/git/development.env --json
```

Expected evidence:

- restore commands and backup artifact paths
- post-restore readiness result
- explicit gap when the current profile has no service-backed backup to restore

## Reset Procedure

### Local Profile Reset

The local reset removes generated proof artifacts only when the operator is intentionally discarding local evidence.
Do not delete committed reports during normal ticket work.

```bash
rm -f /tmp/pydantic-ai-dbos-*.sqlite /tmp/pydantic-ai-dbos-*.jsonl
uv run awf deployment-readiness --profile local --json
uv run awf deployment-smoke --profile local --write --json
```

Expected evidence:

- reset command output
- new readiness result
- new smoke artifact path

### Development-Server Or Production-Like Reset

Reset self-hosted services only after a backup exists or a reviewer accepts that state can be discarded:

```bash
cd ~/data/projects/langfuse
docker compose down
docker volume ls
```

Remove volumes only after recording the exact volume names and approval reason:

```bash
docker volume rm <langfuse-volume-name>
```

For DBOS service-backed storage, reset through the controlled database after recording the database name and backup
artifact:

```bash
psql "$DBOS_DATABASE_URL" -c 'select current_database();'
```

Expected evidence:

- backup artifact or discard approval
- exact volume or database names
- post-reset readiness or smoke result

## T009 Evidence Expectations

An acceptable T009 report names:

- the backup archive or dry-run command inspected
- repo-local evidence paths covered by backup
- DBOS local proof artifact or service-backed dump gap
- Langfuse backup artifacts or explicit service-backed gap
- restore target and verification command
- reset command boundaries and required approval before destructive service-state deletion

## Current Gaps

- T012 rehearsed the repo-local backup and restore path, and fixed the optional `.agent-runs/reviews` archive drift
  found during rehearsal.
- Production DBOS storage and Langfuse persistent volume backups still require controlled service-backed evidence.
