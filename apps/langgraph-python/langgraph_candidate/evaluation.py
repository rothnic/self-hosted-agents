from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .trace import stable_id


@dataclass(frozen=True)
class EvaluationResult:
    evaluation_id: str
    run_id: str
    trace_id: str
    case_id: str
    scorer: dict[str, str]
    criteria: list[dict[str, Any]]
    score: int
    max_score: int
    passed: bool
    summary: str
    gaps: list[str]
    rerun_command: str
    evidence_links: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "criteria": self.criteria,
            "evaluation_id": self.evaluation_id,
            "evidence_links": self.evidence_links,
            "gaps": self.gaps,
            "max_score": self.max_score,
            "passed": self.passed,
            "rerun_command": self.rerun_command,
            "run_id": self.run_id,
            "score": self.score,
            "scorer": self.scorer,
            "summary": self.summary,
            "trace_id": self.trace_id,
        }


def evaluate_candidate_run(
    *,
    run_id: str,
    trace_id: str,
    artifact: dict[str, Any],
    rerun_command: str,
    evidence_links: dict[str, str],
) -> EvaluationResult:
    checks = [
        {
            "name": "recommendation_output",
            "passed": bool(artifact.get("recommendation", {}).get("next_slice"))
            and bool(artifact.get("recommendation", {}).get("reason")),
            "expected": "Recommendation includes a next slice and rationale.",
        },
        {
            "name": "alternatives_and_questions",
            "passed": bool(artifact.get("alternatives")) and bool(artifact.get("questions")),
            "expected": "Output includes alternatives and explicit human questions.",
        },
        {
            "name": "acceptance_check",
            "passed": artifact.get("acceptance_check") == "uv run awf workflow-fixture-test",
            "expected": "Output names the shared workflow fixture acceptance check.",
        },
        {
            "name": "trace_correlation",
            "passed": artifact.get("trace_evidence", {}).get("trace_id") == trace_id
            and bool(evidence_links.get("trace_evidence")),
            "expected": "Trace evidence is linked and shares the run trace id.",
        },
        {
            "name": "evidence_completeness",
            "passed": all(
                evidence_links.get(key)
                for key in [
                    "fixture_input",
                    "run_artifact",
                    "trace_evidence",
                    "evaluation_evidence",
                    "setup_notes",
                    "gap_notes",
                ]
            ),
            "expected": "Run links fixture, run, trace, evaluation, setup, and gap evidence.",
        },
    ]
    score = sum(1 for check in checks if check["passed"])
    gaps = [
        check["expected"]
        for check in checks
        if not check["passed"]
    ]
    if not artifact.get("trace_evidence", {}).get("langfuse", {}).get("configured"):
        gaps.append("Langfuse ingestion is not attempted without hosted or self-hosted credentials.")
    if artifact.get("run_mode") == "deterministic-fixture":
        gaps.append("Evaluation is deterministic fixture scoring; model-judge and dataset workflows remain future work.")
    passed = score == len(checks)
    return EvaluationResult(
        evaluation_id=stable_id("eval", {"run_id": run_id, "trace_id": trace_id, "criteria": checks}),
        run_id=run_id,
        trace_id=trace_id,
        case_id="comparable-agent-workflow-decision-slice",
        scorer={
            "type": "deterministic-assertion",
            "rubric": "docs/evaluation-criteria.md",
        },
        criteria=checks,
        score=score,
        max_score=len(checks),
        passed=passed,
        summary=(
            "Deterministic fixture output satisfies the comparable workflow evidence contract."
            if passed
            else "Deterministic fixture output is missing required comparable workflow evidence."
        ),
        gaps=gaps,
        rerun_command=rerun_command,
        evidence_links=evidence_links,
    )
