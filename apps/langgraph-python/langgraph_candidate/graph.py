from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .trace import TraceRecorder, stable_id


FUNCTIONAL_NEEDS = [
    {
        "area": "Agent orchestration",
        "provider": "LangGraph state graph, deterministic nodes, and typed state boundary",
        "first_slice_status": "scaffolded",
    },
    {
        "area": "Tool and context access",
        "provider": "Fixture-backed project context adapter",
        "first_slice_status": "scaffolded",
    },
    {
        "area": "Observability",
        "provider": "Langfuse or OpenTelemetry trace capture",
        "first_slice_status": "scaffolded",
    },
    {
        "area": "Evaluation",
        "provider": "Deterministic scorer tied to the run artifact",
        "first_slice_status": "scaffolded",
    },
]


@dataclass
class WorkflowState:
    payload: dict[str, Any]
    trace: TraceRecorder
    transitions: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    recommendation: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CandidateRun:
    run_id: str
    candidate_app_id: str
    stack: list[str]
    run_mode: str
    graph: dict[str, Any]
    recommendation: dict[str, Any]
    alternatives: list[dict[str, str]]
    questions: list[str]
    acceptance_check: str
    evidence_paths: dict[str, str]
    gaps: list[str]
    trace_evidence: dict[str, Any]
    trace_export: dict[str, Any]
    evaluation_output: dict[str, Any] = field(default_factory=dict)
    command_used: str = "provided by CLI"

    def to_dict(self) -> dict[str, Any]:
        return {
            "acceptance_check": self.acceptance_check,
            "alternatives": self.alternatives,
            "candidate_app_id": self.candidate_app_id,
            "command_used": self.command_used,
            "evidence_paths": self.evidence_paths,
            "evaluation_output": self.evaluation_output,
            "gaps": self.gaps,
            "graph": self.graph,
            "questions": self.questions,
            "recommendation": self.recommendation,
            "run_id": self.run_id,
            "run_mode": self.run_mode,
            "stack": self.stack,
            "trace_evidence": self.trace_evidence,
        }


def load_context(state: WorkflowState) -> WorkflowState:
    payload = state.payload
    state.context = {
        "candidate": payload.get("candidate", {}),
        "constraints": payload.get("constraints", []),
        "objective": payload.get("objective", ""),
        "project_context": payload.get("project_context", {}),
    }
    state.transitions.append("load_context")
    state.trace.record(
        "load_context",
        {
            "constraint_count": len(state.context["constraints"]),
            "has_objective": bool(state.context["objective"]),
        },
    )
    return state


def map_functional_needs(state: WorkflowState) -> WorkflowState:
    state.context["functional_needs"] = FUNCTIONAL_NEEDS
    state.transitions.append("map_functional_needs")
    state.trace.record("map_functional_needs", {"functional_area_count": len(FUNCTIONAL_NEEDS)})
    return state


def select_slice(state: WorkflowState) -> WorkflowState:
    project_context = state.context.get("project_context", {})
    linked_task = str(project_context.get("next_expected_slice") or "T017")
    state.recommendation = {
        "next_slice": "Update the requirements matrix with LangGraph Python evidence, scores, and gaps.",
        "reason": (
            "The deterministic run now links recommendation, trace, evaluation, setup, and gap evidence, so the next "
            "useful slice is to summarize that evidence for roadmap comparison."
        ),
        "linked_task": linked_task,
    }
    state.transitions.append("select_slice")
    state.trace.record("select_slice", {"linked_task": state.recommendation["linked_task"]})
    return state


def format_run(state: WorkflowState) -> CandidateRun:
    candidate = state.context.get("candidate", {})
    stack = candidate.get("stack") or ["LangGraph Python", "Langfuse"]
    state.transitions.append("format_run")
    state.trace.record("format_run", {"candidate_app_id": str(candidate.get("id") or "langgraph-python")})
    trace_export = state.trace.export()
    run_id = stable_id(
        "run",
        {
            "candidate": candidate,
            "objective": state.context.get("objective"),
            "recommendation": state.recommendation,
            "trace_id": trace_export["trace_id"],
        },
        length=24,
    )
    return CandidateRun(
        run_id=run_id,
        candidate_app_id=str(candidate.get("id") or "langgraph-python"),
        stack=[str(item) for item in stack],
        run_mode="deterministic-fixture",
        graph={
            "style": "langgraph-state-graph",
            "nodes": ["load_context", "map_functional_needs", "select_slice", "format_run"],
            "transitions": state.transitions,
            "functional_needs": state.context["functional_needs"],
        },
        recommendation=state.recommendation,
        alternatives=[
            {
                "option": "Research the next Python candidate now",
                "tradeoff": "Good parallel planning, but it leaves LangGraph evidence unsummarized for comparison.",
            },
            {
                "option": "Add hosted Langfuse ingestion before scoring the slice",
                "tradeoff": "Improves observability depth, but it would make fixture validation depend on service setup.",
            },
        ],
        questions=[
            "Should the first trace evidence prefer Langfuse export, OpenTelemetry export, or both when credentials exist?"
        ],
        acceptance_check="uv run awf workflow-fixture-test",
        evidence_paths={
            "fixture_input": "packages/comparison/fixtures/langgraph-python-decision-slice.json",
            "run_artifact": "provided by --output",
            "setup_notes": "apps/langgraph-python/README.md",
            "gap_notes": "apps/langgraph-python/implementation-plan.md",
            "trace_evidence": "provided by --trace-output or next to --output",
            "evaluation_evidence": "provided by --evaluation-output or next to --output",
        },
        gaps=[
            "Langfuse ingestion is optional and not attempted in deterministic fixture mode without credentials.",
            "Evaluation is deterministic assertion scoring; dataset, model-judge, and annotation workflows are follow-ups.",
            "Durable runtime, persistence, retries, and long-running recovery are outside this first slice.",
        ],
        trace_evidence={
            "provider": trace_export["provider"],
            "trace_id": trace_export["trace_id"],
            "span_count": len(trace_export["spans"]),
            "langfuse": trace_export["langfuse"],
            "gaps": trace_export["gaps"],
        },
        trace_export=trace_export,
    )


def run_candidate_workflow(payload: dict[str, Any]) -> CandidateRun:
    state = WorkflowState(payload=payload, trace=TraceRecorder(payload))
    for node in (load_context, map_functional_needs, select_slice):
        state = node(state)
    return format_run(state)
