from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from dbos import DBOS, DBOSConfig, SetWorkflowID
from pydantic_ai import Agent
from pydantic_ai.durable_exec.dbos import DBOSAgent
from pydantic_ai.models.test import TestModel

from pydantic_candidate.trace import stable_id
from pydantic_candidate.workflow import DecisionRecommendation


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any], pretty: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2 if pretty else None, sort_keys=True) + "\n", encoding="utf-8")


def durable_recommendation() -> dict[str, str]:
    return {
        "linked_task": "T005",
        "next_slice": "Harden the restart/resume smoke so run identity survives process interruption.",
        "reason": (
            "The Pydantic AI DBOS lane now has deterministic retry and resume smoke evidence, so the next useful "
            "slice is preserving run identity across interruption."
        ),
    }


def durable_prompt(payload: dict[str, Any]) -> str:
    project_context = payload.get("project_context", {})
    return (
        f"Objective: {payload.get('objective', '')}\n"
        f"Current slice: T004\n"
        f"Active spec: {project_context.get('active_spec', '')}\n"
        "Return the next implementation slice after durable execution smoke evidence."
    )


def build_dbos_workflow(db_path: Path, payload: dict[str, Any]):
    config: DBOSConfig = {
        "name": "pydantic-ai-durable-smoke",
        "system_database_url": f"sqlite:///{db_path}",
        "application_version": "goal-002-durable-smoke",
    }
    DBOS(config=config)

    base_agent = Agent(
        TestModel(custom_output_args=durable_recommendation(), model_name="self-hosted-agents-dbos-fixture"),
        output_type=DecisionRecommendation,
        instructions=(
            "Return the next implementation slice for the Pydantic AI candidate as structured data. "
            "Do not call external services."
        ),
        name="DecisionSliceDBOSAgent",
    )
    durable_agent = DBOSAgent(base_agent, name="DecisionSliceDBOSAgent")

    @DBOS.step(
        name="controlled_retry_once",
        retries_allowed=True,
        interval_seconds=0.1,
        max_attempts=3,
        backoff_rate=1.0,
    )
    def controlled_retry_once(retry_state_log: str, workflow_id: str, failures_before_success: int) -> dict[str, Any]:
        path = Path(retry_state_log)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
        attempt = len(existing) + 1
        will_fail = attempt <= failures_before_success
        event = {
            "attempt": attempt,
            "event": "controlled-retry",
            "will_fail": will_fail,
            "workflow_id": workflow_id,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        if will_fail:
            raise RuntimeError(f"controlled DBOS retry attempt {attempt}")
        return {
            "attempt": attempt,
            "failures_before_success": failures_before_success,
            "line_count_after": len(existing) + 1,
            "line_count_before": len(existing),
            "log_path": retry_state_log,
        }

    @DBOS.step(name="record_side_effect_once")
    def record_side_effect_once(log_path: str, workflow_id: str) -> dict[str, Any]:
        path = Path(log_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
        event = {
            "event": "side-effect",
            "sequence": len(existing) + 1,
            "workflow_id": workflow_id,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        return {
            "event": event,
            "line_count_after": len(existing) + 1,
            "line_count_before": len(existing),
            "log_path": log_path,
        }

    @DBOS.step(name="controlled_resume_wait")
    def controlled_resume_wait(wait_seconds: float) -> dict[str, Any]:
        if os.getenv("PYDANTIC_AI_DBOS_RESUME_READY") == "1":
            return {"resumed": True, "slept_seconds": 0}
        time.sleep(wait_seconds)
        return {"resumed": False, "slept_seconds": wait_seconds}

    @DBOS.workflow(name="pydantic_ai_durable_smoke")
    def pydantic_ai_durable_smoke(
        side_effect_log: str,
        wait_seconds: float,
        side_effect_step_marker: str,
        retry_state_log: str,
        retry_failures: int,
    ) -> dict[str, Any]:
        workflow_id = DBOS.workflow_id or "unknown-workflow"
        retry = controlled_retry_once(retry_state_log, workflow_id, retry_failures)
        side_effect = record_side_effect_once(side_effect_log, workflow_id)
        if side_effect_step_marker:
            marker_path = Path(side_effect_step_marker)
            marker_path.parent.mkdir(parents=True, exist_ok=True)
            marker_path.write_text(
                json.dumps(
                    {
                        "event": "dbos-side-effect-step-returned",
                        "line_count_after": side_effect["line_count_after"],
                        "workflow_id": workflow_id,
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
        wait_result = controlled_resume_wait(wait_seconds)
        agent_result = durable_agent.run_sync(durable_prompt(payload))
        usage = agent_result.usage
        recommendation = agent_result.output.model_dump()
        trace_id = stable_id("trace", {"workflow_id": workflow_id, "recommendation": recommendation}, length=24)
        run_id = stable_id("run", {"workflow_id": workflow_id, "trace_id": trace_id}, length=24)
        return {
            "agent": {
                "class": "pydantic_ai.durable_exec.dbos.DBOSAgent",
                "model": "pydantic_ai.models.test.TestModel",
                "network_required": False,
                "recommendation": recommendation,
                "usage": {
                    "input_tokens": usage.input_tokens,
                    "output_tokens": usage.output_tokens,
                    "requests": usage.requests,
                },
            },
            "pydantic_ai_run_id": run_id,
            "retry": retry,
            "side_effect": side_effect,
            "trace_id": trace_id,
            "wait": wait_result,
            "workflow_id": workflow_id,
        }

    return pydantic_ai_durable_smoke


def serialize_workflow_status(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    data = {key: item for key, item in getattr(value, "__dict__", {}).items() if not key.startswith("_")}
    if not data:
        data = {"status": getattr(value, "status", "")}
    return {key: str(item) if isinstance(item, BaseException) else item for key, item in data.items()}


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, BaseException):
        return str(value)
    return repr(value)


def serialize_steps(steps: list[Any]) -> list[dict[str, Any]]:
    serialized = []
    for step in steps:
        if isinstance(step, dict):
            data = step
        else:
            data = {key: value for key, value in getattr(step, "__dict__", {}).items() if not key.startswith("_")}
        serialized.append(json_safe(data or {"repr": repr(step)}))
    return serialized


def run_child(args: argparse.Namespace) -> int:
    payload = read_json(args.fixture)
    workflow = build_dbos_workflow(args.db_path, payload)
    DBOS.launch()
    if args.child_phase == "start":
        with SetWorkflowID(args.workflow_id):
            handle = DBOS.start_workflow(
                workflow,
                str(args.side_effect_log),
                args.wait_seconds,
                str(args.side_effect_step_marker),
                str(args.retry_state_log),
                args.retry_failures,
            )
        print(json.dumps({"phase": "start", "workflow_id": handle.get_workflow_id()}), flush=True)
        handle.get_result()
        return 0

    handle = DBOS.retrieve_workflow(args.workflow_id)
    result = handle.get_result()
    child_output = {
        "dbos_steps": serialize_steps(DBOS.list_workflow_steps(args.workflow_id)),
        "workflow_result": result,
        "workflow_status": serialize_workflow_status(DBOS.get_workflow_status(args.workflow_id)),
    }
    if args.child_result_output is not None:
        write_json(args.child_result_output, child_output, args.pretty)
    print(json.dumps({"phase": "resume", "workflow_id": args.workflow_id, "status": "complete"}), flush=True)
    return 0


def wait_for_side_effect(path: Path, proc: subprocess.Popen[str], timeout_seconds: float) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if path.exists() and path.read_text(encoding="utf-8").strip():
            return True
        if proc.poll() is not None:
            return False
        time.sleep(0.1)
    return False


def command_text(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def run_parent(args: argparse.Namespace, argv: list[str] | None) -> int:
    payload = read_json(args.fixture)
    output_dir = args.output.parent if args.output is not None else Path(tempfile.mkdtemp())
    output_dir.mkdir(parents=True, exist_ok=True)
    workflow_id = args.workflow_id or stable_id(
        "dbos-workflow",
        {
            "candidate": payload.get("candidate", {}),
            "issue": "awf-4wg",
            "slice": "T025",
            "started_at_ns": time.time_ns(),
        },
        length=24,
    )
    db_path = args.db_path or output_dir / f"{workflow_id}.sqlite"
    side_effect_log = args.side_effect_log or output_dir / f"{workflow_id}.side-effect.jsonl"
    retry_state_log = args.retry_state_log or output_dir / f"{workflow_id}.retry.jsonl"
    side_effect_step_marker = db_path.parent / f"{workflow_id}.side-effect-step-complete.json"
    child_result_output = db_path.parent / f"{workflow_id}.child-result.json"
    script = Path(__file__).resolve()
    base_child = [
        sys.executable,
        str(script),
        "--fixture",
        str(args.fixture),
        "--db-path",
        str(db_path),
        "--side-effect-log",
        str(side_effect_log),
        "--retry-state-log",
        str(retry_state_log),
        "--side-effect-step-marker",
        str(side_effect_step_marker),
        "--workflow-id",
        workflow_id,
        "--wait-seconds",
        str(args.wait_seconds),
        "--retry-failures",
        str(args.retry_failures),
    ]
    first_command = [*base_child, "--child-phase", "start"]
    first_proc = subprocess.Popen(
        first_command,
        cwd=Path(__file__).resolve().parents[2],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    side_effect_seen = wait_for_side_effect(side_effect_step_marker, first_proc, timeout_seconds=20.0)
    first_stdout = ""
    first_stderr = ""
    if side_effect_seen and first_proc.poll() is None:
        first_proc.kill()
    try:
        first_stdout, first_stderr = first_proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        first_proc.kill()
        first_stdout, first_stderr = first_proc.communicate(timeout=10)

    resume_env = os.environ.copy()
    resume_env["PYDANTIC_AI_DBOS_RESUME_READY"] = "1"
    resume_command = [
        *base_child,
        "--child-phase",
        "resume",
        "--child-result-output",
        str(child_result_output),
    ]
    resume_proc = subprocess.run(
        resume_command,
        cwd=Path(__file__).resolve().parents[2],
        text=True,
        capture_output=True,
        env=resume_env,
        timeout=60,
    )
    child_output = read_json(child_result_output) if child_result_output.exists() else {}
    retry_lines = retry_state_log.read_text(encoding="utf-8").splitlines() if retry_state_log.exists() else []
    retry_events = [json.loads(line) for line in retry_lines if line.strip()]
    side_effect_lines = side_effect_log.read_text(encoding="utf-8").splitlines() if side_effect_log.exists() else []
    side_effect_events = [json.loads(line) for line in side_effect_lines if line.strip()]
    workflow_result = child_output.get("workflow_result", {})
    retry_failures = [event for event in retry_events if event.get("will_fail") is True]
    retry_successes = [event for event in retry_events if event.get("will_fail") is False]
    retry_proven = (
        resume_proc.returncode == 0
        and bool(workflow_result)
        and len(retry_failures) == args.retry_failures
        and len(retry_successes) == 1
        and workflow_result.get("retry", {}).get("attempt") == args.retry_failures + 1
    )
    artifact = {
        "acceptance_command": "uv run awf workflow-fixture-test",
        "candidate_app": "apps/pydantic-ai",
        "command_used": command_text(
            ["uv", "run", "python", "apps/pydantic-ai/durable_smoke.py", *(argv if argv is not None else sys.argv[1:])]
        ),
        "dbos": {
            "db_path": str(db_path),
            "side_effect_step_marker": str(side_effect_step_marker),
            "system_database_url": f"sqlite:///{db_path}",
            "workflow_id": workflow_id,
            "workflow_status": child_output.get("workflow_status", {}),
            "workflow_steps": child_output.get("dbos_steps", []),
        },
        "deterministic_validation": {
            "external_model_required": False,
            "hosted_credentials_required": False,
            "service_count": 0,
        },
        "durable_property": {
            "completed_step_not_duplicated": len(side_effect_events) == 1,
            "controlled_failure": "first child process killed after DBOS side-effect step returned",
            "controlled_retry": (
                f"DBOS step controlled_retry_once failed {args.retry_failures} time(s), then retried and completed"
            ),
            "retry_proven": retry_proven,
            "resume_proven": resume_proc.returncode == 0 and bool(workflow_result),
        },
        "first_attempt": {
            "command": command_text(first_command),
            "exit_code": first_proc.returncode,
            "side_effect_step_returned_before_kill": side_effect_seen,
            "stderr_excerpt": first_stderr[-1000:],
            "stdout_excerpt": first_stdout[-1000:],
        },
        "issue_id": args.issue_id,
        "pydantic_ai": {
            "agent_class": workflow_result.get("agent", {}).get("class"),
            "model_class": workflow_result.get("agent", {}).get("model"),
            "network_required": workflow_result.get("agent", {}).get("network_required"),
            "recommendation": workflow_result.get("agent", {}).get("recommendation", {}),
            "run_id": workflow_result.get("pydantic_ai_run_id", ""),
            "trace_id": workflow_result.get("trace_id", ""),
        },
        "resume_attempt": {
            "command": command_text(resume_command),
            "exit_code": resume_proc.returncode,
            "stderr_excerpt": resume_proc.stderr[-1000:],
            "stdout_excerpt": resume_proc.stdout[-1000:],
        },
        "retry": {
            "events": retry_events,
            "failure_count": len(retry_failures),
            "line_count": len(retry_events),
            "log_path": str(retry_state_log),
            "success_count": len(retry_successes),
        },
        "runtime": {
            "selected": "pydantic_ai_dbos",
            "sqlite_development_mode": True,
        },
        "side_effect": {
            "events": side_effect_events,
            "line_count": len(side_effect_events),
            "log_path": str(side_effect_log),
        },
    }
    first_exit_code = artifact["first_attempt"]["exit_code"]
    artifact["passed"] = (
        artifact["durable_property"]["completed_step_not_duplicated"]
        and artifact["durable_property"]["retry_proven"]
        and artifact["durable_property"]["resume_proven"]
        and artifact["first_attempt"]["side_effect_step_returned_before_kill"]
        and first_exit_code is not None
        and first_exit_code != 0
        and artifact["pydantic_ai"]["agent_class"] == "pydantic_ai.durable_exec.dbos.DBOSAgent"
        and artifact["pydantic_ai"]["network_required"] is False
        and artifact["resume_attempt"]["exit_code"] == 0
    )
    if args.output is not None:
        write_json(args.output, artifact, args.pretty)
    print(json.dumps(artifact, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if artifact["passed"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Pydantic AI DBOS durable smoke proof.")
    parser.add_argument("--fixture", required=True, type=Path, help="Shared comparison fixture JSON path.")
    parser.add_argument("--output", type=Path, help="Optional durable evidence output path.")
    parser.add_argument("--db-path", type=Path, help="Optional local SQLite DBOS system database path.")
    parser.add_argument("--side-effect-log", type=Path, help="Optional side-effect proof log path.")
    parser.add_argument("--retry-state-log", type=Path, help="Optional controlled retry proof log path.")
    parser.add_argument("--retry-failures", type=int, default=1, help="Transient DBOS retry failures before success.")
    parser.add_argument("--issue-id", default="awf-x3q", help="Beads issue id linked to the durable evidence.")
    parser.add_argument("--side-effect-step-marker", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--workflow-id", help="Optional deterministic DBOS workflow id.")
    parser.add_argument("--wait-seconds", type=float, default=300.0, help="Child wait duration before resume.")
    parser.add_argument("--child-phase", choices=["start", "resume"], help=argparse.SUPPRESS)
    parser.add_argument("--child-result-output", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.child_phase:
        return run_child(args)
    return run_parent(args, argv)


if __name__ == "__main__":
    raise SystemExit(main())
