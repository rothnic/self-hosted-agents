# Agent Operating Guide

This repository is managed through specs, local tickets, behavior contracts, small verified changes, and human review gates.
Treat repository artifacts as the durable source of truth; local machines, CI runners, Codex, and cloud agent services are replaceable execution environments.

## First Steps

1. For a fresh environment, run `tools/agent-workflow/bootstrap-dev.sh --install-tools`.
2. Run `uv run awf bootstrap` before making changes.
3. Run `uv run awf context-index` to load current objectives, active specs, tickets, blockers, behavior contracts, and recent runs.
4. Run `uv run awf spec-kit-lint` before changing specification workflow artifacts.
5. Load only the project skill needed for the current role from `.agents/skills/<skill>/SKILL.md`.
6. Prefer dry runs first. Use `--write` only when the requested mode explicitly permits mutation.

## Environment Setup

Agents must keep environment setup reproducible. If a change introduces any required tool, runtime, hook, command,
service, environment variable, or generated artifact needed for normal development, update all relevant bootstrap and
documentation in the same task:

- `tools/agent-workflow/bootstrap-dev.sh`
- `uv run awf bootstrap`
- `pyproject.toml` when Python dependencies or CLI entrypoints change
- `.specify/` when Spec Kit templates, scripts, workflows, or constitution expectations change
- `docs/development-environment.md`
- `README.md` when the first-run command changes
- `.githooks/pre-commit` or `repo-hygiene` policy when the change affects checks

After changing setup, run `tools/agent-workflow/bootstrap-dev.sh` and the normal validation commands.
If `uv run awf ...` fails, run `tools/agent-workflow/bootstrap-dev.sh --install-tools`, then inspect
`uv run awf --help` and the failing subcommand help before changing implementation.

## Project State Machine

Use this loop to keep the project ratcheting forward:

1. **Bootstrap**: verify environment and hooks with `uv run awf bootstrap`.
2. **Index**: inspect current state with `uv run awf context-index`.
3. **Role Select**: choose and load exactly one primary skill for the current activity.
4. **Gate Check**: run `review-gate`; stop if a human decision is required.
5. **Plan**: PM steward aligns objectives, specs, tickets, behavior contracts, checks, recent reports, and learnings.
6. **Decompose**: epic decomposer turns approved scope into small spec tasks.
7. **Ticket**: ticket planner syncs approved tasks into Beads Rust tickets.
8. **Claim**: implementer selects one item from `ready-work` and confirms its spec, objective, and acceptance command.
9. **Change**: make the smallest coherent change for that task.
10. **Verify**: test steward runs the task acceptance command plus relevant workflow checks.
11. **Review**: reviewer validates code, specs, tickets, BDD contracts, and repo hygiene.
12. **Close Or Add Work**: close only when acceptance evidence exists; otherwise add follow-up tasks and return to planning.
13. **Learn**: retrospector records useful process learnings before the next run.

The loop pauses whenever the next transition would require guessing about scope, architecture, priority, acceptance, or behavior.

## Scheduled Orchestration

Cron-like runners use the same CLI and repo artifacts as humans:

- Planner cadence: `uv run awf cron-tick --role planner --write`
- Worker cadence: `uv run awf cron-tick --role worker --worker-id <id> --write`
- Health cadence: `uv run awf health-status --deep --json`

The planner reviews health, objectives, specs, tickets, run reports, and learnings. It creates planning artifacts and logs issues.
Workers only inspect ready work, claim one unclaimed task, and stop if a gate or missing acceptance evidence is found.
Work separation is handled through Beads ready work plus `.agent-runs/claims/`; workers do not mutate unless a task is claimed.
If a cron run finds a problem, it must log it with `uv run awf issue-log --write` before exiting.

## Skill Routing

- Planning cycle, drift detection, or objective alignment: load `pm-steward`.
- Spec Kit feature creation or updates: load `spec-author`.
- Native Spec Kit constitution/spec/plan/tasks work: load `speckit-constitution`, `speckit-specify`, `speckit-plan`, or `speckit-tasks`.
- Bounded research with sources: load `researcher`.
- Breaking approved epics into slices: load `epic-decomposer`.
- Creating or syncing Beads tickets: load `ticket-planner`.
- Implementing one ready ticket: load `implementer`.
- Reviewing code, specs, or tickets: load `reviewer`.
- Running checks and triaging failures: load `test-steward`.
- Reviewing project harness health, status, scheduled runs, or workflow issues: load `health-status`.
- Human approval, blocked state, or resume logic: load `review-gatekeeper`.
- Capturing run learnings and process improvements: load `retrospector`.
- Preparing release/change notes: load `release-notes`.
- Defining implementation-agnostic e2e contracts: load `bdd-contracts`.

## Core Rules

- Do not guess across a human gate. If scope, priority, architecture, acceptance criteria, or behavior expectations are unclear, record a blocked run and stop.
- Keep specs small. Move detailed evidence into `docs/research/` and durable decisions into `docs/adr/`.
- Every implementation ticket must link to a spec id and objective id, and must name the acceptance check required for closure.
- Every user-facing or operationally important behavior should be expressible as an implementation-agnostic BDD contract before framework-specific implementation.
- Execute one coherent ticket at a time unless a human explicitly approves a broader batch.
- Update tests, specs, tickets, behavior contracts, and run reports together when behavior or process changes.
- Product framework decisions are deferred until the workflow foundation is validated.
- Keep the repo clean. Do not add unexpected root files, oversized directories, generated caches, or files that violate line-length policy.
- Run `uv run awf repo-hygiene` before considering a task complete.
- Use `uv run awf <command>` for all workflow actions. Do not add alternate command shims.

## Compatibility Policy

The compatibility policy lives in `.agents/project-policy.json`.

Current default: `lifecycle_stage=alpha`, `maintain_backward_compatibility=false`.

During alpha, agents should prefer direct improvement over compatibility layers.
Do not preserve deprecated paths, duplicate APIs, migration layers, compatibility adapters, shims, or
backwards-compatibility paths unless a human explicitly changes the policy or the task says the system is now
beta/stable.
When a contract changes in alpha, update specs, BDD contracts, test drivers, and tasks directly.

There are no users yet. Remove or replace alpha code directly instead of carrying compatibility debt forward.
The only allowed implementation-specific boundary in this phase is a BDD test driver under `tests/workflow/drivers/`.
Drivers are test harness code, not product adapters or compatibility layers.

If the project policy changes to beta or stable, agents must preserve public behavior unless the linked spec and human review gate approve a breaking change.

## Task Completion

A task is complete only when:

- The linked objective, spec, and Beads ticket are clear.
- The requested change is implemented in the smallest coherent slice.
- The acceptance command named by the task passes.
- Relevant `awf` checks pass: `spec-lint`, `bdd-lint`, `bdd-run`, `review-gate`, `repo-hygiene`, or `workflow-fixture-test`.
- A reviewer or automated review command can verify evidence without relying on hidden context.
- Follow-up work discovered during implementation is recorded as spec tasks or Beads tickets instead of being silently skipped.

## Common Commands

```bash
tools/agent-workflow/bootstrap-dev.sh --install-tools
uv run awf --help
uv run awf bootstrap
uv run awf context-index --json
uv run awf spec-kit-lint
uv run awf workflow-run --mode plan --dry-run
uv run awf health-status --deep
uv run awf cron-tick --role planner --write
uv run awf spec-lint
uv run awf review-gate
uv run awf repo-hygiene
uv run awf bdd-lint
uv run awf bdd-run --driver fixture
uv run awf workflow-fixture-test
```

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->
