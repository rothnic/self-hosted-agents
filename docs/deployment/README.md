# Deployment Reference

Goal 005 turns the selected Pydantic AI plus Langfuse/DBOS product baseline into a reproducible self-hosted deployment
reference.

Start here when an agent needs the deployment profile, target machine, or operating boundary for the selected stack.

## Profile Index

- `profiles.md`: local, development-server, and production-like deployment profiles.
- `service-boundaries.md`: service boundaries, ports, volumes, secret names, storage paths, and target machines.
- `environment-readiness.md`: environment templates and the `awf deployment-readiness` credential-free readiness check.
- `startup.md`: one-command local startup and documented service-backed startup equivalents.
- `smoke.md`: representative selected-stack smoke command and repo-local correlation evidence shape.
- `../operations/backup-restore-reset.md`: backup, restore, and reset runbook for database, service state, and run
  evidence.
- `../operations/diagnostics.md`: health, log, trace, and diagnostics runbook for app, observability, durable runtime,
  and storage.
- `../operations/recovery-retention-cost.md`: rollback, recovery, retention, resource, and cost runbook for one-engineer
  operation.

## Current Profile Recommendation

Use the **local profile** for deterministic development and ticket validation. It must remain credential-free and must
not require model providers, hosted observability, or running self-hosted services.

Use the **development-server profile** on `vps-dev` for heavier service-backed proof work when Docker-backed Langfuse,
DBOS production-storage experiments, or longer smoke runs would be too expensive on the MacBook.

Use the **production-like profile** on `vps-gw` only for controlled always-on management proof. It is not final
production promotion until backup, restore, reset, health, trace, recovery, and fresh-setup evidence are accepted.

## Boundaries

- Deployment profiles define topology and assumptions.
- Service boundaries define the current port, volume, secret-name, storage-path, and target-machine map.
- Environment readiness defines credential-free templates and prerequisite checks.
- Startup defines the local one-command manifest and service-backed equivalent commands.
- Smoke defines the representative selected-stack workflow command.
- Operations runbooks define backup, restore, reset, diagnostics, recovery, retention, and rehearsal surfaces as they
  are completed.
- Deterministic fixture validation remains the closure gate unless a ticket explicitly requires service-backed proof.
