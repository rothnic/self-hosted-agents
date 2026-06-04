# Goal 006 T008 Review Actions Evidence

Status: presenter evidence for independent review.

Ticket: `awf-3c5`
Task: `specs/007-operator-workbench-review-ux/tasks.md#T008`
Acceptance: `uv run awf workflow-fixture-test`

## Scope

T008 adds durable review-gate actions for `approve`, `request-changes`, `defer`, and `ask-question`. The action surface
records reviewer intent as repo-local JSON artifacts and exposes recent actions through `review-gate` and
`operator-status`.

This slice does not implement final reviewer decision records, verdict/finding schemas, follow-up routing, GitHub PR
integration, self-hosted Langfuse deep links, handoff summaries, or a local UI. Those remain T009 through T016.

## Evidence Presented

- `uv run awf review-action`: new CLI command for previewing or writing review actions.
- `.agent-runs/review-actions/defer-goal-006-t008-action-smoke-20260604T085109Z.json`: durable smoke action artifact.
- `.agent-runs/reports/workbench/operator-status-20260604T085121Z.json`: generated status artifact showing the action.
- `tools/agent-workflow/src/agent_workflow/core.py`: adds review-action artifact generation, recent-action loading,
  review-gate/status visibility, and fixture validation.
- `tools/agent-workflow/src/agent_workflow/cli.py`: wires the `review-action` command.
- `docs/workbench/review-actions.md`: documents command usage, artifact fields, and boundaries.
- `docs/workbench/status-artifact-schema.md`: documents `review_actions` and
  `awf.operator-workbench.review-action.v1`.
- `docs/workbench/operator-status-report.md`: lists review action visibility.
- `docs/workbench/README.md`: routes agents to review actions and advances the next step to T009.
- `.agent-runs/claims/awf-3c5.json`: active T008 claim.

## Durable Action Summary

The smoke action was recorded with:

- schema: `awf.operator-workbench.review-action.v1`
- action: `defer`
- target kind: `fixture`
- target id: `goal-006-t008-action-smoke`
- reviewer id: `codex-goal006-t008`
- requires response: true
- human required: false
- decision record deferred to: `Goal 006 T009 reviewer decision records`

Supported actions:

- `approve`
- `request-changes`
- `defer`
- `ask-question`

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`:
  passed.
- `uv run awf review-action --action approve ... --json`: preview passed without writing.
- `uv run awf review-action --action defer ... --write --json`: wrote the durable smoke action.
- `uv run awf review-gate --json`: passed with `human_required_count=0` and surfaced the smoke action.
- `uv run awf operator-status --write --json`: wrote `.agent-runs/reports/workbench/operator-status-20260604T085121Z.json`
  with the smoke action under `review_actions` and `review_gate.actions`.
- `uv run awf repo-hygiene --json`: passed, 393 checked files, no errors.
- `uv run awf workflow-fixture-test --json`: passed, 64 total, 64 passed, 0 failed.
- `git diff --check`: passed.

## Self-Hosted Boundary

The action command writes repo-local artifacts only. It does not require hosted Logfire, hosted Langfuse, GitHub, cloud
credentials, or external project tokens. Written actions are visible to scheduled agents through repo-local status, and
they do not make `review-gate` fail merely because human review might be useful.

## Reviewer Request

An independent reviewer should accept or reject whether T008 is complete by checking the files and command evidence
above. The reviewer should verify that all four actions are supported, written artifacts are durable and repo-local,
`review-gate` remains nonblocking absent a real human-required condition, and T009 remains responsible for full
decision records with verdict, evidence checked, findings, and follow-up routing.

## Independent Review Outcome

Reviewer outcome: accepted.

Reviewer agents:

- `019e91d7-388f-7d22-8c03-9dc39af376a2` / Fermat
- `019e91d5-98ef-75e2-a9c7-eb07481ddc8c` / Hypatia

Reviewer findings: none blocking.

Reviewer evidence checked:

- `uv run awf workflow-fixture-test --json`: passed, 64 total, 64 passed, 0 failed.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `uv run awf operator-status --json`: passed and surfaced the review action plus supported actions.
- `uv run awf review-action ... --json`: all four action previews passed without writing.
- `git diff --check`: passed.

Required follow-up tickets: none for T008.

Human review required: false. No reserved, missing, or contradictory decision is present; progress should continue to
T009 / `awf-09s` for final reviewer decision records.

## Closure

`uv run awf complete-work --issue-id awf-3c5 --write --json` succeeded. It recorded Beads evidence, closed `awf-3c5`,
marked `specs/007-operator-workbench-review-ux/tasks.md#T008` complete, and passed workflow-state lint.

Post-close status artifact:

- `.agent-runs/reports/workbench/operator-status-20260604T085736Z.json`

Next ready ticket:

- `awf-09s` / T009 reviewer decision records.

Post-close validation:

- `uv run awf workflow-fixture-test --json`: passed, 64 total, 64 passed, 0 failed.
- The fixture assertions now accept the valid post-close T009 handoff state for Goal 006 dashboard and evidence-view
  routing.
