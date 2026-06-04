# Goal 004 T012 Non-Selected Candidate Migration Notes

Date: 2026-06-04
Spec: `005-candidate-platform-decision-product-baseline`
Task: T012
Beads issue: `awf-3u9`
Worker: `codex-goal004-t012`

## Scope

T012 records migration notes for reusable code, fixtures, or evidence from frozen non-selected candidate lanes. It does
not move code, reopen frozen lanes, create production-hardening follow-up tickets, or record final Goal 004 increment
acceptance.

## Presenter Evidence

Added `docs/candidate-references/non-selected-candidate-migration-notes.md`.

The migration note records:

- rules for moving assets from frozen references into selected or shared locations;
- concrete posture for LangGraph fixture shape, artifact contract, functional-needs mapping, deterministic eval
  criteria, CLI artifact convention, and graph semantics;
- concrete posture for Mastra TypeScript contrast notes and LangSmith benchmark expectations;
- future extraction candidates for shared run artifact schema, stable ids, product-baseline fixture schema, and shared
  evaluation rubric;
- explicit non-migration decisions for framework-specific code, transient outputs, hosted-only evidence, bytecode
  caches, and rejection/deferment docs.

Updated links:

- `docs/candidate-references/frozen-non-selected-candidates.md`
- `docs/goals/004-candidate-platform-decision-product-baseline.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `docs/roadmap.md`
- `docs/project-structure.md`
- `apps/pydantic-ai/README.md`

## Boundary

This is a migration posture, not an implementation migration. Product-baseline work remains focused on
`apps/pydantic-ai/`. LangGraph Python and Mastra TypeScript remain frozen references unless a future Beads ticket or ADR
explicitly reopens them.

T013 remains responsible for production-hardening follow-up tickets. T014 remains responsible for final Goal 004
increment verification and reviewer-accepted completion evidence.

## Validation

- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=278`.
- `uv run awf bdd-lint --json`: passed.
- `uv run awf bdd-run --driver fixture --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed with `total=45`, `passed=45`, `failed=0`.
- `uv run awf verify --profile ticket --json`: passed. Checks passed: `spec-lint`, `spec-kit-lint`, `bdd-lint`,
  `review-gate`, `repo-hygiene`, `workflow-state-lint`, and acceptance `uv run awf workflow-fixture-test`.

## Independent Review

Reviewer agent: `019e9066-9000-77f0-bbcb-29074e56145b`
Outcome: accepted

Findings: no findings.

Evidence checked:

- `docs/candidate-references/non-selected-candidate-migration-notes.md` defines migration rules and keeps validation
  credential-free.
- `docs/candidate-references/non-selected-candidate-migration-notes.md` records concrete postures for shared fixtures,
  artifact contracts, functional mapping, eval criteria, CLI conventions, LangGraph semantics, Mastra, and LangSmith.
- `docs/candidate-references/frozen-non-selected-candidates.md` keeps non-selected lanes frozen and links the T012
  notes.
- Goal, spec, roadmap, project-structure, and selected-lane README links are accurate and preserve the selected-lane
  boundary.
- The active claim matches T012 / `awf-3u9`.
- This presenter report records the expected validation set.

Reviewer validation:

- `git diff --check`: passed.
- `uv run awf repo-hygiene --json`: passed with `checked_files=279`.
- `uv run awf bdd-lint --json`: passed.
- `uv run awf bdd-run --driver fixture --json`: passed.
- `uv run awf workflow-fixture-test --json`: passed with `total=45`, `passed=45`, `failed=0`.
- `uv run awf verify --profile ticket --json`: passed with `failed_checks=[]`.

Required follow-up tickets: none.
