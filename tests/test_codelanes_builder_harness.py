import json
import os
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_build.codelanes import load_lane_registry
from self_build.context_pack import write_context_pack
from self_build.goals import GoalSpec
from self_build.patch_queue import create_patch_placeholder
from self_build.receipts import BuildReceipt


def test_loads_codelanes_yml():
    registry = load_lane_registry(ROOT / "config" / "codelanes.yml")
    assert {"demo", "docs", "webapp", "integration", "builder"} == set(registry.ids())
    assert registry.get("demo").source_root == "/repo"


def test_lane_guard_catches_wrong_worktree_and_branch_via_injection():
    registry = load_lane_registry(ROOT / "config" / "codelanes.yml")
    result = registry.guard("demo", cwd="/not-repo", branch="feature")
    assert not result.ok
    assert "worktree mismatch" in result.errors[0]
    assert "branch mismatch" in result.errors[1]


def test_goal_init_writes_valid_goal_json(tmp_path):
    _copy_config(tmp_path)
    result = subprocess.run(
        [
            str(ROOT / "scripts" / "codelanes"),
            "goal-init",
            "--lane",
            "demo",
            "--workflow",
            "narrow_implementation",
            "--objective",
            "demo bounded goal",
        ],
        cwd=str(ROOT),
        env={**os.environ, "CODELANES_ROOT": str(tmp_path)},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    goal_path = tmp_path / result.stdout.strip()
    data = json.loads(goal_path.read_text(encoding="utf-8"))
    goal = GoalSpec.from_dict(data)
    assert goal.lane == "demo"
    assert goal.objective == "demo bounded goal"
    assert "examples/fake-app" in goal.allowed_paths


def test_context_pack_writes_bounded_markdown(tmp_path):
    registry = load_lane_registry(ROOT / "config" / "codelanes.yml")
    lane = registry.get("demo")
    goal = GoalSpec.create(
        lane="demo",
        workflow="narrow_implementation",
        objective="demo bounded goal",
        allowed_paths=lane.owns,
        forbidden_paths=lane.forbidden,
        test_commands=lane.default_tests,
        goal_id="demo-test",
    )
    path = write_context_pack(goal, lane, root=tmp_path, max_chars=1000, max_lines=80)
    text = path.read_text(encoding="utf-8")
    assert "## Goal Summary" in text
    assert "## Receipt Requirements" in text
    assert len(text) <= 1000 + 120
    assert len(text.splitlines()) <= 83
    assert (tmp_path / "runs" / "build" / "demo-test" / "runner_manifest.json").exists()


def test_receipt_init_writes_valid_receipt_json(tmp_path):
    goal = GoalSpec.create(
        lane="demo",
        workflow="narrow_implementation",
        objective="demo bounded goal",
        allowed_paths=["examples/fake-app"],
        forbidden_paths=[".env"],
        test_commands=["python -m pytest examples/fake-app/tests"],
        goal_id="demo-receipt",
    )
    receipt = BuildReceipt.init_from_goal(goal, root=tmp_path, branch="main", changed_files=[])
    path = receipt.write_json(receipt.default_path(tmp_path))
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["goal_id"] == "demo-receipt"
    assert data["branch"] == "main"
    assert data["tests_run"] == ["python -m pytest examples/fake-app/tests"]


def test_patch_placeholder_can_be_created(tmp_path):
    goal = GoalSpec.create(
        lane="demo",
        workflow="narrow_implementation",
        objective="demo bounded goal",
        allowed_paths=["examples/fake-app"],
        forbidden_paths=[".env"],
        goal_id="demo-patch",
    )
    path = create_patch_placeholder(goal, root=tmp_path)
    assert path == tmp_path / "patches" / "pending" / "demo-patch.patch.md"
    assert "Apply patches: disabled" in path.read_text(encoding="utf-8")


def test_forbidden_paths_are_preserved_in_lane_config():
    registry = load_lane_registry(ROOT / "config" / "codelanes.yml")
    assert registry.get("builder").forbidden == [
        ".env",
        "secrets",
        "private",
        "runtime/production",
    ]


def _copy_config(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True)
    (config_dir / "codelanes.yml").write_text((ROOT / "config" / "codelanes.yml").read_text(encoding="utf-8"), encoding="utf-8")
