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
| LangGraph Python plus Phoenix | Python-first tracing/evaluation with OpenInference alignment | Product workflow may need more assembly |
| Python app plus MLflow tracing | Strong Python lifecycle story and broader experiment tooling | LLM-agent UX may be less specialized |
| Mastra TypeScript plus shared contracts | Useful cross-language comparison against Python-first choices | Lower fit with Python preference |
| LangSmith | Best-known LangChain baseline | Self-hosted access may require Enterprise approval |

## Recommendation

Do not pick a winner yet. Create a requirements-to-solution matrix and a shared comparison harness first, then implement
the Python-first candidate slices against the same behavior contracts and trace/evaluation expectations.

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
- Phoenix docs: https://arize.com/docs/phoenix
- Phoenix tracing docs: https://arize.com/docs/phoenix/tracing
- OpenInference docs: https://arize-ai.github.io/openinference/
- MLflow tracing docs: https://mlflow.org/docs/latest/genai/tracing/
