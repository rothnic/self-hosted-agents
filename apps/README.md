# Apps

Runnable product implementations live here.

- `mastra-ts/`: future TypeScript Mastra implementation.
- `langgraph-python/`: future Python LangChain/LangGraph implementation.
- `pydantic-ai/`: approved next Python-first Pydantic AI plus Logfire/OpenTelemetry implementation lane.

Each app should own its runtime-specific source, tests, and local setup. Shared contracts belong in `packages/` or specs.
New candidate apps should be added only when the roadmap comparison identifies a separate solution path that needs real
implementation evidence.
