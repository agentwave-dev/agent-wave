"""Lane registry loading and guard checks for the CodeLanes builder harness."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import subprocess
from typing import Any


@dataclass(frozen=True)
class Lane:
    lane_id: str
    source_root: str
    runtime_data_root: str
    expected_branch: str
    tmux_session: str
    owns: list[str]
    forbidden: list[str]
    proof_roots: list[str]
    default_tests: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GuardResult:
    ok: bool
    lane: str
    expected_worktree: str
    actual_worktree: str
    expected_branch: str
    actual_branch: str
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LaneRegistry:
    def __init__(self, lanes: dict[str, Lane]) -> None:
        self._lanes = lanes

    def ids(self) -> list[str]:
        return sorted(self._lanes)

    def get(self, lane_id: str) -> Lane:
        try:
            return self._lanes[lane_id]
        except KeyError as exc:
            known = ", ".join(self.ids()) or "none"
            raise ValueError(f"unknown lane '{lane_id}'. known lanes: {known}") from exc

    def to_dict(self) -> dict[str, Any]:
        return {lane_id: lane.to_dict() for lane_id, lane in sorted(self._lanes.items())}

    def guard(
        self,
        lane_id: str,
        *,
        cwd: str | Path | None = None,
        branch: str | None = None,
    ) -> GuardResult:
        lane = self.get(lane_id)
        actual_worktree = str(Path(cwd).resolve() if cwd is not None else Path.cwd().resolve())
        actual_branch = branch if branch is not None else current_branch(actual_worktree)
        expected_worktree = str(Path(lane.source_root).resolve())
        errors: list[str] = []

        if actual_worktree != expected_worktree:
            errors.append(f"worktree mismatch: expected {expected_worktree}, got {actual_worktree}")
        if actual_branch != lane.expected_branch:
            errors.append(f"branch mismatch: expected {lane.expected_branch}, got {actual_branch}")

        return GuardResult(
            ok=not errors,
            lane=lane_id,
            expected_worktree=expected_worktree,
            actual_worktree=actual_worktree,
            expected_branch=lane.expected_branch,
            actual_branch=actual_branch,
            errors=errors,
        )


def current_branch(cwd: str | Path) -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=str(cwd),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def load_lane_registry(path: str | Path = "config/codelanes.yml") -> LaneRegistry:
    config_path = Path(path)
    data = _parse_lane_config(config_path)
    lanes_raw = data.get("lanes")
    if not isinstance(lanes_raw, dict):
        raise ValueError(f"{config_path} must contain a lanes mapping")

    lanes: dict[str, Lane] = {}
    for lane_id, raw in lanes_raw.items():
        if not isinstance(raw, dict):
            raise ValueError(f"lane '{lane_id}' must be a mapping")
        lanes[lane_id] = _lane_from_mapping(lane_id, raw)
    return LaneRegistry(lanes)


def _lane_from_mapping(lane_id: str, raw: dict[str, Any]) -> Lane:
    required_scalars = [
        "source_root",
        "runtime_data_root",
        "expected_branch",
        "tmux_session",
    ]
    required_lists = ["owns", "forbidden", "proof_roots", "default_tests"]
    missing = [key for key in required_scalars + required_lists if key not in raw]
    if missing:
        raise ValueError(f"lane '{lane_id}' missing required fields: {', '.join(missing)}")

    values: dict[str, Any] = {}
    for key in required_scalars:
        value = raw[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"lane '{lane_id}' field '{key}' must be a non-empty string")
        values[key] = value
    for key in required_lists:
        value = raw[key]
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ValueError(f"lane '{lane_id}' field '{key}' must be a list of strings")
        values[key] = list(value)

    return Lane(lane_id=lane_id, **values)


def _parse_lane_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    root: dict[str, Any] = {}
    lanes: dict[str, dict[str, Any]] = {}
    root["lanes"] = lanes
    current_lane: str | None = None
    current_key: str | None = None

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))

        if indent == 0:
            if stripped != "lanes:":
                raise ValueError(f"{path}:{lineno}: only top-level 'lanes:' is supported")
            continue

        if indent == 2 and stripped.endswith(":"):
            current_lane = stripped[:-1]
            if not current_lane:
                raise ValueError(f"{path}:{lineno}: empty lane id")
            lanes[current_lane] = {}
            current_key = None
            continue

        if current_lane is None:
            raise ValueError(f"{path}:{lineno}: field without lane")

        if indent == 4 and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            lanes[current_lane][key] = [] if value == "" else value
            continue

        if indent == 6 and stripped.startswith("- ") and current_key:
            target = lanes[current_lane].setdefault(current_key, [])
            if not isinstance(target, list):
                raise ValueError(f"{path}:{lineno}: scalar field cannot accept list item")
            target.append(stripped[2:].strip())
            continue

        raise ValueError(f"{path}:{lineno}: unsupported config syntax")

    return root
