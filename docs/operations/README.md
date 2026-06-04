# Operations Runbooks

Goal 005 operations runbooks collect the commands and evidence another agent needs to operate the selected Pydantic AI
plus Langfuse/DBOS stack without prior chat context.

## Index

- `backup-restore-reset.md`: backup, restore, and reset procedures for databases, service state, and run evidence.
- `diagnostics.md`: health, log, trace, and diagnostics procedures for app, observability, durable runtime, and storage.
- `recovery-retention-cost.md`: rollback, recovery, retention, resource, and cost notes for one-engineer operation.
- `.agent-runs/reports/goal-005/t012-clean-path-rehearsal-20260604.md`: clean-path rehearsal evidence, gaps, and
  follow-up ticket routing.

## Boundaries

- Runbooks name secret and storage surfaces without committing secret values.
- Local deterministic validation remains the default proof path.
- Service-backed Langfuse and production DBOS procedures stay self-hosted and require host-local configuration outside
  git.
- T012 records a local clean-path rehearsal. Service-backed Langfuse and production DBOS proof remains follow-up work.
