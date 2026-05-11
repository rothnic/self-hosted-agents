# Requirements Matrix

Date: 2026-05-10

## Purpose

Map the project owner's high-level needs into candidate implementation paths. This matrix should change as prototypes
reveal hidden constraints, integration gaps, or better preferences.

Use `docs/evaluation-criteria.md` as the scoring rubric and `docs/comparison-evidence.md` as the required evidence
checklist before promoting any candidate beyond research or a first implementation slice.

## Target User

The first user is the project owner as an engineer. The working assumptions are:

- Python is preferred for the main engineering workflow.
- Self-hosted LangSmith cannot be assumed because budget or approval may be unavailable.
- The project needs a well-founded comparison tied to actual tested implementations.
- Requirements are incomplete and should be refined through implementation evidence.
- Agents should drive research, implementation, evidence capture, and roadmap updates.

## Requirement Areas

| ID | Requirement | Why It Matters | Evidence Needed |
| --- | --- | --- | --- |
| R1 | Python-first development path | The primary user wants an engineer-friendly Python workflow | Runnable Python app and test loop |
| R2 | Local or self-hostable observability | Hosted-only observability is not acceptable as the default | Local trace UI or exportable traces |
| R3 | Evaluation and regression support | Agent behavior must improve without relying on hidden judgment | Repeatable eval outputs tied to runs |
| R4 | Inspectable orchestration | Multi-step agent behavior must be debuggable | Step/state traces and failure context |
| R5 | Shared comparison harness | Candidate comparison must be fair and implementation-grounded | Same contracts run against each app |
| R6 | Low operator burden | One engineer should be able to run and maintain the system | Documented setup and service count |
| R7 | Scalable architecture path | The chosen approach should grow beyond a toy demo | Clear path to durable services |
| R8 | Roadmap learning loop | Requirements should evolve as prototypes reveal issues | Review notes update specs and backlog |
| R9 | Low custom critical infrastructure | Avoid rebuilding platform capabilities mature tools normally provide | Platform capabilities are provided or intentionally owned |

## Candidate Solution Paths

| Candidate | Fit Today | Primary Evidence To Gather | Current Risk |
| --- | --- | --- | --- |
| LangGraph Python plus Langfuse | Strong Python orchestration plus self-hostable LLM observability | Trace quality, eval workflow, setup effort | Integration depth must be proven |
| LangGraph Python plus Phoenix | Strong Python and OpenInference-style observability path | Local tracing, eval quality, app instrumentation | Deferred until dev experience is better understood |
| Python app plus MLflow tracing | Strong Python lifecycle and broader experiment tracking | Trace/eval ergonomics for agent workflows | Less specialized LLM observability UX |
| Mastra TypeScript plus shared contracts | Useful contrast with a TypeScript-native agent framework | Cross-language cost and feature parity | Lower fit with Python preference |
| LangSmith baseline | Best-known LangChain/LangGraph comparison point | Feature expectations and integration baseline | Self-hosted access may require Enterprise |

## Requirement To Candidate Matrix

Legend: `High` means likely strong fit; `Medium` means plausible but needs proof; `Low` means weak fit or non-primary.

| Requirement | LangGraph + Langfuse | LangGraph + Phoenix | Python + MLflow | Mastra TS | LangSmith Baseline |
| --- | --- | --- | --- | --- | --- |
| R1 Python-first path | High | High | High | Low | High |
| R2 Local/self-hostable observability | High | High | Medium | Medium | Low for this project |
| R3 Evaluation/regression support | Medium | High | Medium | Medium | High |
| R4 Inspectable orchestration | High | High | Medium | Medium | High |
| R5 Shared comparison harness | High | High | High | High | Medium |
| R6 Low operator burden | Medium | Medium | Medium | Medium | Low for self-hosted |
| R7 Scalable architecture path | Medium | Medium | Medium | Medium | High |
| R8 Roadmap learning loop | High | High | High | High | Medium |
| R9 Low custom critical infrastructure | Medium | Medium | Medium | Medium | High if approved |

## Initial Recommendation

Start by comparing Python-first options before investing deeply in TypeScript or a hosted-first baseline.

Recommended first implementation slice:

1. Define one shared agent workflow contract.
2. Implement it in `apps/langgraph-python/`.
3. Instrument it with one local/self-hostable observability path.
4. Capture setup effort, trace quality, eval support, and gaps in this matrix.

Recommended first observability comparison:

1. Start with Langfuse integration depth for LangGraph Python.
2. Keep Phoenix deferred until developer experience is better understood.
3. Keep MLflow tracing as a second Python option if lifecycle/evaluation needs dominate.

## Roadmap Review Questions

These questions should be asked during the next CEO-level roadmap review:

1. Should the first prototype optimize for fastest local demo or best long-term observability architecture?
2. Is LangGraph Python the right first orchestration candidate, or should a simpler Python app establish the harness?
3. What evidence would justify reopening Phoenix as an immediate observability implementation?
4. What minimum demo would convince us the comparison is producing useful evidence?

## Update Rules

- Add evidence only after an implementation or research task produces it.
- Do not mark a candidate as preferred without trace, evaluation, setup, infrastructure ownership, and demo evidence.
- Score candidates against `docs/evaluation-criteria.md`; custom critical infrastructure warnings require roadmap review.
- When implementation exposes a new requirement, update this matrix before creating deeper implementation tickets.
- Roadmap decisions should update this file, the active spec, and Beads tickets together.

## First Python-First Candidate Slice Proposal (T007)

### Proposal Governance (to prevent state drift)

- **Proposal status**: `draft` (planning artifact only; not an approved roadmap decision).
- **Approval gate**: decision must be recorded through T010/T011 before any spec task is marked complete.
- **Backlog alignment rule**: keep `tasks.md`, Beads status, and this matrix in sync in the same change.

### Candidate

- **Name**: `langgraph-python-langfuse-slice-01`
- **App location**: `apps/langgraph-python/`
- **Why first**: Highest immediate fit for R1/R2/R4 while preserving a clean path for shared comparison contracts.

### Slice Scope

1. Build a minimal runnable agent workflow that satisfies the shared comparable workflow contract under `tests/workflow/features/comparable_agent_workflow.feature`.
2. Instrument traces through a local/self-hostable Langfuse path and persist artifacts required by `docs/comparison-evidence.md`.
3. Provide one local run command and one verification command that can be reused by later candidate apps.

### Explicit Non-Goals For This Slice

- No multi-agent orchestration depth beyond the minimum contract flow.
- No production deployment topology or scale tuning.
- No cross-candidate scoring update until evidence artifacts are recorded from a successful run.

### Exit Evidence For T007

- A proposed app path and contract target are documented (this section).
- The candidate is traceable back to requirement matrix priorities (R1, R2, R4, R5).
- Follow-on tasks can implement the second candidate (T008) and minimum demo definition (T009) without reopening selection ambiguity.


### Required Completion Checklist (before closing T007)

- [ ] Proposal approved during roadmap review (T010) and captured as a human decision (T011).
- [ ] Matching Beads issue state reflects completion evidence for the same task id.
- [ ] Shared-contract acceptance and evidence location are unchanged or explicitly updated together.
