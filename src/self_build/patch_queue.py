"""Patch queue placeholder support for the builder harness MVP."""

from __future__ import annotations

from pathlib import Path

from .goals import GoalSpec


def create_patch_placeholder(
    goal: GoalSpec,
    *,
    root: str | Path = ".",
    summary: str = "No diff has been queued or applied for this goal.",
) -> Path:
    pending_dir = Path(root) / "patches" / "pending"
    pending_dir.mkdir(parents=True, exist_ok=True)
    out_path = pending_dir / f"{goal.goal_id}.patch.md"
    lines = [
        f"# Patch Placeholder: {goal.goal_id}",
        "",
        f"- Lane: {goal.lane}",
        f"- Workflow: {goal.workflow}",
        f"- Objective: {goal.objective}",
        f"- Status: {summary}",
        "- Apply patches: disabled in Builder Harness MVP v0.",
    ]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path
