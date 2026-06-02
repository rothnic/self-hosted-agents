# Goal 000: Self-Hosted Agent System Roadmap

## Objective

Execute the self-hosted agent system roadmap in order.

This is the short parent goal for a long-running `/goal` session. It exists only to route work through the ordered
child goals below; each child goal owns its own specs, tasks, Beads backlog, evidence, and review gates.

## Ordered Goals

1. [Self-Hosted Observability And Evaluation Control Plane](001-self-hosted-observability-evaluation-control-plane.md)
   - Accepted. Proved product-grade, self-hosted LLM traces and evaluation evidence.
2. [Durable Agent Execution Runtime](002-durable-agent-execution-runtime.md)
   - Accepted. Proved retry, resume, human wait, and side-effect safety.
3. [Autonomous Multi-Agent Delivery Loop](003-autonomous-multi-agent-delivery-loop.md)
   - Accepted. Made scheduled PM, orchestrator, worker, integrator, and health roles reliable.
4. [Candidate Platform Decision And Product Baseline](004-candidate-platform-decision-product-baseline.md)
   - Recommended next. Choose the primary stack and define the first product workflow.
5. [Self-Hosted Deployment And Operations Reference](005-self-hosted-deployment-operations-reference.md)
   - Prove the selected stack can run on controlled infrastructure.
6. [Operator Workbench And Review UX](006-operator-workbench-review-ux.md)
   - Give the human a self-hosted interface for review, approval, and steering.

## Completion Standard

This goal is complete only when all ordered child goals are complete, reviewed, and backed by durable evidence. Do not
close this parent goal after only one child goal.

For each child goal, one agent presents durable evidence and an independent reviewer agent records acceptance or
rejection. Do not block progress solely because human review might be useful; escalate to the human only when a decision
is explicitly reserved, missing, or contradicted by the evidence.

## Kickoff Prompt

```text
/goal Execute docs/goals/000-self-hosted-agent-system-roadmap.md
in /Users/nroth/workspace/self-hosted-agents. Work through the linked goals in
order, starting with the first incomplete child goal. Goals 001 through 003 have
accepted evidence; the next ordered goal is Goal 004. For each child goal, create or update the focused
spec/tasks/backlog, then implement one Beads ticket at a time with validation
evidence before moving to the next child goal.
```
