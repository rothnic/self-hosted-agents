#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import importlib.util
import tempfile
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
OBJECTIVE_RE = re.compile(r"^ID:\s*`?([^`\s]+)`?\s*$", re.MULTILINE)


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


def run(cmd: list[str], check: bool = False, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("RUST_LOG", "error")
    return subprocess.run(cmd, cwd=cwd or ROOT, text=True, capture_output=True, check=check, env=env)


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


def configured_hooks_path(root: Path = ROOT) -> str | None:
    if not (root / ".git").exists():
        return None
    proc = run(["git", "-C", str(root), "config", "--get", "core.hooksPath"])
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def hooks_installed(root: Path = ROOT) -> bool:
    return configured_hooks_path(root) == ".githooks"


def bootstrap(args: argparse.Namespace) -> int:
    data = bootstrap_data()
    return emit(data, args.json)


def bootstrap_data() -> dict[str, Any]:
    br = find_br()
    has_hooks = hooks_installed(ROOT)
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
        CheckResult("hooks", has_hooks, ".githooks" if has_hooks else "run awf install-hooks"),
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


def tasks_acceptance_command(tasks_path: Path) -> str:
    for line in read_text(tasks_path).splitlines():
        if line.startswith("**Acceptance**:"):
            return line.split(":", 1)[1].strip().strip("`")
    return "uv run awf workflow-fixture-test"


def collect_tasks(root: Path = ROOT) -> list[dict[str, Any]]:
    tasks = []
    for spec in collect_specs(root):
        tasks_path = root / spec["path"] / "tasks.md"
        acceptance = tasks_acceptance_command(tasks_path)
        for line in read_text(tasks_path).splitlines():
            match = TASK_RE.match(line)
            if match:
                item = match.groupdict()
                item["spec_id"] = spec["id"]
                item["done"] = item["done"].lower() == "x"
                item["parallel"] = item["parallel"] == "P"
                item["story"] = item["story"] or "shared"
                item["acceptance"] = acceptance
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


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def write_json_artifact(directory: str, prefix: str, data: dict[str, Any]) -> str:
    path_dir = ROOT / ".agent-runs" / directory
    path_dir.mkdir(parents=True, exist_ok=True)
    path = path_dir / f"{now_id(prefix)}.json"
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return rel(path)


def current_objective_id(root: Path = ROOT) -> str:
    text = read_text(root / "objectives" / "current.md")
    match = OBJECTIVE_RE.search(text)
    return match.group(1) if match else "current"


def task_external_ref(task: dict[str, Any]) -> str:
    return f"specs/{task['spec_id']}/tasks.md#{task['id']}"


def task_source_path(task: dict[str, Any]) -> str:
    return f"specs/{task['spec_id']}/tasks.md"


def task_by_external_ref(external_ref: str) -> dict[str, Any] | None:
    for task in collect_tasks():
        if task_external_ref(task) == external_ref:
            return task
    return None


def task_has_beads_evidence(task: dict[str, Any], issues: list[dict[str, Any]]) -> bool:
    task_id = task["id"]
    external_ref = task_external_ref(task)
    for issue in issues:
        issue_text = "\n".join(
            str(issue.get(key, "")) for key in ["id", "title", "description", "external_ref", "close_reason"]
        )
        if issue.get("external_ref") == external_ref or f"Task: {task_id}" in issue_text or task_id in issue_text:
            return True
        for comment in issue.get("comments", []):
            text = str(comment.get("text", ""))
            if external_ref in text or task_id in text:
                return True
    return False


def is_human_review_issue(issue: dict[str, Any]) -> bool:
    combined = " ".join(
        str(issue.get(key, "")) for key in ["id", "title", "description", "issue_type", "external_ref"]
    ).lower()
    labels = {str(label).lower() for label in issue.get("labels", [])}
    return (
        "human review" in combined
        or "human approval" in combined
        or "review and approve" in combined
        or "review-gate" in labels
        or "human-review" in labels
    )


def issue_open_dependencies(issue: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        dep
        for dep in issue.get("dependencies", [])
        if str(dep.get("type", "blocks")).lower() == "blocks"
        if str(dep.get("status", "")).lower() not in {"closed", "resolved", "done"}
    ]


def is_implementation_issue(issue: dict[str, Any]) -> bool:
    if str(issue.get("issue_type", "")).lower() == "epic":
        return False
    return not is_human_review_issue(issue)


def issue_has_required_metadata(issue: dict[str, Any]) -> bool:
    text = str(issue.get("description", ""))
    return all(
        [
            "Objective:" in text,
            "Spec:" in text,
            "Task:" in text,
            "Acceptance:" in text,
            bool(issue.get("external_ref")),
        ]
    )


def beads_issues() -> list[dict[str, Any]]:
    return read_jsonl(ROOT / ".beads" / "issues.jsonl")


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
    objective_id = current_objective_id()
    existing = beads_issues()
    existing_by_ref = {
        issue.get("external_ref"): issue
        for issue in existing
        if issue.get("external_ref")
    }
    human_gates = [
        issue
        for issue in existing
        if issue.get("status") == "open" and is_human_review_issue(issue)
    ]
    proposals = []
    for task in tasks:
        if task["done"]:
            continue
        external_ref = task_external_ref(task)
        existing_issue = existing_by_ref.get(external_ref)
        if existing_issue is None and is_human_review_issue({"title": task["title"]}) and human_gates:
            existing_issue = human_gates[0]
        implementation_task = is_implementation_issue({"title": task["title"]})
        proposals.append(
            {
                "id": task["id"],
                "title": task["title"],
                "priority": 1 if task["story"] == "US2" else 2,
                "type": "task",
                "status": "open",
                "spec_id": task["spec_id"],
                "objective_id": objective_id,
                "acceptance": task["acceptance"],
                "external_ref": external_ref,
                "source_path": task_source_path(task),
                "existing_issue_id": existing_issue.get("id") if existing_issue else None,
                "blocked_by": [issue["id"] for issue in human_gates if implementation_task],
            }
        )
    br = find_br()
    wrote = []
    if write and br:
        for proposal in proposals:
            if proposal["existing_issue_id"]:
                wrote.append(
                    {
                        "title": proposal["title"],
                        "skipped": True,
                        "reason": "existing issue",
                        "issue_id": proposal["existing_issue_id"],
                    }
                )
                continue
            title = proposal["title"]
            desc = (
                f"Objective: {proposal['objective_id']}\n"
                f"Spec: {proposal['spec_id']}\n"
                f"Task: {proposal['id']}\n"
                f"Source: {proposal['source_path']}\n"
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
                    "--external-ref",
                    proposal["external_ref"],
                    "--json",
                ]
            )
            issue_id = None
            try:
                created = json.loads(proc.stdout)
                if isinstance(created, dict):
                    issue_id = created.get("id")
                elif isinstance(created, list) and created:
                    issue_id = created[0].get("id")
            except json.JSONDecodeError:
                issue_id = None
            dependencies = []
            if issue_id:
                for gate_id in proposal["blocked_by"]:
                    dep_proc = run([br, "dep", "add", issue_id, gate_id, "--json"])
                    dependencies.append(
                        {
                            "depends_on": gate_id,
                            "returncode": dep_proc.returncode,
                            "stdout": dep_proc.stdout.strip(),
                            "stderr": dep_proc.stderr.strip(),
                        }
                    )
            wrote.append(
                {
                    "title": title,
                    "returncode": proc.returncode,
                    "stdout": proc.stdout.strip(),
                    "stderr": proc.stderr.strip(),
                    "issue_id": issue_id,
                    "dependencies": dependencies,
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
        issues = beads_issues()
        proc = run([br, "ready", "--json"])
        raw_ready = []
        if proc.returncode == 0:
            try:
                raw_ready = json.loads(proc.stdout)
            except json.JSONDecodeError:
                raw_ready = []
        human_required = [
            issue for issue in issues if issue.get("status") == "open" and is_human_review_issue(issue)
        ]
        blocked = [
            issue
            for issue in issues
            if issue.get("status") == "open"
            and is_implementation_issue(issue)
            and issue_open_dependencies(issue)
        ]
        ready = [
            issue
            for issue in raw_ready
            if is_implementation_issue(issue) and not issue_open_dependencies(issue)
        ]
        return {
            "br": br,
            "source": "beads",
            "ready": ready,
            "human_required": human_required,
            "blocked": blocked,
            "raw_ready": raw_ready,
            "raw_stdout": proc.stdout,
        }
    ready = [task for task in collect_tasks() if not task["done"]]
    return {"br": br, "source": "tasks-fallback", "ready": ready, "human_required": [], "blocked": []}


def completed_task_evidence_errors(tasks: list[dict[str, Any]], issues: list[dict[str, Any]]) -> list[str]:
    errors = []
    for task in tasks:
        if task["done"] and not task_has_beads_evidence(task, issues):
            errors.append(f"{task_external_ref(task)} is complete but has no Beads evidence")
    return errors


def issue_metadata_errors(issues: list[dict[str, Any]]) -> list[str]:
    errors = []
    for issue in issues:
        if issue.get("status") != "open" or not is_implementation_issue(issue):
            continue
        if not issue_has_required_metadata(issue):
            errors.append(f"{issue.get('id', '<unknown>')} missing objective/spec/task/external_ref/acceptance metadata")
    return errors


def workflow_state_lint_result() -> tuple[int, dict[str, Any]]:
    errors = []
    warnings = []
    tasks = collect_tasks()
    issues = beads_issues()
    ready = ready_work_data()

    errors.extend(completed_task_evidence_errors(tasks, issues))
    errors.extend(issue_metadata_errors(issues))

    if ready.get("human_required") and ready.get("ready"):
        ids = ", ".join(item.get("id", "<unknown>") for item in ready["ready"])
        gates = ", ".join(item.get("id", "<unknown>") for item in ready["human_required"])
        errors.append(f"implementation ready work ({ids}) is exposed while human review is required ({gates})")

    data = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "completed_tasks_checked": len([task for task in tasks if task["done"]]),
        "open_issues_checked": len([issue for issue in issues if issue.get("status") == "open"]),
    }
    return (0 if not errors else 1), data


def git_state_summary(status_text: str) -> dict[str, Any]:
    lines = [line for line in status_text.splitlines() if line.strip()]
    branch = lines[0][3:] if lines and lines[0].startswith("## ") else "unknown"
    changed = [line for line in lines[1:] if line]
    return {
        "branch": branch,
        "clean": not changed,
        "changed_files": len(changed),
        "summary": "clean" if not changed else f"{len(changed)} changed file(s)",
    }


def process_position_summary(
    bootstrap_ok: bool, health: dict[str, Any], ready: dict[str, Any], context: dict[str, Any], status_text: str
) -> dict[str, Any]:
    tasks = context.get("tasks", [])
    open_tasks = [task for task in tasks if not task.get("done")]
    completed_tasks = [task for task in tasks if task.get("done")]
    health_ok = health.get("ok") and not health.get("issues")
    human_required = ready.get("human_required", [])
    implementer_ready = ready.get("ready", [])
    blocked = ready.get("blocked", [])
    git_state = git_state_summary(status_text)

    if not bootstrap_ok or not health_ok:
        phase = "workflow health triage"
        step = "Bootstrap/Verify"
        role = "health-status"
        plain_status = "Workflow checks need attention before planning or implementation."
    elif human_required:
        phase = "human review gate"
        step = "Review"
        role = "review-gatekeeper"
        plain_status = "Automation is paused for a human approval decision."
    elif implementer_ready:
        phase = "implementation"
        step = "Claim"
        role = "implementer"
        plain_status = "At least one Beads ticket is ready for an implementer to claim."
    elif open_tasks:
        phase = "backlog planning"
        step = "Ticket"
        role = "ticket-planner"
        plain_status = "Spec tasks remain, but no implementer-ready work is currently available."
    else:
        phase = "planning"
        step = "Plan"
        role = "pm-steward"
        plain_status = "No ready work is available; the next objective or spec action should be selected."

    return {
        "phase": phase,
        "state_machine_step": step,
        "active_role": role,
        "plain_language_status": plain_status,
        "git": git_state,
        "work_in_progress": {
            "open_spec_tasks": len(open_tasks),
            "completed_spec_tasks": len(completed_tasks),
            "ready_work": len(implementer_ready),
            "human_required": len(human_required),
            "blocked": len(blocked),
            "claims": len(health.get("claims", [])),
        },
    }


def meta_process_notes(health: dict[str, Any], ready: dict[str, Any], status_text: str) -> dict[str, Any]:
    git_state = git_state_summary(status_text)
    if health.get("issues"):
        learning = "Record the health failure with `uv run awf issue-log --write` before continuing."
        risk = "Starting implementation before health is restored may create hidden workflow drift."
    elif ready.get("human_required"):
        learning = "After the human decision, record approval or requested changes in the linked Beads ticket."
        risk = "Do not treat pending human-review tickets as implementer-ready work."
    elif git_state["clean"]:
        learning = "No meta-process follow-up is required unless the next run discovers drift."
        risk = "No immediate workflow risk is visible from git or health state."
    else:
        learning = "Before closing the loop, capture review learnings or follow-up tickets for any process gaps found."
        risk = "Uncommitted workflow changes should be reviewed before more work is layered on top."

    return {
        "learning_follow_up": learning,
        "backlog_spec_hygiene": "Keep `tasks.md` as spec decomposition and Beads as the executable backlog.",
        "risk_to_watch": risk,
    }


def executive_next_action(
    bootstrap_ok: bool,
    health: dict[str, Any],
    ready: dict[str, Any],
    context: dict[str, Any],
    status_text: str,
) -> dict[str, Any]:
    position = process_position_summary(bootstrap_ok, health, ready, context, status_text)
    git_state = position["git"]
    open_tasks = position["work_in_progress"]["open_spec_tasks"]
    ready_count = position["work_in_progress"]["ready_work"]
    human_count = position["work_in_progress"]["human_required"]
    blocked_count = position["work_in_progress"]["blocked"]

    if not bootstrap_ok or health.get("issues"):
        return {
            "where_we_are": "The workflow foundation is present, but the harness needs agent triage before more work starts.",
            "why_it_matters": "A failing workflow check means the backlog or evidence may be unreliable.",
            "recommendation": "Let the health-status agent diagnose and repair the failing check before product planning.",
            "agent_will_do_next": (
                "Run the health checks, isolate the failing workflow area, log a durable issue if needed, "
                "and propose or implement the smallest repair."
            ),
            "what_i_need_from_you": "Only a decision if the repair changes scope, priority, architecture, or acceptance criteria.",
            "questions": [],
        }
    if human_count:
        return {
            "where_we_are": "Work is paused at a human review gate.",
            "why_it_matters": "Agents should not move into implementation until the human decision is recorded.",
            "recommendation": "Review the approval brief and choose approve, request changes, or defer.",
            "agent_will_do_next": (
                "Record your decision, update the linked ticket/task state, rerun validation, "
                "and continue to the next safe lane."
            ),
            "what_i_need_from_you": "Approve the gate, request specific changes, or say what information is missing.",
            "questions": [
                "Do you approve the current gate?",
                "If not, what change or evidence would make it approvable?",
            ],
        }
    if ready_count:
        return {
            "where_we_are": "There is Beads-backed work ready for an implementation agent.",
            "why_it_matters": "The agent can move the project forward without asking you to manage the workflow manually.",
            "recommendation": "Let an implementer claim one ready ticket and execute its acceptance check.",
            "agent_will_do_next": (
                "Claim one ticket, make the smallest coherent change, run the acceptance command, "
                "and return review evidence."
            ),
            "what_i_need_from_you": "No action unless the ticket exposes a scope or product decision.",
            "questions": [],
        }
    if open_tasks or blocked_count:
        return {
            "where_we_are": "The spec has remaining planned work, but nothing is currently implementer-ready.",
            "why_it_matters": "The backlog needs agent planning/ticketing before workers can safely execute.",
            "recommendation": "Let the planner/ticket-planner convert the remaining approved scope into Beads-ready work.",
            "agent_will_do_next": (
                "Inspect open tasks and dependencies, sync or repair backlog tickets, "
                "and present any human decisions needed."
            ),
            "what_i_need_from_you": "Only answer questions where the spec does not define priority, acceptance, or scope.",
            "questions": [],
        }
    if git_state["clean"]:
        return {
            "where_we_are": "The workflow foundation is approved, clean, and has no ready implementation backlog.",
            "why_it_matters": "The next value-producing move is product discovery and roadmap shaping, not more workflow operation.",
            "recommendation": (
                "Have the PM/research agents draft the first product-roadmap options "
                "and come back with a short decision brief."
            ),
            "agent_will_do_next": (
                "Review the objective, inspect existing app placeholders and constraints, "
                "research likely first product slices, and propose 2-3 roadmap options."
            ),
            "what_i_need_from_you": "Answer the strategic product questions or approve the recommended discovery path.",
            "questions": [
                "Who is the first target user for this self-hosted agents project?",
                (
                    "Which first outcome matters most: a working local demo, framework comparison, "
                    "automation reliability, or an operator dashboard?"
                ),
                "What constraint should dominate the next roadmap choice: speed, learning value, reliability, or extensibility?",
            ],
        }
    return {
        "where_we_are": "The workflow is healthy, but local changes are still pending review or publication.",
        "why_it_matters": "Agents should checkpoint approved work before layering new planning or implementation on top.",
        "recommendation": "Let the agent finish the git checkpoint and then continue into product-roadmap discovery.",
        "agent_will_do_next": "Review status, commit or push approved work as appropriate, then produce the next product decision brief.",
        "what_i_need_from_you": "Only a decision if the pending changes have not already been approved.",
        "questions": [],
    }


def next_action_data() -> dict[str, Any]:
    bootstrap_status = bootstrap_data()
    bootstrap_ok = all(item["ok"] for item in bootstrap_status["checks"])
    context = context_index_data()
    health = health_status_data(deep=True)
    ready = ready_work_data()
    status = run(["git", "status", "--short", "--branch"])
    options = []

    if not bootstrap_ok or health["issues"]:
        options.append(
            {
                "id": "fix-health",
                "label": "Fix workflow health",
                "owner": "health-status",
                "command": "uv run awf health-status --deep --json",
                "agent_next_step": "Diagnose and repair the failing workflow health check.",
                "user_action": "Review only if the fix needs a scope or architecture decision.",
                "recommended": True,
            }
        )
    if ready.get("human_required"):
        options.append(
            {
                "id": "human-review",
                "label": "Review and approve the pending human gate",
                "owner": "human reviewer",
                "command": "uv run awf ready-work --json",
                "agent_next_step": "Present the approval brief, then record the human decision and rerun validation.",
                "user_action": "Approve, request changes, or say what evidence is missing.",
                "recommended": not options,
            }
        )
    if ready.get("ready"):
        options.append(
            {
                "id": "implement-ready-work",
                "label": "Claim one implementer-ready Beads item",
                "owner": "implementer",
                "command": "uv run awf claim-work --worker-id <id> --write",
                "agent_next_step": "Claim one ready ticket, implement it, and return acceptance evidence.",
                "user_action": "No action unless a product or scope decision appears.",
                "recommended": not options,
            }
        )
    if not options:
        options.append(
            {
                "id": "plan-next-work",
                "label": "Plan the next objective/spec/backlog action",
                "owner": "pm-steward",
                "command": "uv run awf workflow-run --mode plan --dry-run",
                "agent_next_step": "Research and draft the next product-roadmap options, then ask targeted CEO-level questions.",
                "user_action": "Choose a direction or answer the targeted questions.",
                "recommended": True,
            }
        )
    if len(options) < 2 and status.stdout.strip():
        options.append(
            {
                "id": "review-local-changes",
                "label": "Review local uncommitted changes",
                "owner": "reviewer",
                "command": "git diff",
                "agent_next_step": "Summarize pending changes and recommend commit, revise, or defer.",
                "user_action": "Approve the checkpoint or request changes.",
                "recommended": False,
            }
        )

    recommendation = next((option for option in options if option["recommended"]), options[0])
    executive_brief = executive_next_action(bootstrap_ok, health, ready, context, status.stdout.strip())
    return {
        "ok": health["ok"] and bootstrap_ok,
        "recommendation": recommendation,
        "options": options[:4],
        "process_position": process_position_summary(bootstrap_ok, health, ready, context, status.stdout.strip()),
        "executive_brief": executive_brief,
        "meta_process": meta_process_notes(health, ready, status.stdout.strip()),
        "bootstrap": bootstrap_status,
        "health": health,
        "ready_work": ready,
        "context": context,
        "git_status": status.stdout.strip(),
    }


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
        ("workflow-state-lint", workflow_state_lint_result),
        ("repo-hygiene", repo_hygiene_result),
    ]:
        if name in {"repo-hygiene", "workflow-state-lint"}:
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

    human_required = ready.get("human_required", [])
    if issues:
        next_action = "log issues and stop for planner triage"
    elif human_required:
        next_action = "human review required"
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
        "human_required_count": len(human_required),
        "claims": [rel(path) for path in sorted((ROOT / ".agent-runs" / "claims").glob("*.json"))],
        "next_action": next_action,
    }


