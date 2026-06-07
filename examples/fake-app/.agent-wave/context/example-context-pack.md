# Context Pack: demo-lane

Goal: clean up one fake-app copy string without touching unrelated files.

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
- Write compact completion JSON.
- Prefer artifact paths over inline logs.

## Allowed Paths

- examples/fake-app/
- reports/completions/

## Forbidden Paths

- .env
- secrets
- customer-data
- raw logs

## Completion Requirements

- Write compact completion JSON.
- Write a markdown receipt under 120 lines.
- Include raw log path only.
