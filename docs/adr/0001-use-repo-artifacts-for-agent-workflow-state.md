# ADR 0001: Use Repo Artifacts For Agent Workflow State

Status: accepted

## Context

Agents may run locally, in CI, in Codex, or in cloud environments. The workflow needs continuity without depending on any one runner.

## Decision

Store durable workflow state in repository artifacts: objectives, specs, ADRs, research notes, behavior contracts,
Beads ticket exports, run reports, blocked states, and learning logs.

## Consequences

- Fresh checkouts can reconstruct project context.
- Automation remains environment-agnostic.
- Sensitive runtime credentials and hosted execution details stay outside the durable workflow model.
