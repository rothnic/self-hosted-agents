from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any

from .evaluation import evaluate_candidate_run
from .graph import run_candidate_workflow


def read_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_output(path: Path, data: dict[str, Any], pretty: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    indent = 2 if pretty else None
    path.write_text(json.dumps(data, indent=indent, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the deterministic LangGraph Python comparison workflow.")
    parser.add_argument("--fixture", required=True, type=Path, help="Shared comparison fixture JSON path.")
    parser.add_argument("--output", type=Path, help="Optional run artifact output path.")
    parser.add_argument("--trace-output", type=Path, help="Optional trace export output path.")
    parser.add_argument("--evaluation-output", type=Path, help="Optional evaluation artifact output path.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser


def command_used(argv: list[str] | None) -> str:
    parts = ["python3", "apps/langgraph-python/run.py", *(argv if argv is not None else sys.argv[1:])]
    return " ".join(shlex.quote(part) for part in parts)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    fixture = read_fixture(args.fixture)
    result = run_candidate_workflow(fixture)
    output = result.to_dict()
    output["command_used"] = command_used(argv)
    output["evidence_paths"]["fixture_input"] = str(args.fixture)
    if args.output is not None:
        output["evidence_paths"]["run_artifact"] = str(args.output)
    trace_output = args.trace_output
    if trace_output is None and args.output is not None:
        trace_output = args.output.with_suffix(".trace.json")
    evaluation_output = args.evaluation_output
    if evaluation_output is None and args.output is not None:
        evaluation_output = args.output.with_suffix(".evaluation.json")
    if trace_output is not None:
        write_output(trace_output, result.trace_export, args.pretty)
        output["evidence_paths"]["trace_evidence"] = str(trace_output)
        output["trace_evidence"] = result.trace_evidence
    if evaluation_output is not None:
        output["evidence_paths"]["evaluation_evidence"] = str(evaluation_output)
    evaluation = evaluate_candidate_run(
        run_id=str(output["run_id"]),
        trace_id=str(output["trace_evidence"]["trace_id"]),
        artifact=output,
        rerun_command=output["command_used"],
        evidence_links=output["evidence_paths"],
    ).to_dict()
    output["evaluation_output"] = evaluation
    if evaluation_output is not None:
        write_output(evaluation_output, evaluation, args.pretty)
    if args.output:
        write_output(args.output, output, args.pretty)
    print(json.dumps(output, indent=2 if args.pretty else None, sort_keys=True))
    return 0
