# Context Pack: demo-lane

Goal: clean up destination-domain DNS panel copy only
Lane: demo-lane
Branch: main
Status: ready
Tooling root: .
Target source root: examples/fake-app
Runtime data root: .agent-wave/runtime/demo-lane

## Token Rules
- Read state pack first.
- Do not restate project history.
- Read only target files listed in this context pack.
- Do not scan unrelated files.
- Do not print full diffs or full files.
- Write a heartbeat artifact before deep work.
- Write compact completion JSON.
- If logs exceed the cap, stop broad exploration and summarize.
- Prefer artifact paths over inline logs.
- Use summary extraction commands instead of cat/tail.

## Current Goal
- Keep the fake app lane runnable while demonstrating token-efficient context packs and compact receipts.

## Read Before Work
- docs/project_state/README.md
- docs/project_state/current_build_state.md
- docs/project_state/token_efficiency_rules.md
- docs/project_state/codex_run_contract.md
- skills/token-efficient-codex-run/SKILL.md

## Allowed Paths
- README.md
- docs/
- examples/fake-app/
- scripts/
- skills/
- templates/
- .agent-wave/lanes/demo-lane.yaml
- .agent-wave/context/

## Forbidden Paths
- .codex
- .codex-runtime
- .env
- .env.*
- secrets
- customer-data
- runtime
- artifacts/raw
- vendor/private

## Last Receipts
- reports/completions/latest_codex_completion.md

## Known Blockers
- None

## Completion Budget
- 120 receipt lines, 200 context-pack lines, raw logs referenced by path only.

## Selected Skill: token-efficient-codex-run

## when_to_use

Use this skill when starting a Codex-style coding-agent run that should rely on durable lane state and a compact context pack instead of repeated project history, logs, diffs, or prior completion reports.

## inputs

- Lane name.
- Current goal.
- Lane YAML path.
- Project state pack paths.
- Allowed and forbidden paths.
- Completion budget.

## allowed_actions

- Read the lane file and listed state packs.
- Generate a context pack with `scripts/wave context-pack`.
- Inspect only files named by the context pack or necessary for the current goal.
- Write a heartbeat artifact before deeper implementation work.
- Write compact completion JSON and a markdown receipt.

## forbidden_actions

- Do not paste full project history into the prompt.
- Do not read unrelated source trees.
- Do not print full files or full diffs.
- Do not include raw logs in receipts or chat.
- Do not touch forbidden paths, secrets, tenant data, or private runtime artifacts.

## commands

```bash
scripts/wave smoke
scripts/wave audit
scripts/wave context-pack --lane demo-lane --skill token-efficient-codex-run --goal "describe the bounded task"
test "$(wc -l < .agent-wave/context/latest_demo-lane.md)" -le 200
```

## stop_conditions

- Lane file or skill file is missing.
- Worktree or branch does not match the lane contract.
- Required state pack is missing.
- The goal requires forbidden paths.
- Logs exceed the configured cap and cannot be summarized safely.

## completion_receipt_rules

- Receipt max: 120 lines.
- Include changed files, commands run, tests/build result, blockers, next recommended action, and raw log path only.
- Write `reports/codex_runs/<task>/completion.json`.
- Write `reports/completions/<task>.receipt.md`.
- Update `reports/completions/latest_codex_completion.md`.

## Completion Requirements
- Write reports/codex_runs/<task>/completion.json or the lane-specific equivalent.
- Write a markdown receipt under reports/completions/.
- Keep receipts under 120 lines.
- List changed files, commands run, tests/build result, blockers, next action, and raw log path only.
