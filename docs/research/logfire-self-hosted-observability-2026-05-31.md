# Logfire Self-Hosted Observability Review

Date: 2026-05-31

## Question

Should `awf-52w` / T022 remain blocked on a cloud-hosted Logfire project and token, or can the blocker be resolved with
self-hosted-compatible OpenTelemetry evidence?

## Findings

Pydantic AI's observability path is OpenTelemetry-based. The Pydantic AI docs describe Logfire support as optional and
state that Pydantic AI can send data to any OpenTelemetry-compatible backend. The same docs include two important
self-hosted-friendly paths: use the Logfire SDK with `send_to_logfire=False` and an `OTEL_EXPORTER_OTLP_ENDPOINT`, or
emit OTel without Logfire by configuring OpenTelemetry providers directly.

Logfire itself has a self-hosted path, but it is not a lightweight local dependency. Pydantic's self-hosted deployment
docs say self-hosted Logfire runs in Kubernetes through the official Helm chart, is included in the Enterprise plan, and
requires access to private container images. Production prerequisites include Kubernetes capacity, image pull
credentials, PostgreSQL databases, object storage, identity provider support, and storage configuration.

Pydantic Evals also uses OpenTelemetry for traces and can send those traces to any OpenTelemetry-compatible backend,
including Logfire. That supports keeping Pydantic Evals work in T023 correlated to the same portable trace strategy
rather than making a cloud Logfire project a prerequisite.

## Recommendation

Resolve the blocker by changing T022's acceptance from cloud-hosted Logfire proof to self-hosted-compatible trace
evidence. The tested `apps/pydantic-ai` candidate should keep deterministic fixture validation credential-free, write a
repo-local OTel-style trace artifact linked from the run artifact, and document Logfire's self-hosting feasibility gap.

Cloud-hosted Logfire credentials should not close or block this self-hosted agents assessment. A Logfire export run can
remain optional diagnostic evidence when an operator provides an approved backend, preferably self-managed via
`LOGFIRE_BASE_URL`, but it should not be the acceptance gate.

## Confidence

High for replacing the cloud-hosted blocker with local OTel evidence for T022. Medium for any future self-hosted Logfire
plan because access, pricing, and image availability depend on Pydantic Enterprise terms.

## Sources

- Pydantic AI Logfire and OpenTelemetry integration:
  https://pydantic.dev/docs/ai/integrations/logfire/
- Pydantic Logfire self-hosted deployment overview:
  https://pydantic.dev/docs/logfire/deploy/self-hosted-deployment/overview
- Pydantic Evals Logfire integration:
  https://pydantic.dev/docs/ai/evals/how-to/logfire-integration/
