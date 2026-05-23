# CEO Roadmap Review - 2026-05-23

## Executive Snapshot

Where we are: `main` was refreshed after PR #7, Phase 3 is reviewed, and the Phase 6 implementation backlog is synced.
`uv run awf increment-status --json` now reports the active Phase 6 increment with ready worker tickets and
`review_status=executing`.

Why it matters: the comparison roadmap has moved beyond planning. LangGraph Python now has preliminary runnable fixture
evidence, Pydantic AI plus Logfire/OpenTelemetry has current research evidence, and the next implementation backlog is
approved without declaring a final platform winner.

Current repo state: `specs/002-solution-comparison-roadmap/tasks.md` has T001-T018 complete and Phase 6 tasks T019-T026
open. Beads has the Phase 3 increment epic `awf-ztz` closed, Phase 6 increment epic `awf-ftu` open, and eight ready
worker tickets for the approved Pydantic AI plus Logfire/OpenTelemetry and durable execution backlog.

Work in progress: the next implementation backlog is approved and synced, but no new candidate app has been scaffolded
in this review task. Do not declare a final platform winner.

## Agent Assessment

Objective: build an environment-agnostic operating system for coding agents, then compare self-hostable agent stacks
against real implementation evidence.

What the agent checked:

- `objectives/current.md`
- `specs/002-solution-comparison-roadmap/spec.md`
- `specs/002-solution-comparison-roadmap/plan.md`
- `specs/002-solution-comparison-roadmap/tasks.md`
- `docs/requirements-matrix.md`
- `docs/comparison-evidence.md`
- `docs/roadmap.md`
- `docs/research/pydantic-ai-logfire-functional-needs-2026-05-23.md`
- `.agent-runs/increments/002-solution-comparison-roadmap-phase-3.json`
- `.agent-runs/increments/002-solution-comparison-roadmap-phase-6.json`
- Beads issues `awf-ztz`, `awf-ftu`, `awf-pdz`, `awf-hqu`, and Phase 6 task tickets T019-T026

What changed recently:

- T017 recorded preliminary LangGraph Python evidence from a deterministic fixture run, local OTel-style trace export,
  deterministic evaluation artifact, setup notes, and explicit promotion gaps.
- T018 recorded Pydantic AI plus Logfire/OpenTelemetry research against the functional needs map using current primary
  sources.
- The final T018 closure also fixed a terminal-increment workflow fixture edge case so worker dry-runs route to
  integrator review when no worker work remains.
- The requirements matrix now distinguishes implementation evidence for LangGraph from research-only evidence for
  Pydantic AI.
- Human direction was recorded: hosted observability is part of the tested stack, durable execution is required before
  final promotion, and Phase 6 should evaluate Pydantic AI durable paths plus Hatchet, Temporal, DBOS, Prefect, and
  Restate.
- Phase 6 tasks T019-T026 were synced into Beads and grouped under increment epic `awf-ftu`.

Blockers or risks:

- LangGraph Python is still preliminary evidence. It has not proven hosted or self-hosted Langfuse ingestion, real
  model/tool spans, dataset or judge evals, durable execution, persistence, deployment topology, or recovery.
- Pydantic AI plus Logfire/OpenTelemetry is the approved follow-on candidate, but it has not run the shared comparable
  workflow in this repo.
- Logfire hosting posture and the quality of a generic local OTel backend remain unproven.
- Durable execution must be evaluated carefully to avoid selecting a runtime that adds too much operator complexity.

Research or context needed: no more broad research is needed before T019. Future implementation tickets should gather
specific evidence for hosted Logfire, repo-local trace exports, Pydantic Evals, durable execution behavior, and
operator burden.

## Recommendation

Recommended path: execute Pydantic AI plus Logfire/OpenTelemetry as the next Python-first implementation slice, while
keeping LangGraph Python as the first evidence baseline and Mastra TypeScript as a deferred contrast lane.

Reason: this is the strongest way to test whether typed Python ergonomics, code-first evals, OpenTelemetry portability,
and documented durable execution integrations address the explicit gaps left by the LangGraph fixture slice. This is a
next-slice recommendation only, not a platform winner.

Agent will do next: leave implementation for a separate implementer session, starting with T019 / Beads `awf-hrm`.

Human decision recorded on 2026-05-23: approve the Pydantic AI plus Logfire/OpenTelemetry path as the next
implementation backlog. Hosted observability is required evidence for the full stack. Durable execution is required for
final solutions and must be evaluated before selecting a runtime. The resulting Phase 6 backlog is now synced to Beads.

## Options

1. Selected: Pydantic AI plus Logfire/OpenTelemetry next.
   Effect: tests the strongest Python follow-on candidate against the same contract without declaring a final winner.

2. Deepen LangGraph Python plus Langfuse before adding another candidate.
   Effect: closes real Langfuse ingestion, real model/tool span, and richer eval gaps before comparison breadth grows.

3. Build Mastra TypeScript as the next contrast slice.
   Effect: creates cross-language evidence sooner, but spends the next implementation phase away from the Python-first
   preference.

4. Pause app implementation for local observability substrate research.
   Effect: selects or rejects a default local OTel/Logfire/Phoenix/MLflow review path before any new app lane, but
   delays candidate implementation evidence.

## Questions To Answer

1. Answered: Pydantic AI plus Logfire/OpenTelemetry is approved as the next implementation backlog.
2. Answered: hosted observability is required as part of the stack being tested, not optional-only evidence.
3. Answered: durable execution is required for each final solution; the next phase must evaluate options first.

## Measurable Next-Phase Acceptance Criteria

The approved backlog should be complete only when:

- Spec Kit tasks define the Pydantic AI implementation slice, its non-goals, and its evidence contract.
- Beads tickets are synced from approved Spec Kit tasks and show no duplicate or unsynced implementation work.
- A future `apps/pydantic-ai/` candidate runs the shared comparable-agent workflow without hosted credentials.
- The candidate emits repo-local run, OTel trace export, and evaluation artifacts tied by stable ids.
- The candidate also proves hosted Logfire observability as part of the stack, including setup and credential handling.
- The backlog compares framework-specific Pydantic AI durable execution options first: DBOS, Prefect, Restate, and
  Temporal.
- The backlog compares Hatchet as the primary Python workflow-platform option against Temporal, DBOS, Prefect, and
  Restate.
- The durable option evaluation ranks easy startup, understandable recovery behavior, hosted observability correlation,
  low operator complexity, and scale path.
- Gap notes explicitly cover Logfire self-hosting posture, OTel GenAI semantic-convention stability, durable runtime
  choice, and custom critical infrastructure risk.
- `docs/requirements-matrix.md` records implementation scores and gaps only after runnable evidence exists.
- `uv run awf workflow-fixture-test`, `uv run awf workflow-state-lint --json`, `uv run awf repo-hygiene`,
  `uv run awf verify --profile increment --json`, and `git diff --check` pass before closure.

## Decision Gate

Human direction has been recorded for backlog creation. Do not scaffold a new candidate app or declare a final platform
winner in this review task; implementation belongs to the synced Phase 6 Beads tickets.

## Meta-Process

Learning follow-up: keep implementation evidence and research evidence visually separate in the matrix.

Automation opportunity: default `awf` increment commands now route to Phase 6; use explicit `--phase "Phase 3"` only
when reviewing the completed prior increment.

Risk to watch: a successful second Python slice may still not answer cross-language tradeoffs; keep Mastra available as
a deliberate contrast, not a default next step.

New-session recommendation: start a new implementation session for ready ticket `awf-hrm` / T019.
