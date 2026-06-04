# Increment Dashboard

Status: added for Goal 006 T006.

`uv run awf operator-status --json` includes an `increment_dashboard` section for the active Goal 006 increment. The
dashboard is a compact operator view for deciding which ticket is ready, claimed, blocked, stale, or already complete.
It is generated from repo-local workflow state and does not require hosted credentials.

## Source Inputs

- `uv run awf increment-status --spec-id 007-operator-workbench-review-ux --phase "Goal 006" --json`
- `uv run awf ready-work --json`
- `uv run awf review-gate --json`
- `uv run awf repo-hygiene --json`
- `uv run awf workflow-state-lint --json`
- `.agent-runs/increments/007-operator-workbench-review-ux-goal-006.json`
- `.agent-runs/claims/`
- `.beads/issues.jsonl`

## Included Fields

- `schema`: literal `awf.operator-workbench.increment-dashboard.v1`.
- `source`: repo-relative increment ledger path.
- `increment_id`, `spec_id`, `phase`, `review_status`, and `next_action`.
- `counts`: total, completed, open, ready, blocked, claimed, worker, stale, and validation counts.
- `tickets`: ordered child tickets with task id, Beads id, title, status, and derived queue state.
- `ready_tickets` and `blocked_tickets`: active Beads queue slices from the increment status.
- `active_claims` and `active_workers`: current claims plus worker handoff fields.
- `stale_claims`: stale claim records surfaced without hiding the underlying claim artifact.
- `validation_state`: shallow repo-local checks used by the operator status report.
- `handoff`: next unblocked issue, active ticket, and resumable claim path.
- `self_hosted`: credential-free validation and external-service fallback declaration.

## Operating Rules

- Scope the dashboard to the Goal 006 increment; long-horizon ordering remains in `goal_dashboard`.
- Treat Beads, claim files, and the increment ledger as the source of truth.
- Keep closed tickets visible so the operator can see progress through the task sequence.
- Surface blocked and stale work explicitly; do not silently filter it out of the operator view.
- Preserve deterministic validation without requiring GitHub, hosted Logfire, Langfuse, or external project tokens.
