# Getting Started

This guide walks through a generic `fake-app` lane in CodeLanes. It does not require private infrastructure.

## 1. Verify The Repo

```bash
scripts/wave smoke
scripts/wave audit
scripts/wave context-pack --lane demo-lane --skill token-efficient-codex-run --goal "clean up destination-domain DNS panel copy only"
python -m pytest examples/fake-app/tests
```

## 2. Create A Demo Lane

```bash
mkdir -p /tmp/codelanes-demo/.agent-wave/lanes
mkdir -p /tmp/codelanes-demo/.agent-wave/state
cp templates/state-pack.yaml /tmp/codelanes-demo/.agent-wave/lanes/demo-lane.yaml
cp templates/goal-chain.yaml /tmp/codelanes-demo/.agent-wave/state/demo-goal-chain.yaml
```

Edit the copied state pack so it names the expected worktree, branch, allowed commands, forbidden paths, and receipt location.

## 3. Pick A Skill

Use a focused skill for each run:

- `skills/lane-verify/SKILL.md` for lane checks
- `skills/wave-run-detached/SKILL.md` for detached execution
- `skills/trace-graph/SKILL.md` for trace events
- `skills/learning-ledger/SKILL.md` for visible lessons
- `skills/bounded-healing/SKILL.md` for limited repair attempts
- `skills/goal-chain-planner/SKILL.md` for roadmap breakdown
- `skills/token-efficient-codex-run/SKILL.md` for bounded context and compact receipts
- `skills/log-hygiene/SKILL.md` for safe detached-run inspection

## 4. Run A Bounded Task

```bash
scripts/wave context-pack --lane demo-lane --skill token-efficient-codex-run --goal "run fake-app tests"
WAVE_TASK_ID=demo-lane scripts/wave-run-detached demo-lane "python -m pytest examples/fake-app/tests"
scripts/wave peek --task demo-lane
```

The generated context pack is written to `.agent-wave/context/latest_demo-lane.md` and should stay under 200 lines. The detached run writes `/tmp/<task>_<timestamp>.run`, `.log`, and `.done` markers. Use `scripts/wave peek` for status; do not paste raw logs into chat or receipts.

## 5. Write The Receipts

```bash
mkdir -p examples/fake-app/.agent-wave/completions examples/fake-app/.agent-wave/traces examples/fake-app/.agent-wave/learning
cp templates/completion-receipt.md examples/fake-app/.agent-wave/completions/example-completion.md
cp templates/trace-event.json examples/fake-app/.agent-wave/traces/example-wave-trace.json
cp templates/learning-ledger-entry.md examples/fake-app/.agent-wave/learning/example-ledger.md
```

Every receipt should name changed files, validation commands, blockers, and merge posture. Every trace should link the goal, run, receipt, and review.

For token-efficient runs, also write `reports/codex_runs/<task>/completion.json` from `templates/completion.json` and a markdown receipt from `templates/token-efficient-completion-receipt.md`. Keep the markdown receipt under 120 lines and include raw log paths only.

## 6. Review The Merge Gate

```bash
scripts/wave milestone
```

Only merge after the lane, trace, safety scan, and validation evidence are coherent. CodeLanes is designed for supervised automation, not autonomous branch integration.
