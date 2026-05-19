from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any


def stable_id(prefix: str, value: Any, length: int = 16) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(encoded).hexdigest()[:length]}"


@dataclass(frozen=True)
class TraceSpan:
    name: str
    span_id: str
    parent_span_id: str | None
    attributes: dict[str, Any]
    status: str = "ok"

    def to_dict(self) -> dict[str, Any]:
        return {
            "attributes": self.attributes,
            "name": self.name,
            "parent_span_id": self.parent_span_id,
            "span_id": self.span_id,
            "status": self.status,
        }


@dataclass
class TraceRecorder:
    payload: dict[str, Any]
    provider: str = "local-otel-json"
    spans: list[TraceSpan] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.trace_id = stable_id("trace", self.payload, length=24)

    def record(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        span_value = {"trace_id": self.trace_id, "name": name, "index": len(self.spans)}
        parent = self.spans[-1].span_id if self.spans else None
        self.spans.append(
            TraceSpan(
                name=name,
                span_id=stable_id("span", span_value),
                parent_span_id=parent,
                attributes=attributes or {},
            )
        )

    def export(self) -> dict[str, Any]:
        langfuse_configured = bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_HOST"))
        return {
            "format": "otel-style-json",
            "provider": self.provider,
            "trace_id": self.trace_id,
            "resource": {
                "service.name": "langgraph-python",
                "candidate.id": "langgraph-python",
            },
            "spans": [span.to_dict() for span in self.spans],
            "langfuse": {
                "configured": langfuse_configured,
                "status": "not-sent-during-deterministic-fixture",
            },
            "gaps": [
                "Trace is a local OpenTelemetry-style JSON export; Langfuse ingestion is not attempted in fixture mode.",
                "Token, cost, and model-call spans require the later real model/tool integration slice.",
            ],
        }
