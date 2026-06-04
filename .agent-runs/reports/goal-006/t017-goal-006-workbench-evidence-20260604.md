# Goal 006 T017 Workbench Evidence

Presented by: Codex implementer
Ticket: awf-mtv
Spec task: specs/007-operator-workbench-review-ux/tasks.md#T017
Objective: agentic-development-foundation
Acceptance command: uv run awf workflow-fixture-test

## Scope

T017 presents final Goal 006 evidence for the operator workbench and requests independent reviewer acceptance or
rejection. This report does not rely on a human-review pause; the evidence model is presenter evidence plus independent
reviewer acceptance or rejection.

## Completion Claim

Goal 006 is ready for independent reviewer acceptance.

The workbench now gives operators a repo-backed way to inspect what is happening, what is blocked, what decision is
needed, and which exact source artifacts support the decision. It remains CLI/static and self-hosted for Goal 006, with
repo-local fallback evidence for traces, evals, branch/PR status, reviewer decisions, and scheduled-agent handoffs.

## Evidence Presented

- `specs/007-operator-workbench-review-ux/tasks.md` shows T001 through T016 complete and T017 as the final open
  acceptance task.
- `uv run awf increment-status --spec-id 007-operator-workbench-review-ux --phase 'Goal 006' --json` returned
  `ok=true`, one active claim for `awf-mtv`, zero blockers, and one ready item matching T017.
- `uv run awf operator-status --json` returned `ok=true`, summary `continue claimed ticket awf-mtv`, Goal 006 state
  `active`, next ticket `awf-mtv`, 16 accepted Goal 006 evidence reports, 5 accepted ordered child goals, and 9
  follow-up epics.
- `uv run awf workbench-interface --json` returned `ok=true`, selected interface `cli-static`, implementation status
  `implemented-for-goal-006-t014`, next ticket `awf-mtv`, 6 panels, `human_required=false`, and
  `external_service_required=false`.
- `uv run awf scheduled-agent-workbench --json` returned `ok=true`, schema
  `awf.operator-workbench.scheduled-agent-usage.v1`, role entrypoints for PM/review, orchestrator, worker, integrator,
  and health, no UI/browser/TUI/chat dependency, and `hosted_cloud_dependency=false`.
- `uv run awf review-gate --json` returned `ok=true`, no blocked files, `human_required_count=0`, and durable review
  verdict support for accepted, rejected, deferred, question, and human-required.
- `uv run awf workflow-fixture-test --json` passed with 72 total checks, 72 passed, and 0 failed.

## Accepted Goal 006 Evidence

- `.agent-runs/reports/goal-006/planning-backlog-20260604.md`
- `.agent-runs/reports/goal-006/t001-operator-views-20260604.md`
- `.agent-runs/reports/goal-006/t002-bdd-contract-20260604.md`
- `.agent-runs/reports/goal-006/t003-status-schema-20260604.md`
- `.agent-runs/reports/goal-006/t004-operator-status-20260604.md`
- `.agent-runs/reports/goal-006/t005-goal-dashboard-20260604.md`
- `.agent-runs/reports/goal-006/t006-increment-dashboard-20260604.md`
- `.agent-runs/reports/goal-006/t007-evidence-view-20260604.md`
- `.agent-runs/reports/goal-006/t008-review-actions-20260604.md`
- `.agent-runs/reports/goal-006/t009-review-decisions-20260604.md`
- `.agent-runs/reports/goal-006/t010-branch-pr-status-20260604.md`
- `.agent-runs/reports/goal-006/t011-trace-eval-links-20260604.md`
- `.agent-runs/reports/goal-006/t012-handoff-summary-20260604.md`
- `.agent-runs/reports/goal-006/t013-interface-decision-20260604.md`
- `.agent-runs/reports/goal-006/t014-selected-interface-20260604.md`
- `.agent-runs/reports/goal-006/t015-accessibility-small-screen-20260604.md`
- `.agent-runs/reports/goal-006/t016-scheduled-agent-workbench-20260604.md`

