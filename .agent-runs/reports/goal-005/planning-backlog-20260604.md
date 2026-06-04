# Goal 005 Planning And Backlog Evidence

## Scope

Presenter: Codex planning agent.

Goal: `docs/goals/005-self-hosted-deployment-operations-reference.md`.

Objective: initialize the focused spec, task plan, Beads backlog, dependency routing, and increment ledger for the
self-hosted deployment and operations reference.

## Artifacts

- Spec: `specs/006-self-hosted-deployment-operations-reference/spec.md`.
- Plan: `specs/006-self-hosted-deployment-operations-reference/plan.md`.
- Tasks: `specs/006-self-hosted-deployment-operations-reference/tasks.md`.
- Increment ledger: `.agent-runs/increments/006-self-hosted-deployment-operations-reference-goal-005.json`.
- Beads increment epic: `awf-h2u`.
- Acceptance command for each Goal 005 task: `uv run awf workflow-fixture-test`.

## Beads Backlog

| Task | Beads | Summary | Dependency |
| --- | --- | --- | --- |
| T001 | `awf-n19` | Add deployment operations BDD contract | Ready |
| T002 | `awf-gdu` | Define deployment profiles | Blocks on `awf-n19` |
| T003 | `awf-noh` | Document service boundaries | Blocks on `awf-gdu` |
| T004 | `awf-is8` | Add env templates and readiness checks | Blocks on `awf-noh` |
| T005 | `awf-091` | Add or document one-command startup | Blocks on `awf-is8` |
| T006 | `awf-t1m` | Add deployment smoke command or driver | Blocks on `awf-091` |
| T007 | `awf-xei` | Capture deployment smoke evidence | Blocks on `awf-t1m` |
| T008 | `awf-rgf` | Prove deterministic credential-free validation | Blocks on `awf-xei` |
| T009 | `awf-71o` | Add backup, restore, and reset runbooks | Blocks on `awf-rgf` |
| T010 | `awf-hic` | Add health, log, trace, and diagnostics runbooks | Blocks on `awf-rgf` |
| T011 | `awf-2jm` | Add rollback, retention, resource, and cost notes | Blocks on `awf-rgf` |
| T012 | `awf-pt7` | Run clean-path or fresh setup rehearsal | Blocks on T009, T010, T011 |
| T013 | `awf-xjv` | Present final evidence and record reviewer outcome | Blocks on `awf-pt7` |

## Routing Evidence

`uv run awf ready-work --json` reports one ready Goal 005 task: `awf-n19` for
`specs/006-self-hosted-deployment-operations-reference/tasks.md#T001`.

It reports no human-required items and 12 blocked Goal 005 tasks. Raw ready task ids contain only `awf-n19`; older raw
ready epics remain follow-up backlog, not current worker tasks.

`br show awf-h2u --json` lists all 13 Goal 005 tasks as parent-child dependents. `br show awf-n19 --json` shows parent
`awf-h2u`, label `role:worker`, and dependent `awf-gdu`.

## Workaround Recorded

`uv run awf increment-plan --write` attempted to create the increment label
`increment:006-self-hosted-deployment-operations-reference-goal-005`, but Beads rejects labels longer than 50
characters. The durable workaround is:

- Create Beads epic `awf-h2u` with the expected increment external ref.
- Keep short role labels on the epic and worker tickets.
- Use parent-child dependencies plus the increment ledger path as the authoritative Goal 005 grouping.

Future AWF hardening should shorten generated increment labels or skip labels that exceed Beads constraints.

## Validation

- `uv run awf spec-kit-lint --json`: passed with native Spec `006-self-hosted-deployment-operations-reference`.
- `uv run awf spec-lint --json`: passed with no errors.
- `uv run awf workflow-state-lint --json`: passed with 107 completed tasks and 23 open issues checked.
- `uv run awf repo-hygiene --json`: passed with 289 files checked.
- `uv run awf ready-work --json`: passed; ready task ids contain only `awf-n19`, with no human-required items.
- `uv run awf review-gate --json`: passed with no blocked files and no human-required items.
- `git diff --check`: passed.
- `uv run awf workflow-fixture-test --json`: passed 45/45.

## Reviewer Criteria

An independent reviewer agent should accept this planning checkpoint only if:

- Goal 005 scope is represented by the spec, plan, and tasks.
- The task list is dependency-aware and has one ready worker ticket.
- Beads has objective, spec, task, source, and acceptance metadata for all tasks.
- Deterministic validation remains credential-free and no hosted service is required.
- Goal evidence is routed through presenter evidence plus independent reviewer acceptance, not a human-review block.

## Reviewer Outcome

Accepted by independent reviewer agent `019e909e-8033-7d32-9ff1-92910ecc3bda`.

Reviewer verdict: accepted, with no blocking findings and no new follow-up tickets.

Evidence checked by reviewer:

- Goal 005 scope is represented in the goal document, spec, plan, and tasks.
- Self-hosted/no-cloud and credential-free validation requirements are preserved.
- Goal evidence routing uses presenter evidence plus independent reviewer acceptance or rejection.
- Beads routing is coherent with parent epic `awf-h2u`, next ready T001 `awf-n19`, and later tasks dependency-blocked.
- Increment ledger reports one ready task, 12 blocked tasks, and next unblocked issue `awf-n19`.
- Presenter validation evidence is recorded in this report.

Reviewer also reran the key read-only checks, including `workflow-fixture-test --json`, which passed 45/45.
