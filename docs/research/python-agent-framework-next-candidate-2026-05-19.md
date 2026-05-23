# Python Agent Framework Next Candidate Research

Date checked: 2026-05-19

## Research Question

After the approved LangGraph Python plus Langfuse slice, what Python-first open-source candidate should the roadmap
consider next for a scalable, evidence-backed agent application stack?

## Findings

Pydantic AI is the strongest next Python-first research target. Its current documentation positions it as a Python
agent framework for production-grade generative AI applications and workflows, with model-agnostic support, type-safe
development, evals, Logfire/OpenTelemetry observability, MCP and A2A integration, human-in-the-loop approval, graph
support, and durable execution.

Pydantic AI also documents official durable execution integrations with Temporal, DBOS, Prefect, and Restate. That maps
directly to this project's functional areas around durable execution, human-in-the-loop workflows, scalable service
paths, and low custom critical infrastructure.

LlamaIndex is the strongest fallback if the next product direction is data/RAG-heavy. Its documentation emphasizes
agents over data, context augmentation, data connectors, indexes, engines, observability/evaluation integrations, and
workflows that can be deployed as production microservices.

AutoGen should not be the next new-project candidate despite its multi-agent history because the upstream repository
now marks it as maintenance mode and points new projects toward Microsoft Agent Framework.

CrewAI remains a possible later comparison candidate for high-level multi-agent orchestration. Its open-source page
emphasizes planning, reasoning, tools, memory, knowledge, and collaboration, but it is less directly aligned than
Pydantic AI with this repo's typed Python, eval, observability, and durable execution criteria.

## Recommendation

Research Pydantic AI plus Logfire or OpenTelemetry as the next Python-first candidate after the LangGraph Python slice
produces evidence. Do not create the app lane yet. First, add an approved backlog item to compare Pydantic AI against
the functional needs map and decide whether it should become the third runnable candidate.

Use LlamaIndex as the alternate Python candidate if LangGraph evidence shows that document ingestion, retrieval, or
context augmentation is the primary unresolved functional risk.

## Confidence

Medium. The direction is strong enough for a roadmap follow-up task, but not for implementation commitment. The next
decision should still be based on a focused requirements-to-functional-needs review and, later, the same runnable
comparison evidence required of other candidates.

## Sources

- Pydantic AI overview: https://pydantic.dev/docs/ai/overview/
- Pydantic AI durable execution overview: https://pydantic.dev/docs/ai/integrations/durable_execution/overview/
- LlamaIndex Python framework overview: https://developers.llamaindex.ai/python/framework/
- LlamaIndex agent guide: https://developers.llamaindex.ai/python/framework/understanding/agent/
- AutoGen GitHub repository: https://github.com/microsoft/autogen
- CrewAI open source overview: https://crewai.com/open-source

## Follow-Up Questions

1. After the LangGraph Python slice, did the biggest gap involve typed workflow ergonomics, durable execution,
   observability, evaluation, or RAG/data access?
2. Should the third candidate be Pydantic AI by default, or should LlamaIndex replace it if data-heavy workflows become
   the main functional risk?
