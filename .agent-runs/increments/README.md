# Increment Ledgers

This directory stores phase-level orchestration state created by `uv run awf increment-plan --write`.

Each ledger records objective/spec context, the feature branch, child tickets, worker claims, blockers, stale claims,
validation evidence, review status, and the next action for scheduled automation loops.
