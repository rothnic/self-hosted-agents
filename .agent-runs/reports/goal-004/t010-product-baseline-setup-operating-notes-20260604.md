# Goal 004 T010 Product Baseline Setup And Operating Notes

Date: 2026-06-04
Spec: `005-candidate-platform-decision-product-baseline`
Task: T010
Beads issue: `awf-3mc`
Worker: `codex-goal004-t010`

## Scope

T010 adds setup and operating notes for the selected Pydantic AI plus Langfuse and DBOS product baseline. It does not
add runnable product code, candidate-lane archive notes, migration notes, production hardening tickets, or final Goal
004 acceptance.

## Presenter Evidence

Added `docs/product-baseline/pydantic-ai-setup-operating-notes.md`.

The notes show another agent how to operate the product-baseline work-order workflow without hidden service state. They
cover:

- deterministic fixture mode and required repo-local checks;
- optional self-hosted Langfuse proof mode and its command shape;
- local DBOS durable proof mode and its disposable state boundary;
- start procedure from bootstrap through claim, validation, reviewer handoff, and `complete-work`;
- reset procedure for claims, local Pydantic AI artifacts, DBOS `/tmp` state, and self-hosted Langfuse proof state;
- inspect procedure for workflow state and run, trace, and evaluation artifacts;
- failure handling for missing tooling, stale claims, fixture failures, Langfuse unavailability, DBOS state conflicts,
  and reviewer rejection;
- evidence boundary required for future product-baseline work.

Updated links:

- `docs/product-baseline/pydantic-ai-review-gated-work-order.md`
- `apps/pydantic-ai/README.md`
- `docs/goals/004-candidate-platform-decision-product-baseline.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `docs/roadmap.md`

## Boundary

The setup notes keep deterministic validation independent from hosted credentials or cloud services. Self-hosted
Langfuse proof mode and DBOS local durable proof mode are additive operating paths. Production Langfuse operations,
DBOS production storage, DBOS worker topology, recovery rehearsal, live model/tool trace coverage, and richer eval
workflows remain follow-up proof gates.

## Validation

- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=273`.
- `uv run awf bdd-lint --json`: passed.
- `uv run awf bdd-run --driver fixture --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed `45/45`.
- `uv run awf verify --profile ticket --json`: passed all checks, including acceptance
  `uv run awf workflow-fixture-test`.

## Independent Review

Reviewer agent: `019e9041-7fe0-7bf1-a035-16ca746fede8`
Outcome: accepted

Findings:

- P3: The initial report recorded `repo-hygiene` as `checked_files=272`, while the reviewer's rerun reported
  `checked_files=273`. The pass/fail evidence was accurate. This report has been corrected to `273`.
- No blocking findings.
- No required follow-up tickets for T010 closure.

Evidence checked by reviewer:

- `docs/product-baseline/pydantic-ai-setup-operating-notes.md` defines deterministic fixture mode with no model key,
  hosted Logfire, Langfuse service, persistent DBOS service, or cloud dependency.
- The notes explicitly preserve hosted/cloud independence for fixture validation.
- Self-hosted Langfuse proof mode is optional, additive, and gated by `--require-langfuse-ingestion`.
- DBOS durable proof mode uses local disposable SQLite and JSONL state and avoids production topology claims.
- Start, reset, inspect, failure handling, and evidence-boundary procedures are present.
- Baseline workflow, app README, Goal 004, spec, and roadmap cross-links align T010 with the product-baseline scope.

Validation rerun by reviewer:

- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=273`.
- `uv run awf bdd-lint --json`: passed.
- `uv run awf bdd-run --driver fixture --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed `45/45`.
- `uv run awf verify --profile ticket --json`: passed with seven checks and acceptance command
  `uv run awf workflow-fixture-test`.
