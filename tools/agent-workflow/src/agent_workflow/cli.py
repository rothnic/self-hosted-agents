from __future__ import annotations

import inspect
from types import SimpleNamespace
from typing import Any

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent_workflow import core


app = typer.Typer(
    add_completion=False,
    help="Manage the agentic development workflow: setup, specs, tickets, BDD contracts, and hygiene.",
    rich_markup_mode="rich",
)
console = Console()


class CommandEnvelope(BaseModel):
    ok: bool
    command: str
    summary: str
    data: dict[str, Any] = Field(default_factory=dict)


def ns(**kwargs: Any) -> SimpleNamespace:
    defaults = {"json": False, "write": False, "dry_run": False}
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def print_envelope(envelope: CommandEnvelope, json_output: bool) -> None:
    if json_output:
        console.print_json(envelope.model_dump_json())
        return
    status = "[green]ok[/green]" if envelope.ok else "[red]failed[/red]"
    console.print(Panel(envelope.summary, title=f"{envelope.command}: {status}", expand=False))
    data = envelope.data
    if "checks" in data:
        table = Table(title="Checks")
        table.add_column("Name")
        table.add_column("OK")
        table.add_column("Detail")
        for item in data["checks"]:
            detail = item.get("detail") or item.get("data", {}).get("next_action") or ""
            table.add_row(item["name"], "yes" if item["ok"] else "no", str(detail))
        console.print(table)
    elif "errors" in data:
        if data["errors"]:
            for error in data["errors"]:
                console.print(f"[red]- {error}[/red]")
        else:
            console.print("[green]No errors[/green]")
        for warning in data.get("warnings", []):
            console.print(f"[yellow]- warning: {warning}[/yellow]")
    elif "results" in data:
        summary = data.get("summary", {})
        if summary:
            console.print(
                f"[bold]Results:[/bold] {summary.get('passed', 0)}/{summary.get('total', 0)} passed"
            )
        failure_details = {
            item.get("name"): item.get("detail", "")
            for item in summary.get("failed_results", [])
            if isinstance(item, dict)
        }
        table = Table(title="Fixture Results")
        table.add_column("Name")
        table.add_column("OK")
        table.add_column("Detail")
        for item in data["results"]:
            ok = bool(item.get("ok"))
            detail = failure_details.get(item.get("name"), "")
            table.add_row(str(item.get("name", "")), "yes" if ok else "no", detail)
        console.print(table)
        if failure_details:
            console.print("[red]Failed checks:[/red]")
            for name, detail in failure_details.items():
                suffix = f": {detail}" if detail else ""
                console.print(f"[red]- {name}{suffix}[/red]")


def run_core_tuple(command: str, fn: Any, *, json_output: bool) -> int:
    if inspect.signature(fn).parameters:
        code, data = fn(ns(json=False))
    else:
        code, data = fn()
    envelope = CommandEnvelope(
        ok=code == 0,
        command=command,
        summary="Command completed." if code == 0 else "Command found issues.",
        data=data,
    )
    print_envelope(envelope, json_output)
    return code


