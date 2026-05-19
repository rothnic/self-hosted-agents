# LangGraph Python App

First Python-first candidate app for the solution comparison roadmap. Keep this independent from the TypeScript Mastra
app except for shared contracts and comparison assets.

Detailed slice plan: `apps/langgraph-python/implementation-plan.md`.

## First Slice

Candidate id: `langgraph-python`.

Stack: LangGraph Python plus Langfuse.

The first slice should implement the shared comparable-agent workflow, not a full production agent system. It should
accept a product objective, constraints, and project context, then return:

- a concise recommended next implementation slice;
- meaningful alternatives and tradeoffs;
- explicit human questions when direction is not safe to assume;
- an acceptance check for the proposed implementation work;
- durable run evidence that can be compared with later candidate apps.

## Evidence Required

The first implementation ticket should produce:

- a runnable command for the candidate demo;
- a passing shared behavior-contract or fixture check;
- Langfuse trace evidence for the workflow run;
- evaluation output tied to the same run;
- setup notes covering required services, environment variables, and local startup;
- explicit gaps and custom critical infrastructure risks.

Use `docs/comparison-evidence.md` as the evidence checklist and `docs/evaluation-criteria.md` as the scoring rubric.

## Non-Goals

Do not build the Phoenix, MLflow, Mastra, or LangSmith comparison paths in this app. Do not declare LangGraph plus
Langfuse as the final architecture until comparable implementation evidence exists.
