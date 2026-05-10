# Comparison Evidence

Date: 2026-05-10

## Purpose

This document defines the minimum evidence every candidate app must produce before the roadmap compares agent stack
quality. It complements `docs/evaluation-criteria.md` by specifying what implementation evidence must exist for traces,
evaluations, setup, and known gaps.

Do not treat research notes or framework claims as implementation evidence. A candidate app only has comparable evidence
after the shared behavior contract runs and the artifacts below can be reviewed from repo state or linked run outputs.

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
- Trace evidence that can be inspected by a reviewer.
- Evaluation evidence tied to the same behavior run.
- Setup and operating notes sufficient for another agent or engineer to rerun the slice.
- Explicit gap notes for missing evidence and custom critical infrastructure risk.

Missing evidence should be recorded as a gap, not silently inferred. The next CEO-level roadmap review should receive
candidate options only after these evidence groups exist or the missing groups are clearly called out.

## Storage Rule

T006 will define exact locations for shared packages, fixtures, and app-local implementation code. Until then, evidence
expectations live here, summarized comparison findings belong in `docs/requirements-matrix.md`, and durable task
evidence belongs in Beads comments or run reports.
