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

Goal 002 uses Pydantic AI's DBOS integration as the first durable execution proof. The smoke uses local SQLite DBOS
state, runs a controlled transient failure inside a retry-enabled DBOS step, starts a workflow in one child process,
kills that process after a completed side-effect step, then starts a second child process against the same DBOS
database. The resumed workflow completes through `DBOSAgent` and proves the side-effect step was not duplicated.

This is a local proof path, not a production DBOS topology. SQLite is intentionally used for deterministic fixture
validation. Production storage, worker topology, queues, backups, reset policy, and recovery rehearsal remain Goal 002
follow-up work before DBOS can be considered production-ready.

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
  --output .agent-runs/verifications/pydantic-ai-durable-smoke-t006-20260602.json \
  --db-path /tmp/pydantic-ai-dbos-t006.sqlite \
  --side-effect-log /tmp/pydantic-ai-dbos-side-effect-t006.jsonl \
  --retry-state-log /tmp/pydantic-ai-dbos-retry-t006.jsonl \
  --workflow-id dbos-workflow-t006-side-effect-idempotency \
  --issue-id awf-9cq \
  --pretty
```

Current durable evidence:

- `.agent-runs/verifications/pydantic-ai-durable-smoke-t025-20260531.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t004-20260602.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t005-20260602.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t006-20260602.json`

### DBOS Local Setup

The DBOS smoke is run through the repo `uv` environment. No DBOS server, queue worker, model provider, Langfuse
service, Logfire project, or cloud credential is required.

Local prerequisites:

- Run from the repo root so imports resolve through the app package boundary.
- Keep dependencies installed through the repo `uv` environment.
- Use a writable SQLite path for `--db-path`.
- Use a writable JSONL path for `--side-effect-log`.
- Keep DBOS state paths outside git, usually under `/tmp`.

Useful setup checks:

```bash
uv run python -c "from pydantic_ai.durable_exec.dbos import DBOSAgent; print(DBOSAgent.__name__)"
uv run python apps/pydantic-ai/durable_smoke.py --help
```

The first check proves the optional DBOS dependency is installed and the Pydantic AI DBOS wrapper imports. The second
check shows the supported local smoke flags.

### DBOS State And Reset

The smoke creates local, disposable state:

- `--db-path`: SQLite DBOS system database containing workflow status and completed steps.
- `--retry-state-log`: JSONL proof that the retry-enabled DBOS step failed once and then completed.
- `--side-effect-log`: JSONL proof that the side-effect step ran exactly once.
- `<workflow-id>.side-effect-step-complete.json`: marker written after the DBOS side-effect step returns.
- `<workflow-id>.child-result.json`: child-process recovery output used to build the final evidence artifact.

Use a fresh `--workflow-id` or delete all five local files before rerunning the same explicit workflow id. Reusing a
workflow id with stale SQLite state is useful for recovery inspection, but it is not a clean smoke.

Reset the fixed T006 local paths:

```bash
rm -f /tmp/pydantic-ai-dbos-t006.sqlite \
  /tmp/pydantic-ai-dbos-side-effect-t006.jsonl \
  /tmp/pydantic-ai-dbos-retry-t006.jsonl \
  /tmp/dbos-workflow-t006-side-effect-idempotency.side-effect-step-complete.json \
  /tmp/dbos-workflow-t006-side-effect-idempotency.child-result.json
