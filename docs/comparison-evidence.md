# Comparison Evidence

Date: 2026-05-10

## Purpose

This document defines the minimum evidence every candidate app must produce before the roadmap compares agent stack
quality. It complements `docs/evaluation-criteria.md` by specifying what implementation evidence must exist for traces,
evaluations, setup, and known gaps.

Do not treat research notes or framework claims as implementation evidence. A candidate app only has comparable evidence
after the shared behavior contract runs and the artifacts below can be reviewed from repo state or linked run outputs.

## Minimum Comparable Demo

The minimum demo for candidate comparison is a single decision-ready agent workflow implemented by each candidate app.
It is intentionally smaller than a product prototype and must stay comparable across stacks.

The demo scenario is the shared behavior contract in
`tests/workflow/features/comparable_agent_workflow.feature`: a project owner acting as an engineer provides a product
objective, constraints, and project context, then receives a recommended next implementation slice.

Each candidate demo must accept the same input categories:

- product objective or roadmap goal;
- constraints such as language preference, hosting limits, observability needs, and approval gates;
- current project context such as active spec, ready work, and existing comparison evidence;
- candidate app id and stack under evaluation.

Each candidate demo must return the same output categories:

- recommended next implementation slice;
- alternatives and tradeoffs;
- explicit human questions when direction is not safe to assume;
- acceptance check for the proposed work;
- links or paths to run, trace, evaluation, setup, and gap evidence.

Minimum evidence for a comparable demo run:

- one runnable command for the candidate demo;
- one shared behavior-contract or fixture check proving the scenario;
- one trace or trace export that makes the workflow inspectable;
- one evaluation result tied to the same run;
- setup and operating notes sufficient for another agent to rerun the demo;
- gap notes for missing trace, evaluation, scalability, or operating evidence.

The minimum demo does not include a production deployment, user-facing UI, multi-agent scheduling, durable background
workers, a full observability cluster, or a final platform recommendation. Those are follow-up work after the roadmap
review compares implementation evidence.

## Full-Solution Evidence

The minimum demo can be fixture-backed, but final solution promotion requires more evidence:

- Hosted observability must be exercised as part of the candidate stack, including trace visibility for model calls,
  tool calls, state transitions, failures, tokens or cost where available, and correlation back to run artifacts.
- Durable execution must be proven for the final solution, including retry, resume, human wait, and side-effect
  behavior. The durable runtime should be selected through evidence rather than assumed.
- Local or repo-exported artifacts remain required so agents can validate behavior without hidden hosted state.

## Required Evidence

Each candidate implementation slice must produce these evidence groups.

### Run Artifact

Capture a concise record of the candidate run:

- Candidate app id and stack under evaluation.
- Shared behavior contract or demo scenario exercised.
- Command used to run the candidate and the acceptance check used to verify it.
- Commit or code revision, run timestamp, and pass/fail outcome.
- Links or paths to any traces, eval outputs, logs, screenshots, or generated reports.

### Trace Evidence

Capture enough trace detail to make agent behavior inspectable:

- Trace provider and whether the trace can run locally, self-hosted, or only hosted.
- Trace id, UI link, or export path.
- Coverage for model calls, tool calls, retrieval, state transitions, inputs, outputs, latency, token usage, and failures.
- Correlation from the trace back to the run artifact and candidate app revision.
- Gaps where manual instrumentation, custom storage, or custom visualization would be needed.

### Evaluation Evidence

Capture repeatable evaluation output tied to the same run:

- Evaluation case, dataset, or prompt set used for the candidate.
- Expected behavior or scoring criteria.
- Scorer type, such as deterministic assertion, human annotation, model judge, or product-specific rubric.
- Score, pass/fail result, and reason for failure when applicable.
- Rerun command or process, plus a link back to the trace or run artifact.

### Setup And Operating Evidence

Capture the operating burden for one engineer:

- Setup commands, required services, required environment variables, and secret handling.
- Service count, local startup path, and whether data persists across runs.
- Approximate setup effort and common failure or recovery steps.
- Deployment or self-hosting path if the slice exposes one.
- Custom critical infrastructure warning when the stack pushes trace ingestion, eval storage, dashboards, schedulers,
  workers, queues, or run state back onto this project.

### Gaps And Follow-Up

Capture what the implementation does not prove yet:

- Missing trace or evaluation coverage.
- Reliability, scalability, or operator-experience risks.
- Framework limitations or hosted-only assumptions.
- Follow-up spec tasks or Beads tickets needed before a candidate can be promoted.

## Promotion Gate

A candidate app is not ready for roadmap promotion unless it has:

- A passing shared behavior contract run.
- Hosted trace evidence that can be inspected by a reviewer.
- Repo-local trace and run artifacts that preserve deterministic validation.
- Evaluation evidence tied to the same behavior run.
- Setup and operating notes sufficient for another agent or engineer to rerun the slice.
- Durable execution evidence, or a clear roadmap gate explaining why the candidate is not yet promotable.
- Explicit gap notes for missing evidence and custom critical infrastructure risk.

Missing evidence should be recorded as a gap, not silently inferred. The next CEO-level roadmap review should receive
candidate options only after these evidence groups exist or the missing groups are clearly called out.

## Storage Rule

Exact locations for shared packages, fixtures, and app-local implementation code are defined in
`docs/project-structure.md`. Evidence expectations live here, summarized comparison findings belong in
`docs/requirements-matrix.md`, and durable task evidence belongs in Beads comments or run reports.
