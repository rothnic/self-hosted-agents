# Goal 006 T006 Increment Dashboard Evidence

Status: presenter evidence for independent review.

Ticket: `awf-vty`
Task: `specs/007-operator-workbench-review-ux/tasks.md#T006`
Acceptance: `uv run awf workflow-fixture-test`

## Scope

T006 adds a repo-local increment dashboard to the consolidated operator status report. The dashboard summarizes the
Goal 006 child ticket sequence, ready and blocked tickets, active claims, active workers, stale claims, validation
state, and a resumable handoff.

This slice does not add a local UI, hosted credentials, GitHub integration, Langfuse integration, trace/eval deep links,
or review-gate actions. Those remain later Goal 006 tickets.

## Evidence Presented

- `tools/agent-workflow/src/agent_workflow/core.py`: adds `increment_dashboard` generation and fixture validation.
- `docs/workbench/increment-dashboard.md`: documents source inputs, fields, and operating rules.
- `docs/workbench/status-artifact-schema.md`: adds `increment_dashboard` to the status schema.
- `docs/workbench/operator-status-report.md`: lists `increment_dashboard` in the generated report sections.
- `docs/workbench/README.md`: routes agents to the increment dashboard doc and advances the next step to T007.
- `.agent-runs/claims/awf-vty.json`: active T006 claim.
- `.agent-runs/reports/workbench/operator-status-20260604T082055Z.json`: pre-close generated status artifact.
- `.agent-runs/reports/workbench/operator-status-20260604T082602Z.json`: post-close generated status artifact.

## Generated Dashboard Summary

Pre-close `operator-status --write` generated:

- schema: `awf.operator-workbench.increment-dashboard.v1`
- increment id: `007-operator-workbench-review-ux-goal-006`
- total tickets: 17
- completed tickets: 5
- ready tickets: 1
- active claims: 1
- active workers: 1
- stale claims: 0
- active ticket: `awf-vty`
- credential-free validation: true
- external service required: false

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed, 384 checked files, no errors.
- `uv run awf verify --profile ticket --json`: passed, including `uv run awf workflow-fixture-test`.
- `uv run awf workflow-fixture-test --json`: passed, 62 total, 62 passed, 0 failed.

Post-close status after `uv run awf complete-work --issue-id awf-vty --write --json`:

- `.agent-runs/reports/workbench/operator-status-20260604T082602Z.json` generated.
- T006 completed tickets count advanced to 6.
- next task advanced to T007.
- next unblocked issue advanced to `awf-yu8`.
- active claims and active workers are 0.
- stale claims remain 0.

## Self-Hosted Boundary

The dashboard is generated from Beads, claim files, the increment ledger, and repo-local workflow checks. It preserves
deterministic fixture validation without requiring hosted Logfire, hosted Langfuse, GitHub, or any external project
token. Optional hosted or self-hosted observability links remain future evidence surfaces and are not required by T006.

## Reviewer Request

An independent reviewer should accept or reject whether T006 is complete by checking the files and command evidence
above. The reviewer should verify that the implementation is scoped to T006, keeps validation credential-free, and does
not silently hide blocked or stale work.

## Independent Reviewer Outcome

Reviewer agent: `019e91ba-a055-7cf2-bea6-446c04d12927`
Outcome: accepted.
Findings: none.
Required follow-up tickets: none.
Human review required: false.

Reviewer evidence checked:

- T006 remains scoped to the increment dashboard; T007-T017 remain open.
- `increment_dashboard` covers ticket states, ready and blocked queues, active claims and workers, stale claims,
  validation, handoff, and self-hosted flags.
- `operator-status --json` includes the dashboard from repo-local sources.
- Fixture validation accepts both active T006 claim state and post-completion next-work state.
- Workbench docs, schema, report, and README are aligned.
- The presenter evidence preserves the self-hosted boundary and excludes hosted Logfire, hosted Langfuse, GitHub, and
  external token requirements.

Reviewer validation rerun:

- `uv run awf operator-status --json`: dashboard present, `external_service_required=false`, active ticket `awf-vty`,
  stale claims `0`, blocked and ready queues surfaced.
- `uv run awf workflow-fixture-test --json`: passed, 62 total, 62 passed, 0 failed.