```

The committed evidence artifact under `.agent-runs/verifications/` is durable review evidence and should not be deleted
as part of local reset.

### DBOS Recovery Evidence

The smoke proves retry and recovery by running a DBOS step that fails once and then succeeds on retry, starting the DBOS
workflow in a child process, waiting for the explicit side-effect step marker, killing that child, and then launching a
second child with `PYDANTIC_AI_DBOS_RESUME_READY=1` against the same SQLite database.

The evidence artifact should show:

- `durable_property.retry_proven=true`
- `durable_property.resume_proven=true`
- `durable_property.run_identity_preserved=true`
- `durable_property.side_effect_idempotency_proven=true`
- `durable_property.completed_step_not_duplicated=true`
- `identity.requested_workflow_id`, `identity.first_attempt_workflow_id`, `identity.resume_attempt_workflow_id`,
  `identity.workflow_status_workflow_id`, and `identity.workflow_result_workflow_id` are the same value
- `side_effect.idempotency.before_resume_line_count=1`
- `side_effect.idempotency.after_resume_line_count=1`
- `side_effect.idempotency.resume_duplicate_count=0`
- `side_effect.idempotency.retry_failure_count_before_side_effect=1`
- `side_effect.idempotency.retry_success_count_before_side_effect=1`
- `side_effect.idempotency.workflow_result_event_matches_log=true`
- `retry.failure_count=1`
- `retry.success_count=1`
- `retry.line_count=2`
- `first_attempt.side_effect_step_returned_before_kill=true`
- `first_attempt.exit_code` is nonzero because the first child was killed
- `resume_attempt.exit_code=0`
- `side_effect.line_count=1`
- `dbos.workflow_status.status=SUCCESS`
- `dbos.workflow_status.recovery_attempts` is present
- `dbos.workflow_steps` includes `controlled_retry_once`, `record_side_effect_once`, `controlled_resume_wait`, and the
  DBOS agent run

Inspect the current T006 evidence summary:

```bash
python3 - <<'PY'
import json
from pathlib import Path

path = Path(".agent-runs/verifications/pydantic-ai-durable-smoke-t006-20260602.json")
artifact = json.loads(path.read_text())
print(json.dumps({
    "workflow_id": artifact["dbos"]["workflow_id"],
    "retry_proven": artifact["durable_property"]["retry_proven"],
    "resume_proven": artifact["durable_property"]["resume_proven"],
    "run_identity_preserved": artifact["durable_property"]["run_identity_preserved"],
    "side_effect_idempotency_proven": artifact["durable_property"]["side_effect_idempotency_proven"],
    "first_attempt_workflow_id": artifact["identity"]["first_attempt_workflow_id"],
    "resume_attempt_workflow_id": artifact["identity"]["resume_attempt_workflow_id"],
    "completed_step_not_duplicated": artifact["durable_property"]["completed_step_not_duplicated"],
    "retry_failure_count": artifact["retry"]["failure_count"],
    "retry_success_count": artifact["retry"]["success_count"],
    "side_effect_count": artifact["side_effect"]["line_count"],
    "side_effect_before_resume_count": artifact["side_effect"]["idempotency"]["before_resume_line_count"],
    "side_effect_after_resume_count": artifact["side_effect"]["idempotency"]["after_resume_line_count"],
    "resume_duplicate_count": artifact["side_effect"]["idempotency"]["resume_duplicate_count"],
    "workflow_status": artifact["dbos"]["workflow_status"].get("status"),
    "recovery_attempts": artifact["dbos"]["workflow_status"].get("recovery_attempts"),
}, indent=2))
PY
```

### DBOS Troubleshooting

- `ModuleNotFoundError: No module named 'dbos'`: run through `uv` from this repo so the locked optional dependency is
  available.
- SQLite path errors: choose a writable `--db-path`, keep parent directories present, and avoid paths inside read-only
  worktrees.
- Stale workflow result, missing retry event, or unexpected side-effect count: remove the SQLite DB, retry log,
  side-effect log, side-effect marker, and child-result JSON before rerunning the same workflow id.
- Resume timeout: confirm the first child reached the marker file. If it did not, inspect `first_attempt.stderr_excerpt`
  in the output artifact and rerun after reset.
- `side_effect.line_count` greater than `1`: treat the run as failed evidence. Reset local state and inspect whether the
  side-effect step is still protected by the DBOS step boundary before closing durable work.
- DBOS logs mention DBOS Conductor: the local smoke does not require the hosted console URL printed by DBOS logs.
- SQLite production warning: expected for this smoke. Goal 002 must still document and prove a production storage path
  before final runtime promotion.

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
- Durable smoke failure before resume: remove the temporary DBOS SQLite file, side-effect log, marker, and child-result
  JSON, then rerun the smoke command so it starts with a fresh workflow id and local DBOS state.

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

Do not prove cloud-hosted Logfire, live model or model-judge evals, production DBOS storage, review-wait workflows, or
worker scaling in this scaffold. Do not declare Pydantic AI plus Langfuse/OpenTelemetry plus DBOS as the final
architecture until comparable implementation evidence exists.
