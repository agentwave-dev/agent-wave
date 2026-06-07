# CodeLanes Builder Harness Architecture

CodeLanes Builder Harness is a supervised build operating system, not a giant prompt and not an uncontrolled super-agent. The MVP makes one bounded coding-agent run reliable before introducing multi-agent swarms.

## Builder Definition

Builder = workflow selector + goal decomposer + context packager + lane guard + runner supervisor + receipt collector + repair loop manager + patch queue manager + integration manager + state steward.

The builder coordinates the lifecycle of a bounded implementation goal. It chooses the workflow, converts the objective into a durable goal record, packages only the context needed for that goal, verifies that the lane is safe to run, records runner intent, collects receipts, and preserves enough state for repair or integration without hiding mutations.

## Builder Modes

- `plan`: Convert a broad objective into one or more bounded GoalSpecs with clear acceptance criteria and stop conditions.
- `worker`: Execute one bounded implementation pass inside a lane after guard checks and context packaging.
- `repair`: Re-run a bounded fix attempt against a failed receipt, limited by `max_repair_attempts`.
- `review`: Inspect changed files, receipts, proofs, and safety constraints before integration.
- `integration`: Queue, inspect, and eventually apply accepted patches into the integration lane.
- `memory`: Preserve durable state, receipts, lessons, and future context without importing private project data.

## CodeLane Model

A CodeLane is a supervised operating boundary. Each lane declares:

- `source_root`: the source tree the lane expects to work in.
- `runtime_data_root`: the runtime or artifact root used for proof collection.
- `expected_branch`: the branch the lane expects before work begins.
- `tmux_session`: an operator-visible session name for future detached runners.
- `owns`: paths the lane may normally modify.
- `forbidden`: paths the lane must not touch or include.
- `proof_roots`: paths where receipts, logs, and validation artifacts may be written.
- `default_tests`: test commands expected for the lane.

The lane guard compares the current worktree and branch to the lane declaration and returns a structured result. It does not exit directly; callers decide whether to stop, retry, or report.

## Artifact Flow

The MVP flow is:

1. `GoalSpec`: durable JSON goal record containing lane, workflow, objective, path boundaries, acceptance criteria, commands, proof requirements, and stop conditions.
2. `ContextPack`: bounded markdown artifact written to `runs/build/<goal_id>/context_pack.md`. It summarizes the goal, lane, allowed paths, forbidden paths, acceptance criteria, tests, and receipt requirements.
3. `RunnerManifest`: dry-run intent record for the future supervised runner. MVP v0 does not launch Codex workers; it records the exact context and lane metadata needed by a later runner.
4. `Receipt`: structured JSON artifact written to `runs/build/<goal_id>/receipt.json`. It records worktree, branch, changed files, tests run, exit codes, blocker classification, patch path, and next action.
5. `PatchPlaceholder`: pending patch summary under `patches/pending/` when there is no diff or no patch should be applied yet.

This chain makes build state inspectable without requiring a live worker swarm.

## No-Swarm MVP Boundary

MVP v0 does not launch Codex workers, create swarms, run detached agents, apply patches, or mutate production runtime data. It only creates durable input and output artifacts for one supervised build run:

- lane registry loading
- lane guard result
- GoalSpec creation and validation
- context pack creation
- dry-run runner manifest creation
- receipt initialization
- patch placeholder creation
- focused tests

## Future-State Roadmap

1. Add runner supervision that consumes `RunnerManifest` and launches one worker with bounded context.
2. Add receipt-driven repair loops capped by GoalSpec limits.
3. Add patch queue review and integration gates.
4. Add integration mode that can apply approved patches after safety scans.
5. Add memory mode for durable lessons, state compaction, and cross-run continuity.
6. Add multi-lane orchestration only after single-run receipts, repair, patch review, and integration gates are dependable.
7. Add swarms last, as a coordination layer over stable lanes rather than as the core build mechanism.
