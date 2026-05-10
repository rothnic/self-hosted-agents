# LLM Observability Solution Space

Date checked: 2026-05-10

## Research Question

Given a Python-preferring engineer who cannot assume approval or budget for self-hosted LangSmith, what observability
and evaluation options should be considered while mapping high-level system requirements into comparable agent app
implementations?

## Findings

LangSmith remains relevant as a baseline because it is tightly aligned with LangChain and LangGraph workflows, but
self-hosted LangSmith is positioned as an Enterprise capability. That makes it a constraint and comparison baseline,
not the default assumption for this project.

Langfuse is an open-source LLM engineering platform with self-hosting documentation. It is a strong candidate when the
project needs traces, prompt/evaluation workflows, and a productized observability surface without depending on
LangSmith.

Arize Phoenix is open source and centered on tracing, evaluation, datasets, and OpenInference/OpenTelemetry-style
instrumentation. It is a strong Python-first candidate for local development and implementation-grounded comparison.

MLflow has GenAI tracing documentation and OpenTelemetry-oriented integrations. It may fit if broader experiment
tracking, model/evaluation lifecycle, and Python ecosystem alignment matter more than a purpose-built LLM observability
UI.

OpenTelemetry and OpenInference should be treated as important shared instrumentation concepts. They can reduce lock-in
by making traces and evaluation evidence comparable across app candidates.

## Initial Candidate Map

| Candidate | Why It Matters | Early Risk |
| --- | --- | --- |
| LangGraph Python plus Langfuse | Python orchestration with self-hostable LLM observability | Integration quality must be proven |
| LangGraph Python plus Phoenix | Python-first tracing/evaluation with OpenInference alignment | Defer until developer experience is better understood |
| Python app plus MLflow tracing | Strong Python lifecycle story and broader experiment tooling | LLM-agent UX may be less specialized |
| Mastra TypeScript plus shared contracts | Useful cross-language comparison against Python-first choices | Lower fit with Python preference |
| LangSmith | Best-known LangChain baseline | Self-hosted access may require Enterprise approval |

## Candidate Integration Notes

### LangGraph Python Plus Langfuse

Integration mechanism: use Langfuse's LangChain/LangGraph integration or OpenTelemetry endpoint so the candidate app
can emit traces without depending on LangSmith. The first demo should prove one LangGraph workflow can emit model,
tool, retrieval, and final-answer evidence into a local or low-scale Langfuse deployment.

Self-host story: Langfuse is open source and documents Docker-based self-hosting. Local Docker Compose is a good
comparison target, but production-scale Langfuse introduces real platform components: Postgres, ClickHouse,
Redis/Valkey, S3/blob storage, workers, and operational expectations.

Evidence to gather in the implementation slice:

- Setup steps and services required for a fresh local run.
- Whether LangGraph spans are readable enough for debugging node decisions.
- Whether prompt, score, dataset, and evaluation workflows are usable without LangSmith.
- Whether trace export can stay provider-neutral through OpenTelemetry.

Likely fit: strong first candidate if the project wants a productized observability UI and accepts operating a
multi-service stack later.

### LangGraph Python Plus Phoenix And OpenInference

Integration mechanism: instrument LangChain/LangGraph with `openinference-instrumentation-langchain`, export spans over
OTLP, and inspect them in Phoenix. Phoenix can run locally with `python -m phoenix.server.main serve` or
`phoenix serve`, which makes it a strong early demo path.

Self-host story: Phoenix documents free self-hosting with no feature gates, local terminal and Docker options, and a
privacy model where data stays in the user's infrastructure. This is the closest match for quick local validation.

Evidence to gather in the implementation slice:

- Whether a Python agent can emit complete traces with minimal app-specific instrumentation.
- Whether OpenInference span conventions capture the details we care about: model calls, retrieval, tool use, latency,
  token usage, inputs, outputs, and session context.
- Whether evaluation workflows can attach scores or annotations to the same traces used for debugging.
- Whether the same instrumentation can later export to another OpenTelemetry-compatible backend.

Likely fit: later Python-first comparison candidate. It has attractive open instrumentation properties, but the next
roadmap step should not depend on Phoenix until the developer experience is better understood.

### Python App Plus MLflow Tracing

Integration mechanism: use MLflow's GenAI tracing and `mlflow.langchain.autolog()` for LangChain/LangGraph-adjacent
work. MLflow can capture nested traces to the active experiment and run against a local tracking server.

