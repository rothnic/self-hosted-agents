# Pydantic AI Plus Logfire Functional Needs Research

Date checked: 2026-05-23

## Research Question

Does Pydantic AI plus Logfire or a generic OpenTelemetry backend appear to satisfy the functional needs map strongly
enough to become a later runnable comparison candidate after the LangGraph Python slice, without declaring a final
platform winner now?

## Baseline

The comparison baseline is the T017 LangGraph Python evidence in `docs/requirements-matrix.md`. That evidence proves a
deterministic fixture run, local OTel-style trace artifact, deterministic evaluation artifact, and one-command local
validation path. It does not yet prove hosted or self-hosted Langfuse ingestion, real model/tool spans, dataset evals,
durable execution, persistence, deployment topology, or production recovery.

Any Pydantic AI candidate must preserve the same deterministic fixture validation path without hosted credentials.
Logfire or hosted observability should be additive evidence, not a prerequisite for `uv run awf workflow-fixture-test`.

## Findings

Pydantic AI remains a strong Python-first research candidate. Its current docs describe a Python agent framework for
production-grade GenAI applications and workflows, with model-agnostic support, type-safe development, Pydantic Logfire
observability, evals, capabilities, MCP, A2A, human approval, durable execution, streaming outputs, and graph support.
This maps directly to R1, R3, R4, R7, and R9, but those claims are still framework/documentation evidence until a
runnable candidate slice proves them in this repository.

Pydantic AI instrumentation is based on OpenTelemetry. The docs say Pydantic AI can be monitored with any OTel backend
with GenAI support, and they show direct OTLP exporter configuration without Logfire. This is a strong fit for the
project's portability requirement, but the OpenTelemetry GenAI semantic conventions are still in development. A future
candidate should therefore record the exact instrumentation format/version and avoid depending on unstable attribute
names for fixture assertions.

Logfire is the first-party observability path and is built on OpenTelemetry. Its AI observability docs emphasize LLM
conversation panels, token tracking, cost monitoring, tool-call inspection, streaming support, multi-turn traces,
`pydantic-evals` integration, SQL access to observability data, and an MCP server. That is promising for debugging and
agent-queryable run evidence, but the project still needs to verify whether a local or self-hosted default is available
or whether Logfire is primarily hosted. If Logfire is hosted-only for the practical path, a generic OTel backend must be
the deterministic/default evidence route.

Pydantic Evals is code-first and can run from Python code, print or serialize results, and send results to Logfire when
configured. It supports datasets, cases, experiments, tasks, evaluators, deterministic/code-based checks, custom
evaluators, and span-based evaluation over OpenTelemetry traces. This is a stronger research fit for the repo's
evaluation needs than ad hoc scoring alone, but comparable evidence would still require a fixture-backed evaluation
artifact tied to the same run and trace ids.

Pydantic AI documents official durable execution integrations with Temporal, DBOS, Prefect, and Restate. The docs say
these integrations support progress preservation across failures and restarts, long-running asynchronous workflows, and
human-in-the-loop workflows. This is a better research fit for durable execution than the current LangGraph fixture
slice, but it adds an architecture choice. A future runnable candidate should not adopt one durable runtime silently;
it should first prove the local fixture path, then evaluate one durable runtime as explicit follow-up evidence.

## Functional Needs Fit

| Functional Area | Pydantic AI Plus Logfire/OTel Research Evidence | Research Fit | Risks And Gaps |
| --- | --- | --- | --- |
| Agent orchestration | Agents, capabilities, and graph support are documented as first-class Pydantic AI features | Strong | Needs a runnable comparable workflow before scoring against LangGraph |
| Tool and context access | Tool/dependency injection, capabilities, MCP, A2A, and approval hooks map to typed adapters | Strong | Needs repo-local security testing |
| Observability | Pydantic AI emits OTel instrumentation; Logfire provides first-party AI observability | Strong | Logfire hosting/self-hosting posture and generic OTel backend quality need proof |
| Evaluation | Pydantic Evals provides datasets, cases, evaluators, experiments, serialization, and Logfire integration | Strong | Needs fixture artifacts tied to run and trace ids |
| Evidence storage | Evals can serialize reports; Logfire offers UI and SQL access to telemetry | Medium | Repo-local artifact contract remains necessary without hosted credentials |
| Durable execution | Official Temporal, DBOS, Prefect, and Restate integrations map to recovery needs | Strong | Runtime selection is a separate architecture decision |
| Operator experience | Python-first typed API and first-party instrumentation may reduce glue | Medium | Service count, secrets, local UI, and recovery steps are unmeasured |
| Scalability path | Durable integrations plus OTel export give a plausible route to production services | Strong | Deployment topology and storage model require implementation evidence |

## Preliminary Rubric View

These are research-only directional scores. They must not be treated as implementation scores until a candidate app
produces the evidence required by `docs/comparison-evidence.md`.

| Criterion | Directional Score | Evidence Basis | Gap Or Cap |
| --- | --- | --- | --- |
| Infrastructure ownership | 3 | Logfire, OTel, Pydantic Evals, and durable integrations cover several platform needs | Cap to 2 if no local OTel viewer/store is selected |
| Observability | 3 | First-party Logfire path plus generic OTel export and GenAI semantic conventions | OTel GenAI conventions are still in development; local review path must be proven |
| Evaluation | 3 | Code-first eval datasets, evaluators, experiments, serialization, and span-based eval support | Must prove trace-linked deterministic fixture evals in repo artifacts |
| Scalability | 3 | Official durable execution integrations offer clear durable workflow options | Runtime choice and service topology remain unapproved |
| Operating effort | 2 | Python-first ergonomics are promising | Real bootstrap, secrets, service count, and failure recovery are unknown |

## Recommendation

Keep Pydantic AI plus Logfire/OpenTelemetry as a strong next Python-first research candidate, but do not promote it to a
platform winner or create an app lane from research alone. The next implementation decision should compare whether its
typed agent ergonomics, code-first evals, OTel portability, and durable execution integrations address the explicit
gaps left by the LangGraph Python T017 evidence.

If the roadmap approves a future Pydantic AI slice, it should start with the same comparable-agent workflow and produce:

- a deterministic fixture command with no hosted credentials;
- a repo-local run artifact, OTel trace export, and eval artifact tied by stable ids;
- setup notes for Logfire and at least one generic local OTel backend;
- explicit gap notes for durable runtime choice, Logfire hosting posture, and OTel semantic-convention stability.

## Sources

- Pydantic AI overview: https://pydantic.dev/docs/ai/overview/
- Pydantic AI Logfire and OpenTelemetry integration: https://pydantic.dev/docs/ai/integrations/logfire/
- Pydantic AI durable execution overview: https://pydantic.dev/docs/ai/integrations/durable_execution/overview/
- Pydantic Evals: https://pydantic.dev/docs/ai/evals/evals/
- Logfire AI and LLM observability: https://pydantic.dev/docs/logfire/get-started/ai-observability/
- OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
