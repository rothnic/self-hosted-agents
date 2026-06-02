# Goal 003: Autonomous Multi-Agent Delivery Loop

## Objective

Make the repo-native PM, orchestrator, worker, integrator, and health loops reliable enough to move meaningful work
across sessions and scheduled runs without bypassing review evidence.

## Why This Matters

The project is about self-hosted agents, not one-off coding assistance. The operating loop needs to assign work,
recover from blockers, integrate evidence, and stop at the right review boundaries while keeping state in the repo.

## Product Iteration

This goal turns the existing workflow foundation into a practical autonomous delivery loop. It should support multiple
workers, stale-claim recovery, health checks, verified integration, and compact handoffs.

## Current Status

Goal 003 has accepted evidence for the current roadmap increment. The existing Spec Kit feature
`specs/003-automated-increment-orchestration/` was reopened for this product iteration after Goal 002 reviewer
acceptance, and T009 through T021 are now closed.

Planning/backlog evidence was accepted by independent reviewer agent `019e86e6-7ec3-7481-be8e-adda5d7d508a` in
`.agent-runs/reports/goal-003-backlog-review-20260602.md`.

T009 automation-loop behavior audit evidence is recorded in
`.agent-runs/reports/goal-003-t009-automation-loop-audit-20260602.md`.

T010 safe scheduled loop evidence is recorded in
`.agent-runs/reports/goal-003-t010-safe-scheduled-loop-20260602.md`; the active increment ledger is
`.agent-runs/increments/003-automated-increment-orchestration-goal-003.json`.

T011 stale-claim handoff evidence is recorded in
`.agent-runs/reports/goal-003-t011-stale-claim-handoff-20260602.md`.

T012 blocker reroute evidence is recorded in
`.agent-runs/reports/goal-003-t012-blocker-reroute-20260602.md`.

T013 worker branch/worktree evidence is recorded in
`.agent-runs/reports/goal-003-t013-worker-branch-worktree-20260602.md`.

T014 compact verification artifact evidence is recorded in
`.agent-runs/reports/goal-003-t014-compact-verification-artifacts-20260602.md`.

T015 integrator worker branch handoff evidence is recorded in
`.agent-runs/reports/goal-003-t015-integrator-worker-branch-handoff-20260602.md`.

T016 review-agent invocation guidance evidence is recorded in
`.agent-runs/reports/goal-003-t016-review-agent-invocation-guidance-20260602.md`.

T017 health-loop issue logging evidence is recorded in
`.agent-runs/reports/goal-003-t017-health-loop-issue-logging-20260602.md`.

T018 dry-run role transition fixture evidence is recorded in
`.agent-runs/reports/goal-003-t018-dry-run-role-transition-fixtures-20260602.md`.

T019 active work summary evidence is recorded in
`.agent-runs/reports/goal-003-t019-active-work-summary-20260602.md`.

T020 cleanup work evidence is recorded in
`.agent-runs/reports/goal-003-t020-cleanup-work-20260602.md`.

T021 end-to-end rehearsal evidence is recorded in
`.agent-runs/reports/goal-003-t021-end-to-end-rehearsal-20260602.md`.

Goal 003 increment completion evidence was accepted by independent reviewer agent
`019e87dc-b122-72d1-b3db-af302833dbe1` in `.agent-runs/reports/goal-003-increment-evidence-20260602.md`.

Backlog sync created the executable Beads tasks below:

- `awf-1oz` / T009: audit current PM, orchestrator, worker, integrator, and health automation-loop behavior.
- `awf-7e8` / T010: define the minimum safe scheduled loop for one active increment.
- `awf-h1z` / T011: add stale-claim status and handoff guidance for abandoned active work.
- `awf-j69` / T012: add blocker rerouting so unrelated ready work can continue.
- `awf-869` / T013: add deterministic worker branch naming and worktree setup guidance.
- `awf-6wg` / T014: add compact verification artifacts for ticket and increment profiles.
- `awf-l2j` / T015: add integrator verification of worker branches without merging to `main`.
- `awf-svc` / T016: add review-agent invocation guidance before PR and increment handoffs.
- `awf-8vh` / T017: add health-loop issue logging for recurring workflow failures.
- `awf-j3t` / T018: add dry-run fixtures for role transitions and blocked-state recovery.
- `awf-urx` / T019: add compact active-work summaries for claims, ready work, blockers, and stale work.
- `awf-rgg` / T020: add cleanup commands for obsolete active claims and old worktree pointers.
- `awf-60y` / T021: run a manual end-to-end increment rehearsal and record reviewer-accepted evidence.

Goal 003 has no remaining ready implementation tickets after T021 closure. The next roadmap step is Goal 004 planning;
use `uv run awf ready-work --json` and `uv run awf next-action --json` as the source of truth before claiming or
creating follow-on work, because priorities, blockers, or active claims may change.

## Scope

- Harden `awf automation-loop` roles for real scheduled use.
- Use worktree execution for write-capable worker sessions.
- Improve increment status, assignment, stale-claim handling, and blocker rerouting.
- Add review-agent support before PRs and increment handoffs.
- Store compact evidence that another agent can resume from.
- Keep explicit approval at architecture, priority, and merge boundaries. Use independent reviewer agents for goal
  evidence acceptance, and escalate to the human only when a decision is reserved or the evidence is missing or
  contradictory.

## Task Backlog

1. Audit current automation-loop behavior for PM, orchestrator, worker, integrator, and health roles.
2. Define the minimum safe scheduled loop for one active increment.
3. Add stale-claim detection and handoff guidance for abandoned work.
4. Add blocker rerouting so unrelated ready work can continue.
5. Add worker branch naming and worktree setup guidance.
6. Add compact verification artifacts for ticket and increment profiles.
7. Add integrator behavior that verifies worker branches without merging to `main`.
8. Add review-agent invocation guidance before PR creation.
9. Add health-loop issue logging for recurring failures.
10. Add scheduler docs for Codex app automations and local cron alternatives.
11. Add dry-run fixtures for role transitions and blocked-state recovery.
12. Add dashboards or summaries for active claims, ready work, and stale work.
13. Add cleanup commands for old claims and obsolete worktrees.
14. Run a manual end-to-end increment rehearsal.
15. Record lessons and follow-up tickets for any automation drift.

## Definition Of Done

- A scheduled worker can claim, implement, verify, and hand off one ticket in a worktree.
- The integrator can verify completed worker work and route evidence to an independent reviewer boundary.
- Blockers and stale claims are visible and do not idle unrelated work.
- Health automation logs actionable issues instead of silently failing.
- The workflow fixture covers the key state transitions.

## Proof Commands

```bash
uv run awf verify --profile health --json
uv run awf verify --profile increment --json
uv run awf automation-loop --role pm-review --json
uv run awf automation-loop --role orchestrator --json
uv run awf automation-loop --role worker --worker-id fixture-worker --json
uv run awf automation-loop --role integrator --json
uv run awf workflow-fixture-test
```

## Review Blocking Criteria

- Automation mutates across a human gate.
- Scheduled roles require hidden local state.
- Worker branches cannot be reviewed or resumed by another agent.
- Blocked work hides ready work.
- Evidence is too verbose or too sparse for handoff.

## Kickoff Prompt

```text
/goal Execute docs/goals/003-autonomous-multi-agent-delivery-loop.md
in /Users/nroth/workspace/self-hosted-agents. Harden the repo-native automation
roles so work can move across scheduled sessions using Beads, claims, worktrees,
verification artifacts, and independent review gates. Decompose into spec tasks first,
then implement one claimed ticket at a time.
```
