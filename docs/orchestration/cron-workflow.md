# Automated Increment Workflow

The workflow can run from Codex app automations, local cron, or another scheduler because coordination state lives in
repo artifacts and Beads Rust. The scheduler is replaceable; the repo remains authoritative.

The default increment boundary is one Spec Kit phase. The current active scheduled increment is Goal 003:

- spec: `003-automated-increment-orchestration`
- phase: `Goal 003`
- increment id: `003-automated-increment-orchestration-goal-003`
- ledger: `.agent-runs/increments/003-automated-increment-orchestration-goal-003.json`

Scheduled Goal 003 runs must pass `--spec-id 003-automated-increment-orchestration --phase "Goal 003"`. The no-arg
`automation-loop` defaults still target the older solution-comparison Phase 6 increment, so they are not the safe
scheduler surface for Goal 003 until the default active-increment routing is hardened.

## Roles

- PM/review: checks health, reviews completed work, captures learnings, refreshes backlog, and opens review gates.
- Orchestrator: reads increment state, finds unclaimed unblocked work, assigns worker branches, and routes blockers.
- Worker: claims one ticket, works on a focused branch, verifies the ticket, records evidence, and pushes.
- Integrator: reviews completed worker branches, integrates safe work into the feature branch, and prepares review.
- Health: runs lightweight checks and logs issues before automation silently stalls.

Routine worker branches target the feature branch for the increment. Agents must not merge to `main`; explicit
architecture, product, priority, scope, and final merge decisions remain human decisions. Goal or increment evidence
review is handled by one agent presenting evidence and an independent reviewer agent accepting or rejecting it in a
durable artifact, so automation does not pause solely because a human review label exists.

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
result under `.agent-runs/verifications/`. Written artifacts use compact schema `awf.verify.compact.v1`: they keep
check names, commands, statuses, counts, short failure details, git/ready-work/review-gate summaries, acceptance source,
and the next safe action without embedding full nested command stdout or stderr.

## Increment State

Phase state lives in `.agent-runs/increments/<increment-id>.json`. The ledger records objective/spec context, phase,
feature branch, child tickets, active worker branches, claims, blockers, validation evidence, review status, learning
proposals, and the next action.

Beads remains the executable backlog. Increment membership and role routing use normal labels instead of a Beads schema
fork: `increment:<id>`, `role:<role>`, `scope:<area>`, and `branch:<name>`.

## Example Schedules

Local cron can use `uv run awf`. Codex app automations should use `.venv/bin/awf` directly because `uv` can need cache
or temp filesystem access before `awf` starts.

Minimum safe Goal 003 loop:

1. Health verifies the repo first and logs an issue before implementation work if checks fail.
2. PM/review reads the explicit Goal 003 ledger, backlog, claims, blockers, and evidence.
3. Orchestrator assigns only unclaimed, unblocked Goal 003 Beads work.
4. Each worker uses a stable worker id, acts on one claimed ticket, runs ticket verification, records evidence, pushes,
   and stops.
5. Integrator verifies completed worker branches and increment evidence, routes goal evidence to an independent reviewer
   agent, and does not merge to `main`.

```cron
SCOPE='--spec-id 003-automated-increment-orchestration --phase "Goal 003"'
0 */4 * * * cd /repo && uv run awf automation-loop --role pm-review $SCOPE --write
*/15 * * * * cd /repo && uv run awf automation-loop --role orchestrator $SCOPE --write
*/30 * * * * cd /repo && uv run awf automation-loop --role worker --worker-id worker-1 $SCOPE --write
10 * * * * cd /repo && uv run awf automation-loop --role integrator $SCOPE --write
*/20 * * * * cd /repo && uv run awf automation-loop --role health $SCOPE --write
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

## Worker Branches And Worktrees

Claim files include deterministic worker assignment fields derived from Beads issue metadata:

- `worker_branch`: `codex/<issue-id>-<title-slug>`
- `worktree_path`: `../self-hosted-agents-worktrees/<issue-id>-<title-slug>`
- `worktree_setup.add_worktree`: the exact `git worktree add -b ...` command using the increment feature branch
- `worktree_setup.resume`: the exact command for another agent to inspect the existing worktree

Workers should use those claim fields instead of inventing branch or worktree names. Orchestrators and worker loops
must preserve the claim fields so another agent can resume or integrate the branch without hidden local conventions.

Blocked work does not stop the whole increment unless every remaining task depends on it. A worker that hits a blocker
records the blocker, comments or marks the Beads ticket, creates a follow-up when actionable, and exits. The
orchestrator keeps assigning other unblocked work. The PM/review loop later reprioritizes, decomposes, or asks a
targeted human question.

`increment-status` includes `blocker_reroute` for this decision. When blocked and ready work exist together,
`blocker_reroute.can_continue=true`, `next_unblocked_issue_id` names the next assignable ticket, and blocked entries
preserve their blocking dependency context for PM/review. Orchestrators should keep assigning the unblocked ticket;
PM/review should triage the blockers in parallel.

## Stale Claims

`increment-status` exposes stale active claims after the claim age crosses the workflow threshold. Stale claim entries
include the claim path, worker id, worker branch, feature branch, issue title/status/external ref, acceptance command,
age, and handoff guidance.

Use the stale-claim handoff fields this way:

1. Resume: another agent may continue the same claim after reading the claim file and linked Beads issue.
2. Reassign: PM/review may assign a replacement only after confirming the original worker is abandoned or unreachable.
3. Archive: move the claim under `.agent-runs/claims/archive-<month>/` only after the Beads issue is closed, blocked
   with evidence, or explicitly superseded.

Do not hide stale claims by deleting active claim files. Leave them visible until the resume, reassign, or archive path
is recorded in repo state.

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
