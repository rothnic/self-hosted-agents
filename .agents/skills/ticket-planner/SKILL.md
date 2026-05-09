---
name: ticket-planner
description: Use when syncing approved spec tasks into Beads tickets or validating ticket metadata and dependencies.
---

# Ticket Planner

## Purpose

Keep tickets traceable to specs and objectives.

## Workflow

1. Run `uv run awf ticket-sync`.
2. Verify each task has an objective id, spec id, title, priority, dependency, and acceptance command.
3. If Beads `bd` is available and writes are approved, run with `--write`.
4. Do not create tickets from unapproved or ambiguous specs.

## Beads Notes

The installed Beads CLI may be available as `bd` or `beads`. Older docs may refer to `br`; use the workflow script so command detection stays centralized.

## Stop Conditions

- Missing spec linkage.
- Missing acceptance command.
- Human gate unresolved.
