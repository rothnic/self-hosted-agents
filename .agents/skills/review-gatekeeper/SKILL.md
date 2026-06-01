---
name: review-gatekeeper
description: Use when automation must pause for review evidence or resume after a review outcome is recorded.
---

# Review Gatekeeper

## Purpose

Make ambiguity explicit and resumable.

## Workflow

1. Run `uv run awf review-gate`.
2. If blocked only by goal or increment evidence review, send the evidence to an independent reviewer agent instead of
   stopping for a human decision.
3. If resuming, verify the decision is recorded in the relevant spec, ADR, ticket, or run report.
4. Do not infer approval from silence; require a durable reviewer acceptance or rejection.
5. When verified changes are waiting to merge, present explicit human options: approve and merge, request changes, or
   keep iterating. Do not merge without explicit approval.

## Human Reviewer Lane

The human reviewer owns project objectives, explicitly reserved decisions, priority tradeoffs, and merge decisions.
Agents own gathering evidence, presenting it, and obtaining independent reviewer acceptance for goal and increment
evidence.
Use the `AGENTS.md` next-action response template for review handoffs so the human can see process position, git status,
work in progress, dependencies, recommendation, available options, meta-process notes, and what will happen after
approval.
Do not ask the human reviewer to operate workflow commands manually. Agents should run the checks, summarize evidence,
and use an independent reviewer agent for goal evidence acceptance unless the user explicitly reserves the decision.
After a review decision is recorded and the repo is clean, recommend starting a new session for the next planning or
implementation phase. Include the latest commit, objective/spec, remaining Beads work, and recommended next role.

## Gate Reasons

- Scope unclear
- Priority unclear
- Architecture decision required
- Acceptance criteria missing
- Behavior contract ambiguous
- Product intent unclear
