# Accessibility And Small-Screen Rationale

Status: implemented for Goal 006 T015.

`uv run awf accessibility-small-screen --json` records why Goal 006 does not add UI-specific accessibility or
small-screen checks now. The selected interface remains CLI/static, and no local UI is built for this goal.

Use `uv run awf accessibility-small-screen --write --json` to persist a JSON artifact under
`.agent-runs/reports/workbench/accessibility/`.

Generated artifacts use schema `awf.operator-workbench.accessibility-small-screen.v1`.

## Current Decision

No local UI is built for Goal 006. The workbench is generated from CLI/static repo artifacts:

- `uv run awf workbench-interface --json`
- `uv run awf operator-status --json`
- `uv run awf handoff-summary --json`
- Markdown docs and repo-local JSON evidence

Because there is no browser viewport, terminal UI runtime, focus model, ARIA layer, color palette, responsive layout, or
server process, UI-specific accessibility and small-screen checks would not prove real product behavior.

## Accessibility Model

The current interface relies on standard text surfaces:

- Plain text, Markdown, JSON, terminal, editor, and PR rendering.
- Exact command names and repo-relative artifact handles.
- Line-oriented primary actions for inspect, continue, review, and verify.
- No pointer-only actions, custom keyboard focus, color-only state, or decorative UI controls.

## Small-Screen Model

The current interface stays reviewable without a custom viewport:

- Command output and Markdown sections can wrap in terminals, editors, and mobile PR views.
- Dense data remains in repo-local JSON artifacts instead of fixed-width UI panels.
- Operator docs avoid hidden hover-only controls and nested cards.
- Source artifacts remain linkable when summaries are too narrow to read comfortably.

## Future UI Gate

If a future reviewed decision selects a local web or terminal UI, that future UI must add accessibility and small-screen
evidence before acceptance. At minimum, it should prove:

- Keyboard-only operation for primary actions.
- Screen-reader labels or semantic terminal equivalents.
- Focus order and visible focus indication.
- No color-only state.
- Small-screen or narrow-terminal review.
- Visual or snapshot evidence for rendered UI behavior.

Any future UI must preserve CLI/static automation commands, repo-local source-of-truth artifacts, and credential-free
deterministic validation.

## Self-Hosted Boundary

This rationale is credential-free. It does not call hosted Logfire, hosted Langfuse, GitHub, cloud credentials, external
project tokens, browser automation, or any UI runtime. Repo-local artifacts remain authoritative.
