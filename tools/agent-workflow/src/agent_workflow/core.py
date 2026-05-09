#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import importlib.util
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "AGENTS.md").exists() and (path / ".agents").exists():
            return path
    return start.parents[4]


ROOT = find_repo_root(Path(__file__).resolve())
POLICY_PATH = ROOT / ".agents" / "project-policy.json"
REQUIRED_NATIVE_SPEC_FILES = ["spec.md", "plan.md", "tasks.md"]
REQUIRED_SPECIFY_FILES = [
    ".specify/init-options.json",
    ".specify/integration.json",
    ".specify/memory/constitution.md",
    ".specify/scripts/bash/check-prerequisites.sh",
    ".specify/scripts/bash/common.sh",
    ".specify/scripts/bash/create-new-feature.sh",
    ".specify/scripts/bash/setup-plan.sh",
    ".specify/scripts/bash/setup-tasks.sh",
    ".specify/templates/checklist-template.md",
    ".specify/templates/constitution-template.md",
    ".specify/templates/plan-template.md",
    ".specify/templates/spec-template.md",
    ".specify/templates/tasks-template.md",
    ".specify/workflows/speckit/workflow.yml",
    ".specify/workflows/workflow-registry.json",
]
REQUIRED_SPECKIT_SKILLS = [
    "speckit-analyze",
    "speckit-checklist",
    "speckit-clarify",
    "speckit-constitution",
    "speckit-implement",
    "speckit-plan",
    "speckit-specify",
    "speckit-tasks",
]
TASK_RE = re.compile(
    r"^- \[(?P<done>[ xX])\] (?P<id>T[0-9]{3,})"
    r"(?: \[(?P<parallel>P)\])?(?: \[(?P<story>[^\]]+)\])? (?P<title>.+)$"
)


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def emit(data: Any, as_json: bool) -> int:
    if as_json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (list, tuple)):
                    print(f"{key}:")
                    for item in value:
                        print(f"  - {item}")
                else:
                    print(f"{key}: {value}")
        else:
            print(data)
    return 0


def run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("RUST_LOG", "error")
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=check, env=env)


def find_br() -> str | None:
    return shutil.which("br")


def load_policy() -> dict[str, Any]:
    if not POLICY_PATH.exists():
        return {}
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def now_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def bootstrap(args: argparse.Namespace) -> int:
    data = bootstrap_data()
    return emit(data, args.json)


def bootstrap_data() -> dict[str, Any]:
    br = find_br()
    hook_path = ROOT / ".git" / "config"
    hooks_installed = False
    if hook_path.exists():
        proc = run(["git", "config", "--get", "core.hooksPath"])
        hooks_installed = proc.returncode == 0 and proc.stdout.strip() == ".githooks"
    checks = [
        CheckResult("python3", shutil.which("python3") is not None, shutil.which("python3") or "missing"),
        CheckResult("git", shutil.which("git") is not None, shutil.which("git") or "missing"),
        CheckResult("repo", (ROOT / ".git").exists(), ".git present" if (ROOT / ".git").exists() else "not initialized"),
        CheckResult("br", br is not None, br or "missing; run tools/agent-workflow/bootstrap-dev.sh --install-tools"),
        CheckResult("agents", (ROOT / "AGENTS.md").exists(), "AGENTS.md"),
        CheckResult("skills", (ROOT / ".agents" / "skills").exists(), ".agents/skills"),
        CheckResult("specify", (ROOT / ".specify").exists(), ".specify"),
        CheckResult("specs", True, "Spec Kit creates specs/ when feature artifacts exist"),
        CheckResult("bdd", (ROOT / "tests" / "workflow" / "features").exists(), "tests/workflow/features"),
        CheckResult("hooks", hooks_installed, ".githooks" if hooks_installed else "run awf install-hooks"),
    ]
    policy = load_policy()
    data = {
        "root": str(ROOT),
        "checks": [asdict(c) for c in checks],
        "lifecycle_stage": policy.get("lifecycle_stage", "unknown"),
        "maintain_backward_compatibility": policy.get("maintain_backward_compatibility"),
    }
    return data


