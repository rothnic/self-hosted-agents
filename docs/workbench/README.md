# Operator Workbench

Goal 006 turns repo-native workflow state into a decision-ready operator surface for the project owner and scheduled
agents.

Start here when an agent needs to understand what the workbench must show before implementing commands, reports, or a
local UI.

## View Index

- `operator-views.md`: minimum operator views, source artifacts, required decisions, fallback behavior, and sequencing.
- `status-artifact-schema.md`: generated status and decision-summary artifact schema for later reports or UI surfaces.
- `operator-status-report.md`: first consolidated CLI/static status report, source inputs, sections, and fallbacks.
- `goal-dashboard.md`: long-horizon goal dashboard, current phase, and accepted evidence links.
- `increment-dashboard.md`: increment dashboard for tickets, claims, blockers, workers, and validation state.
- `evidence-view.md`: evidence view for run artifacts, traces, evals, Beads comments, branches, and PR fallback.
- `review-actions.md`: durable review-gate actions for approve, request changes, defer, and ask questions.
- `review-decisions.md`: durable reviewer decision records with verdict, evidence checked, findings, and follow-up
  routing.
- `branch-pr-status.md`: branch and PR status integration with repo-local fallback when GitHub access is unavailable.
- `../goals/006-operator-workbench-review-ux.md`: Goal 006 objective, scope, proof commands, and review blockers.
- `../../specs/007-operator-workbench-review-ux/spec.md`: requirements and success criteria.
- `../../specs/007-operator-workbench-review-ux/tasks.md`: Beads-backed implementation task order.
- `.agent-runs/increments/007-operator-workbench-review-ux-goal-006.json`: current Goal 006 increment ledger.
- `.agent-runs/reports/goal-006/planning-backlog-20260604.md`: planning and backlog evidence accepted by an
  independent reviewer.

## Current Boundary

The first workbench surface should be CLI/static and generated from repo state. A local web or terminal UI is a later
interface decision, not a requirement for the first status proof.

The workbench must not replace source-of-truth artifacts. It should summarize and link to objectives, goals, specs,
Beads issues, claims, blockers, validations, traces, evals, branches, PRs, run reports, and reviewer decisions.

## Operating Rules

- Generate from repo artifacts and workflow commands; do not depend on prior chat context.
- Keep deterministic validation credential-free, even when optional GitHub or self-hosted Langfuse links are present.
- Record goal and increment evidence through presenter evidence plus independent reviewer acceptance or rejection.
- Escalate to the human only when a decision is explicitly reserved, missing, or contradicted by reviewer evidence.
- Preserve exact artifact handles so another agent can resume without reading the whole conversation.

## Next Implementation Step

T011 should add trace and eval deep links for self-hosted Langfuse-backed and repo-local evidence.
