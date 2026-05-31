# Pydantic AI Implementation Plan

## Purpose

Define the approved implementation slice for `apps/pydantic-ai/` before writing candidate app code. This plan maps the
required functional needs to the Pydantic AI, Langfuse/OpenTelemetry, Pydantic Evals, and durable execution components
expected to provide them, then scopes the next implementation tickets so later evidence can be compared against
`apps/langgraph-python/` and future candidate lanes.

## Approved Slice

Candidate id: `pydantic-ai`

Stack under evaluation: Pydantic AI plus Langfuse/OpenTelemetry, with Pydantic Evals planned as the evaluation path and
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

Observability: Pydantic AI OpenTelemetry instrumentation, self-hosted Langfuse as the LLM-aware trace UI, and Logfire as
an optional first-party export target only when an operator provides a suitable backend. First evidence is a repo-local
trace export linked from the run artifact plus explicit self-hosted Langfuse ingestion proof. Watch trace UI, token or
cost views, tool-call inspection, SQL access, and MCP access to telemetry.

Evaluation: Pydantic Evals plus deterministic assertions for the shared comparable workflow. First evidence is eval
output tied to the same run id and trace id. Watch datasets, experiments, span-based evals, and Logfire visualization.

Evidence storage: repo-local run, trace, eval, setup, and gap artifacts, with external UI links only as additive
evidence. First evidence is one run artifact linking all evidence groups. Watch cross-run reports and searchable
self-hosted telemetry.

Durable execution: out of scope for the first runnable slice beyond explicit gap notes. T024 selected Pydantic AI plus
DBOS as the first durable smoke path because it is native to Pydantic AI, can run locally with SQLite for the first
proof, and avoids a separate workflow server for the next slice. Watch Prefect as the closest fallback, Temporal as the
scale fallback, Restate after the package boundary is resolved, and Hatchet as the broader workflow-platform option.

Operator experience: local deterministic command, README setup notes, and optional export env vars. First evidence is
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
7. Keep Logfire optional for deterministic validation; missing external export credentials should become gap evidence,
   not a failed fixture run.

Future T021 command target:

```bash
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-run.json \
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

T022 should add self-hosted-compatible OpenTelemetry trace evidence capture for the tested candidate stack. It should
write repo-local trace evidence, document optional Logfire export handling for an operator-provided backend, preserve
deterministic validation without credentials, and record the instrumentation format or semantic-convention version to
avoid brittle assertions against moving GenAI conventions. A cloud-hosted Logfire project or token is not valid
acceptance evidence for this self-hosted assessment; if self-hosted Logfire is unavailable, record the feasibility gap
and close T022 with repo-local OTel evidence.

T027 should prove self-hosted Langfuse ingestion for the Pydantic AI trace path before eval scoring depends on that
trace context. It should use OpenTelemetry as the transport into Langfuse, document the local deployment shape, record
the env vars and command, and preserve the repo-local trace artifact as deterministic fallback evidence. Phoenix and
Opik remain comparison alternatives, but Langfuse is the default backend target because it is self-hostable,
LLM-specific, and already part of the LangGraph lane.

T023 adds Pydantic Evals output and run artifact capture tied to the same run id and trace id. It keeps a deterministic
assertion path for fixture validation, writes `.evaluation.json` next to the run artifact by default, updates setup
notes with eval rerun details and artifact locations, and treats Logfire visualization as additive evidence.

T024 compares durable execution options before choosing a runtime. The recorded selection is Pydantic AI plus DBOS for
the first T025 smoke, with the comparison basis in
`docs/research/durable-execution-selection-2026-05-31.md` and compact evidence in
`.agent-runs/verifications/verify-durable-options-t024-20260531.json`. The comparison keeps Prefect, Restate, Temporal,
and Hatchet visible as follow-up or fallback options.

T025 adds a DBOS durable execution smoke path using the lowest-complexity viable option selected by T024. The smoke
path proves resume behavior in a way another agent can inspect from command output and a run artifact. It uses local
SQLite DBOS state, deterministic fixture mode, `DBOSAgent`, and one explicit side-effect-like DBOS step. The first child
process is killed after that side-effect step completes; the second child process recovers the pending workflow from the
same SQLite database and proves the completed side-effect step is not duplicated. T025 also adds and locks the DBOS
dependency required to import `DBOSAgent`.

T026 should update `docs/requirements-matrix.md` only after the Pydantic AI lane produces implementation evidence. It
should score the slice against the functional needs map, keep final-solution language blocked until hosted
self-hosted-compatible observability and durable execution evidence exist, and record promotion gaps explicitly.

## Dependency And Live Evaluation Gates

The executable Beads queue must preserve the implementation order implied by this plan:

- T022 depends on T021 because local OTel evidence and optional Logfire export notes require a runnable candidate app.
- T027 depends on T022 because Langfuse ingestion needs the runnable local trace path.
- T023 depends on T027 because Pydantic Evals evidence must correlate to the same run and Langfuse-backed trace ids.
- T024 depends on T021 because durable execution options should be evaluated against the actual candidate lane.
- T025 depends on T024 because the durable smoke path must use the selected lowest-complexity option.
- T026 depends on T023 and T025 because matrix scoring must wait for eval evidence and durable smoke evidence.

Self-hosted observability evaluation means telemetry evidence from the running candidate app can be inspected without
requiring a third-party cloud project. T022 and T027 evidence must include the command used, run id, trace id,
repo-local export path, the trace schema or instrumentation version, and any optional Logfire export setup path.
Provider docs, screenshots, disconnected sample runs, or cloud-only trace links do not satisfy the self-hosted
observability gate.

## Non-Goals

- Do not build the runnable Pydantic AI app in T020.
- Do not add dependencies, fixtures, runtime modules, or generated artifacts before T021.
- Do not require hosted Logfire credentials for deterministic validation or T022 closure.
- Do not treat the T024 DBOS selection as the final platform winner before T025 durable smoke evidence exists.
- Do not treat Pydantic AI plus Langfuse/OpenTelemetry as the final platform winner before comparable evidence exists.
