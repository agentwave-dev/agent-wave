import json
import os
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_build.codelanes import load_lane_registry
from self_build.goal_chains import create_minimal_chain, materialize_chain
from self_build.goals import GoalSpec
from self_build.receipts import BuildReceipt
from self_build.worker import collect_worker_result


def test_worker_plan_creates_prompt_and_run_manifest(tmp_path):
    goal_dir = _goal_dir(tmp_path)
    result = _run_cli(tmp_path, "worker-plan", "--goal-dir", str(goal_dir))

    assert result.returncode == 0
    assert (goal_dir / "worker_prompt.md").exists()
    assert (goal_dir / "worker_run.json").exists()
    run = json.loads((goal_dir / "worker_run.json").read_text(encoding="utf-8"))
    output = json.loads(result.stdout)
    assert run["status"] == "planned"
    assert run["execute"] is False
    assert output["status"] == "success"


def test_worker_run_without_execute_does_not_launch_codex(tmp_path):
    goal_dir = _goal_dir(tmp_path)
    result = _run_cli(tmp_path, "worker-run", "--goal-dir", str(goal_dir))
    run = json.loads((goal_dir / "worker_run.json").read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert run["status"] == "dry_run"
    assert "pid" not in run
    assert json.loads(result.stdout)["summary"] == "worker dry-run prepared; Codex was not launched"


def test_worker_run_execute_without_env_is_blocked(tmp_path):
    goal_dir = _goal_dir(tmp_path)
    result = _run_cli(tmp_path, "worker-run", "--goal-dir", str(goal_dir), "--execute", strip_worker_env=True)
    output = json.loads(result.stdout)
    run = json.loads((goal_dir / "worker_run.json").read_text(encoding="utf-8"))

    assert result.returncode == 1
    assert output["status"] == "blocked"
    assert run["status"] == "blocked"
    assert "CODELANES_ENABLE_WORKER_EXEC=1" in output["summary"]


def test_worker_peek_produces_compact_status(tmp_path):
    goal_dir = _goal_dir(tmp_path)
    _run_cli(tmp_path, "worker-run", "--goal-dir", str(goal_dir))
    result = _run_cli(tmp_path, "worker-peek", "--goal-dir", str(goal_dir))
    output = json.loads(result.stdout)

    assert result.returncode == 0
    assert "active_process=no" in output["summary"]
    assert "done_present=no" in output["summary"]
    assert "log_size_bytes=0" in output["summary"]
    assert (goal_dir / "worker_status.json").exists()


def test_worker_collect_handles_missing_completion_json_safely(tmp_path):
    goal_dir = _goal_dir(tmp_path)
    _run_cli(tmp_path, "worker-run", "--goal-dir", str(goal_dir))
    result = _run_cli(tmp_path, "worker-collect", "--goal-dir", str(goal_dir))
    status = json.loads((goal_dir / "worker_status.json").read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert status["completion_json"] == "missing"
    assert "done marker is not present" in json.loads(result.stdout)["summary"]


def test_worker_collect_updates_blocked_receipt_on_nonzero_done(tmp_path):
    goal_dir = _goal_dir(tmp_path)
    _run_cli(tmp_path, "worker-run", "--goal-dir", str(goal_dir))
    _write_done(goal_dir, 7)

    result = _run_cli(tmp_path, "worker-collect", "--goal-dir", str(goal_dir))
    receipt = json.loads((goal_dir / "receipt.json").read_text(encoding="utf-8"))

    assert result.returncode == 1
    assert receipt["status"] == "blocked"
    assert receipt["tests_build_result"] == "failed"
    assert receipt["blockers"] == ["worker exited nonzero: 7"]


def test_worker_collect_updates_complete_receipt_on_success_done(tmp_path):
    goal_dir = _goal_dir(tmp_path)
    _run_cli(tmp_path, "worker-run", "--goal-dir", str(goal_dir))
    completion = {
        "changed_files": ["examples/fake-app/README.md"],
        "commands_run": ["python -m pytest examples/fake-app/tests"],
        "tests_build_result": "passed",
        "blockers": [],
        "next_recommended_action": "Proceed to chain refresh",
        "raw_log_path": "/tmp/example.log",
    }
    (goal_dir / "completion.json").write_text(json.dumps(completion) + "\n", encoding="utf-8")
    _write_done(goal_dir, 0)

    result = _run_cli(tmp_path, "worker-collect", "--goal-dir", str(goal_dir))
    receipt = json.loads((goal_dir / "receipt.json").read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert receipt["status"] == "complete"
    assert receipt["tests_build_result"] == "passed"
    assert receipt["changed_files"] == ["examples/fake-app/README.md"]
    assert receipt["commands_run"] == ["python -m pytest examples/fake-app/tests"]


def test_worker_collect_refreshes_parent_chain(tmp_path):
    chain_dir = _materialized_chain(tmp_path)
    goal_dir = chain_dir / "goals" / "audit_current_state"
    _run_cli(tmp_path, "worker-run", "--goal-dir", str(goal_dir))
    _write_done(goal_dir, 0)

    result = _run_cli(tmp_path, "worker-collect", "--goal-dir", str(goal_dir))
    status = json.loads((chain_dir / "chain_status.json").read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert status["complete_count"] == 1
    assert status["next_incomplete_goal"] == "implement_small_change"


def test_worker_command_results_do_not_dump_raw_log_text(tmp_path):
    goal_dir = _goal_dir(tmp_path)
    _run_cli(tmp_path, "worker-run", "--goal-dir", str(goal_dir))
    run = json.loads((goal_dir / "worker_run.json").read_text(encoding="utf-8"))
    pathlib.Path(run["log"]).write_text("RAW LOG CONTENT SHOULD STAY OUT\n", encoding="utf-8")

    peek = _run_cli(tmp_path, "worker-peek", "--goal-dir", str(goal_dir))
    collect = collect_worker_result(goal_dir)

    assert "RAW LOG CONTENT" not in peek.stdout
    assert "RAW LOG CONTENT" not in json.dumps(collect.to_dict())


def _goal_dir(tmp_path):
    goal_dir = tmp_path / "runs" / "build" / "demo-worker"
    goal_dir.mkdir(parents=True)
    goal = GoalSpec.create(
        lane="demo",
        workflow="narrow_implementation",
        objective="Run one supervised fake-app goal",
        allowed_paths=["examples/fake-app"],
        forbidden_paths=[".env", "secrets"],
        test_commands=["python -m pytest examples/fake-app/tests"],
        goal_id="demo-worker",
    )
    goal.write_json(goal_dir / "goal.json")
    (goal_dir / "context_pack.md").write_text("# Context Pack\n", encoding="utf-8")
    BuildReceipt.init_from_goal(goal, root=tmp_path, branch="main", changed_files=[]).write_json(goal_dir / "receipt.json")
    _copy_config(tmp_path)
    return goal_dir


def _materialized_chain(tmp_path):
    _copy_config(tmp_path)
    registry = load_lane_registry(tmp_path / "config" / "codelanes.yml")
    chain_path = create_minimal_chain(
        lane="demo",
        title="Worker launcher demo",
        objective="Run one supervised fake-app goal",
        registry=registry,
        root=tmp_path,
    )
    return materialize_chain(chain_path, registry=registry, root=tmp_path)


def _write_done(goal_dir, exit_code):
    run = json.loads((goal_dir / "worker_run.json").read_text(encoding="utf-8"))
    pathlib.Path(run["done"]).write_text(json.dumps({"exit_code": exit_code}) + "\n", encoding="utf-8")


def _run_cli(tmp_path, *args, strip_worker_env=False):
    env = {**os.environ, "CODELANES_ROOT": str(tmp_path)}
    if strip_worker_env:
        env.pop("CODELANES_ENABLE_WORKER_EXEC", None)
    return subprocess.run(
        [str(ROOT / "scripts" / "codelanes"), *args],
        cwd=str(ROOT),
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _copy_config(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "codelanes.yml").write_text((ROOT / "config" / "codelanes.yml").read_text(encoding="utf-8"), encoding="utf-8")
