# Agent Operating Guide

This repository is managed through specs, local tickets, behavior contracts, small verified changes, and review gates.
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
4. **Gate Check**: run `review-gate`; stop only when evidence is missing, contradictory, or outside agent authority.
5. **Plan**: PM steward aligns objectives, specs, tickets, behavior contracts, checks, recent reports, and learnings.
6. **Decompose**: epic decomposer turns approved scope into small spec tasks.
7. **Ticket**: ticket planner syncs approved tasks into Beads Rust tickets.
8. **Claim**: implementer selects one item from `ready-work` and confirms its spec, objective, and acceptance command.
9. **Change**: make the smallest coherent change for that task.
10. **Verify**: test steward runs the task acceptance command plus relevant workflow checks.
11. **Review**: reviewer validates code, specs, tickets, BDD contracts, and repo hygiene.
12. **Close Or Add Work**: complete claimed work with
    `uv run awf complete-work --issue-id <id> --evidence "<summary>" --write` after acceptance evidence exists;
    otherwise add follow-up tasks and return to planning.
13. **Learn**: retrospector records useful process learnings before the next run.

The loop does not pause merely because a human-review label exists. For goal and increment evidence, one agent presents
the evidence and an independent reviewer agent accepts or rejects it in a durable artifact. The loop pauses only when
review evidence is missing or contradictory, or when the user has explicitly reserved a decision for themselves.

## Session Boundaries

Agents should not keep one conversation open indefinitely. Work is organized into deliberate sessions so planning,
implementation, review, and learning remain understandable when another agent resumes later.

Default session shape:

1. **Planning session**: inspect state, gather needed research, update objective/spec/tasks/tickets, and end with a
   clear recommendation or targeted human questions.
2. **Implementation session**: claim one Beads ticket, make the smallest coherent change, verify it, record evidence,
   then commit and push when approved or when the task is self-contained and already authorized.
3. **Review session**: summarize verified changes, risks, validation, and explicit approval options for the human.
4. **Learning session**: record process lessons or follow-up tickets when a run exposed workflow drift.

Recommend starting a new session at these boundaries:

- After a commit is pushed and the repo is clean.
- After a human gate is approved, rejected, or deferred.
- Before switching from planning/research into implementation.
- Before switching from implementation into review or roadmap planning.
- After one substantial ticket, three small tickets, or about 60-90 minutes of active work.
- When the conversation is carrying enough historical detail that the next agent could misunderstand current state.
- When the next step needs a different primary role or skill.

When recommending a new session, the agent should provide a compact handoff:

- Current branch, latest commit, and git cleanliness.
- Current objective/spec and Beads ticket state.
- Completed validation evidence.
- Recommended next role, next ticket or decision, and why.
- Any human decision still needed.

The human should not have to manually manage this. Agents should say when a new session is the cleaner operating move,
finish the current checkpoint, and provide a ready-to-use handoff prompt for the next session.

## State, Backlog, And Next Action

Agents must be able to answer "what should happen next?" from repo state. Use this precedence order:

1. **Objective**: `objectives/current.md` defines what the project is trying to achieve.
2. **Spec**: `specs/<id>/spec.md` and `plan.md` define approved intent and approach.
3. **Spec tasks**: `specs/<id>/tasks.md` is the planning breakdown for a spec, not the worker queue.
4. **Beads backlog**: `.beads/issues.jsonl` is the primary executable backlog for agents.
5. **Claims and evidence**: `.agent-runs/claims/`, Beads comments, run reports, and check output prove status.

When Beads is available, implementers must not choose work directly from `tasks.md`. They use `uv run awf ready-work`
and claim one Beads item. `tasks.md` is used by spec/decomposition roles and as an explicit fallback only when Beads
is unavailable.

When a user asks "what next?", the agent runs the startup/status path and gives a CEO-level decision brief with 2-4
concrete options and one recommendation. Do not tell the human to run workflow commands as the next step; use workflow
commands as agent instrumentation, then translate the result into a business/product decision or a small set of
targeted questions.

```bash
uv run awf next-action --json
uv run awf bootstrap
uv run awf context-index --json
uv run awf health-status --deep --json
uv run awf ready-work --json
git status --short --branch
```

Choose the recommendation by state:

- If health fails: load `health-status`, log or propose the issue, and stop before implementation.
- If a review gate is open: load `review-gatekeeper`; if the gate concerns goal evidence, have an independent reviewer
  agent accept or reject the presented evidence and record the outcome before continuing.
- If there are verified local changes waiting for human review: load `reviewer`; present approve/merge, request changes,
  or continue options. Do not merge without explicit human approval.
- If an approved spec has unsynced open tasks: load `ticket-planner` and run `uv run awf ticket-sync`; use `--write`
  only when mutation is requested.
- If Beads has ready work: load `implementer`, claim one item, and execute only that item.
- If no ready work exists: load `pm-steward` to propose the next objective/spec/backlog action.

Use this response template for every next-action or review handoff. The visible user-facing request should be a
decision, answer, approval, or prioritization choice, not a CLI command.

