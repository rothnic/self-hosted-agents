# Evidence View

Status: added for Goal 006 T007.

`uv run awf operator-status --json` includes an `evidence_view` section for the current Goal 006 ticket, increment, and
goal evidence. The view links durable proof surfaces without requiring hosted credentials or live GitHub access.

## Source Inputs

- `.agent-runs/reports/`
- `.agent-runs/verifications/`
- `.beads/issues.jsonl`
- `.agent-runs/claims/`
- `git branch --show-current`
- `git rev-parse --short HEAD`

## Included Fields

- `schema`: literal `awf.operator-workbench.evidence-view.v1`.
- `target`: current goal, spec, and active or next Beads ticket.
- `presenter_reports`: recent presenter evidence reports with acceptance classification.
- `reviewer_reports`: recent reviewer or review-bearing reports with acceptance classification.
- `run_artifacts`: recent verification and run artifacts.
- `trace_artifacts`: repo-local `*.trace.json` artifacts from `.agent-runs/`.
- `eval_artifacts`: repo-local `*.evaluation.json` artifacts from `.agent-runs/`.
- `beads_comments`: recent Beads issues with durable comments and latest comment handles.
- `branch_pr`: current branch and commit with explicit PR lookup fallback until T010 adds GitHub integration.
- `acceptance_state`: counts for report, verification, trace, eval, and Beads comment evidence.
- `self_hosted`: credential-free validation and external-service fallback declaration.

## Operating Rules

- Keep repo-local artifacts as the source of truth; hosted views are optional links, not validation requirements.
- Show PR evidence as branch and commit fallback until the GitHub integration ticket adds live PR status.
- Surface trace and eval artifacts from repo-local JSON files even when self-hosted Langfuse is unavailable.
- Preserve presenter evidence plus independent reviewer acceptance as the evidence model for goal and increment proof.
- Do not implement review actions, reviewer decision records, branch/PR API integration, or trace/eval deep-linking in
  this slice; those are T008 through T011.
