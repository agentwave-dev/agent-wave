# Context Pack: validate_and_receipt

## Goal Summary
- Lane: demo
- Workflow: validation
- Objective: Validate and write proof for: Show progress through a chain
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
- Configured tests pass or blockers are documented.
- Receipts identify next action.

## Test Commands
- python -m pytest examples/fake-app/tests

## Runtime Commands
- No runtime commands configured.

## Receipt Requirements
- context_pack.md
- receipt.json
- chain_completion.md

## Stop Conditions
- Validation fails without a documented blocker.
- Receipt proof is missing.
