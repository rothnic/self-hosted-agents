# Goal 004 T011 Frozen Non-Selected Candidate References

Date: 2026-06-04
Spec: `005-candidate-platform-decision-product-baseline`
Task: T011
Beads issue: `awf-9a9`
Worker: `codex-goal004-t011`

## Scope

T011 freezes or archives non-selected candidates as comparison references with explicit tradeoffs. It does not migrate
reusable code or fixtures, create production-hardening follow-up tickets, or record final Goal 004 acceptance.

## Presenter Evidence

Added `docs/candidate-references/frozen-non-selected-candidates.md`.

The policy freezes non-selected lanes in place instead of physically moving directories. This preserves runnable
comparison history and avoids path churn before the selected product baseline is deeper.

Candidate dispositions:

- LangGraph Python plus Langfuse: frozen comparison reference.
- Mastra TypeScript plus shared contracts: frozen deferred contrast reference.
- LangSmith baseline: external benchmark only.

The policy records:

- allowed reference-maintenance changes;
- disallowed product-lane changes;
- evidence-based reasons each candidate remains in the repo;
- reasons each candidate should not be deepened by default;
- explicit reopen triggers;
- the T012 boundary for migration of reusable code, fixtures, or evidence.

Updated links:

- `apps/langgraph-python/README.md`
- `apps/langgraph-python/implementation-plan.md`
- `apps/mastra-ts/README.md`
- `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md`
- `docs/goals/004-candidate-platform-decision-product-baseline.md`
- `docs/project-structure.md`
- `docs/roadmap.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`

## Boundary

This is a freeze, not deletion. `apps/langgraph-python/` remains runnable comparison history. `apps/mastra-ts/` remains
a deferred TypeScript reference. Product-baseline work should deepen `apps/pydantic-ai/` unless a future Beads ticket
or ADR explicitly reopens a non-selected lane.

T012 remains responsible for migration notes for reusable code, fixtures, or evidence from non-selected lanes.

## Validation

- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=275`.
- `uv run awf bdd-lint --json`: passed.
- `uv run awf bdd-run --driver fixture --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed with `total=45`, `passed=45`, `failed=0`.
- `uv run awf verify --profile ticket --json`: passed. Checks passed: `spec-lint`, `spec-kit-lint`, `bdd-lint`,
  `review-gate`, `repo-hygiene`, `workflow-state-lint`, and acceptance `uv run awf workflow-fixture-test`.

Post-close workflow hygiene fix:

- `uv run awf cleanup-work --write --json` archived the T011 claim and surfaced that
  `.agent-runs/claims/archive-2026-06` reached 26 files, exceeding repo hygiene's 25-file directory limit.
- Updated `cleanup-work` archive path selection to shard claim archives under `.agent-runs/claims/archive-YYYY-MM/<key>/`
  and moved existing June claim archives into deterministic shards.
- `uv run awf repo-hygiene --json`: passed with `checked_files=276`.
- `uv run awf workflow-state-lint --json`: passed with `completed_tasks_checked=104`, `open_issues_checked=10`.
- `uv run awf workflow-fixture-test --json`: passed with `total=45`, `passed=45`, `failed=0`.
- `uv run awf verify --profile ticket --json`: passed after archive sharding. Checks passed: `spec-lint`,
  `spec-kit-lint`, `bdd-lint`, `review-gate`, `repo-hygiene`, `workflow-state-lint`, and acceptance
  `uv run awf workflow-fixture-test`.

## Independent Review

Reviewer agent: `019e904d-d620-7ca0-893e-8c33c646208b`
Outcome: accepted

Findings: no findings.

Evidence checked:

- `docs/candidate-references/frozen-non-selected-candidates.md` defines allowed and disallowed freeze policy,
  candidate dispositions, hosted-service boundary, and T012 migration boundary.
- `apps/langgraph-python/README.md` and `apps/mastra-ts/README.md` mark those lanes as frozen references, not active
  product lanes.
- ADR, goal, roadmap, project structure, and spec updates consistently keep Pydantic AI plus Langfuse/DBOS as the
  selected product-baseline lane.
- This presenter report records the validation set and boundary.

Reviewer validation:

- `git diff --check`: passed.
- `uv run awf verify --profile ticket --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed with `total=45`, `passed=45`, `failed=0`.

Required follow-up tickets: none.

## Narrow Review After Archive Path Alignment

Reviewer agent: `019e905d-4e05-7881-9b41-6f2d4004317d`
Outcome: accepted

Findings: no findings.

Evidence checked:

- `tools/agent-workflow/src/agent_workflow/core.py` adds deterministic claim archive sharding from claim ids, creates
  the shard parent before moving archived claims, and updates synthetic fixture archive paths to sharded paths.
- `tools/agent-workflow/src/agent_workflow/core.py` cleanup fixture assertions check expected shard markers.
- `docs/orchestration/cron-workflow.md` documents the sharded archive handoff path and explains the key exists for
  repo-hygiene fanout limits.
- This report preserves the post-close sharding evidence and prior reviewer acceptance.

Reviewer validation:

- `git diff --check`: passed.
- `uv run awf cleanup-work --json`: passed with no obsolete active claims.
- `uv run awf repo-hygiene --json`: passed with `checked_files=276`.
- `uv run awf workflow-fixture-test --json`: passed with `total=45`, `passed=45`, `failed=0`.

Required follow-up tickets: none.

## Final Review After Cleanup Hygiene Fix

Reviewer agent: `019e9056-e7f8-77b3-8026-8f4a33165577`
Outcome: accepted

Findings: no findings.

Evidence checked:

- `docs/candidate-references/frozen-non-selected-candidates.md` keeps Pydantic AI plus Langfuse/DBOS as the selected
  baseline, freezes LangGraph and Mastra as references, treats LangSmith as external benchmark only, and preserves the
  T012 migration boundary.
- `tools/agent-workflow/src/agent_workflow/core.py` shards archived claims under
  `.agent-runs/claims/archive-YYYY-MM/<key>/` using deterministic claim-id-derived keys.
- Claim evidence is preserved at `.agent-runs/claims/archive-2026-06/9/awf-9a9.json`, with no root-level JSON files
  left in `.agent-runs/claims/archive-2026-06`.
- `.beads/issues.jsonl` closes `awf-9a9`; `specs/005-candidate-platform-decision-product-baseline/tasks.md` marks
  T011 complete; the increment ledger routes next ready work to T012.

Reviewer validation:

- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=276`.
- `uv run awf workflow-state-lint --json`: passed.
- `uv run awf cleanup-work --json`: passed with no obsolete active claims.
- `uv run awf verify --profile ticket --json`: passed after archive sharding with `failed_checks=[]`.
- `uv run awf workflow-fixture-test --json`: passed with `total=45`, `passed=45`, `failed=0`.

Required follow-up tickets: none.
