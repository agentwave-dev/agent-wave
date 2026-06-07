# completion-receipt-writer

## when_to_use

Use this skill at the end of a coding-agent run or when a run stops with a blocker and needs durable, compact evidence.

## inputs

- Task id.
- Lane name.
- Run id.
- Worktree and branch.
- Changed files.
- Commands run.
- Test/build outcomes.
- Raw log path.
- Blockers and next recommended action.

## allowed_actions

- Read command summaries and validation outputs.
- Read file lists from version-control status.
- Write compact JSON and markdown receipts.
- Update the latest receipt pointer.

## forbidden_actions

- Do not paste raw logs.
- Do not paste full diffs.
- Do not paste full completion markdown into chat.
- Do not invent validation outcomes.
- Do not mark blocked work as complete.

## commands

```bash
mkdir -p reports/codex_runs/<task> reports/completions
cp templates/completion.json reports/codex_runs/<task>/completion.json
cp templates/token-efficient-completion-receipt.md reports/completions/<task>.receipt.md
cp reports/completions/<task>.receipt.md reports/completions/latest_codex_completion.md
```

## stop_conditions

- Validation result is unknown.
- Changed files cannot be determined.
- Raw log path is missing for a detached run.
- Receipt would exceed 120 lines.

## completion_receipt_rules

- Keep JSON parseable.
- Keep markdown under 120 lines.
- Include raw log path only, not log content.
- Include blockers, even when the blocker is `None`.
- Include whether commit and push were made.
