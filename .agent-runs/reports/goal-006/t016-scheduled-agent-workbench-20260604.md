# Goal 006 T016 Presenter Evidence

Presented by: Codex implementer
Ticket: awf-svr
Spec task: specs/007-operator-workbench-review-ux/tasks.md#T016
Objective: agentic-development-foundation
Acceptance command: uv run awf workflow-fixture-test

## Scope

T016 asks for documentation showing how scheduled agents use the workbench artifacts without a fragile UI dependency.
This slice keeps the Goal 006 interface CLI/static and adds a first-class scheduled-agent usage artifact so PM,
orchestrator, worker, integrator, and health loops can start from repo-local commands and exact artifact handles.

## Evidence Presented

- Added `uv run awf scheduled-agent-workbench --json` and `--write --json`.
- Generated `.agent-runs/reports/workbench/scheduled-agents/scheduled-agent-workbench-20260604T113209Z.json`.
- Added `docs/workbench/scheduled-agents.md`.
- Indexed the new document in `docs/workbench/README.md`.
- Cross-linked the scheduled-agent contract from `docs/workbench/interface.md`.
- Updated `docs/workbench/status-artifact-schema.md` and `docs/workbench/operator-status-report.md`.
- Added operator status integration through `scheduled_agent_usage`.
- Added fixture checks for schema, docs, role entrypoints, no UI session requirement, no chat context requirement,
  credential-free self-hosted validation, and post-T016 routing to T017.

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`
  passed.
- `uv run awf scheduled-agent-workbench --json` passed.
- `uv run awf scheduled-agent-workbench --write --json` passed.
- `uv run awf operator-status --json` passed and included `scheduled_agent_usage`.
- Targeted helper check passed:
  `core.operator_workbench_interface_data()["ok"] == True` and
  `core.operator_workbench_scheduled_agent_data()["ok"] == True`.
- `uv run awf workflow-fixture-test --json` initially failed because `docs/workbench/interface.md` lacked the exact
  lowercase term `scheduled agents`; the doc was corrected.
- `uv run awf workflow-fixture-test --json` passed after the fix with 72/72 checks.
- `uv run awf verify --profile ticket --json` passed.
- `uv run awf repo-hygiene --json` passed with 439 checked files.
- `uv run awf workflow-state-lint --json` passed.
- `uv run awf review-gate --json` passed with no human-required gate.
- `git diff --check` passed.

## Reviewer Request

Independent reviewer should accept or reject whether T016 is complete by checking:

- The artifact schema is `awf.operator-workbench.scheduled-agent-usage.v1`.
- The command and docs explain scheduled-agent use without a fragile UI dependency.
- PM/review, orchestrator, worker, integrator, and health role entrypoints are covered.
- The artifact contract uses Beads ready work, claim files, presenter evidence, and independent reviewer records.
- The contract does not require a UI session, browser runtime, terminal UI runtime, prior chat context, hosted
  credentials, cloud services, or external project tokens.
- Follow-on Goal 006 acceptance work remains routed to T017 instead of being claimed in T016.

## Reviewer Outcome

Accepted by independent reviewer agent `019e926c-0c0e-7cd0-b05a-718f63652740`.

Verdict: accepted.

Blocking findings: none.

Reviewer evidence checked:

- T016 remains active before closure and T017 remains separate/open.
- `docs/workbench/scheduled-agents.md` defines CLI/static, repo-local, credential-free scheduled-agent usage without
  UI session or chat-context dependency.
- The generated artifact uses `awf.operator-workbench.scheduled-agent-usage.v1`, covers PM/review, orchestrator,
  worker, integrator, and health entrypoints, and marks UI/browser/TUI/chat/external-service dependencies false.
- `tools/agent-workflow/src/agent_workflow/cli.py` wires the CLI command.
- `tools/agent-workflow/src/agent_workflow/core.py` integrates `scheduled_agent_usage` into operator status and fixture
  coverage.

Reviewer independent checks:

- `uv run awf scheduled-agent-workbench --json` passed.
- `uv run awf operator-status --json` passed and included `scheduled_agent_usage`.
- `uv run awf workflow-fixture-test --json` passed with 72/72 checks.
- `uv run awf verify --profile ticket --json` passed.
- `uv run awf repo-hygiene --json` passed with 440 checked files.
- `uv run awf workflow-state-lint --json` passed.
- `uv run awf review-gate --json` passed with `human_required_count: 0`.
- `git diff --check` passed.

Non-blocking follow-up: proceed with T017 to present final Goal 006 evidence and record independent reviewer acceptance
or rejection.
