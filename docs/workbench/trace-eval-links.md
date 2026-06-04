# Trace And Eval Links

Status: added for Goal 006 T011.

`uv run awf trace-eval-links` summarizes recent repo-local trace and evaluation artifacts and links them to optional
self-hosted Langfuse trace URLs when those URLs are present in trace evidence. The command keeps repo-local trace and
repo-local eval artifacts as the deterministic source of truth, so missing Langfuse access does not block validation.

## Command

```bash
uv run awf trace-eval-links --json
uv run awf trace-eval-links --write --json
```

Use `--write` to persist a repo-local artifact under `.agent-runs/reports/workbench/`.

## Artifact

Each generated status uses schema `awf.operator-workbench.trace-eval-links.v1` and includes:

- `repo_local_trace_links`: recent `*.trace.json` artifacts with run id, trace id, OTLP trace id, span counts, and
  repo-local path links
- `repo_local_eval_links`: recent `*.evaluation.json` artifacts with evaluation id, run id, trace id, score, pass state,
  rerun command, and repo-local path links
- `self_hosted_langfuse_links`: self-hosted Langfuse trace URLs recorded in trace artifacts, when available
- `correlations`: trace/eval pairs with `match_method`, preferring explicit trace-evidence paths before unambiguous id
  fallback
- `availability`: self-hosted Langfuse and repo-local evidence availability states
- `gaps`: explicit explanation when Langfuse deep links are unavailable
- `self_hosted`: credential-free and external-service-required flags

## Boundaries

- Langfuse deep links are optional enrichment, not a validation dependency.
- The command does not call Langfuse or require hosted Logfire, hosted Langfuse, GitHub, cloud credentials, or external
  project tokens.
- If trace artifacts contain verified Langfuse URLs, those URLs are surfaced.
- If Langfuse URLs are missing, repo-local trace and eval artifacts remain authoritative.
- T012 owns concise session and scheduled-agent handoff summaries.
