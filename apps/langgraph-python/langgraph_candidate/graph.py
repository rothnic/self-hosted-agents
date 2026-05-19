from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
    return state


def map_functional_needs(state: WorkflowState) -> WorkflowState:
    state.context["functional_needs"] = FUNCTIONAL_NEEDS
    state.transitions.append("map_functional_needs")
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
    return state


def format_run(state: WorkflowState) -> CandidateRun:
    candidate = state.context.get("candidate", {})
    stack = candidate.get("stack") or ["LangGraph Python", "Langfuse"]
    state.transitions.append("format_run")
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
            "trace_evidence": "T015 follow-up",
            "evaluation_evidence": "T016 follow-up",
        },
    )


def run_candidate_workflow(payload: dict[str, Any]) -> CandidateRun:
    state = WorkflowState(payload=payload)
    for node in (load_context, map_functional_needs, select_slice):
        state = node(state)
    return format_run(state)
