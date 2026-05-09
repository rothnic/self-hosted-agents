---
name: bdd-contracts
description: Use when defining implementation-agnostic BDD contracts with actors, operational observations, and test drivers.
---

# BDD Contracts

## Purpose

Describe full-scenario behavior in a way that can be executed against different implementations through test drivers.

## Contract Rules

- Feature files describe actors, intent, observable outcomes, and operational expectations.
- Feature files do not mention internal framework APIs, databases, queues, or UI implementation details.
- Drivers translate scenario steps into implementation-specific test actions and observations.
- Operational actors are valid actors: analytics, tracing, support, scheduler, and reviewer expectations can be part of a scenario.

## Workflow

1. Identify the primary actor and operational actors.
2. Write a feature file in `tests/workflow/features/`.
3. Include at least one user-facing assertion and one operational assertion when the scenario has operational impact.
4. Add or update driver notes in `tests/workflow/drivers/`.
5. Run `uv run awf bdd-lint`.

## Stop Conditions

- Scenario asserts implementation details instead of behavior.
- Actor expectations are unclear.
- No driver boundary exists for a future implementation to satisfy.
