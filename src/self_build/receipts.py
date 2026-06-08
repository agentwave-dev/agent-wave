"""Build receipt schema and writer."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import subprocess
from typing import Any

from .goals import GoalSpec


@dataclass(frozen=True)
class BuildReceipt:
    goal_id: str
    lane: str
    workflow: str
    worktree: str
    branch: str
    changed_files: list[str]
    tests_run: list[str]
    exit_codes: dict[str, int | None]
    blocker_classification: str
    patch_path: str
    next_action: str

    def __post_init__(self) -> None:
        for field_name in ["goal_id", "lane", "workflow", "worktree", "blocker_classification", "patch_path", "next_action"]:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not isinstance(self.changed_files, list) or not all(isinstance(item, str) for item in self.changed_files):
            raise ValueError("changed_files must be a list of strings")
        if not isinstance(self.tests_run, list) or not all(isinstance(item, str) for item in self.tests_run):
            raise ValueError("tests_run must be a list of strings")
        if not isinstance(self.exit_codes, dict):
            raise ValueError("exit_codes must be a mapping")

    @classmethod
    def init_from_goal(
        cls,
        goal: GoalSpec,
        *,
        root: str | Path = ".",
        branch: str | None = None,
        changed_files: list[str] | None = None,
        tests_run: list[str] | None = None,
        exit_codes: dict[str, int | None] | None = None,
        blocker_classification: str = "none",
        patch_path: str | None = None,
        next_action: str = "run configured validation and update receipt",
    ) -> "BuildReceipt":
        root_path = Path(root).resolve()
        return cls(
            goal_id=goal.goal_id,
            lane=goal.lane,
            workflow=goal.workflow,
            worktree=str(root_path),
            branch=branch if branch is not None else _current_branch(root_path),
            changed_files=changed_files if changed_files is not None else _changed_files(root_path),
            tests_run=tests_run if tests_run is not None else list(goal.test_commands),
            exit_codes=exit_codes if exit_codes is not None else {command: None for command in goal.test_commands},
            blocker_classification=blocker_classification,
            patch_path=patch_path or str(Path("patches") / "pending" / f"{goal.goal_id}.patch.md"),
            next_action=next_action,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BuildReceipt":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write_json(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return out

    def default_path(self, root: str | Path = ".") -> Path:
        return Path(root) / "runs" / "build" / self.goal_id / "receipt.json"


def write_receipt(goal: GoalSpec, *, root: str | Path = ".") -> Path:
    receipt = BuildReceipt.init_from_goal(goal, root=root)
    return receipt.write_json(receipt.default_path(root))


def update_receipt(
    goal_dir: str | Path,
    *,
    status: str | None = None,
    tests_result: str | None = None,
    commands: list[str] | None = None,
    changed_files: list[str] | None = None,
    blockers: list[str] | None = None,
    next_action: str | None = None,
) -> Path:
    if status is not None and status not in {"complete", "blocked"}:
        raise ValueError("status must be complete or blocked")
    if tests_result is not None and tests_result not in {"passed", "failed", "not_run"}:
        raise ValueError("tests_result must be passed, failed, or not_run")

    receipt_path = Path(goal_dir) / "receipt.json"
    data = json.loads(receipt_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("receipt JSON must be an object")

    if status is not None:
        data["status"] = status
        data["blocker_classification"] = "none" if status == "complete" else "blocked"
    if tests_result is not None:
        data["tests_build_result"] = tests_result
    elif status == "complete" and "tests_build_result" not in data:
        data["tests_build_result"] = "not_run"

    if commands:
        existing = _string_list(data.get("commands_run") or data.get("tests_run") or [])
        data["commands_run"] = _append_unique(existing, commands)
        data["tests_run"] = _append_unique(_string_list(data.get("tests_run") or []), commands)
        exit_codes = data.get("exit_codes")
        if not isinstance(exit_codes, dict):
            exit_codes = {}
        default_code = 0 if data.get("tests_build_result") == "passed" else None
        for command in commands:
            exit_codes.setdefault(command, default_code)
        data["exit_codes"] = exit_codes

    if changed_files:
        data["changed_files"] = _append_unique(_string_list(data.get("changed_files") or []), changed_files)

    if blockers:
        data["blockers"] = _append_unique(_string_list(data.get("blockers") or []), blockers)
        data["blocker_classification"] = "blocked"

    if next_action is not None:
        data["next_recommended_action"] = next_action
        data["next_action"] = next_action

    receipt_path.write_text(json.dumps(data, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")
    return receipt_path


def _append_unique(existing: list[str], additions: list[str]) -> list[str]:
    result = list(existing)
    seen = set(result)
    for item in additions:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _current_branch(cwd: Path) -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=str(cwd),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _changed_files(cwd: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=str(cwd),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return []
    changed: list[str] = []
    for line in result.stdout.splitlines():
        if len(line) >= 4:
            changed.append(line[3:])
    return changed
