# Pydantic AI App

Second Python-first candidate app for the solution comparison roadmap. Keep this lane independent from the LangGraph
Python app except for shared contracts and comparison assets.

Detailed slice plan: `apps/pydantic-ai/implementation-plan.md`.

## First Slice

Candidate id: `pydantic-ai`.

Stack: Pydantic AI plus Langfuse/OpenTelemetry, Pydantic Evals, and a DBOS durable smoke path.

The current scaffold implements the shared comparable-agent workflow in deterministic fixture mode. It uses
`pydantic_ai.Agent` with `pydantic_ai.models.test.TestModel` to return structured output without a network model call,
and it writes a repo-local OpenTelemetry-style trace export that is correlated to the run artifact. It does not call a
live model or require cloud-hosted Logfire ingestion.

Run it from the repo root:

```bash
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-run.json \
  --pretty
```

The run artifact records the fixture input, recommendation output, trace id, local trace evidence, Pydantic Evals
evidence, setup notes, gap notes, command used, and acceptance check. When `--output` is provided, the trace export is
written next to it with a `.trace.json` suffix and the evaluation artifact is written next to it with an
`.evaluation.json` suffix unless explicit output paths are set.

Optional explicit trace path:

```bash
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-run.json \
  --trace-output .agent-runs/verifications/pydantic-ai-run.trace.json \
  --evaluation-output .agent-runs/verifications/pydantic-ai-run.evaluation.json \
  --pretty
```

## Pydantic Evals Output

Fixture mode runs a deterministic Pydantic Evals dataset against the run artifact. The evaluation checks
recommendation shape, acceptance command, run and trace correlation, Pydantic AI runtime evidence, and evidence path
completeness. It writes a repo-local artifact that includes the dataset name, case id, evaluator results, score,
summary, rerun command, and links to the run and trace artifacts.

Current T023 evidence:

- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json`

## DBOS Durable Smoke

T025 uses Pydantic AI's DBOS integration as the first durable execution proof. The smoke uses local SQLite DBOS state,
starts a workflow in one child process, kills that process after a completed side-effect step, then starts a second
child process against the same DBOS database. The resumed workflow completes through `DBOSAgent` and proves the
side-effect step was not duplicated.

Run it from the repo root:

```bash
uv run python apps/pydantic-ai/durable_smoke.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-durable-smoke.json \
  --pretty
```

For durable repo evidence, prefer temporary DBOS state paths and keep only the JSON artifact:

```bash
uv run python apps/pydantic-ai/durable_smoke.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-durable-smoke-t025-20260531.json \
  --db-path /tmp/pydantic-ai-dbos-t025.sqlite \
  --side-effect-log /tmp/pydantic-ai-dbos-side-effect-t025.jsonl \
  --pretty
```

Current T025 evidence:

- `.agent-runs/verifications/pydantic-ai-durable-smoke-t025-20260531.json`

## Local Setup

Required local tools:

- Python 3.12 or newer.
- Repo dependencies installed through the existing `uv` environment.

Fixture-mode service count: `0`. The deterministic fixture path does not require a hosted model provider, Logfire
project, local OpenTelemetry collector, queue, worker, or long-running service. The durable smoke uses a local SQLite
DBOS database file and no hosted credentials.

Environment variable placeholders for later tickets:

- `LOGFIRE_TOKEN`: optional Logfire write token for an operator-approved export run.
- `LOGFIRE_PROJECT_URL`: optional safe reviewer-facing project or trace URL when available.
- `LOGFIRE_BASE_URL`: optional self-managed or non-default Logfire backend URL.
- `LANGFUSE_BASE_URL`: self-hosted Langfuse base URL for T027 service-backed OTLP ingestion.
- `LANGFUSE_PUBLIC_KEY`: self-hosted Langfuse project public key for OTLP Basic Auth.
- `LANGFUSE_SECRET_KEY`: self-hosted Langfuse project secret key for OTLP Basic Auth.
- `LANGFUSE_PROJECT_ID`: optional project id used only to record a reviewer-facing trace URL.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: optional generic OpenTelemetry collector endpoint.
- `PYDANTIC_AI_MODEL`: later live model selection; unused in fixture mode.

Logfire export verification remains separate from fixture validation. Cloud-hosted Logfire credentials are not required
and are not sufficient acceptance evidence for this self-hosted agents assessment. If an operator-approved Logfire
backend is available, record the command, run id, trace id, safe project or trace URL, and repo-local trace export path.
The local command records whether `LOGFIRE_TOKEN` was present, but credentials alone do not send traffic. Logfire export
only runs when `--require-logfire-export` is set, and missing credentials do not fail deterministic validation.

Optional Logfire export verification path:

```bash
LOGFIRE_TOKEN=<write-token> \
LOGFIRE_PROJECT_URL=<safe-project-or-trace-url> \
LOGFIRE_BASE_URL=<optional-self-managed-url> \
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-logfire-run.json \
  --require-logfire-export \
  --pretty
```

## Self-Hosted Langfuse Ingestion

T027 uses Langfuse as the self-hosted LLM observability target. Fixture validation still passes without a running
Langfuse service, but a service-backed proof run can require OTLP ingestion and trace lookup:

```bash
LANGFUSE_BASE_URL=http://localhost:3000 \
LANGFUSE_PUBLIC_KEY=<pk-lf-...> \
LANGFUSE_SECRET_KEY=<sk-lf-...> \
LANGFUSE_PROJECT_ID=<optional-project-id> \
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-langfuse-run.json \
  --require-langfuse-ingestion \
  --pretty
```

The command posts OTLP/HTTP JSON to `LANGFUSE_BASE_URL/api/public/otel/v1/traces`, verifies the trace through the
Langfuse public API, and preserves a repo-local `.trace.json` file next to the run artifact as the deterministic
fallback artifact. Credentials alone do not send Langfuse traffic; ingestion only runs when
`--require-langfuse-ingestion` is set. See
`docs/orchestration/self-hosted-langfuse.md` for the local or VPS Docker Compose profile, ports, secrets, reset flow,
and troubleshooting.

Common deterministic-run failures:

- Missing fixture path: rerun from the repo root or pass an absolute `--fixture` path.
- Invalid fixture JSON: keep the fixture categories aligned with `docs/comparison-evidence.md`.
- Missing output directory permission: choose a writable `--output` path under `.agent-runs/verifications/`.
- Missing Langfuse service or keys: omit `--require-langfuse-ingestion` for deterministic fixture validation, or start
  the self-hosted Langfuse profile and export `LANGFUSE_BASE_URL`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_SECRET_KEY`.
- Durable smoke failure before resume: remove the temporary DBOS SQLite file and side-effect log, then rerun the smoke
  command so it starts with a fresh workflow id and local DBOS state.

## Evidence Required

The implementation sequence should produce:

- a runnable command for the candidate demo;
- a passing shared behavior-contract or fixture check;
- repo-local OpenTelemetry evidence for the workflow run, plus self-hosted Langfuse ingestion when services are
  available;
- Pydantic Evals output tied to the same run and trace;
- setup notes covering required services, environment variables, and local startup;
- explicit gaps for self-hosted observability, evaluation, durable execution, scalability, and operating risk.

Use `docs/comparison-evidence.md` as the evidence checklist and `docs/evaluation-criteria.md` as the scoring rubric.

## Non-Goals

Do not prove cloud-hosted Logfire, live model or model-judge evals, production DBOS storage, human-wait workflows, or
worker scaling in this scaffold. Do not declare Pydantic AI plus Langfuse/OpenTelemetry plus DBOS as the final
architecture until comparable implementation evidence exists.
