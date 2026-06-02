# Verification Runs

This directory stores compact verification artifacts from `uv run awf verify --profile <name> --write`.

Verification artifacts are the handoff surface between scheduled roles. They record the checks run, failures, git
state, Beads readiness, review-gate state, acceptance evidence, and the next safe action.

Artifacts use compact schema `awf.verify.compact.v1`. They summarize each check with name, command, status, counts, and
short failure detail rather than embedding full nested command stdout/stderr. This keeps ticket and increment handoffs
small enough for another agent to inspect quickly while preserving the evidence needed to decide the next safe action.
