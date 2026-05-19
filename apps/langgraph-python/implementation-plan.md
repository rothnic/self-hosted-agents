# LangGraph Python Implementation Plan

## Purpose

Define the first approved implementation slice for `apps/langgraph-python/` before writing candidate app code. This
plan maps the required functional needs to the solution components expected to provide them, then scopes the next
implementation tickets so later evidence can be compared against other candidate apps.

## Approved Slice

Candidate id: `langgraph-python`

Stack under evaluation: LangGraph Python plus Langfuse, with OpenTelemetry export considered when it reduces custom
instrumentation or improves portability.

Approved decision: implement this as the first evidence-producing candidate slice. This is not a final platform choice.

Primary goal: prove that a Python-first LangGraph workflow can run the shared comparable-agent scenario and produce
reviewable run, trace, evaluation, setup, and gap evidence without assuming LangSmith approval.

## Functional Needs Mapping

| Functional Area | Provider Components | First-Slice Evidence | Extra Features To Watch |
| --- | --- | --- | --- |
| Agent orchestration | LangGraph state graph, nodes, edges, and typed state | Runnable graph that produces a recommended next slice | Checkpointing, branching, retries, interrupts |
| Tool and context access | App-local typed adapters over fixture project context | Fixture input mapped into graph state and tool calls | Schema reuse, MCP boundary, approval hooks |
| Observability | Langfuse tracing, with OTel export as portability fallback | Trace or trace export linked from run artifact | Token/cost views, failure views, trace-to-eval links |
| Evaluation | Deterministic scorer for the shared comparable workflow | Eval output tied to the same run id as the trace | Dataset support, model-judge path, annotation workflow |
| Evidence storage | Repo run artifact plus trace/eval/setup/gap paths | One evidence record under the app or shared evidence path | Searchable cross-run index, generated report |
| Durable execution | Out of scope for first slice beyond explicit gap notes | Gap note for persistence and long-running recovery | LangGraph checkpointers, external durable runtime |
| Operator experience | Local command, README setup notes, minimal env requirements | One command plus setup and failure notes | Single bootstrap command, diagnostics, low service count |
| Scalability path | App package boundary plus documented future service path | Gap note describing service/storage/worker boundaries | Durable workers, deployment topology, tenancy controls |

## First-Slice Boundary

The first implementation slice should create the smallest runnable path that can be judged against the shared
comparison evidence checklist:

1. Accept the common input categories from `docs/comparison-evidence.md`.
2. Run a LangGraph workflow that emits a recommended next implementation slice, alternatives, questions, and acceptance
   check.
3. Support a deterministic fixture mode so validation does not require hosted credentials.
4. Produce a run artifact that links command, input, output, trace evidence, eval evidence, setup notes, and gaps.
5. Keep Langfuse optional enough that missing credentials are recorded as a gap instead of blocking deterministic
   fixture validation.

## Ticket Mapping

T014 should scaffold the runnable app and deterministic comparable workflow. Its output should include the command,
fixture input/output path, and app-local modules needed by later trace and eval work.

T015 should add trace evidence capture through Langfuse or OpenTelemetry. It should preserve deterministic validation
when tracing credentials are absent and record any observability gaps.

T016 should add evaluation output and run artifact capture tied to the same candidate run. It should make the evidence
easy for T017 to summarize in the requirements matrix.

T017 should update `docs/requirements-matrix.md` only after the prior implementation tickets produce evidence. It
should score the LangGraph Python slice against the functional needs map and record gaps explicitly.

T018 should research Pydantic AI plus Logfire/OpenTelemetry against this same functional needs map before any third
candidate app lane is created.

## Non-Goals

- Do not build production Langfuse deployment automation in the first slice.
- Do not add durable workers, queues, or schedulers before the basic comparable workflow produces evidence.
- Do not implement Phoenix, MLflow, Pydantic AI, Mastra, or LangSmith code in this app.
- Do not treat this slice as final architecture selection.
