# Goal 003 T020 Cleanup Work Evidence

Date: 2026-06-02

Ticket: `awf-rgg` / T020, add cleanup commands for obsolete active claims and old worktree pointers.

## Summary

T020 adds `uv run awf cleanup-work` as a dry-run-first cleanup surface for scheduled PM/review or health loops. The
command preserves historical claim evidence by archiving only obsolete active claim files and pruning stale Git worktree
metadata separately.

## Changes

- `tools/agent-workflow/src/agent_workflow/cli.py` exposes `cleanup-work`.
- `tools/agent-workflow/src/agent_workflow/core.py` adds cleanup helpers for obsolete claim detection, monthly archive
  paths, archive collision handling, worktree prune output parsing, and write-mode cleanup.
- `workflow-fixture-test` includes deterministic cleanup coverage for open, closed, and missing Beads issue states.
- `tests/workflow/features/automated_increment_orchestration.feature` adds the cleanup scenario.
- `docs/orchestration/cron-workflow.md` documents cleanup preview and write behavior.
- `repo-hygiene` file traversal now prunes ignored directories before descent so fixture validation stays bounded.

## Behavior

`uv run awf cleanup-work --json` previews:

- active claim files whose Beads issue is closed;
- active claim files whose Beads issue is missing;
- stale Git worktree metadata from `git worktree prune --dry-run --verbose`.

`uv run awf cleanup-work --write --json`:

- moves obsolete claim files under `.agent-runs/claims/archive-YYYY-MM/`;
- preserves open active and stale claims for resume, reassign, or explicit archive handling;
- runs `git worktree prune --verbose` for stale Git worktree metadata;
- does not delete historical claim evidence.

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`
  passed.
- `uv run awf cleanup-work --help` shows the new command.
- `uv run awf cleanup-work --json` passed and found no obsolete live claims or stale worktree pointers.
- `uv run awf cleanup-work --write --json` passed as a no-op against the current repo state with zero archive
  candidates, zero archived claims, and zero pruned worktree pointers.
- `git diff --check` passed.
- `uv run awf bdd-lint --json` passed.
- `uv run awf repo-hygiene --json` passed with `checked_files=236`.
- `uv run awf workflow-fixture-test --json` passed `44/44`; cleanup fixture
  `cleanup work preserves history while removing obsolete active pointers` passed.
- `uv run awf verify --profile ticket --json` passed with no failed checks for active claim `awf-rgg`.
- `uv run awf verify --profile increment --json` passed all `9` checks with no failed checks.
- `uv run awf workflow-state-lint --json` passed with `completed_tasks_checked=91` and `open_issues_checked=8`.
- `uv run awf review-gate --json` passed with `human_required_count=0`.
- `uv run awf complete-work --issue-id awf-rgg --worker-id codex-goal003-t020 --write --json` passed, closed
  `awf-rgg`, marked T020 complete, and reran workflow-state lint with `completed_tasks_checked=92` and
  `open_issues_checked=7`.
- Post-closure `uv run awf cleanup-work --write --json` archived `.agent-runs/claims/awf-rgg.json` to
  `.agent-runs/claims/archive-2026-06/awf-rgg.json` because the linked Beads issue was closed.
- Post-cleanup `uv run awf increment-plan --spec-id 003-automated-increment-orchestration --phase "Goal 003" --write
  --json` refreshed `.agent-runs/increments/003-automated-increment-orchestration-goal-003.json` with zero active
  claims and next unblocked `awf-60y` / T021.

## Acceptance

T020 satisfies FR-018 for this increment: cleanup behavior preserves historical evidence while removing obsolete active
claims and old worktree pointers that could misroute future scheduled workers.

Independent reviewer agent `019e87cf-a5e2-7490-9544-a1b41b364dad` accepted this evidence on 2026-06-02 with no
findings and no required follow-up tickets. The reviewer independently checked the cleanup command, claim archival
rules, worktree prune separation, fixture coverage, repo-hygiene traversal fix, evidence report, `git diff --check`,
`uv run awf workflow-fixture-test --json`, `uv run awf verify --profile ticket --json`, and
`uv run awf verify --profile increment --json`.
