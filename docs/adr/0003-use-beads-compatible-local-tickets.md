# ADR 0003: Use Beads-Compatible Local Tickets

Status: accepted

## Context

The project needs agent-friendly tickets that work offline and remain git-friendly.

## Decision

Use Beads Rust `br` when available. Workflow scripts also produce Beads-compatible ticket proposals when `br` is
missing, so agents can continue planning without pretending tickets were created.

## Consequences

- Ticket state can be local-first and structured.
- Missing tooling is explicit.
- Ticket proposals remain traceable to specs and objectives.
