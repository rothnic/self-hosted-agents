# Goal 004 T001 Candidate Evidence Audit

Date: 2026-06-02

Presenter: codex-goal004-t001

Work item: `awf-uy0`

Objective: `agentic-development-foundation`

Spec: `005-candidate-platform-decision-product-baseline`

Task: T001, audit current LangGraph Python, Pydantic AI, and Mastra TypeScript evidence against
`docs/comparison-evidence.md`.

Acceptance command: `uv run awf workflow-fixture-test`

## Audit Inputs

- `docs/comparison-evidence.md`
- `docs/requirements-matrix.md`
- `apps/langgraph-python/README.md`
- `apps/langgraph-python/implementation-plan.md`
- `apps/pydantic-ai/README.md`
- `apps/pydantic-ai/implementation-plan.md`
- `apps/mastra-ts/README.md`
- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.json`
- `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json`
- `.agent-runs/verifications/verify-langfuse-t027-20260531.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json`
- `.agent-runs/verifications/verify-pydantic-evals-t023-20260531.json`
- `.agent-runs/verifications/verify-durable-options-t024-20260531.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t025-20260531.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t010-20260602.json`

The audit also reran the LangGraph deterministic fixture as transient evidence:

```bash
python3 apps/langgraph-python/run.py \
  --fixture packages/comparison/fixtures/langgraph-python-decision-slice.json \
  --output /tmp/goal-004-t001-langgraph-python-run.json \
  --pretty
