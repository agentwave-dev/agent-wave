# CodeLanes

CodeLanes is a multi-agent auto-build harness for running many AI coding agents across isolated lanes and tasks simultaneously without losing state, mixing branches, or drowning in logs.

Run many coding agents at once without repo chaos.

## 30-Second Pitch

CodeLanes is the operating discipline around coding agents. It gives each run a lane, state pack, skill, detached process, completion receipt, trace, and merge gate before work starts.

The model is stateless. The lane is stateful.

Instead of trusting chat memory or giant logs, CodeLanes makes agent work inspectable. Context Packs + Completion Receipts give each coding lane durable memory, bounded context, and compact receipts so agents stop burning tokens on repeated history and oversized logs. Every agent run leaves a receipt. Every receipt belongs to a trace. Repair loops are bounded. Merge stays human-controlled.

## Quickstart

From the repo root:

```bash
git clone https://github.com/agentwave-dev/CodeLanes.git
cd CodeLanes

scripts/wave smoke
scripts/wave audit
scripts/wave context-pack --lane demo-lane --skill token-efficient-codex-run --goal "clean up destination-domain DNS panel copy only"
python -m pytest examples/fake-app/tests
```

Create a demo lane:

```bash
mkdir -p /tmp/codelanes-demo/.agent-wave/lanes /tmp/codelanes-demo/.agent-wave/state
cp templates/state-pack.yaml /tmp/codelanes-demo/.agent-wave/lanes/demo-lane.yaml
cp templates/goal-chain.yaml /tmp/codelanes-demo/.agent-wave/state/demo-goal-chain.yaml
```

## What Works Today

- Lane verification contracts for expected worktree, branch, status, and forbidden paths.
- State pack, receipt, trace, learning ledger, healing, and goal-chain templates.
- Context-pack generator for lane plus skill prompts under `.agent-wave/context/`.
- Token-efficient completion JSON and markdown receipt templates.
- Safe `peek` command for detached run status without reading raw logs.
- Detached run wrapper for bounded local commands.
- Smoke and audit commands for repo-level checks.
- Fake app fixture with pytest coverage.
- Public concept docs for Wave Crew, Trace Graph, Learning Ledger, Bounded Healing Loop, Goal Chain Waves, and runtime proof.

## Implemented MVP

The current CodeLanes MVP is a supervised builder harness, not an autonomous agent platform. These primitives are implemented in the public CLI:

- Repo checks: `scripts/codelanes smoke`, `scripts/codelanes audit`, and `scripts/codelanes lanes`.
- Lane setup and guardrails: `lane-guard`, `goal-init`, `context-pack`, and `receipt-init`.
- Context Packs + Completion Receipts for compact prompts and inspectable proof.
- Builder Harness MVP artifacts for goals, context packs, receipts, and runner manifests.
- Sequential Goal Chains with `goal-chain-init`, `goal-chain-materialize`, `goal-chain-status`, `goal-chain-refresh`, `goal-chain-next`, and `goal-receipt-update`.
- Goal Chain Progress from child receipts into chain status and completion rollups.
- Session Contract fields in worker runner manifests.
- CommandResult-style compact command observations.
- Supervised Worker Launcher MVP with `worker-plan`, `worker-run`, `worker-peek`, and `worker-collect`.
- Webbuilder Publish MVP as the first real project chain at `runs/build_chains/webbuilder-publish-mvp`.

## Still Scaffolded / Not Implemented Yet

These are intentionally not implemented as automatic behavior in the current MVP:

- No swarms.
- No automatic patch application.
- No integration apply mode.
- No repair execution.
- No autonomous execution.

## Core Concepts

- CodeLanes: the product and repo, an auto-build harness around coding agents.
- Lane: an isolated workstream with an expected worktree, branch, task, state, and merge posture.
- Wave: a coordinated set of bounded agent runs across one or more lanes.
- Wave Crew: supervised subagents for planning, implementation, testing, docs, safety, and merge review.
- State Pack: durable lane context for current task state, blockers, run ids, receipts, trace pointers, and runtime bridge metadata.
- Context Pack: a generated, max-200-line prompt pack that selects one lane, one skill, one goal, allowed paths, forbidden paths, blockers, and completion requirements.
- Trace Graph: a linked audit trail of lane events, runs, receipts, reviews, and healing attempts.
- Learning Ledger: explicit reviewed learning, not hidden memory.
- Completion Receipt: concise proof of what changed, what ran, and what remains.
- Bounded Healing Loop: controlled repair with attempt limits, receipts, and merge gates.
- Merge Gate: a human-controlled checkpoint before integration.

## Flow

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
# Verify the repo and lane harness.
scripts/wave smoke
scripts/wave audit

# Run a bounded task in a detached process.
WAVE_TASK_ID=demo-lane scripts/wave-run-detached demo-lane "python -m pytest examples/fake-app/tests"

# Peek safely without catting logs.
scripts/wave peek --task demo-lane

# Record proof.
mkdir -p examples/fake-app/.agent-wave/completions examples/fake-app/.agent-wave/traces
cp templates/completion-receipt.md examples/fake-app/.agent-wave/completions/example-completion.md
cp templates/trace-event.json examples/fake-app/.agent-wave/traces/example-wave-trace.json