def collect_specs(root: Path = ROOT) -> list[dict[str, Any]]:
    specs_dir = root / "specs"
    specs = []
    if not specs_dir.exists():
        return specs
    for spec_dir in sorted(p for p in specs_dir.iterdir() if p.is_dir() and not p.name.startswith("_")):
        files = {name: spec_dir / name for name in REQUIRED_NATIVE_SPEC_FILES}
        spec_text = read_text(files["spec.md"])
        status = "unknown"
        spec_id = spec_dir.name
        for line in spec_text.splitlines():
            if line.startswith("**Feature Branch**:"):
                spec_id = line.split(":", 1)[1].strip().strip("`")
            if line.startswith("**Status**:"):
                status = line.split(":", 1)[1].strip()
        specs.append(
            {
                "id": spec_id,
                "path": rel(spec_dir),
                "status": status,
                "format": "spec-kit" if files["spec.md"].exists() else "unknown",
                "missing_files": [name for name, path in files.items() if not path.exists()],
            }
        )
    return specs


def collect_tasks(root: Path = ROOT) -> list[dict[str, Any]]:
    tasks = []
    for spec in collect_specs(root):
        tasks_path = root / spec["path"] / "tasks.md"
        for line in read_text(tasks_path).splitlines():
            match = TASK_RE.match(line)
            if match:
                item = match.groupdict()
                item["spec_id"] = spec["id"]
                item["done"] = item["done"].lower() == "x"
                item["parallel"] = item["parallel"] == "P"
                item["story"] = item["story"] or "shared"
                item["acceptance"] = "uv run awf workflow-fixture-test"
                tasks.append(item)
    return tasks


def collect_bdd_features(root: Path = ROOT) -> list[dict[str, Any]]:
    features = []
    candidates = [root / "tests" / "workflow" / "features", root / "features"]
    paths = []
    for features_root in candidates:
        if features_root.exists():
            paths.extend(sorted(features_root.glob("*.feature")))
    for path in paths:
        text = read_text(path)
        features.append(
            {
                "path": rel(path),
                "feature": next(
                    (
                        line.removeprefix("Feature:").strip()
                        for line in text.splitlines()
                        if line.strip().startswith("Feature:")
                    ),
                    path.stem,
                ),
                "has_actor": "@actor" in text or "As a " in text,
                "has_operational_assertion": (
                    "@operational" in text
                    or "operational" in text.lower()
                    or "analytics" in text.lower()
                ),
                "has_driver_boundary": "driver" in text.lower(),
            }
        )
    return features


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    items = []
    if not path.exists():
        return items
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            items.append({"_invalid": line})
    return items


def context_index(args: argparse.Namespace) -> int:
    return emit(context_index_data(), args.json)


def context_index_data() -> dict[str, Any]:
    br = find_br()
    policy = load_policy()
    data = {
        "root": str(ROOT),
        "lifecycle_stage": policy.get("lifecycle_stage", "unknown"),
        "maintain_backward_compatibility": policy.get("maintain_backward_compatibility"),
        "objectives": [rel(p) for p in sorted((ROOT / "objectives").glob("*.md"))],
        "specs": collect_specs(),
        "tasks": collect_tasks(),
        "bdd_features": collect_bdd_features(),
        "adrs": [rel(p) for p in sorted((ROOT / "docs" / "adr").glob("*.md"))],
        "research": [rel(p) for p in sorted((ROOT / "docs" / "research").glob("*.md"))],
        "blocked": [rel(p) for p in sorted((ROOT / ".agent-runs" / "blocked").glob("*.json"))],
        "recent_reports": [rel(p) for p in sorted((ROOT / ".agent-runs" / "reports").glob("*"))[-5:]],
        "br": br,
        "ticket_fallback": read_jsonl(ROOT / ".beads" / "issues.jsonl"),
    }
    if br:
        proc = run([br, "ready", "--json"])
        data["br_ready"] = proc.stdout.strip() if proc.returncode == 0 else proc.stderr.strip()
    return data


def is_ignored_path(path: Path, ignored_dirs: list[str]) -> bool:
    relative = rel(path)
    parts = path.relative_to(ROOT).parts if path.is_absolute() or str(path).startswith(str(ROOT)) else path.parts
    if any(part == "__pycache__" for part in parts):
        return True
    if any(part.endswith(".egg-info") for part in parts):
        return True
    return any(relative == item or relative.startswith(f"{item}/") for item in ignored_dirs)