def workflow_check(name: str) -> dict[str, Any]:
    args = argparse.Namespace(json=False)
    command = f"uv run awf {name}"
    if name == "bootstrap":
        data = bootstrap_data()
        ok = all(item["ok"] for item in data["checks"])
        return {"name": name, "command": command, "ok": ok, "data": data}
    if name == "spec-lint":
        code, data = spec_lint(args)
    elif name == "spec-kit-lint":
        code, data = spec_kit_lint(args)
    elif name == "bdd-lint":
        code, data = bdd_lint(args)
    elif name == "bdd-run-fixture":
        command = "uv run awf bdd-run --driver fixture"
        code, data = bdd_run_result("fixture")
    elif name == "review-gate":
        code, data = review_gate(args)
    elif name == "repo-hygiene":
        code, data = repo_hygiene_result()
    elif name == "workflow-state-lint":
        code, data = workflow_state_lint_result()
    elif name == "workflow-fixture-test":
        code, data = workflow_fixture_test_result(write=False, include_orchestration=False)
    else:
        return {"name": name, "command": command, "ok": False, "data": {"error": f"unknown check {name}"}}
    return {"name": name, "command": command, "ok": code == 0, "data": data}


def langgraph_python_candidate_smoke_result() -> dict[str, Any]:
    fixture = ROOT / "packages" / "comparison" / "fixtures" / "langgraph-python-decision-slice.json"
    runner = ROOT / "apps" / "langgraph-python" / "run.py"
    if not fixture.exists() or not runner.exists():
        return {
            "ok": False,
            "command": f"{sys.executable} {rel(runner)} --fixture {rel(fixture)}",
            "error": "missing runner or fixture",
            "fixture": rel(fixture),
            "runner": rel(runner),
        }
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "langgraph-python-run.json"
        command = [
            sys.executable,
            str(runner),
            "--fixture",
            str(fixture),
            "--output",
            str(output_path),
            "--pretty",
        ]
        proc = run(command)
        try:
            artifact = json.loads(output_path.read_text(encoding="utf-8")) if output_path.exists() else {}
        except json.JSONDecodeError as exc:
            artifact = {"decode_error": str(exc)}
        trace_path = output_path.with_suffix(".trace.json")
        evaluation_path = output_path.with_suffix(".evaluation.json")
        try:
            trace = json.loads(trace_path.read_text(encoding="utf-8")) if trace_path.exists() else {}
        except json.JSONDecodeError as exc:
            trace = {"decode_error": str(exc)}
        try:
            evaluation = json.loads(evaluation_path.read_text(encoding="utf-8")) if evaluation_path.exists() else {}
        except json.JSONDecodeError as exc:
            evaluation = {"decode_error": str(exc)}
        required = {
            "candidate_app_id": artifact.get("candidate_app_id") == "langgraph-python",
            "run_id": bool(artifact.get("run_id")),
            "recommendation": bool(artifact.get("recommendation", {}).get("next_slice")),
            "alternatives": bool(artifact.get("alternatives")),
            "questions": bool(artifact.get("questions")),
            "acceptance_check": artifact.get("acceptance_check") == "uv run awf workflow-fixture-test",
            "evidence_paths": bool(artifact.get("evidence_paths")),
            "command_used": "apps/langgraph-python/run.py" in artifact.get("command_used", ""),
            "graph_transitions": bool(artifact.get("graph", {}).get("transitions")),
            "trace_export": trace.get("provider") == "local-otel-json" and bool(trace.get("spans")),
            "trace_linked": artifact.get("evidence_paths", {}).get("trace_evidence") == str(trace_path),
            "evaluation_export": evaluation.get("passed") is True and bool(evaluation.get("criteria")),
            "evaluation_linked": artifact.get("evidence_paths", {}).get("evaluation_evidence") == str(evaluation_path),
            "evaluation_correlated": evaluation.get("run_id") == artifact.get("run_id")
            and evaluation.get("trace_id") == trace.get("trace_id"),
            "gap_notes": bool(artifact.get("gaps")) and bool(artifact.get("evidence_paths", {}).get("gap_notes")),
        }
        return {
            "ok": proc.returncode == 0 and all(required.values()),
            "command": " ".join(shlex.quote(item) for item in command),
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "fixture": rel(fixture),
            "output": str(output_path),
            "trace_output": str(trace_path),
            "evaluation_output": str(evaluation_path),
            "required": required,
            "artifact": artifact,
            "trace": trace,
            "evaluation": evaluation,
        }


