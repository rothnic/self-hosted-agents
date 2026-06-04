# Goal 006 T005 Goal Dashboard Evidence

Recorded: 2026-06-04T07:55:10Z
Presenter: Codex implementer
Ticket: awf-sdh
Task: specs/007-operator-workbench-review-ux/tasks.md#T005
Acceptance: uv run awf workflow-fixture-test

## Scope

T005 adds a long-horizon goal dashboard to the repo-backed operator status artifact. It does not add the later increment
dashboard, evidence view, durable review actions, branch/PR integration, trace/eval deep links, handoff summaries, or
local UI.

## Evidence Presented

- Added `goal_dashboard` to `uv run awf operator-status --json`.
- Added dashboard schema `awf.operator-workbench.goal-dashboard.v1`.
- Linked ordered child goals from `docs/goals/000-self-hosted-agent-system-roadmap.md`.
- Marked Goals 001 through 005 as accepted with repo-local acceptance evidence links.
- Marked Goal 006 as active with current phase `Goal 006 Phase 2: Repo-Backed Status Surfaces`.
- Linked accepted Goal 006 checkpoint evidence from planning through T004.
- Exposed active next ticket `awf-sdh` and next task T005.
- Preserved the required presenter plus independent reviewer evidence model.
- Added `docs/workbench/goal-dashboard.md`.
- Updated `docs/workbench/README.md`, `docs/workbench/operator-status-report.md`, and
  `docs/workbench/status-artifact-schema.md`.
- Added the workflow fixture assertion `operator workbench long-horizon goal dashboard is generated`.

## Generated Artifact

`uv run awf operator-status --write --json` wrote
`.agent-runs/reports/workbench/operator-status-20260604T080341Z.json`.

The generated dashboard summary was:

- `schema=awf.operator-workbench.goal-dashboard.v1`
- `current_goal_id=006`
- `phase=Goal 006 Phase 2: Repo-Backed Status Surfaces`
- `next_ticket=awf-sdh`
- `ordered_goal_count=6`
- `accepted_goal_count=5`
- `active_goal_count=1`
- `accepted_evidence_count=10`
- `follow_up_epic_count=9`

## Validation Evidence

- `python3 -m py_compile tools/agent-workflow/src/agent_workflow/core.py tools/agent-workflow/src/agent_workflow/cli.py`: passed.
- `uv run awf operator-status --json`: passed and summarized T005 / `awf-sdh`.
- `uv run awf operator-status --write --json`: passed and wrote the generated artifact above.
- `uv run awf repo-hygiene --json`: passed, `checked_files=378`.
- `git diff --check`: passed.
- `uv run awf workflow-fixture-test --json`: passed, `61/61`.
- `uv run awf verify --profile ticket --json`: passed, including spec lint, Spec Kit lint, BDD lint, review gate,
  repo hygiene, workflow-state lint, and acceptance.

## Reviewer Request

An independent reviewer should verify that the dashboard is generated from repo state, names the active roadmap phase,
links accepted evidence, preserves self-hosted credential-free validation, and does not implement later T006-T017
surfaces.

## Reviewer Outcome

Initial independent reviewer agent: `019e91a4-0800-7f42-92a1-fc487d67a02a`.

Initial outcome: rejected.

Findings:

- P1: `roadmap.accepted_evidence` still used a raw recent-report path filter and counted the unreviewed T005 presenter
  report as accepted evidence.
- P2: Goal 004 was shown as accepted while its final accepted T014 evidence item was classified as `accepted=false`
  because the report also recorded an initial rejection before remediation.

Remediation:

- Updated `roadmap.accepted_evidence` to use the same reviewer-accepted Goal 006 evidence list as `goal_dashboard`.
- Tightened report acceptance detection to explicit accepted-outcome and reviewer-accepted phrases.
- Regenerated `.agent-runs/reports/workbench/operator-status-20260604T080341Z.json`; the corrected artifact stops Goal
  006 accepted evidence at T004 before T005 review, and classifies Goal 004 T014 as accepted.

Delta review:

- Outcome: accepted.
- Findings: none.
- Required follow-up tickets: none.
- Human review required: false.
- Evidence checked: corrected generated artifact, `goal_dashboard`, `core.py`, presenter report, `operator-status`,
  `repo-hygiene`, `git diff --check`, `workflow-fixture-test`, and `verify --profile ticket`.

## Closure

`uv run awf complete-work --issue-id awf-sdh --write --json` closed T005, added Beads comment `136`, marked
`specs/007-operator-workbench-review-ux/tasks.md` complete, and reran workflow-state lint successfully.

Post-close `uv run awf operator-status --write --json` wrote
`.agent-runs/reports/workbench/operator-status-20260604T080857Z.json`. The post-close dashboard points to T006 /
`awf-vty` and reports `accepted_evidence_count=11`, including T005 after independent reviewer acceptance.

Post-close `uv run awf workflow-fixture-test --json`: passed, `61/61`.
