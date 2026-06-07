"""Context pack and dry-run runner manifest writers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .codelanes import Lane
from .goals import GoalSpec


def write_context_pack(
    goal: GoalSpec,
    lane: Lane,
    *,
    root: str | Path = ".",
    output_dir: str | Path | None = None,
    max_chars: int = 12000,
    max_lines: int = 180,
) -> Path:
    out_dir = Path(output_dir) if output_dir is not None else Path(root) / "runs" / "build" / goal.goal_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "context_pack.md"

    lines = [
        f"# Context Pack: {goal.goal_id}",
        "",
        "## Goal Summary",
        f"- Lane: {goal.lane}",
        f"- Workflow: {goal.workflow}",
        f"- Objective: {goal.objective}",
        f"- Created at: {goal.created_at}",
        "",
        "## Lane Summary",
        f"- Source root: {lane.source_root}",
        f"- Runtime data root: {lane.runtime_data_root}",
        f"- Expected branch: {lane.expected_branch}",
        f"- Tmux session: {lane.tmux_session}",
        "",
        "## Allowed Paths",
        *_bullets(goal.allowed_paths),
        "",
        "## Forbidden Paths",
        *_bullets(goal.forbidden_paths),
        "",
        "## Acceptance Criteria",
        *_bullets(goal.acceptance_criteria),
        "",
        "## Test Commands",
        *_bullets(goal.test_commands, empty="No test commands configured."),
        "",
        "## Runtime Commands",
        *_bullets(goal.runtime_commands, empty="No runtime commands configured."),
        "",
        "## Receipt Requirements",
        *_bullets(goal.proof_required),
        "",
        "## Stop Conditions",
        *_bullets(goal.stop_conditions),
    ]

    bounded = _bounded_lines(lines, max_chars=max_chars, max_lines=max_lines)
    out_path.write_text("\n".join(bounded) + "\n", encoding="utf-8")
    write_runner_manifest(goal, lane, root=root, output_dir=out_dir, context_pack_path=out_path)
    return out_path


def write_runner_manifest(
    goal: GoalSpec,
    lane: Lane,
    *,
    root: str | Path = ".",
    output_dir: str | Path | None = None,
    context_pack_path: str | Path,
) -> Path:
    out_dir = Path(output_dir) if output_dir is not None else Path(root) / "runs" / "build" / goal.goal_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "runner_manifest.json"
    manifest: dict[str, Any] = {
        "goal_id": goal.goal_id,
        "lane": goal.lane,
        "workflow": goal.workflow,
        "mode": "dry-run",
        "worker_launch": "disabled",
        "context_pack_path": str(Path(context_pack_path)),
        "source_root": lane.source_root,
        "expected_branch": lane.expected_branch,
        "tmux_session": lane.tmux_session,
        "test_commands": goal.test_commands,
        "max_repair_attempts": goal.max_repair_attempts,
        "next_action": "review context pack before launching any future worker",
    }
    out_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_path


def _bullets(items: list[str], *, empty: str = "None") -> list[str]:
    if not items:
        return [f"- {empty}"]
    return [f"- {item}" for item in items]


def _bounded_lines(lines: list[str], *, max_chars: int, max_lines: int) -> list[str]:
    out: list[str] = []
    used = 0
    for line in lines:
        next_used = used + len(line) + 1
        if len(out) >= max_lines or next_used > max_chars:
            out.append("")
            out.append("## Context Budget")
            out.append("- Context pack truncated by configured budget.")
            break
        out.append(line)
        used = next_used
    return out
