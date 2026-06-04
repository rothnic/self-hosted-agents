# Long-Horizon Goal Backlog

Date: 2026-05-31

## Purpose

This backlog defines major product iterations for the self-hosted agents project. These are intentionally larger than
single Beads tickets. Each goal should take many implementation sessions, produce durable evidence, and move the project
toward a usable self-hosted agent operating system.

Use this backlog when starting a long-running `/goal` session. Start from the umbrella goal when the intent is broad,
or pick one child goal when the intent is a focused product iteration.

Umbrella goal: [Self-Hosted Agent System Roadmap](000-self-hosted-agent-system-roadmap.md)

## Goal Order

0. [Self-Hosted Agent System Roadmap](000-self-hosted-agent-system-roadmap.md)
   - Umbrella. Execute the child goals below in order.
1. [Self-Hosted Observability And Evaluation Control Plane](001-self-hosted-observability-evaluation-control-plane.md)
   - Accepted. Make traces, scores, and run evidence inspectable in a self-hosted LLM observability backend.
2. [Durable Agent Execution Runtime](002-durable-agent-execution-runtime.md)
   - Accepted. Make long-running agent work retry, resume, wait for humans, and avoid duplicate side effects.
3. [Autonomous Multi-Agent Delivery Loop](003-autonomous-multi-agent-delivery-loop.md)
   - Accepted. Let scheduled PM, orchestrator, worker, integrator, and health roles move work safely.
4. [Candidate Platform Decision And Product Baseline](004-candidate-platform-decision-product-baseline.md)
   - Accepted. Chose a primary stack from comparable implementation evidence.
5. [Self-Hosted Deployment And Operations Reference](005-self-hosted-deployment-operations-reference.md)
   - Accepted. Ran the chosen stack on controlled infrastructure with backups, secrets, and recovery.
6. [Operator Workbench And Review UX](006-operator-workbench-review-ux.md)
   - Active. Let the human inspect, approve, and steer agent work without reading raw repo internals.

## Backlog Rules

- Do not implement directly from a goal document.
- Use a selected goal to create or update a focused Spec Kit feature first.
- Decompose the selected goal into tasks and Beads tickets only after scope and proof gates are clear.
- Keep deterministic repo-local validation even when the goal introduces services.
- Record self-hosted service setup, credentials, ports, storage, and recovery evidence as part of completion.
- Do not stop solely because human review may be useful. For goal evidence, one agent presents the evidence and an
  independent reviewer agent records acceptance or rejection. Escalate to the human only when the user explicitly
  reserves the decision or the reviewer finds evidence missing or contradictory.

## Recommended Kickoff

Start with Goal 000 for the full long-horizon roadmap, or Goal 006 for the next focused product iteration. Goals 001
through 005 have accepted evidence for the current roadmap increment. Goal 006 should define and build the operator
workbench for status, evidence, review decisions, and handoffs.

Copy/paste prompt:

```text
/goal Execute docs/goals/000-self-hosted-agent-system-roadmap.md
in /Users/nroth/workspace/self-hosted-agents. Work through the linked goals in
order, starting with the first incomplete child goal. Goals 001 through 003 have
accepted evidence; Goals 004 and 005 have accepted evidence; the next ordered goal is Goal 006. For each child goal, create or update the focused
spec/tasks/backlog, then implement one Beads ticket at a time with validation
evidence before moving to the next child goal.
```
