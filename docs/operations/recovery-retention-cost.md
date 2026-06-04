# Rollback, Recovery, Retention, Resource, And Cost Runbook

Status: added for Goal 005 T011
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

This runbook defines the one-engineer operating model for rollback, recovery, retention, resource usage, and cost
control across the selected Pydantic AI plus Langfuse and DBOS deployment profiles.

This is a runbook and inspection checkpoint. T012 records the clean-path rehearsal after the operations runbooks are
complete.

## Operating Principles

- Preserve repo-local evidence before changing live service state.
- Prefer rollback to a known good commit plus deterministic local smoke before service reset.
- Keep production-like operation small enough for one engineer to understand, inspect, and recover.
- Treat service-backed Langfuse and production DBOS storage as self-hosted surfaces, not hosted-service shortcuts.
- Record gaps as follow-up Beads issues instead of silently carrying unsupported operating burden.

## Rollback Procedure

### 1. Freeze And Capture Current State

Capture the live workflow and service state before rolling back:

```bash
git status --short --branch
uv run awf ready-work --json
find .agent-runs/claims -maxdepth 2 -name '*.json' -print
uv run awf deployment-readiness --profile local --json
```

Expected evidence:

- current branch and dirty state
- active claims or explicit note that none are active
- current readiness result
- reason for rollback

### 2. Choose The Rollback Target

Use a reviewed commit, tag, or PR head as the rollback target:

```bash
git log --oneline --decorate -n 12
git show --stat <rollback-ref>
```

For service-backed profiles, record the matching service configuration and backup artifact before changing versions:

```bash
ls -lh /tmp/self-hosted-agents-backups
```

Expected evidence:

- rollback ref
- service profile affected
- backup artifact or explicit reason no service state is being changed

### 3. Validate Before Restarting Services

Run local deterministic validation before service-backed restart:

```bash
uv run awf workflow-fixture-test
uv run awf deployment-smoke --profile local --write --json
```

For a service-backed profile, restart only after local validation and then run readiness:

```bash
cd ~/data/projects/langfuse
docker compose up -d
uv run awf deployment-readiness --profile development-server --env-file /path/outside/git/development.env --json
```

Expected evidence:

- local fixture result
- smoke artifact path
- service readiness result or explicit service-backed gap

## Recovery Procedure

### Workflow Or App Failure

1. Capture diagnostics from `docs/operations/diagnostics.md`.
2. Run local readiness and smoke to confirm deterministic behavior.
3. If the failure is workflow-state related, inspect Beads and claims before changing code.
4. If scheduled health found the failure, log it with `uv run awf issue-log --write`.

Commands:

```bash
uv run awf context-index --json
uv run awf workflow-state-lint --json
uv run awf deployment-smoke --profile local --write --json
```

Expected evidence:

- failed command and exact profile
- claim, Beads, or workflow-state finding
- new smoke artifact or explanation why smoke was not safe
- follow-up issue id when recovery requires new work

### DBOS Durable Runtime Failure

For local proof, discard transient `/tmp` state only after preserving the evidence artifact:

```bash
find .agent-runs/reports .agent-runs/verifications -name '*durable-smoke*.json' -print
rm -f /tmp/pydantic-ai-dbos-*.sqlite /tmp/pydantic-ai-dbos-*.jsonl
uv run python apps/pydantic-ai/durable_smoke.py --output /tmp/pydantic-ai-durable-smoke.json --pretty
```

For service-backed DBOS storage, recover from the documented backup instead of deleting tables blindly:

```bash
pg_restore --dbname "$DBOS_DATABASE_URL" --clean --if-exists /tmp/self-hosted-agents-backups/<dbos>.dump
```

Expected evidence:

- durable artifact path before reset
- reset or restore command
- post-recovery durable workflow id
- explicit gap when service-backed DBOS storage is not configured

### Langfuse Or Storage Failure

Recover Langfuse from the controlled host:

```bash
cd ~/data/projects/langfuse
docker compose ps
docker compose logs --tail=200
docker compose restart
```

When storage is corrupted or missing, use the backup/restore runbook before destructive reset:

```bash
docker compose stop
```

Expected evidence:

- service names and status
- bounded log output or copied log bundle path outside git
- backup artifact used for restore, or explicit gap
- post-recovery readiness result

