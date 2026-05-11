# Codex Automation Prompts

Use these prompts when creating Codex app automations for this repo. Configure each automation to run in this repository
or a worktree for the target branch, then let the command output drive the next scheduled run.

Codex automations should call the bootstrapped `.venv/bin/awf` entrypoint directly. Some Codex automation sandboxes
reject `uv` cache or temp paths before `awf` can start, even when persistent uv caching is disabled.

```bash
.venv/bin/awf bootstrap --json
```

## PM/Review Loop

```text
Run the PM/review automation loop for this repo.

Use repo artifacts as source of truth. Run
`.venv/bin/awf automation-loop --role pm-review --write --json`.
If the output reports a human gate or unclear objective, summarize the decision needed and stop.
If ready work is low and approved spec tasks exist, refresh backlog through the command output only.
Do not implement product changes.
```

## Orchestrator Loop

```text
Run the orchestrator automation loop for this repo.

Run `.venv/bin/awf automation-loop --role orchestrator --write --json`.
Assign only unclaimed unblocked Beads work. If a blocker or stale claim appears, leave it visible for PM/review and
continue with other unblocked work when available. Do not implement the claimed work in this loop.
```

## Worker Loop

```text
Run the worker automation loop for this repo.

Run `.venv/bin/awf automation-loop --role worker --worker-id <stable-worker-id> --write --json`.
If one ticket is claimed, work only that ticket on its worker branch, make the smallest coherent change, then run
`.venv/bin/awf verify --profile ticket --write --json`. Record evidence on the Beads ticket, push the worker branch,
and stop. If blocked, record the blocker and release the loop to other work.
```

## Integrator Loop

```text
Run the integrator automation loop for this repo.

Review completed worker branches for the active increment. Merge only clean, verified worker branches into the feature
branch. Run `.venv/bin/awf automation-loop --role integrator --write --json` and
`.venv/bin/awf verify --profile increment --write --json`. Prepare the human review PR to `main` when the increment is
ready, but do not merge to `main`.
```

## Health Loop

```text
Run the health automation loop for this repo.

Run `.venv/bin/awf automation-loop --role health --write --json`.
If checks fail, log the issue through the workflow output and stop implementation. If checks pass, report only the next
safe action.
```
