# Pydantic AI App

Second Python-first candidate app for the solution comparison roadmap. Keep this lane independent from the LangGraph
Python app except for shared contracts and comparison assets.

Detailed slice plan: `apps/pydantic-ai/implementation-plan.md`.

## First Slice

Candidate id: `pydantic-ai`.

Stack: Pydantic AI plus Logfire/OpenTelemetry, with Pydantic Evals and durable execution evaluated by later tickets.

The current scaffold implements the shared comparable-agent workflow in deterministic fixture mode. It uses app-local
typed data boundaries to shape fixture input and structured output, but it does not call a live model, send telemetry to
Logfire, run Pydantic Evals, or select a durable runtime.

Run it from the repo root:

```bash
python3 apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output /tmp/pydantic-ai-run.json \
  --pretty
```

The run artifact records the fixture input, recommendation output, trace id, planned trace evidence, planned evaluation
evidence, setup notes, gap notes, command used, and acceptance check.

## Local Setup

Required local tools:

- Python 3.12 or newer.
- Repo dependencies installed through the existing `uv` environment.

Fixture-mode service count: `0`. The deterministic fixture path does not require a hosted model provider, Logfire
project, local OpenTelemetry collector, database, queue, worker, or durable runtime.

Environment variable placeholders for later tickets:

- `LOGFIRE_TOKEN`: hosted Logfire write token for live telemetry evidence.
- `LOGFIRE_PROJECT_URL`: safe reviewer-facing project or trace URL when available.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: optional generic OpenTelemetry collector endpoint.
- `PYDANTIC_AI_MODEL`: later live model selection; unused in fixture mode.

Common deterministic-run failures:

- Missing fixture path: rerun from the repo root or pass an absolute `--fixture` path.
- Invalid fixture JSON: keep the fixture categories aligned with `docs/comparison-evidence.md`.
- Missing output directory permission: choose a writable `--output` path such as `/tmp/pydantic-ai-run.json`.

## Evidence Required

The implementation sequence should produce:

- a runnable command for the candidate demo;
- a passing shared behavior-contract or fixture check;
- hosted Logfire and repo-local OpenTelemetry evidence for the workflow run;
- Pydantic Evals output tied to the same run and trace;
- setup notes covering required services, environment variables, and local startup;
- explicit gaps for hosted observability, evaluation, durable execution, scalability, and operating risk.

Use `docs/comparison-evidence.md` as the evidence checklist and `docs/evaluation-criteria.md` as the scoring rubric.

## Non-Goals

Do not prove hosted Logfire, Pydantic Evals, or durable execution in this scaffold. Do not declare Pydantic AI plus
Logfire/OpenTelemetry as the final architecture until comparable implementation evidence exists.