def is_line_length_exempt(path: Path, exemptions: list[str]) -> bool:
    relative = rel(path)
    return any(relative == item or relative.startswith(item) for item in exemptions)


def iter_repo_files(policy: dict[str, Any]) -> list[Path]:
    hygiene = policy.get("repo_hygiene", {})
    ignored_dirs = hygiene.get("ignored_directories", [])
    files = []
    for path in ROOT.rglob("*"):
        if path.is_file() and not is_ignored_path(path, ignored_dirs):
            files.append(path)
    return sorted(files)


def repo_hygiene_result() -> tuple[int, dict[str, Any]]:
    policy = load_policy()
    hygiene = policy.get("repo_hygiene", {})
    errors = []
    warnings = []

    allowed_root = set(hygiene.get("allowed_root_entries", []))
    actual_root = {path.name for path in ROOT.iterdir()}
    unexpected = sorted(item for item in actual_root - allowed_root if item not in {".DS_Store"})
    if unexpected:
        errors.append(f"unexpected root entries: {', '.join(unexpected)}")

    ignored_dirs = hygiene.get("ignored_directories", [])
    max_files = int(hygiene.get("max_files_per_directory", 25))
    counts: dict[str, int] = {}
    for path in iter_repo_files(policy):
        parent = rel(path.parent)
        counts[parent] = counts.get(parent, 0) + 1
    crowded = sorted((directory, count) for directory, count in counts.items() if count > max_files)
    for directory, count in crowded:
        errors.append(f"directory {directory} has {count} files; limit is {max_files}")

    line_limits = hygiene.get("line_length_by_extension", {})
    exemptions = hygiene.get("line_length_exempt_paths", [])
    for path in iter_repo_files(policy):
        if is_line_length_exempt(path, exemptions):
            continue
        limit = line_limits.get(path.suffix)
        if not limit:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            warnings.append(f"skipped binary or non-utf8 file: {rel(path)}")
            continue
        for lineno, line in enumerate(lines, 1):
            if len(line) > int(limit):
                errors.append(f"{rel(path)}:{lineno} has {len(line)} chars; limit is {limit}")
                break

    data = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "policy": {
            "lifecycle_stage": policy.get("lifecycle_stage", "unknown"),
            "maintain_backward_compatibility": policy.get("maintain_backward_compatibility"),
            "max_files_per_directory": max_files,
        },
        "checked_files": len(iter_repo_files(policy)),
    }
    return (0 if not errors else 1), data


def repo_hygiene(args: argparse.Namespace) -> int:
    code, data = repo_hygiene_result()
    emit(data, args.json)
    return code


def install_hooks(args: argparse.Namespace) -> int:
    data = install_hooks_data()
    return emit(data, args.json) or (0 if data["ok"] else 1)


