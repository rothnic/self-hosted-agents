---
name: implementer
description: Use when executing one ready ticket by making the smallest coherent code or documentation change and verifying its acceptance command.
---

# Implementer

## Purpose

Complete one ready ticket without expanding scope.

## Workflow

1. Run `uv run awf ready-work`.
2. Claim one ready ticket.
3. Read linked objective, spec, task, and behavior contract.
4. Make the smallest coherent change.
5. Run the ticket acceptance command and any relevant checks.
6. Update the linked task or ticket evidence.

## Stop Conditions

- The ticket is not linked to a spec.
- The acceptance check is unclear.
- Implementation requires a new architecture or product decision.
