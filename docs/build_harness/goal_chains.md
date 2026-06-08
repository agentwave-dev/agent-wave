# Goal Chains

A Goal Chain is an ordered set of bounded GoalSpecs for one larger objective. It turns a broad request into small child goals that can each carry their own context pack, receipt, validation commands, stop conditions, and proof requirements.

In the MVP, a chain is a planning and materialization layer on top of the Builder Harness:

```text
chain.yaml
-> chain.json
-> child goal.json files
-> child context_pack.md files
-> child receipt.json files
-> chain_status.json
-> chain_completion.md
```

The chain does not apply patches, merge branches, launch swarms, or retry repairs automatically. A child goal can be handed to the supervised worker launcher, which defaults to dry-run artifacts and only launches one worker behind the explicit execution gate.

## Command Flow

Initialize a sequential chain:

```bash
scripts/codelanes goal-chain-init --lane demo --title "Demo chain" --objective "Make one small validated fake-app improvement"
```

Materialize child goals and receipt stubs:

```bash
scripts/codelanes goal-chain-materialize --chain-file runs/build_chains/demo-demo-chain/chain.json
```

Mark a child goal complete after manual work and validation:

```bash
scripts/codelanes goal-receipt-update \
  --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state \
  --status complete \
  --tests-result passed \
  --command "python -m pytest examples/fake-app/tests" \
  --changed-file "examples/fake-app/README.md" \
  --next-action "Proceed to next child goal"
```

Refresh chain rollups from child receipts:

```bash
scripts/codelanes goal-chain-refresh --chain-file runs/build_chains/demo-demo-chain
```

Get the next incomplete child goal:

```bash
scripts/codelanes goal-chain-next --chain-file runs/build_chains/demo-demo-chain
```

Review compact chain status:

```bash
scripts/codelanes goal-chain-status --chain-file runs/build_chains/demo-demo-chain
```

Plan and dry-run one child worker:

```bash
scripts/codelanes worker-plan --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-run --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-peek --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-collect --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
```

Execution requires both `--execute` and `CODELANES_ENABLE_WORKER_EXEC=1`. `worker-collect` updates `receipt.json` from the done marker and optional compact `completion.json`, then refreshes chain status when the child belongs to a chain.

## Progress Commands

`goal-receipt-update` preserves existing receipt fields while appending compact progress evidence. It accepts `complete`, `blocked`, and `pending` statuses; validation results are `passed`, `failed`, or `not_run`. If a child is marked complete without a validation result, the receipt records `not_run`.

`goal-chain-refresh` re-reads every child `receipt.json`, updates status counts, records the next incomplete child, and writes both rollup artifacts. `goal-chain-next` prints only the next incomplete child goal and its artifact paths. `goal-chain-status` prints the same compact rollup for operators.

## When To Use A Goal Chain

Use a Goal Chain when one objective is too large for a single GoalSpec but still has a clear sequential path. Good fits include:

- audit, implement, validate flows
- docs plus tests plus receipt rollups
- small multi-step harness changes
- migration plans that need proof at each step

Use a single GoalSpec when the work is already narrow enough to fit in one context pack and one receipt.

## Goal Chain Vs GoalSpec

A GoalSpec describes one bounded unit of work: lane, workflow, objective, allowed paths, forbidden paths, tests, proof, and stop conditions.

A Goal Chain describes how multiple GoalSpecs should be ordered. Each child goal remains independently inspectable. The chain adds:

- a shared chain id, title, and objective
- ordered dependencies by child goal id
- per-child materialized harness artifacts
- chain-level status and completion rollups

## Why Sequential In The MVP

The MVP supports only ordered sequential chains. A child goal can depend on prior child goal ids, and dependencies must point backward in the list.

This keeps the first implementation small and auditable. It avoids a DAG scheduler, parallel worker launch, uncontrolled execution, and hidden integration behavior. Human merge gates and receipts remain the source of truth.

## Safety

Goal Chains preserve the existing Builder Harness safety model:

- child goals include allowed and forbidden paths
- context packs remain bounded
- receipt stubs are required before work is treated as complete
- blockers are surfaced in `chain_status.json`
- `chain_completion.md` is a rollup, not a merge approval
- worker status reports log paths and byte counts, not raw logs
- human review and merge gates remain required

## Future Work

Later versions can add parallel waves once the sequential receipt and worker contracts are stable. Future directions include:

- parallel wave grouping for independent child goals
- integration apply mode for reviewed patch queues
- repair loops with explicit attempt budgets
- richer chain status validation
