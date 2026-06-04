# Pydantic AI Product Baseline: Review-Gated Work Order

Status: defined for Goal 004 T008
Selected stack: Pydantic AI plus Langfuse and DBOS
Acceptance command: `uv run awf workflow-fixture-test`
BDD contract: `tests/workflow/features/product_baseline_work_order.feature`
Setup and operating notes: `docs/product-baseline/pydantic-ai-setup-operating-notes.md`

## Purpose

Define the first product-oriented workflow for the selected stack. This baseline is distinct from the comparison demo:
it does not only recommend a next slice for candidate scoring. It turns an approved roadmap or spec request into one
review-gated implementation work order that can be claimed, executed, observed, evaluated, reviewed, and resumed.

## User Job

The project owner wants to hand the system a repo-local goal, spec, or Beads issue and get back one coherent
implementation work order with enough evidence for another agent to execute or review without hidden chat context.

The first product job is:

> Given an approved roadmap goal or selected ready Beads issue, produce and track a self-hosted implementation work
> order that names the intended behavior, execution boundary, acceptance command, trace and evaluation expectations,
> durable recovery behavior, and independent review gate.

## Actors

- **Project owner**: chooses the roadmap goal or priority when tradeoffs remain.
- **Implementer agent**: claims one ready Beads item and executes the work order.
- **Reviewer agent**: accepts or rejects the evidence produced by the implementer.
- **Operator**: inspects local artifacts, self-hosted observability, durable run state, and follow-up tickets.

## Inputs

- Goal, spec, or ticket reference, such as `docs/goals/004-candidate-platform-decision-product-baseline.md` or a Beads
  issue id.
- Current objective state from `objectives/current.md`.
- Spec artifacts from `specs/<id>/spec.md`, `plan.md`, and `tasks.md`.
- Ready-work state from `uv run awf ready-work --json`.
- Constraints from the roadmap, including self-hosted operation, no hosted credential dependency for deterministic
  validation, independent reviewer acceptance, and final-solution promotion blockers.
- Existing evidence artifacts, ADRs, and comparison matrix entries relevant to the selected stack.

## Outputs

The baseline workflow produces a typed work-order artifact with these fields:

- `work_order_id`
- `goal_id`
- `spec_id`
- `beads_issue_id`
- `selected_stack`
- `user_job`
- `behavior_scope`
- `out_of_scope`
- `acceptance_command`
- `implementation_boundary`
- `review_gate`
- `trace_expectations`
- `evaluation_expectations`
- `durable_expectations`
- `setup_expectations`
- `evidence_paths`
- `follow_up_policy`

The work order must also name whether the next action is safe to execute, blocked by missing evidence, or requires a
new product or architecture decision.

## Workflow Steps

1. **Load repo state**: read the current objective, selected goal, linked spec, Beads issue, existing evidence, and
   review-gate state.
2. **Normalize the request**: translate the user request or ready Beads issue into a single behavior scope with explicit
   out-of-scope boundaries.
3. **Create the work order**: emit the typed work-order artifact with acceptance, trace, evaluation, durable, setup, and
   review expectations.
4. **Execute or hand off**: if the work is already claimed by the current agent, execute the implementation slice;
   otherwise hand off the work order to the implementer role.
5. **Capture evidence**: write repo-local run, trace, evaluation, and report artifacts, and link any self-hosted
   observability evidence as additive proof.
6. **Pause for independent review**: require a reviewer agent to accept or reject the evidence before the ticket,
   increment, or goal can be considered accepted.
7. **Resume after review**: continue durable execution only when the reviewer outcome is accepted; otherwise record
   findings, follow-up tickets, or blockers.
8. **Close or route**: close the Beads ticket through `complete-work` when acceptance passes, or route the next safe
   action back into Beads and durable reports.

## Selected Stack Responsibilities

- **Pydantic AI** owns the typed agent boundary, structured work-order output, tool/context adapters, and deterministic
  fixture mode.
- **Langfuse** owns the self-hosted-compatible LLM trace review surface when service-backed proof is available.
- **Repo-local OpenTelemetry artifacts** remain the deterministic trace fallback and must be inspectable without
  hosted credentials.
- **Pydantic Evals** owns repeatable scoring for work-order shape, evidence completeness, and correlation.
- **DBOS** owns durable workflow execution, retry, resume, review wait, side-effect idempotency, and recovery evidence.
- **Beads and awf** remain the executable backlog and workflow-state authority.

## Review Gate

The work order is not accepted until an independent reviewer agent records an outcome in a durable artifact. Reviewer
evidence must include:

- artifact paths reviewed;
- validation commands checked;
- accepted or rejected outcome;
- findings ordered by severity;
- required follow-up tickets, or an explicit statement that none are required.

Human review is not a blocker unless the user explicitly reserves a product, priority, architecture, or scope decision.

## Observability Expectations

Every baseline run must preserve:

- a repo-local trace artifact correlated to `work_order_id`, `beads_issue_id`, `spec_id`, and run id;
- self-hosted Langfuse trace evidence when the local service is available;
- model, tool, state-transition, failure, latency, token, and cost fields where the tested path can provide them;
- explicit gap notes when a field is simulated, unavailable, or deferred.

Deterministic fixture validation must pass without Langfuse, Logfire, cloud model, or hosted trace credentials.

## Evaluation Expectations

The deterministic evaluation should score:

- typed work-order schema completeness;
- single-ticket scope and out-of-scope clarity;
- acceptance command presence;
- trace, eval, durable, review, and Beads correlation;
- reviewer-gate enforcement;
- follow-up policy for missing production evidence.

Model-judge, annotation, or dashboard-backed evaluation can be additive later, but cannot replace repo-local
deterministic scoring.

## Durable Expectations

The baseline workflow must define durable states for:

- claim created;
- work order emitted;
- implementation started;
- evidence captured;
- waiting for independent review;
- accepted and resumable;
- rejected and routed to findings;
- closed through `complete-work`.

DBOS evidence must continue proving retry, resume, review wait, accepted-review resume, side-effect idempotency, and
correlation. Production storage, worker topology, and recovery rehearsal remain promotion blockers until later tickets
close them.

## Setup Expectations

T010 adds operating notes in `docs/product-baseline/pydantic-ai-setup-operating-notes.md` that show how another agent
starts, resets, and inspects the baseline without hidden service state.

The future setup path should preserve these boundaries:

- deterministic fixture mode requires only the repo `uv` environment;
- self-hosted Langfuse is optional for local validation and additive for observability proof;
- DBOS can use local disposable state for fixture validation;
- production-style Langfuse and DBOS operations remain follow-up proof gates.

## First Product Boundary

The first product implementation should deepen `apps/pydantic-ai/` into a work-order app boundary rather than adding
another comparison workflow. Shared BDD contracts, fixtures, and evaluation assets belong under `tests/` or
`packages/`; Pydantic AI, Langfuse, and DBOS glue stays inside `apps/pydantic-ai/` until another selected product lane
needs it.

T009 converted this definition into implementation-agnostic BDD contracts in
`tests/workflow/features/product_baseline_work_order.feature` with driver-boundary notes in
`tests/workflow/drivers/README.md`. T010 adds setup and operating notes in
`docs/product-baseline/pydantic-ai-setup-operating-notes.md`. Later implementation tickets should add the runnable
product boundary and its evidence artifacts.
