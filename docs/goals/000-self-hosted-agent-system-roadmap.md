# Goal 000: Self-Hosted Agent System Roadmap

## Objective

Build a complete self-hosted agent operating system by executing the linked product goals in order.

This is the parent goal. Use it as the single long-running `/goal` target when the work should advance the full
roadmap instead of one focused product iteration.

## Ordered Goals

1. [Self-Hosted Observability And Evaluation Control Plane](001-self-hosted-observability-evaluation-control-plane.md)
   - Prove product-grade, self-hosted LLM traces and evaluation evidence.
2. [Durable Agent Execution Runtime](002-durable-agent-execution-runtime.md)
   - Prove retry, resume, human wait, and side-effect safety.
3. [Autonomous Multi-Agent Delivery Loop](003-autonomous-multi-agent-delivery-loop.md)
   - Make scheduled PM, orchestrator, worker, integrator, and health roles reliable.
4. [Candidate Platform Decision And Product Baseline](004-candidate-platform-decision-product-baseline.md)
   - Choose the primary stack and define the first product workflow.
5. [Self-Hosted Deployment And Operations Reference](005-self-hosted-deployment-operations-reference.md)
   - Prove the selected stack can run on controlled infrastructure.
6. [Operator Workbench And Review UX](006-operator-workbench-review-ux.md)
   - Give the human a self-hosted interface for review, approval, and steering.

## Completion Standard

This umbrella goal is complete only when every linked goal has its own proof evidence, review outcome, and follow-up
backlog. Do not close it after completing only one child goal.

## Kickoff Prompt

```text
/goal Execute docs/goals/000-self-hosted-agent-system-roadmap.md
in /Users/nroth/workspace/self-hosted-agents. Work through the linked goals in
order, starting with Goal 001. For each child goal, create or update the focused
spec/tasks/backlog, then implement one Beads ticket at a time with validation
evidence before moving to the next child goal.
```
