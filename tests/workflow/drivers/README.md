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
