# Agent Wave

Agent Wave is a multi-agent auto-build harness for running many AI coding agents across separate worktrees and tasks simultaneously without losing state, mixing branches, or drowning in logs.

## 30-Second Pitch

Run many AI coding agents at once without repo chaos.

Agent Wave gives coding agents a jobsite: lanes, state, skills, receipts, and merge gates. The model is stateless. The lane is stateful. Each lane names the expected worktree, branch, task, state pack, skill set, detached run, completion receipt, trace, and merge posture before work starts.

Every agent run leaves a receipt. Every receipt belongs to a trace. Self-healing means bounded repair with receipts and human merge gates, not uncontrolled autonomy.

## Quickstart

```bash
git clone https://github.com/agentwave-dev/agent-wave.git
cd agent-wave

scripts/wave smoke
scripts/wave audit
python -m pytest examples/fake-app/tests
```

Create a demo lane:

```bash
mkdir -p /repo/fake-app/.agent-wave/lanes /repo/fake-app/.agent-wave/state
cp templates/state-pack.yaml /repo/fake-app/.agent-wave/lanes/demo-lane.yaml
cp templates/goal-chain.yaml /repo/fake-app/.agent-wave/state/demo-goal-chain.yaml
```

## Core Concepts

- Lanes: named execution tracks with an expected worktree, branch, status policy, and guardrails.
- State Packs: durable lane memory for current task state, blockers, run ids, receipts, trace pointers, and runtime bridge metadata.
- Skills: local, versioned operating procedures that teach agents how to perform repeatable work.
- Detached Runs: background agent or shell runs that can continue without chat scrollback.
- Completion Receipts: explicit evidence that a run reached a stopping point.
- Trace Graph: a linked audit trail of lane events, runs, receipts, reviews, and healing attempts.
- Learning Ledger: a visible record of lessons learned without hidden memory.
- Bounded Healing Loop: limited repair attempts that produce receipts and stop at a merge gate.
- Merge Gates: human-controlled checkpoints before source changes enter the main branch.
- Wave Crew: supervised subagents for planning, implementation, testing, docs, safety, and merge review.
- Goal Chain Waves: roadmap runners that break large objectives into small bounded runs.
- Autobrowse Proof: browser or HTTP evidence attached to a receipt when UI/runtime behavior matters.

## Wave Flow

```text
roadmap goal
    |
    v
lane -> state pack -> skill -> detached run -> completion receipt
  |                                                |
  |                                                v
  +---------- trace graph <- learning ledger <- merge review
                                   |
                                   v
                         bounded healing loop
                                   |
                                   v
                               merge gate
```

## Example Command Flow

```bash
# Verify the lane before starting work.
scripts/wave smoke
scripts/wave audit

# Run a bounded task in a detached process.
scripts/wave-run-detached demo-lane "python -m pytest examples/fake-app/tests"

# Record the result.
cp templates/completion-receipt.md examples/fake-app/.agent-wave/completions/example-completion.md
cp templates/trace-event.json examples/fake-app/.agent-wave/traces/example-wave-trace.json

# Review before merge.
scripts/wave milestone
```

## Safety Model

Agent Wave is built around explicit state and human-controlled gates.

- Work happens in lanes with expected worktrees and branches.
- State packs are small enough to inspect in a diff.
- Detached runs write logs outside source or through a sanitized runtime artifact bridge.
- Completion receipts list changed files, validation commands, blockers, and merge posture.
- Trace events connect receipts to the runs and goals that produced them.
- Healing loops have attempt limits and stop with a receipt.
- Merge gates require review before branch integration.
- Forbidden-path audits keep private paths, secrets, raw logs, and generated runtime sprawl out of public artifacts.

## Roadmap

Current public scaffold:

- v0.1 Lane Harness
- v0.2 State Packs
- v0.3 Skill Library
- v0.4 Wave Crew
- v0.5 Auto-Build Roadmap Runner

Next public primitives:

- v0.6 Trace Graph
- v0.7 Learning Ledger
- v0.8 Bounded Healing Loop
- v0.9 Goal Chain Waves
- v1.0 Autobrowse Proof and Merge Gates

See [docs/roadmap/goals.md](docs/roadmap/goals.md) for details.

## Learn More

- [Agent Wave Protocol](docs/concepts/agent-wave-protocol.md)
- [State Packs](docs/concepts/state-packs.md)
- [Wave Crew](docs/concepts/wave-crew.md)
- [Trace Graph](docs/concepts/trace-graph.md)
- [Learning Ledger](docs/concepts/learning-ledger.md)
- [Bounded Healing Loop](docs/concepts/bounded-healing-loop.md)
- [Goal Chain Waves](docs/concepts/goal-chain-waves.md)
- [Autobrowse Proof](docs/concepts/autobrowse-proof.md)
- [Technical Introduction](docs/articles/agent-wave-technical-introduction.md)

## Contributing

Contributions are welcome when they preserve the core contract: stateful lanes, auditable receipts, bounded repair, and human merge gates. Good first contributions include clearer templates, additional generic examples, new skills, and validation scripts that improve safety without coupling the project to private infrastructure.
