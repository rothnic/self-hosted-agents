# Handoff Summary

Status: defined for Goal 006 T012.

`uv run awf handoff-summary` generates concise handoff summaries for local sessions and scheduled agents. The summary
reduces context bloat while keeping exact artifact handles for the next agent to inspect.

## Commands

```bash
uv run awf handoff-summary --json
uv run awf handoff-summary --audience scheduled --json
uv run awf handoff-summary --write --json
uv run awf handoff-summary --audience scheduled --write --json
```

## Artifact

Each generated artifact uses schema `awf.operator-workbench.handoff-summary.v1` and includes:

- `copy_ready`: short lines suitable for a next-session prompt or scheduled-agent run note
- `current_state`: branch, commit, goal, spec, phase, health, and review-gate state
- `next_work`: next ticket, title, status, external reference, claim path, and worker id when present
- `validation`: exact validation commands and latest shallow status
- `risks`: current handoff risks from the operator status report
- `exact_artifact_handles`: claim, next work source, presenter report, reviewer report, trace, eval, branch, PR, and
  status handles
- `local_session`: resume prompt and first command for a human-started local session
- `scheduled_agent`: resume prompt and first command for scheduled agents
- `self_hosted`: credential-free and external-service-required flags

## Boundaries

- The command reads repo-local operator status, Beads, claims, reports, traces, evals, and PR fallback state.
- It does not require hosted Logfire, hosted Langfuse, GitHub, cloud credentials, or external project tokens.
- The handoff summary is a compact routing artifact, not a substitute for source-of-truth files.
- T013 owns the interface decision for CLI/static versus local UI.

## Usage

Use the default `session` audience when ending or resuming an interactive agent session. Use `--audience scheduled` for
automation loops that need a compact state packet without prior chat context. Both paths remain credential-free and
automation-compatible.
