# Agent Workflow Foundation Research

Status: current

## Findings

- Spec-driven development works best when intent, plan, tasks, and implementation are separate phases.
  This foundation mirrors that lifecycle with local templates and scripts.
- Progressive disclosure is important for agents: global instructions should route to specific skills, and skills should link to references only when needed.
- ADRs are well suited for durable decisions because each record captures one decision, its context, and its consequences.
- Local-first tickets reduce context switching and keep automation independent from hosted project management tools.
- BDD scenarios are useful as implementation-agnostic contracts when they focus on actors, observable outcomes, and
  operational evidence rather than UI or framework internals.

## Recommendation

Use repo artifacts as the durable context layer, a small workflow CLI as the environment boundary, project skills as
role-specific instructions, Beads as local tickets when installed, BDD contracts for e2e behavior, and human gates as
explicit stop states.

## Sources

- Spec Kit: https://github.com/github/spec-kit
- AGENTS.md: https://agents.md/
- ADR guidance: https://adr.github.io/
- Beads Rust: https://github.com/Dicklesworthstone/beads_rust
- Cucumber BDD reference: https://cucumber.io/docs/bdd/
