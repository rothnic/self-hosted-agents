from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from base64 import b64encode
from dataclasses import dataclass, field
from typing import Any


def stable_id(prefix: str, value: Any, length: int = 16) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(encoded).hexdigest()[:length]}"


def stable_hex(value: Any, length: int) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:length]


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
            "uv run python apps/pydantic-ai/run.py --fixture "
            "packages/comparison/fixtures/pydantic-ai-decision-slice.json "
            "--output .agent-runs/verifications/pydantic-ai-logfire-run.json --require-logfire-export --pretty"
        ),
    }


def emit_logfire_export(trace_export: dict[str, Any], *, require: bool) -> dict[str, Any]:
    evidence = logfire_export_state()
    evidence["emission_requested"] = require
    evidence["flush_successful"] = False
    if not evidence["emission_requested"]:
        if evidence["configured"]:
            evidence["status"] = "configured-not-requested"
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


def langfuse_ingestion_state() -> dict[str, Any]:
    base_url = os.getenv("LANGFUSE_BASE_URL", "").rstrip("/")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
    project_id = os.getenv("LANGFUSE_PROJECT_ID", "")
    configured = bool(base_url and public_key and secret_key)
    return {
        "configured": configured,
        "sent": False,
        "verified": False,
        "status": "langfuse-otel-config-present" if configured else "missing-langfuse-otel-config",
        "credential_names": ["LANGFUSE_BASE_URL", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"],
        "base_url_configured": bool(base_url),
        "project_id_recorded": project_id,
        "endpoint_path": "/api/public/otel/v1/traces",
        "trace_url": "",
        "verification_command": (
            "LANGFUSE_BASE_URL=http://localhost:3000 "
            "LANGFUSE_PUBLIC_KEY=<pk-lf-...> LANGFUSE_SECRET_KEY=<sk-lf-...> "
            "LANGFUSE_PROJECT_ID=<optional-project-id> "
            "uv run python apps/pydantic-ai/run.py --fixture "
            "packages/comparison/fixtures/pydantic-ai-decision-slice.json "
            "--output .agent-runs/verifications/pydantic-ai-langfuse-run.json --require-langfuse-ingestion --pretty"
        ),
    }


def otlp_value(value: Any) -> dict[str, Any]:
    if isinstance(value, bool):
        return {"boolValue": value}
    if isinstance(value, int):
        return {"intValue": str(value)}
    if isinstance(value, float):
        return {"doubleValue": value}
    if isinstance(value, (list, tuple)):
        return {"arrayValue": {"values": [otlp_value(item) for item in value]}}
    if isinstance(value, dict):
        return {
            "kvlistValue": {
                "values": [{"key": str(key), "value": otlp_value(item)} for key, item in sorted(value.items())]
            }
        }
    if value is None:
        return {"stringValue": ""}
    return {"stringValue": str(value)}


def otlp_attributes(attributes: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"key": str(key), "value": otlp_value(value)} for key, value in sorted(attributes.items())]


def langfuse_trace_url(base_url: str, project_id: str, trace_id: str) -> str:
    if not base_url or not project_id:
        return ""
    return f"{base_url.rstrip('/')}/project/{urllib.parse.quote(project_id)}/traces/{trace_id}"


