# Goal 006 T001 Operator Views Evidence

## Scope

Beads issue: `awf-x12`.

Task: T001, research and define the minimum operator views in `docs/workbench/`.

Acceptance: `uv run awf workflow-fixture-test`.

## Completed Work

- Added `docs/workbench/README.md` as the workbench index and operating boundary.
- Added `docs/workbench/operator-views.md` with the minimum view catalog, source artifacts, priority, data rules,
  decision states, implementation sequence, and T001 non-goals.
- Added a workflow fixture assertion that verifies the workbench docs define required views, data sources, fallback
  behavior, decision states, and implementation sequencing.

## View Coverage

Minimum views defined:

- Executive Snapshot.
- Roadmap And Goals.
- Increment And Work Queue.
- Evidence Map.
- Review Gate.
- Trace And Eval.
- Branch And PR.
- Handoff.
- Health And Operations.

## Validation

Validation commands:

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- Targeted `operator_workbench_views_data()` check: passed with `ok=true` and `missing=[]`.
- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=365`.
- `uv run awf workflow-state-lint --json`: passed with `completed_tasks_checked=120` and `open_issues_checked=27`.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `uv run awf workflow-fixture-test --json`: passed after the line-length fix.
- `uv run awf verify --profile ticket --json`: passed; `spec-lint`, `spec-kit-lint`, `bdd-lint`, `review-gate`,
  `repo-hygiene`, `workflow-state-lint`, and acceptance were all `ok=true`.

## Reviewer Criteria

An independent reviewer should accept T001 only if:

- `docs/workbench/` defines the minimum operator views from current repo state.
- The docs keep the first workbench surface CLI/static and repo-backed until a later interface decision.
- The docs preserve Beads, Spec Kit, `.agent-runs/`, PR evidence, and workflow commands as source-of-truth surfaces.
- Deterministic validation remains credential-free and does not require GitHub or hosted services.
- The fixture acceptance command proves the new view catalog is present and complete enough for T002.

## Reviewer Outcome

Reviewer agent: `019e916b-4d7d-7903-a27c-cf4dd7e1fa3d`.

Outcome: accepted.

Findings: no blocking findings.

Human review required: false.

Required follow-up tickets: none.

Evidence checked by reviewer:

- `docs/workbench/README.md`: CLI/static first boundary, repo-backed source-of-truth rules, credential-free validation,
  and independent reviewer policy.
- `docs/workbench/operator-views.md`: nine minimum views defined from repo state, with priority, data rules, decision
  states, and T002 handoff.
- `tools/agent-workflow/src/agent_workflow/core.py`: `operator_workbench_views_data()` checks and the
  `workflow-fixture-test` assertion named `operator workbench minimum views are defined`.
- `.agent-runs/claims/awf-x12.json`: claim links objective, spec, T001, and acceptance command.
- `specs/007-operator-workbench-review-ux/tasks.md`: T001 scope matches the delivered docs.

Reviewer reran:

- `operator_workbench_views_data()`: passed with `ok=true` and `missing=[]`.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `uv run awf workflow-fixture-test --json`: passed with `57/57`.
