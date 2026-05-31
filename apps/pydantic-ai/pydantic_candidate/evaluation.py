from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext

from .trace import stable_id


def captured_json_artifact(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    normalized = value.strip()
    return not normalized.startswith("provided by ") and normalized.endswith(".json")


@dataclass
class ComparableWorkflowEvaluator(Evaluator[dict[str, Any], dict[str, Any], dict[str, Any]]):
    def evaluate(self, ctx: EvaluatorContext[dict[str, Any], dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
        output = ctx.output
        evidence_paths = output.get("evidence_paths", {})
        trace = output.get("trace_evidence", {})
        workflow = output.get("workflow", {})
        runtime = workflow.get("pydantic_ai_runtime", {})
        expected_trace_id = str(ctx.metadata.get("trace_id", "")) if ctx.metadata else ""
        expected_run_id = str(ctx.metadata.get("run_id", "")) if ctx.metadata else ""
        expected_linked_task = str(ctx.metadata.get("recommendation_linked_task", "")) if ctx.metadata else ""
        return {
            "recommendation_output": EvaluationReason(
                bool(output.get("recommendation", {}).get("next_slice"))
                and bool(output.get("recommendation", {}).get("reason"))
                and output.get("recommendation", {}).get("linked_task") == expected_linked_task,
                "Recommendation includes the expected next slice and rationale.",
            ),
            "acceptance_check": EvaluationReason(
                output.get("acceptance_check") == "uv run awf workflow-fixture-test",
                "Output names the shared workflow fixture acceptance check.",
            ),
            "run_trace_correlation": EvaluationReason(
                output.get("run_id") == expected_run_id
                and output.get("trace_id") == expected_trace_id
                and trace.get("trace_id") == expected_trace_id,
                "Evaluation case, run artifact, and trace evidence share run and trace ids.",
            ),
            "pydantic_ai_runtime": EvaluationReason(
                runtime.get("agent_class") == "pydantic_ai.Agent"
                and runtime.get("native_otel_span_count", 0) >= 2
                and runtime.get("network_required") is False,
                "Run used Pydantic AI Agent with native OTel spans and no network model requirement.",
            ),
            "evidence_completeness": EvaluationReason(
                bool(evidence_paths.get("fixture_input"))
                and captured_json_artifact(evidence_paths.get("run_artifact"))
                and captured_json_artifact(evidence_paths.get("trace_evidence"))
                and captured_json_artifact(evidence_paths.get("evaluation_evidence"))
                and evidence_paths.get("setup_notes") == "apps/pydantic-ai/README.md"
                and evidence_paths.get("gap_notes") == "apps/pydantic-ai/implementation-plan.md",
                "Run links fixture, run, trace, evaluation, setup, and gap evidence.",
            ),
        }


def compact_report_case(case: Any) -> dict[str, Any]:
    assertions = {}
    for name, result in case.assertions.items():
        assertions[name] = {
            "passed": bool(result.value),
            "reason": result.reason,
            "source": getattr(result.source, "name", str(result.source)),
        }
    return {
        "assertions": assertions,
        "case_id": case.name,
        "output": {
            "candidate_app_id": case.output.get("candidate_app_id"),
            "run_id": case.output.get("run_id"),
            "trace_id": case.output.get("trace_id"),
        },
        "task_duration": case.task_duration,
        "total_duration": case.total_duration,
    }


def evaluate_candidate_run(
    *,
    run_id: str,
    trace_id: str,
    artifact: dict[str, Any],
    rerun_command: str,
    evidence_links: dict[str, str],
) -> dict[str, Any]:
    case_id = "pydantic-ai-comparable-agent-workflow"
    dataset = Dataset(
        name="pydantic-ai-fixture-evaluation",
        cases=[
            Case(
                name=case_id,
                inputs=artifact,
                metadata={
                    "run_id": run_id,
                    "trace_id": trace_id,
                    "linked_task": "T023",
                    "recommendation_linked_task": artifact.get("recommendation", {}).get("linked_task", ""),
                },
            )
        ],
        evaluators=[ComparableWorkflowEvaluator()],
    )
    report = dataset.evaluate_sync(
        lambda inputs: inputs,
        name="pydantic-ai-fixture-evaluation",
        task_name="evaluate_pydantic_ai_run_artifact",
        metadata={
            "candidate_app_id": "pydantic-ai",
            "run_id": run_id,
            "trace_id": trace_id,
            "linked_task": "T023",
        },
        progress=False,
    )
    cases = [compact_report_case(case) for case in report.cases]
    criteria = [
        {"name": name, **result}
        for case in cases
        for name, result in case["assertions"].items()
    ]
    score = sum(1 for item in criteria if item["passed"])
    gaps = [item["reason"] for item in criteria if not item["passed"]]
    passed = score == len(criteria)
    return {
        "case_id": case_id,
        "criteria": criteria,
        "dataset": {
            "case_count": len(report.cases),
            "evaluator_count": len(dataset.evaluators),
            "name": dataset.name,
        },
        "evaluation_id": stable_id(
            "eval",
            {"run_id": run_id, "trace_id": trace_id, "criteria": criteria},
        ),
        "evidence_links": evidence_links,
        "gaps": gaps,
        "max_score": len(criteria),
        "passed": passed,
        "provider": "Pydantic Evals",
        "pydantic_evals": {
            "cases": cases,
            "report_name": report.name,
            "span_id": report.span_id,
            "trace_id": report.trace_id,
        },
        "rerun_command": rerun_command,
        "run_id": run_id,
        "score": score,
        "scorer": {
            "rubric": "docs/evaluation-criteria.md",
            "type": "pydantic-evals-deterministic-assertion",
        },
        "summary": (
            "Pydantic Evals deterministic assertions passed for the comparable workflow artifact."
            if passed
            else "Pydantic Evals deterministic assertions found missing comparable workflow evidence."
        ),
        "trace_id": trace_id,
    }
