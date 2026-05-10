# Cron Workflow

The workflow can run from a basic scheduler because all coordination state is in repo artifacts and Beads Rust.

## Roles

- Planner: checks health, reviews objectives/specs/tickets/reports/learnings, and creates planning output.
- Ticket planner: turns approved open spec tasks into Beads tickets so the executable backlog is populated.
- Worker: checks health, finds ready work, claims one item, and stops unless the claim is safe.
- Health: reports harness status and logs actionable issues.
- Next action: reports the canonical human/agent options for the current state.

## Example Schedules

```cron
*/30 * * * * cd /repo && uv run awf cron-tick --role worker --worker-id worker-1 --write
0 */4 * * * cd /repo && uv run awf cron-tick --role planner --write
15 * * * * cd /repo && uv run awf health-status --deep --json
*/15 * * * * cd /repo && uv run awf next-action --json
```

## Separation

Workers coordinate through Beads ready work and `.agent-runs/claims/`.
A worker may only act on one claimed item. If the item is already claimed, blocked, missing acceptance evidence, or
requires human judgment, the worker logs an issue and exits.

Spec `tasks.md` files are planning artifacts. They are not the normal worker queue. When Beads is available, workers use
`uv run awf ready-work`; ticket planner owns syncing approved tasks into Beads. If ready work is empty but open approved
tasks exist, the next action is ticket sync, not direct implementation from `tasks.md`.

## Issue Path

Any health or cron issue follows this path:

1. Detect with `health-status`, `cron-tick`, or a failing check.
2. Record a JSON artifact under `.agent-runs/health/`.
3. Create a Beads ticket when `--write` is used and `br` is available.
4. Let planner decompose or prioritize the issue in the next planning cycle.