def langfuse_otlp_payload(trace_export: dict[str, Any]) -> dict[str, Any]:
    trace_id = str(trace_export["otel_trace_id"])
    run_id = str(trace_export.get("run_id", ""))
    start = 1_700_000_000_000_000_000
    spans = []
    for index, span in enumerate(trace_export.get("spans", [])):
        span_attributes = {
            **span.get("attributes", {}),
            "candidate.id": "pydantic-ai",
            "langfuse.release": "self-hosted-agents-local-fixture",
            "langfuse.session.id": run_id,
            "langfuse.trace.metadata.local_trace_id": trace_export["trace_id"],
            "langfuse.trace.metadata.run_id": run_id,
            "langfuse.trace.name": "pydantic-ai decision slice",
            "langfuse.trace.tags": ["self-hosted-agents", "pydantic-ai", "fixture"],
            "local.span_id": span.get("span_id", ""),
            "local.trace_id": trace_export["trace_id"],
            "run.id": run_id,
        }
        otlp_span = {
            "traceId": trace_id,
            "spanId": span["otel_span_id"],
            "name": span["name"],
            "kind": 1,
            "startTimeUnixNano": str(start + index * 1_000_000),
            "endTimeUnixNano": str(start + index * 1_000_000 + 500_000),
            "attributes": otlp_attributes(span_attributes),
            "status": {"code": 1},
        }
        if span.get("parent_otel_span_id"):
            otlp_span["parentSpanId"] = span["parent_otel_span_id"]
        spans.append(otlp_span)
    native_span_id_map: dict[str, str] = {}
    native_spans = trace_export.get("pydantic_ai_otel", {}).get("spans", [])
    for index, span in enumerate(native_spans):
        original_span_id = str(span.get("span_id", ""))
        native_span_id_map[original_span_id] = stable_hex(
            {"pydantic_ai_native_span": original_span_id, "index": index},
            16,
        )
    offset = len(spans)
    for index, span in enumerate(native_spans):
        original_span_id = str(span.get("span_id", ""))
        original_parent_span_id = str(span.get("parent_span_id", ""))
        attributes = {
            **span.get("attributes", {}),
            "candidate.id": "pydantic-ai",
            "local.trace_id": trace_export["trace_id"],
            "pydantic_ai.otel.native": True,
            "pydantic_ai.otel.original_span_id": original_span_id,
            "pydantic_ai.otel.original_trace_id": span.get("trace_id", ""),
            "run.id": run_id,
        }
        otlp_span = {
            "traceId": trace_id,
            "spanId": native_span_id_map[original_span_id],
            "name": str(span.get("name", "pydantic_ai_span")),
            "kind": 1,
            "startTimeUnixNano": str(start + (offset + index) * 1_000_000),
            "endTimeUnixNano": str(start + (offset + index) * 1_000_000 + 500_000),
            "attributes": otlp_attributes(attributes),
            "status": {"code": 1},
        }
        if original_parent_span_id and original_parent_span_id in native_span_id_map:
            otlp_span["parentSpanId"] = native_span_id_map[original_parent_span_id]
        spans.append(otlp_span)
    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": otlp_attributes(
                        {
                            "service.name": "pydantic-ai",
                            "candidate.id": "pydantic-ai",
                            "deployment.environment": "self-hosted-agents-fixture",
                        }
                    )
                },
                "scopeSpans": [
                    {
                        "scope": {
                            "name": "self-hosted-agents.pydantic-ai",
                            "version": "0.1.0",
                        },
                        "spans": spans,
                    }
                ],
            }
        ]
    }


def langfuse_request(
    url: str,
    public_key: str,
    secret_key: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    timeout: float = 10.0,
) -> tuple[int, str]:
    auth = b64encode(f"{public_key}:{secret_key}".encode("utf-8")).decode("ascii")
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "x-langfuse-ingestion-version": "4",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8", errors="replace")


def emit_langfuse_ingestion(trace_export: dict[str, Any], *, require: bool) -> dict[str, Any]:
    evidence = langfuse_ingestion_state()
    evidence["ingestion_requested"] = require
    base_url = os.getenv("LANGFUSE_BASE_URL", "").rstrip("/")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
    project_id = os.getenv("LANGFUSE_PROJECT_ID", "")
    trace_id = str(trace_export["otel_trace_id"])
    evidence["otel_trace_id"] = trace_id
    evidence["trace_url"] = langfuse_trace_url(base_url, project_id, trace_id)
    if not evidence["ingestion_requested"]:
        if evidence["configured"]:
            evidence["status"] = "configured-not-requested"
        return evidence
    if not evidence["configured"]:
        evidence["error"] = "LANGFUSE_BASE_URL, LANGFUSE_PUBLIC_KEY, and LANGFUSE_SECRET_KEY are required."
        return evidence

    endpoint = f"{base_url}/api/public/otel/v1/traces"
    evidence["endpoint"] = endpoint
    try:
        status, body = langfuse_request(
            endpoint,
            public_key,
            secret_key,
            method="POST",
            payload=langfuse_otlp_payload(trace_export),
        )
        evidence["http_status"] = status
        evidence["response_excerpt"] = body[:300]
        evidence["sent"] = 200 <= status < 300
        evidence["status"] = "sent-to-langfuse-otel" if evidence["sent"] else "send-failed"
    except urllib.error.HTTPError as exc:
        evidence["http_status"] = exc.code
        evidence["status"] = "send-failed"
        evidence["error"] = exc.read().decode("utf-8", errors="replace")[:300]
        return evidence
    except Exception as exc:  # pragma: no cover - depends on external Langfuse state.
        evidence["status"] = "send-failed"
        evidence["error"] = str(exc)
        return evidence

    deadline = time.monotonic() + (30.0 if require else 0.0)
    trace_api = f"{base_url}/api/public/traces/{trace_id}"
    evidence["trace_api"] = trace_api
    while evidence["sent"] and time.monotonic() <= deadline:
        try:
            status, body = langfuse_request(trace_api, public_key, secret_key, timeout=5.0)
            evidence["verify_http_status"] = status
            evidence["verified"] = status == 200
            evidence["verify_response_excerpt"] = body[:300]
            if evidence["verified"]:
                evidence["status"] = "verified-in-langfuse"
                evidence.pop("verify_error", None)
                break
        except urllib.error.HTTPError as exc:
            evidence["verify_http_status"] = exc.code
            evidence["verify_error"] = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception as exc:  # pragma: no cover - depends on external Langfuse state.
            evidence["verify_error"] = str(exc)
        if not require:
            break
        time.sleep(2.0)
    return evidence


