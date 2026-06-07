# Context Pack: <lane>

Goal: <bounded goal>

Lane:
Branch:
Status:
Tooling root:
Target source root:
Runtime data root:

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

## Read Before Work

- <state pack path>

## Allowed Paths

- <allowed path>

## Forbidden Paths

- <forbidden path>

## Completion Requirements

- Completion JSON under `reports/codex_runs/<task>/completion.json`.
- Markdown receipt under `reports/completions/`.
- Receipt max 120 lines.
- Raw log path only.
