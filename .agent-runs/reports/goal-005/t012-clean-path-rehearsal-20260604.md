# Goal 005 T012 Clean-Path Rehearsal Evidence

## Ticket

- Beads issue: `awf-pt7`
- Spec task: `specs/006-self-hosted-deployment-operations-reference/tasks.md#T012`
- Acceptance: `uv run awf workflow-fixture-test`

## Rehearsal Scope

This was a local clean-path rehearsal for the selected Pydantic AI plus Langfuse/DBOS reference profile. It validated
repo-local backup, clean restore into `/tmp`, credential-free readiness, and a fresh deployment smoke artifact. It did
not claim production-like service promotion.

## Commands Run

- `uv run awf claim-work --worker-id codex-goal005-t012 --write --json`: claimed `awf-pt7`.
- `tar -czf /tmp/self-hosted-agents-backups/repo-evidence-20260604T060332Z.tgz .beads .agent-runs/claims .agent-runs/increments .agent-runs/reports .agent-runs/reviews .agent-runs/verifications specs docs`: failed because `.agent-runs/reviews` did not exist.
- `tar -czf /tmp/self-hosted-agents-backups/repo-evidence-20260604T060332Z.tgz .beads .agent-runs/claims .agent-runs/increments .agent-runs/reports .agent-runs/verifications specs docs`: passed.
- `tar -xzf /tmp/self-hosted-agents-backups/repo-evidence-20260604T060332Z.tgz -C /tmp/self-hosted-agents-restore-check-20260604T060332Z`: passed.
- `test -f /tmp/self-hosted-agents-restore-check-20260604T060332Z/.beads/issues.jsonl`: passed.
- `find /tmp/self-hosted-agents-restore-check-20260604T060332Z/.agent-runs/reports/goal-005 -maxdepth 2 -type f`: listed restored Goal 005 evidence.
- `uv run awf deployment-readiness --profile local --json`: passed with all hosted/service credentials unset.
- `uv run awf deployment-smoke --profile local --write --json`: passed and wrote a fresh smoke artifact.

## Evidence

- Rehearsal record:
  `.agent-runs/reports/goal-005/clean-path-rehearsal-20260604T060332Z/rehearsal.json`
- Backup archive outside git:
  `/tmp/self-hosted-agents-backups/repo-evidence-20260604T060332Z.tgz`
- Backup archive size:
  `10365259` bytes
- Restore target:
  `/tmp/self-hosted-agents-restore-check-20260604T060332Z`
- Restored state surfaces:
  `.beads/issues.jsonl`, `.agent-runs/claims`, `.agent-runs/increments`, `.agent-runs/reports`,
  `.agent-runs/verifications`, `specs`, and `docs`
- Fresh smoke evidence:
  `.agent-runs/reports/goal-005/deployment-smoke-local-20260604T060414Z/deployment-smoke.json`
- Fresh smoke correlation:
  `run-e93c5940e04ff8cf99fe2e21`, `trace-f9cac59a8a238a726e8289e1`, `eval-65ca933b165e3794`,
  `dbos-workflow-dbb52094190e3493ff4ac538`

## Gaps

- Self-hosted Langfuse service-backed backup, restore, and trace visibility still require host-local service evidence.
- Production DBOS storage backup and restore still require a controlled self-hosted database proof.
- `.agent-runs/reviews` was absent in this checkout. The backup runbook now treats it as an optional archive surface
  instead of failing the repo-local backup when acceptance is stored in Beads comments and committed reports.

## Follow-Up Routing

- `awf-eas`: Langfuse production operations proof covers self-hosted retention, backup, reset, and recovery.
- `awf-lkr`: DBOS production storage proof covers self-hosted Postgres or equivalent storage topology.
- `awf-5ae`: DBOS recovery rehearsal and retention proof covers service-backed restore and cleanup.
- `awf-4t2`: Phoenix or Opik fallback comparison remains the route if Langfuse burden is too high.

No new Beads issue was created for `.agent-runs/reviews` because this slice fixed the runbook drift directly.

## Boundary

T012 proves the local clean-path backup, restore, readiness, and smoke path with repo-local evidence and explicit
service-backed gaps. T013 remains responsible for presenting complete Goal 005 evidence and recording independent
reviewer acceptance or rejection.
