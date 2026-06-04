# Goal 005: Self-Hosted Deployment And Operations Reference

## Objective

Create the reference self-hosted deployment and operating model for the selected agent stack on project-controlled
infrastructure.

## Why This Matters

Self-hosted agents are only useful if the system can actually run outside a local laptop. The project needs a concrete
deployment path with secrets, storage, backups, observability, recovery, and operating checks.

## Product Iteration

This goal turns the selected local product baseline into an operations-ready reference deployment. It should fit the
available machine model: local development on the MacBook, heavier development on `vps-dev`, and production-like
management on `vps-gw` when appropriate.

## Scope

- Define the target deployment topology.
- Package the selected app, observability backend, durable runtime, and storage services.
- Add secrets and environment management.
- Add backup, restore, and reset procedures.
- Add health checks, logs, traces, and runbooks.
- Prove a fresh-machine setup path.

## Current State

Goal 005 has been initialized as Spec `006-self-hosted-deployment-operations-reference` with executable Beads backlog.
The increment ledger is
`.agent-runs/increments/006-self-hosted-deployment-operations-reference-goal-005.json`, and the Beads parent epic is
`awf-h2u`.

Completed through T009:

- T001 / `awf-n19`: self-hosted deployment operations BDD contract.
- T002 / `awf-gdu`: local, development-server, and production-like deployment profiles.
- T003 / `awf-noh`: selected-stack service boundaries, ports, volumes, secrets, storage paths, and target machines.
- T004 / `awf-is8`: environment templates and credential-free readiness checks.
- T005 / `awf-091`: one-command local startup manifest and documented service-backed startup equivalents.
- T006 / `awf-t1m`: representative selected-stack deployment smoke command.
- T007 / `awf-xei`: repo-local deployment smoke evidence with run, trace, eval, durable, and health correlation.
- T008 / `awf-rgf`: credential-free fallback proof for absent deployment services or secrets.
- T009 / `awf-71o`: backup, restore, and reset runbooks for database, service state, and run evidence.

Next ready implementer ticket:

- `awf-hic` / T010: add health, log, trace, and diagnostics runbooks for app, observability, durable runtime, and
  storage.

The remaining Goal 005 tickets are dependency-ordered through T013. T013 presents final Goal 005 evidence, and a
separate reviewer agent must record acceptance or rejection. Human review is not a progress blocker unless a decision is
explicitly reserved, missing, or contradicted by evidence.

## Task Backlog

1. Define local, development-server, and production-like deployment profiles.
2. Choose container, process, and service boundaries for the selected stack.
3. Document ports, volumes, credentials, and resource expectations.
4. Add bootstrap checks for required runtimes and services.
5. Add environment templates that do not commit secrets.
6. Add one-command local startup for the full stack where practical.
7. Add deployment scripts or docs for the target VPS profile.
8. Add backup and restore procedures for databases, object storage, and run evidence.
9. Add health checks for app, worker, observability, durable runtime, and storage.
10. Add log and trace collection guidance.
11. Add smoke tests that run against the deployed stack.
12. Add rollback and recovery runbooks.
13. Add resource and cost notes for the chosen topology.
14. Run a fresh setup rehearsal on a clean path or machine.
15. Record operational gaps and scaling follow-ups.

## Definition Of Done

- Another agent can provision the reference stack from repo docs and scripts.
- The deployed stack can run a representative agent workflow.
- Observability and durable execution are available in the deployed profile.
- Backup, restore, health, and recovery procedures are documented and tested at least once.
- Secrets are handled without committing credentials.

## Proof Commands

```bash
tools/agent-workflow/bootstrap-dev.sh --install-tools
uv run awf verify --profile health --json
uv run awf workflow-fixture-test
uv run awf repo-hygiene
```

Add deployment-specific smoke commands when the target topology is defined.

## Review Blocking Criteria

- The deployment depends on third-party hosted services for required behavior.
- Secrets, ports, volumes, or storage are undocumented.
- Backup and restore are not tested.
- The stack cannot be reproduced by another agent.
- The operating burden is too high for one engineer without an explicit tradeoff decision.

## Kickoff Prompt

```text
/goal Execute docs/goals/005-self-hosted-deployment-operations-reference.md
in /Users/nroth/workspace/self-hosted-agents. Define and prove the reference
self-hosted deployment profile for the selected stack, including service topology,
secrets, storage, observability, durable execution, backup, restore, health checks,
and smoke validation.
```
