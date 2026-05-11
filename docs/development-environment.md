# Development Environment

## Supported Entry Point

Use one command for new machines, CI jobs, Codex workspaces, or cloud agent runners:

```bash
tools/agent-workflow/bootstrap-dev.sh --install-tools
```

This script is intentionally small and portable. It:

- Verifies `uv`.
- Verifies `python3` and `git`.
- Initializes git if the workspace is not already a repository.
- Installs `br` from `Dicklesworthstone/beads_rust` when missing and explicitly requested.
- Runs `uv sync` to create the managed Python environment and install the `awf` CLI.
- Runs workflow bootstrap checks.
- Installs the versioned pre-commit hook by setting `core.hooksPath` to `.githooks`.
- Initializes the local `.beads/` workspace when `br` is available.

## When To Update Bootstrap

Update `tools/agent-workflow/bootstrap-dev.sh`, `pyproject.toml`, and `awf bootstrap` in the same task when adding a
required tool, runtime, hook, environment variable, generated artifact, dependency, or setup command.

## CLI Contract

Use `uv run awf --help` for the command index and `uv run awf <command> --help` for command-specific inputs.
Commands use Rich help and human output by default. Pass `--json` to get a typed Pydantic response envelope with:

- `ok`
- `command`
- `summary`
- `data`

Use `uv run awf verify --profile <ticket|increment|health|pre-merge> --json` when an agent needs the correct checks,
evidence summary, and next action for the current context. Use `--write` to create a durable handoff artifact under
`.agent-runs/verifications/`.

Use `uv run awf automation-loop --role <pm-review|orchestrator|worker|integrator|health> --write` for scheduled
Codex or cron-like runs. Each role reads repo state, mutates only its owned workflow artifacts, and returns one
`next_action`. Scheduled Codex runners should set `UV_NO_CACHE=1` before invoking `uv run`; persistent uv cache paths
can be inaccessible in Codex automation sandboxes, including cache directories under `/tmp`.

```bash
UV_NO_CACHE=1 uv run awf automation-loop --role health --write --json
```

If a command fails, first run:

```bash
tools/agent-workflow/bootstrap-dev.sh --install-tools
uv run awf --help
uv run awf <failing-command> --help
```

## Tooling Policy

- Required project scripts use Python standard library only.
- Beads Rust is the ticket backend and should be available as `br`.
- Hosted execution environments should call the same scripts as local development.
- Runtime credentials, cloud-specific setup, and secrets must stay outside repo artifacts.

## Validation

Run:

```bash
uv run awf bootstrap
uv run awf health-status --deep
uv run awf verify --profile increment --json
uv run awf spec-kit-lint
uv run awf spec-lint
uv run awf bdd-lint
uv run awf bdd-run --driver fixture
uv run awf repo-hygiene
uv run awf workflow-fixture-test
```
