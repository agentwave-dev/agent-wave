# CodeLanes: A Multi-Agent Auto-Build Harness for Stateful Coding Agents

## 1. The Problem: AI Coding Agents Create Repo Chaos

AI coding agents are useful, but parallel agent work can quickly make a repository hard to trust. Agents can edit the wrong branch, use the wrong folder, forget earlier constraints, bury important evidence in logs, retry failures without limits, or leave maintainers guessing which run produced which change.

The issue is not only model quality. The issue is missing operating structure.

CodeLanes is that operating structure: a multi-agent auto-build harness for running coding agents across isolated lanes with state packs, context packs, traces, receipts, and merge gates.

## 2. The Core Insight: The Model Is Stateless, The Lane Is Stateful

The model is stateless. The lane is stateful.

A lane is a named execution track with an expected worktree, branch, status policy, state pack, generated context pack, skills, receipts, and merge posture. The agent can come and go, but the lane preserves the truth needed to continue safely.

Instead of relying on chat memory, CodeLanes keeps durable repo context in inspectable files and requires every bounded run to return proof. This is the Context Packs + Completion Receipts feature: durable memory, bounded prompts, safe log peeks, and compact receipts.

## 3. CodeLanes Architecture: Lane -> State Pack -> Skill -> Detached Run -> Receipt -> Trace -> Merge Gate

The CodeLanes architecture is:

```text
lane -> state pack -> skill -> detached run -> receipt -> trace -> merge gate
```

The lane defines where work may happen. The state pack records current truth. The context pack selects only the lane, skill, goal, paths, blockers, and completion requirements needed for one run. The skill defines the procedure. The detached run executes bounded work. The completion receipt records evidence. The trace connects the evidence. The merge gate keeps integration under human control.

Wave remains the protocol inside CodeLanes. A wave is a coordinated set of bounded runs across one or more lanes.

## 4. How Wave Crew / Subagents Work

Wave Crew splits work across supervised subagents. A planner can break down a goal. An implementer can edit code. A tester can run verification. A docs agent can update public docs. A safety agent can run audits. A merge-review agent can summarize risk.

Each subagent gets a bounded prompt, lane context, state entry, detached run, completion receipt, and trace event. No subagent merges autonomously.

## 5. Trace Graph: Every Run Is Auditable

The Trace Graph links goals, runs, receipts, artifacts, learning entries, healing attempts, and merge reviews. It answers the questions maintainers ask after an agent run:

- What goal started this work?
- Which lane owned it?
- Which command ran?
- Which receipt claims completion?
- Which validation commands support the claim?
- Which merge gate reviewed it?

Every agent run leaves a receipt. Every receipt belongs to a trace.

## 6. Context Packs + Completion Receipts: Token Discipline

Agent runs should not repeatedly paste old project history, multi-MB logs, full diffs, or previous completion reports into every prompt. CodeLanes moves repeated context into durable state packs, then generates a compact context pack:

```bash
scripts/wave context-pack --lane demo-lane --skill token-efficient-codex-run --goal "run fake-app tests"
```

The output is `.agent-wave/context/latest_demo-lane.md`, capped at 200 lines. It includes lane state, selected skill, goal, allowed paths, forbidden paths, blockers, and completion requirements.

Completion receipts are capped at 120 lines. They include changed files, commands run, tests/build result, blockers, next recommended action, and raw log path only.

## 7. Learning Ledger: Improvement Without Hidden Memory

CodeLanes avoids hidden learning. When a run teaches the system something reusable, the lesson goes into a Learning Ledger entry with an observation, decision, future instruction, and evidence receipt.

Useful lessons can later become skills, but only after review. This keeps learning inspectable and reversible.

## 8. Bounded Healing Loop: Repair Without Uncontrolled Autonomy

Self-healing means bounded repair with receipts and human merge gates, not uncontrolled autonomy.

A failed run can enter a Bounded Healing Loop. The loop classifies the failure, makes one small repair, runs validation, writes a healing receipt, and stops when the attempt budget is exhausted or the failure is resolved.

## 9. Runtime Artifact Bridge: Source Edits Vs Runtime Proof

Source edits and live runtime proof are different evidence types. A source test can show that a function behaves correctly. A browser check or HTTP response can show what a running app exposed.

The Runtime Artifact Bridge gives agents a safe way to reference sanitized runtime evidence without dumping raw logs, secrets, or generated private artifacts into source.

## 10. Goal Chain Waves: Turning Big Roadmap Items Into Bounded Runs

Goal Chain Waves convert large roadmap items into ordered, bounded goals. Each goal names a lane, skill, validation command, receipt requirement, and merge gate.

The runner advances only when the previous goal has a receipt, trace event, and acceptable validation posture.

## 11. Fake-App Walkthrough

In `examples/fake-app`, a demo wave can:

1. Verify the lane with `scripts/wave smoke`.
2. Run tests with `scripts/wave-run-detached demo-lane "python -m pytest examples/fake-app/tests"`.
3. Write `examples/fake-app/.agent-wave/completions/example-completion.md`.
4. Link the run in `examples/fake-app/.agent-wave/traces/example-wave-trace.json`.
5. Record a reusable lesson in `examples/fake-app/.agent-wave/learning/example-ledger.md`.
6. Prepare `examples/fake-app/.agent-wave/merge-reviews/example-merge-review.md`.

The example is intentionally generic. It demonstrates the protocol without relying on private infrastructure.

## 12. Why CodeLanes Is Not Another Coding Agent

CodeLanes is not a model and it is not another coding agent. It is the jobsite discipline around coding agents.

The harness gives agents lanes, state, skills, receipts, traces, and merge gates so many agents can work in parallel without turning the repository into guesswork.

## 13. Roadmap

The public scaffold currently covers lane harnesses, state packs, skills, Wave Crew, trace concepts, learning ledgers, healing receipts, and roadmap runner concepts.

Next steps include stronger trace validation, ledger promotion workflows, enforced healing budgets, goal-chain execution commands, autobrowse proof attachments, richer merge gates, and more examples for common coding-agent workflows.

GitHub: https://github.com/agentwave-dev/CodeLanes

X: @getcodelanes
