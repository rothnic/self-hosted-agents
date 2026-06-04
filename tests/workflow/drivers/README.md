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
