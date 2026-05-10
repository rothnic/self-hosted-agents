# Project Structure

The repository is organized by purpose so it can grow beyond a single Python app.

## Top-Level Lanes

- `apps/`: runnable product implementations.
- `packages/`: shared contracts, fixtures, and cross-implementation assets.
- `tools/`: development and orchestration tooling.
- `specs/`: Spec Kit-managed feature artifacts created by Specify tooling.
- `objectives/`: current project objectives and constraints.
- `docs/`: ADRs, research, environment setup, and orchestration notes.
- `.agents/`: project policy and agent skills.
- `.agent-runs/`: durable run reports, health issues, claims, and learnings.
- `.beads/`: Beads Rust ticket state.

## Current App Plan

- `apps/mastra-ts/` will hold the TypeScript Mastra implementation.
- `apps/langgraph-python/` will hold the Python LangChain/LangGraph implementation.

Both apps should prove behavior through shared BDD contracts and future shared packages, not by sharing app internals.
Additional candidate apps may be added when the roadmap comparison identifies a distinct implementation path worth
testing, such as a Python-first stack using a different orchestration or observability approach.

Candidate apps must remain runnable and independently understandable. Shared comparison assets belong in `packages/`,
`tests/`, or docs; app internals should not be coupled just to make comparison easier.

## Comparison Ownership Boundaries

Use these locations when adding solution-comparison implementation, fixtures, and evidence:

- `apps/<candidate>/`: runnable candidate implementation code, app-specific tests, app-specific configuration, and
  app-specific notes. Do not place shared comparison contracts, shared fixtures, shared evaluation assets, or reusable
  cross-candidate helpers inside an app directory.
- `packages/`: shared contracts, reusable fixtures, schemas or types, evaluation assets, and cross-candidate utilities
  that multiple candidate apps use to prove comparable behavior.
- `tests/workflow/features/`: implementation-agnostic BDD contracts that describe behavior all candidate apps must prove.
- `tests/workflow/fixtures/`: workflow and test harness fixtures used by BDD drivers or workflow checks. These fixtures
  are not product implementation code for any candidate app.
- `docs/`: comparison evidence, roadmap notes, evaluation criteria, requirements mapping, ADRs, and research.

When a file could fit in both an app and a shared location, choose the shared location only if at least two candidate
apps are expected to consume it or if it defines comparison behavior. Keep implementation-specific framework glue inside
the candidate app until it becomes shared by evidence, not by anticipation.

## Python Tooling

The `awf` CLI is repo tooling, not product code. Its source lives under `tools/agent-workflow/src/`.
Python build artifacts such as `.egg-info`, `.eggs`, `build/`, and `dist/` are ignored and must not be committed.

## Specification Tooling

Spec Kit owns `specs/`. Do not add local alternate templates or custom split spec folders.
Use `uv run awf spec-new <short-name> "<description>" --write` or the installed Spec Kit skills to create native
`spec.md`, `plan.md`, and `tasks.md` artifacts.