```markdown
## Executive Snapshot

- Where we are:
- Why it matters:
- Current repo state:
- Work in progress:

## Agent Assessment

- Objective:
- What the agent checked:
- What changed recently:
- Blockers or risks:
- Research/context needed:

## Recommendation

Recommended path:
Reason:
Agent will do next:
What I need from you:

## Your Options

1. Recommended: <decision/action> - <business or project effect>
2. <decision/action> - <business or project effect>
3. <decision/action> - <business or project effect>

## Questions To Answer

1. <specific question that unblocks the next agent action>
2. <optional question>
3. <optional question>

## Meta-Process

- Learning/process follow-up:
- Automation opportunity:
- Risk to watch:
- New-session recommendation:
```

Keep the filled response concise, but include enough context that a human opening the message can tell where the project
stands, what decision is needed, why the recommendation is grounded in repo state, and what agents will do after the
human responds. If more information is needed, the agent should gather bounded research first, then ask targeted
questions. If the next action is safe and does not require a human decision, the agent should proceed instead of asking
the human to operate the workflow manually.

## Role Swimlanes

- **Human reviewer**: sets project objectives, can reserve decisions explicitly, chooses priority when tradeoffs remain,
  and approves merges. The human should not need to manually inspect status commands; agents present options and evidence.
- **PM steward**: reads project state and returns the next safe action, options, blockers, and recommendation. It does not
  implement product changes.
- **Spec author / Spec Kit roles**: create or update native Spec Kit artifacts.
- **Epic decomposer**: turns approved specs into small `tasks.md` slices with acceptance commands.
- **Ticket planner**: turns approved open spec tasks into Beads backlog items and validates traceability.
- **Implementer**: consumes Beads ready work, claims one item, makes the smallest coherent change, and records evidence.
- **Test steward**: runs acceptance and workflow checks, then records precise failures or passing evidence.
- **Reviewer**: reviews code/spec/ticket alignment and goal evidence. For goal or increment completion, the presenting
  agent records evidence and an independent reviewer agent records acceptance or rejection.
- **Review gatekeeper**: pauses automation when review evidence is missing or contradictory and resumes after the
  review outcome is recorded in a durable artifact.
- **Retrospector**: records durable process learnings after a run.

## Backlog Population

Backlog population is spec driven:

1. PM steward confirms the objective and approved spec.
2. Epic decomposer updates `tasks.md` with small, independently verifiable slices.
3. Ticket planner runs `uv run awf ticket-sync` to preview Beads tickets.
4. With explicit write approval, ticket planner runs `uv run awf ticket-sync --write`.
5. Implementers work only from `uv run awf ready-work`, not by scanning `tasks.md`.

Completion is proven when `uv run awf complete-work --issue-id <id> --evidence "<summary>" --write` records passing
acceptance evidence, closes the Beads issue, marks the linked task complete, and reruns workflow-state lint. Do not
manually mark a task complete before the linked issue has completion evidence.

## Scheduled Orchestration

Cron-like runners use the same CLI and repo artifacts as humans:

- PM/review cadence: `uv run awf automation-loop --role pm-review --write`
- Orchestrator cadence: `uv run awf automation-loop --role orchestrator --write`
- Worker cadence: `uv run awf automation-loop --role worker --worker-id <id> --write`
- Integrator cadence: `uv run awf automation-loop --role integrator --write`
- Health cadence: `uv run awf automation-loop --role health --write`

For Codex app automations, use the bootstrapped `.venv/bin/awf` entrypoint for these scheduled role commands instead
of `uv run awf`. The `uv` launcher can fail before `awf` starts when the automation sandbox blocks uv cache or temp
filesystem paths. Configure Codex cron automations with the `worktree` execution environment; `local` automation
sessions may be read-only and fail when `awf --write` creates claim, verification, or evidence files. Local shells and
normal cron can continue using `uv run awf`.

The PM/review loop reviews health, objectives, specs, tickets, run reports, and learnings.
It refreshes backlog when ready work runs low and opens phase review gates when needed.
The orchestrator reads increment state, claims unblocked work, and assigns worker branches.
Workers only inspect claimed work, verify with `uv run awf verify --profile ticket`, record evidence, and push.
The integrator reviews completed worker branches, verifies the increment, and routes goal evidence to an independent
reviewer agent. It does not stop solely because human review might be useful.
Work separation is handled through Beads ready work plus `.agent-runs/claims/`; workers do not mutate unless a task is
claimed.
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
- For automation handoffs, `uv run awf verify --profile ticket` or `uv run awf verify --profile increment` passes.
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
uv run awf verify --profile increment --json
uv run awf next-action --json
uv run awf automation-loop --role pm-review --write
uv run awf automation-loop --role orchestrator --write
uv run awf automation-loop --role worker --worker-id worker-1 --write
uv run awf automation-loop --role integrator --write
uv run awf spec-lint
uv run awf review-gate
uv run awf repo-hygiene
uv run awf workflow-state-lint
uv run awf complete-work --issue-id <id> --evidence "<summary>" --write
uv run awf bdd-lint
uv run awf bdd-run --driver fixture
uv run awf workflow-fixture-test
```

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->
