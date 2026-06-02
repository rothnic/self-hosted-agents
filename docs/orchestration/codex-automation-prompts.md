# Codex Automation Prompts

Use these prompts when creating Codex app automations for this repo. Configure each automation to run in this repository
or a worktree for the target branch, then let the command output drive the next scheduled run.

Codex automations should call the bootstrapped `.venv/bin/awf` entrypoint directly. Some Codex automation sandboxes
reject `uv` cache or temp paths before `awf` can start, even when persistent uv caching is disabled.
Configure Codex cron automations with the `worktree` execution environment; `local` automation sessions may be
read-only and fail when `awf --write` creates claim, verification, or evidence files.

```bash
.venv/bin/awf bootstrap --json
.venv/bin/awf increment-status \
  --spec-id 003-automated-increment-orchestration \
  --phase "Goal 003" \
  --json
```

## PM/Review Loop

Run the PM/review automation loop for this repo.

Use repo artifacts as source of truth. Run:

```bash
.venv/bin/awf automation-loop \
  --role pm-review \
  --spec-id 003-automated-increment-orchestration \
  --phase "Goal 003" \
  --write \
  --json
```

If the output reports missing or contradictory evidence, summarize the decision needed and stop. If the gate is only
goal or increment evidence review, route it to an independent reviewer agent and record the outcome.
If ready work is low and approved spec tasks exist, refresh backlog through the command output only.
Do not implement product changes.

## Orchestrator Loop

Run the orchestrator automation loop for this repo.

Run:

```bash
.venv/bin/awf automation-loop \
  --role orchestrator \
  --spec-id 003-automated-increment-orchestration \
  --phase "Goal 003" \
  --write \
  --json
```

Assign only unclaimed unblocked Beads work. If a blocker or stale claim appears, leave it visible for PM/review and
continue with other unblocked work when available. Do not implement the claimed work in this loop.

## Worker Loop

Run the worker automation loop for this repo.

Run:

```bash
.venv/bin/awf automation-loop \
  --role worker \
  --worker-id <stable-worker-id> \
  --spec-id 003-automated-increment-orchestration \
  --phase "Goal 003" \
  --write \
  --json
```

If one ticket is claimed, work only that ticket on its worker branch, make the smallest coherent change, then run
`.venv/bin/awf verify --profile ticket --write --json`. Record evidence on the Beads ticket, push the worker branch,
and stop. If blocked, record the blocker and release the loop to other work.

## Integrator Loop

Run the integrator automation loop for this repo.

Review completed worker branches for the active increment. Merge only clean, verified worker branches into the feature
branch. Run:

```bash
.venv/bin/awf automation-loop \
  --role integrator \
  --spec-id 003-automated-increment-orchestration \
  --phase "Goal 003" \
  --write \
  --json
```

Then run
`.venv/bin/awf verify --profile increment --write --json`. Present increment evidence for independent reviewer
acceptance when ready, record the reviewer outcome durably, and do not merge to `main`.

## Health Loop

Run the health automation loop for this repo.

Run:

```bash
.venv/bin/awf automation-loop \
  --role health \
  --spec-id 003-automated-increment-orchestration \
  --phase "Goal 003" \
  --write \
  --json
```

If checks fail, log the issue through the workflow output and stop implementation. If checks pass, report only the next
safe action.
