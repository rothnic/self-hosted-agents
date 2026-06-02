# Goal 003 T017 Health Loop Issue Logging

## Scope

- Beads issue: `awf-8vh`
- Spec task: `specs/003-automated-increment-orchestration/tasks.md#T017`
- Acceptance command: `uv run awf verify --profile increment --json`

T017 adds repo-local issue evidence when the health automation loop sees workflow failures. The health role now reports
`logged` issue records, writes durable `.agent-runs/health/*.json` artifacts when `--write` is used, adds recurrence
fingerprints and previous-path context, attempts Beads issue creation, and stops implementation until health or PM
triage can route the failure.

## Implementation Evidence

- `tools/agent-workflow/src/agent_workflow/core.py` adds health issue fingerprints, prior-record lookup, Beads issue
  creation, health-loop record generation, and health automation-loop `logged` output.
- The write path populates `path` and Beads creation evidence before writing the durable health JSON artifact.
- `docs/orchestration/codex-automation-prompts.md` and `docs/orchestration/cron-workflow.md` document the logged health
  artifact, recurrence fields, Beads creation result, and stop-implementation expectation.
- `tests/workflow/features/automated_increment_orchestration.feature` adds the recurring health failure behavior
  contract.
- `uv run awf workflow-fixture-test --json` passed with `41/41` fixture checks, including:
  - `health loop issue logging records recurring workflow failures`
  - `health loop issue logging persists Beads evidence before writing artifact`

## Reviewer Evidence

Independent reviewer agent `019e8796-81be-7693-87d8-b6e7b40de218` first rejected the draft because the durable JSON
artifact was written before Beads creation evidence was attached. After the fix, the same independent reviewer accepted
the updated T017 diff.

Reviewer outcome: `accepted`

Evidence checked by reviewer:

- Updated T017 diff only.
- Write path now sets `item["path"]`, populates `item["beads"]`, then writes the JSON artifact.
- New deterministic fixture uses a temporary health directory and fake Beads writer, reads the persisted JSON artifact,
  and asserts persisted `path` plus Beads evidence match the returned record.
- `python3 -B -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- Presenter evidence that `uv run awf workflow-fixture-test --json` passed `41/41`.

Required follow-up tickets: none for T017.

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf automation-loop --role health --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --json`:
  healthy repo returned `ok: true`, `logged: []`, and no failed checks.
- `uv run awf verify --profile ticket --json`: passed before reviewer; rerun after closure is recorded below.
- `uv run awf workflow-fixture-test --json`: passed with `41/41`.
- `uv run awf repo-hygiene --json`: passed before reviewer; rerun after closure is recorded below.
- `uv run awf review-gate --json`: passed before reviewer; rerun after closure is recorded below.
- `uv run awf workflow-state-lint --json`: passed before reviewer; rerun after closure is recorded below.

## Closure

`uv run awf complete-work --issue-id awf-8vh --worker-id codex-goal003-t017 --write --json` succeeded.

- Beads issue `awf-8vh` closed.
- Spec task `T017` marked complete in `specs/003-automated-increment-orchestration/tasks.md`.
- Completion comment recorded the implementation, validation, and independent reviewer acceptance evidence.
- `uv run awf increment-plan --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --write --json`
  refreshed `.agent-runs/increments/003-automated-increment-orchestration-goal-003.json`.
- Claim archived to `.agent-runs/claims/archive-2026-06/awf-8vh.json`.
- Next unblocked Beads item after closure: `awf-j3t` / T018.

Post-close validation:

- `uv run awf workflow-state-lint --json`: passed; `completed_tasks_checked: 89`, `open_issues_checked: 10`.
- `uv run awf review-gate --json`: passed; no blocked files, open questions, spec errors, or human-required gates.
- `uv run awf repo-hygiene --json`: passed; `checked_files: 231`.
- `git diff --check`: passed.
- `uv run awf verify --profile increment --json`: passed all checks.
- `uv run awf workflow-fixture-test --json`: passed `41/41`.
- `uv run awf automation-loop --role health --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --json`:
  passed with `logged_count: 0`.
- `uv run awf ready-work --json`: next ready Beads item is `awf-j3t` / T018.
