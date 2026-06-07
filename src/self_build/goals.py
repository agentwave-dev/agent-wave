"""GoalSpec schema and JSON helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class GoalSpec:
    goal_id: str
    lane: str
    workflow: str
    objective: str
    allowed_paths: list[str]
    forbidden_paths: list[str]
    acceptance_criteria: list[str]
    test_commands: list[str]
    runtime_commands: list[str]
    max_repair_attempts: int
    proof_required: list[str]
    stop_conditions: list[str]
    created_at: str

    def __post_init__(self) -> None:
        _require_text("goal_id", self.goal_id)
        _require_text("lane", self.lane)
        _require_text("workflow", self.workflow)
        _require_text("objective", self.objective)
        if self.max_repair_attempts < 0:
            raise ValueError("max_repair_attempts must be >= 0")
        for field_name in [
            "allowed_paths",
            "forbidden_paths",
            "acceptance_criteria",
            "test_commands",
            "runtime_commands",
            "proof_required",
            "stop_conditions",
        ]:
            value = getattr(self, field_name)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise ValueError(f"{field_name} must be a list of strings")

    @classmethod
    def create(
        cls,
        *,
        lane: str,
        workflow: str,
        objective: str,
        allowed_paths: list[str],
        forbidden_paths: list[str],
        acceptance_criteria: list[str] | None = None,
        test_commands: list[str] | None = None,
        runtime_commands: list[str] | None = None,
        max_repair_attempts: int = 1,
        proof_required: list[str] | None = None,
        stop_conditions: list[str] | None = None,
        goal_id: str | None = None,
    ) -> "GoalSpec":
        safe_lane = re.sub(r"[^A-Za-z0-9_.-]", "-", lane).strip("-") or "lane"
        return cls(
            goal_id=goal_id or f"{safe_lane}-{uuid4().hex[:12]}",
            lane=lane,
            workflow=workflow,
            objective=objective,
            allowed_paths=list(allowed_paths),
            forbidden_paths=list(forbidden_paths),
            acceptance_criteria=acceptance_criteria or ["All requested artifacts are created.", "Configured tests pass."],
            test_commands=test_commands or [],
            runtime_commands=runtime_commands or [],
            max_repair_attempts=max_repair_attempts,
            proof_required=proof_required or ["receipt.json", "context_pack.md"],
            stop_conditions=stop_conditions or [
                "Wrong worktree or branch.",
                "Unrelated dirty tracked files.",
                "Forbidden path or private data would be touched.",
            ],
            created_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GoalSpec":
        return cls(**data)

    @classmethod
    def read_json(cls, path: str | Path) -> "GoalSpec":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write_json(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return out

    def default_path(self, root: str | Path = ".") -> Path:
        return Path(root) / "runs" / "build" / self.goal_id / "goal.json"


def _require_text(field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
