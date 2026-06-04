# Goal 006 T010 Branch And PR Status Evidence

Status: presenter evidence for independent review.

Ticket: `awf-1cx`
Task: `specs/007-operator-workbench-review-ux/tasks.md#T010`
Acceptance: `uv run awf workflow-fixture-test`

## Scope

T010 adds branch and PR status integration with repo-local fallback when GitHub access is unavailable. The status surface
uses `gh pr view` when available and still reports trusted branch, commit, upstream, ahead/behind, and working tree
state when GitHub is missing, unauthenticated, offline, or skipped.

This slice does not implement self-hosted Langfuse trace/eval deep links, session handoff summaries, interface
selection, local UI implementation, accessibility checks, scheduled-agent usage docs, or final Goal 006 acceptance.
Those remain T011 through T017.

## Evidence Presented

- `uv run awf branch-pr-status`: new CLI command for branch and PR status.
- `.agent-runs/reports/workbench/branch-pr-status-20260604T092651Z.json`: durable branch/PR status artifact.
- `.agent-runs/reports/workbench/operator-status-20260604T092651Z.json`: generated status artifact showing branch/PR
  integration in `branch_pr`, `availability.github`, and `evidence_view.branch_pr`.
- `tools/agent-workflow/src/agent_workflow/core.py`: adds branch/PR status generation, GitHub lookup, fallback
  behavior, status/evidence integration, and fixture validation.
- `tools/agent-workflow/src/agent_workflow/cli.py`: wires the `branch-pr-status` command.
- `docs/workbench/branch-pr-status.md`: documents command usage, artifact fields, GitHub availability, and boundaries.
- `docs/workbench/status-artifact-schema.md`: documents `awf.operator-workbench.branch-pr.v1`.
- `docs/workbench/operator-status-report.md`, `docs/workbench/evidence-view.md`, and `docs/workbench/README.md`: route
  agents to branch/PR status and update the next implementation step.
- `.agent-runs/claims/awf-1cx.json`: active T010 claim.

## Durable Branch/PR Summary

The live branch/PR status recorded:

- schema: `awf.operator-workbench.branch-pr.v1`
- branch: `codex/pydantic-ai-fixture-scaffold`
- commit: `5f8ebf5`
- state: `available`
- PR URL: `https://github.com/rothnic/self-hosted-agents/pull/12`
- PR number: `12`
- draft: true
- GitHub state: `available`

Fallback proof:

- `uv run awf branch-pr-status --skip-github --json` passed and returned `state=repo-local-fallback`.
- The fallback includes branch, commit, remote, upstream, ahead/behind, and working tree state without requiring GitHub.

## Validation So Far

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`:
  passed.
- `uv run awf branch-pr-status --skip-github --json`: passed with `state=repo-local-fallback`.
- `uv run awf branch-pr-status --json`: passed with PR #12 metadata available.
- `uv run awf branch-pr-status --write --json`: wrote
  `.agent-runs/reports/workbench/branch-pr-status-20260604T092651Z.json`.
- `uv run awf operator-status --write --json`: wrote `.agent-runs/reports/workbench/operator-status-20260604T092651Z.json`
  with PR #12 visible.
- `uv run awf workflow-fixture-test --json`: passed, 66 total, 66 passed, 0 failed.
- `uv run awf verify --profile ticket --json`: passed for `awf-1cx` with no failed checks.
- `uv run awf repo-hygiene --json`: passed, 408 checked files, no errors.
- `uv run awf workflow-state-lint --json`: passed, 129 completed tasks checked and 18 open issues checked.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `git diff --check`: passed.

## Self-Hosted Boundary

The branch/PR command is useful with GitHub available but does not require GitHub for deterministic validation.
`--skip-github` provides credential-free fallback proof. The command does not require hosted Logfire, hosted Langfuse,
cloud credentials, or external project tokens.

## Reviewer Request

An independent reviewer should accept or reject whether T010 is complete by checking the files and command evidence
above. The reviewer should verify that GitHub PR status is integrated when available, repo-local fallback works when
GitHub is skipped or unavailable, status/evidence surfaces show the branch/PR state, and T011-T017 boundaries are
preserved.

## Independent Review Outcome

Reviewer outcome: accepted.

Reviewer agent:

- `019e91f7-48ef-7db2-b490-e324082e0cc9` / Chandrasekhar

Reviewer findings: none blocking.

Reviewer evidence checked:

- `uv run awf branch-pr-status --skip-github --json`: passed with `state=repo-local-fallback`,
  `github.checked=false`, and `external_service_required=false`.
- `uv run awf branch-pr-status --json`: passed with PR #12 metadata available.
- `uv run awf operator-status --json`: passed and surfaced `availability.github`, `branch_pr`, and
  `evidence_view.branch_pr`.
- `uv run awf workflow-fixture-test --json`: passed, 66 total, 66 passed, 0 failed.
- `uv run awf repo-hygiene --json`: passed.
- `uv run awf workflow-state-lint --json`: passed.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`:
  passed.
- `git diff --check`: passed.

Required follow-up tickets: none for T010.

Human review required: false. No reserved, missing, or contradictory decision is present; progress should continue to
T011 / `awf-diw` for trace and eval deep links.

## Closure

`uv run awf complete-work --issue-id awf-1cx --write --json` succeeded. It recorded Beads evidence, closed `awf-1cx`,
marked `specs/007-operator-workbench-review-ux/tasks.md#T010` complete, and passed workflow-state lint.

Post-close status artifact:

- `.agent-runs/reports/workbench/operator-status-20260604T093355Z.json`

Next ready ticket:

- `awf-diw` / T011 trace and eval deep links.

Post-close validation:

- `uv run awf workflow-fixture-test --json`: passed, 66 total, 66 passed, 0 failed.
- The fixture assertions now accept the valid post-close T011 handoff state for Goal 006 dashboard and evidence-view
  routing.
