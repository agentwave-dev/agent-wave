"""Supervised worker launcher for one bounded CodeLanes goal."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any

from .goal_chains import refresh_chain
from .goals import GoalSpec
from .results import CommandResult, blocked_result, error_result, success_result


CODEX_BIN = Path("/home/joe/.npm-global/bin/codex")


def resolve_goal_dir(goal_dir: str | Path) -> Path:
    resolved = Path(goal_dir).expanduser().resolve()
    if not resolved.is_dir():
        raise FileNotFoundError(f"goal directory not found: {resolved}")
    if not (resolved / "goal.json").exists():
        raise FileNotFoundError(f"goal.json missing in {resolved}")
    return resolved


def load_goal_artifacts(goal_dir: str | Path) -> dict[str, Any]:
    directory = resolve_goal_dir(goal_dir)
    goal = GoalSpec.read_json(directory / "goal.json")
    root = _infer_root(directory)
    artifacts = {
        "goal_dir": directory,
        "root": root,
        "goal": goal,
        "goal_file": directory / "goal.json",
        "context_pack": directory / "context_pack.md",
        "receipt": directory / "receipt.json",
        "prompt": directory / "worker_prompt.md",
        "run": directory / "worker_run.json",
        "status": directory / "worker_status.json",
    }
    return artifacts


def prepare_worker_prompt(goal_dir: str | Path) -> Path:
    artifacts = load_goal_artifacts(goal_dir)
    goal: GoalSpec = artifacts["goal"]
    prompt_path: Path = artifacts["prompt"]
    lines = [
        f"# CodeLanes Worker Prompt: {goal.goal_id}",
        "",
        "## Bounded Task",
        goal.objective,
        "",
        "## Required Artifacts",
        f"- Context pack: {_display_path(artifacts['context_pack'], artifacts['root'])}",
        f"- Goal file: {_display_path(artifacts['goal_file'], artifacts['root'])}",
        f"- Receipt path: {_display_path(artifacts['receipt'], artifacts['root'])}",
        "",
        "## Boundaries",
        "- Work only inside the allowed paths below.",
        "- Do not touch forbidden paths.",
        "- Do not expose raw logs in receipts, docs, reports, or command output.",
        "",
        "## Allowed Paths",
        *_bullets(goal.allowed_paths),
        "",
        "## Forbidden Paths",
        *_bullets(goal.forbidden_paths),
        "",
        "## Tests",
        *_bullets(goal.test_commands, empty="No tests configured; explain why validation is not_run."),
        "",
        "## Completion Requirement",
        "- Update receipt.json or write completion.json before exiting.",
        "- completion.json may be written at reports/codex_runs/<task>/completion.json or in this goal directory.",
        "- Include compact JSON fields: changed_files, commands_run, tests_build_result, blockers, next_recommended_action, raw_log_path.",
        "- Mark blockers clearly when the bounded task cannot be completed.",
    ]
    prompt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return prompt_path


def create_worker_run_manifest(goal_dir: str | Path, execute: bool = False) -> Path:
    artifacts = load_goal_artifacts(goal_dir)
    prompt_path = prepare_worker_prompt(artifacts["goal_dir"])
    manifest = _base_manifest(artifacts, prompt_path=prompt_path, execute=execute)
    if not execute:
        manifest["status"] = "planned"
        manifest["next_action"] = "run worker-run --execute with CODELANES_ENABLE_WORKER_EXEC=1 to launch one supervised worker"
    artifacts["run"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_status(artifacts["goal_dir"], _status_from_manifest(manifest))
    return artifacts["run"]


def launch_worker(goal_dir: str | Path, execute: bool = False) -> CommandResult:
    artifacts = load_goal_artifacts(goal_dir)
    prompt_path = prepare_worker_prompt(artifacts["goal_dir"])
    manifest = _base_manifest(artifacts, prompt_path=prompt_path, execute=execute)

    if not execute:
        manifest["status"] = "dry_run"
        manifest["next_action"] = "review worker_prompt.md, then rerun with --execute and CODELANES_ENABLE_WORKER_EXEC=1 if approved"
        artifacts["run"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _write_status(artifacts["goal_dir"], _status_from_manifest(manifest))
        return success_result(
            "worker dry-run prepared; Codex was not launched",
            artifacts=[_rel(artifacts["prompt"], artifacts["root"]), _rel(artifacts["run"], artifacts["root"]), _rel(artifacts["status"], artifacts["root"])],
            next_actions=[manifest["next_action"]],
        )

    if os.environ.get("CODELANES_ENABLE_WORKER_EXEC") != "1":
        manifest["status"] = "blocked"
        manifest["next_action"] = "set CODELANES_ENABLE_WORKER_EXEC=1 only after operator approval"
        artifacts["run"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _write_status(artifacts["goal_dir"], _status_from_manifest(manifest, next_action=manifest["next_action"]))
        return blocked_result(
            "worker execution blocked by missing CODELANES_ENABLE_WORKER_EXEC=1",
            artifacts=[_rel(artifacts["prompt"], artifacts["root"]), _rel(artifacts["run"], artifacts["root"]), _rel(artifacts["status"], artifacts["root"])],
            next_actions=[manifest["next_action"]],
            recovery_hint="dry-run artifacts are ready; execution requires both --execute and the environment gate",
        )

    if not CODEX_BIN.exists():
        manifest["status"] = "blocked"
        manifest["next_action"] = f"install Codex at {CODEX_BIN} or rerun without --execute"
        artifacts["run"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _write_status(artifacts["goal_dir"], _status_from_manifest(manifest, next_action=manifest["next_action"]))
        return blocked_result(
            "worker execution blocked because Codex binary was not found",
            artifacts=[_rel(artifacts["run"], artifacts["root"]), _rel(artifacts["status"], artifacts["root"])],
            next_actions=[manifest["next_action"]],
        )

    command_text = _detached_command(CODEX_BIN, prompt_path, Path(manifest["log"]), Path(manifest["done"]), artifacts["root"])
    Path(manifest["run"]).write_text(json.dumps({"task": manifest["task"], "started_at": manifest["started_at"]}, sort_keys=True) + "\n", encoding="utf-8")
    process = subprocess.Popen(  # noqa: S603
        ["bash", "-lc", command_text],
        cwd=str(artifacts["root"]),
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    manifest["pid"] = process.pid
    manifest["command"] = [str(CODEX_BIN), "exec", "--cd", str(artifacts["root"]), "<", str(prompt_path)]
    manifest["status"] = "running"
    manifest["next_action"] = "use worker-peek for compact status; use worker-collect after the done marker appears"
    artifacts["run"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_status(artifacts["goal_dir"], _status_from_manifest(manifest))
    return success_result(
        "worker launched",
        artifacts=[_rel(artifacts["run"], artifacts["root"]), _rel(artifacts["status"], artifacts["root"])],
        next_actions=[manifest["next_action"]],
        raw_output_path=str(manifest["log"]),
    )


def peek_worker(goal_dir: str | Path) -> CommandResult:
    artifacts = load_goal_artifacts(goal_dir)
    if not artifacts["run"].exists():
        create_worker_run_manifest(artifacts["goal_dir"], execute=False)
    manifest = _read_json(artifacts["run"])
    status = _status_from_manifest(manifest)
    _write_status(artifacts["goal_dir"], status)
    return success_result(
        _compact_status_summary(status),
        artifacts=[_rel(artifacts["status"], artifacts["root"])],
        next_actions=[str(status["next_action"])],
    )


def collect_worker_result(goal_dir: str | Path) -> CommandResult:
    artifacts = load_goal_artifacts(goal_dir)
    if not artifacts["run"].exists():
        create_worker_run_manifest(artifacts["goal_dir"], execute=False)
    manifest = _read_json(artifacts["run"])
    status = _status_from_manifest(manifest)
    completion = _load_completion_json(artifacts, str(manifest.get("task") or artifacts["goal"].goal_id))
    exit_code = status.get("done_exit_code")
    receipt_path = artifacts["receipt"]

    if completion:
        _merge_receipt_fields(receipt_path, completion)
        status["completion_json"] = _display_path(completion["_path"], artifacts["root"])
    else:
        status["completion_json"] = "missing"

    if exit_code is None:
        status["next_action"] = "worker has not produced a done marker; run worker-peek later"
        _write_status(artifacts["goal_dir"], status)
        return success_result(
            "worker collect recorded pending status; done marker is not present",
            artifacts=[_rel(artifacts["status"], artifacts["root"])],
            next_actions=[str(status["next_action"])],
        )

    if exit_code == 0:
        receipt = _read_json(receipt_path)
        tests_result = str(receipt.get("tests_build_result") or "not_run")
        if tests_result not in {"passed", "not_run"}:
            tests_result = "not_run"
        note = "worker finished successfully"
        if tests_result == "not_run":
            note = "worker finished successfully; validation not_run because no passing test result was recorded"
        _merge_receipt_fields(
            receipt_path,
            {
                "status": "complete",
                "tests_build_result": tests_result,
                "blocker_classification": "none",
                "next_recommended_action": note,
                "raw_log_path": str(manifest.get("log", "")),
            },
        )
        status["receipt_status"] = "complete"
        status["next_action"] = "refresh chain status and review receipt"
    else:
        blocker = f"worker exited nonzero: {exit_code}"
        _merge_receipt_fields(
            receipt_path,
            {
                "status": "blocked",
                "tests_build_result": "failed",
                "blocker_classification": "blocked",
                "blockers": [blocker],
                "next_recommended_action": "inspect bounded artifacts and decide whether to run a repair goal",
                "raw_log_path": str(manifest.get("log", "")),
            },
        )
        status["receipt_status"] = "blocked"
        status["next_action"] = "review blocker summary and decide whether to run bounded repair"

    refreshed = _refresh_parent_chain(artifacts["goal_dir"])
    if refreshed:
        status["chain_status_refreshed"] = str(refreshed / "chain_status.json")
    _write_status(artifacts["goal_dir"], status)
    result = success_result if exit_code == 0 else blocked_result
    return result(
        _compact_status_summary(status),
        artifacts=[_rel(receipt_path, artifacts["root"]), _rel(artifacts["status"], artifacts["root"])],
        next_actions=[str(status["next_action"])],
        raw_output_path=str(manifest.get("log", "")) or None,
    )


def _base_manifest(artifacts: dict[str, Any], *, prompt_path: Path, execute: bool) -> dict[str, Any]:
    goal: GoalSpec = artifacts["goal"]
    timestamp = _stamp()
    task = _safe_task(goal.goal_id)
    base = Path("/tmp") / f"{task}_{timestamp}"
    return {
        "task": task,
        "goal_dir": str(artifacts["goal_dir"]),
        "root": str(artifacts["root"]),
        "prompt": str(prompt_path),
        "run": str(base.with_suffix(".run")),
        "log": str(base.with_suffix(".log")),
        "done": str(base.with_suffix(".done")),
        "started_at": _now(),
        "execute": execute,
        "command": [],
        "status": "planned",
    }


def _status_from_manifest(manifest: dict[str, Any], *, next_action: str | None = None) -> dict[str, Any]:
    done_path = Path(str(manifest.get("done", "")))
    log_path = Path(str(manifest.get("log", "")))
    done_exit_code = _done_exit_code(done_path)
    active = _pid_active(manifest.get("pid"))
    receipt_status = _receipt_status(Path(str(manifest.get("goal_dir", ""))) / "receipt.json")
    action = next_action
    if action is None:
        if active:
            action = "wait for done marker, then run worker-collect"
        elif done_path.exists():
            action = "run worker-collect"
        elif manifest.get("status") in {"planned", "dry_run"}:
            action = "review worker_prompt.md before any approved execution"
        elif manifest.get("status") == "blocked":
            action = str(manifest.get("next_action") or "resolve worker launch blocker")
        else:
            action = "run worker-peek later or inspect worker_run.json"
    return {
        "active_process": active,
        "done_present": done_path.exists(),
        "done_exit_code": done_exit_code,
        "log_path": str(log_path),
        "log_size_bytes": log_path.stat().st_size if log_path.exists() else 0,
        "receipt_status": receipt_status,
        "next_action": action,
    }


def _write_status(goal_dir: Path, status: dict[str, Any]) -> Path:
    out = goal_dir / "worker_status.json"
    out.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def _detached_command(codex_bin: Path, prompt: Path, log: Path, done: Path, root: Path) -> str:
    return (
        "set -o pipefail; "
        f"{shutil.which('mkdir') or 'mkdir'} -p {json.dumps(str(log.parent))} {json.dumps(str(done.parent))}; "
        f"{json.dumps(str(codex_bin))} exec --cd {json.dumps(str(root))} < {json.dumps(str(prompt))} "
        f"> {json.dumps(str(log))} 2>&1; "
        "code=$?; "
        f"printf '{{\"exit_code\":%s,\"finished_at\":\"%s\"}}\\n' \"$code\" \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\" > {json.dumps(str(done))}"
    )


def _load_completion_json(artifacts: dict[str, Any], task: str) -> dict[str, Any] | None:
    candidates = [
        artifacts["root"] / "reports" / "codex_runs" / task / "completion.json",
        artifacts["goal_dir"] / "completion.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            data = _read_json(candidate)
            if isinstance(data, dict):
                data["_path"] = candidate
                return data
    return None


def _merge_receipt_fields(path: Path, updates: dict[str, Any]) -> None:
    data = _read_json(path)
    for key in ["changed_files", "commands_run", "blockers"]:
        if key in updates:
            data[key] = _append_unique(_string_list(data.get(key)), _string_list(updates.get(key)))
    if "commands_run" in updates:
        data["tests_run"] = _append_unique(_string_list(data.get("tests_run")), _string_list(updates.get("commands_run")))
    for key in ["tests_build_result", "status", "blocker_classification", "next_recommended_action", "raw_log_path"]:
        if key in updates and updates[key] is not None:
            data[key] = updates[key]
    if "next_recommended_action" in data:
        data["next_action"] = data["next_recommended_action"]
    if data.get("status") == "complete":
        data["blocker_classification"] = "none"
    if data.get("status") == "blocked":
        data["blocker_classification"] = "blocked"
    path.write_text(json.dumps(data, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")


def _refresh_parent_chain(goal_dir: Path) -> Path | None:
    if goal_dir.parent.name != "goals":
        return None
    chain_dir = goal_dir.parent.parent
    if not (chain_dir / "chain.json").exists():
        return None
    return refresh_chain(chain_dir)


def _infer_root(goal_dir: Path) -> Path:
    env_root = os.environ.get("CODELANES_ROOT")
    if env_root:
        return Path(env_root).resolve()
    parts = goal_dir.parts
    if "runs" in parts:
        index = parts.index("runs")
        if index > 0:
            return Path(*parts[:index]).resolve()
    receipt = goal_dir / "receipt.json"
    if receipt.exists():
        data = _read_json(receipt)
        worktree = data.get("worktree")
        if isinstance(worktree, str) and worktree:
            return Path(worktree).resolve()
    return Path.cwd().resolve()


def _receipt_status(path: Path) -> str:
    if not path.exists():
        return "missing"
    data = _read_json(path)
    status = data.get("status")
    if status in {"complete", "blocked", "pending"}:
        return str(status)
    if data.get("blocker_classification") == "blocked" or data.get("blockers"):
        return "blocked"
    return "pending"


def _done_exit_code(path: Path) -> int | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        text = path.read_text(encoding="utf-8").strip()
        return int(text) if text.isdigit() else None
    value = data.get("exit_code")
    return value if isinstance(value, int) else None


def _pid_active(pid: Any) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _compact_status_summary(status: dict[str, Any]) -> str:
    active = "yes" if status.get("active_process") else "no"
    done = "yes" if status.get("done_present") else "no"
    return (
        f"active_process={active}; done_present={done}; "
        f"log_size_bytes={status.get('log_size_bytes', 0)}; "
        f"receipt_status={status.get('receipt_status', 'unknown')}; "
        f"next_action={status.get('next_action', '')}"
    )


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _append_unique(existing: list[str], additions: list[str]) -> list[str]:
    result = list(existing)
    seen = set(result)
    for item in additions:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item.strip()]


def _bullets(items: list[str], *, empty: str = "None") -> list[str]:
    return [f"- {item}" for item in items] if items else [f"- {empty}"]


def _display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _rel(path: Path, root: Path) -> str:
    return _display_path(path, root)


def _safe_task(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "-", value).strip("-") or "worker"


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
