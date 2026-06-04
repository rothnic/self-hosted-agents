# LangGraph Python App

First Python-first candidate app for the solution comparison roadmap. Keep this independent from the TypeScript Mastra
app except for shared contracts and comparison assets.

Detailed slice plan: `apps/langgraph-python/implementation-plan.md`.

Current disposition: frozen comparison reference.

Reference policy: `docs/candidate-references/frozen-non-selected-candidates.md`.

This lane remains in the repo for comparison history and regression context. Product-baseline work should deepen the
selected Pydantic AI plus Langfuse/DBOS stack unless a future Beads ticket or ADR explicitly reopens LangGraph-specific
work.

## First Slice

Candidate id: `langgraph-python`.

Stack: LangGraph Python plus Langfuse.

The current scaffold implements the shared comparable-agent workflow in deterministic fixture mode, not a full
production agent system. It accepts a product objective, constraints, and project context, then returns:

- a concise recommended next implementation slice;
- meaningful alternatives and tradeoffs;
- explicit human questions when direction is not safe to assume;
- an acceptance check for the proposed implementation work;
- durable run evidence that can be compared with later candidate apps.

Run it from the repo root:

```bash
python3 apps/langgraph-python/run.py \
  --fixture packages/comparison/fixtures/langgraph-python-decision-slice.json \
  --output /tmp/langgraph-python-run.json \
  --pretty
```

When `--output` is set, the command also writes deterministic sibling artifacts:

- `/tmp/langgraph-python-run.trace.json`: local OpenTelemetry-style trace export. Use `--trace-output` to choose a
  different trace path.
- `/tmp/langgraph-python-run.evaluation.json`: deterministic assertion evaluation tied to the same run id and trace id.
  Use `--evaluation-output` to choose a different evaluation path.

The run artifact links the fixture input, recommendation output, trace evidence, evaluation output, setup notes, gap
notes, command used, and acceptance check. The trace export records Langfuse ingestion as a gap when credentials are
absent, so fixture validation remains deterministic without hosted services.

## Evidence Required

The implementation sequence should produce:

- a runnable command for the candidate demo;
- a passing shared behavior-contract or fixture check;
- Langfuse trace evidence for the workflow run;
- evaluation output tied to the same run;
- setup notes covering required services, environment variables, and local startup;
- explicit gaps and custom critical infrastructure risks.

Use `docs/comparison-evidence.md` as the evidence checklist and `docs/evaluation-criteria.md` as the scoring rubric.

## Non-Goals

Do not build the Phoenix, MLflow, Mastra, or LangSmith comparison paths in this app. Do not declare LangGraph plus
Langfuse as the final architecture until comparable implementation evidence exists.

Do not add product-baseline features here by default. Keep changes limited to reference maintenance, fixture
compatibility, or an explicitly reopened comparison ticket.
