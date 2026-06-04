# Goal 006 T013 Interface Decision Evidence

Status: presented for independent reviewer acceptance.

Ticket: `awf-s6n`
Task: `specs/007-operator-workbench-review-ux/tasks.md#T013`
Acceptance: `uv run awf workflow-fixture-test`

## Decision

The selected Goal 006 workbench interface is CLI/static repo-backed artifacts. A local UI is not selected for this goal.

The decision is captured in:

- `docs/workbench/interface-decision.md`
- `docs/workbench/status-artifact-schema.md`
- `.agent-runs/reports/workbench/interface-decision-20260604T103748Z.json`
- `.agent-runs/reports/workbench/operator-status-20260604T103821Z.json`

## Evidence

- `uv run awf interface-decision --json` returned `ok=true`, schema
  `awf.operator-workbench.interface-decision.v1`, decision `cli-static`, and
  `external_service_required=false`.
- `uv run awf interface-decision --write --json` wrote
  `.agent-runs/reports/workbench/interface-decision-20260604T103748Z.json`.
- `uv run awf operator-status --write --json` wrote
  `.agent-runs/reports/workbench/operator-status-20260604T103821Z.json` and surfaced `interface_decision`.
- `jq '{generated_by, path, has_path: has("path")}'` confirmed both persisted artifacts include their own `path` and
  record the `--write --json` command that generated the file.
- `uv run awf workflow-fixture-test --json` passed 69/69 after the T013 fixture assertion was added.
- `uv run awf repo-hygiene --json` passed after wrapping long decision strings.
- `uv run awf workflow-state-lint --json` passed.
- `uv run awf review-gate --json` passed with `human_required_count=0`.

## Review Iteration

Independent reviewer `019e9232-6e37-7c62-9b7b-18b207de17bb` initially rejected this evidence because the persisted
interface-decision JSON did not include its own `path` and recorded `generated_by` as the non-write command. The fix
updates the repo-local JSON artifact writer to include `path` before writing and updates write-mode `generated_by` for
`interface-decision` and `operator-status`; stale generated artifacts were replaced with the paths cited above.

The same independent reviewer then accepted the corrected evidence with no blocking findings and
`human_review_required=false`. The reviewer verified the corrected artifacts, decision docs, schema docs, code paths,
and live validation evidence. No follow-up tickets were required.

## Closure

`uv run awf complete-work --issue-id awf-s6n --write --json` closed Beads issue `awf-s6n`, marked T013 complete in
`specs/007-operator-workbench-review-ux/tasks.md`, and recorded Beads comment `144`.

Post-close evidence:

- `uv run awf ready-work --json` now reports `awf-1f9` / T014 as the next ready worker ticket.
- `uv run awf operator-status --write --json` wrote
  `.agent-runs/reports/workbench/operator-status-20260604T104517Z.json` with next ticket `awf-1f9`.
- `uv run awf workflow-fixture-test --json` passed 69/69 after T013 closure.
- `uv run awf repo-hygiene --json` passed.
- `uv run awf workflow-state-lint --json` passed.
- `git diff --check` passed.

## Acceptance Coverage

The decision record compares:

- operating burden
- self-hosting requirements
- accessibility
- small-screen review
- automation compatibility
- source-of-truth preservation

The CLI/static option is selected because the existing workbench artifacts already expose status, goal state,
increment state, evidence, review actions, reviewer decisions, branch/PR state, trace/eval links, and handoff
summaries without requiring a UI runtime or hosted credentials.

The local UI option is explicitly deferred because it would add runtime, asset/build, accessibility, small-screen, and
visual verification costs before evidence shows it improves operator decisions or scheduled-agent throughput.

## Boundaries

No local UI was implemented in T013. The work only records the interface decision, exposes it in `operator-status`, and
adds deterministic fixture coverage.

Credential-free validation is preserved. The decision path does not require hosted Logfire, hosted Langfuse, GitHub,
cloud credentials, external project tokens, or a UI runtime.

## Reviewer Request

Please accept or reject this T013 evidence. Review that:

- the CLI/static decision is explicit and evidence-based;
- the required comparison criteria are recorded;
- CLI/static repo source-of-truth workflows remain mandatory;
- no local UI implementation is included in this task;
- `operator-status` exposes `interface_decision`;
- deterministic validation remains credential-free and passed.
