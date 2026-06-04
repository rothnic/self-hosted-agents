# Current Objectives

## Objective: Agentic Development Foundation

ID: `agentic-development-foundation`
Status: active

Build an environment-agnostic operating system for coding agents, then use it to compare self-hostable agent application
stacks against real implementations. The first target user is the project owner as an engineer who prefers Python,
cannot rely on approved self-hosted LangSmith access, and needs evidence-backed choices about observability,
evaluation, orchestration, scalability, and operating effort.

Current long-horizon goal: execute `docs/goals/000-self-hosted-agent-system-roadmap.md` as the parent goal, working
through its linked child goals in order.

Current roadmap checkpoint: Goals 001 through 004 are accepted for this roadmap increment by independent reviewer
evidence. Goal 004 selected Pydantic AI plus Langfuse and DBOS as the first product-baseline stack from comparable
implementation evidence, defined the product baseline workflow, added BDD contracts and setup notes, froze non-selected
candidate references, recorded migration notes, and created production-hardening follow-up epics. The active follow-on
work is Goal 005: define and prove the self-hosted deployment and operations reference for the selected stack.

## Success Criteria

- A new agent can start from `AGENTS.md`, run bootstrap/context commands, and know the next safe action.
- Specs, ADRs, research notes, tickets, behavior contracts, run reports, and learnings have clear homes.
- Planning, ticketing, review-gate, BDD contract, and retrospective flows can run without product-specific implementation.
- Workflow validation passes against an isolated fixture.
- The product roadmap maps high-level system requirements into comparable implementation options.
- The product roadmap keeps a functional needs map that lists the minimum functional areas every candidate must cover,
  identifies which solution components provide each function, and records useful extra capabilities that should affect
  scoring when a candidate provides them without custom infrastructure.
- Each candidate solution is tested as a separate runnable app while sharing common contracts, fixtures, and evaluation
  assets where useful.
- Final candidate solutions include self-hosted, LLM-aware observability evidence as part of the tested stack, while
  preserving deterministic repo-local artifacts for repeatable validation.
- Final candidate solutions include durable execution, with candidate runtimes evaluated for low complexity, easy
  startup, understandable recovery behavior, and a credible scale path.
- Long-horizon product iterations are tracked as goal documents with proof gates, task backlogs, review criteria, and
  kickoff prompts before being decomposed into executable Beads tickets.
- Roadmap reviews can be initiated by the human and should produce refreshed objectives, specs, tasks, tickets, and
  comparison criteria without requiring manual workflow operation.

## Constraints

- Keep durable project state in git-friendly repo artifacts.
- Keep execution environment assumptions behind scripts.
- Use Beads Rust as the ticket system when available, while scripts must degrade clearly when `br` is missing.
- Use Spec Kit concepts without requiring a hosted service.
- Use BDD contracts to describe implementation-agnostic e2e behavior before comparing implementations.

## Non-Goals

- Do not treat the selected Pydantic AI plus Langfuse/DBOS product baseline as a final solution until production
  observability, evaluation, durable execution, setup, and recovery blockers have repo-local or self-hosted evidence.
- Do not automate risky writes without explicit `--write`.
- Do not let recurring agents bypass review gates; goal and increment evidence requires independent reviewer
  acceptance unless the user explicitly reserves the decision.
