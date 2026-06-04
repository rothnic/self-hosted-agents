# Workbench Status Artifact Schema

Status: defined for Goal 006 T003.

The workbench status artifact is the stable generated output that later CLI/static reports or local UI surfaces consume.
It summarizes repo state without replacing the source artifacts. All paths are repo-relative unless a field explicitly
names a self-hosted URL.

## Artifact Versions

- `awf.operator-workbench.status.v1`: generated status surface for the project owner, scheduled agents, and local
  sessions.
- `awf.operator-workbench.decision-summary.v1`: generated review decision summary linked from the status artifact.

## Status Artifact

Required top-level fields:

- `schema`: literal `awf.operator-workbench.status.v1`.
- `generated_at`: ISO-8601 timestamp.
- `generated_by`: command, role, or agent id that generated the artifact.
- `generated_from`: source commands and repo artifacts used to build the status.
- `scope`: objective id, active goal, spec id, phase, branch, PR, and optional Beads issue id.
- `availability`: explicit `available`, `unavailable`, or `not_checked` state for GitHub, self-hosted Langfuse, DBOS,
  and local repo evidence.
- `executive_snapshot`: current phase, active role, recommendation, reason, next owner, and risks.
- `roadmap`: ordered goals, accepted evidence, current goal, next child goal, and follow-up epics.
- `goal_dashboard`: ordered child goals with accepted evidence links, current phase, next ticket, and follow-up epics.
- `increment_dashboard`: scoped increment tickets, claims, blockers, active workers, stale claims, and validation state.
- `work_queue`: ready work, blocked work, human-required work, active claims, stale claims, and Beads source metadata.
- `evidence_map`: presenter reports, reviewer reports, verification artifacts, trace artifacts, eval artifacts, Beads
  comments, and PR evidence.
- `review_gate`: current verdict, reviewer id, evidence checked, findings, follow-up tickets, and escalation state.
- `trace_eval`: repo-local trace/eval links, optional self-hosted Langfuse links, and unavailable-service gaps.
- `branch_pr`: branch, commit, PR URL, draft or ready state, and GitHub fallback.
- `handoff`: copy-ready next role or ticket, required files, validation commands, risks, and exact artifact handles.
- `health`: latest health, repo-hygiene, workflow-state, review-gate, and acceptance summaries.
- `decision_summaries`: repo-relative paths to decision summary artifacts.

Minimal shape:

