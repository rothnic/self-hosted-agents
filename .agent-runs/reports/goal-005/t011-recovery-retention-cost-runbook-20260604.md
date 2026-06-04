# Goal 005 T011 Recovery, Retention, Resource, And Cost Evidence

## Ticket

- Beads issue: `awf-2jm`
- Spec task: `specs/006-self-hosted-deployment-operations-reference/tasks.md#T011`
- Acceptance: `uv run awf workflow-fixture-test`

## Implemented

- Added `docs/operations/recovery-retention-cost.md`.
- Updated `docs/operations/README.md` with the new runbook entry.
- Updated deployment profile, service-boundary, and Goal 005 routing docs through T011.
- Added `deployment_recovery_retention_cost_runbook_data()` to the workflow fixture helper.
- Added fixture assertion `deployment recovery retention cost runbook covers one engineer operation`.

## Runbook Coverage

The runbook covers:

- rollback freeze, target selection, and validation commands
- recovery command sequences for workflow/app failures, DBOS durable runtime failures, and Langfuse or storage failures
- retention policy surfaces for Beads, claims, reports, verifications, DBOS local state, backups, Langfuse data, and logs
- resource expectations for local, development-server, and production-like profiles
- cost and operating-burden tradeoffs for hosted services, Langfuse, DBOS storage, model calls, backups, and always-on
  services
- escalation criteria and follow-up issue policy when one-engineer operation becomes unsafe

## Validation

- `uv run python` helper check for `deployment_recovery_retention_cost_runbook_data()`: passed, no missing checks.
- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `uv run awf workflow-fixture-test --json`: passed `54/54`.
- `uv run awf repo-hygiene --json`: passed with `checked_files=339`.
- `git diff --check`: passed.

## Boundary

T011 documents rollback, recovery, retention, resource, and cost procedures and adds deterministic fixture validation
for the runbook shape. It does not claim a clean-path recovery rehearsal. T012 remains responsible for the clean-path or
fresh setup rehearsal with commands, evidence, and remaining gaps.
