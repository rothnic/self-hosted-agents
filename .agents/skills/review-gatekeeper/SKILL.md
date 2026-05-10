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
5. When verified changes are waiting to merge, present explicit human options: approve and merge, request changes, or
   keep iterating. Do not merge without explicit approval.

## Human Reviewer Lane

The human reviewer owns approvals, priority tradeoffs, and merge decisions. Agents own gathering evidence and presenting
the decision in a compact form.
Use the `AGENTS.md` next-action response template for review handoffs so the human can see process position, git status,
work in progress, dependencies, recommendation, available options, meta-process notes, and what will happen after
approval.

## Gate Reasons

- Scope unclear
- Priority unclear
- Architecture decision required
- Acceptance criteria missing
- Behavior contract ambiguous
- Product intent unclear
