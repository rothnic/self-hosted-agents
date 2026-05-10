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

## Python Tooling

The `awf` CLI is repo tooling, not product code. Its source lives under `tools/agent-workflow/src/`.
Python build artifacts such as `.egg-info`, `.eggs`, `build/`, and `dist/` are ignored and must not be committed.

## Specification Tooling

Spec Kit owns `specs/`. Do not add local alternate templates or custom split spec folders.
Use `uv run awf spec-new <short-name> "<description>" --write` or the installed Spec Kit skills to create native
`spec.md`, `plan.md`, and `tasks.md` artifacts.
