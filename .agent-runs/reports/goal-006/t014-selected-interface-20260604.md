# Goal 006 T014 Selected Interface Evidence

Ticket: `awf-1f9`
Task: `specs/007-operator-workbench-review-ux/tasks.md#T014`
Presenter agent: Codex implementer
Review status: accepted by independent reviewer
Reviewer agent: `019e924c-0d15-73e1-bf3e-2b08a29f94d2`

## Scope

Implemented the selected CLI/static workbench interface with restrained operating-tool design. This follows the T013
decision to avoid a local UI for Goal 006 and keep the workbench generated from repo state.

## Completed Work

- Added `uv run awf workbench-interface --json`.
- Added `uv run awf workbench-interface --write --json`.
- Added schema `awf.operator-workbench.interface.v1`.
- Added generated interface artifact:
  `.agent-runs/reports/workbench/interface/workbench-interface-20260604T105847Z.json`.
- Added `docs/workbench/interface.md`.
- Updated `docs/workbench/README.md`, `docs/workbench/operator-status-report.md`, and
  `docs/workbench/status-artifact-schema.md`.
- Added fixture coverage for the selected interface.
- Nested new interface artifacts under `.agent-runs/reports/workbench/interface/` so the workbench report directory
  stays within repo-hygiene child limits.

## Design Boundary

No local web UI, terminal UI runtime, build step, server process, hosted credential, hosted Logfire, hosted Langfuse,
GitHub token, cloud token, or external project token is required. Optional self-hosted Langfuse and PR links remain
repo-local evidence surfaced by existing workbench artifacts.

## Interface Shape

The generated artifact includes:

- Decision strip: phase, next owner, recommendation, next ticket, review state, and human-required state.
- Four primary actions: inspect status, continue work, record review, and run acceptance.
- Six panels: decision, work, evidence, review, trace/eval, and branch/PR.
- Exact source handles for docs, claims, presenter/reviewer reports, verification artifacts, traces, evals, PR fallback,
  and Beads comments.
- Scheduled-agent compatibility fields.

## Validation

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`
  passed.
- `uv run awf workbench-interface --json` passed.
- `uv run awf workbench-interface --write --json` passed.
- `uv run awf repo-hygiene --json` passed after nested artifact write path.
- `uv run awf workflow-fixture-test --json` passed, 70/70.
- `uv run awf verify --profile ticket --json` passed.
- `uv run awf workflow-state-lint --json` passed.
- `uv run awf review-gate --json` passed with `human_required_count: 0`.
- `git diff --check` passed.

## Acceptance Request

Independent reviewer should accept or reject whether T014 is complete:

1. The selected CLI/static interface is implemented as a first-class command and generated artifact.
2. The design is restrained and operator-oriented, with no local UI runtime introduced.
3. The interface preserves repo source-of-truth artifacts and exact command/file handles.
4. Deterministic validation remains credential-free.
5. T015 and T016 remain future tasks; this report does not claim their completion.

## Reviewer Outcome

Outcome: accepted.

Independent reviewer agent `019e924c-0d15-73e1-bf3e-2b08a29f94d2` accepted T014 with no blocking findings.

Reviewer evidence checked:

- `.agent-runs/reports/goal-006/t014-selected-interface-20260604.md`
- `specs/007-operator-workbench-review-ux/tasks.md#T014`
- `docs/workbench/interface.md`
- `docs/workbench/status-artifact-schema.md`
- `tools/agent-workflow/src/agent_workflow/cli.py`
- `tools/agent-workflow/src/agent_workflow/core.py`
- `.agent-runs/reports/workbench/interface/workbench-interface-20260604T105847Z.json`

Reviewer rechecked:

- `uv run awf workbench-interface --json`
- `uv run awf workflow-fixture-test --json`, 70/70
- `uv run awf verify --profile ticket --json`
- `uv run awf repo-hygiene --json`
- `uv run awf workflow-state-lint --json`
- `uv run awf review-gate --json`
- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`
- `git diff --check`

Required follow-up tickets: none for T014. T015 and T016 remain correctly open future tasks.