```json
{
  "schema": "awf.operator-workbench.status.v1",
  "generated_at": "2026-06-04T00:00:00Z",
  "generated_by": "uv run awf operator-status --write --json",
  "generated_from": {
    "commands": [
      "uv run awf next-action --json",
      "uv run awf context-index --json",
      "uv run awf ready-work --json",
      "uv run awf review-gate --json"
    ],
    "artifacts": [
      "docs/goals/000-self-hosted-agent-system-roadmap.md",
      ".beads/issues.jsonl",
      ".agent-runs/claims/",
      ".agent-runs/reports/"
    ]
  },
  "scope": {
    "objective_id": "agentic-development-foundation",
    "goal": "006-operator-workbench-review-ux",
    "spec_id": "007-operator-workbench-review-ux",
    "phase": "Goal 006",
    "branch": "codex/pydantic-ai-fixture-scaffold",
    "pr_url": "https://github.com/rothnic/self-hosted-agents/pull/12",
    "beads_issue_id": "awf-vht"
  },
  "availability": {
    "github": {"state": "available", "fallback": "git status and PR body"},
    "self_hosted_langfuse": {"state": "unavailable", "fallback": "repo-local trace artifacts"},
    "dbos": {"state": "available", "fallback": "repo-local durable smoke evidence"},
    "repo_local_evidence": {"state": "available", "fallback": null}
  },
  "executive_snapshot": {
    "current_phase": "implementation",
    "active_role": "implementer",
    "recommendation": "claim ready Beads work",
    "reason": "one unblocked worker ticket is ready",
    "next_owner": "implementer",
    "risks": []
  },
  "roadmap": {
    "current_goal": "006-operator-workbench-review-ux",
    "next_goal": null,
    "accepted_evidence": [".agent-runs/reports/goal-006/t002-bdd-contract-20260604.md"],
    "follow_up_epics": ["awf-eas", "awf-lkr"]
  },
  "goal_dashboard": {
    "schema": "awf.operator-workbench.goal-dashboard.v1",
    "source": "docs/goals/000-self-hosted-agent-system-roadmap.md",
    "current_goal_id": "006",
    "current_phase": {
      "phase": "Goal 006 Phase 2: Repo-Backed Status Surfaces",
      "completed_task_count": 4,
      "open_task_count": 13,
      "next_task": {"id": "T005", "title": "Add a long-horizon goal dashboard"}
    },
    "next_ticket": "awf-sdh",
    "goals": [],
    "accepted_evidence_links": [],
    "follow_up_epics": []
  },
  "increment_dashboard": {
    "schema": "awf.operator-workbench.increment-dashboard.v1",
    "source": ".agent-runs/increments/007-operator-workbench-review-ux-goal-006.json",
    "increment_id": "007-operator-workbench-review-ux-goal-006",
    "spec_id": "007-operator-workbench-review-ux",
    "phase": "Goal 006",
    "review_status": "executing",
    "next_action": "orchestrator-loop should keep assigning unblocked work while pm-review-loop triages blockers",
    "counts": {
      "total_tickets": 17,
      "completed_tickets": 5,
      "open_tickets": 12,
      "ready_tickets": 1,
      "blocked_tickets": 11,
      "active_claims": 1,
      "active_workers": 1,
      "stale_claims": 0,
      "validation_checks": 3
    },
    "tickets": [],
    "ready_tickets": [],
    "blocked_tickets": [],
    "active_claims": [],
    "active_workers": [],
    "stale_claims": [],
    "validation_state": {"ok": true, "credential_free": true},
    "handoff": {"active_ticket": "awf-vty", "resume_claim": ".agent-runs/claims/awf-vty.json"},
    "self_hosted": {"external_service_required": false}
  },
  "work_queue": {
    "source": "beads",
    "ready": [{"id": "awf-vht", "title": "Define the generated artifact schema"}],
    "blocked": [],
    "human_required": [],
    "active_claims": [".agent-runs/claims/awf-vht.json"],
    "stale_claims": []
  },
  "evidence_map": {
    "presenter_reports": [".agent-runs/reports/goal-006/t002-bdd-contract-20260604.md"],
    "reviewer_reports": [],
    "verification_artifacts": [],
    "trace_artifacts": [],
    "eval_artifacts": [],
    "beads_comments": [{"issue_id": "awf-288", "comment_id": 133}],
    "pr_evidence": ["https://github.com/rothnic/self-hosted-agents/pull/12"]
  },
  "review_gate": {
    "state": "accepted",
    "reviewer_id": "019e9175-86d4-72b3-98f1-af27e927b050",
    "evidence_checked": ["tests/workflow/features/operator_workbench_review_ux.feature"],
    "findings": [],
    "follow_up_tickets": [],
    "human_required": false
  },
  "trace_eval": {
    "repo_local_trace_links": [],
    "repo_local_eval_links": [],
    "self_hosted_langfuse_links": [],
    "gaps": ["self-hosted Langfuse not checked for this fixture-only schema slice"]
  },
  "branch_pr": {
    "branch": "codex/pydantic-ai-fixture-scaffold",
    "commit": "bf0db3d",
    "pr_url": "https://github.com/rothnic/self-hosted-agents/pull/12",
    "state": "draft",
    "github_fallback": "git status plus PR body"
  },
  "handoff": {
    "next_role": "implementer",
    "next_ticket": "awf-vht",
    "required_files": ["docs/workbench/status-artifact-schema.md"],
    "validation_commands": ["uv run awf workflow-fixture-test"],
    "risks": [],
    "artifact_handles": [".agent-runs/claims/awf-vht.json"]
  },
  "health": {
    "repo_hygiene": "passed",
    "workflow_state_lint": "passed",
    "review_gate": "passed",
    "acceptance": "passed"
  },
  "decision_summaries": [".agent-runs/reviews/example-decision-summary.json"]
}
```

## Decision Summary Artifact

Required top-level fields:

- `schema`: literal `awf.operator-workbench.decision-summary.v1`.
- `decision_id`: stable id for this decision.
- `recorded_at`: ISO-8601 timestamp.
- `target`: goal, increment, ticket, branch, PR, or artifact being reviewed.
- `reviewer`: reviewer agent id and role.
- `outcome`: one of `accepted`, `rejected`, `deferred`, `question`, or `human-required`.
- `evidence_checked`: artifact paths, command summaries, trace/eval links, and PR links inspected by the reviewer.
- `findings`: ordered findings with severity, summary, and required action.
- `follow_up_tickets`: Beads ids or proposed tickets required after the decision.
- `human_required`: boolean plus reason when true.
- `source_artifacts`: presenter evidence and validation artifacts that justify the decision.

Minimal shape:

```json
{
  "schema": "awf.operator-workbench.decision-summary.v1",
  "decision_id": "goal-006-t003-review-20260604",
  "recorded_at": "2026-06-04T00:00:00Z",
  "target": {
    "kind": "ticket",
    "id": "awf-vht",
    "spec_id": "007-operator-workbench-review-ux",
    "task_id": "T003"
  },
  "reviewer": {
    "agent_id": "019e0000-0000-0000-0000-000000000000",
    "role": "reviewer"
  },
  "outcome": "accepted",
  "evidence_checked": [
    "docs/workbench/status-artifact-schema.md",
    "uv run awf workflow-fixture-test"
  ],
  "findings": [],
  "follow_up_tickets": [],
  "human_required": {
    "required": false,
    "reason": null
  },
  "source_artifacts": [
    ".agent-runs/reports/goal-006/t003-status-schema-20260604.md"
  ]
}
```

## Validation Rules

- Status artifacts must be generated from repo commands and source artifacts, not prior chat context.
- Every linked artifact must be repo-relative or an explicit self-hosted URL.
- Optional GitHub and self-hosted Langfuse data must use availability state and fallback fields instead of failing
  deterministic validation.
- `work_queue.source` must remain `beads` when Beads is available.
- `human_required.required` may be true only for user-reserved, missing, or contradictory decisions.
- Decision summaries must be reviewer-attributed and must name evidence checked before an outcome is accepted.
- Handoff data must include exact next role or ticket, validation commands, risks, and artifact handles.
