# BDD Driver Contract

Drivers execute behavior contracts against a concrete implementation while keeping feature files implementation-agnostic.
They are test harnesses only. They are not product adapters, shims, or compatibility layers.

Each driver must provide:

- `name`: stable implementation id.
- `start()`: prepare the implementation under test.
- `act(step)`: perform actor-level actions.
- `observe(assertion)`: return user-facing or operational evidence.
- `stop()`: clean up resources.

Feature files may mention driver boundaries but must not mention internal framework APIs.

The fixture driver also covers scheduled orchestration contracts. It validates the observable workflow behavior:
verification summaries, next-action selection, blocked-work rerouting, and human review boundaries.

## Product Baseline Work Order

The product baseline driver boundary starts from a repo-local roadmap goal, spec, or ready Beads ticket and observes
the work-order artifact produced for an implementer. A concrete driver should translate the contract into these
observable actions:

- load the current objective, linked spec, ready-work state, and existing evidence;
- produce exactly one behavior scope with out-of-scope boundaries and the acceptance command;
- expose repo-local trace, evaluation, durable state, review gate, and evidence paths;
- keep completion waiting until an independent reviewer acceptance artifact exists;
- prove deterministic fixture validation without hosted observability credentials.

Self-hosted observability evidence can enrich the operational observations, but the contract remains satisfied by
repo-local fixture evidence when hosted or service-backed credentials are unavailable.

## Self-Hosted Deployment Operations

The deployment operations driver boundary starts from the selected Pydantic AI plus Langfuse/DBOS stack and observes
whether another agent can operate it through repo-local deployment artifacts. A concrete driver should translate the
contract into these observable actions:

- load local, development-server, and production-like deployment profiles;
- verify that profiles name services, ports, storage paths, secret names, resource expectations, and target machines;
- report missing tools, services, paths, or secret names without exposing or requiring secret values;
- start or inspect the reference deployment profile through documented commands;
- run the representative selected-stack smoke workflow when the profile is available;
- expose repo-local run, trace, evaluation, durable, health, setup, and gap evidence;
- prove deterministic fixture validation without hosted credentials, external model providers, or cloud services;
- expose backup, restore, reset, health, log, trace, rollback, and recovery runbook evidence;
- keep Goal 005 completion waiting until an independent reviewer acceptance or rejection artifact exists.

Service-backed observability, durable execution, and deployment smoke evidence should be captured when controlled
self-hosted services are available. The contract remains testable in fixture mode by recording the unavailable
service-backed evidence as explicit gaps instead of silently requiring hosted services.
