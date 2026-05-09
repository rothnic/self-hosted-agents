---
name: spec-author
description: Use when creating or updating Spec Kit feature specs that describe intent, requirements, design, acceptance, and task mapping without becoming a single giant document.
---

# Spec Author

## Purpose

Maintain small, linked Spec Kit feature artifacts that can drive tickets and BDD contracts.

## Inputs

- `.specify/templates/`
- `.specify/scripts/bash/`
- Spec Kit skills: `speckit-specify`, `speckit-plan`, `speckit-tasks`, `speckit-clarify`, `speckit-analyze`
- Current objective
- Research notes, ADRs, and planning reports
- Existing BDD contracts when behavior changes

## Workflow

1. Use Spec Kit tooling/skills for feature artifacts; do not hand-create alternate spec formats.
2. Keep generated feature work under `specs/<number>-<short-name>/`.
3. Use native Spec Kit files: `spec.md`, `plan.md`, `tasks.md`, plus optional `research.md`, `data-model.md`, `contracts/`, and `checklists/`.
4. Put durable decisions in ADRs, not feature specs.
5. Put evidence and source-heavy notes in `docs/research/`.
6. Run `uv run awf spec-kit-lint` and `uv run awf spec-lint`.

## Stop Conditions

- The goal or non-goals are unclear.
- Acceptance cannot be tested.
- The change needs a new architecture decision.
- A non-Spec-Kit spec format appears under `specs/`.
