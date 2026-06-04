# Pydantic AI Product Baseline Setup And Operating Notes

Status: defined for Goal 004 T010
Selected stack: Pydantic AI plus Langfuse and DBOS
Baseline workflow: `docs/product-baseline/pydantic-ai-review-gated-work-order.md`
BDD contract: `tests/workflow/features/product_baseline_work_order.feature`
Acceptance command: `uv run awf workflow-fixture-test`

## Purpose

Show another agent how to start, reset, inspect, and operate the selected product baseline without hidden chat context or
hosted service dependencies.

These notes are for the product-baseline work-order workflow. They do not promote the stack as final production
infrastructure. Langfuse production operations, DBOS production storage, DBOS worker topology, recovery rehearsal, live
model/tool trace coverage, and richer evaluation workflows remain follow-up proof gates.

## Operating Modes

### Deterministic Fixture Mode

Use this mode for normal local validation, CI-like checks, and ticket closure.

Requirements:

- repo checkout;
- `uv` environment bootstrapped by `tools/agent-workflow/bootstrap-dev.sh --install-tools`;
- Beads available through the repo workflow commands;
- no model provider key;
- no hosted Logfire project;
- no Langfuse service;
- no persistent DBOS service.

Primary checks:

```bash
uv run awf bootstrap
uv run awf bdd-lint
uv run awf bdd-run --driver fixture
uv run awf workflow-fixture-test
uv run awf verify --profile ticket --json
```

Deterministic fixture validation must continue to pass when `LANGFUSE_BASE_URL`, `LANGFUSE_PUBLIC_KEY`,
`LANGFUSE_SECRET_KEY`, `LOGFIRE_TOKEN`, and model-provider credentials are unset.

### Self-Hosted Observability Proof Mode

Use this mode only when an operator has a local or controlled self-hosted Langfuse service available.

Reference setup:

- `docs/orchestration/self-hosted-langfuse.md`
- `apps/pydantic-ai/README.md`

Proof command shape:

```bash
LANGFUSE_BASE_URL=http://localhost:3000 \
LANGFUSE_PUBLIC_KEY=<self-hosted-project-public-key> \
LANGFUSE_SECRET_KEY=<self-hosted-project-secret-key> \
LANGFUSE_PROJECT_ID=self-hosted-agents-pydantic-ai \
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-product-baseline-langfuse.json \
  --require-langfuse-ingestion \
  --pretty
```

Credentials alone must not trigger network ingestion. The app sends Langfuse traffic only when
`--require-langfuse-ingestion` is passed. Without that flag, ambient credentials cannot make deterministic fixture
validation depend on a service.

### Durable Local Proof Mode

Use this mode when the work-order path needs DBOS retry, resume, review-wait, or side-effect evidence.

Reference setup:

- `apps/pydantic-ai/README.md`
- `.agent-runs/verifications/pydantic-ai-durable-smoke-t010-20260602.json`

The durable proof uses local disposable SQLite and JSONL paths. It does not require a DBOS server, DBOS queue worker,
model provider, Langfuse service, hosted Logfire project, or cloud credential.

## Start Procedure

1. Bootstrap the repo:

   ```bash
   tools/agent-workflow/bootstrap-dev.sh --install-tools
   uv run awf bootstrap
   ```

2. Inspect current state:

   ```bash
   uv run awf context-index --json
   uv run awf ready-work --json
   uv run awf review-gate --json
   git status --short --branch
   ```

3. Claim one Beads-ready product-baseline item:

   ```bash
   uv run awf claim-work --worker-id <stable-worker-id> --write --json
   ```

4. Build the work-order evidence from repo artifacts:

   - current objective: `objectives/current.md`;
   - Goal 004: `docs/goals/004-candidate-platform-decision-product-baseline.md`;
   - selected-stack ADR: `docs/adr/0005-select-pydantic-ai-langfuse-dbos-for-product-baseline.md`;
   - baseline workflow: `docs/product-baseline/pydantic-ai-review-gated-work-order.md`;
   - BDD contract: `tests/workflow/features/product_baseline_work_order.feature`;
   - linked spec: `specs/005-candidate-platform-decision-product-baseline/`.

5. Validate before reviewer handoff:

   ```bash
   uv run awf bdd-lint --json
   uv run awf bdd-run --driver fixture --json
   uv run awf workflow-fixture-test --json
   uv run awf verify --profile ticket --json
   ```

