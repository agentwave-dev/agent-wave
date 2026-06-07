"""Sequential Goal Chain support for the builder harness."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any
from uuid import uuid4

from .codelanes import LaneRegistry
from .context_pack import write_context_pack
from .goals import GoalSpec
from .receipts import BuildReceipt


REQUIRED_CHAIN_FIELDS = ["chain_id", "title", "objective", "lane", "default_workflow", "goals"]
REQUIRED_GOAL_FIELDS = ["goal_id", "title", "objective"]
@dataclass(frozen=True)
class ChainGoal:
    goal_id: str
    title: str
    objective: str
    workflow: str
    lane: str
    depends_on: list[str]
    allowed_paths: list[str]
    forbidden_paths: list[str]
    acceptance_criteria: list[str]
    test_commands: list[str]
    proof_required: list[str]
    stop_conditions: list[str]

    @classmethod
    def from_mapping(cls, raw: dict[str, Any], *, chain: dict[str, Any], registry: LaneRegistry) -> "ChainGoal":
        missing = [field for field in REQUIRED_GOAL_FIELDS if field not in raw]
        if missing:
            raise ValueError(f"chain goal missing required fields: {', '.join(missing)}")

        lane_id = _text(raw.get("lane") or chain["lane"], "goal.lane")
        lane = registry.get(lane_id)
        workflow = _text(raw.get("workflow") or chain["default_workflow"], "goal.workflow")

        return cls(
            goal_id=_safe_id(_text(raw["goal_id"], "goal.goal_id")),
            title=_text(raw["title"], "goal.title"),
            objective=_text(raw["objective"], "goal.objective"),
            workflow=workflow,
            lane=lane_id,
            depends_on=_strings(raw.get("depends_on", []), "goal.depends_on"),
            allowed_paths=_strings(raw.get("allowed_paths", lane.owns), "goal.allowed_paths"),
            forbidden_paths=_strings(raw.get("forbidden_paths", lane.forbidden), "goal.forbidden_paths"),
            acceptance_criteria=_strings(raw.get("acceptance_criteria", ["Goal acceptance criteria are satisfied."]), "goal.acceptance_criteria"),
            test_commands=_strings(raw.get("test_commands", lane.default_tests), "goal.test_commands"),
            proof_required=_strings(raw.get("proof_required", ["context_pack.md", "receipt.json"]), "goal.proof_required"),
            stop_conditions=_strings(
                raw.get(
                    "stop_conditions",
                    [
                        "Wrong worktree or branch.",
                        "Forbidden path or private data would be touched.",
                        "Dependency receipt has a blocker.",
                    ],
                ),
                "goal.stop_conditions",
            ),
        )

    def to_goal_spec(self) -> GoalSpec:
        return GoalSpec.create(
            goal_id=self.goal_id,
            lane=self.lane,
            workflow=self.workflow,
            objective=self.objective,
            allowed_paths=self.allowed_paths,
            forbidden_paths=self.forbidden_paths,
            acceptance_criteria=self.acceptance_criteria,
            test_commands=self.test_commands,
            proof_required=self.proof_required,
            stop_conditions=self.stop_conditions,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GoalChain:
    chain_id: str
    title: str
    objective: str
    lane: str
    default_workflow: str
    goals: list[ChainGoal]
    created_at: str

    @classmethod
    def from_mapping(cls, raw: dict[str, Any], *, registry: LaneRegistry) -> "GoalChain":
        missing = [field for field in REQUIRED_CHAIN_FIELDS if field not in raw]
        if missing:
            raise ValueError(f"goal chain missing required fields: {', '.join(missing)}")
        goals_raw = raw["goals"]
        if not isinstance(goals_raw, list) or not goals_raw:
            raise ValueError("goal chain field 'goals' must be a non-empty list")

        chain = {
            "chain_id": _safe_id(_text(raw["chain_id"], "chain_id")),
            "title": _text(raw["title"], "title"),
            "objective": _text(raw["objective"], "objective"),
            "lane": _text(raw["lane"], "lane"),
            "default_workflow": _text(raw["default_workflow"], "default_workflow"),
        }
        registry.get(chain["lane"])

        goals: list[ChainGoal] = []
        seen: set[str] = set()
        for item in goals_raw:
            if not isinstance(item, dict):
                raise ValueError("each goal chain goal must be a mapping")
            goal = ChainGoal.from_mapping(item, chain=chain, registry=registry)
            if goal.goal_id in seen:
                raise ValueError(f"duplicate goal_id: {goal.goal_id}")
            missing_deps = [dep for dep in goal.depends_on if dep not in seen]
            if missing_deps:
                raise ValueError(f"goal '{goal.goal_id}' has unknown or out-of-order dependencies: {', '.join(missing_deps)}")
            seen.add(goal.goal_id)
            goals.append(goal)

        return cls(
            chain_id=chain["chain_id"],
            title=chain["title"],
            objective=chain["objective"],
            lane=chain["lane"],
            default_workflow=chain["default_workflow"],
            goals=goals,
            created_at=_text(raw.get("created_at") or _now(), "created_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "chain_id": self.chain_id,
            "title": self.title,
            "objective": self.objective,
            "lane": self.lane,
            "default_workflow": self.default_workflow,
            "created_at": self.created_at,
            "execution_mode": "sequential",
            "worker_launch": "disabled",
            "goals": [goal.to_dict() for goal in self.goals],
        }

    def default_dir(self, root: str | Path = ".") -> Path:
        return Path(root) / "runs" / "build_chains" / self.chain_id


def create_minimal_chain(*, lane: str, title: str, objective: str, registry: LaneRegistry, root: str | Path = ".") -> Path:
    lane_config = registry.get(lane)
    chain_id = _safe_id(f"{lane}-{title}")[:48] or f"{lane}-{uuid4().hex[:8]}"
    if (Path(root) / "runs" / "build_chains" / chain_id).exists():
        chain_id = f"{chain_id}-{uuid4().hex[:8]}"

    raw = {
        "chain_id": chain_id,
        "title": title,
        "objective": objective,
        "lane": lane,
        "default_workflow": "narrow_implementation",
        "goals": [
            {
                "goal_id": "audit_current_state",
                "title": "Audit current state",
                "objective": f"Audit current state for: {objective}",
                "workflow": "audit",
                "lane": lane,
                "depends_on": [],
                "allowed_paths": lane_config.owns,
                "forbidden_paths": lane_config.forbidden,
                "acceptance_criteria": ["Current behavior and constraints are identified."],
                "test_commands": lane_config.default_tests,
                "proof_required": ["context_pack.md", "receipt.json"],
                "stop_conditions": ["Wrong worktree or branch.", "Forbidden path or private data would be touched."],
            },
            {
                "goal_id": "implement_small_change",
                "title": "Implement small change",
                "objective": f"Implement one bounded change for: {objective}",
                "workflow": "narrow_implementation",
                "lane": lane,
                "depends_on": ["audit_current_state"],
                "allowed_paths": lane_config.owns,
                "forbidden_paths": lane_config.forbidden,
                "acceptance_criteria": ["The bounded change is implemented.", "No patches are applied automatically by the chain."],
                "test_commands": lane_config.default_tests,
                "proof_required": ["context_pack.md", "receipt.json"],
                "stop_conditions": ["Dependency receipt has a blocker.", "Forbidden path or private data would be touched."],
            },
            {
                "goal_id": "validate_and_receipt",
                "title": "Validate and receipt",
                "objective": f"Validate and write proof for: {objective}",
                "workflow": "validation",
                "lane": lane,
                "depends_on": ["implement_small_change"],
                "allowed_paths": lane_config.owns,
                "forbidden_paths": lane_config.forbidden,
                "acceptance_criteria": ["Configured tests pass or blockers are documented.", "Receipts identify next action."],
                "test_commands": lane_config.default_tests,
                "proof_required": ["context_pack.md", "receipt.json", "chain_completion.md"],
                "stop_conditions": ["Validation fails without a documented blocker.", "Receipt proof is missing."],
            },
        ],
    }
    chain = GoalChain.from_mapping(raw, registry=registry)
    return write_chain_json(chain, root=root)


def load_chain_file(path: str | Path, *, registry: LaneRegistry) -> GoalChain:
    raw = _load_mapping(Path(path))
    return GoalChain.from_mapping(raw, registry=registry)


def write_chain_json(chain: GoalChain, *, root: str | Path = ".") -> Path:
    chain_dir = chain.default_dir(root)
    chain_dir.mkdir(parents=True, exist_ok=True)
    out = chain_dir / "chain.json"
    out.write_text(json.dumps(chain.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def materialize_chain(chain_file: str | Path, *, registry: LaneRegistry, root: str | Path = ".") -> Path:
    chain = load_chain_file(chain_file, registry=registry)
    chain_json = write_chain_json(chain, root=root)
    chain_dir = chain_json.parent
    goals_dir = chain_dir / "goals"

    for chain_goal in chain.goals:
        goal_dir = goals_dir / chain_goal.goal_id
        goal = chain_goal.to_goal_spec()
        goal.write_json(goal_dir / "goal.json")
        write_context_pack(goal, registry.get(goal.lane), root=root, output_dir=goal_dir)
        receipt = BuildReceipt.init_from_goal(
            goal,
            root=root,
            blocker_classification="pending",
            patch_path=str(goal_dir / "patch_placeholder_disabled.md"),
            next_action="complete this child goal manually, then update receipt",
        )
        receipt.write_json(goal_dir / "receipt.json")

    write_chain_status(chain_dir)
    write_chain_completion(chain_dir)
    return chain_dir


def write_chain_status(chain_dir: str | Path) -> Path:
    directory = Path(chain_dir)
    chain = json.loads((directory / "chain.json").read_text(encoding="utf-8"))
    goals_status = []
    blockers: list[str] = []
    next_incomplete: str | None = None

    for goal in chain["goals"]:
        goal_id = goal["goal_id"]
        receipt_path = directory / "goals" / goal_id / "receipt.json"
        receipt_status = "missing"
        blocker = "receipt missing"
        if receipt_path.exists():
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            blocker = str(receipt.get("blocker_classification", "unknown"))
            exit_codes = receipt.get("exit_codes", {})
            if blocker == "none" and isinstance(exit_codes, dict) and all(code == 0 for code in exit_codes.values()):
                receipt_status = "complete"
            else:
                receipt_status = "incomplete"
        if receipt_status != "complete" and next_incomplete is None:
            next_incomplete = goal_id
        if blocker not in ("none", "pending"):
            blockers.append(f"{goal_id}: {blocker}")
        goals_status.append(
            {
                "goal_id": goal_id,
                "depends_on": goal.get("depends_on", []),
                "receipt": receipt_status,
                "blocker": blocker,
            }
        )

    status = {
        "chain_id": chain["chain_id"],
        "title": chain["title"],
        "execution_mode": "sequential",
        "worker_launch": "disabled",
        "goal_count": len(chain["goals"]),
        "goals": goals_status,
        "blockers": blockers,
        "next_incomplete_goal": next_incomplete,
        "updated_at": _now(),
    }
    out = directory / "chain_status.json"
    out.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def write_chain_completion(chain_dir: str | Path) -> Path:
    directory = Path(chain_dir)
    status = json.loads((directory / "chain_status.json").read_text(encoding="utf-8"))
    lines = [
        f"# Goal Chain Completion: {status['chain_id']}",
        "",
        f"- Execution mode: {status['execution_mode']}",
        f"- Worker launch: {status['worker_launch']}",
        f"- Goal count: {status['goal_count']}",
        f"- Next incomplete goal: {status['next_incomplete_goal'] or 'none'}",
        f"- Blockers: {', '.join(status['blockers']) if status['blockers'] else 'none'}",
        "",
        "## Goal Receipts",
    ]
    for goal in status["goals"]:
        lines.append(f"- {goal['goal_id']}: {goal['receipt']} ({goal['blocker']})")
    lines.extend(["", "Human review and merge gates remain required."])
    out = directory / "chain_completion.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def compact_status(chain_file_or_dir: str | Path) -> str:
    chain_dir = _chain_dir(chain_file_or_dir)
    status_path = write_chain_status(chain_dir)
    status = json.loads(status_path.read_text(encoding="utf-8"))
    lines = [
        f"chain id: {status['chain_id']}",
        f"goal count: {status['goal_count']}",
        "receipt status:",
    ]
    for goal in status["goals"]:
        lines.append(f"- {goal['goal_id']}: {goal['receipt']} ({goal['blocker']})")
    lines.append(f"blockers: {', '.join(status['blockers']) if status['blockers'] else 'none'}")
    lines.append(f"next incomplete goal: {status['next_incomplete_goal'] or 'none'}")
    return "\n".join(lines)


def _chain_dir(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_dir():
        return candidate
    if candidate.name == "chain.json":
        return candidate.parent
    if candidate.exists():
        data = json.loads(candidate.read_text(encoding="utf-8")) if candidate.suffix == ".json" else _load_mapping(candidate)
        chain_id = _text(data.get("chain_id"), "chain_id")
        cwd_candidate = Path.cwd() / "runs" / "build_chains" / _safe_id(chain_id)
        if cwd_candidate.exists():
            return cwd_candidate
    raise FileNotFoundError(f"chain directory not found for {candidate}")


def _load_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("chain JSON must be an object")
        return data
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None
    if yaml is not None:
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            raise ValueError("chain YAML must be a mapping")
        return data
    return _parse_simple_yaml(text, path)


def _parse_simple_yaml(text: str, path: Path) -> dict[str, Any]:
    root: dict[str, Any] = {}
    current_root_list: str | None = None
    current_goal: dict[str, Any] | None = None
    current_goal_list: str | None = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0:
            key, value = _split_yaml_pair(stripped, path, lineno)
            if value == "":
                root[key] = []
                current_root_list = key
            else:
                root[key] = _parse_scalar(value)
                current_root_list = None
            current_goal = None
            current_goal_list = None
            continue

        if indent == 2 and current_root_list == "goals" and stripped.startswith("- "):
            current_goal = {}
            root["goals"].append(current_goal)
            body = stripped[2:].strip()
            if body:
                key, value = _split_yaml_pair(body, path, lineno)
                current_goal[key] = _parse_scalar(value)
            current_goal_list = None
            continue

        if indent == 4 and current_goal is not None:
            key, value = _split_yaml_pair(stripped, path, lineno)
            if value == "":
                current_goal[key] = []
                current_goal_list = key
            else:
                current_goal[key] = _parse_scalar(value)
                current_goal_list = None
            continue

        if indent == 6 and current_goal is not None and current_goal_list and stripped.startswith("- "):
            current_goal[current_goal_list].append(_parse_scalar(stripped[2:].strip()))
            continue

        raise ValueError(f"{path}:{lineno}: unsupported goal-chain YAML syntax")

    return root


def _split_yaml_pair(stripped: str, path: Path, lineno: int) -> tuple[str, str]:
    if ":" not in stripped:
        raise ValueError(f"{path}:{lineno}: expected key: value")
    key, value = stripped.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"{path}:{lineno}: empty key")
    return key, value.strip()


def _parse_scalar(value: str) -> Any:
    if value in ("[]", ""):
        return [] if value == "[]" else ""
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _strings(value: Any, field_name: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field_name} must be a list of strings")
    return [item.strip() for item in value]


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "-", value).strip("-").lower()


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