@app.command()
def bootstrap(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Verify runtime tools, Beads Rust, hooks, repo layout, and project policy."""
    data = core.bootstrap_data()
    ok = all(item["ok"] for item in data["checks"])
    print_envelope(
        CommandEnvelope(ok=ok, command="bootstrap", summary="Environment bootstrap status.", data=data),
        json_output,
    )
    raise typer.Exit(0 if ok else 1)


@app.command("context-index")
def context_index(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Summarize objectives, specs, BDD contracts, tickets, blockers, and recent runs."""
    data = core.context_index_data()
    print_envelope(
        CommandEnvelope(ok=True, command="context-index", summary="Project context index.", data=data),
        json_output,
    )


@app.command("spec-lint")
def spec_lint(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Validate native Spec Kit feature structure and parseable tasks."""
    raise typer.Exit(run_core_tuple("spec-lint", core.spec_lint, json_output=json_output))


@app.command("spec-kit-lint")
def spec_kit_lint(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Validate Spec Kit tooling substrate, skills, constitution, and native feature artifacts."""
    raise typer.Exit(run_core_tuple("spec-kit-lint", core.spec_kit_lint, json_output=json_output))


@app.command("bdd-lint")
def bdd_lint(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Validate BDD contracts have actors, operational assertions, and driver boundaries."""
    raise typer.Exit(run_core_tuple("bdd-lint", core.bdd_lint, json_output=json_output))


@app.command("bdd-run")
def bdd_run(
    driver: str = typer.Option(..., "--driver", help="Driver name from tests/workflow/drivers."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Execute BDD contracts through a named test driver."""
    code, data = core.bdd_run_result(driver)
    print_envelope(
        CommandEnvelope(ok=code == 0, command="bdd-run", summary=f"Driver `{driver}` run.", data=data),
        json_output,
    )
    raise typer.Exit(code)


@app.command("review-gate")
def review_gate(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Check whether automation must pause for human review."""
    raise typer.Exit(run_core_tuple("review-gate", core.review_gate, json_output=json_output))


@app.command("repo-hygiene")
def repo_hygiene(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Enforce root cleanliness, directory size, line length, and alpha compatibility policy."""
    raise typer.Exit(run_core_tuple("repo-hygiene", core.repo_hygiene_result, json_output=json_output))


@app.command("workflow-state-lint")
def workflow_state_lint(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Validate task, Beads, gate, and ready-work consistency."""
    raise typer.Exit(run_core_tuple("workflow-state-lint", core.workflow_state_lint_result, json_output=json_output))


@app.command("install-hooks")
def install_hooks(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Install versioned git hooks by setting core.hooksPath to .githooks."""
    data = core.install_hooks_data()
    print_envelope(
        CommandEnvelope(ok=data["ok"], command="install-hooks", summary="Git hook installation status.", data=data),
        json_output,
    )
    raise typer.Exit(0 if data["ok"] else 1)


@app.command("workflow-fixture-test")
def workflow_fixture_test(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Run isolated workflow tests before product implementation."""
    code, data = core.workflow_fixture_test_result(write=False)
    print_envelope(
        CommandEnvelope(ok=code == 0, command="workflow-fixture-test", summary="Fixture validation.", data=data),
        json_output,
    )
    raise typer.Exit(code)


@app.command("ready-work")
def ready_work(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Show ready Beads work, falling back to parseable spec tasks."""
    data = core.ready_work_data()
    print_envelope(CommandEnvelope(ok=True, command="ready-work", summary="Ready work.", data=data), json_output)


@app.command("next-action")
def next_action(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Show the canonical next action and human/agent options from current repo state."""
    data = core.next_action_data()
    summary = data["recommendation"]["label"]
    print_envelope(CommandEnvelope(ok=data["ok"], command="next-action", summary=summary, data=data), json_output)
    raise typer.Exit(0 if data["ok"] else 1)


@app.command("health-status")
def health_status(
    deep: bool = typer.Option(False, "--deep", help="Run deeper fixture validation too."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Review project harness health and recommend the next safe action."""
    data = core.health_status_data(deep=deep)
    print_envelope(
        CommandEnvelope(ok=data["ok"], command="health-status", summary=data["next_action"], data=data),
        json_output,
    )
    raise typer.Exit(0 if data["ok"] else 1)


@app.command("verify")
def verify(
    profile: str = typer.Option(..., "--profile", help="ticket, increment, health, or pre-merge."),
    write: bool = typer.Option(False, "--write", help="Write a verification artifact."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Run the right workflow checks for a ticket, increment, health, or pre-merge context."""
    data = core.verify_data(profile=profile, write=write)
    print_envelope(
        CommandEnvelope(ok=data["ok"], command="verify", summary=data.get("next_action", "verify failed"), data=data),
        json_output,
    )
    raise typer.Exit(0 if data["ok"] else 1)


@app.command("increment-status")
def increment_status(
    increment_id: str | None = typer.Option(None, "--increment-id", help="Increment id, defaults from spec and phase."),
    spec_id: str = typer.Option("002-solution-comparison-roadmap", "--spec-id", help="Spec id."),
    phase: str = typer.Option("Phase 3", "--phase", help="Spec phase label."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Show phase-level increment state, child tickets, blockers, claims, and next action."""
    data = core.increment_status_data(increment_id=increment_id, spec_id=spec_id, phase=phase)
    print_envelope(
        CommandEnvelope(ok=data["ok"], command="increment-status", summary=data["next_action"], data=data),
        json_output,
    )


@app.command("increment-plan")
def increment_plan(
    increment_id: str | None = typer.Option(None, "--increment-id", help="Increment id, defaults from spec and phase."),
    spec_id: str = typer.Option("002-solution-comparison-roadmap", "--spec-id", help="Spec id."),
    phase: str = typer.Option("Phase 3", "--phase", help="Spec phase label."),
    write: bool = typer.Option(False, "--write", help="Write increment ledger and Beads labels."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Create or refresh the increment ledger for a spec phase."""
    data = core.increment_plan_data(increment_id=increment_id, spec_id=spec_id, phase=phase, write=write)
    print_envelope(
        CommandEnvelope(ok=data["ok"], command="increment-plan", summary=data["next_action"], data=data),
        json_output,
    )


@app.command("automation-loop")
def automation_loop(
    role: str = typer.Option(..., "--role", help="pm-review, orchestrator, worker, integrator, or health."),
    worker_id: str | None = typer.Option(None, "--worker-id", help="Worker id for worker/orchestrator roles."),
    increment_id: str | None = typer.Option(None, "--increment-id", help="Increment id, defaults from spec and phase."),
    spec_id: str = typer.Option("002-solution-comparison-roadmap", "--spec-id", help="Spec id."),
    phase: str = typer.Option("Phase 3", "--phase", help="Spec phase label."),
    write: bool = typer.Option(False, "--write", help="Mutate claims, ledgers, tickets, or evidence when safe."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Run one cron-safe PM/review, orchestrator, worker, integrator, or health loop."""
    data = core.automation_loop_data(
        role=role,
        write=write,
        worker_id=worker_id,
        increment_id=increment_id,
        spec_id=spec_id,
        phase=phase,
    )
    print_envelope(
        CommandEnvelope(
            ok=data["ok"],
            command="automation-loop",
            summary=data.get("next_action", "automation loop failed"),
            data=data,
        ),
        json_output,
    )
    raise typer.Exit(0 if data["ok"] else 1)


@app.command("issue-log")
def issue_log(
    title: str = typer.Option(..., "--title", help="Issue title."),
    severity: str = typer.Option("follow-up", "--severity", help="blocker, warning, or follow-up."),
    source: str = typer.Option("manual", "--source", help="Check or process that found the issue."),
    details: str = typer.Option("", "--details", help="Concise issue details."),
    write: bool = typer.Option(False, "--write", help="Write health artifact and Beads ticket."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Log a workflow issue so it can be resolved through the normal process."""
    if severity not in {"blocker", "warning", "follow-up"}:
        raise typer.BadParameter("severity must be blocker, warning, or follow-up")
    data = core.issue_log_data(title=title, severity=severity, source=source, details=details, write=write)
    print_envelope(CommandEnvelope(ok=True, command="issue-log", summary="Issue logged.", data=data), json_output)


@app.command("claim-work")
def claim_work(
    worker_id: str = typer.Option(..., "--worker-id", help="Stable id for the worker process."),
    write: bool = typer.Option(False, "--write", help="Write the claim file."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Claim one ready item for a worker without mixing concurrent work."""
    data = core.claim_work_data(worker_id=worker_id, write=write)
    print_envelope(
        CommandEnvelope(ok=data["ok"], command="claim-work", summary=data.get("reason", "Claim result."), data=data),
        json_output,
    )
    raise typer.Exit(0 if data["ok"] else 1)


@app.command("complete-work")
def complete_work(
    issue_id: str | None = typer.Option(None, "--issue-id", help="Beads issue id. Defaults to active claim."),
    evidence: str = typer.Option("", "--evidence", help="Evidence text to add before closing the issue."),
    worker_id: str | None = typer.Option(None, "--worker-id", help="Evidence author. Defaults to awf."),
    write: bool = typer.Option(False, "--write", help="Write Beads evidence, close issue, and mark the task complete."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Complete one claimed work item without task/Beads drift."""
    data = core.complete_work_data(issue_id=issue_id, evidence=evidence, worker_id=worker_id, write=write)
    print_envelope(
        CommandEnvelope(
            ok=data["ok"],
            command="complete-work",
            summary=data.get("next_action", "completion failed"),
            data=data,
        ),
        json_output,
    )
    raise typer.Exit(0 if data["ok"] else 1)


@app.command("cron-tick")
def cron_tick(
    role: str = typer.Option(..., "--role", help="planner or worker."),
    worker_id: str | None = typer.Option(None, "--worker-id", help="Required for worker role."),
    write: bool = typer.Option(False, "--write", help="Write artifacts, claims, and issue logs."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Run one cron-safe orchestration tick for planner or worker roles."""
    if role == "worker" and not worker_id:
        raise typer.BadParameter("worker role requires --worker-id")
    data = core.cron_tick_data(role=role, worker_id=worker_id, write=write)
    print_envelope(
        CommandEnvelope(ok=data["ok"], command="cron-tick", summary=data.get("next_action", "cron tick failed"), data=data),
        json_output,
    )
    raise typer.Exit(0 if data["ok"] else 1)


@app.command("ticket-sync")
def ticket_sync(
    write: bool = typer.Option(False, "--write", help="Create Beads tickets instead of proposals."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Convert approved spec tasks into Beads-compatible ticket proposals or real tickets."""
    data = core.ticket_sync_data(write=write)
    print_envelope(
        CommandEnvelope(ok=True, command="ticket-sync", summary="Ticket sync complete.", data=data),
        json_output,
    )


@app.command("workflow-run")
def workflow_run(
    mode: str = typer.Option(..., "--mode", help="Planning mode: plan, implement, or review."),
    trigger: str = typer.Option("manual", "--trigger", help="Trigger source for the run manifest."),
    write: bool = typer.Option(False, "--write", help="Write run manifest and report."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Force dry-run reporting."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Create a workflow run report for planning, implementation, or review."""
    if mode not in {"plan", "implement", "review"}:
        raise typer.BadParameter("mode must be one of: plan, implement, review")
    data = core.workflow_run_data(mode=mode, trigger=trigger, write=write, dry_run=dry_run)
    print_envelope(
        CommandEnvelope(ok=True, command="workflow-run", summary="Workflow run generated.", data=data),
        json_output,
    )


@app.command("run-report")
def run_report(json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output.")) -> None:
    """Show available run reports and the latest report body."""
    data = core.run_report_data()
    print_envelope(CommandEnvelope(ok=True, command="run-report", summary="Run reports.", data=data), json_output)


@app.command("learning-capture")
def learning_capture(
    note: str = typer.Option(..., "--note", help="Concise process learning to record."),
    source: str = typer.Option("manual", "--source", help="Where the learning came from."),
    write: bool = typer.Option(False, "--write", help="Write the learning artifact."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Capture a concise process learning for future planning cycles."""
    data = core.learning_capture_data(note=note, source=source, write=write)
    print_envelope(
        CommandEnvelope(ok=True, command="learning-capture", summary="Learning captured.", data=data),
        json_output,
    )


@app.command("spec-new")
def spec_new(
    short_name: str = typer.Argument(..., help="Spec Kit short feature name."),
    description: str = typer.Argument(..., help="Feature description passed to Spec Kit."),
    write: bool = typer.Option(False, "--write", help="Create Spec Kit files and branch instead of dry-run."),
    force: bool = typer.Option(False, "--force", help="Allow an existing generated branch."),
    json_output: bool = typer.Option(False, "--json", help="Emit typed JSON output."),
) -> None:
    """Create a native Spec Kit feature using the generated Specify script."""
    code, data = core.spec_new_result(slug=short_name, objective=description, write=write, force=force)
    print_envelope(
        CommandEnvelope(ok=code == 0, command="spec-new", summary="Spec creation result.", data=data),
        json_output,
    )
    raise typer.Exit(code)


def main() -> None:
    app()
