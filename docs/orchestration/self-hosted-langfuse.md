# Self-Hosted Langfuse Profile

This profile is the Goal 001 observability target for local or VPS-backed proof runs. It keeps Langfuse as the
LLM-aware trace UI while preserving repo-local artifacts for deterministic fixture validation.

## Source

Use the upstream Langfuse Docker Compose deployment for local and low-scale VM proofs:

```bash
git clone https://github.com/langfuse/langfuse.git ~/data/projects/langfuse
cd ~/data/projects/langfuse
docker compose up -d
```

The official profile requires Git, Docker, and Docker Compose. The web UI listens on `3000`; the OTLP/HTTP trace
ingestion endpoint is `http://<host>:3000/api/public/otel/v1/traces`. Langfuse requires Basic Auth with the project
public key as the username and secret key as the password. Include `x-langfuse-ingestion-version=4` for the current
OTel ingestion path.

## Services

The Docker Compose profile starts the Langfuse web app, worker, Postgres, ClickHouse, Redis or Valkey, and S3-compatible
blob storage. Plan for at least 4 CPU cores, 16 GiB memory, and enough disk for trace storage on a VM proof host.

Only port `3000` must be reachable by the candidate app. MinIO ports are for the stack internals and should not be part
of the proof contract.

## Headless Setup

For repeatable proof runs, configure Langfuse headless initialization in the Compose environment before first startup:

```bash
LANGFUSE_INIT_ORG_ID=self-hosted-agents
LANGFUSE_INIT_ORG_NAME=Self Hosted Agents
LANGFUSE_INIT_PROJECT_ID=self-hosted-agents-pydantic-ai
LANGFUSE_INIT_PROJECT_NAME=Pydantic AI Candidate
LANGFUSE_INIT_PROJECT_PUBLIC_KEY=pk-lf-self-hosted-agents
LANGFUSE_INIT_PROJECT_SECRET_KEY=sk-lf-self-hosted-agents
LANGFUSE_INIT_USER_EMAIL=operator@example.local
LANGFUSE_INIT_USER_NAME=Operator
LANGFUSE_INIT_USER_PASSWORD=<local-only-password>
```

If the Compose file is cloned upstream, keep generated secrets outside this repository. The proof command only needs:

```bash
LANGFUSE_BASE_URL=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-lf-self-hosted-agents
LANGFUSE_SECRET_KEY=sk-lf-self-hosted-agents
LANGFUSE_PROJECT_ID=self-hosted-agents-pydantic-ai
```

## Proof Command

Run from this repository:

```bash
LANGFUSE_BASE_URL=http://localhost:3000 \
LANGFUSE_PUBLIC_KEY=pk-lf-self-hosted-agents \
LANGFUSE_SECRET_KEY=sk-lf-self-hosted-agents \
LANGFUSE_PROJECT_ID=self-hosted-agents-pydantic-ai \
python3 apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output /tmp/pydantic-ai-run.json \
  --require-langfuse-ingestion \
  --pretty
```

Passing service-backed evidence requires the command to write `/tmp/pydantic-ai-run.trace.json`, send OTLP/HTTP JSON to
Langfuse, and verify the same OTLP trace id through `GET /api/public/traces/<trace-id>`.

## Deterministic Fallback

Do not require Langfuse for `uv run awf workflow-fixture-test`. Without `LANGFUSE_BASE_URL`,
`LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_SECRET_KEY`, the Pydantic AI command records
`missing-langfuse-otel-config`, writes the local trace artifact, and exits successfully unless
`--require-langfuse-ingestion` is set.

## Reset

For an isolated proof stack:

```bash
cd ~/data/projects/langfuse
docker compose down -v
docker compose up -d
```

Reset removes local Langfuse data and API keys. Reapply headless initialization values before restarting if the Compose
environment was not persisted.

## Troubleshooting

- `docker` missing locally: run the profile on `vps` or another controlled host and reach it through an SSH tunnel.
- `401` or `403`: verify the public and secret key pair belongs to the project receiving OTLP traces.
- `404` during trace verification: wait for worker ingestion, then retry the proof command; queued ingestion can lag.
- Empty UI trace list: confirm the command used `/api/public/otel/v1/traces` and sent the ingestion-version header.
- High memory usage: stop the stack with `docker compose down` when proof is complete.
