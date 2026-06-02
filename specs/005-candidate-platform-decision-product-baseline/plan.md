# Implementation Plan: Candidate Platform Decision And Product Baseline

**Branch**: `005-candidate-platform-decision-product-baseline` | **Date**: 2026-06-02 |
**Spec**: `specs/005-candidate-platform-decision-product-baseline/spec.md`

## Summary

Use the accepted Goal 001 through Goal 003 evidence to choose the primary product stack and define the first product
baseline workflow. The work starts with a normalized evidence audit, then records an independently reviewed platform
decision, then creates BDD and backlog surfaces for product work on the selected stack.

## Technical Context

**Language/Version**: Python 3.14 for workflow tooling; candidate apps may include Python and TypeScript references.
**Primary Dependencies**: Existing `awf` CLI, Beads, Spec Kit artifacts, comparison fixtures, candidate app artifacts.
**Storage**: `docs/requirements-matrix.md`, `docs/roadmap.md`, `docs/adr/`, `.agent-runs/reports/`,
`.agent-runs/increments/`, `.beads/issues.jsonl`, `tests/workflow/features/`.
**Testing**: `uv run awf workflow-fixture-test`, `uv run awf verify --profile increment --json`,
`uv run awf review-gate`, `uv run awf repo-hygiene`, `uv run awf workflow-state-lint --json`.
**Target Platform**: Local repo validation and self-hosted/controlled infrastructure evidence.
**Project Type**: Workflow and candidate-app comparison repo moving toward one selected product app baseline.
**Constraints**: Do not make deterministic validation depend on hosted credentials. Do not select a stack from research
alone. Do not discard non-selected candidates without recorded tradeoffs.

## Constitution Check

- Repository artifacts are the source of truth: PASS.
- Human-only pause is not required for goal evidence: PASS; presenter and independent reviewer evidence are required.
- Testable behavior comes before implementation depth: PASS through BDD and workflow fixture acceptance.
- Small slices and traceable tickets: PASS through Beads tasks generated from this spec.
- Alpha means no compatibility debt: PASS; future product work may replace comparison-only boundaries directly.

## Project Structure

```text
docs/
├── adr/
├── goals/
├── requirements-matrix.md
└── roadmap.md

specs/
└── 005-candidate-platform-decision-product-baseline/

tests/
└── workflow/
    └── features/

apps/
├── langgraph-python/
├── pydantic-ai/
└── mastra-ts/              # Only created if the audit requires a runnable contrast slice.
```

## Phased Plan

1. Audit candidate evidence from current repo artifacts and mark each evidence class as proven, missing, or deferred.
2. Decide whether Mastra TypeScript needs a runnable contrast slice before platform selection.
3. Normalize requirements-matrix scoring around implementation evidence only.
4. Record a platform decision ADR and roadmap/matrix updates with explicit rejected/deferred candidate rationale.
5. Present decision evidence to an independent reviewer agent and record acceptance or rejection.
6. Define the first product baseline workflow and BDD contract for the selected stack.
7. Freeze or archive non-selected candidate lanes as comparison references, with migration notes where useful.
8. Sync follow-up tasks into Beads and continue with one implementer ticket at a time.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| Platform decision before production hardening | The roadmap needs one product lane to deepen | Waiting for all production gaps would keep comparison open indefinitely |
| Independent reviewer acceptance for architecture evidence | The user directed progress not to block on implicit human review | Unreviewed agent self-approval would weaken decision evidence |
| Candidate freeze instead of deletion | Comparison history remains valuable | Deleting candidate lanes would lose implementation lessons and tradeoffs |
