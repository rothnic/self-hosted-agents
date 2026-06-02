# Goal 003 T015 Integrator Worker Branch Handoff

## Scope

- Beads issue: `awf-l2j`
- Spec task: `specs/003-automated-increment-orchestration/tasks.md#T015`
- Acceptance: `uv run awf verify --profile increment --json`

## Presenter Evidence

Implemented integrator handoff data that lets the integrator verify completed worker branches without merging to
`main`.

Key behavior:

- `automation-loop --role integrator` now returns an `integrator_handoff` block.
- Worker branch review entries resolve local refs or `origin/<worker_branch>` refs before generating commands.
- Missing local worktrees produce a detached `git worktree add` verification command instead of a dead `cd`.
- Feature-branch integration commands are limited to the active feature branch and resolved worker refs.
- The handoff explicitly reports `main_merge_allowed=false` and `draft_pr_boundary=true`.
- Reviewer evidence is routed through `uv run awf verify --profile increment --write --json`.

Documentation updates:

- `docs/orchestration/codex-automation-prompts.md`
- `docs/orchestration/cron-workflow.md`

Fixture coverage:

- `workflow_fixture_test_result` covers a remote-only completed worker branch and a missing local worktree.
- The fixture asserts no generated command targets `main`.
- `tests/workflow/features/automated_increment_orchestration.feature` now states the integrator verifies worker branches
  without merging to `main`.

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py` passed.
- `uv run awf install-hooks --json` passed.
- `git diff --check` passed.
- `uv run awf verify --profile ticket --json` passed.
- `uv run awf workflow-fixture-test --json` passed `38/38`.
- Focused integrator loop passed:
  - `main_merge_allowed=false`
  - `draft_pr_boundary=true`
  - `worker_branch_count=7`
  - `ready_to_verify_count=0`
  - `pending_worker_count=1`
  - next action: wait for active workers to finish before integrating their branches

## Independent Review

Reviewer agent `019e8761-c818-72a0-be89-bffa536e23d5` initially found three issues:

- Undefined `branch_reviews` state was accidentally inserted into `install_hooks_data`.
- Remote-only worker branches were detected but commands still used the local branch name.
- Verification commands could `cd` into missing worktree paths.

Fixes applied:

- Removed the stray `install_hooks_data` insertion.
- Added resolved ref handling and exposed `resolved_ref` in worker branch review entries.
- Added worktree existence checks and detached worktree setup commands for missing paths.
- Strengthened fixture coverage around remote-only refs and missing worktrees.

The same reviewer re-reviewed the corrected diff and accepted the evidence with no remaining findings.

## Closure Evidence

`uv run awf complete-work --issue-id awf-l2j --worker-id codex-goal003-t015 --write --json` passed.

Workflow close results:

- Beads issue `awf-l2j` closed.
- Task `T015` marked complete in `specs/003-automated-increment-orchestration/tasks.md`.
- Beads evidence comment `85` recorded by `codex-goal003-t015`.
- `workflow-state-lint` passed during completion.

Post-close increment refresh:

- `uv run awf increment-plan --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --write --json`
  passed.
- Active claims: none.
- Ready count: `6`.
- Next unblocked issue: `awf-svc` / T016.

The completed claim was archived to `.agent-runs/claims/archive-2026-06/awf-l2j.json`.

## Post-Close Validation

- `uv run awf workflow-state-lint --json` passed.
- `uv run awf review-gate --json` passed with no human-required items.
- `uv run awf repo-hygiene --json` passed.
- `git diff --check` passed.
- `uv run awf ready-work --json` reported `awf-svc` / T016 as the next ready item.
- `uv run awf verify --profile increment --json` passed with `9` checks and no failed checks.
- `uv run awf automation-loop --role integrator --spec-id 003-automated-increment-orchestration --phase 'Goal 003'
  --json` passed with `main_merge_allowed=false`, `draft_pr_boundary=true`, no pending workers, and no ready worker
  branches requiring verification.
- `uv run awf workflow-fixture-test --json` passed `38/38`, including
  `integrator handoff verifies worker branches without touching main`.
