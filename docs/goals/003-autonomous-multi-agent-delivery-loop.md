# Goal 003: Autonomous Multi-Agent Delivery Loop

## Objective

Make the repo-native PM, orchestrator, worker, integrator, and health loops reliable enough to move meaningful work
across sessions and scheduled runs without bypassing human review.

## Why This Matters

The project is about self-hosted agents, not one-off coding assistance. The operating loop needs to assign work,
recover from blockers, integrate evidence, and stop at the right review boundaries while keeping state in the repo.

## Product Iteration

This goal turns the existing workflow foundation into a practical autonomous delivery loop. It should support multiple
workers, stale-claim recovery, health checks, verified integration, and compact handoffs.

## Scope

- Harden `awf automation-loop` roles for real scheduled use.
- Use worktree execution for write-capable worker sessions.
- Improve increment status, assignment, stale-claim handling, and blocker rerouting.
- Add review-agent support before PRs and increment handoffs.
- Store compact evidence that another agent can resume from.
- Keep human approval at architecture, priority, and merge boundaries.

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
- The integrator can verify completed worker work and stop at human review.
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
verification artifacts, and human review gates. Decompose into spec tasks first,
then implement one claimed ticket at a time.
```
