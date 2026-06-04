# Goal 006 T002 BDD Contract Evidence

## Scope

Beads issue: `awf-288`.

Task: T002, add an operator workbench BDD contract for status, evidence, review decisions, and handoffs.

Acceptance: `uv run awf workflow-fixture-test`.

## Completed Work

- Added `tests/workflow/features/operator_workbench_review_ux.feature` with actor-centered scenarios for decision
  status, durable review decisions, and scheduled-agent handoffs.
- Updated `tests/workflow/drivers/README.md` with the operator workbench driver boundary and observable actions.
- Updated `tests/workflow/drivers/fixture_driver.py` so the fixture driver reports an operator workbench observation.
- Added `operator_workbench_bdd_contract_data()` and a `workflow-fixture-test` assertion named
  `operator workbench BDD contract covers status evidence review and handoffs`.

## Contract Coverage

The BDD contract covers:

- Status: active objective, current goal/spec, Beads work state, validation state, and next owner.
- Evidence: repo-local trace, eval, branch, PR, report, review, and fallback links.
- Review decisions: reviewer id, verdict, evidence checked, findings, follow-up routing, and human-required status.
- Handoffs: next ticket or role, required files, validation commands, risks, and exact artifact handles.

## Validation

Validation commands:

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py`: passed.
- `uv run awf bdd-lint --json`: passed and collected `operator_workbench_review_ux.feature`.
- `uv run awf bdd-run --driver fixture --json`: passed and included the operator workbench feature and observation.
- Targeted `operator_workbench_bdd_contract_data()` check: passed with `ok=true` and `missing=[]`.
- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=367`.
- `uv run awf workflow-fixture-test --json`: passed with `58/58`.
- `uv run awf workflow-state-lint --json`: passed with `completed_tasks_checked=121` and `open_issues_checked=26`.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `uv run awf verify --profile ticket --json`: passed; `spec-lint`, `spec-kit-lint`, `bdd-lint`, `review-gate`,
  `repo-hygiene`, `workflow-state-lint`, and acceptance were all `ok=true`.

## Reviewer Criteria

An independent reviewer should accept T002 only if:

- The feature file is implementation-agnostic and actor-centered.
- The contract covers status, evidence, review decisions, and handoffs.
- The driver notes define a future implementation boundary without product adapters or compatibility shims.
- Deterministic validation remains credential-free and does not require hosted services, cloud credentials, GitHub access,
  or external project tokens.
- The fixture acceptance command proves the BDD contract is present and connected to the repo-local driver boundary.

## Reviewer Outcome

Reviewer agent: `019e9175-86d4-72b3-98f1-af27e927b050`.

Outcome: accepted.

Findings: none.

Human review required: false.

Required follow-up tickets: none.

Evidence checked by reviewer:

- `tests/workflow/features/operator_workbench_review_ux.feature`: actor-centered scenarios cover status, evidence,
  review decisions, and scheduled handoffs without implementation APIs.
- `tests/workflow/drivers/README.md`: defines the future driver boundary as test harness behavior, not product adapters
  or compatibility shims.
- `tests/workflow/drivers/fixture_driver.py`: fixture emits the operator workbench observation.
- `tools/agent-workflow/src/agent_workflow/core.py`: `operator_workbench_bdd_contract_data()` verifies required terms,
  surfaces, decision verbs, and credential-free fallback.
- `.agent-runs/claims/awf-288.json`: claim links objective, spec, T002, and acceptance command.
- `specs/007-operator-workbench-review-ux/tasks.md`: T002 scope matches delivered work.

Reviewer reran:

- `operator_workbench_bdd_contract_data()`: passed with `ok=true` and `missing=[]`.
- `uv run awf bdd-lint --json`: passed and collected `operator_workbench_review_ux.feature`.
- `uv run awf bdd-run --driver fixture --json`: passed and included the operator workbench feature plus observation.
- `uv run awf review-gate --json`: passed with `human_required_count=0`.
- `uv run awf workflow-fixture-test --json`: passed with `58/58`.
