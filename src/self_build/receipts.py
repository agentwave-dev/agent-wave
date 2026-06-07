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
