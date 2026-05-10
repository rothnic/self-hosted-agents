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
Do not ask the human reviewer to operate workflow commands manually. Agents should run the checks, summarize evidence,
and ask only for the approval, rejection, prioritization, or clarification decision that requires human judgment.
After a review decision is recorded and the repo is clean, recommend starting a new session for the next planning or
implementation phase. Include the latest commit, objective/spec, remaining Beads work, and recommended next role.

## Gate Reasons

- Scope unclear
- Priority unclear
- Architecture decision required
- Acceptance criteria missing
- Behavior contract ambiguous
- Product intent unclear
