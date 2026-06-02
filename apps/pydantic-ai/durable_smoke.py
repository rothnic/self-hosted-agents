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
        "linked_task": "T011",
        "next_slice": "Update roadmap, requirements, and promotion gates with the durable proof result.",
        "reason": (
            "The Pydantic AI DBOS lane now has deterministic retry, resume, run identity, and side-effect "
            "idempotency evidence plus fixture-safe review wait, accepted-review continuation, and durable artifact "
            "correlation with fixture shape assertions, so the next useful slice is updating promotion gates."
        ),
    }


def durable_prompt(payload: dict[str, Any]) -> str:
    project_context = payload.get("project_context", {})
    return (
        f"Objective: {payload.get('objective', '')}\n"
        f"Current slice: T010\n"
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

    @DBOS.step(name="record_review_wait_state")
    def record_review_wait_state(
        wait_state_path: str,
        acceptance_path: str,
        post_wait_log: str,
        workflow_id: str,
        issue_id: str,
        required_evidence_path: str,
    ) -> dict[str, Any]:
        wait_state_file = Path(wait_state_path)
        wait_state_file.parent.mkdir(parents=True, exist_ok=True)
        acceptance_file = Path(acceptance_path)
        accepted = acceptance_file.exists()
        state = {
            "acceptance_path": acceptance_path,
            "beads_issue_id": issue_id,
            "event": "review-wait",
            "post_wait_side_effect_log": post_wait_log,
            "post_wait_side_effects_allowed": accepted,
            "required_evidence_path": required_evidence_path,
            "status": "accepted" if accepted else "waiting-for-reviewer-acceptance",
            "workflow_id": workflow_id,
        }
        wait_state_file.write_text(json.dumps(state, sort_keys=True) + "\n", encoding="utf-8")
        return state

    @DBOS.step(name="record_post_wait_side_effect")
    def record_post_wait_side_effect(post_wait_log: str, workflow_id: str) -> dict[str, Any]:
        path = Path(post_wait_log)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
        event = {
            "event": "post-wait-side-effect",
            "sequence": len(existing) + 1,
            "workflow_id": workflow_id,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        return {
            "event": event,
            "line_count_after": len(existing) + 1,
            "line_count_before": len(existing),
            "log_path": post_wait_log,
        }

    @DBOS.workflow(name="pydantic_ai_review_wait_smoke")
    def pydantic_ai_review_wait_smoke(
        wait_state_path: str,
        acceptance_path: str,
        post_wait_log: str,
        issue_id: str,
        required_evidence_path: str,
    ) -> dict[str, Any]:
        workflow_id = DBOS.workflow_id or "unknown-workflow"
        wait_state = record_review_wait_state(
            wait_state_path,
            acceptance_path,
            post_wait_log,
            workflow_id,
            issue_id,
            required_evidence_path,
        )
        if wait_state["status"] != "accepted":
            return {
                "post_wait_side_effect": {"skipped": True, "reason": "reviewer acceptance missing"},
                "review_wait": wait_state,
                "workflow_id": workflow_id,
            }
        post_wait_side_effect = record_post_wait_side_effect(post_wait_log, workflow_id)
        return {
            "post_wait_side_effect": post_wait_side_effect,
            "review_wait": wait_state,
            "workflow_id": workflow_id,
        }

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

    pydantic_ai_durable_smoke.review_wait_workflow = pydantic_ai_review_wait_smoke
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

    if args.child_phase == "review-wait":
        review_wait_workflow = getattr(workflow, "review_wait_workflow")
        with SetWorkflowID(args.workflow_id):
            handle = DBOS.start_workflow(
                review_wait_workflow,
                str(args.review_wait_state),
                str(args.review_acceptance),
                str(args.post_wait_side_effect_log),
                args.issue_id,
                args.required_review_evidence_path,
            )
        result = handle.get_result()
        child_output = {
            "dbos_steps": serialize_steps(DBOS.list_workflow_steps(args.workflow_id)),
            "workflow_result": result,
            "workflow_status": serialize_workflow_status(DBOS.get_workflow_status(args.workflow_id)),
        }
        if args.child_result_output is not None:
            write_json(args.child_result_output, child_output, args.pretty)
        print(
            json.dumps(
                {
                    "phase": "review-wait",
                    "status": result.get("review_wait", {}).get("status"),
                    "workflow_id": args.workflow_id,
                }
            ),
            flush=True,
        )
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


def parse_child_stdout(stdout: str) -> dict[str, Any]:
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("workflow_id"):
            return value
    return {}


def workflow_ids_from_events(events: list[dict[str, Any]]) -> list[str]:
    return sorted({str(event.get("workflow_id", "")) for event in events if event.get("workflow_id")})


def read_jsonl_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_review_acceptance_artifact(
    path: Path,
    *,
    issue_id: str,
    required_evidence_path: str,
    reviewer_agent_id: str,
    workflow_id: str,
    pretty: bool,
) -> dict[str, Any]:
    artifact = {
        "accepted": True,
        "accepted_at": "fixture-deterministic-review-acceptance",
        "beads_issue_id": issue_id,
        "decision": "accepted",
        "event": "independent-reviewer-acceptance",
        "presented_by_agent_id": "fixture-worker-presenter",
        "required_evidence_path": required_evidence_path,
        "reviewer_agent_id": reviewer_agent_id,
        "workflow_id": workflow_id,
    }
    write_json(path, artifact, pretty)
    return artifact


def side_effect_event_keys(events: list[dict[str, Any]]) -> list[str]:
    return sorted(
        f"{event.get('workflow_id', '')}:{event.get('event', '')}:{event.get('sequence', '')}" for event in events
    )


def run_parent(args: argparse.Namespace, argv: list[str] | None) -> int:
    payload = read_json(args.fixture)
    output_dir = args.output.parent if args.output is not None else Path(tempfile.mkdtemp())
    output_dir.mkdir(parents=True, exist_ok=True)
    workflow_id = args.workflow_id or stable_id(
        "dbos-workflow",
        {
            "candidate": payload.get("candidate", {}),
            "issue": args.issue_id,
            "slice": "T010",
            "started_at_ns": time.time_ns(),
        },
        length=24,
    )
    db_path = args.db_path or output_dir / f"{workflow_id}.sqlite"
    side_effect_log = args.side_effect_log or output_dir / f"{workflow_id}.side-effect.jsonl"
    retry_state_log = args.retry_state_log or output_dir / f"{workflow_id}.retry.jsonl"
    side_effect_step_marker = db_path.parent / f"{workflow_id}.side-effect-step-complete.json"
    child_result_output = db_path.parent / f"{workflow_id}.child-result.json"
    review_wait_workflow_id = f"{workflow_id}-review-wait"
    review_wait_state = args.review_wait_state or output_dir / f"{review_wait_workflow_id}.review-wait.json"
    review_acceptance = args.review_acceptance or output_dir / f"{review_wait_workflow_id}.review-acceptance.json"
    post_wait_side_effect_log = (
        args.post_wait_side_effect_log or output_dir / f"{review_wait_workflow_id}.post-wait-side-effect.jsonl"
    )
    required_review_evidence_path = (
        args.required_review_evidence_path
        or f".agent-runs/reviews/{args.issue_id}-{review_wait_workflow_id}-acceptance.json"
    )
    review_child_result_output = db_path.parent / f"{review_wait_workflow_id}.child-result.json"
    accepted_review_workflow_id = f"{workflow_id}-review-accepted"
    accepted_review_wait_state = (
        args.accepted_review_wait_state or output_dir / f"{accepted_review_workflow_id}.review-wait.json"
    )
    accepted_review_acceptance = (
        args.accepted_review_acceptance or output_dir / f"{accepted_review_workflow_id}.review-acceptance.json"
    )
    accepted_post_wait_side_effect_log = (
        args.accepted_post_wait_side_effect_log
        or output_dir / f"{accepted_review_workflow_id}.post-wait-side-effect.jsonl"
    )
    accepted_required_review_evidence_path = (
        args.accepted_required_review_evidence_path
        or f".agent-runs/reviews/{args.issue_id}-{accepted_review_workflow_id}-acceptance.json"
    )
    accepted_review_child_result_output = db_path.parent / f"{accepted_review_workflow_id}.child-result.json"
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
        "--issue-id",
        args.issue_id,
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

    retry_events_before_resume = read_jsonl_events(retry_state_log)
    side_effect_events_before_resume = read_jsonl_events(side_effect_log)
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
    review_wait_command = [
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
        "--workflow-id",
        review_wait_workflow_id,
        "--wait-seconds",
        str(args.wait_seconds),
        "--retry-failures",
        str(args.retry_failures),
        "--issue-id",
        args.issue_id,
        "--review-wait-state",
        str(review_wait_state),
        "--review-acceptance",
        str(review_acceptance),
        "--post-wait-side-effect-log",
        str(post_wait_side_effect_log),
        "--required-review-evidence-path",
        required_review_evidence_path,
        "--child-phase",
        "review-wait",
        "--child-result-output",
        str(review_child_result_output),
    ]
    review_wait_proc = subprocess.run(
        review_wait_command,
        cwd=Path(__file__).resolve().parents[2],
        text=True,
        capture_output=True,
        timeout=60,
    )
    accepted_review_acceptance_data = write_review_acceptance_artifact(
        accepted_review_acceptance,
        issue_id=args.issue_id,
        required_evidence_path=accepted_required_review_evidence_path,
        reviewer_agent_id="fixture-independent-reviewer",
        workflow_id=accepted_review_workflow_id,
        pretty=args.pretty,
    )
    accepted_review_wait_command = [
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
        "--workflow-id",
        accepted_review_workflow_id,
        "--wait-seconds",
        str(args.wait_seconds),
        "--retry-failures",
        str(args.retry_failures),
        "--issue-id",
        args.issue_id,
        "--review-wait-state",
        str(accepted_review_wait_state),
        "--review-acceptance",
        str(accepted_review_acceptance),
        "--post-wait-side-effect-log",
        str(accepted_post_wait_side_effect_log),
        "--required-review-evidence-path",
        accepted_required_review_evidence_path,
        "--child-phase",
        "review-wait",
        "--child-result-output",
        str(accepted_review_child_result_output),
    ]
    accepted_review_wait_proc = subprocess.run(
        accepted_review_wait_command,
        cwd=Path(__file__).resolve().parents[2],
        text=True,
        capture_output=True,
        timeout=60,
    )
    child_output = read_json(child_result_output) if child_result_output.exists() else {}
    review_child_output = read_json(review_child_result_output) if review_child_result_output.exists() else {}
    accepted_review_child_output = (
        read_json(accepted_review_child_result_output) if accepted_review_child_result_output.exists() else {}
    )
    retry_events = read_jsonl_events(retry_state_log)
    side_effect_events = read_jsonl_events(side_effect_log)
    post_wait_side_effect_events = read_jsonl_events(post_wait_side_effect_log)
    accepted_post_wait_side_effect_events = read_jsonl_events(accepted_post_wait_side_effect_log)
    workflow_result = child_output.get("workflow_result", {})
    review_wait_result = review_child_output.get("workflow_result", {})
    accepted_review_wait_result = accepted_review_child_output.get("workflow_result", {})
    review_wait_state_data = read_json(review_wait_state) if review_wait_state.exists() else {}
    accepted_review_wait_state_data = read_json(accepted_review_wait_state) if accepted_review_wait_state.exists() else {}
    retry_failures = [event for event in retry_events if event.get("will_fail") is True]
    retry_successes = [event for event in retry_events if event.get("will_fail") is False]
    retry_failures_before_resume = [event for event in retry_events_before_resume if event.get("will_fail") is True]
    retry_successes_before_resume = [event for event in retry_events_before_resume if event.get("will_fail") is False]
    workflow_result_side_effect = workflow_result.get("side_effect", {})
    first_identity = parse_child_stdout(first_stdout)
    resume_identity = parse_child_stdout(resume_proc.stdout)
    workflow_status = child_output.get("workflow_status", {})
    status_output = workflow_status.get("output", {}) if isinstance(workflow_status.get("output"), dict) else {}
    identity = {
        "first_attempt_phase": first_identity.get("phase", ""),
        "first_attempt_workflow_id": first_identity.get("workflow_id", ""),
        "requested_workflow_id": workflow_id,
        "resume_attempt_phase": resume_identity.get("phase", ""),
        "resume_attempt_status": resume_identity.get("status", ""),
        "resume_attempt_workflow_id": resume_identity.get("workflow_id", ""),
        "retry_event_workflow_ids": workflow_ids_from_events(retry_events),
        "side_effect_event_workflow_ids": workflow_ids_from_events(side_effect_events),
        "workflow_result_workflow_id": workflow_result.get("workflow_id", ""),
        "workflow_status_workflow_id": workflow_status.get("workflow_id", ""),
        "workflow_status_output_workflow_id": status_output.get("workflow_id", ""),
    }
    identity_values = [
        identity["first_attempt_workflow_id"],
        identity["requested_workflow_id"],
        identity["resume_attempt_workflow_id"],
        identity["workflow_result_workflow_id"],
        identity["workflow_status_workflow_id"],
        identity["workflow_status_output_workflow_id"],
        *identity["retry_event_workflow_ids"],
        *identity["side_effect_event_workflow_ids"],
    ]
    identity_proven = (
        resume_proc.returncode == 0
        and bool(workflow_result)
        and identity["first_attempt_phase"] == "start"
        and identity["resume_attempt_phase"] == "resume"
        and identity["resume_attempt_status"] == "complete"
        and all(value == workflow_id for value in identity_values)
    )
    retry_proven = (
        resume_proc.returncode == 0
        and bool(workflow_result)
        and len(retry_failures) == args.retry_failures
        and len(retry_successes) == 1
        and workflow_result.get("retry", {}).get("attempt") == args.retry_failures + 1
    )
    side_effect_idempotency_proven = (
        retry_proven
        and len(retry_failures_before_resume) == args.retry_failures
        and len(retry_successes_before_resume) == 1
        and len(side_effect_events_before_resume) == 1
        and len(side_effect_events) == 1
        and side_effect_events == side_effect_events_before_resume
        and workflow_result_side_effect.get("line_count_before") == 0
        and workflow_result_side_effect.get("line_count_after") == 1
        and workflow_result_side_effect.get("event") == side_effect_events[0]
    )
    side_effect_idempotency = {
        "after_resume_line_count": len(side_effect_events),
        "before_resume_line_count": len(side_effect_events_before_resume),
        "event_keys": side_effect_event_keys(side_effect_events),
        "events_unchanged_after_resume": side_effect_events == side_effect_events_before_resume,
        "proven": side_effect_idempotency_proven,
        "resume_duplicate_count": max(len(side_effect_events) - len(side_effect_events_before_resume), 0),
        "retry_failure_count_before_side_effect": len(retry_failures_before_resume),
        "retry_line_count_before_side_effect": len(retry_events_before_resume),
        "retry_success_count_before_side_effect": len(retry_successes_before_resume),
        "workflow_result_event_matches_log": workflow_result_side_effect.get("event") == (
            side_effect_events[0] if side_effect_events else {}
        ),
        "workflow_result_line_count_after": workflow_result_side_effect.get("line_count_after"),
        "workflow_result_line_count_before": workflow_result_side_effect.get("line_count_before"),
    }
    review_wait_workflow_status = review_child_output.get("workflow_status", {})
    review_wait_proven = (
        review_wait_proc.returncode == 0
        and review_wait_result.get("review_wait", {}).get("status") == "waiting-for-reviewer-acceptance"
        and review_wait_state_data.get("status") == "waiting-for-reviewer-acceptance"
        and review_wait_state_data.get("workflow_id") == review_wait_workflow_id
        and review_wait_state_data.get("beads_issue_id") == args.issue_id
        and review_wait_state_data.get("required_evidence_path") == required_review_evidence_path
        and review_wait_state_data.get("post_wait_side_effects_allowed") is False
        and not review_acceptance.exists()
        and len(post_wait_side_effect_events) == 0
        and review_wait_result.get("post_wait_side_effect", {}).get("skipped") is True
    )
    accepted_review_workflow_status = accepted_review_child_output.get("workflow_status", {})
    accepted_post_wait_side_effect = accepted_review_wait_result.get("post_wait_side_effect", {})
    accepted_post_wait_event = accepted_post_wait_side_effect_events[0] if accepted_post_wait_side_effect_events else {}
    accepted_review_resume_proven = (
        accepted_review_wait_proc.returncode == 0
        and accepted_review_acceptance.exists()
        and accepted_review_acceptance_data.get("accepted") is True
        and bool(accepted_review_acceptance_data.get("reviewer_agent_id"))
        and accepted_review_acceptance_data.get("workflow_id") == accepted_review_workflow_id
        and accepted_review_acceptance_data.get("beads_issue_id") == args.issue_id
        and accepted_review_acceptance_data.get("required_evidence_path") == accepted_required_review_evidence_path
        and accepted_review_wait_result.get("review_wait", {}).get("status") == "accepted"
        and accepted_review_wait_result.get("workflow_id") == accepted_review_workflow_id
        and accepted_review_wait_state_data.get("status") == "accepted"
        and accepted_review_wait_state_data.get("workflow_id") == accepted_review_workflow_id
        and accepted_review_wait_state_data.get("beads_issue_id") == args.issue_id
        and accepted_review_wait_state_data.get("required_evidence_path") == accepted_required_review_evidence_path
        and accepted_review_wait_state_data.get("post_wait_side_effects_allowed") is True
        and len(accepted_post_wait_side_effect_events) == 1
        and accepted_post_wait_side_effect.get("line_count_before") == 0
        and accepted_post_wait_side_effect.get("line_count_after") == 1
        and accepted_post_wait_side_effect.get("event") == accepted_post_wait_event
        and accepted_post_wait_event.get("workflow_id") == accepted_review_workflow_id
    )
    pydantic_run_id = workflow_result.get("pydantic_ai_run_id", "")
    trace_id = workflow_result.get("trace_id", "")
    evaluation_id = stable_id(
        "eval",
        {
            "accepted_review_workflow_id": accepted_review_workflow_id,
            "issue_id": args.issue_id,
            "pydantic_ai_run_id": pydantic_run_id,
            "task_id": "T010",
            "trace_id": trace_id,
            "workflow_id": workflow_id,
        },
    )
    artifact_output_path = str(args.output) if args.output is not None else ""
    correlation_proven = (
        bool(pydantic_run_id)
        and bool(trace_id)
        and evaluation_id.startswith("eval-")
        and identity_proven
        and review_wait_state_data.get("workflow_id") == review_wait_workflow_id
        and review_wait_state_data.get("beads_issue_id") == args.issue_id
        and accepted_review_acceptance_data.get("reviewer_agent_id") == "fixture-independent-reviewer"
        and accepted_review_acceptance_data.get("workflow_id") == accepted_review_workflow_id
        and accepted_review_acceptance_data.get("beads_issue_id") == args.issue_id
        and accepted_review_wait_state_data.get("workflow_id") == accepted_review_workflow_id
        and accepted_review_wait_state_data.get("beads_issue_id") == args.issue_id
        and accepted_post_wait_event.get("workflow_id") == accepted_review_workflow_id
    )
    artifact = {
        "acceptance_command": "uv run awf workflow-fixture-test",
        "candidate_app": "apps/pydantic-ai",
        "command_used": command_text(
            ["uv", "run", "python", "apps/pydantic-ai/durable_smoke.py", *(argv if argv is not None else sys.argv[1:])]
        ),
        "correlation": {
            "accepted_review_resume": {
                "post_wait_event_workflow_id": accepted_post_wait_event.get("workflow_id", ""),
                "post_wait_side_effect_log": str(accepted_post_wait_side_effect_log),
                "state_path": str(accepted_review_wait_state),
                "workflow_id": accepted_review_workflow_id,
            },
            "beads": {
                "acceptance_command": "uv run awf workflow-fixture-test",
                "beads_issue_id": args.issue_id,
                "evidence_artifact": artifact_output_path,
                "external_ref": "specs/004-durable-agent-execution-runtime/tasks.md#T010",
                "objective_id": "agentic-development-foundation",
                "spec_id": "004-durable-agent-execution-runtime",
                "task_id": "T010",
            },
            "durable_run": {
                "durable_run_id": workflow_id,
                "resume_attempt_workflow_id": identity.get("resume_attempt_workflow_id", ""),
                "workflow_result_workflow_id": identity.get("workflow_result_workflow_id", ""),
                "workflow_status_workflow_id": identity.get("workflow_status_workflow_id", ""),
            },
            "evaluation": {
                "evaluation_id": evaluation_id,
                "provider": "deterministic-fixture-correlation",
                "run_id": pydantic_run_id,
                "trace_id": trace_id,
            },
            "observability": {
                "pydantic_ai_run_id": pydantic_run_id,
                "trace_id": trace_id,
            },
            "proven": correlation_proven,
            "review_wait": {
                "required_evidence_path": required_review_evidence_path,
                "state_path": str(review_wait_state),
                "workflow_id": review_wait_workflow_id,
            },
            "reviewer_acceptance": {
                "acceptance_path": str(accepted_review_acceptance),
                "accepted": accepted_review_acceptance_data.get("accepted", False),
                "required_evidence_path": accepted_required_review_evidence_path,
                "reviewer_agent_id": accepted_review_acceptance_data.get("reviewer_agent_id", ""),
                "workflow_id": accepted_review_acceptance_data.get("workflow_id", ""),
            },
        },
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
            "artifact_correlation_proven": correlation_proven,
            "run_identity_preserved": identity_proven,
            "retry_proven": retry_proven,
            "review_wait_proven": review_wait_proven,
            "review_resume_proven": accepted_review_resume_proven,
            "resume_proven": resume_proc.returncode == 0 and bool(workflow_result),
            "side_effect_idempotency_proven": side_effect_idempotency_proven,
        },
        "first_attempt": {
            "command": command_text(first_command),
            "exit_code": first_proc.returncode,
            "side_effect_step_returned_before_kill": side_effect_seen,
            "stderr_excerpt": first_stderr[-1000:],
            "stdout_excerpt": first_stdout[-1000:],
        },
        "identity": identity,
        "issue_id": args.issue_id,
        "pydantic_ai": {
            "agent_class": workflow_result.get("agent", {}).get("class"),
            "model_class": workflow_result.get("agent", {}).get("model"),
            "network_required": workflow_result.get("agent", {}).get("network_required"),
            "recommendation": workflow_result.get("agent", {}).get("recommendation", {}),
            "run_id": pydantic_run_id,
            "trace_id": trace_id,
        },
        "resume_attempt": {
            "command": command_text(resume_command),
            "exit_code": resume_proc.returncode,
            "stderr_excerpt": resume_proc.stderr[-1000:],
            "stdout_excerpt": resume_proc.stdout[-1000:],
        },
        "review_wait": {
            "acceptance_artifact_exists": review_acceptance.exists(),
            "acceptance_path": str(review_acceptance),
            "beads_issue_id": args.issue_id,
            "command": command_text(review_wait_command),
            "exit_code": review_wait_proc.returncode,
            "post_wait_side_effect": {
                "events": post_wait_side_effect_events,
                "line_count": len(post_wait_side_effect_events),
                "log_path": str(post_wait_side_effect_log),
            },
            "proven": review_wait_proven,
            "required_evidence_path": required_review_evidence_path,
            "state": review_wait_state_data,
            "state_path": str(review_wait_state),
            "stderr_excerpt": review_wait_proc.stderr[-1000:],
            "stdout_excerpt": review_wait_proc.stdout[-1000:],
            "workflow_id": review_wait_workflow_id,
            "workflow_result": review_wait_result,
            "workflow_status": review_wait_workflow_status,
            "workflow_steps": review_child_output.get("dbos_steps", []),
        },
        "accepted_review_resume": {
            "acceptance": accepted_review_acceptance_data,
            "acceptance_artifact_exists": accepted_review_acceptance.exists(),
            "acceptance_path": str(accepted_review_acceptance),
            "beads_issue_id": args.issue_id,
            "command": command_text(accepted_review_wait_command),
            "exit_code": accepted_review_wait_proc.returncode,
            "post_wait_side_effect": {
                "events": accepted_post_wait_side_effect_events,
                "line_count": len(accepted_post_wait_side_effect_events),
                "log_path": str(accepted_post_wait_side_effect_log),
            },
            "proven": accepted_review_resume_proven,
            "required_evidence_path": accepted_required_review_evidence_path,
            "state": accepted_review_wait_state_data,
            "state_path": str(accepted_review_wait_state),
            "stderr_excerpt": accepted_review_wait_proc.stderr[-1000:],
            "stdout_excerpt": accepted_review_wait_proc.stdout[-1000:],
            "workflow_id": accepted_review_workflow_id,
            "workflow_result": accepted_review_wait_result,
            "workflow_status": accepted_review_workflow_status,
            "workflow_steps": accepted_review_child_output.get("dbos_steps", []),
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
            "idempotency": side_effect_idempotency,
            "line_count": len(side_effect_events),
            "log_path": str(side_effect_log),
        },
    }
    first_exit_code = artifact["first_attempt"]["exit_code"]
    artifact["passed"] = (
        artifact["durable_property"]["completed_step_not_duplicated"]
        and artifact["durable_property"]["artifact_correlation_proven"]
        and artifact["durable_property"]["run_identity_preserved"]
        and artifact["durable_property"]["retry_proven"]
        and artifact["durable_property"]["review_resume_proven"]
        and artifact["durable_property"]["review_wait_proven"]
        and artifact["durable_property"]["resume_proven"]
        and artifact["durable_property"]["side_effect_idempotency_proven"]
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
    parser.add_argument("--review-wait-state", type=Path, help="Optional review-wait state JSON path.")
    parser.add_argument("--review-acceptance", type=Path, help="Optional reviewer acceptance artifact path.")
    parser.add_argument("--post-wait-side-effect-log", type=Path, help="Optional post-review side-effect proof log path.")
    parser.add_argument("--accepted-review-wait-state", type=Path, help="Optional accepted-review state JSON path.")
    parser.add_argument("--accepted-review-acceptance", type=Path, help="Optional accepted reviewer artifact path.")
    parser.add_argument(
        "--accepted-post-wait-side-effect-log",
        type=Path,
        help="Optional accepted-review post-wait side-effect proof log path.",
    )
    parser.add_argument(
        "--required-review-evidence-path",
        help="Reviewer evidence path the review-wait proof records as required before resume.",
    )
    parser.add_argument(
        "--accepted-required-review-evidence-path",
        help="Reviewer evidence path the accepted-review resume proof links before post-wait continuation.",
    )
    parser.add_argument("--retry-failures", type=int, default=1, help="Transient DBOS retry failures before success.")
    parser.add_argument("--issue-id", default="awf-75o", help="Beads issue id linked to the durable evidence.")
    parser.add_argument("--side-effect-step-marker", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--workflow-id", help="Optional deterministic DBOS workflow id.")
    parser.add_argument("--wait-seconds", type=float, default=300.0, help="Child wait duration before resume.")
    parser.add_argument("--child-phase", choices=["start", "resume", "review-wait"], help=argparse.SUPPRESS)
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
