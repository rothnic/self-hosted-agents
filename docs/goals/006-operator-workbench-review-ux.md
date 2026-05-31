# Goal 006: Operator Workbench And Review UX

## Objective

Build the human-facing workbench for inspecting, approving, and steering self-hosted agent work without reading raw repo
internals or manually assembling workflow command output.

## Why This Matters

The project owner should operate at the decision level. A useful self-hosted agent system needs a clear interface for
current goals, active work, blockers, evidence, approvals, traces, evals, and next choices.

## Product Iteration

This goal turns the repo-native operating model into an operator experience. It may start as CLI reports and static
artifacts, then evolve into a local web or terminal UI if evidence shows that is worth the maintenance cost.

## Scope

- Define the operator information architecture.
- Show objectives, goals, specs, tickets, claims, blockers, traces, evals, and review gates.
- Provide approve, request changes, defer, and prioritize flows.
- Link Beads issues to run artifacts, trace views, eval reports, and PRs.
- Keep the workbench self-hosted and repo-backed.
- Preserve command-line workflows for automation and testability.

## Task Backlog

1. Research the minimum operator views needed for this project.
2. Define BDD contracts for human review and approval workflows.
3. Add a consolidated `awf status` or equivalent report if missing.
4. Add a goal dashboard showing long-horizon goals and current phase.
5. Add an increment dashboard showing tickets, claims, blockers, and validation.
6. Add an evidence view linking run artifacts, traces, evals, and Beads comments.
7. Add review-gate actions for approve, request changes, defer, and ask questions.
8. Add PR and branch status integration if GitHub access is available.
9. Add trace and eval deep links for Langfuse-backed runs.
10. Add concise daily or session handoff summaries.
11. Decide whether the workbench should remain CLI/static or become a local UI.
12. Implement the selected interface with restrained operating-tool design.
13. Add accessibility and small-screen review checks if a UI is built.
14. Add workflow fixture coverage for key operator actions.
15. Document how scheduled agents use the workbench artifacts.

## Definition Of Done

- The human can see what is happening, what is blocked, and what decision is needed.
- Review decisions are recorded in durable repo artifacts.
- Evidence links connect goals, tickets, runs, traces, evals, branches, and PRs.
- Agents can still operate through CLI and repo artifacts without a fragile UI dependency.
- The workbench reduces context bloat in long-running sessions.

## Proof Commands

```bash
uv run awf next-action --json
uv run awf context-index --json
uv run awf verify --profile increment --json
uv run awf workflow-fixture-test
uv run awf repo-hygiene
```

Add UI or report-specific verification commands after interface selection.

## Review Blocking Criteria

- The workbench hides source-of-truth repo artifacts.
- Human decisions are not recorded durably.
- The UI or report cannot be regenerated from repo state.
- It encourages agents to bypass review gates.
- It adds a separate product surface before the selected stack and deployment are stable.

## Kickoff Prompt

```text
/goal Execute docs/goals/006-operator-workbench-review-ux.md
in /Users/nroth/workspace/self-hosted-agents. Define and build the operator
workbench for goals, tickets, claims, blockers, evidence, traces, evals, approvals,
branches, and PRs while keeping repo artifacts and CLI workflows as the source of
truth.
```
