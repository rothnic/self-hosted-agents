# Goal 004 T002 Mastra Contrast Decision

Date: 2026-06-02

Presenter: codex-goal004-t002

Work item: `awf-8nb`

Objective: `agentic-development-foundation`

Spec: `005-candidate-platform-decision-product-baseline`

Task: T002, decide whether Mastra TypeScript needs a runnable contrast slice before platform selection.

Acceptance command: `uv run awf workflow-fixture-test`

## Decision

Mastra TypeScript does not need a runnable contrast slice before the Goal 004 platform selection.

Disposition: `deferred-before-platform-selection`.

Mastra remains a documented contrast candidate, but it must not be scored as implementation-proven in T003 or T004.
The platform decision can proceed with Mastra marked as not comparable from implementation evidence, while preserving a
future reopen path if TypeScript-specific product needs appear.

## Evidence Checked

- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `specs/005-candidate-platform-decision-product-baseline/plan.md`
- `specs/005-candidate-platform-decision-product-baseline/tasks.md`
- `docs/comparison-evidence.md`
- `docs/requirements-matrix.md`
- `.agent-runs/reports/goal-004-t001-candidate-evidence-audit-20260602.md`
- `apps/mastra-ts/README.md`
- `docs/research/llm-observability-solution-space.md`
- Official Mastra framework, workflow, and observability pages checked on 2026-06-02:
  - `https://mastra.ai/`
  - `https://mastra.ai/ai-workflows`
  - `https://mastra.ai/ai-agent-observability`
  - `https://mastra.ai/ai-agent-framework`

## Rationale

The T001 audit found Pydantic AI has committed run, self-hosted trace, evaluation, setup, local durable, and gap
evidence. LangGraph Python has partial implementation evidence. Mastra has only planning/reference evidence and no
runnable app, package manifest, fixture, trace export, eval artifact, or durable runtime proof.

Current Mastra documentation supports the idea that Mastra is a credible TypeScript contrast candidate: it is a
TypeScript agent framework with agents, workflows, observability, evals, OpenTelemetry-compatible tracing, workflow
suspend/resume, Studio, and Node-compatible deployment paths. That strengthens the reason to keep Mastra as a future
reference, but it does not create repo-local implementation evidence.

The project's current target user and requirements remain Python-first. A runnable Mastra slice would mainly answer
cross-language ownership and TypeScript workflow ergonomics. It would not directly close the highest-risk final
promotion blockers already visible in the stronger tested lane: production DBOS storage, worker topology, recovery
operations, Langfuse operating recovery, live model/tool trace coverage, and richer eval workflows.

Adding Mastra now would also expand scope before Goal 004 records a platform decision. That would slow the roadmap
without being required by FR-005, because FR-005 requires repo-local run, trace, evaluation, setup, durable, and gap
evidence for the selected primary stack, not for every reference candidate.

## T003 And T004 Instructions

T003 should normalize Mastra as:

- evidence status: `missing implementation evidence`
- disposition: `deferred-before-platform-selection`
- scoring status: `not implementation-comparable`
- rationale: useful TypeScript contrast, but lower fit with the Python-first owner and no repo-local evidence

T004 should score Mastra only as a non-selected, unproven reference. It should not assign implementation-backed scores
for observability, evaluation, durable execution, scalability, or operating effort.

## Reopen Triggers

Create a runnable Mastra contrast slice only if one of these becomes true:

- T004 scoring cannot distinguish the Python candidates without cross-language evidence.
- The selected product baseline requires TypeScript-native app integration, web-framework deployment, or Mastra Studio
  features as a core product need.
- Pydantic AI and LangGraph both fail the platform decision on Python-specific evidence and the roadmap needs a fresh
  candidate before selection.
- A future goal explicitly asks for a TypeScript contrast implementation after the primary Python product lane is
  selected.

## Follow-Up Work

No new Beads ticket is required for T002. Existing Goal 004 tasks already cover the next steps:

- T003 normalizes candidate evidence in `docs/requirements-matrix.md`.
- T004 scores candidates.
- T005 through T007 record and review the platform decision.
- T011 and T012 freeze/archive non-selected lanes and capture migration notes after the decision.

## Presenter Conclusion

T002 is complete when this decision is accepted by an independent reviewer and the normal workflow acceptance checks
pass. The decision is to defer Mastra implementation before platform selection, not to delete the lane or declare it
irrelevant.

## Independent Reviewer Acceptance

Reviewer agent id: `codex-independent-reviewer-goal004-t002`

Review agent path: `019e8809-88ad-7d91-a6a3-8ddb33667d21`

Outcome: `accepted`

Evidence checked:

- `.agent-runs/reports/goal-004-t002-mastra-contrast-decision-20260602.md`
- `specs/005-candidate-platform-decision-product-baseline/spec.md`
- `specs/005-candidate-platform-decision-product-baseline/tasks.md`
- `specs/005-candidate-platform-decision-product-baseline/plan.md`
- `docs/comparison-evidence.md`
- `.agent-runs/reports/goal-004-t001-candidate-evidence-audit-20260602.md`
- `apps/mastra-ts/README.md`
- `docs/requirements-matrix.md`

Reviewer findings:

- No blocking findings.
- No non-blocking findings.
- The T002 decision satisfies FR-003 by explicitly deferring a runnable Mastra contrast slice before selection with an
  evidence-based rationale.
- Repo evidence supports the decision because Mastra is missing runnable app, package manifest, fixture, trace export,
  eval artifact, and durable runtime proof.
- The report and plan preserve the boundary that Mastra must not be scored as implementation-proven in T003 or T004.
- The decision does not select the final platform.
- The reopen path is specific and reasonable.
- Deterministic validation remains independent from hosted or cloud services.

Required follow-up tickets:

- None for T002 acceptance.
- Continue existing Goal 004 tasks T003, T004, T005, T006, and T007 for matrix normalization, scoring, platform
  decision, and independent decision review.
