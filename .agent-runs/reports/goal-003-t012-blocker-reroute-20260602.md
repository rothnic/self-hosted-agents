# Goal 003 T012 Blocker Reroute - 2026-06-02

## Scope

Ticket: `awf-j69` / T012, add blocker rerouting so unrelated ready work can continue.

Claimed by: `codex-goal003-t012`

Acceptance command: `uv run awf verify --profile increment --json`

## Presented Evidence

T012 adds explicit blocker reroute evidence to increment status.

Implementation:

- `tools/agent-workflow/src/agent_workflow/core.py` adds `blocker_reroute_data`.
- `increment-status` now includes a `blocker_reroute` object for the current increment.
- When blocked and ready scoped work exist together, `blocker_reroute.can_continue=true`, `next_unblocked_issue_id`
  points to the next assignable ticket, and blocked items retain blocking dependency context.
- `workflow-fixture-test` includes a deterministic mixed blocked-plus-ready assertion proving unrelated ready work stays
  assignable while blockers stay visible.
- `docs/orchestration/cron-workflow.md` documents the orchestrator and PM/review split for blocker rerouting.

## Reroute Behavior

The scheduler should handle mixed blocked and ready state this way:

- Orchestrator keeps assigning unblocked ready work.
- PM/review triages blocked work and its blocking dependencies.
- Blocked work remains visible in increment status instead of idling unrelated work.

## Acceptance Evidence

Validation captured on 2026-06-02:

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf verify --profile ticket --json`: passed with zero failed checks.
- `uv run awf verify --profile increment --json`: passed with zero failed checks.
- `uv run awf workflow-fixture-test --json`: passed with `35/35` fixture checks before closure and again after
  `complete-work` closed `awf-j69`.
- Ticket profile checks: `spec-lint`, `spec-kit-lint`, `bdd-lint`, `review-gate`, `repo-hygiene`,
  `workflow-state-lint`, and the nested acceptance command all passed.
- Increment profile checks: `bootstrap`, `spec-lint`, `spec-kit-lint`, `bdd-lint`, `bdd-run-fixture`, `review-gate`,
  `repo-hygiene`, `workflow-state-lint`, and `workflow-fixture-test` all passed.
- `increment-status` with explicit Goal 003 scope reported the active T012 claim and a normal no-blocker reroute state.
- A deterministic mixed blocked-plus-ready fixture produced `can_continue=true`, preserved blocking dependency context,
  and routed the orchestrator to keep assigning unblocked work.

## Independent Review

Reviewer: `019e8724-a9ed-7a82-b046-855bac1bae6f`

Outcome: accepted with no findings.

The reviewer accepted T012 evidence on 2026-06-02 after reviewing the T012 claim, FR-009/T012 scope, blocker reroute
implementation, Goal 003 operator guidance, deterministic fixture coverage, and this evidence report. The reviewer
confirmed that blocked work remains visible with dependency context, mixed blocked-plus-ready state reports
`can_continue` with a next unblocked issue, orchestrator/status guidance keeps unrelated ready work moving while
PM/review triages blockers, deterministic workflow fixture coverage exists and passed, and validation evidence is
coherent.
