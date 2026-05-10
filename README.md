# Agentic Project Foundation

This repository starts with the development process foundation before product implementation. Agents use specs,
BDD behavior contracts, local Beads Rust tickets, workflow scripts, and human review gates to make incremental tested
progress.

## Fresh Environment Setup

Run:

```bash
tools/agent-workflow/bootstrap-dev.sh --install-tools
```

The bootstrap checks `uv`, `python3`, `git`, the repo layout, and `br` from `Dicklesworthstone/beads_rust`.
If `br` is missing, it installs the Rust implementation using the upstream installer with `--skip-skills` so the
project keeps its own local agent skills.
It then runs `uv sync` and installs the `awf` CLI from `pyproject.toml`.

After bootstrap:

```bash
uv run awf --help
uv run awf context-index
uv run awf health-status --deep
uv run awf verify --profile health --json
uv run awf bdd-run --driver fixture
uv run awf repo-hygiene
uv run awf workflow-fixture-test
```

For cron-style orchestration, use:

```bash
uv run awf automation-loop --role pm-review --write
uv run awf automation-loop --role orchestrator --write
uv run awf automation-loop --role worker --worker-id worker-1 --write
uv run awf automation-loop --role integrator --write
```

## Operating Model

- `AGENTS.md` is the entrypoint for all agents.
- `.agents/skills/` contains role-specific instructions loaded only when needed.
- `apps/` contains runnable product implementations such as Mastra TypeScript and LangGraph Python.
- `packages/` contains shared contracts, fixtures, and cross-implementation assets.
- `tools/` contains development tooling such as the uv-managed `awf` CLI.
- `objectives/`, Spec Kit-managed `specs/`, `docs/adr/`, and `docs/research/` hold durable planning context.
- `tests/workflow/features/` holds BDD contracts for implementation-agnostic e2e behavior.
- `.beads/` holds local-first ticket state through Beads Rust.
- `.agent-runs/` holds run reports, manifests, blocked states, increments, verifications, and learnings.

Product framework work is intentionally deferred until this foundation validates cleanly.
