# Frozen Non-Selected Candidate References

Status: defined for Goal 004 T011
Selected product baseline: Pydantic AI plus Langfuse and DBOS
Decision record: `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md`
Migration notes: `docs/candidate-references/non-selected-candidate-migration-notes.md`
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

Freeze the non-selected candidate lanes as comparison references so product work can deepen the selected Pydantic AI
baseline without losing implementation lessons or reopening the platform decision by default.

This is a freeze, not deletion. The candidate apps stay in place because their docs, fixtures, and gaps still explain
why the selected stack won the current evidence-backed decision.

## Freeze Policy

Non-selected candidate lanes are not product implementation lanes for Goal 004 or follow-on product-baseline work.

Allowed changes:

- keep deterministic fixture checks passing when shared contracts or tooling change;
- update docs when accepted evidence changes their status;
- reuse ideas or fixtures through an explicit migration task;
- reopen a candidate through a future Beads ticket or ADR when a product requirement justifies it.

Disallowed changes:

- add new product features to a non-selected lane by default;
- score deferred or partial evidence as implementation-proven;
- require hosted services to validate a frozen reference;
- delete evidence, fixtures, or docs needed to understand the platform decision;
- move reusable assets into the selected product baseline without T012 migration notes.

## Candidate References

### LangGraph Python Plus Langfuse

Disposition: frozen comparison reference.

Keep in repo because it has a runnable deterministic fixture, local trace/eval artifacts, and useful Python
orchestration lessons.

Do not deepen by default because it lacks durable execution proof, committed full verification parity, self-hosted
Langfuse product-depth evidence, and selected-stack review acceptance.

Reopen only when a future requirement needs LangGraph-specific graph or checkpoint semantics, or when the selected
Pydantic AI baseline fails a product requirement.

### Mastra TypeScript Plus Shared Contracts

Disposition: frozen deferred contrast reference.

Keep in repo because it preserves the TypeScript-native question, expected evidence categories, and cross-language
tradeoff record.

Do not deepen by default because it has no runnable app, package manifest, fixture command, trace export, eval artifact,
setup proof, or durable runtime proof.

Reopen only when a future TypeScript product need appears or Python-first ownership becomes the wrong product
assumption.

### LangSmith Baseline

Disposition: external benchmark only.

Keep as a reference because it remains useful as a feature expectation baseline for LangChain/LangGraph-style
observability.

Do not deepen by default because hosted-only trace inspection does not satisfy the self-hosted assessment and
self-hosted access cannot be assumed.

Reopen only when a future budget or enterprise decision provides self-hosted-compatible access and a spec reopens the
benchmark.

## Reference Locations

- LangGraph Python: `apps/langgraph-python/`
- Mastra TypeScript: `apps/mastra-ts/`
- Platform decision: `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md`
- Requirements matrix: `docs/requirements-matrix.md`
- Comparison evidence checklist: `docs/comparison-evidence.md`
- Product baseline workflow: `docs/product-baseline/pydantic-ai-review-gated-work-order.md`
- Migration notes: `docs/candidate-references/non-selected-candidate-migration-notes.md`

## Tradeoffs

Freezing in place is preferred over physical archive movement for this checkpoint because:

- existing comparison commands and docs remain inspectable without path migrations;
- future reviewers can compare selected-stack claims against the earlier candidate evidence;
- the repo avoids a compatibility or path-migration task before product-baseline work is deeper;
- T012 can separately decide which fixtures, docs, or implementation ideas should migrate into shared or selected-stack
  locations.
  T012 records that posture in `docs/candidate-references/non-selected-candidate-migration-notes.md`.

The cost is that `apps/langgraph-python/` and `apps/mastra-ts/` remain visible beside the selected product lane. Agents
must use this reference policy, ADR 0005, and Beads ready-work state to avoid treating those directories as active
product lanes.

## Evidence Boundary

Goal 004 can treat the freeze as complete when:

- each non-selected lane has an explicit disposition and tradeoff;
- app READMEs point to this reference policy;
- roadmap/spec/goal surfaces say product work deepens the selected Pydantic AI baseline;
- deterministic fixture validation still passes without hosted credentials;
- migration of reusable assets remains assigned to T012 instead of being silently skipped.