Self-host story: MLflow is familiar in Python and broader model lifecycle work. It may be easier to justify when the
project also needs experiments, model artifacts, datasets, and evaluation records rather than only LLM trace inspection.

Evidence to gather in the implementation slice:

- Whether MLflow traces give enough agent-specific debugging detail without extra custom spans.
- Whether evaluation outputs and implementation comparison results fit naturally into experiments.
- Whether the local UI supports the desired CEO-level demo review without custom reporting.
- How much LangGraph-specific support is available versus generic LangChain tracing.

Likely fit: useful baseline for Python lifecycle integration, but probably not the first observability candidate unless
experiment tracking becomes the dominant requirement.

### Mastra TypeScript Plus Shared Contracts

Integration mechanism: use Mastra's built-in observability for agent runs, workflow steps, tool calls, model
interactions, logs, metrics, and AI tracing exporters. It supports built-in storage and external exporters including
Arize/Phoenix, Langfuse, LangSmith, and OpenTelemetry-compatible systems.

Self-host story: Mastra is not Python-first, but it gives a strong contrast case for how much workflow, tracing, eval,
and developer-experience capability a TypeScript-native agent framework provides out of the box.

Evidence to gather in the implementation slice:

- Whether the same behavior contract can be implemented with less orchestration and observability glue than Python.
- Whether the built-in traces expose comparable details to the Python candidates.
- Whether crossing into TypeScript creates unacceptable maintenance cost for a Python-preferring owner.
- Whether Mastra's exporter model helps keep observability backend choices flexible.

Likely fit: valuable contrast candidate after one Python path is proven. It should not lead the roadmap unless the
Python candidates show materially higher implementation or operating cost.

### LangSmith Baseline

Integration mechanism: use LangSmith as the known LangChain/LangGraph baseline for traces, evaluation, prompt
engineering, and deployment-adjacent workflows.

Self-host story: LangSmith documents cloud, hybrid, and self-hosted deployment under Enterprise-oriented docs. That
makes it an important comparison reference, but not an assumption for this project because approval and budget are
explicit constraints.

Evidence to gather in the implementation slice:

- Which capabilities the non-LangSmith candidates must reproduce for a solo engineer.
- Whether hosted LangSmith could still be used for a low-friction prototype if data or budget constraints allow it.
- Which features require sales, Enterprise access, or organization-level approval.

Likely fit: comparison baseline and fallback reference, not the default architecture.

## Research Confidence

Confidence is medium-high for choosing the first research direction: LangGraph Python plus Langfuse is the strongest
immediate candidate because it fits Python preference, has a self-hosting path, and offers a productized observability
surface. Phoenix/OpenInference remains worth tracking, but should be deferred until developer experience risk is reduced.
Confidence is lower for final platform selection because the decisive evidence should come from running comparable demos
against shared behavior contracts.

## Recommendation

Do not pick a final winner yet. Create evaluation criteria and a shared comparison harness first, then start with a
LangGraph Python plus Langfuse slice. Keep Phoenix/OpenInference as a later comparison candidate, not the immediate
implementation path.

The first product comparison should answer:

1. Can we run, inspect, and debug the agent workflow locally?
2. Can traces, evaluations, and run evidence be captured without LangSmith?
3. How much code and operating setup is required for a useful demo?
4. How well does the candidate scale from a local demo to durable self-hosted service operation?
5. What implementation details change our requirements or preferences?

## Sources

- LangSmith self-hosting docs: https://docs.smith.langchain.com/self_hosting
- LangSmith observability docs: https://docs.smith.langchain.com/observability
- Langfuse self-hosting docs: https://langfuse.com/self-hosting
- Langfuse docs: https://langfuse.com/docs
- Langfuse LangChain/LangGraph integration: https://langfuse.com/docs/integrations/langchain
- Phoenix docs: https://arize.com/docs/phoenix
- Phoenix tracing docs: https://arize.com/docs/phoenix/tracing
- Phoenix self-hosting docs: https://arize.com/docs/phoenix/self-hosting
- Phoenix LangGraph tracing docs: https://arize.com/docs/phoenix/integrations/python/langgraph/langgraph-tracing
- OpenInference docs: https://arize-ai.github.io/openinference/
- MLflow tracing docs: https://mlflow.org/docs/latest/genai/tracing/
- MLflow LangChain autologging: https://mlflow.org/docs/latest/genai/flavors/langchain/autologging
- Mastra observability tracing: https://mastra.ai/en/docs/observability/tracing
- Mastra AI tracing reference: https://mastra.ai/en/reference/observability/ai-tracing/ai-tracing
