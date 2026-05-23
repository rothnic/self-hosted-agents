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

## Functional Needs Map

Every candidate must be evaluated against a high-level functional representation of the system needs before scoring
or promotion. A functional area may be provided by one framework feature, an observability product, a separate service,
or a small amount of app-local glue. The comparison should name those provider components explicitly.

| Functional Area | Minimum Need | Provider Mapping Evidence | Extra Features To Score |
| --- | --- | --- | --- |
| Agent orchestration | Represent the workflow as inspectable steps | Framework graph, runtime, or app-local pipeline | Branching, retries, persistence, skills, or approval hooks |
| Tool and context access | Safely call tools over project context | Tool APIs, DI, MCP, retrieval connectors, or typed adapters | Connectors, approval policy, schemas, or capability bundles |
| Observability | Inspect model/tool/state behavior | Langfuse, Logfire, Phoenix, MLflow, OTel, traces, or framework tracing | Cost tracking, failure views, eval dashboards, OTel export, or local UI |
| Evaluation | Rerun and score comparable behavior | Deterministic checks, eval datasets, framework evals, or custom scorer | Regression history, trace-linked scores, judges, or annotation workflows |
| Evidence storage | Preserve run, trace, eval, setup, and gaps | Repo artifacts, observability backend, eval store, or exports | Cross-run comparison UI, searchable evidence, or reports |
| Durable execution | Recover or resume long-running workflows | Persistence, Temporal, DBOS, Prefect, Restate, queues, or local state | Retries, human waits, distributed workers, or hosted workers |
| Operator experience | Keep setup and debugging manageable | Bootstrap scripts, service topology, local UI, documented recovery | Single-command local stack, low service count, or diagnostics |
| Scalability path | Show how the slice becomes a durable service | Deployment target, storage model, runtime model, and boundaries | Microservice deployment, tenancy controls, or supported hosting |

Scoring rule: if a candidate provides significant useful features inside a functional area without adding custom
critical infrastructure, record them as positive scoring evidence. If a candidate requires the project to build a
missing provider component, record that as a custom critical infrastructure warning.

## Candidate Solution Paths

| Candidate | Fit Today | Primary Evidence To Gather | Current Risk |
| --- | --- | --- | --- |
| LangGraph Python plus Langfuse | Strong Python orchestration plus self-hostable LLM observability | Trace quality, eval workflow, setup effort | Integration depth must be proven |
| LangGraph Python plus Phoenix | Strong Python and OpenInference-style observability path | Local tracing, eval quality, app instrumentation | Deferred until dev experience is better understood |
| Python app plus MLflow tracing | Strong Python lifecycle and broader experiment tracking | Trace/eval ergonomics for agent workflows | Less specialized LLM observability UX |
| Pydantic AI plus Logfire/OTel | Python-native typed agents with evals and durability | Typed ergonomics, evals, OTel evidence, runtime fit | Newer framework; fit needs demo proof |
| Mastra TypeScript plus shared contracts | Useful contrast with a TypeScript-native agent framework | Cross-language cost and feature parity | Lower fit with Python preference |
| LangSmith baseline | Best-known LangChain/LangGraph comparison point | Feature expectations and integration baseline | Self-hosted access may require Enterprise |

## Requirement To Candidate Matrix

Legend: `High` means likely strong fit; `Medium` means plausible but needs proof; `Low` means weak fit or non-primary.

| Requirement | LangGraph + Langfuse | LangGraph + Phoenix | Python + MLflow | Pydantic AI + Logfire/OTel | Mastra TS | LangSmith Baseline |
| --- | --- | --- | --- | --- | --- | --- |
| R1 Python-first path | High | High | High | High | Low | High |
| R2 Local/self-hostable observability | High | High | Medium | Medium | Medium | Low for this project |
| R3 Evaluation/regression support | Medium | High | Medium | High | Medium | High |
| R4 Inspectable orchestration | High | High | Medium | Medium | Medium | High |
| R5 Shared comparison harness | High | High | High | High | High | Medium |
| R6 Low operator burden | Medium | Medium | Medium | Medium | Medium | Low for self-hosted |
| R7 Scalable architecture path | Medium | Medium | Medium | High | Medium | High |
| R8 Roadmap learning loop | High | High | High | High | High | Medium |
| R9 Low custom critical infrastructure | Medium | Medium | Medium | Medium | Medium | High if approved |

## Initial Recommendation

Start by comparing Python-first options before investing deeply in TypeScript or a hosted-first baseline.

Recommended first implementation slice:

1. Build `apps/langgraph-python/` as the first candidate app.
2. Use LangGraph Python for orchestration and Langfuse as the first self-hostable observability target.
3. Prove the shared comparable-agent workflow before adding broader product behavior.
4. Capture the functional needs map, setup effort, trace quality, evaluation support, operating burden, and gaps in this
   matrix.

Recommended first observability comparison:

1. Start with Langfuse integration depth for LangGraph Python.
2. Keep Phoenix deferred until developer experience is better understood.
3. Keep MLflow tracing as a second Python option if lifecycle/evaluation needs dominate.
4. Research Pydantic AI plus Logfire/OpenTelemetry as the next Python-first candidate before creating the third
   candidate app lane.

## First Candidate Slice Proposal

Candidate app id: `langgraph-python`.

Stack under evaluation: LangGraph Python plus Langfuse.

Primary purpose: prove whether a Python-first agent workflow can produce decision-ready implementation-slice output
with inspectable local or self-hostable run evidence, without assuming LangSmith approval.

Shared behavior to prove: the comparable-agent workflow in
`tests/workflow/features/comparable_agent_workflow.feature`. The demo should accept a product objective, constraints,
and project context, then return a concise recommendation with alternatives, explicit questions, and an acceptance
check.

First-slice demo boundary:

- One LangGraph workflow that turns structured project context into a next-slice recommendation.
- One deterministic or fixture-backed test path so the comparison harness can run without hidden hosted dependencies.
- Langfuse instrumentation for the workflow run, including model/tool or node-level spans where available.
- One evaluation output tied to the same run, even if the first scorer is deterministic and limited.
- One run artifact that links the command, trace evidence, evaluation output, setup notes, and known gaps.

This boundary scopes only the first `langgraph-python` candidate slice. The cross-candidate minimum demo is defined in
`docs/comparison-evidence.md`.

The first slice must also fill the functional needs map for `langgraph-python`, naming which parts of LangGraph,
Langfuse, shared test assets, and app-local code provide each required function.

Out of scope for the first slice:

- A full self-hosted production Langfuse deployment.
- Multi-agent scheduling, durable workers, or background orchestration beyond the single comparable workflow.
- Declaring LangGraph plus Langfuse as the final platform winner.
- Implementing Phoenix, MLflow, Mastra, or LangSmith comparison code in the same slice.

Promotion questions for the next roadmap review:

1. Is the Langfuse trace readable enough to debug node decisions and failure context?
2. Does the evaluation output attach cleanly to the same run evidence reviewers inspect?
3. Does local setup stay reasonable for one engineer, or does service count become the main risk?
4. Which evidence gaps must be closed before building the second comparison candidate?

## LangGraph Python Evidence Update (T017)

Evidence status: preliminary implementation evidence exists for `langgraph-python`, but this does not select
LangGraph plus Langfuse as the final platform. The current evidence proves the first deterministic fixture path and
identifies the gaps that must be closed before deeper roadmap promotion.

Evidence inspected on 2026-05-23:

- **Run artifact**: the fixture command produced `run-ee283d60c76a866b84bfaa53` in deterministic fixture mode.

  ```bash
  python3 apps/langgraph-python/run.py \
    --fixture packages/comparison/fixtures/langgraph-python-decision-slice.json \
    --output /tmp/langgraph-python-run.json \
    --pretty
  ```

- **Trace artifact**: `/tmp/langgraph-python-run.trace.json` used provider `local-otel-json`, trace id
  `trace-fe8ff3cbf135e5b0e7e81cf3`, and four spans for `load_context`, `map_functional_needs`, `select_slice`, and
  `format_run`. Langfuse ingestion was not sent because fixture mode runs without hosted or self-hosted credentials.
- **Evaluation artifact**: `/tmp/langgraph-python-run.evaluation.json` passed deterministic assertion scoring with
  score `5/5`, evaluation id `eval-c7acb33558860147`, and the same run and trace ids.
- **Setup notes**: `apps/langgraph-python/README.md` documents the repo-root run command and sibling trace/evaluation
  artifact behavior.
- **Gap notes**: `apps/langgraph-python/implementation-plan.md` keeps durable execution, persistence, retries,
  long-running recovery, hosted Langfuse ingestion, dataset evals, and model-judge evals outside the first slice.

### Functional Needs Evidence

