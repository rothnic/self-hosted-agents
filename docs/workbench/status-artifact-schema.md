# Workbench Status Artifact Schema

Status: defined for Goal 006 T003.

The workbench status artifact is the stable generated output that later CLI/static reports or local UI surfaces consume.
It summarizes repo state without replacing the source artifacts. All paths are repo-relative unless a field explicitly
names a self-hosted URL.

## Artifact Versions

- `awf.operator-workbench.status.v1`: generated status surface for the project owner, scheduled agents, and local
  sessions.
- `awf.operator-workbench.decision-summary.v1`: repo-local reviewer decision summary linked from the status artifact.
- `awf.operator-workbench.review-action.v1`: repo-local review-gate action input linked from the status artifact.
- `awf.operator-workbench.branch-pr.v1`: repo-local branch and optional GitHub PR status linked from the status
  artifact.
- `awf.operator-workbench.trace-eval-links.v1`: repo-local trace/eval links plus optional self-hosted Langfuse deep
  links.

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
- `evidence_view`: evidence links grouped by presenter/reviewer reports, runs, traces, evals, Beads comments, branch,
  and PR fallback.
- `evidence_map`: presenter reports, reviewer reports, verification artifacts, trace artifacts, eval artifacts, Beads
  comments, and PR evidence.
- `review_gate`: current verdict, reviewer id, evidence checked, findings, follow-up tickets, decision records, and
  escalation state.
- `review_actions`: recent durable review-action artifacts and supported review-gate actions.
- `trace_eval`: repo-local trace/eval links, trace/eval correlations, optional self-hosted Langfuse links, availability,
  and unavailable-service gaps.