```

That command passed and produced run `run-ee283d60c76a866b84bfaa53`, trace
`trace-fe8ff3cbf135e5b0e7e81cf3`, and eval `eval-c7acb33558860147`. The generated artifacts were left in `/tmp`
because T001 is an audit slice, not the matrix-normalization or evidence-storage slice.

## Evidence Status Legend

- `proven`: current repo state contains implementation evidence that satisfies the checklist item.
- `partial`: implementation evidence exists, but a required comparison or promotion property is missing.
- `missing`: no runnable or inspectable implementation evidence exists in current repo state.
- `deferred`: repo state intentionally positions the item as future contrast or follow-up work.

## Candidate Summary

### LangGraph Python

Overall status: `partial`.

Implementation evidence exists for the minimum deterministic comparable demo, but it is not yet comparable to the
Pydantic AI lane for self-hosted observability or durable execution.

- Run artifact: `partial`. The app is runnable through `apps/langgraph-python/run.py` and the 2026-06-02 audit rerun
  produced a passing deterministic fixture artifact in `/tmp`. The committed durable evidence is currently the
  requirements-matrix summary and app-local setup docs, not a committed `.agent-runs/verifications` candidate artifact.
- Trace evidence: `partial`. The audit rerun produced a local OpenTelemetry-style JSON trace with four graph spans:
  `load_context`, `map_functional_needs`, `select_slice`, and `format_run`. Langfuse ingestion, model-call spans,
  token/cost fields, failure views, and a reviewer-inspectable self-hosted trace UI are not proven.
- Evaluation evidence: `partial`. The deterministic assertion scorer passed with score `5/5` in the audit rerun and in
  the matrix summary. Dataset, model-judge, annotation, and trace-linked eval UI evidence are not proven.
- Setup and operating evidence: `partial`. `apps/langgraph-python/README.md` documents the local fixture command and
  sibling trace/eval artifacts. Self-hosted Langfuse setup effort, service count, reset, recovery, and secrets handling
  are not measured for this candidate.
- Durable execution evidence: `missing`. The implementation plan explicitly keeps persistence, retries, queues,
  schedulers, and long-running recovery outside the first slice.
- Gap evidence: `proven`. `apps/langgraph-python/implementation-plan.md` and `docs/requirements-matrix.md` record the
  observability, evaluation, durable execution, and scalability gaps.

T001 finding: LangGraph Python remains a useful first-candidate slice, but it is not final-solution comparable until
self-hosted trace ingestion and durable execution are exercised from the tested candidate path.

### Pydantic AI

Overall status: `proven` for tested candidate-slice comparison and `partial` for final-solution promotion.

Pydantic AI has the strongest current implementation evidence because run, trace, evaluation, self-hosted Langfuse, and
local DBOS durable proof are all represented by committed artifacts.

- Run artifact: `proven`. `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.json` records
  `run-e545699517a2885613711cf9` in deterministic fixture mode. The evaluated rerun artifact is
  `.agent-runs/verifications/pydantic-ai-evals-run-20260531.json`.
- Trace evidence: `proven` for self-hosted-compatible candidate-slice observability. The repo-local trace artifact is
  `.agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json`, with local trace
  `trace-573f0157f5d65ccdc1c963d4` and OTLP trace `735c1665d723b965ef77950eeeac36df`. The verification artifact
  `.agent-runs/verifications/verify-langfuse-t027-20260531.json` records self-hosted Langfuse ingestion through the
  tested app path, HTTP 200 ingestion, and HTTP 200 trace retrieval.
- Evaluation evidence: `proven`. `.agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json` records
  Pydantic Evals result `eval-a584886d68bad6f4`, score `5/5`, and correlation to the same run and trace identities.
- Setup and operating evidence: `proven` for fixture and service-backed proof. `apps/pydantic-ai/README.md` documents
  fixture, explicit trace/eval output, and DBOS smoke commands. `docs/orchestration/self-hosted-langfuse.md` documents
  the self-hosted Langfuse service shape used by T027.
- Durable execution evidence: `proven` for local durable proof. The T010 DBOS artifact records retry, resume,
  preserved workflow identity, side-effect idempotency, review wait, accepted-review resume, and artifact correlation:
  `.agent-runs/verifications/pydantic-ai-durable-smoke-t010-20260602.json`. The earlier DBOS smoke proof is
  `.agent-runs/verifications/pydantic-ai-durable-smoke-t025-20260531.json`.
- Gap evidence: `proven`. The implementation plan, README, and matrix preserve explicit promotion blockers: production
  DBOS storage, worker topology, queue behavior, recovery operations, Langfuse operating recovery, live model/tool
  traces, token/cost/failure coverage, and broader eval workflows.

T001 finding: Pydantic AI is the only candidate with committed evidence across every comparison checklist category.
It still should not be called the final solution until Goal 004 scores it against alternatives and records the platform
decision with independent reviewer acceptance.

### Mastra TypeScript

Overall status: `missing` for implementation evidence and `deferred` as a contrast lane.

Mastra TypeScript currently has only planning/setup intent in `apps/mastra-ts/README.md`.

- Run artifact: `missing`. There is no runnable Mastra app file, package manifest, shared fixture, or committed run
  artifact under `apps/mastra-ts/`.
- Trace evidence: `missing`. There is no Mastra trace export, self-hosted backend proof, or local trace artifact.
- Evaluation evidence: `missing`. There is no deterministic fixture or eval artifact for Mastra.
- Setup and operating evidence: `partial`. The README states the intended contrast and evidence categories, but it does
  not document install commands, package management, services, env vars, reset, or recovery.
- Durable execution evidence: `missing`. No runtime, retry, resume, review wait, or side-effect behavior is proven.
- Gap evidence: `proven`. The README explicitly positions the lane as future contrast and records cross-language
  maintenance cost as a risk to measure.

T001 finding: Mastra must not be scored as implementation-proven. It can only be used as a documented contrast option
until T002 decides whether a runnable contrast slice is required before platform selection.

## Downstream Implications

- T002 should make an explicit decision on Mastra. If Goal 004 needs cross-language implementation proof before a
  platform decision, Mastra needs a runnable contrast slice. If the decision can be Python-first from current evidence,
  Mastra should be deferred with the missing-evidence rationale above.
- T003 should normalize the matrix without inflating transient LangGraph evidence into committed evidence. The matrix
  should distinguish "runnable in audit" from "durably committed verification artifact".
- T004 scoring should treat Pydantic AI as the current strongest implementation-backed candidate while preserving final
  promotion caps for production DBOS, Langfuse operations, live model/tool traces, and richer eval workflows.
- T007 and T014 should apply the presenter/reviewer pattern: one agent presents decision or goal evidence and a
  separate reviewer agent records acceptance or rejection.

## T001 Presenter Conclusion

The audit satisfies FR-001 and FR-002 for the current state:

- LangGraph Python has partial implementation evidence for a deterministic comparable demo.
- Pydantic AI has proven tested-candidate evidence across run, trace, eval, setup, durable, and gap categories.
- Mastra TypeScript has no runnable implementation evidence and remains deferred unless T002 requires a contrast slice.

This is an evidence audit only. It does not choose the primary platform and does not close any final-solution promotion
blockers.

## Independent Reviewer Acceptance

Reviewer agent id: `codex-independent-reviewer-goal004-t001`

Review agent path: `019e8801-0bb4-7573-9659-609c5319f924`

Outcome: `accepted`

Evidence checked:

- `.agent-runs/reports/goal-004-t001-candidate-evidence-audit-20260602.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `specs/005-candidate-platform-decision-product-baseline/tasks.md`
- `docs/comparison-evidence.md`
- `docs/requirements-matrix.md`
- `apps/langgraph-python/README.md`
- `apps/langgraph-python/implementation-plan.md`
- `apps/pydantic-ai/README.md`
- `apps/pydantic-ai/implementation-plan.md`
- `apps/mastra-ts/README.md`
- `.agent-runs/verifications/verify-langfuse-t027-20260531.json`
- `.agent-runs/verifications/verify-pydantic-evals-t023-20260531.json`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t010-20260602.json`
- A reviewer rerun of the LangGraph fixture to confirm the transient `/tmp` evidence shape and deterministic ids.

Reviewer findings:

- No blocking findings.
- The report satisfies T001 and distinguishes `proven`, `partial`, `missing`, and `deferred` evidence states.
- LangGraph `partial`, Pydantic AI `tested candidate slice proven / final promotion partial`, and Mastra
  `missing/deferred` are supported by repo artifacts.
- Deterministic validation remains repo-local without hosted credentials.
- The only service-backed observability proof is recorded as a self-hosted Langfuse stack, not a cloud dependency.

Required follow-up tickets:

- None for T001 acceptance.
- Continue existing Goal 004 follow-ups T002, T003, and T004 for Mastra disposition, matrix normalization, and candidate
  scoring without turning this audit into a platform decision.
