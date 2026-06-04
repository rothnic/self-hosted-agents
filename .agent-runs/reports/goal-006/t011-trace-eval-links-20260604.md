# Goal 006 T011 Trace And Eval Links Evidence

Status: presenter evidence for independent review.

Ticket: `awf-diw`
Task: `specs/007-operator-workbench-review-ux/tasks.md#T011`
Acceptance: `uv run awf workflow-fixture-test`

## Scope

T011 adds trace and eval deep links for self-hosted Langfuse-backed and repo-local evidence. The operator workbench can
now expose repo-local trace artifacts, repo-local eval artifacts, correlations between evals and traces, and optional
self-hosted Langfuse trace URLs already recorded in trace evidence.

This slice does not implement daily/session handoff summaries, interface selection, local UI implementation,
accessibility checks, scheduled-agent usage docs, or final Goal 006 acceptance. Those remain T012 through T017.

## Evidence Presented

- `uv run awf trace-eval-links`: new CLI command for trace/eval evidence links.
- `.agent-runs/reports/workbench/trace-eval-links-20260604T095246Z.json`: durable trace/eval links artifact.
- `.agent-runs/reports/workbench/operator-status-20260604T095248Z.json`: generated status artifact showing the same
  trace/eval links in `trace_eval` and `availability.self_hosted_langfuse`.
- `tools/agent-workflow/src/agent_workflow/core.py`: adds trace/eval link extraction, Langfuse URL extraction from
  existing trace artifacts, eval-to-trace correlation, operator-status integration, and fixture validation.
- `tools/agent-workflow/src/agent_workflow/cli.py`: wires the `trace-eval-links` command.
- `docs/workbench/trace-eval-links.md`: documents command usage, artifact fields, self-hosted Langfuse boundaries, and
  credential-free fallback behavior.
- `docs/workbench/status-artifact-schema.md`: documents `awf.operator-workbench.trace-eval-links.v1`.
- `docs/workbench/operator-status-report.md` and `docs/workbench/README.md`: route agents to the new trace/eval view
  and update the next implementation step.
- `.agent-runs/claims/awf-diw.json`: active T011 claim.

## Durable Trace/Eval Summary

The live `trace-eval-links` artifact recorded:

- schema: `awf.operator-workbench.trace-eval-links.v1`
- repo-local trace count: 5
- repo-local eval count: 4
- correlated eval-to-trace pairs: 4
- correlation match methods: `trace_evidence`
- self-hosted Langfuse deep links found in existing trace artifacts: 1
- `availability.self_hosted_langfuse.state`: `available`
- `availability.repo_local_evidence.state`: `available`

The self-hosted Langfuse link is sourced from existing repo-local trace evidence:

- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json`
- `http://127.0.0.1:13300/project/self-hosted-agents-pydantic-ai/traces/735c1665d723b965ef77950eeeac36df`

## Validation So Far

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`:
  passed.
- `uv run awf trace-eval-links --json`: passed with 5 traces, 4 evals, 4 correlations, and 1 self-hosted Langfuse
  link.
- `uv run awf trace-eval-links --write --json`: wrote
  `.agent-runs/reports/workbench/trace-eval-links-20260604T095246Z.json`.
- `LANGFUSE_BASE_URL=http://example.invalid LANGFUSE_HOST=http://example.invalid LANGFUSE_PROJECT_ID=ambient-project uv run awf trace-eval-links --json`:
  passed and still returned only the artifact-recorded `127.0.0.1:13300` Langfuse link.
- `uv run awf operator-status --write --json`: wrote `.agent-runs/reports/workbench/operator-status-20260604T095248Z.json`
  with `trace_eval.schema=awf.operator-workbench.trace-eval-links.v1`.
- `uv run awf workflow-fixture-test --json`: passed, 67 total, 67 passed, 0 failed.
- `uv run awf verify --profile ticket --json`: passed for `awf-diw` with no failed checks.
- `uv run awf repo-hygiene --json`: passed, 414 checked files, no errors.
- `uv run awf workflow-state-lint --json`: passed, 130 completed tasks checked and 17 open issues checked.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `git diff --check`: passed.

