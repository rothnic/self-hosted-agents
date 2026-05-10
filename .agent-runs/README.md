# Agent Runs

This directory stores durable run artifacts created by workflow commands.

- `manifests/`: machine-readable run inputs and mode.
- `reports/`: human-readable and JSON reports.
- `blocked/`: human review gates that must be resolved before continuing.
- `claims/`: one-work-item claims owned by an agent or scheduled worker.
- `increments/`: phase-level ledgers for decentralized worker and integration runs.
- `verifications/`: compact outputs from `uv run awf verify --write`.
- `learnings/`: concise retrospective notes for future planning cycles.
