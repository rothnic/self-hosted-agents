---
name: ticket-planner
description: Use when syncing approved spec tasks into Beads tickets or validating ticket metadata and dependencies.
---

# Ticket Planner

## Purpose

Keep tickets traceable to specs and objectives.

## Workflow

1. Run `uv run awf ticket-sync`.
2. Verify each open task has an objective id, spec id, task id, title, priority, dependency, and acceptance command.
3. Compare proposed tickets with existing Beads issues to avoid duplicates and stale work.
4. If Beads is available and writes are explicitly approved, run with `--write`.
5. Confirm implementers can see the result through `uv run awf ready-work`.
6. Do not create tickets from unapproved or ambiguous specs.

## Source Of Truth

- `tasks.md` is the spec planning breakdown.
- Beads is the executable backlog and the source implementers query for work.
- Ticket planner owns the translation from approved spec tasks to Beads issues.
- If `tasks.md` and Beads disagree, report drift and recommend a sync or spec update before implementation.

## Beads Notes

The installed Beads CLI may be available as `br`. Use the workflow script so command detection stays centralized.

## Stop Conditions

- Missing spec linkage.
- Missing acceptance command.
- Human gate unresolved.
- Ticket sync would create duplicate or completed work.
