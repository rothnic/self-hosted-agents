# Goal 005 T010 Diagnostics Runbook Evidence

## Ticket

- Beads issue: `awf-hic`
- Spec task: `specs/006-self-hosted-deployment-operations-reference/tasks.md#T010`
- Acceptance: `uv run awf workflow-fixture-test`

## Implemented

- Added `docs/operations/diagnostics.md`.
- Updated `docs/operations/README.md` with the diagnostics runbook entry.
- Updated deployment profile, service-boundary, and Goal 005 routing docs through T010.
- Added `deployment_diagnostics_runbook_data()` to the workflow fixture helper.
- Added fixture assertion `deployment diagnostics runbook covers health logs traces and storage surfaces`.

## Runbook Coverage

The runbook covers:

- app health through local readiness, local smoke, and health verification commands
- Langfuse health, Compose status, bounded service logs, and explicit service-backed gaps
- repo-local trace inspection with `run_id`, `trace_id`, and `evaluation_id` correlation
- DBOS durable runtime diagnostics for local proof artifacts and service-backed storage gaps
- Langfuse storage diagnostics for Postgres, ClickHouse, Redis or Valkey, and object storage gaps
- incident triage sequence another agent can repeat without hosted services

## Validation

- `uv run python` helper check for `deployment_diagnostics_runbook_data()`: passed, no missing checks.
- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `uv run awf workflow-fixture-test --json`: passed `53/53`.
- `uv run awf repo-hygiene --json`: passed with `checked_files=336`.
- `git diff --check`: passed.

## Boundary

T010 documents diagnostics and adds deterministic fixture validation for the runbook shape. It does not claim a full
clean-path incident response rehearsal. T012 remains responsible for the clean-path or fresh setup rehearsal with
commands, evidence, and remaining gaps.
