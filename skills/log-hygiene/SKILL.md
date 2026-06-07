# log-hygiene

## when_to_use

Use this skill when inspecting long-running detached agent runs, large logs, failed validation, or any workflow that might tempt a maintainer to paste logs into chat.

## inputs

- Task id.
- `.run` marker path.
- Log path.
- Done marker path.
- Completion JSON path.
- Log-size cap.

## allowed_actions

- Show active process status.
- Show done marker presence.
- Show log size only.
- Show completion JSON readiness.
- Use narrow status/token grep.
- Record raw log paths in receipts.

## forbidden_actions

- Do not run `cat "$LOG"`.
- Do not run broad `tail -200 "$LOG"`.
- Do not paste full logs into docs, prompts, receipts, or chat.
- Do not dump full diffs as a substitute for a receipt.

## commands

```bash
scripts/wave peek --task <task>
wc -c /tmp/<task>_<timestamp>.log
grep -Eim 5 "token|status|error|failed|passed|complete" /tmp/<task>_<timestamp>.log || true
```

## stop_conditions

- Log exceeds the configured cap and the current task is broad exploration.
- The `.run` marker is missing.
- The done marker and active process disagree.
- Completion JSON is expected but missing.

## completion_receipt_rules

- Include log path and log size.
- Include only summarized error/status lines.
- Include the command used to inspect status.
- Include next action when log inspection finds a blocker.
