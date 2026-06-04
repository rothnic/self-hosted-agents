# Implementation Plan: Operator Workbench And Review UX

**Branch**: `007-operator-workbench-review-ux` | **Date**: 2026-06-04 |
**Spec**: `specs/007-operator-workbench-review-ux/spec.md`

## Summary

Turn the repo-native self-hosted agent operating model into a decision-ready operator workbench. Start with information
architecture and BDD contracts, then build repo-backed status and evidence surfaces, add durable review actions, decide
whether CLI/static artifacts are sufficient or a local UI is justified, and finish with independent reviewer-accepted
Goal 006 evidence.

## Technical Context

**Language/Version**: Python 3.14 for `awf` workflow tooling, shell for Git/Beads integration, and selected app artifacts
where trace/eval links are produced.
**Primary Dependencies**: Existing `awf` CLI, Beads, Spec Kit artifacts, `.agent-runs/` reports/verifications/claims,
Pydantic AI product-baseline evidence, self-hosted-compatible Langfuse trace artifacts, GitHub CLI or connector only
when available.
**Storage**: `docs/workbench/`, `.agent-runs/reports/`, `.agent-runs/verifications/`, `.agent-runs/increments/`,
`.agent-runs/claims/`, `.beads/issues.jsonl`, and optional local UI assets if selected.
**Testing**: `uv run awf workflow-fixture-test`, `uv run awf verify --profile increment --json`,
`uv run awf context-index --json`, `uv run awf next-action --json`, `uv run awf repo-hygiene`, plus workbench-specific
commands added by this spec.
**Target Platform**: Local MacBook development, `vps-dev` for heavier development, and `vps-gw` for production-like
management when appropriate.
**Project Type**: Workflow/product operating surface for a self-hosted agent system.
**Constraints**: Keep source-of-truth state in repo artifacts. Do not require hosted services or GitHub credentials for
deterministic validation. Do not let a UI hide review gates or bypass durable evidence.

## Constitution Check

- Repository artifacts are the source of truth: PASS.
- Human-only pause is not required for goal evidence: PASS; presenter and independent reviewer evidence are required.
- Testable behavior comes before implementation depth: PASS through BDD and fixture coverage before UI decisions.
- Small slices and traceable tickets: PASS through Beads tasks generated from this spec.
- Alpha means no compatibility debt: PASS; existing reports and CLI surfaces can be changed directly when tests and
  docs move with them.

## Project Structure

```text
docs/
├── workbench/           # information architecture, interface decision, operator docs
├── goals/               # roadmap and Goal 006 status
└── operations/          # links back to scheduled-agent and handoff use

tools/
└── agent-workflow/      # awf status/workbench/review commands and fixture helpers

tests/
└── workflow/
    └── features/        # operator workbench and review UX BDD contract

.agent-runs/
├── reports/             # presenter/reviewer evidence and handoff artifacts
├── verifications/       # generated workbench/status validation artifacts
└── increments/          # Goal 006 increment ledger
```

## Phased Plan

1. Define minimum operator views and an implementation-agnostic BDD contract for status, evidence, review decisions,
   and handoffs.
2. Add a consolidated operator status surface that pulls from existing context, next-action, Beads, claims, validations,
   traces, evals, and PR evidence.
3. Add goal, increment, evidence, review, trace/eval, branch/PR, and handoff views or sections with exact artifact links.
4. Add durable review-gate actions for approve, request changes, defer, and ask questions.
5. Decide whether the workbench remains CLI/static or becomes a local UI, with operating burden and accessibility
   criteria documented before implementation.
6. Implement the selected interface and fixture coverage while preserving CLI/static automation workflows.
7. Document scheduled-agent use and record Goal 006 presenter evidence plus independent reviewer acceptance or rejection.

## Complexity Tracking

- Workbench breadth: needed because the operator needs one coherent decision surface across goals, tickets, claims,
  traces, evals, PRs, and review gates.
- UI timing: deferred until after CLI/static proof because a local UI adds maintenance and verification cost.
- External integrations: GitHub and self-hosted Langfuse deep links are optional enhancements; deterministic validation
  must remain repo-local and credential-free.