## Self-Hosted Boundary

The trace/eval command reads repo-local artifacts only. It does not call hosted Logfire, hosted Langfuse, GitHub, cloud
services, or external project tokens. Hosted or self-hosted deep links are optional evidence enrichment when they are
already present in trace artifacts. Deterministic validation remains credential-free and falls back to repo-local trace
and eval evidence.

## Reviewer Request

An independent reviewer should accept or reject whether T011 is complete by checking the files and command evidence
above. The reviewer should verify that repo-local traces and evals are linked, evals are correlated to traces,
self-hosted Langfuse URLs are surfaced from existing artifacts when present, operator status consumes the same data,
deterministic validation remains credential-free, and T012-T017 boundaries are preserved.

## Independent Review Round 1

Reviewer outcome: rejected.

Reviewer agent:

- `019e9209-6a2c-7b63-8f61-485e2d963324` / Singer

Reviewer findings:

- `trace-eval-links` could synthesize Langfuse trace URLs from ambient `LANGFUSE_BASE_URL`, `LANGFUSE_HOST`, and
  `LANGFUSE_PROJECT_ID` instead of only surfacing URLs recorded in trace artifacts.
- Correlation could choose a newer trace with duplicate run or trace ids before honoring the explicit
  `trace_evidence` path.

Fixes applied:

- Removed ambient Langfuse URL and project-id synthesis. The command now reads Langfuse deep links only from
  repo-local trace artifacts.
- Changed correlation to prefer explicit `trace_evidence` paths. Id fallback is used only when no explicit trace
  evidence exists and there is exactly one id match.
- Added `match_method` to correlations and updated trace/eval docs and schema examples.

## Independent Review Round 2

Reviewer outcome: accepted.

Reviewer agent:

- `019e9209-6a2c-7b63-8f61-485e2d963324` / Singer

Reviewer findings: none blocking.

Reviewer evidence checked:

- `tools/agent-workflow/src/agent_workflow/core.py`: `trace_link_item` now reads Langfuse project id and URL only from
  trace artifact metadata.
- `tools/agent-workflow/src/agent_workflow/core.py`: `trace_eval_correlation` now prefers explicit `trace_evidence`
  paths and only uses id fallback when no explicit trace evidence exists and exactly one id match exists.
- Ambient-env stress command returned only the artifact-recorded `http://127.0.0.1:13300/...` URL.
- `.agent-runs/reports/workbench/trace-eval-links-20260604T095246Z.json`: all 4 correlations use
  `match_method=trace_evidence`.
- `.agent-runs/reports/workbench/operator-status-20260604T095248Z.json`: `availability.self_hosted_langfuse` matches
  `trace_eval.availability.self_hosted_langfuse`.
- `uv run awf workflow-fixture-test --json`: passed, 67 total, 67 passed, 0 failed.
- `uv run awf verify --profile ticket --json`: passed.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `git diff --check`: passed.

Required follow-up tickets: none for T011.

Human review required: false. No reserved, missing, or contradictory decision is present; progress should continue to
T012 after closing `awf-diw`.

## Closure

`uv run awf complete-work --issue-id awf-diw --write --json` succeeded. It recorded Beads evidence, closed `awf-diw`,
marked `specs/007-operator-workbench-review-ux/tasks.md#T011` complete, and made T012 / `awf-xwm` the next ready
ticket.

Post-close status artifact:

- `.agent-runs/reports/workbench/operator-status-20260604T095811Z.json`

Next ready ticket:

- `awf-xwm` / T012 concise daily or session handoff summaries.

Post-close validation:

- `uv run awf workflow-fixture-test --json`: passed, 67 total, 67 passed, 0 failed.
- `uv run awf verify --profile ticket --json`: passed.
- `uv run awf repo-hygiene --json`: passed, 417 checked files, no errors.
- `uv run awf workflow-state-lint --json`: passed, 131 completed tasks checked and 16 open issues checked.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `git diff --check`: passed.