- `branch_pr`: branch, commit, upstream, ahead/behind counts, PR URL, draft or ready state, GitHub availability, and
  repo-local fallback.
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
  "evidence_view": {
    "schema": "awf.operator-workbench.evidence-view.v1",
    "source": "repo-local artifacts and Beads comments",
    "target": {
      "goal": "006-operator-workbench-review-ux",
      "spec_id": "007-operator-workbench-review-ux",
      "ticket_id": "awf-yu8"
    },
    "presenter_reports": [],
    "reviewer_reports": [],
    "run_artifacts": [],
    "trace_artifacts": [],
    "eval_artifacts": [],
    "beads_comments": [],
    "branch_pr": {
      "branch": "codex/pydantic-ai-fixture-scaffold",
      "commit": "5c099ff",
      "pr_url": null,
      "state": "not_checked",
      "fallback": "repo-local branch and commit; GitHub PR lookup is deferred to T010"
    },
    "acceptance_state": {
      "presenter_report_count": 0,
      "reviewer_report_count": 0,
      "accepted_report_count": 0,
      "verification_artifact_count": 0,
      "trace_artifact_count": 0,
      "eval_artifact_count": 0,
      "beads_issue_with_comments_count": 0
    },
    "self_hosted": {"credential_free": true, "external_service_required": false}
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
    "human_required": false,
    "supported_actions": ["approve", "ask-question", "defer", "request-changes"],
    "actions": []
  },
  "review_actions": [],
  "trace_eval": {
    "schema": "awf.operator-workbench.trace-eval-links.v1",
    "repo_local_trace_links": [
      {
        "path": ".agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json",
        "kind": "trace",
        "provider": "Pydantic AI",
        "run_id": "pydantic-ai-langfuse-run-20260531",
        "trace_id": "pydantic-ai-langfuse-run-20260531",
        "otel_trace_id": "735c1665d723b965ef77950eeeac36df",
        "repo_local_url": ".agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json",
        "langfuse": {
          "state": "available",
          "trace_url": "http://127.0.0.1:13300/project/self-hosted-agents-pydantic-ai/traces/735c1665d723b965ef77950eeeac36df",
          "fallback": null
        }
      }
    ],
    "repo_local_eval_links": [
      {
        "path": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json",
        "kind": "evaluation",
        "provider": "Pydantic Evals",
        "evaluation_id": "pydantic-ai-evals-run-20260531",
        "run_id": "pydantic-ai-evals-run-20260531",
        "trace_evidence": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json",
        "repo_local_url": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json"
      }
    ],
    "self_hosted_langfuse_links": [
      {
        "trace_path": ".agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json",
        "otel_trace_id": "735c1665d723b965ef77950eeeac36df",
        "url": "http://127.0.0.1:13300/project/self-hosted-agents-pydantic-ai/traces/735c1665d723b965ef77950eeeac36df",
        "verified": true,
        "status": "verified"
      }
    ],
    "correlations": [
      {
        "evaluation_path": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json",
        "trace_path": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json",
        "correlated": true,
        "match_method": "trace_evidence",
        "langfuse_trace_url": null
      }
    ],
    "availability": {
      "self_hosted_langfuse": {"state": "available", "fallback": "repo-local trace artifacts"},
      "repo_local_evidence": {"state": "available", "fallback": null}
    },
    "gaps": [],
    "self_hosted": {"credential_free": true, "external_service_required": false}
  },
  "branch_pr": {
    "branch": "codex/pydantic-ai-fixture-scaffold",
    "commit": "bf0db3d",
    "pr_url": "https://github.com/rothnic/self-hosted-agents/pull/12",
    "state": "draft",
    "github": {"state": "available", "checked": true},
    "github_fallback": "GitHub PR status available through gh"
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
  "decision_summaries": [".agent-runs/review-decisions/example-decision-summary.json"]
}
```

## Trace And Eval Links Artifact

The trace/eval links artifact is generated by `uv run awf trace-eval-links`. It gives operators a compact path from
status surfaces to repo-local trace evidence, repo-local eval evidence, correlations between those artifacts, and
optional self-hosted Langfuse deep links captured inside existing trace artifacts.

The command is credential-free. It reads recent repo-local evidence files only; it does not call hosted Logfire, hosted
Langfuse, GitHub, or any external service. If no self-hosted Langfuse URL is present, the artifact records an
unavailable state and keeps repo-local trace links authoritative.

Required top-level fields:

- `schema`: literal `awf.operator-workbench.trace-eval-links.v1`.
- `generated_at`: ISO-8601 timestamp.
- `generated_by`: command that generated the artifact.
- `repo_local_trace_links`: repo-local trace artifacts with run ids, trace ids, OTel ids, span counts, and Langfuse
  metadata when present.
- `repo_local_eval_links`: repo-local eval artifacts with evaluation ids, scores, trace-evidence links, and rerun
  commands when present.
- `self_hosted_langfuse_links`: self-hosted Langfuse trace URLs found in trace artifacts; empty when unavailable.
- `correlations`: eval-to-trace matches by run id, trace id, or explicit trace evidence path.
- `availability`: explicit states for `self_hosted_langfuse` and `repo_local_evidence`.
- `gaps`: unavailable-service or missing-link notes.
- `self_hosted`: credential-free and external-service-required flags.
- `path`: repo-relative artifact path when generated with `--write`.

Minimal shape:

```json
{
  "schema": "awf.operator-workbench.trace-eval-links.v1",
  "generated_at": "2026-06-04T00:00:00Z",
  "generated_by": "uv run awf trace-eval-links --json",
  "repo_local_trace_links": [
    {
      "path": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json",
      "kind": "trace",
      "provider": "Pydantic AI",
      "format": "OpenTelemetry JSON",
      "run_id": "pydantic-ai-evals-run-20260531",
      "trace_id": "pydantic-ai-evals-run-20260531",
      "otel_trace_id": "564f9c96c05a4500b9908c0a9144a1b2",
      "span_count": 5,
      "repo_local_url": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json",
      "langfuse": {
        "state": "unavailable",
        "trace_url": null,
        "fallback": "repo-local trace artifact"
      },
      "gaps": []
    }
  ],
  "repo_local_eval_links": [
    {
      "path": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json",
      "kind": "evaluation",
      "provider": "Pydantic Evals",
      "evaluation_id": "pydantic-ai-evals-run-20260531",
      "run_id": "pydantic-ai-evals-run-20260531",
      "passed": true,
      "score": 6,
      "max_score": 6,
      "repo_local_url": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json",
      "trace_evidence": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json",
      "rerun_command": "uv run awf pydantic-ai-evals --write"
    }
  ],
  "self_hosted_langfuse_links": [
    {
      "trace_path": ".agent-runs/verifications/pydantic-ai-langfuse-run-20260531.trace.json",
      "otel_trace_id": "735c1665d723b965ef77950eeeac36df",
      "url": "http://127.0.0.1:13300/project/self-hosted-agents-pydantic-ai/traces/735c1665d723b965ef77950eeeac36df",
      "verified": true,
      "status": "verified"
    }
  ],
  "correlations": [
    {
      "evaluation_path": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.evaluation.json",
      "trace_path": ".agent-runs/verifications/pydantic-ai-evals-run-20260531.trace.json",
      "run_id": "pydantic-ai-evals-run-20260531",
      "trace_id": "pydantic-ai-evals-run-20260531",
      "evaluation_id": "pydantic-ai-evals-run-20260531",
      "correlated": true,
      "match_method": "trace_evidence",
      "langfuse_trace_url": null
    }
  ],
  "availability": {
    "self_hosted_langfuse": {"state": "available", "fallback": "repo-local trace artifacts"},
    "repo_local_evidence": {"state": "available", "fallback": null}
  },
  "gaps": [],
  "self_hosted": {
    "credential_free": true,
    "external_service_required": false
  },
  "path": ".agent-runs/reports/workbench/trace-eval-links-20260604T000000Z.json"
}
```

## Branch And PR Artifact

Required top-level fields:

- `schema`: literal `awf.operator-workbench.branch-pr.v1`.
- `generated_at`: ISO-8601 timestamp.
- `branch`: current Git branch.
- `commit`: current short commit.
- `clean`: whether the working tree is clean.
- `remote`: origin remote URL when configured.
- `upstream`: upstream branch when configured.
- `ahead_by` and `behind_by`: upstream comparison counts.
- `state`: `available` when GitHub PR metadata is available, otherwise `repo-local-fallback`.
- `pr_url`, `pr_number`, `pr_state`, `is_draft`, `review_decision`, and `merge_state_status`: GitHub PR fields when
  `gh pr view` succeeds.
- `github`: availability state, checked flag, reason, and tool.
- `fallback`: repo-local fallback summary.
- `self_hosted`: credential-free and external-service-required flags.

Minimal fallback shape:

```json
{
  "schema": "awf.operator-workbench.branch-pr.v1",
  "generated_at": "2026-06-04T00:00:00Z",
  "branch": "codex/pydantic-ai-fixture-scaffold",
  "commit": "5f8ebf5",
  "clean": true,
  "remote": "https://github.com/rothnic/self-hosted-agents.git",
  "upstream": "origin/codex/pydantic-ai-fixture-scaffold",
  "ahead_by": 0,
  "behind_by": 0,
  "state": "repo-local-fallback",
  "pr_url": null,
  "github": {
    "state": "unavailable",
    "checked": true,
    "reason": "gh pr view failed",
    "tool": "gh"
  },
  "fallback": "repo-local branch, commit, upstream, ahead/behind, and working tree status",
  "self_hosted": {
    "credential_free": true,
    "external_service_required": false,
    "fallback_required": true
  }
}
```

## Review Action Artifact

Required top-level fields:

- `schema`: literal `awf.operator-workbench.review-action.v1`.
- `action_id`: stable id for the action artifact.
- `recorded_at`: ISO-8601 timestamp.
- `action`: one of `approve`, `request-changes`, `defer`, or `ask-question`.
- `state`: action recording state.
- `target`: target kind and id.
- `reviewer`: reviewer agent id and role.
- `source_artifacts`: evidence paths cited by the reviewer.
- `note`: short note, question, or requested-change summary.
- `requires_response`: true for request changes, defer, and ask question actions.
- `human_required`: boolean plus reason; deterministic action capture defaults to false.
- `decision_record_deferred_to`: pointer to T009 decision records.

Minimal shape:

```json
{
  "schema": "awf.operator-workbench.review-action.v1",
  "action_id": "review-action-approve-awf-example-20260604T000000Z",
  "recorded_at": "2026-06-04T00:00:00Z",
  "action": "approve",
  "state": "recorded",
  "target": {"kind": "ticket", "id": "awf-example"},
  "reviewer": {"agent_id": "019e0000-0000-0000-0000-000000000000", "role": "reviewer"},
  "source_artifacts": [".agent-runs/reports/example.md"],
  "note": "Accepted after checking the cited evidence.",
  "requires_response": false,
  "human_required": {"required": false, "reason": null},
  "decision_record_deferred_to": "Goal 006 T009 reviewer decision records"
}
```

## Decision Summary Artifact

Required top-level fields:

- `schema`: literal `awf.operator-workbench.decision-summary.v1`.
- `decision_id`: stable id for this decision.
- `recorded_at`: ISO-8601 timestamp.
- `target`: goal, increment, ticket, branch, PR, or artifact being reviewed.
- `reviewer`: reviewer agent id and role.
- `verdict`: one of `accepted`, `rejected`, `deferred`, `question`, or `human-required`.
- `outcome`: one of `accepted`, `rejected`, `deferred`, `question`, or `human-required`.
- `evidence_checked`: artifact paths, command summaries, trace/eval links, and PR links inspected by the reviewer.
- `findings`: ordered findings with severity, summary, and required action.
- `follow_up_tickets`: Beads ids or proposed tickets required after the decision.
- `follow_up_routing`: whether follow-up work is required, linked tickets, and the next owner.
- `human_required`: boolean plus reason when true.
- `source_artifacts`: presenter evidence and validation artifacts that justify the decision.
- `self_hosted`: credential-free and external-service-required flags.

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
  "verdict": "accepted",
  "outcome": "accepted",
  "evidence_checked": [
    "docs/workbench/status-artifact-schema.md",
    "uv run awf workflow-fixture-test"
  ],
  "findings": [],
  "follow_up_tickets": [],
  "follow_up_routing": {
    "required": false,
    "tickets": [],
    "next_owner": null
  },
  "human_required": {
    "required": false,
    "reason": null
  },
  "source_artifacts": [
    ".agent-runs/reports/goal-006/t003-status-schema-20260604.md"
  ],
  "self_hosted": {
    "credential_free": true,
    "external_service_required": false
  }
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
