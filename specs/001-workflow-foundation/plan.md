# Implementation Plan: Agent Workflow Foundation

**Branch**: `001-workflow-foundation` | **Date**: 2026-05-09 | **Spec**: `specs/001-workflow-foundation/spec.md`
**Input**: Feature specification from `/specs/001-workflow-foundation/spec.md`

## Summary

Establish an environment-agnostic operating system for coding agents before product implementation. The foundation uses
Spec Kit for feature artifacts, Beads Rust for local tickets, BDD contracts for implementation-agnostic behavior,
repo artifacts for durable state, and a small `awf` CLI as the execution boundary.

## Technical Context

**Language/Version**: Python 3.14 for tooling; future product apps may use TypeScript and Python.
**Primary Dependencies**: `uv`, Typer, Rich, Pydantic, Beads Rust `br`, GitHub Spec Kit.
**Storage**: Repo artifacts, `.beads/issues.jsonl`, generated Beads local DB files, `.agent-runs/` JSON and Markdown.
**Testing**: `uv run awf workflow-fixture-test`, BDD fixture driver, repo hygiene, pre-commit hook.
**Target Platform**: Local development, Codex workspaces, CI, and cloud agent services.
**Project Type**: Multi-lane repo with `apps/`, `packages/`, `tools/`, `.specify/`, `.agents/`, and workflow tests.
**Performance Goals**: CLI checks should be fast enough for pre-commit and cron use.
**Constraints**: No hosted-only dependencies, no compatibility debt during alpha, explicit `--write` for mutations.
**Scale/Scope**: Foundation for recurring semi-automated coding agents before product framework comparisons.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Repository artifacts are the source of truth: PASS.
- Human gates prevent drift: PASS.
- Testable behavior comes before implementation: PASS through BDD contracts and fixture tests.
- Small slices and traceable tickets: PASS through Beads and claims.
- Alpha means no compatibility debt: PASS; old custom specs were removed rather than preserved through adapters.

## Project Structure

### Documentation (this feature)

```text
specs/001-workflow-foundation/
├── spec.md
├── plan.md
└── tasks.md
```

### Source Code (repository root)

```text
.agents/
├── project-policy.json
└── skills/

.agent-runs/
├── claims/
├── health/
├── learnings/
├── manifests/
└── reports/

.beads/
└── issues.jsonl

.specify/
├── memory/
├── scripts/
├── templates/
└── workflows/

apps/
├── langgraph-python/
└── mastra-ts/

packages/

tools/
└── agent-workflow/
    ├── bootstrap-dev.sh
    └── src/agent_workflow/

tests/
└── workflow/
    ├── drivers/
    ├── features/
    └── fixtures/
```

**Structure Decision**: Keep product implementations in `apps/`, shared contracts and assets in `packages/`, and repo
orchestration in `tools/agent-workflow/`. Spec Kit owns `specs/`; no custom alternate spec format is allowed.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple repo lanes | Product will compare TypeScript and Python implementations | A single root `src/` would not scale to Mastra and LangGraph examples |
| Local workflow CLI | Agents need deterministic commands across runtimes | Ad hoc scripts would hide contracts and make cron/cloud runs inconsistent |
