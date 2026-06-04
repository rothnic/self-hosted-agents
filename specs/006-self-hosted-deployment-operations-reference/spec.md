# Feature Specification: Self-Hosted Deployment And Operations Reference

**Feature Branch**: `006-self-hosted-deployment-operations-reference`
**Created**: 2026-06-04
**Status**: Draft
**Input**: Goal 005 from `docs/goals/005-self-hosted-deployment-operations-reference.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deployment Profiles Are Reproducible (Priority: P1)

As an agent operator, I can inspect the local, development-server, and production-like deployment profiles and know
which services, ports, volumes, secrets, and machine assumptions are required for each profile.

**Why this priority**: Goal 005 cannot safely deploy anything until the target topology and operating boundaries are
explicit, self-hosted, and reproducible by another agent.

**Independent Test**: Inspect the deployment profile docs, environment template, and bootstrap/readiness checks; confirm
they identify all services, secret names, storage paths, ports, and machine targets without committing credentials.

**Acceptance Scenarios**:

1. **Given** the selected Pydantic AI plus Langfuse/DBOS stack, **When** the deployment profile is reviewed, **Then**
   local, development-server, and production-like profiles name service boundaries, storage, ports, secrets, and machine
   assumptions.
2. **Given** a fresh agent environment, **When** bootstrap/readiness checks run, **Then** missing tools, services,
   secrets, or storage paths are reported without requiring cloud-hosted credentials.

---

### User Story 2 - Representative Workflow Runs On Controlled Infrastructure (Priority: P1)

As a project maintainer, I can run a representative selected-stack workflow against the reference profile and inspect
repo-local evidence that observability and durable execution are available.

**Why this priority**: The roadmap is self-hosted agents, not local-only comparison fixtures. The selected stack needs a
controlled deployment proof before deeper product work can rely on it.

**Independent Test**: Run the deployment smoke command and inspect its repo-local evidence for service profile, run id,
trace id, durable run id, health results, and deterministic fallback behavior.

**Acceptance Scenarios**:

1. **Given** the reference profile is started, **When** the smoke workflow runs, **Then** it records run, trace, eval,
   durable, and service-health evidence under repo-controlled artifacts.
2. **Given** hosted credentials are absent, **When** deterministic validation runs, **Then** it still passes without
   sending network traffic to hosted services.

---

### User Story 3 - Operations Runbooks Are Tested (Priority: P2)

As an operator, I can follow runbooks for backup, restore, reset, logs, traces, health checks, rollback, and recovery,
and see evidence that at least one agent rehearsed the procedures.

**Why this priority**: A self-hosted reference stack is incomplete if another agent cannot recover or diagnose it after
setup.

**Independent Test**: Inspect the runbooks and rehearsal report; confirm backup/restore/reset, health, log, trace,
rollback, resource, and recovery procedures have commands, expected evidence, and tested gaps.

**Acceptance Scenarios**:

1. **Given** the reference services have state, **When** backup and restore procedures are rehearsed, **Then** the runbook
   records commands, state paths, verification checks, and gaps.
2. **Given** a service or workflow failure is simulated or described, **When** recovery guidance is reviewed, **Then**
   another agent can identify logs, traces, health checks, rollback steps, and escalation criteria.

## Requirements *(mandatory)*

- **FR-001**: Goal 005 MUST define local, development-server, and production-like deployment profiles for the selected
  Pydantic AI plus Langfuse/DBOS stack.
- **FR-002**: Deployment profiles MUST identify service boundaries, ports, volumes, storage paths, credentials, resource
  expectations, and target machines without committing secrets.
- **FR-003**: The reference topology MUST avoid required third-party hosted services for core behavior.
- **FR-004**: Bootstrap or readiness checks MUST report missing runtimes, service configuration, secrets, and storage
  prerequisites.
- **FR-005**: The reference profile MUST include a one-command local startup path where practical, or a documented
  equivalent when startup spans multiple services.
- **FR-006**: A deployment smoke MUST run a representative selected-stack workflow and capture repo-local evidence.
- **FR-007**: Deployment evidence MUST show observability and durable execution availability in the reference profile.
- **FR-008**: Deterministic fixture validation MUST remain valid without hosted credentials, external model providers,
  or cloud services.
- **FR-009**: Backup, restore, reset, health, log, trace, rollback, and recovery runbooks MUST be documented.
- **FR-010**: At least one fresh setup or clean-path rehearsal MUST be recorded with commands, evidence, and gaps.
- **FR-011**: Resource, cost, and operating-burden notes MUST be recorded for one-engineer operation.
- **FR-012**: Goal 005 completion evidence MUST be presented by one agent and accepted or rejected by an independent
  reviewer agent.

### Key Entities

- **Deployment Profile**: A named topology for local, development-server, or production-like operation, including
  services, ports, volumes, secrets, storage, and machine assumptions.
- **Service Boundary**: The app, observability, durable runtime, database, worker, or storage component with explicit
  runtime and ownership expectations.
- **Environment Template**: A non-secret configuration file or document that names required variables and safe defaults.
- **Deployment Smoke Evidence**: Repo-local proof that the selected stack ran in the reference profile with health,
  trace, eval, durable, and run correlation.
- **Operations Runbook**: Commands and expected evidence for startup, reset, backup, restore, health, logs, traces,
  rollback, and recovery.

## Success Criteria *(mandatory)*

- **SC-001**: Another agent can identify the recommended local and production-like deployment profiles without reading
  prior chat.
- **SC-002**: The reference profile can run a representative selected-stack workflow and produce repo-local evidence.
- **SC-003**: Observability and durable execution are visible in the deployment evidence.
- **SC-004**: Backup, restore, reset, health, and recovery procedures have at least one recorded rehearsal or explicit
  gap.
- **SC-005**: Secrets remain uncommitted and deterministic validation stays credential-free.

## Assumptions

- Goal 004 selected Pydantic AI plus Langfuse and DBOS as the first product-baseline stack, not the final solution.
- Local MacBook development remains useful, but heavier development can be offloaded to `vps-dev` and production-like
  management can target `vps-gw` when appropriate.
- The first Goal 005 proof may use a controlled local or VPS-like profile before full production hardening, as long as
  gaps are explicit and self-hosted requirements are preserved.