def extract_acceptance_command(item: dict[str, Any] | None) -> str | None:
    if not item:
        return None
    for key in ["acceptance", "acceptance_command"]:
        if item.get(key):
            return str(item[key]).strip()
    text = "\n".join(str(item.get(key, "")) for key in ["description", "close_reason"])
    for line in text.splitlines():
        if line.startswith("Acceptance:"):
            return line.split(":", 1)[1].strip()
    work = item.get("work")
    return extract_acceptance_command(work) if isinstance(work, dict) else None


def issue_by_id(issue_id: str) -> dict[str, Any] | None:
    for issue in beads_issues():
        if issue.get("id") == issue_id:
            return issue
    return None


def active_claims() -> list[dict[str, Any]]:
    claims = []
    for path in sorted((ROOT / ".agent-runs" / "claims").glob("*.json")):
        data = read_json(path)
        if not data or data.get("error"):
            continue
        issue = issue_by_id(str(data.get("id", "")))
        if issue and issue.get("status") == "open":
            data["path"] = rel(path)
            data["issue"] = issue
            claims.append(data)
    return claims


def current_acceptance_item() -> dict[str, Any] | None:
    claims = sorted(active_claims(), key=lambda item: str(item.get("claimed_at", "")), reverse=True)
    if claims:
        return claims[0]
    ready = ready_work_data().get("ready", [])
    return ready[0] if ready else None


