# Completion Receipts

A completion receipt is the source of truth for whether a lane finished a task.

Receipts include:

- Lane and task id
- Run id
- Worktree and branch verified
- Files changed
- Tests run
- Audit results
- Commit status
- Blockers and next actions
- Raw log path only

Token-efficient receipts also write machine-readable evidence:

- `reports/codex_runs/<task>/completion.json`
- `reports/completions/<task>.receipt.md`
- `reports/completions/latest_codex_completion.md`

Receipts should be written before a merge proposal and after verification commands complete.

## Receipt Limits

- Markdown receipt max: 120 lines.
- No raw logs.
- No full diffs.
- Include changed files, commands run, tests/build result, blockers, next recommended action, commit status, push status, and raw log path only.

## Safe Detached-Run Status

Use:

```bash
scripts/wave peek --task <task>
```

This reports active process status, done marker presence, log size, completion JSON readiness, and narrow status grep. It must not use `cat "$LOG"`, broad `tail`, full diff dumps, or pasted completion markdown.
