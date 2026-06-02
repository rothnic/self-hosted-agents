# Goal 003 T018 Dry-Run Role Transition Fixtures

## Scope

- Beads issue: `awf-j3t`
- Spec task: `specs/003-automated-increment-orchestration/tasks.md#T018`
- Acceptance command: `uv run awf verify --profile increment --json`

T018 adds deterministic fixture evidence that the scheduled role transitions can be represented without mutating active
claims while blocked-state recovery remains visible. This is fixture proof for the Goal 003 automation loop, not a live
scheduler or cleanup surface.

## Implementation Evidence

- `tools/agent-workflow/src/agent_workflow/core.py` adds `dry_run_role_transition_fixture()`.
- The fixture models PM/review, orchestrator, worker, integrator, and health transitions for the Goal 003 increment.
- The orchestrator transition uses `claim_work_data(write=False)` with a deterministic worker branch and worktree path.
- The blocked-state recovery path keeps a blocked ticket and dependency visible while routing unrelated ready work
  forward through `blocker_reroute_data`.
- The integrator transition uses reviewer-facing handoff data and keeps `main_merge_allowed=false`.
- The health transition uses repo-local issue evidence in dry-run mode without writing `.agent-runs/health/` artifacts.
- `tests/workflow/features/automated_increment_orchestration.feature` adds the dry-run role transition and blocked-state
  recovery scenario.
- `docs/orchestration/cron-workflow.md` documents what the dry-run fixture proves and that live scheduling still uses
  Beads, claims, increment ledgers, and review-agent acceptance.

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf bdd-lint --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed `42/42`; new fixture
  `dry-run role transition fixture covers blocked-state recovery` passed with role order
  `pm-review -> orchestrator -> worker -> integrator -> health`, `dry_run_mutation_safe=true`, and
  `blocked_state_recovery=true`.
- `uv run awf verify --profile ticket --json`: passed for acceptance source `awf-j3t` with no failed checks.
- `uv run awf repo-hygiene --json`: passed with `checked_files=232`.
- `uv run awf workflow-state-lint --json`: passed with no errors or warnings.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.

## Reviewer Evidence

Independent reviewer agent `019e87ad-8ae1-7fd2-a3e3-6065176c5441` accepted the T018 diff.

Reviewer outcome: `accepted`

Evidence checked by reviewer:

- T018-only diff in `core.py`, `automated_increment_orchestration.feature`, and `cron-workflow.md`.
- Scope alignment with `specs/003-automated-increment-orchestration/tasks.md#T018`.
- Alignment with FR-012 and Goal 003 fixture/recovery requirements in the spec.
- Independent `uv run awf verify --profile increment --json`: passed with `failed_checks=[]`.
- Presenter fixture artifact `/tmp/awf-t018-fixture.json`: passed `42/42`; new dry-run fixture passed.

Required follow-up tickets: none for T018.

## Closure

`uv run awf complete-work --issue-id awf-j3t --worker-id codex-goal003-t018 --write --json` succeeded.

- Beads issue `awf-j3t` closed.
- Spec task `T018` marked complete in `specs/003-automated-increment-orchestration/tasks.md`.
- Completion comment recorded the implementation, validation, and independent reviewer acceptance evidence.
- Claim archived to `.agent-runs/claims/archive-2026-06/awf-j3t.json`.
- `uv run awf increment-plan --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --write --json`
  refreshed `.agent-runs/increments/003-automated-increment-orchestration-goal-003.json`.
- Next unblocked Beads item after closure: `awf-urx` / T019.

Post-close validation:

- `uv run awf workflow-state-lint --json`: passed; `completed_tasks_checked: 90`, `open_issues_checked: 9`.
- `uv run awf review-gate --json`: passed; no blocked files, open questions, spec errors, or human-required gates.
- `uv run awf repo-hygiene --json`: passed; `checked_files: 233`.
- `git diff --check`: passed.
- `uv run awf verify --profile increment --json`: passed all checks.
- `uv run awf workflow-fixture-test --json`: passed `42/42`; new dry-run fixture passed.
- `uv run awf automation-loop --role health --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --json`:
  passed with `logged_count: 0`.
- `uv run awf ready-work --json`: next ready Beads item is `awf-urx` / T019.
