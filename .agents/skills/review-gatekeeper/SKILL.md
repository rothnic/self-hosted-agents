---
name: review-gatekeeper
description: Use when automation must pause for human review or resume after a human decision is recorded.
---

# Review Gatekeeper

## Purpose

Make ambiguity explicit and resumable.

## Workflow

1. Run `uv run awf review-gate`.
2. If blocked, summarize the decision needed and stop.
3. If resuming, verify the decision is recorded in the relevant spec, ADR, ticket, or run report.
4. Do not infer human approval from silence.

## Gate Reasons

- Scope unclear
- Priority unclear
- Architecture decision required
- Acceptance criteria missing
- Behavior contract ambiguous
- Product intent unclear
