# ADR 0002: Use Progressive Skills And Human Gates

Status: accepted

## Context

Large agent instruction files create drift and overload context. Fully automated agents can also continue through unclear objectives unless the process forces a pause.

## Decision

Keep `AGENTS.md` minimal and route agents to concise role skills. Require explicit human gates for unclear scope,
priority, architecture, acceptance criteria, behavior expectations, or product intent.

## Consequences

- Agents load only context relevant to their role.
- Ambiguity becomes visible and resumable.
- Process improvements can be made by updating skills and checks instead of rewriting all instructions.
