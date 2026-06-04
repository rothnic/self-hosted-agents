# Goal 006 T003 Workbench Status Schema Evidence

Recorded: 2026-06-04T07:20:18Z
Presenter: Codex implementer
Ticket: awf-vht
Task: specs/007-operator-workbench-review-ux/tasks.md#T003
Acceptance: uv run awf workflow-fixture-test

## Scope

T003 defines the generated artifact schema for operator workbench status and decision summaries.
It does not implement the status report command or local UI. Those remain later Goal 006 tasks.

## Evidence Presented

- Added `docs/workbench/status-artifact-schema.md`.
- Indexed the schema from `docs/workbench/README.md`.
- Added `operator_workbench_status_schema_data()` in `tools/agent-workflow/src/agent_workflow/core.py`.
- Added the workflow fixture assertion `operator workbench generated artifact schema is defined`.

The schema defines:

- `awf.operator-workbench.status.v1` for generated operator status artifacts.
- `awf.operator-workbench.decision-summary.v1` for reviewer-attributed decision summaries.
- Required source, scope, availability, work queue, evidence, review gate, trace/eval, branch/PR, handoff, health, and
  decision summary fields.
- Self-hosted and credential-free fallback behavior for optional GitHub, self-hosted Langfuse, and repo-local trace
  evidence.
- Validation rules requiring generated artifacts to come from repo commands and source artifacts, not prior chat
  context.

## Validation Evidence

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- Targeted helper check for `operator_workbench_status_schema_data()`: `ok=true`, `missing=[]`.
- `uv run awf repo-hygiene --json`: passed, `checked_files=370`.
- `git diff --check`: passed.
- `uv run awf workflow-fixture-test --json`: passed, `59/59`.
- `uv run awf workflow-state-lint --json`: passed.
- `uv run awf review-gate --json`: passed, `human_required_count=0`.
- `uv run awf verify --profile ticket --json`: passed, including spec lint, Spec Kit lint, BDD lint, review gate,
  repo hygiene, workflow-state lint, and acceptance.

## Reviewer Outcome

Accepted by independent reviewer agent `019e9182-075e-7191-af5d-fbfecf1a999c`.

- Outcome: accepted.
- Findings: none.
- Required follow-up tickets: none.
- Human review required: false.
- Evidence checked: claim, report, schema doc, workbench README, fixture assertion helper, T003 task, targeted helper
  result, workflow fixture result, review gate result, and diff hygiene.
