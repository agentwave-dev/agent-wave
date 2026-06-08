import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_build.results import CommandResult, blocked_result, error_result, success_result


def test_command_result_success_helper():
    result = success_result(
        "chain refreshed",
        artifacts=["runs/build_chains/demo/chain_status.json"],
        next_actions=["inspect next goal"],
    )

    assert result.success is True
    assert result.status == "success"
    assert result.to_dict()["summary"] == "chain refreshed"
    assert result.artifacts == ["runs/build_chains/demo/chain_status.json"]
    assert result.next_actions == ["inspect next goal"]


def test_command_result_error_helper():
    result = error_result(
        "receipt missing",
        recovery_hint="run goal-chain-materialize first",
    )

    assert result.success is False
    assert result.status == "error"
    assert result.recovery_hint == "run goal-chain-materialize first"


def test_command_result_blocked_helper():
    result = blocked_result(
        "goal blocked",
        next_actions=["operator expands allowed paths or updates receipt"],
    )

    assert result.success is False
    assert result.status == "blocked"
    assert result.next_actions == ["operator expands allowed paths or updates receipt"]


def test_command_result_validates_status_success_pair():
    with pytest.raises(ValueError, match="success must match status"):
        CommandResult(
            success=True,
            status="blocked",
            summary="bad result",
            artifacts=[],
            next_actions=[],
        )
