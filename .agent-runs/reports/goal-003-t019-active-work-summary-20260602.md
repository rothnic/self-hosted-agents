# Goal 003 T019 Active Work Summary

## Scope

- Beads issue: `awf-urx`
- Spec task: `specs/003-automated-increment-orchestration/tasks.md#T019`
- Acceptance command: `uv run awf verify --profile increment --json`

T019 adds a compact active-work status surface for operators and agents. It summarizes ready work, active claims, stale
claims, blockers, and the next safe action without adding cleanup or archive behavior, which remains T020 scope.

## Implementation Evidence

- `tools/agent-workflow/src/agent_workflow/core.py` adds compact issue and claim summaries.
- `increment-status` and refreshed increment ledgers now include `active_work_summary`.
- `active_work_summary.summary_schema` is `awf.active-work.compact.v1`.
- The summary includes counts for ready work, active claims, stale claims, and blockers.
- The summary includes `next_action`, `next_unblocked_issue_id`, compact ready entries, compact active claim entries,
  stale-claim handoff context, and blocker dependency context.
- `tests/workflow/features/automated_increment_orchestration.feature` adds the compact active-work status scenario.
- `docs/orchestration/cron-workflow.md` documents `active_work_summary` as the quick operator handoff surface.

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf bdd-lint --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed `43/43`; new fixture
  `active work summary compactly lists ready claims blockers and stale work` passed.
- `uv run awf increment-status --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --json`: returned
  `active_work_summary` with schema `awf.active-work.compact.v1`, active claim `awf-urx`, and ready ids `awf-urx`,
  `awf-rgg`, and `awf-60y`.
- `uv run awf verify --profile ticket --json`: passed for acceptance source `awf-urx` with no failed checks.
- `uv run awf repo-hygiene --json`: passed with `checked_files=234`.
- `uv run awf workflow-state-lint --json`: passed with no errors or warnings.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.

## Reviewer Evidence

Independent reviewer agent `019e87bd-89b0-7d42-bfa9-291678c3ac8f` accepted the T019 diff.

Reviewer outcome: `accepted`

Evidence checked by reviewer:

- T019-only diff in `core.py`, `automated_increment_orchestration.feature`, and `cron-workflow.md`.
- Scope alignment with FR-017 and separation from T020 cleanup behavior.
- Compact counts, next action, next unblocked issue id, ready items, active claims, stale-claim handoff context, and
  blocker dependency context.
- Fixture result `/tmp/awf-t019-fixture.json`: passed and covered ready, active, stale, blocked, and reroute fields.
- Independent `uv run awf verify --profile increment --json`: passed with `failed_checks=[]`.

Required follow-up tickets: none for T019.

## Closure

`uv run awf complete-work --issue-id awf-urx --worker-id codex-goal003-t019 --write --json` succeeded.

- Beads issue `awf-urx` closed.
- Spec task `T019` marked complete in `specs/003-automated-increment-orchestration/tasks.md`.
- Completion comment recorded implementation, validation, and independent reviewer acceptance evidence.
- Claim archived to `.agent-runs/claims/archive-2026-06/awf-urx.json`.
- `uv run awf increment-plan --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --write --json`
  refreshed `.agent-runs/increments/003-automated-increment-orchestration-goal-003.json`.
- Next unblocked Beads item after closure: `awf-rgg` / T020.

Post-close validation:

- `uv run awf workflow-state-lint --json`: passed; `completed_tasks_checked: 91`, `open_issues_checked: 8`.
- `uv run awf review-gate --json`: passed; no blocked files, open questions, spec errors, or human-required gates.
- `uv run awf repo-hygiene --json`: passed; `checked_files: 235`.
- `git diff --check`: passed.
- `uv run awf verify --profile increment --json`: passed all checks.
- `uv run awf workflow-fixture-test --json`: passed `43/43`; new active-work summary fixture passed.
- `uv run awf automation-loop --role health --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --json`:
  passed with `logged_count: 0`.
- `uv run awf ready-work --json`: next ready Beads item is `awf-rgg` / T020.