@dataclass(frozen=True)
class TraceSpan:
    name: str
    span_id: str
    otel_span_id: str
    parent_span_id: str | None
    parent_otel_span_id: str | None
    attributes: dict[str, Any]
    status: str = "ok"

    def to_dict(self) -> dict[str, Any]:
        return {
            "attributes": self.attributes,
            "name": self.name,
            "otel_span_id": self.otel_span_id,
            "parent_span_id": self.parent_span_id,
            "parent_otel_span_id": self.parent_otel_span_id,
            "span_id": self.span_id,
            "status": self.status,
        }


@dataclass
class TraceRecorder:
    payload: dict[str, Any]
    provider: str = "local-otel-json"
    spans: list[TraceSpan] = field(default_factory=list)
    pydantic_ai_otel_spans: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.trace_id = stable_id("trace", self.payload, length=24)
        self.otel_trace_id = stable_hex({"trace_id": self.trace_id, "payload": self.payload}, 32)

    def record(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        span_value = {"trace_id": self.trace_id, "name": name, "index": len(self.spans)}
        parent = self.spans[-1] if self.spans else None
        self.spans.append(
            TraceSpan(
                name=name,
                span_id=stable_id("span", span_value),
                otel_span_id=stable_hex(span_value, 16),
                parent_span_id=parent.span_id if parent else None,
                parent_otel_span_id=parent.otel_span_id if parent else None,
                attributes=attributes or {},
            )
        )

    def record_pydantic_ai_otel_spans(self, spans: list[dict[str, Any]]) -> None:
        self.pydantic_ai_otel_spans.extend(spans)

    def export(self) -> dict[str, Any]:
        return {
            "format": "otel-style-json",
            "instrumentation": {
                "target": "Repo-local OTLP export with Pydantic AI native OpenTelemetry spans",
                "semantic_conventions": "OpenTelemetry GenAI semantic conventions 1.37.0",
                "pydantic_ai_format_version": 2,
                "notes": [
                    "The deterministic agent path captures spans from Pydantic AI's Instrumentation capability.",
                    "Repo-local workflow spans are normalized with Pydantic AI native spans for Langfuse ingestion.",
                    "OpenTelemetry GenAI conventions are experimental and may change.",
                ],
            },
            "provider": self.provider,
            "trace_id": self.trace_id,
            "otel_trace_id": self.otel_trace_id,
            "resource": {
                "service.name": "pydantic-ai",
                "candidate.id": "pydantic-ai",
            },
            "spans": [span.to_dict() for span in self.spans],
            "pydantic_ai_otel": {
                "status": "captured" if self.pydantic_ai_otel_spans else "missing",
                "span_count": len(self.pydantic_ai_otel_spans),
                "spans": self.pydantic_ai_otel_spans,
            },
            "logfire": logfire_export_state(),
            "langfuse": langfuse_ingestion_state(),
            "gaps": [
                "External Logfire telemetry is not sent during deterministic fixture validation.",
                "Self-hosted Langfuse ingestion is not attempted without an explicit proof flag.",
                "Optional Logfire export requires an operator-provided token and backend.",
                "Token, cost, and live model-call spans require a later non-fixture model run.",
            ],
        }
