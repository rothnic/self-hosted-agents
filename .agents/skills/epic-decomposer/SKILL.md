---
name: epic-decomposer
description: Use when an approved objective or spec needs to be broken into small dependency-aware tasks before ticket sync.
---

# Epic Decomposer

## Purpose

Convert approved epic-level changes into small slices that can be implemented and verified independently.

## Workflow

1. Read the approved spec and acceptance criteria.
2. Identify behavior contracts that should exist before implementation.
3. Create slices that each have one acceptance command.
4. Add dependencies only when one slice truly cannot be done first.
5. Update `tasks.md` before creating tickets.

## Task Rules

- One coherent behavior or workflow improvement per task.
- Include objective id, priority, acceptance command, and dependency.
- Prefer vertical slices that can be tested.

## Stop Conditions

- The epic lacks acceptance criteria.
- A required human decision is unresolved.
