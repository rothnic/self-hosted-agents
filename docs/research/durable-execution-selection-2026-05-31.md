# Durable Execution Selection For The Pydantic AI Lane

Date checked: 2026-05-31

## Research Question

Which durable execution option should T025 implement first for the tested `apps/pydantic-ai` lane so the project can
prove retry or resume behavior without adding unnecessary self-hosted infrastructure?

## Decision

Select **Pydantic AI plus DBOS** for the T025 durable smoke path.

This is not a final platform decision. It is the lowest-complexity viable next proof because DBOS is a native Pydantic
AI durable execution integration, can run in the application process, supports SQLite for local examples, and moves to a
database-backed production path without introducing a separate workflow server for the first smoke.

## Current Repo Evidence

- `apps/pydantic-ai` already has deterministic run, trace, self-hosted Langfuse, and Pydantic Evals artifacts.
- The local installed `pydantic-ai==1.104.0` package exposes module specs for `pydantic_ai.durable_exec.dbos`,
  `pydantic_ai.durable_exec.prefect`, and `pydantic_ai.durable_exec.temporal`.
- `from pydantic_ai.durable_exec.dbos import DBOSAgent` currently fails with `ModuleNotFoundError: No module named
  'dbos'`, so T025 must add and lock the DBOS optional dependency before the smoke can run.
- The same installed package does not expose `pydantic_ai.durable_exec.restate`, even though current Pydantic docs list
  Restate as an official durable execution option. Restate remains in the comparison, but it should not be the first
  smoke for this pinned candidate without resolving that version/package boundary.
- T025 needs inspectable retry or resume evidence from command output, run artifacts, traces, or logs. It does not need
  to prove every final Goal 002 behavior in one slice.

## Comparison

### Pydantic AI + DBOS

Verdict: **select first**.

- Local setup: Python package plus SQLite for local proof; Postgres path later.
- Pydantic AI fit: native `DBOSAgent`; wraps agent run as workflow and model or MCP calls as steps.
- Recovery model: database checkpoints resume from the last completed step.
- Side-effect fit: custom tool I/O must be explicit DBOS steps, making boundaries visible.
- Observability path: DBOS and Pydantic AI can emit OTel spans correlated with existing trace ids.

### Pydantic AI + Prefect

Verdict: good fallback if DBOS step boundaries are awkward.

- Local setup: embedded worker is possible; server optional for UI and scheduling.
- Pydantic AI fit: native `PrefectAgent`; wraps agent run as flow and tools or model calls as tasks.
- Recovery model: result persistence and transactions rather than deterministic replay.
- Side-effect fit: strong task retry/cache semantics, but agent human-wait shape needs proof.
- Observability path: Prefect UI plus Logfire/OTel path, with more product surface than needed first.

### Pydantic AI + Restate

Verdict: defer until the package or version boundary is resolved.

- Local setup: requires Restate server in front of the app service.
- Pydantic AI fit: current docs show `RestateAgent`, but the installed package lacks the module.
- Recovery model: journal replay skips completed steps and resumes from the log.
- Side-effect fit: strong side-effect model through durable steps.
- Observability path: Restate service observability plus external OTel path; extra runtime boundary.

### Pydantic AI + Temporal

Verdict: too heavy for the first one-engineer smoke.

- Local setup: requires Temporal dev server plus worker.
- Pydantic AI fit: native `TemporalAgent`; strong durable workflow model.
- Recovery model: deterministic workflows plus activities; mature replay semantics.
- Side-effect fit: strong long-running and human-wait fit, but strict workflow/activity split.
- Observability path: mature visibility stack that can be correlated later.

### Hatchet

Verdict: keep as workflow-platform comparison, not the first Pydantic-specific smoke.

- Local setup: Hatchet Lite or self-hosted control plane plus worker.
- Pydantic AI fit: no native Pydantic AI wrapper; integration glue required.
- Recovery model: durable task checkpoints and replay.
- Side-effect fit: strong event waits, durable tasks, and dashboard.
- Observability path: built-in task history, traces, logs, and OTel.

## T025 Smoke Contract

Implement the smallest DBOS smoke that proves a durable property against the current Pydantic AI candidate lane:

1. Add the required DBOS dependency through `pyproject.toml` and `uv.lock`.
2. Run from a deterministic local command without hosted credentials or external model providers.
3. Use a local SQLite DBOS system database under a temp or `.agent-runs/verifications/` path.
4. Wrap the existing deterministic `pydantic_ai.Agent` path with `DBOSAgent`.
5. Include one explicit DBOS step for non-deterministic or side-effect-like work.
6. Force a controlled first-attempt failure and prove the rerun resumes without duplicating the completed step.
7. Write a repo-local durable evidence artifact linking:
   - DBOS workflow/run id;
   - Pydantic AI run id;
   - trace id;
   - eval id if the same run is evaluated;
   - command used;
   - SQLite path or temp-path policy;
   - side-effect counter or log proving non-duplication.

Human wait behavior may be simulated in T025 only if it stays small. If it would broaden the smoke too much, record it
as the next Goal 002 follow-up after retry/resume proof.

## Rejected First-Smoke Paths

- Do not start with Temporal unless DBOS cannot express the needed retry/resume proof. Temporal is likely the strongest
  scale fallback, but it adds a server, worker, deterministic workflow constraints, and more setup than T025 needs.
- Do not start with Restate until the repo's pinned package exposes the documented integration or the task explicitly
  chooses the Restate SDK integration boundary.
- Do not start with Hatchet for the Pydantic AI-specific smoke because it is not a native Pydantic AI integration. It
  remains a serious candidate for the later autonomous multi-agent delivery loop.
- Do not use Prefect first unless DBOS fails the smoke, because Prefect's broader orchestration surface is useful but
  larger than the first durable proof requires.

## Sources

- Pydantic AI durable execution overview: https://pydantic.dev/docs/ai/integrations/durable_execution/overview/
- Pydantic AI DBOS integration: https://pydantic.dev/docs/ai/integrations/durable_execution/dbos/
- Pydantic AI Prefect integration: https://pydantic.dev/docs/ai/integrations/durable_execution/prefect/
- Pydantic AI Restate integration: https://pydantic.dev/docs/ai/integrations/durable_execution/restate/
- Pydantic AI Temporal integration: https://pydantic.dev/docs/ai/integrations/durable_execution/temporal/
- DBOS docs: https://docs.dbos.dev/
- Prefect durable execution: https://www.prefect.io/solutions/durable-execution
- Hatchet durable execution: https://docs.hatchet.run/v1/durable-execution
- Hatchet self-hosting: https://docs.hatchet.run/self-hosting