def run_acceptance_command(command: str | None) -> dict[str, Any]:
    if not command:
        return {
            "name": "acceptance",
            "command": "",
            "ok": False,
            "data": {"error": "no acceptance command found for active or ready work"},
        }
    if command == "uv run awf workflow-fixture-test":
        check = workflow_check("workflow-fixture-test")
        check["name"] = "acceptance"
        check["command"] = command
        return check
    if not command.startswith("uv run awf "):
        return {
            "name": "acceptance",
            "command": command,
            "ok": False,
            "data": {"error": "acceptance command is outside the awf command boundary"},
        }
    proc = run(shlex.split(command))
    return {
        "name": "acceptance",
        "command": command,
        "ok": proc.returncode == 0,
        "data": {"returncode": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()},
    }


def compact_check_result(check: dict[str, Any]) -> dict[str, Any]:
    data = check.get("data", {})
    detail = data.get("error") or data.get("next_action") or ""
    if not detail and data.get("errors"):
        detail = "; ".join(str(error) for error in data["errors"][:3])
    result = {
        "name": check.get("name"),
        "command": check.get("command"),
        "ok": check.get("ok"),
        "detail": detail,
    }
    if "results" in data:
        result["result_count"] = len(data["results"])
        result["failed_results"] = [item["name"] for item in data["results"] if not item.get("ok")]
    if "errors" in data:
        result["error_count"] = len(data["errors"])
    return result


def compact_acceptance_source(item: dict[str, Any] | None) -> dict[str, Any] | None:
    if not item:
        return None
    work = item.get("work") if isinstance(item.get("work"), dict) else item
    return {
        "id": work.get("id"),
        "title": work.get("title"),
        "status": work.get("status"),
        "external_ref": work.get("external_ref"),
    }


