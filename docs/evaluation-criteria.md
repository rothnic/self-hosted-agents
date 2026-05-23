# Evaluation Criteria

Date: 2026-05-10

## Purpose

This rubric defines how candidate agent application stacks are compared before the project chooses a deeper
implementation path. It complements `docs/requirements-matrix.md` and `docs/comparison-evidence.md` by turning
high-level needs into evidence that can be checked against runnable apps.

Do not use this rubric to declare a final winner from research alone. A candidate should only be promoted after it has
implementation evidence from a runnable app, shared contracts, traces, evaluations, and setup notes.
Final-solution promotion also requires hosted observability exercised as part of the candidate stack and durable
execution proof. Repo-local artifacts remain required for repeatable validation, but they are not enough by themselves
for final-solution acceptance.

## Scoring Scale

Use a qualitative 1-4 score for each criterion.

| Score | Meaning | Decision Use |
| --- | --- | --- |
| 1 | Poor fit | Do not choose unless there is a strong strategic reason |
| 2 | Risky or incomplete fit | Keep as fallback or research-only option |
| 3 | Viable fit with known tradeoffs | Candidate can proceed if gaps are acceptable |
| 4 | Strong fit | Candidate is ready for deeper implementation comparison |

If a candidate requires custom critical infrastructure, cap the affected criterion at `2` unless the roadmap explicitly
decides that owning that infrastructure is strategically necessary.

For final-solution review, cap Observability at `2` when hosted observability has not been exercised by the candidate
app and linked to the same run evidence reviewers inspect. Cap Durable Execution and Scalability at `2` when retry,
resume, human wait, and side-effect behavior are not proven through a selected or explicitly evaluated durable runtime.
These caps do not block research or first-slice implementation work; they mean the candidate is not final-solution
ready.

## Criteria

### Technical Scope And Infrastructure Ownership

Evaluate whether the stack provides expected critical capabilities without forcing us to build cloud-service-grade
infrastructure ourselves.

Strong evidence:

- Mature platform support for tracing, evals, storage, dashboards, scheduling, auth boundaries, and operational
  workflows.

Warning conditions:

- We must implement our own observability backend, eval store, scheduler, durable queue, dashboard, trace UI, or other
  complex critical component.

### Observability

Evaluate whether hosted observability and local or exportable traces make agent behavior inspectable. Hosted
observability is part of the full stack under evaluation, while repo-local artifacts keep validation repeatable.

Strong evidence:

- Readable hosted traces for model calls, tools, retrieval, state transitions, inputs, outputs, latency, tokens, costs,
  and failures.
- Hosted trace evidence produced by the candidate app as part of the tested stack, correlated to the run artifact,
  evaluation output, and candidate revision.
- Repo-local trace exports that let agents validate behavior without hosted credentials.

Warning conditions:

- Traces are incomplete, hard to correlate, local-only, hosted-only without portable exports, or require extensive
  custom instrumentation.
- Hosted observability remains a planned integration, disconnected sample, screenshot, or framework claim instead of
  stack evidence from the tested candidate.

### Evaluation

Evaluate whether agent behavior can be evaluated repeatably and tied back to concrete runs.

Strong evidence:

- Repeatable evals, scores or annotations attached to traces, dataset or prompt workflow support, and
  regression-friendly outputs.

Warning conditions:

- Evaluation is mostly manual, detached from traces, hard to rerun, or hidden in ad hoc scripts.

### Scalability

Evaluate whether the candidate has a plausible path from local demo to durable self-hosted operation.

Strong evidence:

- Clear service topology, storage model, export path, deployment story, and known growth constraints.

Warning conditions:

- Scaling requires undefined architecture, custom persistence, custom workers, or unproven operational glue.

### Durable Execution

Evaluate whether the candidate can recover or resume long-running agent workflows without duplicated side effects.

Strong evidence:

- A durable runtime captures model calls, tool calls, human waits, retries, and recovery state with understandable
  semantics.
- The runtime is easy for one engineer to start locally, inspect, and scale when the workload grows.

Warning conditions:

- Durable execution is deferred, simulated only, tied to a runtime that is too complex to operate, or requires custom
  retry/state infrastructure owned by this project.
- Durable execution is described as future work while the candidate is being considered for final-solution language.

### Operating Effort

Evaluate whether one engineer can run and maintain the stack without excessive burden.

Strong evidence:

- Simple bootstrap, documented services, manageable secrets, low service count, and clear failure recovery.

Warning conditions:

- Setup is fragile, service count is high, upgrades are unclear, or normal operation needs constant manual care.

## Custom Critical Infrastructure Rule

The project should avoid becoming the maintainer of infrastructure that mature cloud or platform products normally
provide. Self-hosting is acceptable when the chosen tool already provides the core product behavior and the project only
owns deployment and configuration.

Score a candidate poorly when it pushes us toward building or maintaining any of these ourselves:

- Trace ingestion, storage, search, and visualization.
- Evaluation dataset management, scoring history, and regression reporting.
- Durable job queues, schedulers, workers, retries, and run state.
- Operator dashboards for routine debugging and review.
- Cross-run evidence stores needed for roadmap decisions.
- Security, access control, or secret-management surfaces beyond local development needs.

Exceptions require an explicit roadmap decision that the custom component is part of the product strategy, not just a
gap created by the candidate stack.

## How To Use This Rubric

For each candidate implementation slice:

1. Run the same shared behavior contract.
2. Capture the evidence groups defined in `docs/comparison-evidence.md`.
3. Score each criterion from 1-4 and record the evidence behind the score.
4. Update `docs/requirements-matrix.md` only after implementation or bounded research changes the evidence.
5. Apply the final-solution caps before using final-solution language for any candidate.
6. Bring any score of `1` or any custom critical infrastructure warning to the next CEO-level roadmap review.

The first comparison should favor candidates that minimize custom infrastructure while still meeting the system's
expected needs for local development, self-hostable evidence, and later durable operation.
