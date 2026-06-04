# Operator Status Report

Status: added for Goal 006 T004.

`uv run awf operator-status --json` generates the first consolidated operator workbench status report from repo-local
workflow state. It is a CLI/static surface, not a local UI.

Use `uv run awf operator-status --write --json` to persist a JSON artifact under `.agent-runs/reports/workbench/`.

## Source Inputs

The report is generated from:

- `uv run awf context-index --json`
- `uv run awf ready-work --json`
- `uv run awf increment-status --spec-id 007-operator-workbench-review-ux --phase "Goal 006" --json`
- `uv run awf review-gate --json`
- `uv run awf repo-hygiene --json`
- `uv run awf workflow-state-lint --json`
- `.beads/issues.jsonl`
- `.agent-runs/claims/`
- `.agent-runs/reports/`
- `docs/goals/000-self-hosted-agent-system-roadmap.md`

## Included Sections

- `executive_snapshot`: phase, active role, recommendation, next owner, and risks.
- `roadmap`: ordered goal files, accepted Goal 006 evidence, and follow-up epics.
- `goal_dashboard`: ordered child goals, current Goal 006 phase, next ticket, and accepted evidence links.
- `increment_dashboard`: scoped Goal 006 tickets, claims, blockers, active workers, and validation state.
- `work_queue`: Beads-ready work, blocked work, human-required work, active claims, and stale claims.
- `evidence_view`: presenter and reviewer reports, run artifacts, traces, evals, Beads comments, branch, and PR fallback.
- `evidence_map`: presenter reports, reviewer reports, verification artifacts, trace/eval artifacts, Beads comments,
  and PR evidence placeholders.
- `review_gate`: current gate state, findings, human-required count, supported actions, and recent review actions.
- `review_actions`: recent durable review-action artifacts from `.agent-runs/review-actions/`.
- `decision_summaries`: recent reviewer decision records from `.agent-runs/review-decisions/`.
- `trace_eval`: repo-local trace/eval links, trace/eval correlations, optional self-hosted Langfuse deep links, and
  fallback state.
- `branch_pr`: branch, commit, upstream, GitHub PR metadata when available, and repo-local fallback when unavailable.
- `handoff`: exact next role or ticket, files, validation commands, risks, and artifact handles.
- `handoff_summary`: concise local-session and scheduled-agent prompts with exact artifact handles.
- `interface_decision`: selected CLI/static interface decision plus local UI deferral rationale.
- `health`: shallow validation summaries for repo hygiene, workflow-state lint, and review gate.

## Self-Hosted Behavior

The report does not require hosted credentials, GitHub access, or an external project token. Optional GitHub,
self-hosted Langfuse, and DBOS visibility are represented as availability states with repo-local fallbacks. Full
acceptance remains `uv run awf workflow-fixture-test`; `operator-status` intentionally does not run that command while
generating the report.
