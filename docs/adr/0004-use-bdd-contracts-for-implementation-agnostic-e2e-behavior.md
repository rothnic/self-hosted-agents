# ADR 0004: Use BDD Contracts For Implementation-Agnostic E2E Behavior

Status: accepted

## Context

The project will compare multiple framework implementations. E2E tests should express what actors expect from a full scenario without encoding framework details.

## Decision

Use BDD-style feature files as high-level behavior contracts. Each implementation must provide a test driver that can
execute the same scenario contract and expose operational observations such as analytics, traces, artifacts, or
persisted state.

## Consequences

- Product behavior can be specified before framework selection.
- Different implementations can be compared against the same scenario.
- Operational concerns become part of the contract rather than afterthoughts.
- Driver boundaries keep scenarios stable while implementation details evolve without becoming product compatibility layers.