6. Present evidence to an independent reviewer agent. The reviewer must accept or reject the evidence in a durable
   report before the ticket or increment is considered accepted.

7. Close the Beads ticket only after acceptance evidence exists:

   ```bash
   uv run awf complete-work --issue-id <issue-id> \
     --worker-id <stable-worker-id> \
     --evidence "<summary of accepted evidence and validation>" \
     --write --json
   ```

## Reset Procedure

Reset only disposable state. Do not delete committed evidence artifacts.

For workflow claims:

```bash
uv run awf cleanup-work --write --json
```

For deterministic Pydantic AI run artifacts created during local experiments:

```bash
rm -f .agent-runs/verifications/pydantic-ai-product-baseline-local.json \
  .agent-runs/verifications/pydantic-ai-product-baseline-local.trace.json \
  .agent-runs/verifications/pydantic-ai-product-baseline-local.evaluation.json
```

For DBOS local smoke state, prefer explicit `/tmp` paths and remove those paths before reusing the same workflow id.
The detailed DBOS reset command lives in `apps/pydantic-ai/README.md`.

For self-hosted Langfuse proof state:

```bash
cd ~/data/projects/langfuse
docker compose down -v
docker compose up -d
```

Keep generated Langfuse keys outside this repository. Resetting Langfuse removes local trace data and project keys.

## Inspect Procedure

Use repo-local inspection first:

```bash
uv run awf ready-work --json
uv run awf workflow-state-lint --json
uv run awf repo-hygiene --json
uv run awf verify --profile ticket --json
```

Inspect deterministic run evidence:

```bash
uv run python apps/pydantic-ai/run.py \
  --fixture packages/comparison/fixtures/pydantic-ai-decision-slice.json \
  --output .agent-runs/verifications/pydantic-ai-product-baseline-local.json \
  --pretty
```

Expected local artifacts:

- `.agent-runs/verifications/pydantic-ai-product-baseline-local.json`;
- `.agent-runs/verifications/pydantic-ai-product-baseline-local.trace.json`;
- `.agent-runs/verifications/pydantic-ai-product-baseline-local.evaluation.json`.

Inspect the local artifact summary:

```bash
python3 - <<'PY'
import json
from pathlib import Path

path = Path(".agent-runs/verifications/pydantic-ai-product-baseline-local.json")
artifact = json.loads(path.read_text())
print(json.dumps({
    "candidate_app_id": artifact["candidate_app_id"],
    "run_id": artifact["run_id"],
    "trace_id": artifact["trace_id"],
    "acceptance_check": artifact["acceptance_check"],
    "trace_evidence": artifact["evidence_paths"].get("trace_evidence"),
    "evaluation_evidence": artifact["evidence_paths"].get("evaluation_evidence"),
    "gaps": artifact["gaps"],
}, indent=2))
PY
```

When self-hosted Langfuse proof mode is used, inspect both the repo-local `.trace.json` file and the Langfuse UI or API
for the same trace id. A Langfuse UI link is additive evidence, not a replacement for repo-local artifacts.

## Failure Handling

- Missing `uv`, `br`, or hook setup: run `tools/agent-workflow/bootstrap-dev.sh --install-tools`.
- Dirty or stale claims: run `uv run awf cleanup-work --write --json`, then inspect `uv run awf ready-work --json`.
- `workflow-fixture-test` fails: treat it as a blocker for ticket closure and record the failing check output in the
  task report or issue log.
- Langfuse unavailable: continue deterministic fixture validation and record the observability proof as a gap unless
  the specific ticket requires service-backed self-hosted Langfuse evidence.
- DBOS local state conflict: delete the explicit `/tmp` DBOS SQLite and JSONL paths before rerunning the same workflow
  id.
- Reviewer rejects evidence: do not close the ticket. Record findings in the task report and create follow-up Beads
  work if the fix is outside the claimed ticket.

## Evidence Boundary

Accepted product-baseline work must leave enough evidence for another agent to verify without prior chat:

- linked Beads issue and spec task;
- commands run and pass/fail status;
- repo-local run, trace, evaluation, durable, or report artifacts as applicable;
- independent reviewer id and accepted/rejected outcome;
- explicit follow-up tickets or a statement that none are required for the slice;
- PR body updated when the checkpoint changes the roadmap evidence state.
