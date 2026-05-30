from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .trace import stable_id


FUNCTIONAL_NEEDS = [
    {
        "area": "Agent orchestration",
        "provider": "Pydantic AI typed agent and structured output boundary",
        "first_slice_status": "scaffolded",
    },
    {
        "area": "Tool and context access",
        "provider": "Typed fixture-backed dependencies for project context",
        "first_slice_status": "scaffolded",
    },
    {
        "area": "Observability",
        "provider": "Logfire plus portable OpenTelemetry export",
        "first_slice_status": "planned-for-T022",
    },
    {
        "area": "Evaluation",
        "provider": "Pydantic Evals with deterministic assertions",
        "first_slice_status": "planned-for-T023",
    },
    {
        "area": "Durable execution",
        "provider": "DBOS, Prefect, Restate, Temporal, or Hatchet comparison",
        "first_slice_status": "planned-for-T024",
    },
]


@dataclass(frozen=True)
class Candidate:
    id: str = "pydantic-ai"
    stack: list[str] = field(default_factory=lambda: ["Pydantic AI", "Logfire/OpenTelemetry"])


@dataclass(frozen=True)
class ProjectContext:
    active_spec: str = ""
    comparison_contract: str = ""
    current_slice: str = "T021"
    next_expected_slice: str = "T022"
    previous_candidate: str = "langgraph-python"


@dataclass(frozen=True)
class FixturePayload:
    objective: str
    candidate: Candidate = field(default_factory=Candidate)
    constraints: list[str] = field(default_factory=list)
    project_context: ProjectContext = field(default_factory=ProjectContext)


@dataclass(frozen=True)
class CandidateRun:
    acceptance_check: str
    alternatives: list[dict[str, str]]
    candidate_app_id: str
    evaluation_output: dict[str, Any]
    evidence_paths: dict[str, str]
    gaps: list[str]
    questions: list[str]
    recommendation: dict[str, str]
    run_id: str
    run_mode: str
    stack: list[str]
    trace_evidence: dict[str, Any]
    trace_id: str
    workflow: dict[str, Any]
    command_used: str = "provided by CLI"

    def to_dict(self) -> dict[str, Any]:
        return {
            "acceptance_check": self.acceptance_check,
            "alternatives": self.alternatives,
            "candidate_app_id": self.candidate_app_id,
            "command_used": self.command_used,
            "evaluation_output": self.evaluation_output,
            "evidence_paths": self.evidence_paths,
            "gaps": self.gaps,
            "questions": self.questions,
            "recommendation": self.recommendation,
            "run_id": self.run_id,
            "run_mode": self.run_mode,
            "stack": self.stack,
            "trace_evidence": self.trace_evidence,
            "trace_id": self.trace_id,
            "workflow": self.workflow,
        }


class DecisionSliceAgentScaffold:
    def __init__(self, payload: FixturePayload) -> None:
        self.payload = payload
        self.steps: list[str] = []

    def load_context(self) -> None:
        self.steps.append("load_typed_fixture_context")

    def map_functional_needs(self) -> None:
        self.steps.append("map_pydantic_ai_functional_needs")

    def select_next_slice(self) -> dict[str, str]:
        self.steps.append("select_next_slice")
        linked_task = self.payload.project_context.next_expected_slice or "T022"
        return {
            "next_slice": "Add hosted Logfire and OpenTelemetry trace evidence for the Pydantic AI slice.",
            "reason": (
                "The deterministic scaffold now proves the Pydantic AI lane can accept the shared comparison input "
                "and return structured decision output, so the next useful slice is live observability evidence."
            ),
            "linked_task": linked_task,
        }

    def format_run(self, recommendation: dict[str, str]) -> CandidateRun:
        self.steps.append("format_structured_run_artifact")
        candidate_data = {"id": self.payload.candidate.id, "stack": self.payload.candidate.stack}
        trace_id = stable_id(
            "trace",
            {
                "candidate": candidate_data,
                "objective": self.payload.objective,
                "steps": self.steps,
            },
            length=24,
        )
        run_id = stable_id(
            "run",
            {
                "candidate": candidate_data,
                "recommendation": recommendation,
                "trace_id": trace_id,
            },
            length=24,
        )
        return CandidateRun(
            acceptance_check="uv run awf workflow-fixture-test",
            alternatives=[
                {
                    "option": "Add Pydantic Evals before hosted telemetry",
                    "tradeoff": "Useful scoring path, but it would not satisfy the Logfire evidence dependency.",
                },
                {
                    "option": "Compare durable runtimes immediately",
                    "tradeoff": "Useful architecture research, but it should evaluate the actual runnable candidate lane.",
                },
            ],
            candidate_app_id=self.payload.candidate.id,
            evaluation_output={
                "status": "planned",
                "linked_task": "T023",
                "provider": "Pydantic Evals",
                "gaps": [
                    "No Pydantic Evals dataset, scorer, or serialized report is emitted by the T021 scaffold.",
                ],
            },
            evidence_paths={
                "fixture_input": "packages/comparison/fixtures/pydantic-ai-decision-slice.json",
                "run_artifact": "provided by --output",
                "setup_notes": "apps/pydantic-ai/README.md",
                "gap_notes": "apps/pydantic-ai/implementation-plan.md",
            },
            gaps=[
                "Hosted Logfire telemetry is not sent in deterministic fixture mode and remains T022 evidence.",
                "Repo-local OpenTelemetry export shape is planned for T022 after the runnable lane exists.",
                "Pydantic Evals output is planned for T023 and is not represented as passing implementation evidence.",
                "Durable runtime selection and smoke proof remain T024 and T025 work.",
            ],
            questions=[
                "Which hosted Logfire project should receive the first live Pydantic AI telemetry evidence?",
            ],
            recommendation=recommendation,
            run_id=run_id,
            run_mode="deterministic-fixture",
            stack=self.payload.candidate.stack,
            trace_evidence={
                "status": "planned",
                "linked_task": "T022",
                "provider": "Logfire/OpenTelemetry",
                "trace_id": trace_id,
                "instrumentation_target": "Pydantic AI OpenTelemetry instrumentation",
                "hosted_logfire_configured": False,
                "gaps": [
                    "No hosted Logfire run is emitted by the T021 scaffold.",
                    "No local OTLP or trace JSON export is emitted by the T021 scaffold.",
                ],
            },
            trace_id=trace_id,
            workflow={
                "style": "pydantic-ai-typed-agent-scaffold",
                "agent": "DecisionSliceAgent",
                "deterministic_model": "fixture-response",
                "steps": self.steps,
                "functional_needs": FUNCTIONAL_NEEDS,
                "input_categories": [
                    "candidate",
                    "constraints",
                    "objective",
                    "project_context",
                ],
            },
        )

    def run(self) -> CandidateRun:
        self.load_context()
        self.map_functional_needs()
        recommendation = self.select_next_slice()
        return self.format_run(recommendation)


def run_candidate_workflow(payload: dict[str, Any]) -> CandidateRun:
    candidate = Candidate(**payload.get("candidate", {}))
    project_context = ProjectContext(**payload.get("project_context", {}))
    fixture = FixturePayload(
        candidate=candidate,
        constraints=[str(item) for item in payload.get("constraints", [])],
        objective=str(payload["objective"]),
        project_context=project_context,
    )
    return DecisionSliceAgentScaffold(fixture).run()
