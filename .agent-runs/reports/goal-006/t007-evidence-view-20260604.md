# Goal 006 T007 Evidence View Evidence

Status: presenter evidence for independent review.

Ticket: `awf-yu8`
Task: `specs/007-operator-workbench-review-ux/tasks.md#T007`
Acceptance: `uv run awf workflow-fixture-test`

## Scope

T007 adds a repo-local evidence view to the consolidated operator status report. The view links presenter reports,
reviewer reports, run and verification artifacts, trace artifacts, eval artifacts, Beads comments, branch context, and a
PR fallback placeholder.

This slice does not implement durable review actions, reviewer decision records, GitHub PR API integration, self-hosted
Langfuse deep links, handoff summaries, or a local UI. Those remain T008 through T016.

## Evidence Presented

- `tools/agent-workflow/src/agent_workflow/core.py`: adds `evidence_view` generation and fixture validation.
- `docs/workbench/evidence-view.md`: documents evidence-view inputs, fields, and operating rules.
- `docs/workbench/status-artifact-schema.md`: adds `evidence_view` to the generated status schema.
- `docs/workbench/operator-status-report.md`: lists the evidence view in the report sections.
- `docs/workbench/README.md`: routes agents to the evidence view doc and advances the next step to T008.
- `.agent-runs/claims/awf-yu8.json`: active T007 claim.
- `.agent-runs/reports/workbench/operator-status-20260604T083502Z.json`: pre-close generated status artifact.
- `.agent-runs/reports/workbench/operator-status-20260604T084119Z.json`: post-close generated status artifact.

## Generated Evidence View Summary

Pre-close `operator-status --write` generated:

- schema: `awf.operator-workbench.evidence-view.v1`
- target ticket: `awf-yu8`
- presenter reports: 26
- reviewer reports: 14
- accepted reports: 8
- verification artifacts: 20
- trace artifacts: 5
- eval artifacts: 4
- Beads issues with comments: 8
- branch: `codex/pydantic-ai-fixture-scaffold`
- PR state: `not_checked`
- PR fallback: repo-local branch and commit; GitHub PR lookup is deferred to T010
- credential-free validation: true
- external service required: false

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed, 388 checked files, no errors.
- `uv run awf workflow-state-lint --json`: passed, 126 completed tasks and 21 open issues checked.
- `uv run awf workflow-fixture-test --json`: passed, 63 total, 63 passed, 0 failed.

Post-close status after `uv run awf complete-work --issue-id awf-yu8 --write --json`:

- `.agent-runs/reports/workbench/operator-status-20260604T084119Z.json` generated.
- T007 completed and next task advanced to T008.
- target ticket advanced to `awf-3c5`.
- accepted report count advanced to 9.
- PR state remains `not_checked` with explicit T010 fallback.

## Self-Hosted Boundary

The evidence view is generated from `.agent-runs/`, Beads comments, git branch, and git commit state. It preserves
deterministic fixture validation without requiring hosted Logfire, hosted Langfuse, GitHub, or any external project
token. Optional hosted/self-hosted links remain future evidence surfaces and are not required by T007.

## Reviewer Request

An independent reviewer should accept or reject whether T007 is complete by checking the files and command evidence
above. The reviewer should verify that the implementation is scoped to the evidence view, keeps validation
credential-free, links run/trace/eval/Beads/branch/PR-fallback evidence, and leaves T008 through T016 for later tickets.

## Independent Reviewer Outcome

Reviewer agent: `019e91c7-852a-7933-b7ae-b2c850417707`
Outcome: accepted.
Findings: none.
Required follow-up tickets: none.
Human review required: false.

Reviewer evidence checked:

- T007 scope is limited to the evidence view; T008-T016 remain open.
- `.agent-runs/claims/awf-yu8.json` links the claim to `tasks.md#T007` and acceptance
  `uv run awf workflow-fixture-test`.
- `evidence_view` generation includes presenter/reviewer reports, run artifacts, trace/eval artifacts, Beads comments,
  branch/commit, PR fallback, and self-hosted flags.
- `operator-status --json` includes the view from repo-local sources.
- Fixture validation permits both claimed T007 and post-completion T008 / `awf-3c5` state.
- Workbench docs, schema, report, and README are aligned.

Reviewer validation rerun:

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf operator-status --json`: evidence view present, target `awf-yu8`, `external_service_required=false`, PR
  state `not_checked` with T010 fallback, and all evidence categories surfaced.
- `uv run awf workflow-fixture-test --json`: passed, 63 total, 63 passed, 0 failed.