VERIFY_PROFILES = {
    "health": ["bootstrap", "review-gate", "workflow-state-lint", "repo-hygiene"],
    "ticket": ["spec-lint", "spec-kit-lint", "bdd-lint", "review-gate", "repo-hygiene", "workflow-state-lint", "acceptance"],
    "increment": [
        "bootstrap",
        "spec-lint",
        "spec-kit-lint",
        "bdd-lint",
        "bdd-run-fixture",
        "review-gate",
        "repo-hygiene",
        "workflow-state-lint",
        "workflow-fixture-test",
    ],
    "pre-merge": [
        "bootstrap",
        "spec-lint",
        "spec-kit-lint",
        "bdd-lint",
        "bdd-run-fixture",
        "review-gate",
        "repo-hygiene",
        "workflow-state-lint",
        "workflow-fixture-test",
    ],
}


def verify_next_action(profile: str, checks: list[dict[str, Any]], ready: dict[str, Any]) -> str:
    failed = [check for check in checks if not check["ok"]]
    if failed:
        if profile == "health":
            return "health-loop should log issues and stop implementation"
        return "fix failing checks before closing or integrating work"
    if ready.get("human_required"):
        return "pm-review-loop should present the human review gate"
    if profile == "ticket":
        return "record evidence and close the ticket if scope is complete"
    if profile in {"increment", "pre-merge"}:
        if ready.get("ready"):
            return "orchestrator-loop should continue assigning unblocked work"
        return "integrator-loop should prepare the increment review gate"
    return health_status_data(deep=False)["next_action"]


def verify_data(profile: str, write: bool) -> dict[str, Any]:
    if profile not in VERIFY_PROFILES:
        return {"ok": False, "profile": profile, "error": f"profile must be one of: {', '.join(VERIFY_PROFILES)}"}
    acceptance_item = current_acceptance_item()
    acceptance_command = extract_acceptance_command(acceptance_item)
    checks = []
    for name in VERIFY_PROFILES[profile]:
        checks.append(run_acceptance_command(acceptance_command) if name == "acceptance" else workflow_check(name))
    ready = ready_work_data()
    status = run(["git", "status", "--short", "--branch"]).stdout.strip()
    failed = [check for check in checks if not check["ok"]]
    data = {
        "ok": not failed,
        "profile": profile,
        "checks": checks,
        "failed_checks": [check["name"] for check in failed],
        "acceptance_command": acceptance_command,
        "acceptance_source": acceptance_item,
        "git": git_state_summary(status),
        "git_status": status,
        "ready_work": {
            "ready_count": len(ready.get("ready", [])),
            "blocked_count": len(ready.get("blocked", [])),
            "human_required_count": len(ready.get("human_required", [])),
            "source": ready.get("source"),
        },
        "review_gate": next((check["data"] for check in checks if check["name"] == "review-gate"), {}),
        "next_action": verify_next_action(profile, checks, ready),
    }
    if write:
        artifact = {
            "ok": data["ok"],
            "profile": profile,
            "failed_checks": data["failed_checks"],
            "acceptance_command": acceptance_command,
            "acceptance_source": compact_acceptance_source(acceptance_item),
            "git": data["git"],
            "ready_work": data["ready_work"],
            "review_gate_ok": data["review_gate"].get("ok"),
            "next_action": data["next_action"],
            "checks": [compact_check_result(check) for check in checks],
        }
        data["path"] = write_json_artifact("verifications", f"verify-{profile}", artifact)
    return data


def parse_spec_phase_tasks(spec_id: str, phase: str) -> list[dict[str, Any]]:
    tasks_path = ROOT / "specs" / spec_id / "tasks.md"
    if not tasks_path.exists():
        return []
    acceptance = tasks_acceptance_command(tasks_path)
    capture = False
    tasks = []
    for line in read_text(tasks_path).splitlines():
        if line.startswith("## "):
            capture = phase.lower() in line.lower()
            continue
        if not capture:
            continue
        match = TASK_RE.match(line)
        if match:
            item = match.groupdict()
            item["spec_id"] = spec_id
            item["done"] = item["done"].lower() == "x"
            item["parallel"] = item["parallel"] == "P"
            item["story"] = item["story"] or "shared"
            item["acceptance"] = acceptance
            tasks.append(item)
    return tasks


