# Learning Ledger Entry

Date: 2026-01-01
Lane: demo-lane
Goal: goal-demo-001
Trace: trace-fake-app-demo-001
Evidence Receipt: examples/fake-app/.agent-wave/completions/example-completion.md

## Observation

The fake-app test command is the smallest useful baseline validation for this example.

## Decision

Use `python -m pytest examples/fake-app/tests` as the default validation command for fake-app examples.

## Future Instruction

When a fake-app task changes source behavior, run the fake-app tests before writing the completion receipt.

## Promotion Status

local-note