| Functional Area | LangGraph Python Evidence | Preliminary Score | Explicit Gaps |
| --- | --- | --- | --- |
| Agent orchestration | Four inspectable graph node spans | 3 | Real model/tool nodes, branching, retries, interrupts, and checkpointing are not proven |
| Tool and context access | Fixture context adapter maps objective and repo context into graph state | 3 | MCP/tool approval boundaries and reusable schemas remain future work |
| Observability | Local OTel-style trace is linked from the run artifact | 3 | Langfuse ingestion, trace UI, token/cost spans, model-call spans, and failure views are not proven |
| Evaluation | Deterministic assertion evaluation ties to the same run and trace ids | 3 | Datasets, model judges, annotations, and trace-linked eval dashboards are not proven |
| Evidence storage | Run artifact links fixture, trace, evaluation, setup, and gap evidence | 3 | No searchable cross-run store or report UI exists |
| Durable execution | First slice records durable runtime as an explicit gap | 2 | Persistence, retries, queues, schedulers, and long-running recovery are unimplemented |
| Operator experience | One local command runs without LangSmith or hosted Langfuse credentials | 3 | Hosted/self-hosted Langfuse setup effort and recovery path are unmeasured |
| Scalability path | App boundary and gap notes describe future service/storage/worker boundaries | 2 | Deployment topology, storage model, tenancy, and worker operations are unproven |

### Preliminary Rubric Scores

These scores use `docs/evaluation-criteria.md` and are intentionally provisional.

| Criterion | Score | Evidence Basis | Gap Or Cap |
| --- | --- | --- | --- |
| Infrastructure ownership | 2 | Fixture mode avoids hosted dependencies and records required artifacts | Workers, eval store, trace UI, and cross-run storage need platform proof |
| Observability | 3 | Local trace export captures graph state transitions and correlates to the run | Langfuse ingestion and richer model/tool telemetry are not proven |
| Evaluation | 3 | Deterministic scorer passes and links to run and trace evidence | Datasets, judges, annotations, and regression history are not proven |
| Scalability | 2 | The app boundary is clean enough for later service extraction | Persistence, storage, deployment topology, and recovery are not implemented |
| Operating effort | 3 | Fixture validation runs locally with one command and no hosted credentials | Langfuse setup, secrets, service count, and failure recovery remain unmeasured |

### Gaps Blocking Promotion

- Do not promote LangGraph plus Langfuse beyond first-candidate status until hosted or self-hosted Langfuse ingestion is
  proven against the same run artifact contract.
- Preserve deterministic fixture validation without hosted credentials; hosted observability must be additive, not a
  prerequisite for `uv run awf workflow-fixture-test`.
- Add real model/tool spans or explicit simulated equivalents before claiming trace coverage for production agent
  behavior.
- Add dataset, model-judge, annotation, or regression-history evidence before treating evaluation support as strong.
- Resolve durable execution and persistence strategy before claiming scalable architecture fit.

## Second Candidate Slice Proposal

Candidate app id: `mastra-ts`.

Stack under evaluation: Mastra TypeScript plus the shared comparison contract.

Primary purpose: provide a cross-language contrast to the Python-first LangGraph slice. This candidate should test
whether a TypeScript-native agent framework reduces orchestration, observability, evaluation, or workflow glue enough
to justify the language and maintenance cost for a Python-preferring owner.

Useful contrast against `langgraph-python`:

- Framework-integrated agent and workflow primitives versus Python LangGraph orchestration.
- Built-in or framework-native observability/export paths versus explicit Langfuse instrumentation in Python.
- TypeScript package and runtime operations versus Python app setup and local service expectations.
- Different tradeoffs for future web UI, deployment, and service composition.

Second-slice demo boundary:

- Implement the same comparable-agent workflow after the first Python slice has produced reviewable evidence.
- Use the same objective, constraints, project-context input shape, and decision-ready output expectations.
- Capture trace, evaluation, setup, and gap evidence in the same format as `langgraph-python`.
- Record any cross-language friction that affects maintenance, test ergonomics, or shared-contract reuse.

Out of scope for the second candidate:

- Replacing the Python-first preference before implementation evidence exists.
- Building a broader TypeScript product surface or web UI.
- Using Mastra-specific behavior that cannot be compared through the shared contract.
- Treating easier demo setup as sufficient if observability, evaluation, or operating evidence is weaker.

Promotion questions for the roadmap review after both slices:

1. Does Mastra reduce custom glue enough to offset TypeScript ownership cost?
2. Are its traces and evaluation outputs comparable to the LangGraph plus Langfuse evidence?
3. Does the shared contract remain clean across Python and TypeScript without app-internal coupling?
4. Should the third candidate stay Python-first, such as MLflow or Phoenix, or should the roadmap deepen the stronger
   of the first two slices?

## Next Python Candidate Research

Initial bounded research on 2026-05-19 points to Pydantic AI plus Logfire or OpenTelemetry as the next Python-first
candidate to evaluate after the approved LangGraph Python slice. It appears more aligned than AutoGen for new work
because AutoGen is in maintenance mode, and more directly agent-runtime-focused than LlamaIndex unless the next product
decision centers on data/RAG-heavy workflows. LlamaIndex remains a strong fallback candidate if document and retrieval
capabilities become the dominant functional area.

