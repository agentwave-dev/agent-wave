# Getting Started

This guide walks through a generic `fake-app` lane in CodeLanes. It does not require private infrastructure.

## 1. Verify The Repo

```bash
scripts/wave smoke
scripts/wave audit
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

## 4. Run A Bounded Task

```bash
scripts/wave-run-detached demo-lane "python -m pytest examples/fake-app/tests"
```

The run should produce a completion receipt and a trace event. If the run fails, use the bounded healing loop instead of launching unbounded retries.

## 5. Write The Receipts

```bash
mkdir -p examples/fake-app/.agent-wave/completions examples/fake-app/.agent-wave/traces examples/fake-app/.agent-wave/learning
cp templates/completion-receipt.md examples/fake-app/.agent-wave/completions/example-completion.md
cp templates/trace-event.json examples/fake-app/.agent-wave/traces/example-wave-trace.json
cp templates/learning-ledger-entry.md examples/fake-app/.agent-wave/learning/example-ledger.md
```

Every receipt should name changed files, validation commands, blockers, and merge posture. Every trace should link the goal, run, receipt, and review.

## 6. Review The Merge Gate

```bash
scripts/wave milestone
```

Only merge after the lane, trace, safety scan, and validation evidence are coherent. CodeLanes is designed for supervised automation, not autonomous branch integration.
