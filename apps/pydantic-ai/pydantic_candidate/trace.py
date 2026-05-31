from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any


def stable_id(prefix: str, value: Any, length: int = 16) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(encoded).hexdigest()[:length]}"


def logfire_export_state() -> dict[str, Any]:
    project_url = os.getenv("LOGFIRE_PROJECT_URL", "")
    base_url = os.getenv("LOGFIRE_BASE_URL", "")
    configured = bool(os.getenv("LOGFIRE_TOKEN"))
    return {
        "configured": configured,
        "sent": False,
        "status": "logfire-export-config-present" if configured else "missing-logfire-export-config",
        "credential_names": ["LOGFIRE_TOKEN"],
        "base_url_configured": bool(base_url),
        "project_url_recorded": project_url,
        "verification_command": (
            "LOGFIRE_TOKEN=<write-token> LOGFIRE_PROJECT_URL=<safe-project-or-trace-url> "
            "LOGFIRE_BASE_URL=<optional-self-managed-url> "
            "python3 apps/pydantic-ai/run.py --fixture "
            "packages/comparison/fixtures/pydantic-ai-decision-slice.json "
            "--output /tmp/pydantic-ai-run.json --require-logfire-export --pretty"
        ),
    }


def emit_logfire_export(trace_export: dict[str, Any], *, require: bool) -> dict[str, Any]:
    evidence = logfire_export_state()
    evidence["emission_requested"] = require or evidence["configured"]
    evidence["flush_successful"] = False
    if not evidence["emission_requested"]:
        return evidence
    if not evidence["configured"]:
        evidence["error"] = "LOGFIRE_TOKEN is required only when requiring Logfire export evidence."
        return evidence
    try:
        import logfire
    except ImportError as exc:
        evidence["status"] = "missing-logfire-sdk"
        evidence["error"] = str(exc)
        return evidence

    try:
        configure_options: dict[str, Any] = {
            "send_to_logfire": "if-token-present",
            "token": os.getenv("LOGFIRE_TOKEN"),
            "service_name": "pydantic-ai",
        }
        if os.getenv("LOGFIRE_BASE_URL"):
            configure_options["advanced"] = logfire.AdvancedOptions(base_url=os.environ["LOGFIRE_BASE_URL"])
        logfire.configure(**configure_options)
        with logfire.span(
            "pydantic-ai candidate workflow",
            attributes={
                "candidate.id": "pydantic-ai",
                "trace_id": trace_export["trace_id"],
                "span_count": len(trace_export.get("spans", [])),
            },
        ):
            for span in trace_export.get("spans", []):
                attributes = dict(span.get("attributes", {}))
                attributes.update(
                    {
                        "candidate.id": "pydantic-ai",
                        "local.trace_id": trace_export["trace_id"],
                        "local.span_id": span.get("span_id", ""),
                    }
                )
                with logfire.span(str(span.get("name", "candidate_step")), attributes=attributes):
                    pass
        evidence["flush_successful"] = bool(logfire.force_flush())
        evidence["sent"] = evidence["flush_successful"]
        evidence["status"] = "sent-to-logfire" if evidence["sent"] else "flush-failed"
    except Exception as exc:  # pragma: no cover - depends on external Logfire state.
        evidence["status"] = "send-failed"
        evidence["error"] = str(exc)
    return evidence


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
        return {
            "format": "otel-style-json",
            "instrumentation": {
                "target": "Pydantic AI OpenTelemetry instrumentation",
                "semantic_conventions": "OpenTelemetry GenAI semantic conventions 1.37.0",
                "pydantic_ai_format_version": 2,
                "notes": [
                    "Pydantic AI Logfire instrumentation defaults to format version 2.",
                    "OpenTelemetry GenAI conventions are experimental and may change.",
                ],
            },
            "provider": self.provider,
            "trace_id": self.trace_id,
            "resource": {
                "service.name": "pydantic-ai",
                "candidate.id": "pydantic-ai",
            },
            "spans": [span.to_dict() for span in self.spans],
            "logfire": logfire_export_state(),
            "gaps": [
                "External Logfire telemetry is not sent during deterministic fixture validation.",
                "Self-hosted assessment acceptance uses the repo-local OpenTelemetry trace export.",
                "Optional Logfire export requires an operator-provided token and backend.",
                "Token, cost, and live model-call spans require a later non-fixture model run.",
            ],
        }
