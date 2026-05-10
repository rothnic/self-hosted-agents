---
name: pm-steward
description: Use for PM-like planning across objectives, specs, tickets, tests, blockers, and learnings.
---

# PM Steward

## Purpose

Align the project without doing implementation work. Produce a concise planning report that identifies drift, blockers,
missing specs, stale tickets, missing behavior contracts, and the next safe action.

## Inputs

- `objectives/current.md`
- `uv run awf context-index`
- Active specs in `specs/`
- Open Beads tickets or ticket proposals
- Recent `.agent-runs/reports/` and `.agent-runs/learnings/`
- BDD contracts in `tests/workflow/features/`

## Workflow

1. Build a context index.
2. Compare current objectives with active specs, tasks, tickets, and checks.
3. Identify drift, missing acceptance criteria, unresolved human gates, and work that is too large.
4. Inspect Beads ready work and git status before telling the user what to do next.
5. Give the user 2-4 concrete next-step options, clearly mark the recommended one, and state who owns each option.
6. Recommend one of: approve/merge verified changes, update specs, decompose epic, create tickets, run review gate,
   implement one ready ticket, or stop for human input.
7. Write only a planning report unless explicitly asked to perform approved mutations.

## Next-Step Output Rules

- Always answer "what do I do now?" with options, not a single vague instruction.
- Use the `AGENTS.md` next-action response template so the message includes process position, git state, work in
  progress, context, recommendation, options, meta-process notes, and what happens after approval.
- If local changes are already verified, the human owns approval; the agent can prepare merge/commit/PR steps after approval.
- If Beads has ready work, the implementer owns execution after claiming one issue.
- If `tasks.md` has open work that is not in Beads, ticket planner owns backlog sync before implementers start.
- If a decision affects scope, priority, architecture, or acceptance, the human owns that decision.

## Stop Conditions

- Product intent is unclear.
- Acceptance criteria are missing.
- The next action would choose architecture or scope without human review.
- BDD contract expectations are ambiguous.

## References

- Load `references/planning-report.md` when writing a planning report.