def install_hooks_data() -> dict[str, Any]:
    hook = ROOT / ".githooks" / "pre-commit"
    if not hook.exists():
        return {"ok": False, "error": f"missing {rel(hook)}"}
    hook.chmod(0o755)
    proc = run(["git", "config", "core.hooksPath", ".githooks"])
    return {
        "ok": proc.returncode == 0,
        "hooksPath": ".githooks",
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def spec_lint(args: argparse.Namespace, root: Path = ROOT) -> tuple[int, dict[str, Any]]:
    errors = []
    for spec in collect_specs(root):
        if spec["missing_files"]:
            errors.append(f"{spec['id']} missing files: {', '.join(spec['missing_files'])}")
        spec_path = root / spec["path"]
        spec_text = read_text(spec_path / "spec.md")
        if (spec_path / "spec.md").exists() and "## User Scenarios & Testing" not in spec_text:
            errors.append(f"{spec['id']} spec.md missing User Scenarios & Testing")
        if (spec_path / "spec.md").exists() and "## Requirements" not in spec_text:
            errors.append(f"{spec['id']} spec.md missing Requirements")
        if (spec_path / "tasks.md").exists():
            tasks = [task for task in collect_tasks(root) if task["spec_id"] == spec["id"]]
            if not tasks:
                errors.append(f"{spec['id']} tasks.md has no parseable Spec Kit tasks")
    specs_dir = root / "specs"
    if specs_dir.exists():
        for spec_dir in sorted(path for path in specs_dir.iterdir() if path.is_dir() and not path.name.startswith("_")):
            if not (spec_dir / "spec.md").exists():
                errors.append(f"{rel(spec_dir)} is not a native Spec Kit feature folder")
    data = {"ok": not errors, "errors": errors, "specs": collect_specs(root)}
    return (0 if not errors else 1), data


def spec_kit_lint(args: argparse.Namespace, root: Path = ROOT) -> tuple[int, dict[str, Any]]:
    errors = []
    warnings = []
    missing = [path for path in REQUIRED_SPECIFY_FILES if not (root / path).exists()]
    if missing:
        errors.append(f"missing Spec Kit files: {', '.join(missing)}")
    missing_skills = [
        skill for skill in REQUIRED_SPECKIT_SKILLS if not (root / ".agents" / "skills" / skill / "SKILL.md").exists()
    ]
    if missing_skills:
        errors.append(f"missing Spec Kit Codex skills: {', '.join(missing_skills)}")

    constitution = read_text(root / ".specify" / "memory" / "constitution.md")
    placeholder_markers = ["[PROJECT_NAME]", "[PRINCIPLE_", "[SECTION_", "[GOVERNANCE_RULES]"]
    unresolved = [marker for marker in placeholder_markers if marker in constitution]
    if unresolved:
        errors.append(f"Spec Kit constitution has unresolved placeholders: {', '.join(unresolved)}")

    native_specs = []
    non_native_specs = []
    specs_dir = root / "specs"
    if specs_dir.exists():
        for spec_dir in sorted(path for path in specs_dir.iterdir() if path.is_dir() and not path.name.startswith("_")):
            if (spec_dir / "spec.md").exists():
                missing_native = [
                    name for name in ["spec.md", "plan.md", "tasks.md"] if not (spec_dir / name).exists()
                ]
                native_specs.append({"path": rel(spec_dir), "missing_files": missing_native})
                if missing_native:
                    errors.append(f"{rel(spec_dir)} missing native Spec Kit files: {', '.join(missing_native)}")
            else:
                non_native_specs.append(rel(spec_dir))
    if non_native_specs:
        errors.append("non-native spec folders are not allowed: " + ", ".join(non_native_specs))

    data = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "missing_files": missing,
        "missing_skills": missing_skills,
        "native_specs": native_specs,
        "non_native_specs": non_native_specs,
    }
    return (0 if not errors else 1), data


def bdd_lint(args: argparse.Namespace, root: Path = ROOT) -> tuple[int, dict[str, Any]]:
    errors = []
    features = collect_bdd_features(root)
    if not features:
        errors.append("no BDD feature files found in tests/workflow/features")
    for feature in features:
        if not feature["has_actor"]:
            errors.append(f"{feature['path']} missing actor marker")
        if not feature["has_operational_assertion"]:
            errors.append(f"{feature['path']} missing operational assertion")
        if not feature["has_driver_boundary"]:
            errors.append(f"{feature['path']} missing driver boundary")
    driver_files = []
    for driver_root in [root / "tests" / "workflow" / "drivers", root / "drivers"]:
        if driver_root.exists():
            driver_files.extend(sorted(driver_root.glob("*.md")))
    if not driver_files:
        errors.append("no BDD driver notes found in tests/workflow/drivers")
    data = {"ok": not errors, "errors": errors, "features": features, "drivers": [rel(p) for p in driver_files]}
    return (0 if not errors else 1), data


def ticket_sync(args: argparse.Namespace) -> int:
    return emit(ticket_sync_data(write=args.write), args.json)


def ticket_sync_data(write: bool) -> dict[str, Any]:
    tasks = collect_tasks()
    proposals = []
    for task in tasks:
        proposals.append(
            {
                "id": task["id"],
                "title": task["title"],
                "priority": 2,
                "type": "task",
                "status": "closed" if task["done"] else "open",
                "spec_id": task["spec_id"],
                "objective_id": "current",
                "acceptance": task["acceptance"],
            }
        )
    br = find_br()
    wrote = []
    if write and br:
        for proposal in proposals:
            title = proposal["title"]
            desc = (
                f"Spec: {proposal['spec_id']}\n"
                f"Objective: {proposal['objective_id']}\n"
                f"Acceptance: {proposal['acceptance']}"
            )
            proc = run(
                [
                    br,
                    "create",
                    title,
                    "--type",
                    "task",
                    "--priority",
                    str(proposal["priority"]),
                    "--description",
                    desc,
                    "--json",
                ]
            )
            wrote.append(
                {
                    "title": title,
                    "returncode": proc.returncode,
                    "stdout": proc.stdout.strip(),
                    "stderr": proc.stderr.strip(),
                }
            )
        run([br, "sync", "--flush-only"])
    return {"write": write, "br": br, "proposals": proposals, "created": wrote}


