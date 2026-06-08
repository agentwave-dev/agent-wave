import json
import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_build.codelanes import load_lane_registry
from self_build.context_pack import write_context_pack
from self_build.goals import GoalSpec
from self_build.session_contract import SessionContract, build_session_contract


def test_session_contract_has_required_fields(tmp_path):
    goal, lane = _goal_and_lane()
    contract = build_session_contract(
        goal,
        lane,
        mode="worker",
        root=tmp_path,
        output_dir=tmp_path / "runs" / "build" / goal.goal_id,
        context_pack_path=tmp_path / "runs" / "build" / goal.goal_id / "context_pack.md",
    )
    data = contract.to_dict()

    for field in [
        "mode",
        "lane",
        "cwd",
        "branch",
        "model",
        "approval_policy",
        "allowed_tools",
        "hidden_tools",
        "loaded_skills",
        "max_turns",
        "max_log_bytes",
        "context_budget",
        "goal_file",
        "context_pack_path",
        "receipt_path",
        "run_file",
        "log_path",
        "done_path",
        "resume_from",
    ]:
        assert field in data


@pytest.mark.parametrize("mode", ["plan", "review"])
def test_plan_and_review_modes_are_read_only(tmp_path, mode):
    goal, lane = _goal_and_lane()
    contract = build_session_contract(
        goal,
        lane,
        mode=mode,
        root=tmp_path,
        output_dir=tmp_path / "runs" / "build" / goal.goal_id,
        context_pack_path=tmp_path / "runs" / "build" / goal.goal_id / "context_pack.md",
    )

    assert contract.is_read_only
    assert "apply_patch" not in contract.allowed_tools


def test_read_only_modes_reject_write_tools():
    with pytest.raises(ValueError, match="plan mode must be read-only"):
        SessionContract(
            mode="plan",
            lane="demo",
            cwd="/repo",
            branch="main",
            model="operator-selected",
            approval_policy="operator-required",
            allowed_tools=["read_files", "apply_patch"],
            hidden_tools=[],
            loaded_skills=[],
            max_turns=8,
            max_log_bytes=20000,
            context_budget=12000,
            goal_file="goal.json",
            context_pack_path="context_pack.md",
            receipt_path="receipt.json",
            run_file="runner_manifest.json",
            log_path="runner.log",
            done_path="runner.done",
            resume_from=None,
        )


def test_runner_manifest_includes_session_contract(tmp_path):
    goal, lane = _goal_and_lane()
    context_pack = write_context_pack(goal, lane, root=tmp_path)
    manifest_path = context_pack.parent / "runner_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    contract = manifest["session_contract"]
    assert contract["mode"] == "worker"
    assert contract["lane"] == "demo"
    assert contract["context_pack_path"] == str(context_pack)
    assert contract["receipt_path"].endswith("receipt.json")
    assert "apply_patch" in contract["allowed_tools"]


def _goal_and_lane():
    registry = load_lane_registry(ROOT / "config" / "codelanes.yml")
    lane = registry.get("demo")
    goal = GoalSpec.create(
        lane="demo",
        workflow="narrow_implementation",
        objective="demo bounded goal",
        allowed_paths=lane.owns,
        forbidden_paths=lane.forbidden,
        test_commands=lane.default_tests,
        goal_id="demo-session-contract",
    )
    return goal, lane
