# Operator View Catalog

Status: defined for Goal 006 T001.

This catalog defines the minimum views needed before implementing the operator workbench. It is intentionally
interface-neutral: each view can start as a CLI/static report and later feed a local UI if T013 accepts that interface
decision. The initial surface is repo-backed and credential-free.

## Research Inputs

The minimum view set comes from current repo operating evidence:

- `docs/goals/000-self-hosted-agent-system-roadmap.md` for ordered long-horizon goals and evidence policy.
- `docs/goals/006-operator-workbench-review-ux.md` for Goal 006 scope and proof commands.
- `specs/007-operator-workbench-review-ux/spec.md` for functional requirements and success criteria.
- `uv run awf next-action --json` for process position and recommended owner.
- `uv run awf context-index --json` for objectives, specs, tickets, blockers, and recent runs.
- `uv run awf ready-work --json` for Beads-ready work, blocked work, and human-required gates.
- `uv run awf increment-status --increment-id 007-operator-workbench-review-ux-goal-006 --spec-id
  007-operator-workbench-review-ux --phase "Goal 006" --json` for scoped increment state.
- `.agent-runs/reports/`, `.agent-runs/verifications/`, `.agent-runs/claims/`, and `.agent-runs/increments/` for
  durable evidence.
- `.beads/issues.jsonl` for executable backlog and comments.
- Git branch and PR state when GitHub access is available.

## Minimum Views

### Executive Snapshot

Question: Where are we, why does it matter, and who owns the next move?

Sources: `next-action`, `context-index`, current objective, and git status.

Output: Current phase, active role, recommended path, risks, and exact next owner.

### Roadmap And Goals

Question: Which long-horizon goal is active and what evidence is accepted?

Sources: `docs/goals/`, `.agent-runs/reports/`, and the PR body.

Output: Ordered goals, accepted reviewer evidence, active goal, and next child goal.

### Increment And Work Queue

Question: What worker task is ready, claimed, blocked, or stale?

Sources: `ready-work`, `increment-status`, `.beads/issues.jsonl`, and `.agent-runs/claims/`.

Output: Ready ticket, blocked tickets with blockers, active claims, stale claims, and worker handoff.

### Evidence Map

Question: What proof exists for the current ticket, increment, or goal?

Sources: `.agent-runs/reports/`, `.agent-runs/verifications/`, and Beads comments.

Output: Presenter report, reviewer report, validation commands, run artifacts, and acceptance state.

### Review Gate

Question: What decision is needed and has a reviewer accepted it?

Sources: `review-gate`, reviewer reports, and Beads comments.

Output: Verdict, reviewer id, evidence checked, findings, follow-up tickets, and escalation status.

### Trace And Eval

Question: Where are run, trace, eval, and durable execution artifacts?

Sources: Pydantic AI artifacts, Langfuse links, DBOS smoke evidence, and deployment smoke evidence.

Output: Repo-local trace/eval links, optional self-hosted Langfuse deep links, and missing-service fallback.

### Branch And PR

Question: What branch or PR contains the evidence?

Sources: git status/log, `gh pr view` when available, and the PR body.

Output: Branch, commit, PR URL, draft/ready state, and unavailable-GitHub fallback.

### Handoff

Question: What should the next agent do without reading prior chat?

Sources: status views, reports, claims, and latest validation.

Output: Copy-ready next ticket or role, required files, validation commands, and risks.

### Health And Operations

Question: Are workflow checks, services, and runbooks healthy enough to continue?

Sources: `health-status`, `repo-hygiene`, and deployment/operations docs.

Output: Health result, failed checks, service-backed gaps, and recovery or issue-log routing.

## View Priority

P1 views required before the first status command:

1. Executive Snapshot.
2. Roadmap And Goals.
3. Increment And Work Queue.
4. Evidence Map.
5. Review Gate.

P2 views required before Goal 006 acceptance:

1. Trace And Eval.
2. Branch And PR.
3. Handoff.
4. Health And Operations.

## Data Rules

- Every view must include repo-relative artifact links when evidence exists.
- Every generated status must say whether GitHub and self-hosted Langfuse links were available or unavailable.
- Missing optional services must appear as explicit fallback state, not as validation failure.
- Goal and increment evidence must use presenter evidence plus independent reviewer acceptance or rejection.
- Human-required state must come from durable review artifacts or explicit user-reserved decisions.
- Beads remains the executable backlog; the workbench must not route implementers from `tasks.md` when Beads is
  available.

## Decision States

The workbench should normalize review and routing decisions to these states:

| State | Meaning | Next Owner |
| --- | --- | --- |
| `planning` | No ready worker task exists or a spec/backlog action is needed | PM steward, spec author, epic decomposer, or ticket planner |
| `ready` | One or more Beads tasks are ready and unclaimed | Implementer |
| `claimed` | A worker has an active claim | Current worker or PM steward for stale claim triage |
| `blocked` | A required dependency, check, or reviewer finding prevents progress | PM steward, health-status, or ticket planner |
| `ready-for-review` | Presenter evidence exists and needs independent review | Reviewer |
| `accepted` | Independent reviewer accepted evidence | PM steward or next ordered role |
| `rejected` | Independent reviewer found blocking gaps | Implementer or planner for follow-up work |
| `human-required` | The user explicitly reserved a decision or evidence is contradictory | Human reviewer |

## Implementation Sequence

1. T002 defines BDD expectations for the views, review decisions, and handoffs.
2. T003 defines the generated artifact schema for status and decision summaries.
3. T004 builds the first consolidated operator status report.
4. T005 through T012 add focused goal, increment, evidence, review, trace/eval, branch/PR, and handoff coverage.
5. T013 decides whether CLI/static remains enough or a local UI is justified.
6. T014 through T016 implement the selected interface and scheduled-agent docs.
7. T017 presents final Goal 006 evidence for independent reviewer acceptance or rejection.

## Non-Goals For T001

- Do not add a local UI.
- Do not add review action commands.
- Do not query hosted services.
- Do not require GitHub credentials.
- Do not replace Beads, Spec Kit, `.agent-runs/`, or PR evidence as the source of truth.