def default_increment_id(spec_id: str, phase: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", f"{spec_id}-{phase}".lower()).strip("-")
    return slug


def increment_path(increment_id: str) -> Path:
    safe_id = re.sub(r"[^A-Za-z0-9_.-]", "-", increment_id)
    return ROOT / ".agent-runs" / "increments" / f"{safe_id}.json"


def existing_increment_epic(increment_id: str) -> dict[str, Any] | None:
    external_ref = f".agent-runs/increments/{increment_id}.json"
    for issue in beads_issues():
        if issue.get("external_ref") == external_ref:
            return issue
    return None


def child_ticket_for_task(task: dict[str, Any], issues: list[dict[str, Any]]) -> dict[str, Any] | None:
    external_ref = task_external_ref(task)
    for issue in issues:
        if issue.get("external_ref") == external_ref:
            return issue
    return None


def stale_claims_for_increment(claims: list[dict[str, Any]], stale_hours: int = 2) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    stale = []
    for claim in claims:
        claimed_at = str(claim.get("claimed_at", ""))
        try:
            timestamp = datetime.fromisoformat(claimed_at)
        except ValueError:
            continue
        age_hours = (now - timestamp).total_seconds() / 3600
        if age_hours >= stale_hours:
            stale.append({"id": claim.get("id"), "path": claim.get("path"), "age_hours": round(age_hours, 2)})
    return stale


def increment_status_data(increment_id: str | None, spec_id: str, phase: str) -> dict[str, Any]:
    resolved_id = increment_id or default_increment_id(spec_id, phase)
    path = increment_path(resolved_id)
    existing = read_json(path)
    state = existing or {}
    tasks = parse_spec_phase_tasks(spec_id, phase)
    issues = beads_issues()
    child_tickets = []
    for task in tasks:
        ticket = child_ticket_for_task(task, issues)
        child_tickets.append(
            {
                "task_id": task["id"],
                "title": task["title"],
                "done": task["done"],
                "ticket_id": ticket.get("id") if ticket else None,
                "ticket_status": ticket.get("status") if ticket else "missing",
                "external_ref": task_external_ref(task),
            }
        )
    ready = ready_work_data()
    claims = active_claims()
    all_children_closed = child_tickets and all(
        item["done"] or item["ticket_status"] in {"closed", "resolved", "done"} for item in child_tickets
    )
    if ready.get("human_required"):
        review_status = "human-review-required"
        next_action = "pm-review-loop should present the human gate"
    elif ready.get("blocked") and not ready.get("ready"):
        review_status = "blocked"
        next_action = "pm-review-loop should triage blockers or decompose follow-up work"
    elif ready.get("ready"):
        review_status = "executing"
        next_action = "orchestrator-loop should assign unclaimed unblocked work"
    elif all_children_closed:
        review_status = "ready-for-increment-review"
        next_action = "integrator-loop should prepare the phase review PR"
    else:
        review_status = "planning"
        next_action = "pm-review-loop should refresh backlog from the approved spec phase"
    return {
        "ok": True,
        "increment_id": resolved_id,
        "path": rel(path),
        "exists": path.exists(),
        "state": state,
        "objective_id": current_objective_id(),
        "spec_id": spec_id,
        "phase": phase,
        "base_branch": "main",
        "feature_branch": f"codex/{resolved_id}",
        "child_tickets": child_tickets,
        "active_claims": claims,
        "active_worker_branches": [
            claim.get("worker_branch") for claim in claims if claim.get("worker_branch")
        ],
        "stale_claims": stale_claims_for_increment(claims),
        "blocked": ready.get("blocked", []),
        "validation_evidence": state.get("validation_evidence", []),
        "learning_proposals": state.get("learning_proposals", []),
        "ready_count": len(ready.get("ready", [])),
        "human_required": ready.get("human_required", []),
        "review_status": review_status,
        "next_action": next_action,
    }


def ensure_increment_epic(status: dict[str, Any], write: bool) -> dict[str, Any] | None:
    if not write:
        return existing_increment_epic(status["increment_id"])
    br = find_br()
    if not br:
        return None
    existing = existing_increment_epic(status["increment_id"])
    if existing:
        return existing
    desc = (
        f"Objective: {status['objective_id']}\n"
        f"Spec: {status['spec_id']}\n"
        f"Increment: {status['increment_id']}\n"
        f"Phase: {status['phase']}\n"
        "Acceptance: uv run awf verify --profile increment"
    )
    proc = run(
        [
            br,
            "create",
            f"Increment {status['increment_id']}",
            "--type",
            "epic",
            "--priority",
            "1",
            "--description",
            desc,
            "--external-ref",
            f".agent-runs/increments/{status['increment_id']}.json",
            "--labels",
            f"increment:{status['increment_id']},role:pm-review,role:orchestrator",
            "--json",
        ]
    )
    try:
        created = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None
    if isinstance(created, dict):
        return created
    if isinstance(created, list) and created:
        return created[0]
    return None


def increment_plan_data(increment_id: str | None, spec_id: str, phase: str, write: bool) -> dict[str, Any]:
    status = increment_status_data(increment_id, spec_id, phase)
    epic = ensure_increment_epic(status, write)
    status["beads_epic_id"] = epic.get("id") if epic else None
    if write:
        path = increment_path(status["increment_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        status["updated_at"] = datetime.now(timezone.utc).isoformat()
        status["exists"] = True
        artifact = dict(status)
        artifact.pop("state", None)
        path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        br = find_br()
        if br and epic:
            for item in status["child_tickets"]:
                ticket_id = item.get("ticket_id")
                if not ticket_id:
                    continue
                run([br, "update", ticket_id, "--add-label", f"increment:{status['increment_id']}", "--json"])
                run([br, "update", ticket_id, "--add-label", "role:worker", "--json"])
                run([br, "dep", "add", ticket_id, epic["id"], "--type", "parent-child", "--json"])
            run([br, "sync", "--flush-only"])
    return status


def automation_loop_data(
    role: str,
    write: bool,
    worker_id: str | None,
    increment_id: str | None,
    spec_id: str,
    phase: str,
) -> dict[str, Any]:
    if role not in {"pm-review", "orchestrator", "worker", "integrator", "health"}:
        return {
            "ok": False,
            "role": role,
            "error": "role must be pm-review, orchestrator, worker, integrator, or health",
        }
    status = increment_status_data(increment_id, spec_id, phase)
    if role == "health":
        verify = verify_data("health", write=write)
        return {
            "ok": verify["ok"],
            "role": role,
            "increment": status,
            "verify": verify,
            "next_action": verify["next_action"],
        }
    health = verify_data("health", write=False)
    if not health["ok"]:
        return {
            "ok": False,
            "role": role,
            "increment": status,
            "verify": health,
            "next_action": "health-loop should repair or log failures first",
        }
    if role == "pm-review":
        ticket_sync = (
            ticket_sync_data(write=write)
            if status["ready_count"] == 0
            else {"write": write, "proposals": [], "created": []}
        )
        planned = increment_plan_data(status["increment_id"], spec_id, phase, write=write)
        return {
            "ok": True,
            "role": role,
            "increment": planned,
            "ticket_sync": ticket_sync,
            "next_action": planned["next_action"],
        }
    if role == "orchestrator":
        ready = ready_work_data()
        if not ready.get("ready"):
            return {"ok": True, "role": role, "increment": status, "next_action": status["next_action"], "claim": None}
        chosen = ready["ready"][0]
        worker = worker_id or f"worker-{chosen.get('id', 'unassigned')}"
        claim = claim_work_data(worker_id=worker, write=write)
        worker_slug = re.sub(r"[^a-z0-9]+", "-", chosen.get("title", "work").lower()).strip("-")[:40]
        worker_branch = f"codex/{chosen.get('id', 'work')}-{worker_slug}"
        if write and claim.get("ok") and claim.get("claimed", {}).get("path"):
            claim_path_obj = ROOT / claim["claimed"]["path"]
            claim_data = read_json(claim_path_obj)
            if claim_data:
                claim_data.update(
                    {
                        "increment_id": status["increment_id"],
                        "feature_branch": status["feature_branch"],
                        "worker_branch": worker_branch,
                        "assigned_by": "automation-loop:orchestrator",
                    }
                )
                claim_path_obj.write_text(json.dumps(claim_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            else:
                claim = {
                    **claim,
                    "ok": False,
                    "reason": f"claim file is missing or invalid: {rel(claim_path_obj)}",
                }
        return {
            "ok": bool(claim.get("ok")),
            "role": role,
            "increment": status,
            "claim": claim,
            "worker_branch": worker_branch,
            "next_action": "worker-loop should implement the claimed ticket on its worker branch",
        }
    if role == "worker":
        claim = active_claims()
        if claim:
            claim_result = {"ok": True, "claimed": claim[0], "dry_run": False}
            next_action = (
                "implement one claimed ticket, run `uv run awf verify --profile ticket`, "
                "record evidence, and push the worker branch"
            )
        elif write:
            claim_result = claim_work_data(worker_id=worker_id or "worker", write=True)
            next_action = (
                "implement one claimed ticket, run `uv run awf verify --profile ticket`, "
                "record evidence, and push the worker branch"
            )
        else:
            ready = ready_work_data().get("ready", [])
            if ready:
                claim_result = {
                    "ok": True,
                    "claimed": {"work": ready[0], "worker_id": worker_id or "worker"},
                    "dry_run": True,
                    "ready_count": len(ready),
                }
                next_action = (
                    "implement one claimed ticket, run `uv run awf verify --profile ticket`, "
                    "record evidence, and push the worker branch"
                )
            elif status["review_status"] == "ready-for-increment-review":
                claim_result = None
                next_action = "no worker work remains; integrator-loop should prepare the phase review PR"
            else:
                claim_result = {"ok": False, "claimed": None, "dry_run": True, "ready_count": 0}
                next_action = "worker stopped"
        return {
            "ok": claim_result is None or bool(claim_result.get("ok")),
            "role": role,
            "increment": status,
            "claim": claim_result,
            "next_action": next_action,
        }
    verify = verify_data("increment", write=write)
    if status["review_status"] == "ready-for-increment-review" and verify["ok"]:
        next_action = "prepare the feature branch for human review against main"
    elif status["blocked"]:
        next_action = "route blockers to pm-review-loop before integrating"
    else:
        next_action = "wait for workers or continue orchestrating ready work"
    return {"ok": verify["ok"], "role": role, "increment": status, "verify": verify, "next_action": next_action}


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


def mark_task_done_text(text: str, task_id: str) -> tuple[str, bool]:
    changed = False
    lines = []
    task_pattern = re.compile(rf"^- \[(?P<done>[ xX])\] {re.escape(task_id)}(?P<rest>.*)$")
    for line in text.splitlines(keepends=True):
        line_body = line[:-1] if line.endswith("\n") else line
        newline = "\n" if line.endswith("\n") else ""
        match = task_pattern.match(line_body)
        if match and match.group("done").lower() != "x":
            line = f"- [X] {task_id}{match.group('rest')}{newline}"
            changed = True
        lines.append(line)
    return "".join(lines), changed


def mark_task_done(task: dict[str, Any], write: bool) -> dict[str, Any]:
    path = ROOT / task_source_path(task)
    original = read_text(path)
    updated, changed = mark_task_done_text(original, task["id"])
    if changed and write:
        path.write_text(updated, encoding="utf-8")
    return {"path": rel(path), "task_id": task["id"], "changed": changed}


def complete_work_data(issue_id: str | None, evidence: str, worker_id: str | None, write: bool) -> dict[str, Any]:
    br = find_br()
    if not br:
        return {"ok": False, "error": "Beads Rust br is unavailable"}

    item = issue_by_id(issue_id) if issue_id else current_acceptance_item()
    if not item:
        return {"ok": False, "error": "no issue id supplied and no active claim or ready work found"}

    work = item.get("work") if isinstance(item.get("work"), dict) else item
    target_issue_id = str(work.get("id", ""))
    issue = issue_by_id(target_issue_id)
    if not issue:
        return {"ok": False, "error": f"issue {target_issue_id or '<unknown>'} not found"}

    external_ref = issue.get("external_ref") or work.get("external_ref")
    if not external_ref:
        return {"ok": False, "issue_id": target_issue_id, "error": "issue has no external_ref"}
    task = task_by_external_ref(str(external_ref))
    if not task:
        return {"ok": False, "issue_id": target_issue_id, "external_ref": external_ref, "error": "linked task not found"}

    acceptance_command = extract_acceptance_command(issue) or extract_acceptance_command(work)
    acceptance = run_acceptance_command(acceptance_command)
    if not acceptance["ok"]:
        return {
            "ok": False,
            "issue_id": target_issue_id,
            "external_ref": external_ref,
            "acceptance": acceptance,
            "error": "acceptance check failed; no completion state was written",
        }

    comment_text = evidence.strip() or (
        f"Completion evidence recorded {datetime.now(timezone.utc).date().isoformat()}. "
        f"Acceptance passed: {acceptance_command}."
    )
    comment = None
    close = None
    task_update = mark_task_done(task, write=False)
    state_lint = {"ok": True, "skipped": True}
    sync = None

    if write:
        comment_proc = run(
            [br, "comments", "add", target_issue_id, "--author", worker_id or "awf", "--message", comment_text, "--json"]
        )
        comment = {
            "returncode": comment_proc.returncode,
            "stdout": comment_proc.stdout.strip(),
            "stderr": comment_proc.stderr.strip(),
        }
        if comment_proc.returncode != 0:
            return {
                "ok": False,
                "issue_id": target_issue_id,
                "acceptance": acceptance,
                "comment": comment,
                "error": "failed to record Beads evidence; task and issue were left unchanged",
            }

        close_reason = f"Completed {task['id']} through awf complete-work. Acceptance passed: {acceptance_command}."
        close_proc = run([br, "close", target_issue_id, "--reason", close_reason, "--json"])
        close = {
            "returncode": close_proc.returncode,
            "stdout": close_proc.stdout.strip(),
            "stderr": close_proc.stderr.strip(),
        }
        if close_proc.returncode != 0:
            return {
                "ok": False,
                "issue_id": target_issue_id,
                "acceptance": acceptance,
                "comment": comment,
                "close": close,
                "error": "failed to close Beads issue; task was left unchanged",
            }

        task_update = mark_task_done(task, write=True)
        sync_proc = run([br, "sync", "--flush-only"])
        sync = {
            "returncode": sync_proc.returncode,
            "stdout": sync_proc.stdout.strip(),
            "stderr": sync_proc.stderr.strip(),
        }
        code, state_lint_data = workflow_state_lint_result()
        state_lint = {"ok": code == 0, "data": state_lint_data}

    ok = acceptance["ok"] and state_lint.get("ok", False)
    return {
        "ok": ok,
        "write": write,
        "issue_id": target_issue_id,
        "external_ref": external_ref,
        "task_id": task["id"],
        "acceptance": acceptance,
        "comment": comment,
        "close": close,
        "task_update": task_update,
        "sync": sync,
        "state_lint": state_lint,
        "next_action": "commit completion checkpoint" if write and ok else "rerun with --write to complete work",
    }


def workflow_fixture_result_detail(result: dict[str, Any]) -> str:
    data = result.get("data")
    if not isinstance(data, dict):
        return ""
    if data.get("error"):
        return str(data["error"])
    if data.get("errors"):
        return "; ".join(str(error) for error in data["errors"][:3])
    if data.get("spec_errors"):
        return "; ".join(str(error) for error in data["spec_errors"][:3])
    claim = data.get("claim")
    if isinstance(claim, dict):
        if claim.get("reason"):
            return str(claim["reason"])
        if claim.get("dry_run") is False and claim.get("claimed", {}).get("path"):
            return f"using active claim {claim['claimed']['path']}"
        if claim.get("dry_run") is True:
            return "previewed a dry-run claim"
    if data.get("next_action"):
        return str(data["next_action"])
    if "ok" in data:
        return f"nested ok={data['ok']}"
    return ""


def workflow_fixture_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [
        {
            "name": str(result.get("name", "<unnamed>")),
            "detail": workflow_fixture_result_detail(result),
        }
        for result in results
        if not result.get("ok")
    ]
    return {
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "failed_results": failed,
    }


def worker_loop_non_mutating(worker: dict[str, Any], claim_paths_before: set[str], claim_paths_after: set[str]) -> bool:
    if claim_paths_before != claim_paths_after:
        return False
    increment = worker.get("increment")
    if isinstance(increment, dict) and increment.get("review_status") == "ready-for-increment-review":
        return worker.get("claim") is None
    claim = worker.get("claim")
    if not isinstance(claim, dict) or not claim.get("ok"):
        return False
    if claim.get("dry_run") is True:
        return True
    claimed = claim.get("claimed")
    if not isinstance(claimed, dict):
        return False
    path = claimed.get("path")
    return claim.get("dry_run") is False and isinstance(path, str) and path in claim_paths_before


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


def linked_worktree_hook_detection_result() -> dict[str, Any]:
    git = shutil.which("git")
    if not git:
        return {"ok": False, "error": "git missing"}

    with tempfile.TemporaryDirectory(prefix="awf-linked-worktree-") as temp_dir:
        root = Path(temp_dir)
        repo = root / "repo"
        worktree = root / "linked"
        commands = [
            [git, "init", str(repo)],
            [git, "-C", str(repo), "config", "core.hooksPath", ".githooks"],
        ]
        for command in commands:
            proc = subprocess.run(command, text=True, capture_output=True)
            if proc.returncode != 0:
                return {"ok": False, "command": command, "stderr": proc.stderr.strip()}

        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
        commit_commands = [
            [git, "-C", str(repo), "add", "README.md"],
            [
                git,
                "-C",
                str(repo),
                "-c",
                "user.email=fixture@example.com",
                "-c",
                "user.name=Fixture",
                "commit",
                "-m",
                "fixture",
            ],
            [git, "-C", str(repo), "worktree", "add", "--detach", str(worktree), "HEAD"],
        ]
        for command in commit_commands:
            proc = subprocess.run(command, text=True, capture_output=True)
            if proc.returncode != 0:
                return {"ok": False, "command": command, "stderr": proc.stderr.strip()}

        git_marker = worktree / ".git"
        detected_path = configured_hooks_path(worktree)
        return {
            "ok": git_marker.is_file() and detected_path == ".githooks",
            "git_marker_is_file": git_marker.is_file(),
            "hooksPath": detected_path,
        }


def workflow_fixture_test_result(write: bool, include_orchestration: bool = True) -> tuple[int, dict[str, Any]]:
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
    data = langgraph_python_candidate_smoke_result()
    results.append(
        {
            "name": "langgraph python deterministic fixture app runs",
            "ok": data["ok"],
            "data": data,
        }
    )
    code, data = repo_hygiene_result()
    results.append({"name": "root repo hygiene passes", "ok": code == 0, "data": data})
    code, data = workflow_state_lint_result()
    results.append({"name": "root workflow state lint passes", "ok": code == 0, "data": data})
    linked_worktree_hooks = linked_worktree_hook_detection_result()
    results.append(
        {
            "name": "linked worktree bootstrap detects hooks from git config",
            "ok": linked_worktree_hooks["ok"],
            "data": linked_worktree_hooks,
        }
    )
    ready = ready_work_data()
    results.append(
        {
            "name": "human review work is separated from implementer ready work",
            "ok": not any(is_human_review_issue(item) for item in ready.get("ready", []))
            and not (ready.get("human_required") and ready.get("ready")),
            "data": ready,
        }
    )
    ticket_data = ticket_sync_data(write=False)
    open_task_ids = {task["id"] for task in collect_tasks() if not task.get("done")}
    existing_open_task_ids = {
        proposal["id"] for proposal in ticket_data["proposals"] if proposal.get("existing_issue_id")
    }
    results.append(
        {
            "name": "ticket sync skips completed tasks and recognizes existing open work",
            "ok": (
                all(proposal["status"] == "open" for proposal in ticket_data["proposals"])
                and not any(proposal["id"] == "T032" for proposal in ticket_data["proposals"])
                and existing_open_task_ids.issubset(open_task_ids)
            ),
            "data": ticket_data,
        }
    )
    orchestration_tasks = [
        task for task in collect_tasks() if task["spec_id"] == "003-automated-increment-orchestration"
    ]
    results.append(
        {
            "name": "task parser preserves tasks.md acceptance command",
            "ok": bool(orchestration_tasks)
            and all(task["acceptance"] == "uv run awf verify --profile increment --json" for task in orchestration_tasks),
            "data": {"tasks": orchestration_tasks},
        }
    )
    synthetic_task = {
        "id": "T999",
        "title": "Synthetic complete task",
        "done": True,
        "spec_id": "001-workflow-foundation",
    }
    results.append(
        {
            "name": "workflow state lint detects completed task without Beads evidence",
            "ok": bool(completed_task_evidence_errors([synthetic_task], [])),
            "data": {"errors": completed_task_evidence_errors([synthetic_task], [])},
        }
    )
    synthetic_issue = {
        "id": "awf-synthetic",
        "title": "Synthetic implementation",
        "status": "open",
        "description": "Spec: 001-workflow-foundation",
    }
    results.append(
        {
            "name": "workflow state lint detects missing Beads metadata",
            "ok": bool(issue_metadata_errors([synthetic_issue])),
            "data": {"errors": issue_metadata_errors([synthetic_issue])},
        }
    )
    marked, changed = mark_task_done_text("- [ ] T123 [US1] Synthetic task\n", "T123")
    results.append(
        {
            "name": "complete-work can mark one linked task complete",
            "ok": changed and marked == "- [X] T123 [US1] Synthetic task\n",
            "data": {"changed": changed, "text": marked},
        }
    )
    synthetic_summary = workflow_fixture_summary(
        [{"name": "synthetic failure", "ok": False, "data": {"errors": ["clear failure detail"]}}]
    )
    results.append(
        {
            "name": "workflow fixture summary exposes failed check detail",
            "ok": synthetic_summary["failed_results"][0]["detail"] == "clear failure detail",
            "data": synthetic_summary,
        }
    )
    if include_orchestration:
        verify_health = verify_data("health", write=False)
        results.append(
            {
                "name": "verify health profile returns a next action",
                "ok": verify_health["ok"] and bool(verify_health.get("next_action")),
                "data": verify_health,
            }
        )
        verify_increment = verify_data("increment", write=False)
        results.append(
            {
                "name": "verify increment profile runs the full workflow gate",
                "ok": verify_increment["ok"]
                and "workflow-fixture-test" in {check["name"] for check in verify_increment["checks"]}
                and bool(verify_increment.get("next_action")),
                "data": verify_increment,
            }
        )
        increment_status = increment_status_data(None, "002-solution-comparison-roadmap", "Phase 3")
        results.append(
            {
                "name": "increment status exposes child work and next action",
                "ok": bool(increment_status["child_tickets"]) and bool(increment_status["next_action"]),
                "data": increment_status,
            }
        )
        pm_loop = automation_loop_data(
            role="pm-review",
            write=False,
            worker_id=None,
            increment_id=None,
            spec_id="002-solution-comparison-roadmap",
            phase="Phase 3",
        )
        results.append(
            {
                "name": "pm-review loop returns a bounded planning action",
                "ok": pm_loop["ok"] and bool(pm_loop["next_action"]),
                "data": pm_loop,
            }
        )
        orchestrator = automation_loop_data(
            role="orchestrator",
            write=False,
            worker_id="fixture-worker",
            increment_id=None,
            spec_id="002-solution-comparison-roadmap",
            phase="Phase 3",
        )
        results.append(
            {
                "name": "orchestrator loop selects a safe next action",
                "ok": orchestrator["ok"] and bool(orchestrator["next_action"]),
                "data": orchestrator,
            }
        )
        claim_paths_before = {rel(path) for path in sorted((ROOT / ".agent-runs" / "claims").glob("*.json"))}
        worker = automation_loop_data(
            role="worker",
            write=False,
            worker_id="fixture-worker",
            increment_id=None,
            spec_id="002-solution-comparison-roadmap",
            phase="Phase 3",
        )
        claim_paths_after = {rel(path) for path in sorted((ROOT / ".agent-runs" / "claims").glob("*.json"))}
        results.append(
            {
                "name": "worker loop reports claim state without mutating claims",
                "ok": worker["ok"] and worker_loop_non_mutating(worker, claim_paths_before, claim_paths_after),
                "data": {
                    **worker,
                    "claim_paths_before": sorted(claim_paths_before),
                    "claim_paths_after": sorted(claim_paths_after),
                },
            }
        )
        integrator = automation_loop_data(
            role="integrator",
            write=False,
            worker_id=None,
            increment_id=None,
            spec_id="002-solution-comparison-roadmap",
            phase="Phase 3",
        )
        results.append(
            {
                "name": "integrator loop verifies increment without merging to main",
                "ok": integrator["ok"] and "merge to main" not in integrator["next_action"].lower(),
                "data": integrator,
            }
        )

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
    summary = workflow_fixture_summary(results)
    data = {"ok": ok, "summary": summary, "results": results}
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