def ready_work(args: argparse.Namespace) -> int:
    data = ready_work_data()
    if data.get("raw_stdout") and not args.json:
        print(data["raw_stdout"])
        return 0
    return emit(data, args.json)


def ready_work_data() -> dict[str, Any]:
    br = find_br()
    if br:
        proc = run([br, "ready", "--json"])
        if proc.returncode == 0:
            try:
                ready = json.loads(proc.stdout)
            except json.JSONDecodeError:
                ready = []
            return {"br": br, "ready": ready, "raw_stdout": proc.stdout}
    ready = [task for task in collect_tasks() if not task["done"]]
    return {"br": br, "ready": ready}


def health_status_data(deep: bool) -> dict[str, Any]:
    check_args = argparse.Namespace(json=False)
    checks = []
    bootstrap_status = bootstrap_data()
    checks.append(
        {
            "name": "bootstrap",
            "ok": all(item["ok"] for item in bootstrap_status["checks"]),
            "data": bootstrap_status,
        }
    )
    for name, fn in [
        ("spec-lint", spec_lint),
        ("spec-kit-lint", spec_kit_lint),
        ("bdd-lint", bdd_lint),
        ("review-gate", review_gate),
        ("repo-hygiene", repo_hygiene_result),
    ]:
        if name == "repo-hygiene":
            code, data = fn()
        else:
            code, data = fn(check_args)
        checks.append({"name": name, "ok": code == 0, "data": data})
    if deep:
        code, data = workflow_fixture_test_result(write=False)
        checks.append({"name": "workflow-fixture-test", "ok": code == 0, "data": data})

    ready = ready_work_data()
    issues = []
    for check in checks:
        if not check["ok"]:
            issues.append(
                {
                    "severity": "blocker",
                    "title": f"Workflow health check failed: {check['name']}",
                    "source": check["name"],
                    "details": check["data"],
                }
            )
    if not find_br():
        issues.append(
            {
                "severity": "blocker",
                "title": "Beads Rust br is unavailable",
                "source": "bootstrap",
                "details": {"remediation": "Run tools/agent-workflow/bootstrap-dev.sh --install-tools"},
            }
        )

    if issues:
        next_action = "log issues and stop for planner triage"
    elif ready.get("ready"):
        next_action = "worker may claim one ready item"
    else:
        next_action = "planner should identify the next iteration of work"

    return {
        "ok": not issues,
        "deep": deep,
        "checks": checks,
        "issues": issues,
        "ready_count": len(ready.get("ready", [])),
        "claims": [rel(path) for path in sorted((ROOT / ".agent-runs" / "claims").glob("*.json"))],
        "next_action": next_action,
    }


def health_issue_path(issue_id: str) -> Path:
    return ROOT / ".agent-runs" / "health" / f"{issue_id}.json"


