# Branch And PR Status

Status: added for Goal 006 T010.

`uv run awf branch-pr-status` reports the current Git branch, commit, upstream relationship, working tree state, and
GitHub PR metadata when available. If GitHub access is unavailable, the command returns an explicit repo-local fallback
instead of failing deterministic validation.

## Command

```bash
uv run awf branch-pr-status --json
uv run awf branch-pr-status --write --json
uv run awf branch-pr-status --skip-github --json
```

Use `--skip-github` for deterministic fixture or offline runs. Use `--write` to persist a repo-local artifact under
`.agent-runs/reports/workbench/`.

## Artifact

Each generated status uses schema `awf.operator-workbench.branch-pr.v1` and includes:

- branch name and short commit
- working tree clean state and compact Git status
- origin remote, upstream branch, and ahead/behind counts
- PR URL, number, draft state, PR state, review decision, and merge state when `gh pr view` is available
- GitHub availability state: `available`, `unavailable`, or `not_checked`
- repo-local fallback text that names what can still be trusted without GitHub
- self-hosted flags showing no external service is required for deterministic validation

## Boundaries

- GitHub integration is optional enrichment, not a validation dependency.
- When `gh` is missing, unauthenticated, offline, or has no PR for the branch, status remains useful through the
  repo-local fallback.
- T011 owns self-hosted Langfuse trace and eval deep links.
- The branch/PR command is credential-free when `--skip-github` is used and does not require hosted Logfire,
  hosted Langfuse, or external project tokens.
