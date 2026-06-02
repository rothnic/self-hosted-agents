# Roadmap

## Current Focus

The workflow foundation is approved. The next focus is requirements-driven solution comparison for a self-hosted agent
system.

Target user: the project owner as an engineer who prefers Python, needs practical local/self-hosted agent workflows, and
cannot assume access to approved self-hosted LangSmith.

## Operating Model

Agents own workflow commands, research, decomposition, tickets, implementation evidence, and independent evidence
review. The human operates at the roadmap and approval level when they explicitly reserve a decision:

1. The human states goals, constraints, and tradeoffs.
2. Agents translate current repo state into a short decision brief.
3. Agents research unclear solution areas before asking for decisions.
4. A presenter agent records evidence and an independent reviewer agent accepts or rejects it.
5. Agents update objectives, specs, tasks, Beads tickets, and comparison artifacts.
6. Implementers build small slices in separate apps and run shared acceptance checks.
7. Reviewers compare demo behavior, observability, scalability, and operating effort.
8. The roadmap is revisited whenever new implementation evidence changes requirements or preferences.

## Roadmap Phases

### Phase 1: Requirements And Solution Map

Capture the high-level system requirements and map them to candidate implementation choices. Requirements are expected
to evolve as implementation reveals hidden constraints.

Maintain a functional needs map as part of the requirements matrix. For each required functional area, name the
solution-space component or components that provide the function, then record significant extra features that should
affect scoring when they are useful and arrive with the solution rather than custom project infrastructure.

Initial requirement areas:

- Python-first engineering workflow.
- Self-hostable or local-first observability and evaluation.
- Traceability from objectives, specs, tickets, code, tests, and run evidence.
- Multi-agent or workflow orchestration that can be inspected and debugged.
- Scalable enough to grow from local demos to durable services.
- Low operating burden for one engineer.
- Comparable demos across candidate solutions.

### Phase 2: Shared Comparison Harness

Define common behavior contracts, fixtures, trace expectations, evaluation outputs, and demo scenarios. Shared assets
belong in `packages/` or `tests/`; app internals stay isolated. Candidate evidence expectations are defined in
`docs/comparison-evidence.md`.

### Phase 3: Candidate Implementations

Each candidate solution gets a separate runnable app under `apps/`. Existing app lanes:

- `apps/langgraph-python/`: Python LangGraph/LangChain candidate.
- `apps/mastra-ts/`: TypeScript Mastra candidate used as a cross-language comparison point.

The active Python-first follow-on lane is Pydantic AI plus self-hosted Langfuse/OpenTelemetry, Pydantic Evals, and DBOS
smoke evidence. LlamaIndex remains a strong fallback if data/RAG workflows become the dominant functional area.

### Phase 4: Evidence Review

After each implementation slice, agents update the comparison matrix with actual evidence:

- Functional needs coverage and the solution components providing each function.
- Feature coverage.
- Observability and evaluation quality.
- Integration effort.
- Scalability path.
- Local/self-hosted operating burden.
- Gaps found during implementation.

### Phase 5: Roadmap Review

A roadmap review can be initiated by asking for a roadmap review or next CEO-level plan. The PM steward should inspect
repo state, research any new solution-space questions, and return:

- Current status.
- What changed since the last review.
- Recommended next direction.
- Options and tradeoffs.
- Targeted questions for the human.
- Required updates to objectives, specs, tasks, tickets, and comparison artifacts.

## Long-Horizon Goal Backlog

Major product iterations live in `docs/goals/`. These are the forward-looking goals to use when the project needs a
long-running `/goal` session rather than one small Beads ticket.

Current goal backlog:

0. `docs/goals/000-self-hosted-agent-system-roadmap.md`
1. `docs/goals/001-self-hosted-observability-evaluation-control-plane.md`
2. `docs/goals/002-durable-agent-execution-runtime.md`
3. `docs/goals/003-autonomous-multi-agent-delivery-loop.md`
4. `docs/goals/004-candidate-platform-decision-product-baseline.md`
5. `docs/goals/005-self-hosted-deployment-operations-reference.md`
6. `docs/goals/006-operator-workbench-review-ux.md`

Start with Goal 001 unless the human explicitly prioritizes durable execution, automation, deployment, or operator UX.
Goal documents are planning backlogs, not executable worker queues. A selected goal should be decomposed into a focused
spec, tasks, and Beads tickets before implementation.

## Current Recommendation

Latest CEO-level review: `docs/roadmap-review-2026-05-31.md`.

Phase 6 is implementation-complete and independently reviewed. `apps/pydantic-ai/` now has tested evidence for
self-hosted-compatible observability, Pydantic Evals, DBOS durable behavior, and requirements-matrix scoring. Neither
Pydantic AI nor DBOS is a final platform winner.

Accepted next direction: Goal 001 is complete for the current roadmap increment, and Goal 002 is the active durable
execution goal. Goal 001 has the required self-hosted Langfuse proof, repo-local trace fallback, Pydantic Evals output,
fixture-safe service-unavailable behavior, setup docs, and matrix scoring.

Goal 002 local DBOS proof is complete through T010. The committed durable artifact proves controlled retry, process
resume with stable identity, side-effect idempotency, review wait without acceptance, accepted-review continuation, and
correlation across durable run, Pydantic AI run, trace, eval, reviewer, Beads, spec, and task ids. The remaining Goal 002
closeout work is to record independent reviewer acceptance and follow-up tickets for production storage, worker
topology, queue behavior, backup/restore, retention, and recovery rehearsal.

Goal 001 follow-up Beads epics are recorded for the remaining non-blocking gaps: `awf-eas` for Langfuse production
operations, `awf-2du` for richer Langfuse evaluation workflows, and `awf-4t2` for Phoenix or Opik fallback comparison if
Langfuse becomes too heavy.

Alternative directions are documented in the latest review: deepen Langfuse operations before Goal 002, compare Phoenix
or Opik before accepting Langfuse, or reopen candidate comparison before durable runtime work.

The minimum comparable demo is defined in `docs/comparison-evidence.md`. Candidate apps should continue to implement
that same decision-ready workflow before roadmap review compares platform quality.

There are no remaining Phase 6 worker tickets. Independent review accepted Goal 001 evidence in
`.agent-runs/reports/goal-001-evidence-review-20260601.md`. Goal 002 has a focused Spec Kit feature and Beads backlog;
workers should continue from `uv run awf ready-work` rather than selecting isolated roadmap tasks.
