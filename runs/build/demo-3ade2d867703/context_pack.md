# Context Pack: demo-3ade2d867703

## Goal Summary
- Lane: demo
- Workflow: narrow_implementation
- Objective: demo bounded goal
- Created at: 2026-06-07T17:48:20Z

## Lane Summary
- Source root: /repo
- Runtime data root: /runtime
- Expected branch: main
- Tmux session: codelanes-demo

## Allowed Paths
- examples/fake-app
- runs/build
- reports/completions

## Forbidden Paths
- .env
- secrets
- private
- runtime/production

## Acceptance Criteria
- All requested artifacts are created.
- Configured tests pass.

## Test Commands
- python -m pytest examples/fake-app/tests

## Runtime Commands
- No runtime commands configured.

## Receipt Requirements
- receipt.json
- context_pack.md

## Stop Conditions
- Wrong worktree or branch.
- Unrelated dirty tracked files.
- Forbidden path or private data would be touched.
