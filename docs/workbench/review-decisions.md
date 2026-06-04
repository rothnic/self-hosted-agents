# Review Decisions

Status: added for Goal 006 T009.

`uv run awf review-decision` records final reviewer decisions as repo-local JSON artifacts under
`.agent-runs/review-decisions/`. Decision records sit above review actions: actions capture operator intent, while
decisions capture the reviewer verdict, evidence checked, findings, and follow-up routing.

## Command

```bash
uv run awf review-decision \
  --verdict accepted \
  --target-kind ticket \
  --target-id awf-example \
  --spec-id 007-operator-workbench-review-ux \
  --task-id T009 \
  --reviewer-id reviewer-agent-id \
  --evidence-checked "uv run awf workflow-fixture-test" \
  --source-artifact .agent-runs/reports/example.md \
  --note "Accepted after checking the cited evidence." \
  --write \
  --json
```

Omit `--write` to preview the decision without mutating the repo.

## Artifact

Each written decision uses schema `awf.operator-workbench.decision-summary.v1` and includes:

- decision id and recorded timestamp
- verdict: `accepted`, `rejected`, `deferred`, `question`, or `human-required`
- target kind and target id, with optional spec id and task id
- reviewer id and role
- `evidence_checked` values named by the reviewer
- structured findings from `--finding severity|summary|required action`
- follow-up tickets and `follow_up_routing`
- explicit `human_required.required` plus reason when true
- source artifact paths and note text
- self-hosted, credential-free flags

## Boundaries

- Decision records are durable reviewer evidence, not GitHub PR integration.
- T010 owns branch and PR status integration.
- T011 owns self-hosted Langfuse trace and eval deep links.
- Human review is required only for user-reserved, missing, or contradictory decisions.
- The decision command is credential-free and does not require GitHub, hosted Logfire, hosted Langfuse, or external
  tokens.