def issue_log_data(title: str, severity: str, source: str, details: str, write: bool) -> dict[str, Any]:
    issue_id = now_id("health")
    item = {
        "id": issue_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "title": title,
        "severity": severity,
        "source": source,
        "details": details,
        "beads": None,
    }
    if write:
        path = health_issue_path(issue_id)
        path.write_text(json.dumps(item, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        item["path"] = rel(path)
        br = find_br()
        if br:
            desc = f"Source: {source}\nSeverity: {severity}\n\n{details}"
            proc = run(
                [
                    br,
                    "create",
                    title,
                    "--type",
                    "task",
                    "--priority",
                    "1" if severity == "blocker" else "2",
                    "--description",
                    desc,
                    "--json",
                ]
            )
            item["beads"] = {
                "returncode": proc.returncode,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
            }
            run([br, "sync", "--flush-only"])
    return item


def claim_path(work_id: str) -> Path:
    safe_id = re.sub(r"[^A-Za-z0-9_.-]", "-", work_id)
    return ROOT / ".agent-runs" / "claims" / f"{safe_id}.json"


def claim_work_data(worker_id: str, write: bool) -> dict[str, Any]:
    ready = ready_work_data().get("ready", [])
    for item in ready:
        work_id = item.get("id") or item.get("title", "unknown")
        path = claim_path(str(work_id))
        if path.exists():
            continue
        claim = {
            "id": work_id,
            "worker_id": worker_id,
            "claimed_at": datetime.now(timezone.utc).isoformat(),
            "work": item,
        }
        if write:
            path.write_text(json.dumps(claim, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            claim["path"] = rel(path)
        return {"ok": True, "claimed": claim, "ready_count": len(ready)}
    return {"ok": False, "claimed": None, "ready_count": len(ready), "reason": "no unclaimed ready work"}


def cron_tick_data(role: str, worker_id: str | None, write: bool) -> dict[str, Any]:
    health = health_status_data(deep=False)
    logged = []
    if health["issues"] and write:
        for issue in health["issues"]:
            logged.append(
                issue_log_data(
                    title=issue["title"],
                    severity=issue["severity"],
                    source=issue["source"],
                    details=json.dumps(issue["details"], indent=2, sort_keys=True),
                    write=True,
                )
            )
    if role == "planner":
        run_data = workflow_run_data(mode="plan", trigger="cron", write=write, dry_run=not write)
        next_action = "planner produced run artifact" if write else "planner dry run complete"
        return {"ok": health["ok"], "role": role, "health": health, "logged": logged, "run": run_data, "next_action": next_action}
    if role == "worker":
        claim = claim_work_data(worker_id or "worker", write=write) if health["ok"] else None
        if claim and claim["ok"] and write:
            next_action = "worker claimed one item"
        elif claim and claim["ok"]:
            next_action = "worker would claim one item"
        else:
            next_action = "worker stopped"
        return {"ok": health["ok"], "role": role, "health": health, "logged": logged, "claim": claim, "next_action": next_action}
    return {"ok": False, "role": role, "health": health, "logged": logged, "error": "role must be planner or worker"}


def review_gate(args: argparse.Namespace, root: Path = ROOT) -> tuple[int, dict[str, Any]]:
    blocked_dir = root / ".agent-runs" / "blocked"
    existing = sorted(blocked_dir.glob("*.json")) if blocked_dir.exists() else []
    spec_errors = spec_lint(args, root)[1]["errors"]
    open_questions = []
    for path in sorted((root / "specs").glob("*/spec.md")):
        if path.parent.name.startswith("_"):
            continue
        text = read_text(path)
        if "[NEEDS CLARIFICATION:" in text:
            open_questions.append(rel(path))
    data = {
        "ok": not existing and not open_questions and not spec_errors,
        "blocked_files": [rel(p) for p in existing],
        "open_questions": open_questions,
        "spec_errors": spec_errors,
    }
    return (0 if data["ok"] else 1), data


def workflow_run(args: argparse.Namespace) -> int:
    data = workflow_run_data(
        mode=args.mode,
        trigger=args.trigger,
        write=args.write,
        dry_run=args.dry_run,
    )
    return emit(data, args.json)


def workflow_run_data(mode: str, trigger: str, write: bool, dry_run: bool) -> dict[str, Any]:
    gate_args = argparse.Namespace(json=False)
    run_id = now_id(f"run-{mode}")
    context = {
        "run_id": run_id,
        "mode": mode,
        "dry_run": dry_run or not write,
        "trigger": trigger,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "context": {
            "specs": collect_specs(),
            "tasks": collect_tasks(),
            "bdd_features": collect_bdd_features(),
            "blocked": [rel(p) for p in sorted((ROOT / ".agent-runs" / "blocked").glob("*.json"))],
        },
        "next_action": "resolve review gate" if review_gate(gate_args)[0] else "select one ready ticket or update specs",
    }
    if write:
        manifest = ROOT / ".agent-runs" / "manifests" / f"{run_id}.json"
        report = ROOT / ".agent-runs" / "reports" / f"{run_id}.md"
        manifest.write_text(json.dumps(context, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        report.write_text(render_report(context), encoding="utf-8")
    return context


def render_report(context: dict[str, Any]) -> str:
    return (
        f"# Workflow Run Report\n\n"
        f"Run id: `{context['run_id']}`\n"
        f"Mode: `{context['mode']}`\n"
        f"Trigger: `{context['trigger']}`\n"
        f"Dry run: `{context['dry_run']}`\n\n"
        f"## Next Action\n\n{context['next_action']}\n"
    )


def run_report(args: argparse.Namespace) -> int:
    return emit(run_report_data(), args.json)


def run_report_data() -> dict[str, Any]:
    reports = sorted((ROOT / ".agent-runs" / "reports").glob("*.md"))
    return {"reports": [rel(p) for p in reports], "latest": read_text(reports[-1]) if reports else ""}


def learning_capture(args: argparse.Namespace) -> int:
    if not args.note:
        return emit({"ok": False, "error": "--note is required"}, args.json) or 1
    return emit(
        learning_capture_data(note=args.note, source=args.source, write=getattr(args, "write", False)),
        args.json,
    )


def learning_capture_data(note: str, source: str, write: bool) -> dict[str, Any]:
    item = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "note": note,
        "source": source,
    }
    if write:
        path = ROOT / ".agent-runs" / "learnings" / f"{now_id('learning')}.json"
        path.write_text(json.dumps(item, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        item["path"] = rel(path)
    return item


def workflow_fixture_test(args: argparse.Namespace) -> int:
    code, data = workflow_fixture_test_result(write=getattr(args, "write", False))
    emit(data, args.json)
    return code


def workflow_fixture_test_result(write: bool) -> tuple[int, dict[str, Any]]:
    args = argparse.Namespace(json=False)
    fixture = ROOT / "tests" / "workflow" / "fixtures" / "sample-project"
    results = []
    code, data = spec_lint(args, fixture)
    results.append({"name": "fixture spec lint detects incomplete spec", "ok": code != 0, "data": data})
    code, data = review_gate(args, fixture)
    blocks = data["blocked_files"] or data["open_questions"] or data["spec_errors"]
    results.append(
        {
            "name": "fixture review gate blocks ambiguity",
            "ok": code != 0 and bool(blocks),
            "data": data,
        }
    )
    code, data = bdd_lint(args, fixture)
    results.append({"name": "fixture BDD lint validates actor and operational contracts", "ok": code == 0, "data": data})

    code, data = spec_lint(args, ROOT)
    results.append({"name": "root spec lint passes", "ok": code == 0, "data": data})
    code, data = spec_kit_lint(args, ROOT)
    results.append({"name": "root Spec Kit substrate lint passes", "ok": code == 0, "data": data})
    code, data = bdd_lint(args, ROOT)
    results.append({"name": "root BDD lint passes", "ok": code == 0, "data": data})
    code, data = bdd_run_result("fixture")
    results.append({"name": "root fixture BDD driver run passes", "ok": code == 0, "data": data})
    code, data = repo_hygiene_result()
    results.append({"name": "root repo hygiene passes", "ok": code == 0, "data": data})

    ok = all(item["ok"] for item in results)
    if write:
        learning = ROOT / ".agent-runs" / "learnings" / f"{now_id('fixture')}.json"
        learning.write_text(
            json.dumps(
                {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "note": "Workflow fixture validates spec lint, BDD contract lint, and review gate behavior.",
                    "ok": ok,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    data = {"ok": ok, "results": results}
    return (0 if ok else 1), data


def bdd_run_result(driver: str) -> tuple[int, dict[str, Any]]:
    driver_path = ROOT / "tests" / "workflow" / "drivers" / f"{driver}_driver.py"
    if not driver_path.exists():
        return 1, {"ok": False, "error": f"missing driver {rel(driver_path)}"}
    spec = importlib.util.spec_from_file_location(f"{driver}_driver", driver_path)
    if spec is None or spec.loader is None:
        return 1, {"ok": False, "error": f"could not load driver {rel(driver_path)}"}
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(driver_path.parent))
    spec.loader.exec_module(module)
    if not hasattr(module, "run"):
        return 1, {"ok": False, "error": f"driver {rel(driver_path)} missing run(features)"}
    features = collect_bdd_features(ROOT)
    result = module.run(features)
    ok = bool(result.get("ok"))
    return 0 if ok else 1, result


def bdd_run(args: argparse.Namespace) -> int:
    code, data = bdd_run_result(args.driver)
    emit(data, args.json)
    return code


def spec_new(args: argparse.Namespace) -> int:
    code, data = spec_new_result(
        slug=args.slug,
        objective=args.objective,
        write=args.write,
        force=args.force,
    )
    emit(data, args.json)
    return code


def spec_new_result(slug: str, objective: str, write: bool, force: bool) -> tuple[int, dict[str, Any]]:
    script = ROOT / ".specify" / "scripts" / "bash" / "create-new-feature.sh"
    if not script.exists():
        return 1, {"ok": False, "error": f"missing {rel(script)}"}
    cmd = [str(script), "--json", "--short-name", slug, objective]
    if not write:
        cmd.insert(1, "--dry-run")
    if force:
        cmd.insert(1, "--allow-existing-branch")
    proc = run(cmd)
    data = {"ok": proc.returncode == 0, "command": cmd, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}
    return (0 if proc.returncode == 0 else 1), data


def command_status_tuple(fn, args: argparse.Namespace) -> int:
    code, data = fn(args)
    emit(data, args.json)
    return code


def main() -> int:
    argv = sys.argv[1:]
    trailing_json = "--json" in argv
    if trailing_json:
        argv = [item for item in argv if item != "--json"]
    parser = argparse.ArgumentParser(description="Environment-agnostic agent workflow CLI")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("bootstrap")
    sub.add_parser("context-index")
    sub.add_parser("spec-lint")
    sub.add_parser("spec-kit-lint")
    sub.add_parser("bdd-lint")
    bdd_run_p = sub.add_parser("bdd-run")
    bdd_run_p.add_argument("--driver", required=True)
    sub.add_parser("ready-work")
    sub.add_parser("review-gate")
    sub.add_parser("repo-hygiene")
    sub.add_parser("install-hooks")
    sub.add_parser("run-report")
    sub.add_parser("workflow-fixture-test")

    spec_new_p = sub.add_parser("spec-new")
    spec_new_p.add_argument("slug")
    spec_new_p.add_argument("--objective", default="agentic-development-foundation")
    spec_new_p.add_argument("--write", action="store_true")
    spec_new_p.add_argument("--force", action="store_true")

    ticket = sub.add_parser("ticket-sync")
    ticket.add_argument("--dry-run", action="store_true")
    ticket.add_argument("--write", action="store_true")

    workflow = sub.add_parser("workflow-run")
    workflow.add_argument("--mode", choices=["plan", "implement", "review"], required=True)
    workflow.add_argument("--trigger", default="manual")
    workflow.add_argument("--dry-run", action="store_true")
    workflow.add_argument("--write", action="store_true")

    learning = sub.add_parser("learning-capture")
    learning.add_argument("--note")
    learning.add_argument("--source", default="manual")
    learning.add_argument("--write", action="store_true")

    args = parser.parse_args(argv)
    args.json = args.json or trailing_json
    if args.command == "bootstrap":
        return bootstrap(args)
    if args.command == "context-index":
        return context_index(args)
    if args.command == "spec-lint":
        return command_status_tuple(spec_lint, args)
    if args.command == "spec-kit-lint":
        return command_status_tuple(spec_kit_lint, args)
    if args.command == "bdd-lint":
        return command_status_tuple(bdd_lint, args)
    if args.command == "bdd-run":
        return bdd_run(args)
    if args.command == "ticket-sync":
        return ticket_sync(args)
    if args.command == "ready-work":
        return ready_work(args)
    if args.command == "review-gate":
        return command_status_tuple(review_gate, args)
    if args.command == "repo-hygiene":
        return repo_hygiene(args)
    if args.command == "install-hooks":
        return install_hooks(args)
    if args.command == "workflow-run":
        return workflow_run(args)
    if args.command == "run-report":
        return run_report(args)
    if args.command == "learning-capture":
        return learning_capture(args)
    if args.command == "workflow-fixture-test":
        return workflow_fixture_test(args)
    if args.command == "spec-new":
        return spec_new(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
