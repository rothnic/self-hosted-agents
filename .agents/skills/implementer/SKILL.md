---
name: implementer
description: Use when executing one ready ticket by making the smallest coherent code or documentation change and verifying its acceptance command.
---

# Implementer

## Purpose

Complete one ready ticket without expanding scope.

## Workflow

1. Run `uv run awf ready-work`.
2. Confirm the item came from Beads when Beads is available.
3. Claim one ready ticket.
4. Read linked objective, spec, task, and behavior contract.
5. Make the smallest coherent change.
6. Run the ticket acceptance command and any relevant checks.
7. Update the linked task or ticket evidence.
8. At completion, recommend a new session when the repo is clean and pushed, the next step is review/planning, or a
   different primary skill should take over.

## Work Queue Rule

Beads is the executable backlog. Do not choose implementation work by scanning `tasks.md` unless `uv run awf ready-work`
explicitly reports it is falling back because Beads is unavailable. If ready work is missing but `tasks.md` has open
tasks, stop and route to `ticket-planner`.

## Stop Conditions

- The ticket is not linked to a spec.
- The acceptance check is unclear.
- Implementation requires a new architecture or product decision.
- The work exists only as an unsynced spec task while Beads is available.
