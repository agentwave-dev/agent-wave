# runtime-sync-check

## when_to_use

Use this skill when source-code proof may differ from runtime proof, or when a detached run should be checked without reading raw logs.

## inputs

- Lane name.
- Runtime data root.
- Task id.
- Expected completion JSON path.
- Expected done marker path.
- Validation commands.

## allowed_actions

- Check runtime marker files.
- Check completion JSON readiness.
- Compare source test results with runtime status summaries.
- Reference sanitized runtime artifact paths.
- Run `scripts/wave peek --task <task>`.

## forbidden_actions

- Do not copy runtime artifacts into source unless sanitized and intentional.
- Do not commit raw logs.
- Do not infer runtime success from source tests alone.
- Do not paste raw runtime output into receipts.

## commands

```bash
scripts/wave peek --task <task>
test -f reports/codex_runs/<task>/completion.json
python -m json.tool reports/codex_runs/<task>/completion.json >/dev/null
```

## stop_conditions

- Runtime marker files are missing.
- Completion JSON is missing or invalid.
- Runtime status contradicts source validation.
- Runtime data points outside the lane runtime root or `/tmp` marker pattern.

## completion_receipt_rules

- Separate source validation from runtime validation.
- Include artifact paths, not artifact contents.
- Include contradictions as blockers.
- Include the exact status commands used.
