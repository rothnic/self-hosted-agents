# Scheduled-Agent Workbench Usage

Status: implemented for Goal 006 T016.

`uv run awf scheduled-agent-workbench --json` records how scheduled agents use the CLI/static workbench without a
fragile UI dependency.

Use `uv run awf scheduled-agent-workbench --write --json` to persist a JSON artifact under
`.agent-runs/reports/workbench/scheduled-agents/`.

Generated artifacts use schema `awf.operator-workbench.scheduled-agent-usage.v1`.

## Current Decision

Scheduled agents must start from repo-local artifacts and commands instead of a browser session, local UI state, prior
chat context, or hidden service state. The selected interface remains CLI/static.

The stable entry commands are:

- `uv run awf scheduled-agent-workbench --json`
- `uv run awf handoff-summary --audience scheduled --json`
- `uv run awf operator-status --json`
- `uv run awf ready-work --json`

## Role Entrypoints

PM/review agents inspect `operator-status`, `goal_dashboard`, `increment_dashboard`, and `review_gate` before routing
backlog, blockers, or review actions.

Orchestrator agents inspect Beads ready work, claim files, and increment handoff fields before assigning one unblocked
ticket.

Worker agents inspect the scheduled handoff summary, active claim artifact, source docs, linked spec task, and ticket
acceptance command before making the smallest coherent change.

Integrator agents inspect branch/PR fallback, evidence view, review-gate state, and increment dashboards before
presenting evidence to an independent reviewer.

Health agents inspect `health-status`, repo hygiene, workflow-state lint, and review-gate state before logging issues
and stopping unsafe mutation.

## Artifact Contract

Scheduled agents use these source-of-truth handles:

- `.beads/issues.jsonl`
- `.agent-runs/claims/`
- `.agent-runs/reports/`
- `.agent-runs/review-decisions/`
- `.agent-runs/verifications/`
- `docs/workbench/`
- `specs/007-operator-workbench-review-ux/tasks.md`

The workbench artifact requires copy-ready handles, Beads ready work, claim files, and independent reviewer evidence.
It does not require a UI session, browser runtime, terminal UI runtime, or prior chat context.

## Resilience Rules

- Start from repo-local commands and artifacts.
- Use Beads ready work and claim files for work separation.
- Record presenter evidence and independent reviewer acceptance or rejection in durable repo state.
- Treat GitHub, self-hosted Langfuse, and other service links as optional enrichment with repo-local fallback.
- Run credential-free deterministic validation before closing work.

## Self-Hosted Boundary

This scheduled-agent workbench usage contract is credential-free. It does not call hosted Logfire, hosted Langfuse,
GitHub, cloud credentials, external project tokens, browser automation, or any UI runtime. Repo-local artifacts remain
authoritative.
