# Mastra TypeScript App

Second comparison candidate for the solution comparison roadmap. Keep this independent from the Python LangGraph app
except for shared contracts and comparison assets.

## Intended Contrast

Candidate id: `mastra-ts`.

Stack: Mastra TypeScript plus the shared comparison contract.

This candidate should follow the first `langgraph-python` slice. Its job is to test whether a TypeScript-native agent
framework gives enough built-in workflow, observability, evaluation, or deployment leverage to justify the language and
maintenance cost for a Python-preferring owner.

## Second Slice

The first Mastra implementation ticket should prove the same comparable-agent workflow as `langgraph-python`. It should
accept the same objective, constraints, and project context, then return:

- a concise recommended next implementation slice;
- alternatives and tradeoffs comparable to the Python candidate;
- explicit human questions when direction is not safe to assume;
- an acceptance check for proposed implementation work;
- durable run evidence that can be reviewed beside the Python run.

## Evidence Required

The Mastra slice should produce evidence in the same categories as the Python candidate:

- runnable command and setup notes;
- passing shared behavior-contract or fixture check;
- trace evidence for workflow steps, model calls, tools, inputs, outputs, latency, failures, and token usage where
  available;
- evaluation output tied to the same run;
- operating notes for services, environment variables, package management, and deployment path;
- explicit gaps, especially cross-language maintenance cost and any shared-contract friction.

Use `docs/comparison-evidence.md` as the evidence checklist and `docs/evaluation-criteria.md` as the scoring rubric.

## Non-Goals

Do not use this app to replace the Python-first preference before comparable evidence exists. Do not build a broader
TypeScript product UI or Mastra-specific behavior that cannot be evaluated through the shared contract.
