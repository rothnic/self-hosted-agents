# Goal 003 T010 Safe Scheduled Loop - 2026-06-02

## Scope

Ticket: `awf-7e8` / T010, define the minimum safe scheduled loop for one active increment.

Claimed by: `codex-goal003-t010`

Acceptance command: `uv run awf verify --profile increment --json`

## Presented Evidence

The current active increment was written with:

```bash
uv run awf increment-plan --spec-id 003-automated-increment-orchestration --phase "Goal 003" --write --json
```

Durable ledger:

- `.agent-runs/increments/003-automated-increment-orchestration-goal-003.json`

The ledger records:

- objective `agentic-development-foundation`
- spec `003-automated-increment-orchestration`
- phase `Goal 003`
- increment id `003-automated-increment-orchestration-goal-003`
- feature branch `codex/003-automated-increment-orchestration-goal-003`
- active T010 claim `awf-7e8` by `codex-goal003-t010`
- T009 closed and T010 through T021 visible as the remaining Goal 003 increment work
- no blocked, stale, or human-required work

## Minimum Safe Loop

Scheduled Goal 003 runs must use explicit scope arguments:

```bash
--spec-id 003-automated-increment-orchestration --phase "Goal 003"
```

Local cron can run `uv run awf`. Codex app automations should run `.venv/bin/awf` in a worktree execution environment.

Safe role order:

1. Health verifies first and logs an issue before implementation work if checks fail.
2. PM/review reads the explicit Goal 003 ledger, backlog, active claims, blockers, and evidence.
3. Orchestrator assigns only unclaimed, unblocked Goal 003 Beads work.
4. Each worker uses a stable worker id, acts on one claimed ticket, runs ticket verification, records evidence, pushes,
   and stops.
5. Integrator verifies completed worker branches and increment evidence, routes goal evidence to an independent reviewer
   agent, and does not merge to `main`.

Goal and increment evidence review is an agent-to-agent handoff: this implementer presents the evidence, and an
independent reviewer agent accepts or rejects it in this report or a linked durable artifact. The loop should not pause
only because a human review label exists. Human decisions remain for architecture, product, priority, scope, and final
merge choices.

## Scheduler Commands

Local cron:

```bash
SCOPE='--spec-id 003-automated-increment-orchestration --phase "Goal 003"'
uv run awf automation-loop --role pm-review $SCOPE --write --json
uv run awf automation-loop --role orchestrator $SCOPE --write --json
uv run awf automation-loop --role worker --worker-id worker-1 $SCOPE --write --json
uv run awf automation-loop --role integrator $SCOPE --write --json
uv run awf automation-loop --role health $SCOPE --write --json
```

Codex app worktree automations:

```bash
SCOPE='--spec-id 003-automated-increment-orchestration --phase "Goal 003"'
.venv/bin/awf automation-loop --role pm-review $SCOPE --write --json
.venv/bin/awf automation-loop --role orchestrator $SCOPE --write --json
.venv/bin/awf automation-loop --role worker --worker-id worker-1 $SCOPE --write --json
.venv/bin/awf automation-loop --role integrator $SCOPE --write --json
.venv/bin/awf automation-loop --role health $SCOPE --write --json
```

## Safety Boundaries

- Default no-arg `automation-loop` still targets the older Phase 6 solution-comparison increment and is not scheduler
  safe for Goal 003.
- Workers must not scan `tasks.md` directly when Beads is available.
- Workers act on one claimed item and stop after evidence is recorded.
- Integrator verifies worker output and increment evidence without merging to `main`.
- Goal and increment evidence goes to an independent reviewer agent instead of waiting on human review by default.
- Remaining hardening work is already represented by T011 through T021.

## Follow-Up Coverage

- T011 covers stale-claim status and handoff guidance.
- T013 covers deterministic worker branch naming and worktree setup guidance.
- T014 covers compact verification artifacts.
- T016 covers review-agent invocation guidance before PR and increment handoffs.
- T017 covers health-loop issue logging for recurring failures.
- T019 covers compact active-work summaries.
- T021 covers the manual end-to-end increment rehearsal.

## Acceptance Evidence

Validation captured on 2026-06-02:

- `git diff --check`: passed.
- `uv run awf verify --profile ticket --json`: passed with zero failed checks.
- `uv run awf verify --profile increment --json`: passed with zero failed checks.
- `uv run awf workflow-fixture-test --json`: passed with `33/33` fixture checks before closure and again after
  `complete-work` closed `awf-7e8`.
- Ticket profile checks: `spec-lint`, `spec-kit-lint`, `bdd-lint`, `review-gate`, `repo-hygiene`,
  `workflow-state-lint`, and the nested acceptance command all passed.
- Increment profile checks: `bootstrap`, `spec-lint`, `spec-kit-lint`, `bdd-lint`, `bdd-run-fixture`, `review-gate`,
  `repo-hygiene`, `workflow-state-lint`, and `workflow-fixture-test` all passed.
- `review-gate` reported no blocked files, no open questions, and `human_required_count=0`.
- `ready-work` evidence reported `ready_count=12`, `blocked_count=0`, and `human_required_count=0`.

## Independent Review

Reviewer: `019e8701-e9f5-7972-9d40-315e11888ba6`

Outcome: accepted with no blocking findings.

The reviewer accepted T010 evidence on 2026-06-02 after reviewing the T010 report, Goal 003 scheduler docs, Codex
automation prompts, active increment ledger, and `awf-7e8` claim. The reviewer confirmed that the evidence defines a
minimum safe scheduled loop using explicit Goal 003 scope, calls out the unsafe no-arg `automation-loop` default,
records the repo-local increment ledger, uses presenter-plus-independent-reviewer evidence review without blocking
solely on human review, maps remaining gaps to existing follow-up tasks, and has coherent passing validation evidence.
