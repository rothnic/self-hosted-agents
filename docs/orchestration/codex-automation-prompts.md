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

If one ticket is claimed, work only that ticket using the claim file's `worker_branch`, `worktree_path`, and
`worktree_setup` fields. Make the smallest coherent change, then run
`.venv/bin/awf verify --profile ticket --write --json`. Record evidence on the Beads ticket, push the worker branch,
and stop. If blocked, record the blocker and release the loop to other work.

## Integrator Loop

Run the integrator automation loop for this repo.

Review the command output's `integrator_handoff.worker_branch_reviews`. For each completed worker branch, run the
reported verification and diff commands before integrating it into the feature branch. Integrator output must not merge
to `main`; `main_merge_allowed=false` is the expected policy. Run:

```bash
.venv/bin/awf automation-loop \
  --role integrator \
  --spec-id 003-automated-increment-orchestration \
  --phase "Goal 003" \
  --write \
  --json
```

Then run `.venv/bin/awf verify --profile increment --write --json`. Before creating or updating a PR as goal or
increment evidence, use `integrator_handoff.review_agent_invocation` as the reviewer prompt. Send the reviewer the
increment ledger path, written verification artifact, `integrator_handoff.worker_branch_reviews`, git status, feature
branch diff, and relevant `.agent-runs/reports/` evidence. The reviewer must be separate from the presenting agent and
must return `accepted` or `rejected` with findings and required follow-up tickets. Record the reviewer agent id,
outcome, evidence checked, findings, follow-ups, and timestamp durably. Do not block solely because human review might
be useful, and do not merge to `main`.

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
