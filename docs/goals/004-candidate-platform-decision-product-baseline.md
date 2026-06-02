# Goal 004: Candidate Platform Decision And Product Baseline

## Objective

Use comparable implementation evidence to choose the primary agent application stack and turn it into the first product
baseline for self-hosted agent work.

## Why This Matters

The repo should not keep comparing frameworks indefinitely. Once observability, evaluation, durable execution, and
operator burden have enough evidence, the project needs a primary stack and a product baseline to deepen.

## Product Iteration

This goal moves from candidate comparison to platform decision. It keeps non-selected candidates as documented
alternatives, but focuses future implementation on the selected stack.

## Scope

- Complete comparable evidence for LangGraph Python, Pydantic AI, and any needed contrast candidate.
- Score candidates against the same functional needs map.
- Identify the selected primary stack and why it wins.
- Define the first product baseline workflow beyond the comparison demo.
- Keep self-hosted observability, evals, durable execution, and review gates in scope.
- Record explicit reasons rejected candidates are not selected now.

## Task Backlog

1. Audit current evidence for LangGraph Python, Pydantic AI, and Mastra TypeScript.
2. Decide whether Mastra needs a runnable contrast slice before platform selection.
3. Normalize run, trace, eval, setup, and durable evidence across candidates.
4. Update the functional needs map with implementation evidence only.
5. Score infrastructure ownership, observability, evaluation, scalability, and operating effort.
6. Run a CEO-level roadmap review with recommendation and options.
7. Record the platform decision in objective, spec, matrix, and Beads with independent reviewer acceptance.
8. Define the first product baseline workflow for the selected stack.
9. Convert comparison-only code into a product-oriented app boundary.
10. Add product-level BDD contracts for the baseline workflow.
11. Add setup and operating docs for the selected stack.
12. Archive or freeze non-selected candidates as comparison references.
13. Add migration notes for useful code or fixtures from non-selected lanes.
14. Update automation loops to prefer the selected stack for product work.
15. Create follow-up goals for UI, deployment, and production hardening.

## Definition Of Done

- The repo has a recorded platform decision accepted by an independent reviewer agent.
- The selected stack has comparable evidence across run, trace, eval, setup, and durability.
- The first product baseline workflow is defined with BDD contracts and acceptance checks.
- Rejected or deferred candidates have explicit evidence-based reasons.
- Future implementation no longer has to re-litigate the framework choice.

## Proof Commands

```bash
uv run awf workflow-fixture-test
uv run awf verify --profile increment --json
uv run awf review-gate
uv run awf repo-hygiene
uv run awf workflow-state-lint --json
```

## Review Blocking Criteria

- The decision is based on docs or preference rather than implementation evidence.
- Observability, evals, or durable execution remain unproven for the selected stack.
- The product baseline is just the comparison demo renamed.
- Non-selected candidates are discarded without recorded tradeoffs.

## Kickoff Prompt

```text
/goal Execute docs/goals/004-candidate-platform-decision-product-baseline.md
in /Users/nroth/workspace/self-hosted-agents. Complete the candidate evidence
needed for an independently reviewed platform decision, update the comparison matrix, record the
selected primary stack, and define the first product baseline workflow with BDD
contracts and validation gates.
```
