# Goal 003 T016 Review-Agent Invocation Guidance

## Scope

- Beads issue: `awf-svc`
- Spec task: `specs/003-automated-increment-orchestration/tasks.md#T016`
- Acceptance: `uv run awf verify --profile increment --json`

## Presenter Evidence

Implemented explicit review-agent invocation guidance before PR and increment handoffs.

Key behavior:

- `integrator_handoff` now includes `review_agent_invocation`.
- The guidance names the reviewer role and requires a reviewer agent separate from the presenting implementer or
  integrator.
- The guidance states that agents should not block solely for human review unless the user explicitly reserves a
  decision or the reviewer finds a product, priority, architecture, or scope question.
- The guidance identifies trigger points before PR evidence updates, increment acceptance, and goal evidence completion.
- The prompt asks the reviewer to verify evidence, return `accepted` or `rejected`, list findings by severity, and name
  required follow-up tickets.
- The evidence list includes the increment ledger, written increment verification, worker branch reviews, git status,
  feature branch diff, and relevant `.agent-runs/reports/` evidence.
- Durable outcome fields include reviewer id, outcome, evidence checked, findings, follow-up tickets, and timestamp.

Documentation updates:

- `docs/orchestration/codex-automation-prompts.md`
- `docs/orchestration/cron-workflow.md`

Fixture coverage:

- `workflow_fixture_test_result` now validates `review_agent_invocation` shape and required policy fields.
- `tests/workflow/features/automated_increment_orchestration.feature` now expects review-agent invocation guidance and
  increment evidence without merging to `main`.

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py` passed.
- `git diff --check` passed.
- `uv run awf automation-loop --role integrator --spec-id 003-automated-increment-orchestration --phase 'Goal 003'
  --json` passed and returned `integrator_handoff.review_agent_invocation`.
- `uv run awf verify --profile ticket --json` passed for `awf-svc`.
- `uv run awf workflow-fixture-test --json` passed `39/39`, including
  `review-agent invocation guidance precedes PR and increment handoffs`.
- `uv run awf review-gate --json` passed with no human-required items.
- `uv run awf workflow-state-lint --json` passed.
- `uv run awf repo-hygiene --json` passed.

## Independent Review

Reviewer agent `019e8778-f398-7ee2-b534-5d8cf95009a2` accepted the current T016 diff with no findings.

Evidence checked by the reviewer:

- Current uncommitted T016 diff only: `core.py`, orchestration docs, BDD feature text, and active claim
  `.agent-runs/claims/awf-svc.json`.
- Alignment with FR-011 and FR-012 in `specs/003-automated-increment-orchestration/spec.md`.
- `integrator_handoff.review_agent_invocation` reviewer role, independence, no-human-block policy, trigger-before
  guidance, prompt, evidence list, and durable outcome fields.
- Documentation consistency for invoking a separate reviewer before PR or increment handoff evidence is accepted.
- Presenter validation commands listed above.

Required follow-up tickets: none for T016.

## Closure Evidence

`uv run awf complete-work --issue-id awf-svc --worker-id codex-goal003-t016 --write --json` passed.

Workflow close results:

- Beads issue `awf-svc` closed.
- Task `T016` marked complete in `specs/003-automated-increment-orchestration/tasks.md`.
- Beads evidence comment `86` recorded by `codex-goal003-t016`.
- `workflow-state-lint` passed during completion.

Post-close increment refresh:

- `uv run awf increment-plan --spec-id 003-automated-increment-orchestration --phase 'Goal 003' --write --json`
  passed.
- Active claims: none.
- Ready count: `5`.
- Next unblocked issue: `awf-8vh` / T017.

The completed claim was archived to `.agent-runs/claims/archive-2026-06/awf-svc.json`.

## Post-Close Validation

- `uv run awf workflow-state-lint --json` passed.
- `uv run awf review-gate --json` passed with no human-required items.
- `uv run awf repo-hygiene --json` passed.
- `uv run awf ready-work --json` reported `awf-8vh` / T017 as the next ready item.
- `git diff --check` passed.
- `uv run awf verify --profile increment --json` passed with `9` checks and no failed checks.
- `uv run awf automation-loop --role integrator --spec-id 003-automated-increment-orchestration --phase 'Goal 003'
  --json` passed with `main_merge_allowed=false`, `draft_pr_boundary=true`, `review_agent_role=reviewer`, and no
  pending worker branches.
- `uv run awf workflow-fixture-test --json` passed `39/39`, including
  `review-agent invocation guidance precedes PR and increment handoffs`.
