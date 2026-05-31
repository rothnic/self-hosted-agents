from __future__ import annotations

from dataclasses import dataclass, field
from importlib.metadata import version
from typing import Any

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.capabilities.instrumentation import Instrumentation
from pydantic_ai.models.test import TestModel
from pydantic_ai.models.instrumented import InstrumentationSettings
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

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
        "provider": "Portable OpenTelemetry export with optional self-hosted Langfuse ingestion",
        "first_slice_status": "completed-through-T027",
    },
    {
        "area": "Evaluation",
        "provider": "Pydantic Evals with deterministic assertions",
        "first_slice_status": "completed-through-T023",
    },
    {
        "area": "Durable execution",
        "provider": "Pydantic AI DBOSAgent plus local SQLite DBOS smoke evidence",
        "first_slice_status": "completed-through-T025",
    },
]


@dataclass(frozen=True)
class Candidate:
    id: str = "pydantic-ai"
    stack: list[str] = field(default_factory=lambda: ["Pydantic AI", "Langfuse/OpenTelemetry", "Pydantic Evals", "DBOS"])


@dataclass(frozen=True)
class ProjectContext:
    active_spec: str = ""
    comparison_contract: str = ""
    current_slice: str = "T026"
    next_expected_slice: str = "roadmap-review"
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


class DecisionRecommendation(BaseModel):
    next_slice: str
    reason: str
    linked_task: str


def expected_recommendation(linked_task: str) -> dict[str, str]:
    if linked_task == "roadmap-review":
        return {
            "next_slice": "Run the roadmap review for Pydantic AI promotion and next-goal routing.",
            "reason": (
                "The Pydantic AI lane now has deterministic run, trace, self-hosted Langfuse, Pydantic Evals, "
                "durable selection, DBOS smoke, and requirements scoring evidence. The next useful slice is a "
                "roadmap review that decides whether to deepen Pydantic AI, compare another stack, or move to the "
                "next parent goal while keeping final-solution gaps explicit."
            ),
            "linked_task": linked_task,
        }
    if linked_task == "T026":
        return {
            "next_slice": "Update the requirements matrix with Pydantic AI evidence, scores, and promotion gaps.",
            "reason": (
                "The runnable candidate now has deterministic run, trace, self-hosted Langfuse, Pydantic Evals, "
                "and DBOS durable smoke evidence, so the next useful slice is requirements scoring with final-solution "
                "gaps kept explicit."
            ),
            "linked_task": linked_task,
        }
    return {
        "next_slice": "Add Pydantic Evals output and run artifact capture for the Pydantic AI slice.",
        "reason": (
            "The runnable candidate now has deterministic local trace evidence plus optional self-hosted "
            "Langfuse ingestion, so the next useful slice is evaluation evidence correlated to the same run "
            "and trace identity."
        ),
        "linked_task": linked_task,
    }


def serialize_otel_span(span: Any) -> dict[str, Any]:
    context = span.get_span_context()
    parent = span.parent
    return {
        "attributes": dict(span.attributes or {}),
        "kind": str(span.kind.name),
        "name": span.name,
        "parent_span_id": f"{parent.span_id:016x}" if parent else "",
        "span_id": f"{context.span_id:016x}",
        "status_code": str(span.status.status_code.name),
        "trace_id": f"{context.trace_id:032x}",
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
        linked_task = self.payload.project_context.next_expected_slice or "roadmap-review"
        expected = expected_recommendation(linked_task)
        span_exporter = InMemorySpanExporter()
        tracer_provider = TracerProvider()
        tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
        instrumentation = Instrumentation(
            InstrumentationSettings(
                tracer_provider=tracer_provider,
                include_content=True,
                version=2,
            )
        )
        agent = Agent(
            TestModel(custom_output_args=expected, model_name="self-hosted-agents-fixture"),
            output_type=DecisionRecommendation,
            instructions=(
                "Return the next implementation slice for the Pydantic AI candidate as structured data. "
                "Do not call external services."
            ),
            name="DecisionSliceAgent",
            capabilities=[instrumentation],
        )
        result = agent.run_sync(
            (
                f"Objective: {self.payload.objective}\n"
                f"Current slice: {self.payload.project_context.current_slice}\n"
                f"Next expected slice: {linked_task}"
            )
        )
        recommendation = result.output
        usage = result.usage
        pydantic_ai_spans = [serialize_otel_span(span) for span in span_exporter.get_finished_spans()]
        self.trace.record_pydantic_ai_otel_spans(pydantic_ai_spans)
        self.steps.append("run_pydantic_ai_agent")
        self.trace.record(
            "run_pydantic_ai_agent",
            {
                "agent": "DecisionSliceAgent",
                "linked_task": recommendation.linked_task,
                "model": "TestModel",
                "native_otel_span_count": len(pydantic_ai_spans),
                "pydantic_ai_version": version("pydantic-ai"),
                "requests": usage.requests,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
            },
        )
        self.trace.record("select_next_slice", {"linked_task": recommendation.linked_task})
        return recommendation.model_dump()

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
                    "option": "Deepen DBOS production proof immediately",
                    "tradeoff": "Useful if Pydantic AI is the likely primary path, but it skips a roadmap comparison gate.",
                },
                {
                    "option": "Start another candidate lane immediately",
                    "tradeoff": "Useful contrast, but it should be chosen after reviewing the Pydantic AI scores and gaps.",
                },
            ],
            candidate_app_id=self.payload.candidate.id,
            evaluation_output={
                "status": "provided-by-cli",
                "linked_task": "T023",
                "provider": "Pydantic Evals",
                "artifact": "provided by --evaluation-output or next to --output",
            },
            evidence_paths={
                "fixture_input": "packages/comparison/fixtures/pydantic-ai-decision-slice.json",
                "run_artifact": "provided by --output",
                "setup_notes": "apps/pydantic-ai/README.md",
                "gap_notes": "apps/pydantic-ai/implementation-plan.md",
                "trace_evidence": "provided by --trace-output or next to --output",
                "evaluation_evidence": "provided by --evaluation-output or next to --output",
            },
            gaps=[
                "External Logfire export is optional diagnostic evidence and is not required for fixture validation.",
                "DBOS durable smoke is local SQLite proof; retry, human wait, production storage, and workers remain gaps.",
                "Self-hosted Langfuse proof exists, but production deployment, retention, backup, and recovery remain gaps.",
            ],
            questions=[
                "Should the next roadmap step deepen Pydantic AI or compare another stack before primary-stack selection?",
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
                "style": "pydantic-ai-typed-agent",
                "agent": "DecisionSliceAgent",
                "deterministic_model": "pydantic_ai.models.test.TestModel",
                "pydantic_ai_runtime": {
                    "package": "pydantic-ai",
                    "version": version("pydantic-ai"),
                    "agent_class": "pydantic_ai.Agent",
                    "instrumentation": "pydantic_ai.capabilities.instrumentation.Instrumentation",
                    "model_class": "pydantic_ai.models.test.TestModel",
                    "native_otel_span_count": len(trace_export["pydantic_ai_otel"]["spans"]),
                    "output_model": "DecisionRecommendation",
                    "network_required": False,
                },
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
