# Goal Dashboard

Status: added for Goal 006 T005.

The goal dashboard is generated inside `uv run awf operator-status --json` as the `goal_dashboard` section. It gives the
operator a long-horizon view of the roadmap without requiring them to open every goal file or report.

Use `uv run awf operator-status --write --json` to persist the dashboard with the full workbench status artifact under
`.agent-runs/reports/workbench/`.

## Source Inputs

The dashboard is generated from:

- `docs/goals/000-self-hosted-agent-system-roadmap.md`
- `docs/goals/001-*.md` through `docs/goals/006-*.md`
- `specs/007-operator-workbench-review-ux/tasks.md`
- `uv run awf ready-work --json`
- `.beads/issues.jsonl`
- `.agent-runs/claims/`
- `.agent-runs/reports/goal-001*`
- `.agent-runs/reports/goal-002*`
- `.agent-runs/reports/goal-003*`
- `.agent-runs/reports/goal-004*`
- `.agent-runs/reports/goal-005/`
- `.agent-runs/reports/goal-006/`

## Included Fields

- `schema`: literal `awf.operator-workbench.goal-dashboard.v1`.
- `source`: the parent roadmap goal path.
- `review_model`: the required presenter plus independent reviewer evidence policy.
- `current_goal_id`: the active ordered child goal id.
- `current_phase`: current Goal 006 phase, completed/open task counts, next task, and phase task ids.
- `next_ticket`: the active claimed or ready Beads ticket.
- `goals`: ordered child goals with title, path, state, phase, accepted evidence, and next ticket for the active goal.
- `accepted_evidence_links`: flattened accepted evidence links with reviewer ids where the report records them.
- `follow_up_epics`: open follow-up epics that are intentionally not current blockers.
- `counts`: ordered goal, accepted goal, active goal, accepted evidence, and follow-up epic counts.

## Operating Rules

- The dashboard is read-only and generated from repo state.
- Goals 001 through 005 are shown as accepted only when their durable acceptance report paths are present.
- Goal 006 is shown as active until T017 presents final evidence and an independent reviewer accepts it.
- Accepted evidence links are repo-relative paths, not hidden chat references.
- Missing optional hosted services do not block the dashboard; service availability remains represented by the parent
  status artifact.
