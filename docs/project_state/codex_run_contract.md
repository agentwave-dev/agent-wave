# Codex Run Contract

This contract describes a token-efficient coding-agent run.

## Before Work

1. Verify worktree, branch, and lane state.
2. Read the project state pack and lane file.
3. Generate or use a context pack for the selected lane and skill.
4. Confirm allowed paths, forbidden paths, current goal, blockers, and receipt budget.
5. Write a heartbeat artifact when entering deeper exploration or implementation.

## During Work

- Keep file reads bounded to the target paths.
- Prefer search summaries over broad file dumps.
- Keep raw logs in runtime paths.
- Stop and summarize when logs exceed the configured cap.
- Keep edits scoped to the lane goal.

## Completion

Every run should produce compact evidence:

- `reports/codex_runs/<task>/completion.json`
- `reports/completions/<task>.receipt.md`
- `reports/completions/latest_codex_completion.md`

Receipts must include changed files, commands run, tests/build result, blockers, next recommended action, and raw log path only.

## Detached Run Pattern

Every detached run should create:

- `/tmp/<task>_<timestamp>.run`
- `/tmp/<task>_<timestamp>.log`
- `/tmp/<task>_<timestamp>.done`

The `.run` file should contain `TASK`, `ROOT`, `PROMPT`, `LOG`, `DONE`, and `STARTED_AT`.
