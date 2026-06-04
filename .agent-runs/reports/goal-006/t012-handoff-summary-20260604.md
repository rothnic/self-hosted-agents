# Goal 006 T012 Handoff Summary Evidence

Status: presenter evidence for independent review.

Ticket: `awf-xwm`
Task: `specs/007-operator-workbench-review-ux/tasks.md#T012`
Acceptance: `uv run awf workflow-fixture-test`

## Scope

T012 adds concise daily or session handoff summaries for scheduled agents and local sessions. The workbench now produces
a compact, repo-local handoff artifact that reduces context bloat while preserving exact artifact handles for claims,
next work source refs, presenter reports, reviewer reports, traces, evals, branch/PR state, and status regeneration.

This slice does not decide whether the workbench remains CLI/static or becomes a local UI, does not implement a UI, and
does not add accessibility or scheduled-agent usage docs beyond the handoff-summary surface. Those remain T013 through
T016. Final Goal 006 acceptance remains T017.

## Evidence Presented

- `uv run awf handoff-summary`: new CLI command for local-session and scheduled-agent handoff summaries.
- `.agent-runs/reports/workbench/handoff-summary-session-20260604T101040Z.json`: durable session handoff artifact.
- `.agent-runs/reports/workbench/handoff-summary-scheduled-20260604T101041Z.json`: durable scheduled-agent handoff
  artifact.
- `.agent-runs/reports/workbench/operator-status-20260604T101041Z.json`: generated status artifact with embedded
  `handoff_summary`.
- `tools/agent-workflow/src/agent_workflow/core.py`: adds handoff summary generation, exact handles, operator-status
  integration, and fixture validation.
- `tools/agent-workflow/src/agent_workflow/cli.py`: wires the `handoff-summary` command.
- `docs/workbench/handoff-summary.md`: documents command usage, artifact fields, local-session and scheduled-agent
  boundaries, and credential-free behavior.
- `docs/workbench/status-artifact-schema.md`: documents `awf.operator-workbench.handoff-summary.v1`.
- `docs/workbench/operator-status-report.md` and `docs/workbench/README.md`: route agents to the new handoff view and
  update the next implementation step.
- `.agent-runs/claims/awf-xwm.json`: active T012 claim.

## Durable Handoff Summary

The live handoff artifacts recorded:

- schema: `awf.operator-workbench.handoff-summary.v1`
- session audience lines: 8
- scheduled audience lines: 8
- next work: `awf-xwm`
- claim handle: `.agent-runs/claims/awf-xwm.json`
- next work source: `specs/007-operator-workbench-review-ux/tasks.md#T012`
- local session first command: `uv run awf operator-status --json`
- scheduled agent first command: `uv run awf handoff-summary --json`
- self-hosted external service required: false

## Validation So Far

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`:
  passed.
- `uv run awf handoff-summary --json`: passed with 8 copy-ready lines, exact claim/source handles, and no external
  service requirement.
- `uv run awf handoff-summary --audience scheduled --json`: passed with 8 copy-ready lines and scheduled-agent resume
  guidance.
- `uv run awf handoff-summary --write --json`: wrote
  `.agent-runs/reports/workbench/handoff-summary-session-20260604T101040Z.json`.
- `uv run awf handoff-summary --audience scheduled --write --json`: wrote
  `.agent-runs/reports/workbench/handoff-summary-scheduled-20260604T101041Z.json`.
- `uv run awf operator-status --write --json`: wrote `.agent-runs/reports/workbench/operator-status-20260604T101041Z.json`
  with `handoff_summary.schema=awf.operator-workbench.handoff-summary.v1`.
- `uv run awf workflow-fixture-test --json`: passed, 68 total, 68 passed, 0 failed.
- `uv run awf verify --profile ticket --json`: passed for `awf-xwm` with no failed checks.
- `uv run awf repo-hygiene --json`: passed, 421 checked files, no errors.
- `uv run awf workflow-state-lint --json`: passed, 131 completed tasks checked and 16 open issues checked.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `git diff --check`: passed.

## Self-Hosted Boundary

The handoff-summary command reads repo-local operator status, Beads, claims, reports, traces, evals, review-gate state,
and branch/PR fallback state. It does not require hosted Logfire, hosted Langfuse, GitHub, cloud credentials, or
external project tokens. The summary is a compact routing artifact, not a replacement for source-of-truth repo files.

## Reviewer Request

An independent reviewer should accept or reject whether T012 is complete by checking the files and command evidence
above. The reviewer should verify that local-session and scheduled-agent handoffs are concise, exact artifact handles
are preserved, `operator-status` embeds the summary, deterministic validation remains credential-free, and T013-T017
boundaries are preserved.

## Independent Review Outcome

Reviewer outcome: accepted.

Reviewer agent:

- `019e921f-b8f7-71a2-9cd6-2010496f2c37` / Kuhn

Reviewer findings: none blocking.

Reviewer evidence checked:

- `uv run awf handoff-summary --json`: passed with 8 copy-ready lines, `awf-xwm`, claim path, T012 source, reports,
  trace/eval paths, PR URL, and status command.
- `uv run awf handoff-summary --audience scheduled --json`: passed.
- `uv run awf handoff-summary --audience daily --json`: passed.
- `uv run awf operator-status --json`: passed and embedded `handoff_summary`.
- `uv run awf workflow-fixture-test --json`: passed, 68 total, 68 passed, 0 failed.
- `uv run awf verify --profile ticket --json`: passed.
- `uv run awf repo-hygiene --json`: passed.
- `uv run awf workflow-state-lint --json`: passed.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `git diff --check`: passed.
- Scope check: no T013-T016 UI/interface behavior was implemented.

Required follow-up tickets: none for T012.

Human review required: false. No reserved, missing, or contradictory decision is present; progress should continue to
T013 after closing `awf-xwm`.

## Closure

`uv run awf complete-work --issue-id awf-xwm --write --json` succeeded. It recorded Beads evidence, closed `awf-xwm`,
marked `specs/007-operator-workbench-review-ux/tasks.md#T012` complete, and made T013 / `awf-s6n` the next ready
ticket.

Post-close status artifact:

- `.agent-runs/reports/workbench/operator-status-20260604T101742Z.json`

Next ready ticket:

- `awf-s6n` / T013 decide whether the workbench remains CLI/static or becomes a local UI.

Post-close validation:

- `uv run awf workflow-fixture-test --json`: passed, 68 total, 68 passed, 0 failed.
- `uv run awf verify --profile ticket --json`: passed.
- `uv run awf repo-hygiene --json`: passed, 422 checked files, no errors.
- `uv run awf workflow-state-lint --json`: passed, 132 completed tasks checked and 15 open issues checked.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `git diff --check`: passed.
