# Supervised Worker Launcher

The supervised worker launcher runs one bounded child goal at a time. Dry-run is the default. Execution is disabled unless an operator passes `--execute` and sets `CODELANES_ENABLE_WORKER_EXEC=1`.

## Commands

Plan worker artifacts without launching Codex:

```bash
scripts/codelanes worker-plan --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
```

Prepare or refresh the dry-run worker manifest:

```bash
scripts/codelanes worker-run --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
```

Launch one detached worker only after the explicit safety gate:

```bash
CODELANES_ENABLE_WORKER_EXEC=1 scripts/codelanes worker-run --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state --execute
```

Peek at compact status:

```bash
scripts/codelanes worker-peek --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
```

Collect the done marker, optional completion JSON, receipt state, and chain refresh:

```bash
scripts/codelanes worker-collect --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
```

## Artifacts

Each child goal directory gets:

- `worker_prompt.md`
- `worker_run.json`
- `worker_status.json`

Detached execution, when enabled, uses `/tmp/<task>_<timestamp>.run`, `.log`, and `.done`. The CLI reports the log path and byte size only. It does not print raw logs.

## Receipt Collection

`worker-collect` reads `worker_run.json`, the done marker, `receipt.json`, and optional completion JSON at either:

- `reports/codex_runs/<task>/completion.json`
- `<goal_dir>/completion.json`

When completion JSON exists, these compact fields may update the receipt:

- `changed_files`
- `commands_run`
- `tests_build_result`
- `blockers`
- `next_recommended_action`
- `raw_log_path`

If the done marker has `exit_code=0`, pending receipts are marked complete when validation is `passed` or `not_run` with a clear note. If the done marker has a nonzero exit code, the receipt is marked blocked with a compact blocker summary. If the goal belongs to a chain, `goal-chain-refresh` is run after collection.

## Limits

- No swarms.
- No parallel workers.
- No patch application.
- No integration apply mode.
- No broad autonomous execution.
- No raw log dumps in CLI output, docs, receipts, or completion reports.
