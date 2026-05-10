# Evaluation Criteria

Date: 2026-05-10

## Purpose

This rubric defines how candidate agent application stacks are compared before the project chooses a deeper
implementation path. It complements `docs/requirements-matrix.md` by turning high-level needs into evidence that can be
checked against runnable apps.

Do not use this rubric to declare a final winner from research alone. A candidate should only be promoted after it has
implementation evidence from a runnable app, shared contracts, traces, evaluations, and setup notes.

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

Evaluate whether local or self-hostable tracing makes agent behavior inspectable.

Strong evidence:

- Readable traces for model calls, tools, retrieval, state transitions, inputs, outputs, latency, tokens, and failures.

Warning conditions:

- Traces are incomplete, hard to correlate, hosted-only, or require extensive custom instrumentation.

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
2. Capture traces, evaluation outputs, setup notes, service topology, and maintenance gaps.
3. Score each criterion from 1-4 and record the evidence behind the score.
4. Update `docs/requirements-matrix.md` only after implementation or bounded research changes the evidence.
5. Bring any score of `1` or any custom critical infrastructure warning to the next CEO-level roadmap review.

The first comparison should favor candidates that minimize custom infrastructure while still meeting the system's
expected needs for local development, self-hostable evidence, and later durable operation.
