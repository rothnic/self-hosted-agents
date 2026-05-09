---
name: health-status
description: Use when reviewing project harness health, workflow status, scheduled run readiness, or workflow issues.
---

# Health Status

## Purpose

Assess whether the project harness can safely continue. Focus on the workflow system: environment setup, hooks, Beads,
specs, BDD contracts, review gates, repo hygiene, ready work, claims, recent runs, and unresolved health issues.

## Inputs

- `uv run awf health-status --deep --json`
- `uv run awf context-index --json`
- `uv run awf ready-work --json`
- `.agent-runs/health/`
- `.agent-runs/claims/`
- `.agent-runs/reports/`
- `.agent-runs/learnings/`

## Workflow

1. Run `uv run awf health-status --deep`.
2. If health is clean, report the next safe state-machine transition.
3. If health has issues, classify each issue as blocker, warning, or follow-up.
4. Log every actionable issue with `uv run awf issue-log --write`.
5. If a human decision is required, stop and route to `review-gatekeeper`.
6. If ready work exists and no gate is active, route to `implementer`.
7. If no ready work exists, route to `pm-steward` for the next planning cycle.

## Scheduled Runs

- Planner cron: run `uv run awf cron-tick --role planner --write`.
- Worker cron: run `uv run awf cron-tick --role worker --worker-id <id> --write`.
- Health cron: run `uv run awf health-status --deep --json`.

## Stop Conditions

- Bootstrap, review gate, repo hygiene, spec lint, or BDD lint fails.
- Beads is unavailable.
- A ready task lacks objective, spec, or acceptance evidence.
- Another worker has already claimed the task.
- The next action would require product or architecture judgment.

## Output

Return a concise status summary, next safe action, issue ids logged, and commands run.
