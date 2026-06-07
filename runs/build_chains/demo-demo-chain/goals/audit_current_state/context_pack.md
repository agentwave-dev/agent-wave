# Context Pack: audit_current_state

## Goal Summary
- Lane: demo
- Workflow: audit
- Objective: Audit current state for: Make one small validated fake-app improvement
- Created at: 2026-06-07T17:59:06Z

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
- Current behavior and constraints are identified.

## Test Commands
- python -m pytest examples/fake-app/tests

## Runtime Commands
- No runtime commands configured.

## Receipt Requirements
- context_pack.md
- receipt.json

## Stop Conditions
- Wrong worktree or branch.
- Forbidden path or private data would be touched.
