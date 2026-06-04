# Goal 005 T009 Backup Restore Reset Runbook Evidence

Date: 2026-06-04
Ticket: `awf-71o`
Task: `specs/006-self-hosted-deployment-operations-reference/tasks.md#T009`
Acceptance: `uv run awf workflow-fixture-test`

## Evidence

T009 added backup, restore, and reset procedures for database, service state, and run evidence:

- `docs/operations/README.md`
- `docs/operations/backup-restore-reset.md`

The runbook covers:

- repo-local evidence state: `.beads/`, `.agent-runs/claims/`, `.agent-runs/increments/`,
  `.agent-runs/reports/`, `.agent-runs/reviews/`, and `.agent-runs/verifications/`
- DBOS local proof state and service-backed database dump/restore boundaries
- self-hosted Langfuse service state, database, ClickHouse, and object-storage backup boundaries
- backup, restore, and reset procedures for local, development-server, and production-like profiles
- destructive reset safeguards that require a backup artifact or explicit discard approval

## Fixture Coverage

`uv run awf workflow-fixture-test --json` passed `52/52`.

The new fixture assertion is:

- `deployment backup restore reset runbook covers state and evidence surfaces`

It verifies that `docs/operations/backup-restore-reset.md` exists and includes the required sections, state surfaces,
commands, and evidence expectations for backup, restore, and reset work.

## Boundary

This ticket documents and validates the runbook surface. It does not claim a full fresh restore rehearsal. T012 remains
responsible for recording clean-path or fresh setup rehearsal evidence with commands, gaps, and follow-up tickets.
