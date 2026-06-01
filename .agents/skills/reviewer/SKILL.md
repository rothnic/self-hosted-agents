---
name: reviewer
description: Use when reviewing code, specs, tickets, behavior contracts, or workflow changes for correctness, drift, and missing tests.
---

# Reviewer

## Purpose

Find bugs, process drift, missing acceptance criteria, and mismatches between specs, tickets, behavior contracts, and implementation.

## Review Checklist

- Does the change match the linked objective and spec?
- Is scope limited to the ticket?
- Are behavior contracts updated for changed e2e behavior?
- Are operational expectations covered when relevant?
- Do acceptance checks pass?
- For goal or increment evidence, did a presenting agent provide enough durable evidence to accept the goal?
- Are new decisions recorded instead of guessed?

## Output

Lead with findings ordered by severity. Include file and line references when reviewing local files.
When reviewing goal or increment evidence, clearly state `accepted` or `rejected`, list the evidence checked, and name
any required follow-up tickets. When reviewing merge readiness, state the human's next options: approve/merge, request
changes, or continue with another ready Beads item. Do not imply that approval or merge happened unless it was
explicitly requested and completed.
