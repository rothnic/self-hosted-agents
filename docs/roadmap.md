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

Likely additional Python-first candidates should be researched before creation, such as a Pydantic AI or custom
FastAPI/OpenTelemetry app if they map better to the requirement matrix.

### Phase 4: Evidence Review

After each implementation slice, agents update the comparison matrix with actual evidence:

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

Start with Phase 1 and Phase 2: define the requirement matrix and shared comparison harness before building the first
product slice. Then implement the Python-first candidate first, while keeping a second candidate available for contrast.
