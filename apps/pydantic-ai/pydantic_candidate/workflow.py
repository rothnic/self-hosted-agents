from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .trace import TraceRecorder, stable_id


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
        "provider": "Portable OpenTelemetry export with optional Logfire export",
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
    trace_export: dict[str, Any]
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
    def __init__(self, payload: FixturePayload, trace: TraceRecorder) -> None:
        self.payload = payload
        self.trace = trace
        self.steps: list[str] = []

    def load_context(self) -> None:
        self.steps.append("load_typed_fixture_context")
        self.trace.record(
            "load_typed_fixture_context",
            {
                "constraint_count": len(self.payload.constraints),
                "has_objective": bool(self.payload.objective),
            },
        )

    def map_functional_needs(self) -> None:
        self.steps.append("map_pydantic_ai_functional_needs")
        self.trace.record(
            "map_pydantic_ai_functional_needs",
            {"functional_area_count": len(FUNCTIONAL_NEEDS)},
        )

    def select_next_slice(self) -> dict[str, str]:
        self.steps.append("select_next_slice")
        linked_task = self.payload.project_context.next_expected_slice or "T022"
        self.trace.record("select_next_slice", {"linked_task": linked_task})
        return {
            "next_slice": "Add self-hosted-compatible OpenTelemetry trace evidence for the Pydantic AI slice.",
            "reason": (
                "The deterministic scaffold now proves the Pydantic AI lane can accept the shared comparison input "
                "and return structured decision output, so the next useful slice is inspectable local observability "
                "evidence with an optional Logfire export path."
            ),
            "linked_task": linked_task,
        }

    def format_run(self, recommendation: dict[str, str]) -> CandidateRun:
        self.steps.append("format_structured_run_artifact")
        candidate_data = {"id": self.payload.candidate.id, "stack": self.payload.candidate.stack}
        self.trace.record(
            "format_structured_run_artifact",
            {"candidate_app_id": self.payload.candidate.id},
        )
        trace_export = self.trace.export()
        trace_id = trace_export["trace_id"]
        otel_trace_id = trace_export["otel_trace_id"]
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
                    "option": "Add Pydantic Evals before trace evidence",
                    "tradeoff": "Useful scoring path, but it would leave the run hard to inspect and correlate.",
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
                "trace_evidence": "provided by --trace-output or next to --output",
            },
            gaps=[
                "External Logfire export is optional diagnostic evidence and is not required for fixture validation.",
                "Pydantic Evals output is planned for T023 and is not represented as passing implementation evidence.",
                "Durable runtime selection and smoke proof remain T024 and T025 work.",
            ],
            questions=[
                "Which self-hosted OpenTelemetry backend should later receive live Pydantic AI telemetry evidence?",
            ],
            recommendation=recommendation,
            run_id=run_id,
            run_mode="deterministic-fixture",
            stack=self.payload.candidate.stack,
            trace_evidence={
                "status": "captured",
                "linked_task": "T022",
                "provider": trace_export["provider"],
                "trace_id": trace_id,
                "otel_trace_id": otel_trace_id,
                "span_count": len(trace_export["spans"]),
                "instrumentation": trace_export["instrumentation"],
                "logfire": trace_export["logfire"],
                "logfire_configured": bool(trace_export["logfire"]["configured"]),
                "langfuse": trace_export["langfuse"],
                "langfuse_configured": bool(trace_export["langfuse"]["configured"]),
                "gaps": trace_export["gaps"],
            },
            trace_export=trace_export,
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
    trace = TraceRecorder(
        {
            "candidate": {"id": fixture.candidate.id, "stack": fixture.candidate.stack},
            "objective": fixture.objective,
            "project_context": {
                "active_spec": fixture.project_context.active_spec,
                "current_slice": fixture.project_context.current_slice,
                "next_expected_slice": fixture.project_context.next_expected_slice,
            },
        }
    )
    return DecisionSliceAgentScaffold(fixture, trace).run()
