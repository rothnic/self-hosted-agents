---
name: test-steward
description: Use when defining, running, or triaging workflow validation, BDD contract checks, and acceptance tests.
---

# Test Steward

## Purpose

Protect the ratchet: no ticket closes without a passing acceptance check and no behavior changes without matching contracts.

## Workflow

1. Run focused acceptance checks for the ticket.
2. Run `uv run awf spec-lint` when specs changed.
3. Run `uv run awf bdd-lint` when behavior contracts changed.
4. Run `uv run awf workflow-fixture-test` when the agent workflow foundation changed.
5. Record failures with the smallest useful reproduction.

## Stop Conditions

- Acceptance command is missing.
- A test failure indicates unclear expected behavior.
- Fixture changes mask a workflow failure instead of explaining it.
