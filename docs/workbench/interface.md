# Workbench Interface

Status: implemented for Goal 006 T014.

`uv run awf workbench-interface --json` generates the selected CLI/static operating interface for the workbench. It is
a restrained command-and-artifact surface over the existing status, evidence, review, trace/eval, branch/PR, and handoff
reports.

Use `uv run awf workbench-interface --write --json` to persist a JSON artifact under `.agent-runs/reports/workbench/`.

## Interface Contract

Generated artifacts use schema `awf.operator-workbench.interface.v1`.

The interface keeps the Goal 006 decision from `docs/workbench/interface-decision.md`:

- Selected: CLI/static repo artifacts.
- Deferred: local web or terminal UI.
- No local UI runtime is required or added by T014.
- Deterministic validation remains credential-free.

## Restrained Operating Design

The interface is intentionally small:

- One decision strip for phase, next owner, recommendation, next ticket, review state, and human-required state.
- Four primary action entries: inspect status, continue work, record review, and run acceptance.
- Six panels: decision, work, evidence, review, trace/eval, and branch/PR.
- Exact source artifacts instead of hidden state or chat-only context.

The generated surface favors dense text, JSON, and exact artifact handles over decorative layout. It does not add cards,
nested panels, a browser runtime, a terminal UI runtime, a build step, or a server process.

## Primary Actions

Inspect:

```bash
uv run awf operator-status --json
```

Continue:

```bash
uv run awf handoff-summary --json
```

Review:

```bash
uv run awf review-decision --target-kind ticket --target-id <ticket-id> --verdict accepted --reviewer-id <agent-id> --evidence <path> --write --json
```

Verify:

```bash
uv run awf workflow-fixture-test
```

## Source Artifacts

The interface links back to source artifacts instead of replacing them:

- `docs/workbench/operator-status-report.md`
- `docs/workbench/status-artifact-schema.md`
- `docs/workbench/interface-decision.md`
- `.agent-runs/claims/`
- `.agent-runs/reports/`
- `.agent-runs/verifications/`
- `.agent-runs/review-decisions/`
- `.beads/issues.jsonl`

## Self-Hosted Behavior

The command does not call hosted Logfire, hosted Langfuse, GitHub, cloud credentials, or external project tokens. Optional
self-hosted Langfuse and PR links are displayed only when already present in repo-local artifacts. Repo-local trace and
eval artifacts remain authoritative.

## Scheduled Agents

Scheduled agents, including scheduled agents in automation loops, can use the same interface without a fragile UI
dependency. `docs/workbench/scheduled-agents.md`
defines the fuller role-by-role contract. The generated artifact includes `scheduled_agent_compatibility` so scheduled
agents can start from the same command surface as local sessions:

```bash
uv run awf scheduled-agent-workbench --json
uv run awf workbench-interface --json
uv run awf handoff-summary --json
uv run awf operator-status --json
```

The interface exposes the exact next ticket, claim path, evidence handles, review command shape, and acceptance command
needed for PM, worker, integrator, reviewer, and health loops.
