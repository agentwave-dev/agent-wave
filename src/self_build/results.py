"""Structured command result helpers for compact builder observations."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal


ResultStatus = Literal["success", "error", "blocked"]


@dataclass(frozen=True)
class CommandResult:
    success: bool
    status: ResultStatus
    summary: str
    artifacts: list[str]
    next_actions: list[str]
    recovery_hint: str | None = None
    raw_output_path: str | None = None

    def __post_init__(self) -> None:
        if self.status not in {"success", "error", "blocked"}:
            raise ValueError("status must be success, error, or blocked")
        if self.success != (self.status == "success"):
            raise ValueError("success must match status")
        if not isinstance(self.summary, str) or not self.summary.strip():
            raise ValueError("summary must be a non-empty string")
        for field_name in ["artifacts", "next_actions"]:
            value = getattr(self, field_name)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise ValueError(f"{field_name} must be a list of strings")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def success_result(
    summary: str,
    *,
    artifacts: list[str] | None = None,
    next_actions: list[str] | None = None,
    raw_output_path: str | None = None,
) -> CommandResult:
    return CommandResult(
        success=True,
        status="success",
        summary=summary,
        artifacts=artifacts or [],
        next_actions=next_actions or [],
        raw_output_path=raw_output_path,
    )


def error_result(
    summary: str,
    *,
    artifacts: list[str] | None = None,
    next_actions: list[str] | None = None,
    recovery_hint: str | None = None,
    raw_output_path: str | None = None,
) -> CommandResult:
    return CommandResult(
        success=False,
        status="error",
        summary=summary,
        artifacts=artifacts or [],
        next_actions=next_actions or [],
        recovery_hint=recovery_hint,
        raw_output_path=raw_output_path,
    )


def blocked_result(
    summary: str,
    *,
    artifacts: list[str] | None = None,
    next_actions: list[str] | None = None,
    recovery_hint: str | None = None,
    raw_output_path: str | None = None,
) -> CommandResult:
    return CommandResult(
        success=False,
        status="blocked",
        summary=summary,
        artifacts=artifacts or [],
        next_actions=next_actions or [],
        recovery_hint=recovery_hint,
        raw_output_path=raw_output_path,
    )
