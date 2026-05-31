# Self-Hosted Agent Observability Backend

Date: 2026-05-31

## Question

What self-hosted observability backend should this project target for agent traces instead of treating generic
OpenTelemetry exports as sufficient evidence?

## Findings

Generic OpenTelemetry is the portability layer, not the product experience. It is useful as the ingestion and export
format, but agent comparison needs an LLM-aware backend that can inspect model calls, tool calls, prompts, scores,
sessions, metadata, and evaluations.

Langfuse is the strongest default for this project right now. It is open source, self-hostable with Docker Compose for
low-scale deployments, and designed around LLM traces, evaluations, prompt management, datasets, scores, and a review UI.
It can receive OTLP traces at `/api/public/otel`, including from a local deployment, and its docs include a Pydantic AI
integration path. The operating cost is real: self-hosted Langfuse uses web and worker containers plus Postgres,
ClickHouse, Redis or Valkey, and S3/blob storage. That is still a better fit than relying on a third-party hosted
project because the full stack can run on project-controlled infrastructure.

Phoenix remains the best lightweight Python-first alternative to keep in the comparison set. It is open source,
self-hosted, and built around OpenInference/OpenTelemetry tracing, experimentation, and evaluation. It may be easier for
local development than Langfuse, but it would add a second observability product to compare and is less aligned with the
existing LangGraph plus Langfuse lane.

Opik is also a credible self-hosted option for traces, evaluation, prompt engineering, and optimization. It should be
kept as a future comparison option, but switching to it now would expand the solution space more than necessary.

## Recommendation

Use self-hosted Langfuse as the primary LLM observability backend for this project, with OpenTelemetry as the transport
layer and repo-local trace artifacts as deterministic fallback evidence. T022's local OTel artifact is useful as a
portable backup, but it should not be treated as the final observability experience.

Before Pydantic Evals scoring is considered comparable, add a follow-up slice that proves the tested `apps/pydantic-ai`
candidate can emit its trace evidence into a self-hosted or locally deployed Langfuse instance. The proof should record
the local deployment shape, env vars, run id, trace id, Langfuse trace URL or local project path, and repo-local fallback
artifact path.

## Confidence

High for choosing Langfuse as the next backend target because it is self-hosted, LLM-specific, already appears in the
repo's LangGraph lane, and supports OpenTelemetry ingestion. Medium for long-term dominance because Phoenix and Opik may
prove simpler or stronger after implementation-grounded comparison.

## Sources

- Langfuse self-hosting:
  https://langfuse.com/docs/deployment/self-host
- Langfuse OpenTelemetry ingestion:
  https://langfuse.com/integrations/native/opentelemetry
- Langfuse integrations overview:
  https://langfuse.com/integrations
- Phoenix overview:
  https://arize.com/docs/phoenix/
- Phoenix OpenTelemetry setup:
  https://www.arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/setup-using-phoenix-otel
- Opik documentation:
  https://www.comet.com/docs/opik/