## Roadmap Review Questions

These questions should be asked during the next CEO-level roadmap review:

1. Should the first prototype optimize for fastest local demo or best long-term observability architecture?
2. Is LangGraph Python the right first orchestration candidate, or should a simpler Python app establish the harness?
3. What evidence would justify reopening Phoenix as an immediate observability implementation?
4. Does the minimum comparable demo in `docs/comparison-evidence.md` produce enough evidence for a roadmap decision?

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

1. Build a minimal runnable agent workflow in `apps/langgraph-python/` that satisfies the shared contract in `tests/workflow/features/comparable_agent_workflow.feature`.
2. Instrument traces through a local/self-hostable Langfuse path and persist artifacts required by `docs/comparison-evidence.md`.
3. Define one candidate run command and one candidate verification command so later apps can mirror the same operator flow.

### Contract + Evidence Targets

- **Contract target**: satisfy scenario assertions in
  `tests/workflow/features/comparable_agent_workflow.feature`
  (recommendation, alternatives, explicit questions, acceptance check, durable run evidence).
- **Run artifact destination**: record run metadata and pass/fail outcome in `.agent-runs/reports/` with links to trace/eval artifacts.
- **Trace artifact destination**: store export path or retrievable trace reference under a candidate-owned folder in `artifacts/comparison/langgraph-python/`.
- **Evaluation artifact destination**: store repeatable eval outputs under `artifacts/comparison/langgraph-python/evals/`.
- **Operating notes destination**: capture setup commands, required services, and env vars in `apps/langgraph-python/README.md`.

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

## Second Comparison Candidate Proposal (T008)

### Candidate

- **Name**: `mastra-ts-slice-01`
- **App location**: `apps/mastra-ts/`
- **Why this contrast is useful**: it provides a deliberate cross-language counterpoint against the Python-first lane,
  testing whether TypeScript-native workflow ergonomics or framework defaults outperform the Python path enough to
  justify ecosystem switching cost.

### Contrast Hypothesis

If `mastra-ts-slice-01` can satisfy the same shared contract with materially better observability/eval ergonomics or
lower operating burden than the first Python slice, the roadmap should revisit the Python-first default before deeper
implementation lock-in.

### Scope

1. Implement the same comparable workflow contract used by `langgraph-python-langfuse-slice-01`.
2. Capture equivalent run, trace, evaluation, and setup evidence groups defined in `docs/comparison-evidence.md`.
3. Document cross-language friction explicitly (tooling, dependency management, onboarding, and maintenance burden).

### Explicit Non-Goals

- No attempt to prove feature-complete parity with all Python integrations.
- No expansion into production deployment architecture.
- No replacement decision for the primary lane without the CEO-level roadmap review gate.

### Exit Evidence For T008

- Shared-contract parity claim is backed by runnable evidence artifacts.
- Cross-language tradeoffs are explicit enough to compare against R1, R6, and R9.
- A reviewer can determine whether contrast value is high enough to justify continued TypeScript investment.

## Minimum Comparable Demo Definition (T009)

### Demo Goal

Provide the smallest end-to-end demonstration that allows apples-to-apples scoring across candidate apps while
producing contract, trace, evaluation, and operating evidence.

### Required Demo Flow

1. **Input**: objective + constraints + project context supplied through the contract driver.
2. **Behavior**: candidate proposes a next implementation slice.
3. **Output**: concise recommendation, alternatives, explicit questions, and a named acceptance check.
4. **Operational evidence**: durable run artifact, trace artifact, eval artifact, and setup notes.

### Demo Pass Criteria

A candidate demo is comparable only if all of the following are true:

- Shared BDD contract scenario passes for the candidate implementation.
- Trace evidence is inspectable and tied to the same run artifact.
- Evaluation output is repeatable and tied to the same scenario/run.
- Setup notes allow another engineer/agent to rerun the slice locally.
- Gaps and custom-critical-infrastructure warnings are explicitly recorded.

### Demo Evidence Checklist Template

Use this checklist for each candidate run:

- [ ] Candidate id, commit, run timestamp, and commands recorded.
- [ ] Shared contract scenario and result recorded.
- [ ] Trace provider, trace link/export path, and coverage notes recorded.
- [ ] Eval dataset/cases, scorer type, score result, and rerun command recorded.
- [ ] Setup prerequisites, env vars, and required services recorded.
- [ ] Known gaps, risks, and follow-up tickets/spec tasks recorded.
