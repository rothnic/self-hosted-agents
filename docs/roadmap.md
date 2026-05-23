# Roadmap

## Current Focus

The workflow foundation is approved. The next focus is requirements-driven solution comparison for a self-hosted agent
system.

Target user: the project owner as an engineer who prefers Python, needs practical local/self-hosted agent workflows, and
cannot assume access to approved self-hosted LangSmith.

## Operating Model

Agents own workflow commands, research, decomposition, tickets, and implementation evidence. The human operates at the
roadmap and approval level:

1. The human states goals, constraints, and tradeoffs.
2. Agents translate current repo state into a short decision brief.
3. Agents research unclear solution areas before asking for decisions.
4. The human answers targeted questions or approves a recommended path.
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

The active Python-first follow-on lane is Pydantic AI plus Logfire/OpenTelemetry. LlamaIndex remains a strong fallback
if data/RAG workflows become the dominant functional area.

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

## Current Recommendation

Latest CEO-level review: `docs/roadmap-review-2026-05-23.md`.

Phase 3 is reviewed and Phase 6 is the active implementation increment. `apps/langgraph-python/` using LangGraph
Python plus Langfuse has preliminary deterministic fixture evidence, and Pydantic AI plus Logfire/OpenTelemetry is the
approved next implementation lane. Neither path is a final platform winner.

Approved next direction: execute the Pydantic AI plus Logfire/OpenTelemetry implementation backlog while keeping
LangGraph Python as the first evidence baseline and Mastra TypeScript as a deferred contrast lane. Hosted observability
is part of the stack being tested, not optional-only evidence.

Durable execution is required for final solutions. The next phase should evaluate framework-specific Pydantic AI
options first, then compare Hatchet as the primary Python workflow-platform option against Temporal, DBOS, Prefect, and
Restate. The runtime decision should favor easy startup, understandable recovery behavior, low operating complexity, and
a credible scale path.

The proposed contrast candidate is `apps/mastra-ts/` using Mastra TypeScript plus the same shared comparison contract.
It should test whether framework-integrated TypeScript workflow and observability capabilities offset the language and
maintenance cost for a Python-preferring owner.

The minimum comparable demo is defined in `docs/comparison-evidence.md`. Candidate apps should implement that same
decision-ready workflow before roadmap review compares platform quality.

The active next tickets are Phase 6 tasks T019-T026. Start with T019 / Beads `awf-hrm`, then use the remaining tickets
to scaffold the Pydantic AI lane, prove hosted Logfire and repo-local trace evidence, capture Pydantic Evals output,
compare durable execution options, add a lowest-complexity durable smoke path, and update the matrix with implementation
evidence.
