# Non-Selected Candidate Migration Notes

Status: defined for Goal 004 T012
Selected product baseline: Pydantic AI plus Langfuse and DBOS
Freeze policy: `docs/candidate-references/frozen-non-selected-candidates.md`
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

Record what can be reused from frozen non-selected candidate lanes without turning those lanes back into active product
implementation lanes.

T011 froze LangGraph Python, Mastra TypeScript, and LangSmith as references. T012 decides the migration posture for
their useful code, fixtures, and evidence. This note does not move code. Future movement requires an explicit Beads
ticket, acceptance evidence, and updated docs.

## Migration Rules

Reusable assets can migrate only when all of these are true:

- the destination is the selected `apps/pydantic-ai/` product-baseline lane, a shared `packages/` asset, a `tests/`
  contract, or a durable `docs/` evidence artifact;
- the move strengthens the Pydantic AI product baseline or a shared implementation-agnostic contract;
- deterministic fixture validation still passes without hosted credentials or cloud services;
- the new location is named in the linked Beads ticket and reviewed by an independent reviewer agent;
- the source candidate remains understandable as a frozen reference after the migration.

Do not migrate an asset only because it exists in a frozen lane. Copying framework-specific implementation across app
lanes creates hidden coupling and makes the platform decision harder to audit.

## Migration Ledger

### Comparable Fixture Shape

Source references:

- `packages/comparison/fixtures/langgraph-python-decision-slice.json`
- `packages/comparison/fixtures/pydantic-ai-decision-slice.json`
- `tests/workflow/features/comparable_agent_workflow.feature`

Disposition: already shared.

The comparable fixture input shape is already outside app-local directories. Keep both candidate fixture files because
they preserve comparison history and expected stack-specific context. Future product-baseline fixtures should add new
product-oriented inputs instead of mutating these comparison fixtures.

Migration action: none for T012. If a future product workflow needs a reusable fixture schema, create it under
`packages/` or `tests/workflow/fixtures/` through a new product-baseline ticket.

### Run, Trace, And Evaluation Artifact Contract

Source references:

- `apps/langgraph-python/langgraph_candidate/graph.py`
- `apps/langgraph-python/langgraph_candidate/trace.py`
- `apps/langgraph-python/langgraph_candidate/evaluation.py`
- `apps/pydantic-ai/pydantic_candidate/workflow.py`
- `apps/pydantic-ai/pydantic_candidate/trace.py`
- `apps/pydantic-ai/pydantic_candidate/evaluation.py`

Disposition: partially represented in selected lane; future shared extraction candidate.

Both Python lanes use the same broad artifact idea: a run JSON links fixture input, trace evidence, evaluation evidence,
setup notes, gap notes, command used, and the acceptance command. The selected Pydantic AI lane already implements the
stronger product-baseline version because it uses Pydantic AI native OpenTelemetry spans, optional self-hosted Langfuse
OTLP ingestion, Pydantic Evals output, and DBOS correlation.

Do not import `langgraph_candidate` modules into `apps/pydantic-ai/`. If two or more active product or comparison lanes
need the same stable id, artifact-schema, or trace-export helper, extract a small implementation-agnostic helper under
`packages/` in a future ticket. That future ticket must prove both affected lanes still pass
`uv run awf workflow-fixture-test`.

Migration action: no code movement for T012. Treat the LangGraph implementation as reference evidence for the artifact
contract and keep the Pydantic implementation as the active product path.

### Functional Needs Mapping

Source references:

- `docs/requirements-matrix.md`
- `apps/langgraph-python/langgraph_candidate/graph.py`
- `apps/pydantic-ai/pydantic_candidate/workflow.py`

Disposition: already migrated into roadmap evidence.

The functional-needs categories from the LangGraph slice helped define the normalized matrix and selected-stack scoring.
The selected Pydantic lane already has an expanded provider mapping that includes durable execution and Pydantic Evals.

Migration action: keep the mapping in `docs/requirements-matrix.md` as the durable source of truth. Do not extract the
LangGraph `FUNCTIONAL_NEEDS` constant unless a future shared schema task needs multiple runnable lanes to consume the
same machine-readable map.

### Deterministic Evaluation Criteria

Source references:

