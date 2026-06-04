# Review Actions

Status: added for Goal 006 T008.

`uv run awf review-action` records durable review-gate actions as repo-local JSON artifacts under
`.agent-runs/review-actions/`. The action surface supports the four operator verbs required by the workbench contract:
`approve`, `request-changes`, `defer`, and `ask-question`.

## Command

```bash
uv run awf review-action \
  --action approve \
  --target-kind ticket \
  --target-id awf-example \
  --reviewer-id reviewer-agent-id \
  --evidence .agent-runs/reports/example.md \
  --note "Accepted after checking the cited evidence." \
  --write \
  --json
```

Omit `--write` to preview the action without mutating the repo.

## Artifact

Each written action uses schema `awf.operator-workbench.review-action.v1` and includes:

- action id and recorded timestamp
- action: `approve`, `request-changes`, `defer`, or `ask-question`
- target kind and target id
- reviewer id and role
- source artifact paths
- note text
- whether a response is expected
- explicit `human_required.required=false`
- `decision_record_deferred_to=Goal 006 T009 reviewer decision records`

## Boundaries

- Review actions are durable operator inputs, not final reviewer decision records.
- T009 owns verdict fields, evidence-checked detail, findings, and follow-up routing.
- T008 actions are visible through `review-gate` and `operator-status` but do not block deterministic validation.
- Human review remains required only for user-reserved, missing, or contradictory decisions.
- The action command is credential-free and does not require GitHub, hosted Logfire, hosted Langfuse, or external tokens.
