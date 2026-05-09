---
name: retrospector
description: Use after a workflow run to capture concise learnings and propose small process improvements for future agent runs.
---

# Retrospector

## Purpose

Improve the process without turning every run into a large process rewrite.

## Workflow

1. Review the run report and checks.
2. Capture what slowed the agent down or caused ambiguity.
3. Propose at most three improvements.
4. Separate accepted changes from proposals needing human review.
5. Use `uv run awf learning-capture --note "..."`

## Output

- What happened
- What helped
- What failed or was unclear
- One next process improvement
