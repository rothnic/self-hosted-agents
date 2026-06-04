# Operations Runbooks

Goal 005 operations runbooks collect the commands and evidence another agent needs to operate the selected Pydantic AI
plus Langfuse/DBOS stack without prior chat context.

## Index

- `backup-restore-reset.md`: backup, restore, and reset procedures for databases, service state, and run evidence.
- `diagnostics.md`: health, log, trace, and diagnostics procedures for app, observability, durable runtime, and storage.

## Boundaries

- Runbooks name secret and storage surfaces without committing secret values.
- Local deterministic validation remains the default proof path.
- Service-backed Langfuse and production DBOS procedures stay self-hosted and require host-local configuration outside
  git.
- T012 records a clean-path rehearsal after the runbooks are complete.
