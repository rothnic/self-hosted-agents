# Current Objectives

## Objective: Agentic Development Foundation

ID: `agentic-development-foundation`
Status: active

Build an environment-agnostic operating system for coding agents that can inspect repo context, align objectives and
specs, decompose approved work into tickets, pause for human review, implement small verified slices, and capture
learnings for future runs.

## Success Criteria

- A new agent can start from `AGENTS.md`, run bootstrap/context commands, and know the next safe action.
- Specs, ADRs, research notes, tickets, behavior contracts, run reports, and learnings have clear homes.
- Planning, ticketing, review-gate, BDD contract, and retrospective flows can run without product-specific implementation.
- Workflow validation passes against an isolated fixture.

## Constraints

- Keep durable project state in git-friendly repo artifacts.
- Keep execution environment assumptions behind scripts.
- Use Beads Rust as the ticket system when available, while scripts must degrade clearly when `br` is missing.
- Use Spec Kit concepts without requiring a hosted service.
- Use BDD contracts to describe implementation-agnostic e2e behavior before comparing implementations.

## Non-Goals

- Do not implement LangGraph, LangChain, Mastra, RAG, frontend, or product workflow features in this phase.
- Do not automate risky writes without explicit `--write`.
- Do not let recurring agents bypass human review gates.
