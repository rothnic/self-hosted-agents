# Goal 006 Planning And Backlog Evidence

## Scope

Presenter: Codex planning agent.

Goal: `docs/goals/006-operator-workbench-review-ux.md`.

Objective: initialize the focused spec, task plan, Beads backlog, dependency routing, and increment ledger for the
operator workbench and review UX.

## Artifacts

- Spec: `specs/007-operator-workbench-review-ux/spec.md`.
- Plan: `specs/007-operator-workbench-review-ux/plan.md`.
- Tasks: `specs/007-operator-workbench-review-ux/tasks.md`.
- Increment ledger: `.agent-runs/increments/007-operator-workbench-review-ux-goal-006.json`.
- Beads increment epic: `awf-yug`.
- Acceptance command for each Goal 006 task: `uv run awf workflow-fixture-test`.

## Beads Backlog

| Task | Beads | Summary | Dependency |
| --- | --- | --- | --- |
| T001 | `awf-x12` | Research minimum operator views | Ready |
| T002 | `awf-288` | Add operator workbench BDD contract | Blocks on `awf-x12` |
| T003 | `awf-vht` | Define generated artifact schema | Blocks on `awf-288` |
| T004 | `awf-isu` | Add consolidated operator status report | Blocks on `awf-vht` |
| T005 | `awf-sdh` | Add long-horizon goal dashboard | Blocks on `awf-isu` |
| T006 | `awf-vty` | Add increment dashboard | Blocks on `awf-sdh` |
| T007 | `awf-yu8` | Add evidence view | Blocks on `awf-vty` |
| T008 | `awf-3c5` | Add durable review-gate actions | Blocks on `awf-yu8` |
| T009 | `awf-09s` | Add reviewer decision records | Blocks on `awf-3c5` |
| T010 | `awf-1cx` | Add branch and PR status integration | Blocks on `awf-09s` |
| T011 | `awf-diw` | Add trace and eval deep links | Blocks on `awf-1cx` |
| T012 | `awf-xwm` | Add concise handoff summaries | Blocks on `awf-diw` |
| T013 | `awf-s6n` | Decide CLI/static versus local UI | Blocks on `awf-xwm` |
| T014 | `awf-1f9` | Implement selected interface | Blocks on `awf-s6n` |
| T015 | `awf-jr7` | Add accessibility or CLI/static justification checks | Blocks on `awf-1f9` |
| T016 | `awf-svr` | Document scheduled-agent use of workbench artifacts | Blocks on `awf-jr7` |
| T017 | `awf-mtv` | Present final evidence and record reviewer outcome | Blocks on `awf-svr` |

## Routing Evidence

`uv run awf ready-work --json` reports one ready Goal 006 task: `awf-x12` for
`specs/007-operator-workbench-review-ux/tasks.md#T001`.

It reports no human-required items and 16 blocked Goal 006 tasks. Raw ready epics from earlier goals remain follow-up
backlog and are not current Goal 006 worker tasks.

`uv run awf increment-plan --increment-id 007-operator-workbench-review-ux-goal-006 --spec-id
007-operator-workbench-review-ux --phase "Goal 006" --write --json` wrote the increment ledger, found Beads epic
`awf-yug`, and reported `ready_count=1`, `blocked=16`, `review_status=executing`, and next unblocked issue `awf-x12`.

## Workaround Recorded

The known Beads long-label risk from Goal 005 still applies. Instead of relying on a long generated increment label,
this checkpoint uses:

- Beads epic `awf-yug` with external ref `.agent-runs/increments/007-operator-workbench-review-ux-goal-006.json`.
- Short labels on the epic and worker tickets.
- Parent-child dependencies plus the increment ledger path as the authoritative Goal 006 grouping.

## Validation

- `uv run awf spec-kit-lint --json`: passed with native Spec `007-operator-workbench-review-ux`.
- `uv run awf spec-lint --json`: passed with no errors.
- `uv run awf workflow-state-lint --json`: passed with 120 completed tasks and 27 open issues checked.
- `uv run awf repo-hygiene --json`: passed with 361 files checked.
- `uv run awf ready-work --json`: passed; scoped ready Goal 006 work is `awf-x12` / T001, with no human-required
  blockers.
- `uv run awf review-gate --json`: passed with no blocked files and no human-required items.
- `uv run awf workflow-fixture-test --json`: passed 56/56.
- `git diff --check`: passed.

## Reviewer Criteria

An independent reviewer agent should accept this planning checkpoint only if:

- Goal 006 scope is represented by the spec, plan, and tasks.
- The task list is dependency-aware and has one ready worker ticket.
- Beads has objective, spec, task, source, and acceptance metadata for all tasks.
- The workbench remains self-hosted, repo-backed, and credential-free for deterministic validation.
- Goal evidence is routed through presenter evidence plus independent reviewer acceptance or rejection, not a
  human-review block.

## Reviewer Outcome

Accepted by independent reviewer agent `019e915f-292a-7322-8ab4-6f5cdfd8bb7e`.

Reviewer record id: `codex-independent-reviewer-20260604`.

Reviewer verdict: accepted, with no blocking findings and no new follow-up tickets.

Evidence checked by reviewer:

- Goal 006 goal, spec, plan, tasks, presenter report, increment ledger, and Beads rows for `awf-yug` plus T001-T017.
- `uv run awf ready-work --json`: one scoped ready worker ticket, T001 / `awf-x12`; no human-required items.
- `uv run awf increment-status --increment-id 007-operator-workbench-review-ux-goal-006 --spec-id
  007-operator-workbench-review-ux --phase "Goal 006" --json`: `ready_count=1`, `blocked=16`, and
  `next_unblocked_issue_id=awf-x12`.
- `uv run awf review-gate --json`: no blocked files, open questions, spec errors, or human-required items.
- Beads task metadata includes objective, spec, task, source, acceptance, external refs, and parent-child routing for
  all listed task ids.

Human review required for progress: no.
