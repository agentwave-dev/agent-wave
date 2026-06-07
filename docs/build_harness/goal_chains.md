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

The chain does not launch Codex workers, apply patches, merge branches, or retry repairs automatically. It only writes bounded artifacts that a human or future supervised runner can review.

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
- human review and merge gates remain required

## Future Work

Later versions can add parallel waves once the sequential receipt contract is stable. Future directions include:

- parallel wave grouping for independent child goals
- integration mode for reviewed patch queues
- repair loops with explicit attempt budgets
- richer chain status validation
- worker launch only after a human-approved runner contract exists
