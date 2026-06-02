# Goal 003 T011 Stale Claim Handoff - 2026-06-02

## Scope

Ticket: `awf-h1z` / T011, add stale-claim status and handoff guidance for abandoned active work.

Claimed by: `codex-goal003-t011`

Acceptance command: `uv run awf verify --profile increment --json`

## Presented Evidence

T011 strengthens increment status so stale active claims are inspectable and actionable instead of only showing an id,
path, and age.

Implementation:

- `tools/agent-workflow/src/agent_workflow/core.py` enriches stale claim entries with claim age, stale threshold,
  worker id, worker branch, feature branch, issue title/status/external ref, acceptance command, and handoff guidance.
- `increment-status` now scopes active and stale claims to the current increment child tickets instead of reporting
  unrelated active claims from other increments.
- `workflow-fixture-test` includes a deterministic synthetic stale claim assertion for the handoff shape.
- `docs/orchestration/cron-workflow.md` documents resume, reassign, and archive behavior for stale claims.

## Handoff Behavior

Stale claim entries include three operator paths:

- Resume: continue the same claim after reading the claim file and linked Beads issue.
- Reassign: PM/review may assign a replacement only after confirming the original worker is abandoned or unreachable.
- Archive: move the claim into `.agent-runs/claims/archive-<month>/` only after the Beads issue is closed, blocked with
  evidence, or explicitly superseded.

This keeps abandoned work visible while still allowing unrelated unblocked work to continue.

## Acceptance Evidence

Validation captured on 2026-06-02:

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `git diff --check`: passed.
- `uv run awf verify --profile ticket --json`: passed with zero failed checks.
- `uv run awf verify --profile increment --json`: passed with zero failed checks.
- `uv run awf workflow-fixture-test --json`: passed with `34/34` fixture checks before closure and again after
  `complete-work` closed `awf-h1z`.
- Ticket profile checks: `spec-lint`, `spec-kit-lint`, `bdd-lint`, `review-gate`, `repo-hygiene`,
  `workflow-state-lint`, and the nested acceptance command all passed.
- Increment profile checks: `bootstrap`, `spec-lint`, `spec-kit-lint`, `bdd-lint`, `bdd-run-fixture`, `review-gate`,
  `repo-hygiene`, `workflow-state-lint`, and `workflow-fixture-test` all passed.
- `increment-status` with explicit Goal 003 scope reported the active T011 claim and no stale claims yet, as expected
  for a fresh claim.
- A deterministic synthetic stale claim produced worker, branch, feature branch, issue, acceptance, age, and
  resume/reassign/archive handoff fields.

## Independent Review

Reviewer: `019e8714-cc5d-7e70-95e2-46ea206744be`

Outcome: accepted with no findings.

The reviewer accepted T011 evidence on 2026-06-02 after reviewing the T011 claim, stale-claim implementation, Goal 003
increment status behavior, stale-claim fixture coverage, operator docs, and this evidence report. The reviewer confirmed
that the evidence satisfies FR-013 and T011: stale active claims expose age, threshold, worker, branch, feature branch,
issue context, acceptance command, and resume/reassign/archive handoff guidance; active and stale claims are scoped to
the active increment; deterministic workflow fixture coverage exists and passed; operator behavior is documented; and
the validation evidence is coherent.
