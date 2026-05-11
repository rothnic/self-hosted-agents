# Automated Increment Workflow

The workflow can run from Codex app automations, local cron, or another scheduler because coordination state lives in
repo artifacts and Beads Rust. The scheduler is replaceable; the repo remains authoritative.

The default increment boundary is one Spec Kit phase. For the solution-comparison roadmap, the first target increment
is Phase 3 of `002-solution-comparison-roadmap`.

## Roles

- PM/review: checks health, reviews completed work, captures learnings, refreshes backlog, and opens review gates.
- Orchestrator: reads increment state, finds unclaimed unblocked work, assigns worker branches, and routes blockers.
- Worker: claims one ticket, works on a focused branch, verifies the ticket, records evidence, and pushes.
- Integrator: reviews completed worker branches, integrates safe work into the feature branch, and prepares review.
- Health: runs lightweight checks and logs issues before automation silently stalls.

Routine worker branches target the feature branch for the increment. Agents must not merge to `main`; the normal human
gate is the final feature-branch PR to `main` or an explicit architecture, product, priority, or scope decision.

## Verification Surface

Agents should use one command instead of remembering long checklists:

```bash
uv run awf verify --profile ticket --json
uv run awf verify --profile increment --json
uv run awf verify --profile health --json
uv run awf verify --profile pre-merge --json
```

`verify` runs the checks for the selected context, includes acceptance evidence when ticket work is active, summarizes
git status, Beads readiness, review-gate state, failures, and returns one `next_action`. Pass `--write` to store the
result under `.agent-runs/verifications/`.

## Increment State

Phase state lives in `.agent-runs/increments/<increment-id>.json`. The ledger records objective/spec context, phase,
feature branch, child tickets, active worker branches, claims, blockers, validation evidence, review status, learning
proposals, and the next action.

Beads remains the executable backlog. Increment membership and role routing use normal labels instead of a Beads schema
fork: `increment:<id>`, `role:<role>`, `scope:<area>`, and `branch:<name>`.

## Example Schedules

Set `UV_CACHE_DIR` to a writable path outside the repo before invoking `uv run`; Codex and other hosted runners may not
be able to use the default shared user cache.

```cron
0 */4 * * * cd /repo && export UV_CACHE_DIR="${TMPDIR:-/tmp}/codex-uv-cache/self-hosted-agents" && mkdir -p "$UV_CACHE_DIR" && uv run awf automation-loop --role pm-review --write
*/15 * * * * cd /repo && export UV_CACHE_DIR="${TMPDIR:-/tmp}/codex-uv-cache/self-hosted-agents" && mkdir -p "$UV_CACHE_DIR" && uv run awf automation-loop --role orchestrator --write
*/30 * * * * cd /repo && export UV_CACHE_DIR="${TMPDIR:-/tmp}/codex-uv-cache/self-hosted-agents" && mkdir -p "$UV_CACHE_DIR" && uv run awf automation-loop --role worker --worker-id worker-1 --write
10 * * * * cd /repo && export UV_CACHE_DIR="${TMPDIR:-/tmp}/codex-uv-cache/self-hosted-agents" && mkdir -p "$UV_CACHE_DIR" && uv run awf automation-loop --role integrator --write
*/20 * * * * cd /repo && export UV_CACHE_DIR="${TMPDIR:-/tmp}/codex-uv-cache/self-hosted-agents" && mkdir -p "$UV_CACHE_DIR" && uv run awf automation-loop --role health --write
```

Codex app automation prompts for these roles live in
`docs/orchestration/codex-automation-prompts.md`.

## Separation

Workers coordinate through Beads ready work and `.agent-runs/claims/`.
A worker may only act on one claimed item. If the item is already claimed, blocked, missing acceptance evidence, or
requires human judgment, the worker logs an issue and exits.

Spec `tasks.md` files are planning artifacts. They are not the normal worker queue. When Beads is available, workers use
`uv run awf ready-work`; ticket planner owns syncing approved tasks into Beads. If ready work is empty but open approved
tasks exist, the next action is ticket sync, not direct implementation from `tasks.md`.

Blocked work does not stop the whole increment unless every remaining task depends on it. A worker that hits a blocker
records the blocker, comments or marks the Beads ticket, creates a follow-up when actionable, and exits. The
orchestrator keeps assigning other unblocked work. The PM/review loop later reprioritizes, decomposes, or asks a
targeted human question.

## Session Cadence

Interactive agent sessions should be bounded by workflow phase. A planner session should end with an approved plan,
targeted questions, or populated Beads work. An implementation session should usually complete one claimed ticket,
verify it, record evidence, and stop at a clean pushed checkpoint. A review session should record the human decision and
handoff the next role.

Recommend a new session after a pushed commit, a resolved human gate, a planning-to-implementation transition, an
implementation-to-review transition, or a long run where current context could confuse the next action. The handoff must
include git status, latest commit, active objective/spec, ready work, validation evidence, and recommended next role.

## Issue Path

Any health or cron issue follows this path:

1. Detect with `health-status`, `cron-tick`, or a failing check.
2. Record a JSON artifact under `.agent-runs/health/`.
3. Create a Beads ticket when `--write` is used and `br` is available.
4. Let planner decompose or prioritize the issue in the next planning cycle.
