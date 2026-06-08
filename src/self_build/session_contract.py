"""Session contract schema for future supervised builder runners."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

from .codelanes import Lane
from .goals import GoalSpec


SessionMode = Literal["plan", "worker", "repair", "review", "integration", "memory"]
READ_ONLY_MODES = {"plan", "review"}


@dataclass(frozen=True)
class SessionContract:
    mode: SessionMode
    lane: str
    cwd: str
    branch: str
    model: str
    approval_policy: str
    allowed_tools: list[str]
    hidden_tools: list[str]
    loaded_skills: list[str]
    max_turns: int
    max_log_bytes: int
    context_budget: int
    goal_file: str
    context_pack_path: str
    receipt_path: str
    run_file: str
    log_path: str
    done_path: str
    resume_from: str | None

    def __post_init__(self) -> None:
        if self.mode not in {"plan", "worker", "repair", "review", "integration", "memory"}:
            raise ValueError("mode must be plan, worker, repair, review, integration, or memory")
        for field_name in [
            "lane",
            "cwd",
            "branch",
            "model",
            "approval_policy",
            "goal_file",
            "context_pack_path",
            "receipt_path",
            "run_file",
            "log_path",
            "done_path",
        ]:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        for field_name in ["allowed_tools", "hidden_tools", "loaded_skills"]:
            value = getattr(self, field_name)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise ValueError(f"{field_name} must be a list of strings")
        for field_name in ["max_turns", "max_log_bytes", "context_budget"]:
            value = getattr(self, field_name)
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"{field_name} must be a non-negative integer")
        if self.mode in READ_ONLY_MODES and not self.is_read_only:
            raise ValueError(f"{self.mode} mode must be read-only")

    @property
    def is_read_only(self) -> bool:
        write_tools = {"apply_patch", "exec_write", "shell_write", "patch_apply"}
        return not any(tool in write_tools for tool in self.allowed_tools)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_session_contract(
    goal: GoalSpec,
    lane: Lane,
    *,
    mode: SessionMode,
    root: str | Path,
    output_dir: str | Path,
    context_pack_path: str | Path,
    model: str = "operator-selected",
    approval_policy: str = "operator-required",
    resume_from: str | None = None,
) -> SessionContract:
    out_dir = Path(output_dir)
    goal_file = out_dir / "goal.json"
    return SessionContract(
        mode=mode,
        lane=goal.lane,
        cwd=lane.source_root or str(Path(root).resolve()),
        branch=lane.expected_branch,
        model=model,
        approval_policy=approval_policy,
        allowed_tools=_allowed_tools(mode),
        hidden_tools=[],
        loaded_skills=[],
        max_turns=8 if mode in READ_ONLY_MODES else 20,
        max_log_bytes=20000,
        context_budget=12000,
        goal_file=str(goal_file),
        context_pack_path=str(Path(context_pack_path)),
        receipt_path=str(out_dir / "receipt.json"),
        run_file=str(out_dir / "runner_manifest.json"),
        log_path=str(out_dir / "runner.log"),
        done_path=str(out_dir / "runner.done"),
        resume_from=resume_from,
    )


def _allowed_tools(mode: SessionMode) -> list[str]:
    if mode in {"plan", "review"}:
        return ["read_files", "run_read_only_commands"]
    if mode == "worker":
        return ["read_files", "run_tests", "apply_patch"]
    if mode == "repair":
        return ["read_files", "run_tests", "apply_patch"]
    if mode == "integration":
        return ["read_files", "patch_queue"]
    if mode == "memory":
        return ["read_files", "write_docs_state"]
    raise ValueError(f"unsupported mode: {mode}")
