# Goal 004 T013 Production Hardening Follow-Up Tickets

Date: 2026-06-04
Spec: `005-candidate-platform-decision-product-baseline`
Task: T013
Beads issue: `awf-fpn`
Worker: `codex-goal004-t013`

## Scope

T013 records follow-up Beads work for production-hardening gaps that remain after the platform decision. It does not
implement those hardening gaps, promote the selected stack as the final solution, or record final Goal 004 increment
acceptance.

## Presenter Evidence

Created Goal 004-specific follow-up Beads epics:

- `awf-4x7`: Follow up product baseline runnable work-order app proof.
- `awf-6zf`: Follow up live model and tool trace coverage proof.
- `awf-7ck`: Follow up product tool and context approval boundary proof.

Existing follow-up epics already covered broader production promotion gaps:

- `awf-eas`: Langfuse production operations proof.
- `awf-2du`: Langfuse evaluation workflow proof.
- `awf-4t2`: Phoenix or Opik fallback comparison.
- `awf-lkr`: DBOS production storage proof.
- `awf-ygu`: DBOS worker and queue topology proof.
- `awf-5ae`: DBOS recovery rehearsal and retention proof.

Updated links:

- `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md`
- `docs/goals/004-candidate-platform-decision-product-baseline.md`
- `docs/requirements-matrix.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `docs/roadmap.md`
- `objectives/current.md`

## Gap Coverage

The new epics cover Goal 004-specific gaps that were not already represented by Goal 001 or Goal 002 hardening epics:

- the product-baseline work-order app is defined and contracted, but not yet implemented as a runnable product
  boundary;
- live or explicitly simulated model/tool trace coverage, token/cost fields, failure spans, and tool-call context are
  not yet proven for the selected product-baseline lane;
- real repo-context and tool approval boundaries are not yet proven through typed adapters or MCP-style boundaries.

These are follow-up epics, not blockers for accepting the Goal 004 platform decision. They remain final-solution
promotion gates until future specs and tickets close them with repo-local or self-hosted evidence.

## Boundary

The follow-up items are Beads epics rather than Goal 004 worker tasks so T014 can still record final Goal 004 increment
acceptance after the backlog is durable. Future PM/spec work should decompose each epic into focused specs and Beads
tasks before implementation.

## Validation

- `br list --status open --json`: shows `awf-4x7`, `awf-6zf`, and `awf-7ck` as open Goal 004 follow-up epics.
- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=281`.
- `uv run awf workflow-state-lint --json`: passed with `completed_tasks_checked=105` and `open_issues_checked=12`.
- `uv run awf ready-work --json`: kept `awf-fpn` as the ready T013 task and kept `awf-ivd` blocked behind it.
- `uv run awf verify --profile ticket --json`: passed, including `workflow-fixture-test` acceptance.
- `uv run awf workflow-fixture-test --json`: passed `45/45`.

## Independent Review

Reviewer agent: `019e9074-65d6-7290-9b65-3e8f59916e14`

Initial outcome: rejected.

Finding:

- P1: `awf-6zf` and `awf-7ck` had non-resolving `external_ref` anchors for
  `docs/requirements-matrix.md#live-model-tool-trace-follow-up` and
  `docs/requirements-matrix.md#tool-context-approval-follow-up`.

Remediation:

- Added durable `Live Model Tool Trace Follow-up` and `Tool Context Approval Follow-up` sections to
  `docs/requirements-matrix.md` so the Beads external references resolve to product-baseline promotion-gap context.

Final outcome: accepted.

Re-check evidence:

- `awf-6zf` external ref resolves to `docs/requirements-matrix.md#live-model-tool-trace-follow-up`.
- `awf-7ck` external ref resolves to `docs/requirements-matrix.md#tool-context-approval-follow-up`.
- The three Goal 004 follow-up epics cover product app boundary, live or simulated model/tool tracing, and tool/context
  approval without duplicating Goal 001 or Goal 002 operations epics.
- Pydantic AI remains the product baseline, not the final solution.
- No required follow-up tickets.
