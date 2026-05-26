# Pydantic AI Implementation Plan

## Purpose

Define the approved implementation slice for `apps/pydantic-ai/` before writing candidate app code. This plan maps the
required functional needs to the Pydantic AI, Logfire/OpenTelemetry, Pydantic Evals, and durable execution components
expected to provide them, then scopes the next implementation tickets so later evidence can be compared against
`apps/langgraph-python/` and future candidate lanes.

## Approved Slice

Candidate id: `pydantic-ai`

Stack under evaluation: Pydantic AI plus Logfire/OpenTelemetry, with Pydantic Evals planned as the evaluation path and
durable execution options evaluated after the deterministic comparable workflow exists.

Approved decision: implement this as the next Python-first evidence-producing candidate lane. This is not a final
platform choice.

Primary goal: prove that a typed Pydantic AI workflow can run the shared comparable-agent scenario and produce
reviewable run, trace, evaluation, setup, and gap evidence without requiring hosted credentials for deterministic
validation.

## Functional Needs Mapping

Each functional area should name the provider component, first-slice evidence, and useful extra features without
treating research claims as implementation evidence.

Agent orchestration: Pydantic AI agent, typed dependencies, structured output, and optional graph or capability
features. First evidence is a runnable comparable workflow that proposes a next implementation slice. Watch capability
composition, graph support, streaming, and approval hooks.

Tool and context access: app-local typed adapters over fixture project context, exposed through Pydantic AI tools or
dependencies. First evidence is fixture input mapped into tool or context calls with typed outputs. Watch MCP, A2A, and
reusable capability bundles.

Observability: Pydantic AI OpenTelemetry instrumentation, Logfire as the hosted first-party path, and generic OTel as
the portability path. First evidence is a repo-local trace export linked from the run artifact, with hosted Logfire gap
or evidence recorded separately. Watch trace UI, token or cost views, tool-call inspection, SQL access, and MCP access
to telemetry.

Evaluation: Pydantic Evals plus deterministic assertions for the shared comparable workflow. First evidence is eval
output tied to the same run id and trace id. Watch datasets, experiments, span-based evals, and Logfire visualization.

Evidence storage: repo-local run, trace, eval, setup, and gap artifacts, with hosted links only as additive evidence.
First evidence is one run artifact linking all evidence groups. Watch cross-run reports and searchable hosted telemetry.

Durable execution: out of scope for the first runnable slice beyond explicit gap notes. First evidence is a gap note
naming durable runtime selection as blocked until T024/T025 evidence. Watch DBOS, Prefect, Restate, Temporal, and
Hatchet.

Operator experience: local deterministic command, README setup notes, and optional hosted env vars. First evidence is
one no-credential command plus setup and failure notes. Watch single-command local stack, low service count, and
diagnostics.

Scalability path: app package boundary plus later durable runtime comparison. First evidence is a gap note describing
service, storage, and runtime boundaries. Watch durable workers, deployment topology, and recovery dashboard.

## First-Slice Boundary

The first runnable Pydantic AI slice should create the smallest path that can be judged against the shared comparison
evidence checklist:

1. Accept the common input categories from `docs/comparison-evidence.md`.
2. Run a Pydantic AI workflow that emits a recommended next implementation slice, alternatives, questions, and
   acceptance check.
3. Support a deterministic fixture mode so validation does not require hosted credentials or live model calls.
4. Produce a run artifact that links command, input, output, trace evidence, eval evidence, setup notes, and gaps.
5. Emit a repo-local OpenTelemetry trace or trace-shaped export that is correlated to the run artifact.
6. Record the Pydantic AI instrumentation format or semantic-convention version used by the trace path.
7. Keep Logfire optional for deterministic validation; missing hosted credentials should become gap evidence, not a
   failed fixture run.

Future T021 command target:

```bash
python3 apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output /tmp/pydantic-ai-run.json \
  --pretty
```

The future run artifact should preserve the comparable output categories already used by the LangGraph slice:
`candidate_app_id`, `stack`, `run_id`, `trace_id`, `recommendation`, `alternatives`, `questions`, `acceptance_check`,
`evaluation_output`, `evidence_paths`, and `gaps`.

## Ticket Mapping

T021 should scaffold `apps/pydantic-ai/`, the deterministic comparable workflow, the fixture input, the CLI command,
app-local modules needed by later trace and evaluation work, and app README setup notes for the local fixture path. The
setup notes must include the rerun command, required local tools, env var placeholders, service count for fixture mode,
and common deterministic-run failure notes. T021 should not require hosted Logfire credentials.

T022 should add hosted Logfire and repo-local OpenTelemetry trace evidence capture. It should prove hosted telemetry
from the tested candidate stack, document credential handling and hosted verification commands, preserve deterministic
validation without credentials, and record the instrumentation format or semantic-convention version to avoid brittle
assertions against moving GenAI conventions. T022 is not complete with only local OTel plus a gap note; if hosted
credentials are unavailable, record the blocker and leave the hosted-evidence portion open.

T023 should add Pydantic Evals output and run artifact capture tied to the same run id and trace id. It should keep a
deterministic assertion path for fixture validation, update setup notes with eval rerun details and artifact locations,
and treat hosted Logfire visualization as additive evidence.

T024 should compare durable execution options before choosing a runtime. Evaluate Pydantic AI framework-specific paths
first: DBOS, Prefect, Restate, and Temporal. Compare Hatchet as the primary non-framework-specific Python workflow
platform option.

T025 should add a durable execution smoke path only after T024 selects the lowest-complexity viable option. The smoke
path must prove retry or resume behavior in a way another agent can inspect from command output, run artifacts, traces,
or logs.

T026 should update `docs/requirements-matrix.md` only after the Pydantic AI lane produces implementation evidence. It
should score the slice against the functional needs map, keep final-solution language blocked until hosted
observability and durable execution evidence exist, and record promotion gaps explicitly.

## Non-Goals

- Do not build the runnable Pydantic AI app in T020.
- Do not add dependencies, fixtures, runtime modules, or generated artifacts before T021.
- Do not require hosted Logfire credentials for deterministic validation.
- Do not choose DBOS, Prefect, Restate, Temporal, Hatchet, or another durable runtime in this planning task.
- Do not treat Pydantic AI plus Logfire/OpenTelemetry as the final platform winner before comparable evidence exists.
