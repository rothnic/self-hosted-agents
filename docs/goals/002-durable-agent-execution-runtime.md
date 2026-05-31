# Goal 002: Durable Agent Execution Runtime

## Objective

Choose and prove the durable execution runtime for long-running self-hosted agent work. The end state is that agent
tasks can retry, resume after crashes, wait for human decisions, and avoid duplicate side effects with evidence another
agent can inspect.

## Why This Matters

The project cannot become a reliable self-hosted agent system if every meaningful job depends on one uninterrupted
chat session or one fragile local process. Durable execution is the boundary between demos and useful automation.

## Product Iteration

This goal turns candidate workflow code into recoverable agent execution. It compares DBOS, Prefect, Restate, Temporal,
and Hatchet against the actual candidate app lane, then implements the lowest-complexity viable runtime.

## Scope

- Compare durable runtime options against the same self-hosted constraints.
- Select one runtime through evidence, not preference.
- Implement a small durable smoke path for the chosen runtime.
- Prove retry, resume, human wait, and side-effect behavior.
- Correlate durable runs with observability and evaluation evidence.
- Document service topology, storage, local startup, and recovery operations.

## Task Backlog

1. Review Pydantic AI durable execution integrations and Hatchet as the workflow-platform alternative.
2. Define the durable smoke scenario with retry, resume, human wait, and side-effect boundaries.
3. Score DBOS, Prefect, Restate, Temporal, and Hatchet against local setup and operator burden.
4. Create a decision note recommending the lowest-complexity viable runtime.
5. Add a focused Spec Kit feature for the selected runtime.
6. Add service setup docs and bootstrap checks for the selected runtime.
7. Implement a durable workflow around the comparable candidate run.
8. Add a controlled failure that proves retry behavior.
9. Add a restart or resume proof that preserves workflow state.
10. Add a human wait proof that stops and resumes without bypassing review gates.
11. Add idempotency or side-effect evidence.
12. Link durable run ids to trace ids, eval ids, and Beads evidence.
13. Add workflow fixture coverage for durable evidence shape.
14. Update requirements scoring and promotion gates.
15. Record follow-up tickets for production hardening, storage, or worker scaling gaps.

## Definition Of Done

- One durable runtime is selected with a recorded comparison basis.
- A runnable smoke path proves retry, resume, human wait, and side-effect behavior.
- Durable run evidence is linked to observability, evals, and repo-local artifacts.
- The service setup can be reproduced by another agent from repo docs.
- Final-solution promotion remains blocked until this evidence exists.

## Current Selection Evidence

T024 selects Pydantic AI plus DBOS as the first durable smoke path for Goal 002. The decision is intentionally scoped to
the next proof, not the final platform. DBOS was selected because the tested Pydantic AI package exposes a native DBOS
module, the first smoke can use local SQLite state, and the proof can run without hosted services or external model
providers. T025 must add the missing DBOS optional dependency before importing `DBOSAgent`.

Evidence to inspect:

- `docs/research/durable-execution-selection-2026-05-31.md`
- `.agent-runs/verifications/verify-durable-options-t024-20260531.json`

Next proof: T025 should implement a DBOS smoke around the existing deterministic Pydantic AI candidate path and prove
retry or resume behavior without duplicating an explicit side-effect-like step.

## Current Smoke Evidence

T025 adds the first DBOS durable smoke for the Pydantic AI lane. It uses a local SQLite DBOS system database, starts a
workflow in one child process, kills that process after a completed DBOS side-effect step, then starts a second child
process against the same DBOS database. The resumed workflow completes through `DBOSAgent` with `TestModel`, records a
Pydantic AI run id and trace id, and proves the side-effect log still contains exactly one event.

Evidence to inspect:

- `.agent-runs/verifications/pydantic-ai-durable-smoke-t025-20260531.json`

## Proof Commands

```bash
uv run awf verify --profile ticket --json
uv run awf verify --profile increment --json
uv run awf workflow-fixture-test
uv run awf repo-hygiene
uv run awf workflow-state-lint --json
```

Add runtime-specific smoke commands after selection.

## Review Blocking Criteria

- The runtime is selected without comparing alternatives.
- Recovery behavior is described but not exercised.
- Human waits can be bypassed by scheduled automation.
- Side effects can duplicate after retry or resume.
- Runtime setup introduces undocumented infrastructure.

## Kickoff Prompt

```text
/goal Execute docs/goals/002-durable-agent-execution-runtime.md
in /Users/nroth/workspace/self-hosted-agents. Compare durable runtime options
against the actual Pydantic AI candidate lane, record the selection basis, then
implement a small durable smoke path proving retry, resume, human wait, and
side-effect behavior with repo-local evidence.
```
