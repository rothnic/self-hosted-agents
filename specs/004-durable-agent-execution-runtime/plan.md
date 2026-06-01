# Implementation Plan: Durable Agent Execution Runtime

**Branch**: `004-durable-agent-execution-runtime` | **Date**: 2026-06-01 |
**Spec**: `specs/004-durable-agent-execution-runtime/spec.md`

## Summary

Deepen the selected Pydantic AI plus DBOS lane into a durable execution proof. The proof must stay deterministic and
self-hosted: local fixture runs prove retry, resume, review wait, side-effect idempotency, and evidence correlation
without hosted credentials or external model providers.

## Technical Context

**Language/Version**: Python 3.12 through `uv`.
**Primary Dependencies**: Pydantic AI, DBOS optional integration, local OpenTelemetry/Langfuse evidence fixtures.
**Storage**: Repo-local JSON artifacts, SQLite DBOS system database for smoke tests, Beads evidence, docs.
**Testing**: `uv run awf workflow-fixture-test`, `uv run awf verify --profile ticket --json`, focused app tests.
**Target Platform**: Local development first with a documented path to self-hosted services and production storage.
**Project Type**: Multi-app comparison repo with a Python candidate lane under `apps/pydantic-ai/`.
**Constraints**: No cloud dependency for acceptance. Human-style waits must be satisfied by durable reviewer evidence
from another agent unless the user explicitly reserves the decision.

## Constitution Check

- Repository artifacts are the source of truth: PASS.
- Review gates prevent drift: PASS; goal evidence uses presenter plus independent reviewer acceptance.
- Testable behavior comes before implementation: PASS; tasks start with contracts and fixture assertions.
- Small slices and traceable tickets: PASS through Spec Kit tasks and Beads.
- Alpha means no compatibility debt: PASS; the durable proof can change current fixture shapes directly.

## Project Structure

```text
apps/
└── pydantic-ai/
    └── durable DBOS smoke code and tests

docs/
├── requirements-matrix.md
├── adr/
└── research/

.agent-runs/
├── reports/
├── verifications/
└── increments/

specs/
└── 004-durable-agent-execution-runtime/
```

## Phased Plan

1. Lock the durable execution contract and self-hosted acceptance expectations.
2. Convert the existing DBOS smoke into a deeper proof for retry, resume, and side-effect idempotency.
3. Add a fixture-safe review wait that resumes only after independent reviewer acceptance exists.
4. Correlate durable run evidence with traces, evals, and Beads tickets.
5. Document local setup, storage, reset, recovery, and remaining production hardening gaps.
6. Update requirements scoring and promotion gates only after evidence is reproducible.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| DBOS-specific smoke path | The selected Pydantic AI lane exposes native DBOS integration | Generic OpenTelemetry-only proof would not test durable behavior |
| Reviewer acceptance fixture | Durable waits must model real review gates without stopping automation | A manual-only human gate would block the self-hosted agent loop |

## Open Questions

1. Which production storage topology should be selected after the local SQLite proof is complete?
2. How much worker scaling evidence is needed before the runtime can be considered production-ready?
3. Should later goals keep DBOS or compare Hatchet/Temporal again after operational requirements sharpen?
