# CodeLanes Worker Prompt: audit_current_state

## Bounded Task
Audit current state for: Run one supervised fake-app goal

## Required Artifacts
- Context pack: runs/build_chains/demo-worker-launcher-demo/goals/audit_current_state/context_pack.md
- Goal file: runs/build_chains/demo-worker-launcher-demo/goals/audit_current_state/goal.json
- Receipt path: runs/build_chains/demo-worker-launcher-demo/goals/audit_current_state/receipt.json

## Boundaries
- Work only inside the allowed paths below.
- Do not touch forbidden paths.
- Do not expose raw logs in receipts, docs, reports, or command output.

## Allowed Paths
- examples/fake-app
- runs/build
- reports/completions

## Forbidden Paths
- .env
- secrets
- private
- runtime/production

## Tests
- python -m pytest examples/fake-app/tests

## Completion Requirement
- Update receipt.json or write completion.json before exiting.
- completion.json may be written at reports/codex_runs/<task>/completion.json or in this goal directory.
- Include compact JSON fields: changed_files, commands_run, tests_build_result, blockers, next_recommended_action, raw_log_path.
- Mark blockers clearly when the bounded task cannot be completed.
