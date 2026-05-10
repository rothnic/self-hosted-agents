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
**Primary Dependencies**: To be chosen through requirements mapping. Initial research candidates include LangGraph,
Langfuse, Phoenix/OpenInference, MLflow tracing, and Mastra.
**Storage**: Repo artifacts, `.beads/issues.jsonl`, docs, specs, app-specific source, shared comparison fixtures.
**Testing**: Shared BDD contracts, app-specific tests, trace/evaluation evidence checks, `uv run awf workflow-fixture-test`.
**Target Platform**: Local development first, with self-hosted service path considered during comparison.
**Project Type**: Multi-app comparison repo.
**Constraints**: No default dependency on approved self-hosted LangSmith. Requirements and preferences are expected to
evolve after implementation evidence.

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

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| Multiple candidate apps | Comparison must be grounded in actual implementations | A single app would hide framework tradeoffs |
| Shared harness before deep app work | Evidence must be comparable across candidates | App-specific tests alone would bias the comparison |

## Open Questions

1. Which first outcome matters most: local demo, framework comparison, automation reliability, or operator dashboard?
2. What should dominate the first roadmap decision: speed, learning value, reliability, or extensibility?
3. Which observability/evaluation capability is non-negotiable for the first candidate slice?
