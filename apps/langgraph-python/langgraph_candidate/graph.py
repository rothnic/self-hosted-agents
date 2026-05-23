from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .trace import TraceRecorder


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
        "first_slice_status": "planned-follow-up",
    },
    {
        "area": "Evaluation",
        "provider": "Deterministic scorer tied to the run artifact",
        "first_slice_status": "planned-follow-up",
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
    candidate_app_id: str
    stack: list[str]
    run_mode: str
    graph: dict[str, Any]
    recommendation: dict[str, Any]
    alternatives: list[dict[str, str]]
    questions: list[str]
    acceptance_check: str
    evidence_paths: dict[str, str]
    trace_evidence: dict[str, Any]
    trace_export: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "acceptance_check": self.acceptance_check,
            "alternatives": self.alternatives,
            "candidate_app_id": self.candidate_app_id,
            "evidence_paths": self.evidence_paths,
            "graph": self.graph,
            "questions": self.questions,
            "recommendation": self.recommendation,
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
    state.recommendation = {
        "next_slice": "Add trace evidence capture for the LangGraph Python slice.",
        "reason": (
            "The deterministic scaffold proves the comparable workflow can run; trace capture is the next missing "
            "functional need before evaluation and scoring work can be trusted."
        ),
        "linked_task": "T015",
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
    return CandidateRun(
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
                "option": "Add evaluation artifact capture first",
                "tradeoff": "Useful soon, but weaker without a trace identifier to correlate against.",
            },
            {
                "option": "Research the next Python candidate now",
                "tradeoff": "Good parallel planning, but it does not improve evidence for the approved first slice.",
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
            "evaluation_evidence": "T016 follow-up",
        },
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