## Retention Policy

| Evidence or state | Default retention | Location | Cleanup rule |
| --- | --- | --- | --- |
| Beads state | keep indefinitely | `.beads/issues.jsonl` | commit workflow mutations |
| Goal reports and reviewer evidence | keep indefinitely | `.agent-runs/reports/`, `.agent-runs/reviews/` | commit selected proof artifacts |
| Claims and increments | keep while useful for audit | `.agent-runs/claims/`, `.agent-runs/increments/` | archive claims with `uv run awf cleanup-work --write --json` |
| Verification artifacts | keep selected proof artifacts | `.agent-runs/verifications/` | delete only unreferenced scratch artifacts |
| Local DBOS SQLite and JSONL | disposable | `/tmp/pydantic-ai-dbos-*` | remove during local reset after artifact is recorded |
| Backup archives | operator-controlled | `/tmp/self-hosted-agents-backups` or host path | rotate after newer backup and restore proof exist |
| Langfuse service data | operator-controlled | Docker volumes or host paths | do not delete without backup or discard approval |
| Service logs | bounded diagnostic windows | host-local log bundle outside git | keep only incident-relevant snippets in reports |

Retention gaps that affect promotion must become follow-up Beads issues before Goal 005 final acceptance.

## Resource Expectations

### Local Profile

- Expected to run without Docker services, hosted credentials, or model-provider credentials.
- Uses repo `uv`, Pydantic AI fixture runner, local trace/eval writers, and transient DBOS SQLite state.
- Suitable for ticket acceptance and deterministic workflow validation.
- If memory pressure is high, offload service-backed proof to `vps-dev` instead of running Langfuse locally.

### Development-Server Profile

- Preferred for Docker-backed Langfuse, DBOS storage experiments, and longer smoke runs.
- Expected host: `vps-dev`.
- Expected service root: `~/data/projects`.
- Requires Docker or equivalent service runtime, plus host-local env files outside git.
- Must keep public ingress closed by default; use SSH tunnels or private networking for proof work.

### Production-Like Profile

- Target host: `vps-gw`.
- Use only after development-server operations are understood.
- Keep services minimal and observable enough for one engineer.
- Do not promote to final production until backup, restore, diagnostics, rollback, recovery, retention, and rehearsal
  evidence are accepted.

## Cost And Operating Burden

| Cost surface | Default stance | Escalation trigger |
| --- | --- | --- |
| Hosted services | not required for core behavior | only explicit comparison or live proof tickets |
| Langfuse service | self-hosted on controlled infrastructure | operating burden exceeds one-engineer recovery |
| DBOS storage | local SQLite proof now, self-hosted database later | production storage proof remains missing |
| Model provider calls | absent from deterministic validation | explicit live-model proof ticket |
| Backup storage | host-local first | remote/object backup only after documented operator decision |
| Always-on services | `vps-gw` only for controlled proof | memory, cost, or recovery burden exceeds expected one-engineer operation |

If service-backed Langfuse or DBOS makes the production-like profile too costly or fragile for one engineer, record a
follow-up issue to compare Phoenix or Opik, reduce service scope, or defer production promotion.

## Escalation Criteria

Escalate to a new Beads issue or reviewer decision when:

- rollback target is unclear
- service state would be destroyed without backup or discard approval
- secret values appear in logs, reports, or artifacts
- recovery requires public ingress that is not already approved
- production DBOS storage is required but not configured
- Langfuse storage cannot be backed up or restored from controlled infrastructure
- resource or cost burden exceeds one-engineer operation

## T011 Evidence Expectations

An acceptable T011 report names:

- rollback target selection command and validation command
- recovery command sequence for workflow/app, DBOS, and Langfuse or explicit profile gap
- retention policy surfaces and cleanup boundaries
- resource expectation by local, development-server, and production-like profile
- cost and operating-burden tradeoffs
- escalation criteria and follow-up issue policy
- T012 rehearsal boundary

## Current Gaps

- T011 documents rollback, recovery, retention, resource, and cost procedures but does not rehearse them.
- Production DBOS storage retention and recovery still require controlled service-backed proof.
- Langfuse backup retention and object storage recovery still require host-local service evidence.
- T012 must record a clean-path or fresh setup rehearsal with commands, evidence, and remaining gaps.