## Workbench Surfaces

- `docs/workbench/operator-views.md` defines the minimum operator views.
- `docs/workbench/operator-status-report.md` defines the consolidated status report.
- `docs/workbench/goal-dashboard.md` defines the long-horizon goal dashboard embedded in `operator-status`.
- `docs/workbench/increment-dashboard.md` defines the Goal 006 increment dashboard embedded in `operator-status`.
- `docs/workbench/evidence-view.md` defines evidence links for reports, traces, evals, Beads comments, branches, and PRs.
- `docs/workbench/review-actions.md` and `docs/workbench/review-decisions.md` define durable review flows.
- `docs/workbench/branch-pr-status.md` defines GitHub integration with repo-local fallback.
- `docs/workbench/trace-eval-links.md` defines self-hosted Langfuse and repo-local trace/eval link behavior.
- `docs/workbench/handoff-summary.md` defines compact session and scheduled-agent handoffs.
- `docs/workbench/interface-decision.md` selects CLI/static for Goal 006.
- `docs/workbench/interface.md` documents the selected CLI/static workbench surface.
- `docs/workbench/accessibility-small-screen.md` records why UI-specific checks are deferred while CLI/static remains
  selected.
- `docs/workbench/scheduled-agents.md` documents scheduled-agent use without a fragile UI dependency.

## Self-Hosted Boundary

Goal 006 does not require hosted Logfire, hosted Langfuse, GitHub credentials, cloud services, external project tokens,
a browser session, a terminal UI runtime, or hidden chat context. Optional GitHub and self-hosted Langfuse links enrich
the workbench when available, but deterministic acceptance uses repo-local artifacts and workflow commands.

## Reviewer Request

Independent reviewer should accept or reject whether Goal 006 is complete by checking:

- T001 through T016 are complete and backed by durable evidence.
- T017 presents final Goal 006 evidence and does not claim closure before reviewer acceptance.
- The operator can see current goal, work, blockers, decisions, evidence, traces, evals, branch/PR status, and handoffs
  without raw artifact spelunking.
- Review decisions are repo-local, reviewer-attributed, and inspectable.
- The selected CLI/static interface preserves self-hosted operation and scheduled-agent compatibility.
- Credential-free fixture validation passes.

## Reviewer Outcome

Accepted by independent reviewer agent `019e9277-dc80-7582-afc0-aa6c31e50232`.

Verdict: accepted.

Blocking findings: none.

Reviewer evidence checked:

- `.agent-runs/reports/goal-006/t017-goal-006-workbench-evidence-20260604.md`
- `specs/007-operator-workbench-review-ux/tasks.md`
- `docs/goals/006-operator-workbench-review-ux.md`
- `docs/goals/000-self-hosted-agent-system-roadmap.md`
- `docs/workbench/interface.md`
- `docs/workbench/scheduled-agents.md`
- `docs/workbench/trace-eval-links.md`

Reviewer commands checked:

- `uv run awf workflow-fixture-test --json` passed with 72/72.
- `uv run awf operator-status --json` passed and showed no human-required state.
- `uv run awf increment-status --spec-id 007-operator-workbench-review-ux --phase 'Goal 006' --json` passed and
  showed T017 open/claimed after T001 through T016.
- `uv run awf workbench-interface --json` passed with selected interface `cli-static`,
  `human_required=false`, and `external_service_required=false`.
- `uv run awf scheduled-agent-workbench --json` passed with no fragile UI dependency and
  `hosted_cloud_dependency=false`.
- `uv run awf review-gate --json` passed with `human_required_count=0`.

Required follow-up tickets: none.

Human review required: no.

Non-blocking note: `operator-status` reported 16 accepted Goal 006 evidence entries and omitted T013 from that specific
accepted-evidence list, while the T013 report itself records reviewer acceptance and this T017 report cites it. This
does not block Goal 006 acceptance, but tightening the dashboard classifier would improve completeness.
