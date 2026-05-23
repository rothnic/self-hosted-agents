# Durable Execution Options Research

Date checked: 2026-05-23

## Research Question

Which durable execution options should the next Python-first candidate evaluate so the final solution can stay easy to
start, easy to understand, and easy to scale without adding unnecessary infrastructure complexity?

## Direction Recorded

The final solution must include durable execution. Hosted observability is also part of the stack being tested, not an
optional add-on. Deterministic local fixtures remain useful for repeatable tests, but they are not enough to promote a
candidate as a complete solution.

## Findings

Pydantic AI has co-maintained durable execution integrations with Temporal, DBOS, Prefect, and Restate. That makes those
four the first framework-specific options for a Pydantic AI implementation slice.

Hatchet is not listed as an official Pydantic AI durable execution integration, but it is a Python-friendly workflow and
task platform with durable tasks, a dashboard, replay, OpenTelemetry export, and self-host or cloud paths. It should be
evaluated as the main non-Pydantic-specific Python durable option because it may offer a simpler operator model for
background tasks and agent workflows than a lower-level durable runtime.

Logfire hosted observability is a real part of the Pydantic AI stack. Logfire also has a self-hosted path, but the
self-hosted deployment is Enterprise and Kubernetes-heavy. The next slice should therefore prove hosted Logfire
observability as part of the full solution while keeping repo-local artifacts for deterministic validation and review.

DBOS appears lightweight for Python and Pydantic AI because it can wrap an agent with `DBOSAgent`, checkpoint workflow
state in a database, and use SQLite for local examples or Postgres-like system storage for stronger operation. Its risk
is that deterministic workflow and step boundaries must be understood early.

Prefect appears attractive for low-friction Python background work because it can start embedded in an app process and
uses persisted task results rather than replaying whole workflows. Its risk is whether the model maps cleanly to
agent/tool call durability and human waits without becoming a general data-orchestration layer.

Restate appears strong for service-oriented durable handlers. It records execution steps in a journal, retries failed
invocations, and supports Python services, but it introduces a Restate server in front of the service. Its risk is extra
runtime architecture compared with DBOS or an embedded worker path.

Temporal remains the most proven durable execution platform in the set, with open-source self-hosting and Temporal
Cloud. Its risk for this project is complexity and operator burden relative to the current one-engineer objective.

## Recommendation

Use the next Pydantic AI slice to compare durable execution options before selecting one. Evaluate in this order:

1. Pydantic AI framework-specific paths: DBOS, Prefect, Restate, and Temporal.
2. Hatchet as the primary Python workflow-platform comparison.
3. Reject any option that cannot produce simple local setup, understandable recovery behavior, hosted observability
   correlation, and a credible scale path without excessive service sprawl.

Do not choose a durable runtime in this planning task. The next backlog should produce evidence that lets the roadmap
pick the lowest-complexity viable option.

## Candidate Comparison Questions

- What is the smallest local setup that proves crash/resume or retry behavior?
- Does the durable runtime preserve model calls, tool calls, human waits, and external side effects without duplicates?
- Can hosted observability correlate durable workflow runs to model/tool traces and evaluation outputs?
- How many services, credentials, and moving parts does one engineer need to run and debug it?
- What is the credible path from local proof to production scale?

## Confidence

Medium-high for the option set and evaluation order. Medium for final ranking because real repo implementation evidence
does not exist yet.

## Sources

- Pydantic AI durable execution overview: https://pydantic.dev/docs/ai/integrations/durable_execution/overview/
- Pydantic AI DBOS integration: https://pydantic.dev/docs/ai/integrations/durable_execution/dbos/
- Pydantic AI Restate integration: https://pydantic.dev/docs/ai/integrations/durable_execution/restate/
- Hatchet durable execution: https://hatchet.run/use-cases/durable-execution
- Hatchet core concepts: https://www.mintlify.com/hatchet-dev/hatchet/concepts
- Temporal durable execution overview: https://temporal.io/
- DBOS docs: https://docs.dbos.dev/
- Prefect durable execution: https://www.prefect.io/solutions/durable-execution
- Restate durable execution concepts: https://docs.restate.dev/foundations/key-concepts#durable-execution
- Logfire self-hosted deployment: https://pydantic.dev/docs/logfire/deploy/self-hosted-deployment/overview/