# Review before merge.
scripts/wave milestone
```

## Goal Chains

Goal Chains split one larger objective into ordered child GoalSpecs, then materialize child `goal.json`, `context_pack.md`, `receipt.json`, `chain_status.json`, and `chain_completion.md` artifacts. The MVP is sequential and does not apply patches or launch swarms.

The first real project chain is Webbuilder Publish MVP, loaded from the final Webbuilder manifesto at `runs/build_chains/webbuilder-publish-mvp`. It is planning-only in this repo: worker launch is disabled, context packs stay compact, and source edits belong to the separate Webbuilder lane.

```bash
scripts/codelanes goal-chain-init --lane demo --title "Demo chain" --objective "Make one small validated fake-app improvement"
scripts/codelanes goal-chain-materialize --chain-file runs/build_chains/demo-demo-chain/chain.json
scripts/codelanes goal-chain-next --chain-file runs/build_chains/demo-demo-chain
scripts/codelanes goal-receipt-update --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state --status complete --tests-result passed --command "python -m pytest examples/fake-app/tests" --changed-file "examples/fake-app/README.md" --next-action "Proceed to next child goal"
scripts/codelanes goal-chain-refresh --chain-file runs/build_chains/demo-demo-chain
scripts/codelanes goal-chain-status --chain-file runs/build_chains/demo-demo-chain
```

Plan, dry-run, peek, and collect one supervised child worker:

```bash
scripts/codelanes worker-plan --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-run --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-peek --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-collect --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
```

Real worker execution requires both `--execute` and `CODELANES_ENABLE_WORKER_EXEC=1`. Worker status reports marker files, receipt state, and log size only; it does not dump raw logs.

## Builder Harness Contracts

The builder harness now has three small contracts for supervised progress:

- Goal Chain Progress: child receipts drive chain status, completion rollups, and next-goal selection.
- Session Contract: `runner_manifest.json` includes the mode, lane, branch, tool boundary, context budget, and artifact paths a future launcher must honor.
- CommandResult: commands can return compact observations with artifact paths and next actions instead of raw log dumps.
- Supervised Worker Launcher: one child goal can prepare a prompt, dry-run a manifest, launch behind a two-part execution gate, peek compact status, collect receipt state, and refresh its parent chain.

The bounded repair loop is documented as a scaffold only. Repair execution, swarms, autonomous patch application, integration apply mode, and complex scheduling remain out of scope.

## Safety Model

CodeLanes is built for supervised automation, not autonomous branch integration.

- Work happens in lanes with expected worktrees and branches.
- State packs are small enough to inspect in a diff.
- Detached runs write logs outside source or through a sanitized runtime artifact bridge.
- Detached run status is inspected through marker files, log size, completion JSON readiness, and narrow status grep.
- Completion receipts list changed files, validation commands, blockers, and merge posture.
- Trace events connect receipts to the runs and goals that produced them.
- Learning ledger entries are explicit, reviewed, and reversible.
- Healing loops have attempt limits and stop with a receipt.
- Merge gates require review before branch integration.
- Forbidden-path audits keep private paths, secrets, raw logs, and generated runtime sprawl out of public artifacts.

## Roadmap

Completed public primitives:

- v0.1 Lane Harness
- v0.2 State Packs
- v0.3 Skill Library
- v0.4 Wave Crew
- v0.5 Auto-Build Roadmap Runner
- v0.6 Context Packs + Completion Receipts
- Builder Harness MVP
- Sequential Goal Chains + Goal Chain Progress
- Session Contract + CommandResult
- Supervised Worker Launcher MVP
- Webbuilder Publish MVP as the first real project chain

Next public primitives:

1. Integration Gate MVP
2. Bounded Repair Execution MVP
3. Live codex-builder port
4. First Webbuilder Goal 0 dry-run
5. Reviewer subagent as a read-only tool

Swarms are deferred.

See [docs/roadmap/goals.md](docs/roadmap/goals.md) for details.

## Learn More

- [Technical Introduction](docs/articles/codelanes-technical-introduction.md)
- [Launch Thread](docs/articles/x-launch-thread.md)
- [Positioning](docs/articles/positioning.md)
- [Clone and Run](docs/guides/clone-and-run.md)
- [Wave Protocol Inside CodeLanes](docs/concepts/agent-wave-protocol.md)
- [State Packs](docs/concepts/state-packs.md)
- [Wave Crew](docs/concepts/wave-crew.md)
- [Trace Graph](docs/concepts/trace-graph.md)
- [Learning Ledger](docs/concepts/learning-ledger.md)
- [Bounded Healing Loop](docs/concepts/bounded-healing-loop.md)
- [Goal Chain Waves](docs/concepts/goal-chain-waves.md)
- [Autobrowse Proof](docs/concepts/autobrowse-proof.md)
- [Builder Session Contract](docs/build_harness/session_contract.md)
- [Builder CommandResult](docs/build_harness/command_results.md)
- [Builder Bounded Repair Loop](docs/build_harness/bounded_repair_loop.md)
- [Builder Supervised Worker Launcher](docs/build_harness/supervised_worker_launcher.md)

## Contributing

Contributions are welcome when they preserve the core contract: stateful lanes, auditable receipts, bounded repair, and human merge gates. Good first contributions include clearer templates, additional generic examples, new skills, and validation scripts that improve safety without coupling the project to private infrastructure.

GitHub: https://github.com/agentwave-dev/CodeLanes

X: @getcodelanes
