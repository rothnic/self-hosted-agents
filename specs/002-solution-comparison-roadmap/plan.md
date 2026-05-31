# Implementation Plan: Solution Comparison Roadmap

**Branch**: `002-solution-comparison-roadmap` | **Date**: 2026-05-10 |
**Spec**: `specs/002-solution-comparison-roadmap/spec.md`

## Summary

Create the planning substrate for comparing agent application stacks against high-level system requirements. The project
will use separate runnable apps for candidate implementations and shared comparison assets for behavior, traces,
evaluations, and demo evidence.

## Technical Context

**Language/Version**: Python preferred for first product implementation; TypeScript remains available for Mastra
comparison.
**Primary Dependencies**: To be chosen through requirements mapping. Current candidates include LangGraph, Langfuse,
Pydantic AI, Logfire, Phoenix/OpenInference, MLflow tracing, Mastra, Hatchet, Temporal, DBOS, Prefect, and Restate.
**Storage**: Repo artifacts, `.beads/issues.jsonl`, docs, specs, app-specific source, shared comparison fixtures.
**Testing**: Shared BDD contracts, app-specific tests, trace/evaluation evidence checks, `uv run awf workflow-fixture-test`.
**Target Platform**: Local development first, with self-hosted service path considered during comparison.
**Project Type**: Multi-app comparison repo.
**Constraints**: No default dependency on approved self-hosted LangSmith. Hosted observability is required evidence for
full solutions, but deterministic repo-local artifacts must keep validation repeatable. Durable execution is required
before final promotion, but the runtime must be selected through comparison rather than assumed.

## Constitution Check

- Repository artifacts are the source of truth: PASS.
- Human gates prevent drift: PASS; roadmap direction remains human-owned.
- Testable behavior comes before implementation: PASS; comparison harness precedes deep app work.
- Small slices and traceable tickets: PASS through Spec Kit tasks and Beads.
- Alpha means no compatibility debt: PASS; candidates may change directly as learning improves.

## Project Structure

```text
apps/
├── langgraph-python/
└── mastra-ts/

packages/
└── shared comparison assets to be defined

docs/
├── roadmap.md
└── research/
    └── llm-observability-solution-space.md

specs/
└── 002-solution-comparison-roadmap/
```

## Phased Plan

1. Define the requirement matrix and candidate comparison criteria.
2. Decide the first shared comparison harness shape.
3. Select the first Python-first candidate implementation slice.
4. Implement candidate app slices one at a time.
5. Review demos and evidence with the human.
6. Update requirements, matrix, specs, and backlog as implementation learning changes the decision space.
7. Evaluate self-hosted-compatible observability and durable execution as first-class solution components before
   promoting a candidate.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| Multiple candidate apps | Comparison must be grounded in actual implementations | A single app would hide framework tradeoffs |
| Shared harness before deep app work | Evidence must be comparable across candidates | App-specific tests alone would bias the comparison |

## Open Questions

1. Which durable execution option is easiest to start, understand, and scale for the first Python production path?
2. Does Pydantic AI's OpenTelemetry path provide enough self-hosted-compatible observability without excessive
   operational burden?
3. Which durable runtime should be selected after comparing framework-specific Pydantic AI options and Hatchet?