- `apps/langgraph-python/langgraph_candidate/evaluation.py`
- `apps/pydantic-ai/pydantic_candidate/evaluation.py`
- `docs/evaluation-criteria.md`

Disposition: concept migrated; implementation stays lane-specific.

The LangGraph deterministic scorer proved the minimum comparable assertions. The selected Pydantic lane already uses
Pydantic Evals to score the same evidence categories plus Pydantic AI runtime and run/trace correlation.

Migration action: keep evaluation implementation lane-specific for now. Future shared extraction should target a small
rubric or assertion schema only after the product-baseline work-order app has its own runnable evidence.

### CLI And Sibling Artifact Convention

Source references:

- `apps/langgraph-python/run.py`
- `apps/pydantic-ai/run.py`
- `apps/langgraph-python/README.md`
- `apps/pydantic-ai/README.md`

Disposition: already represented in selected lane.

Both runnable Python lanes use a fixture input, JSON output, and sibling `.trace.json` and `.evaluation.json` artifacts.
The selected Pydantic lane already preserves that operator convention with stronger trace and evaluation proof.

Migration action: keep the convention. Do not share CLI internals until a future ticket needs a reusable runner for
multiple active lanes.

### LangGraph Orchestration Semantics

Source references:

- `apps/langgraph-python/langgraph_candidate/graph.py`
- `apps/langgraph-python/implementation-plan.md`

Disposition: reference-only unless reopened.

LangGraph remains useful for graph-oriented workflow vocabulary: nodes, transitions, state, and graph semantics. The
selected product baseline currently relies on Pydantic AI typed agent boundaries plus DBOS durable states instead.

Migration action: do not migrate LangGraph graph code into the Pydantic product lane. Reopen only through a future
ticket or ADR if the Pydantic baseline fails a product requirement that specifically needs LangGraph graph or
checkpoint semantics.

### Mastra TypeScript Contrast Notes

Source references:

- `apps/mastra-ts/README.md`
- `.agent-runs/reports/goal-004-t002-mastra-contrast-decision-20260602.md`

Disposition: reference-only.

Mastra has no runnable app, fixture command, trace export, eval artifact, package manifest, or durable runtime proof in
current repo state. There is no code or fixture to migrate into the selected baseline.

Migration action: none. Preserve the TypeScript contrast questions for future product or ownership decisions. A future
Mastra reopening must create its own runnable evidence instead of borrowing Pydantic or LangGraph proof.

### LangSmith Feature Benchmark

Source references:

- `docs/requirements-matrix.md`
- `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md`

Disposition: reference-only.

LangSmith remains a useful feature expectation benchmark for trace review and evaluation workflows, but hosted-only
inspection does not satisfy this self-hosted assessment.

Migration action: no code or fixture movement. Use LangSmith only as product-expectation research unless a future spec
proves self-hosted-compatible access.

## Future Migration Candidates

Future tickets may consider these extractions after the product-baseline app has runnable work-order evidence:

- a shared run artifact schema for `run_id`, `trace_id`, `evaluation_id`, evidence paths, gaps, and acceptance command;
- a small stable-id helper if at least two active lanes need identical deterministic id semantics;
- a shared fixture schema for product-baseline work orders, distinct from comparison candidate fixtures;
- a shared evaluation rubric for evidence completeness and reviewer-gate enforcement.

Each extraction should name its consumers before implementation. If the selected product baseline is the only consumer,
keep the code in `apps/pydantic-ai/`.

## Non-Migration Decisions

Do not migrate:

- LangGraph framework-specific graph code into the Pydantic product lane;
- Mastra TypeScript scaffolding into Python product code;
- transient audit outputs from `/tmp`;
- hosted-only LangSmith evidence;
- Python bytecode caches or generated local state;
- docs that explain why a candidate was rejected or deferred.

These assets either remain comparison evidence, lack implementation proof, or would add coupling without moving the
selected product baseline forward.

## Completion Evidence

T012 can be treated as complete when:

- this migration note is linked from the freeze policy, Goal 004, the spec, and roadmap state;
- each frozen candidate has an explicit migration posture;
- reusable ideas are separated from framework-specific code;
- deterministic validation still passes without hosted credentials;
- follow-up production hardening remains assigned to T013 instead of being folded into migration work.
