# Goal 001: Self-Hosted Observability And Evaluation Control Plane

## Objective

Build the project-owned LLM observability and evaluation control plane for agent work. The end state is not generic
trace export. The end state is that traces, tool calls, prompts, scores, datasets, run artifacts, and review evidence
are inspectable in a self-hosted LLM observability product, with repo-local artifacts as deterministic fallback.

## Why This Matters

Agent work cannot be trusted or improved if traces and evaluations are hidden in ad hoc JSON files or third-party cloud
projects. This project needs observability that is self-hostable, LLM-aware, tied to runs and tickets, and good enough
for human review and automated regression checks.

## Product Iteration

This goal turns observability from a local trace artifact into a product capability. Langfuse is the default target
because it is self-hostable, LLM-specific, and already fits the LangGraph baseline. Phoenix and Opik remain comparison
alternatives if Langfuse proves too operationally heavy.

## Scope

- Prove local or self-hosted Langfuse ingestion for `apps/pydantic-ai`.
- Keep OpenTelemetry as the transport layer, not the final user experience.
- Preserve deterministic fixture validation without Langfuse credentials or running services.
- Record repo-local fallback trace and evaluation artifacts for every tested run.
- Add Pydantic Evals output tied to the same run and trace identity.
- Update comparison scoring to distinguish generic trace export from product-grade LLM observability.
- Document service topology, startup, ports, secrets, storage, reset, and troubleshooting.

## Task Backlog

1. Review current T022/T027/T023 state and confirm the selected trace identity contract.
2. Define the minimal self-hosted Langfuse local deployment profile for development.
3. Add setup docs for Langfuse service count, ports, env vars, storage, and reset flow.
4. Add a Pydantic AI trace exporter path that can send to Langfuse over OTLP.
5. Preserve the repo-local `.trace.json` artifact as deterministic fallback.
6. Add a fixture-safe mode that records Langfuse as unavailable without failing validation.
7. Add an explicit `--require-langfuse-ingestion` or equivalent proof mode for service-backed runs.
8. Prove one local Langfuse-backed run from `apps/pydantic-ai` and record the trace URL or local project path.
9. Add Pydantic Evals fixture output tied to the same run id and trace id.
10. Record evaluation scores in a repo-local artifact and, when available, in Langfuse.
11. Update `docs/comparison-evidence.md` so LLM-aware observability is the strong-evidence path.
12. Update `docs/evaluation-criteria.md` to cap observability when only generic traces exist.
13. Update `docs/requirements-matrix.md` with Langfuse-backed Pydantic AI evidence and gaps.
14. Add workflow fixture assertions for trace, eval, fallback, and service-unavailable behavior.
15. Record follow-up blockers if Langfuse is too heavy and Phoenix or Opik needs a comparison slice.

## Definition Of Done

- A reviewer can inspect a tested Pydantic AI run in a self-hosted or local Langfuse instance.
- The same run has repo-local run, trace, and eval artifacts.
- Fixture validation passes without Langfuse credentials or services.
- The docs explain how to start, stop, reset, and troubleshoot the observability stack.
- The matrix distinguishes product-grade LLM observability from generic OTel export.
- Follow-up Beads tickets exist for any remaining Phoenix, Opik, or Langfuse operation gaps.

## Proof Commands

```bash
uv run awf workflow-fixture-test
uv run awf repo-hygiene
uv run awf workflow-state-lint --json
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-run.json \
  --pretty
```

Service-backed Langfuse proof command from T027:

```bash
LANGFUSE_BASE_URL=http://127.0.0.1:13300 \
LANGFUSE_PUBLIC_KEY=<project-public-key> \
LANGFUSE_SECRET_KEY=<project-secret-key> \
LANGFUSE_PROJECT_ID=self-hosted-agents-pydantic-ai \
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-langfuse-run.json \
  --require-langfuse-ingestion \
  --pretty
```

T027 evidence lives in `.agent-runs/verifications/verify-langfuse-t027-20260531.json`.

T023 Pydantic Evals evidence:

- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json`
- `.agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json`

## Review Blocking Criteria

- The only observability proof is local JSON without an LLM-aware UI.
- A cloud-hosted service is required to pass acceptance.
- Trace ids, run ids, eval ids, and Beads evidence cannot be correlated.
- Setup requires undocumented services, secrets, ports, or persistent storage.
- The repo declares a final platform winner before comparable evidence exists.

## Kickoff Prompt

```text
/goal Execute docs/goals/001-self-hosted-observability-evaluation-control-plane.md
in /Users/nroth/workspace/self-hosted-agents. Start by reconciling T027 and T023
into a focused spec/task plan, then implement one Beads ticket at a time. Use
self-hosted Langfuse as the default LLM observability target, preserve
deterministic fixture validation, and prove trace/eval correlation with repo-local
fallback artifacts.
```
