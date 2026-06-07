import json
import os
import pathlib
import subprocess
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_build.codelanes import load_lane_registry
from self_build.goal_chains import load_chain_file


def test_goal_chain_init_creates_chain_artifact(tmp_path):
    _copy_config(tmp_path)
    result = _run_cli(
        tmp_path,
        "goal-chain-init",
        "--lane",
        "demo",
        "--title",
        "Demo chain",
        "--objective",
        "Make one small validated fake-app improvement",
    )
    chain_path = tmp_path / result.stdout.strip()
    data = json.loads(chain_path.read_text(encoding="utf-8"))
    assert data["chain_id"].startswith("demo-demo-chain")
    assert data["execution_mode"] == "sequential"
    assert len(data["goals"]) == 3


def test_goal_chain_materialize_creates_child_artifacts(tmp_path):
    chain_path = _init_chain(tmp_path)
    result = _run_cli(tmp_path, "goal-chain-materialize", "--chain-file", str(chain_path))
    chain_dir = tmp_path / result.stdout.strip()

    child_dirs = sorted((chain_dir / "goals").iterdir())
    assert [path.name for path in child_dirs] == [
        "audit_current_state",
        "implement_small_change",
        "validate_and_receipt",
    ]
    for child in child_dirs:
        assert (child / "goal.json").exists()
        assert (child / "context_pack.md").exists()
        assert (child / "receipt.json").exists()
    assert (chain_dir / "chain_status.json").exists()
    assert (chain_dir / "chain_completion.md").exists()


def test_goal_chain_status_prints_compact_output(tmp_path):
    chain_path = _init_chain(tmp_path)
    chain_dir = tmp_path / _run_cli(tmp_path, "goal-chain-materialize", "--chain-file", str(chain_path)).stdout.strip()
    result = _run_cli(tmp_path, "goal-chain-status", "--chain-file", str(chain_dir))

    output = result.stdout
    assert "chain id:" in output
    assert "goal count: 3" in output
    assert "receipt status:" in output
    assert "next incomplete goal: audit_current_state" in output
    assert "{" not in output


def test_goal_chain_rejects_missing_required_fields(tmp_path):
    _copy_config(tmp_path)
    bad_chain = tmp_path / "bad-chain.json"
    bad_chain.write_text(json.dumps({"chain_id": "bad", "goals": []}) + "\n", encoding="utf-8")
    registry = load_lane_registry(tmp_path / "config" / "codelanes.yml")

    with pytest.raises(ValueError, match="missing required fields"):
        load_chain_file(bad_chain, registry=registry)


def test_generated_context_packs_remain_bounded(tmp_path):
    chain_path = _init_chain(tmp_path)
    chain_dir = tmp_path / _run_cli(tmp_path, "goal-chain-materialize", "--chain-file", str(chain_path)).stdout.strip()

    for context_pack in chain_dir.glob("goals/*/context_pack.md"):
        text = context_pack.read_text(encoding="utf-8")
        assert len(text) <= 12000
        assert len(text.splitlines()) <= 180


def _init_chain(tmp_path):
    _copy_config(tmp_path)
    result = _run_cli(
        tmp_path,
        "goal-chain-init",
        "--lane",
        "demo",
        "--title",
        "Demo chain",
        "--objective",
        "Make one small validated fake-app improvement",
    )
    return tmp_path / result.stdout.strip()


def _run_cli(tmp_path, *args):
    return subprocess.run(
        [str(ROOT / "scripts" / "codelanes"), *args],
        cwd=str(ROOT),
        env={**os.environ, "CODELANES_ROOT": str(tmp_path)},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _copy_config(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "codelanes.yml").write_text((ROOT / "config" / "codelanes.yml").read_text(encoding="utf-8"), encoding="utf-8")
