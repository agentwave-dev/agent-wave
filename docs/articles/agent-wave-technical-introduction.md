# Agent Wave: A Multi-Agent Auto-Build Harness for Stateful Coding Agents

## 1. The Problem: AI Coding Agents Create Repo Chaos

AI coding agents are useful, but parallel agent work can quickly make a repository hard to trust. Agents can edit the wrong branch, forget earlier constraints, bury important evidence in logs, retry failures without limits, or leave maintainers guessing which run produced which change.

The issue is not only model quality. The issue is missing operating structure.

## 2. The Core Insight: The Model Is Stateless, The Lane Is Stateful

Agent Wave starts from a simple premise: the model is stateless. The lane is stateful.

A lane is a named execution track with an expected worktree, branch, status policy, state pack, skills, receipts, and merge posture. The agent can come and go, but the lane preserves the truth needed to continue safely.

## 3. The Wave Protocol

The Wave protocol is:

```text
lane -> state pack -> skill -> detached run -> receipt -> trace -> merge gate
```

The lane defines where work may happen. The state pack records current truth. The skill defines the procedure. The detached run executes bounded work. The receipt records evidence. The trace connects the evidence. The merge gate keeps integration under human control.

## 4. How Subagents Work Inside Wave Crew

Wave Crew splits work across supervised subagents. A planner can break down a goal. An implementer can edit code. A tester can run verification. A docs agent can update public docs. A safety agent can run audits. A merge-review agent can summarize risk.

Each subagent gets a bounded prompt, state entry, detached run, completion receipt, and trace event. No subagent merges autonomously.

## 5. Trace Graph: How Every Run Becomes Auditable

The Trace Graph links goals, runs, receipts, artifacts, learning entries, healing attempts, and merge reviews. It answers the questions maintainers ask after an agent run:

- What goal started this work?
- Which lane owned it?
- Which command ran?
- Which receipt claims completion?
- Which validation commands support the claim?
- Which merge gate reviewed it?

Every agent run leaves a receipt. Every receipt belongs to a trace.

## 6. Learning Ledger: How The System Improves Without Hidden Memory

Agent Wave avoids hidden learning. When a run teaches the system something reusable, the lesson goes into a Learning Ledger entry with an observation, decision, future instruction, and evidence receipt.

Useful lessons can later become skills, but only after review. This keeps learning inspectable and reversible.

## 7. Bounded Healing Loop: How Failed Waves Repair Themselves Safely

Self-healing means bounded repair with receipts and human merge gates, not uncontrolled autonomy.

A failed run can enter a Bounded Healing Loop. The loop classifies the failure, makes one small repair, runs validation, writes a healing receipt, and stops when the attempt budget is exhausted or the failure is resolved.

## 8. Runtime Artifact Bridge: Separating Source Edits From Live Runtime Proof

Source edits and live runtime proof are different evidence types. A source test can show that a function behaves correctly. A browser check or HTTP response can show what a running app exposed.

The Runtime Artifact Bridge gives agents a safe way to reference sanitized runtime evidence without dumping raw logs, secrets, or generated private artifacts into source.

## 9. Goal Chain Waves: Turning Big Roadmap Items Into Small Bounded Runs

Goal Chain Waves convert large roadmap items into ordered, bounded goals. Each goal names a lane, skill, validation command, receipt requirement, and merge gate.

The runner advances only when the previous goal has a receipt, trace event, and acceptable validation posture.

## 10. Example Walkthrough With Fake-App

In `examples/fake-app`, a demo wave can:

1. Verify the lane with `scripts/wave smoke`.
2. Run tests with `scripts/wave-run-detached demo-lane "python -m pytest examples/fake-app/tests"`.
3. Write `examples/fake-app/.agent-wave/completions/example-completion.md`.
4. Link the run in `examples/fake-app/.agent-wave/traces/example-wave-trace.json`.
5. Record a reusable lesson in `examples/fake-app/.agent-wave/learning/example-ledger.md`.
6. Prepare `examples/fake-app/.agent-wave/merge-reviews/example-merge-review.md`.

The example is intentionally generic. It demonstrates the protocol without relying on private infrastructure.

## 11. Why This Is Not Another Coding Agent

Agent Wave is not a model. It is the jobsite around the model. It gives coding agents lanes, state, skills, receipts, traces, and merge gates so many agents can work in parallel without turning the repository into guesswork.

## 12. Roadmap

The public scaffold currently covers lane harnesses, state packs, skills, Wave Crew, and roadmap runner concepts. Next steps include stronger trace validation, ledger promotion workflows, enforced healing budgets, goal-chain execution commands, autobrowse proof attachments, and richer merge gates.
