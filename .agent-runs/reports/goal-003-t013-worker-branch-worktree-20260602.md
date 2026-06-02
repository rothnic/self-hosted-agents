# Goal 003 T013 Worker Branch And Worktree Guidance - 2026-06-02

## Scope

Ticket: `awf-869` / T013, add deterministic worker branch naming and worktree setup guidance.

Claimed by: `codex-goal003-t013`

Acceptance command: `uv run awf verify --profile increment --json`

## Presented Evidence

T013 adds deterministic worker assignment guidance derived from Beads issue metadata.

Implementation:

- `tools/agent-workflow/src/agent_workflow/core.py` adds deterministic worker assignment helpers.
- Claim creation now persists `worker_branch`, `worktree_path`, and `worktree_setup` fields.
- Active claim loading backfills those fields for older claim files so status remains resumable.
- `increment-status` now reports `active_worktrees` alongside `active_worker_branches`.
- Stale-claim handoff guidance now names the worktree path as well as the branch.
- Worker-loop dry-run and write paths expose the same assignment shape.
- `workflow-fixture-test` includes deterministic coverage for branch/worktree derivation and claim payload shape.
- `docs/orchestration/cron-workflow.md` and `docs/orchestration/codex-automation-prompts.md` document that workers
  must use claim fields instead of hidden branch/worktree conventions.

## Deterministic Assignment Shape

For a Beads issue, the worker assignment shape is:

- `worker_branch`: `codex/<issue-id>-<title-slug>`
- `worktree_path`: `../self-hosted-agents-worktrees/<issue-id>-<title-slug>`
- `worktree_setup.add_worktree`: `git worktree add -b <worker_branch> <worktree_path> <feature_branch>`
- `worktree_setup.resume`: command for another agent to inspect the existing worktree

The active T013 claim records:

- `worker_branch`: `codex/awf-869-add-deterministic-worker-branch-naming-a`
- `worktree_path`: `../self-hosted-agents-worktrees/awf-869-add-deterministic-worker-branch-naming-a`
- `feature_branch`: `codex/003-automated-increment-orchestration-goal-003`

## Acceptance Evidence

Validation captured on 2026-06-02:

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf workflow-fixture-test --json`: passed with `36/36` fixture checks.
- `uv run awf verify --profile ticket --json`: passed with zero failed checks.
- Nested acceptance command `uv run awf verify --profile increment --json`: passed with zero failed checks.
- Standalone `uv run awf verify --profile increment --json`: passed with zero failed checks.
- `uv run awf increment-status --spec-id 003-automated-increment-orchestration --phase "Goal 003" --json` reports
  the active T013 claim with deterministic `worker_branch`, `worktree_path`, and `active_worktrees`.
- `uv run awf complete-work --issue-id awf-869 --worker-id codex-goal003-t013 --write --json`: passed, closed
  `awf-869`, marked T013 complete, and reran workflow-state lint with no errors.
- Post-close increment refresh reports no active claims and `awf-6wg` / T014 as the next unblocked ticket.
- Post-close `uv run awf verify --profile increment --json`: passed with zero failed checks.
- Post-close `uv run awf workflow-fixture-test --json`: passed with `36/36` fixture checks.

## Independent Review

Reviewer: `019e8740-051a-76e2-96a9-de71503493e2`

Outcome: accepted with no findings.

The reviewer accepted T013 evidence on 2026-06-02 after reviewing FR-014, the T013 task scope, deterministic assignment
helpers, claim persistence, active claim/status exposure, stale-claim resume context, worker/orchestrator claim paths,
fixture coverage, docs guidance, the live T013 claim file, and this evidence report. The reviewer confirmed that the
presented validation evidence is coherent with the current scoped artifacts and required no follow-up tickets.
