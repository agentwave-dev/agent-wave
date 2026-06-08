# Context Pack: implement_small_change

## Goal Summary
- Lane: demo
- Workflow: narrow_implementation
- Objective: Implement one bounded change for: Show progress through a chain
- Created at: 2026-06-08T01:10:46Z

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
- The bounded change is implemented.
- No patches are applied automatically by the chain.

## Test Commands
- python -m pytest examples/fake-app/tests

## Runtime Commands
- No runtime commands configured.

## Receipt Requirements
- context_pack.md
- receipt.json

## Stop Conditions
- Dependency receipt has a blocker.
- Forbidden path or private data would be touched.
