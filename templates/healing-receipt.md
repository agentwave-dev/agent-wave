# Healing Receipt

Lane: demo-lane
Goal: goal-demo-001
Trace: trace-demo-lane-001
Attempt: 1 of 2
Started: 2026-01-01T00:00:00Z
Completed: 2026-01-01T00:05:00Z

## Failure

Command: `python -m pytest examples/fake-app/tests`
Failure Class: test-failure

## Diagnosis

Summarize the smallest plausible cause.

## Repair

List changed files and why each change was necessary.

## Validation

- `python -m pytest examples/fake-app/tests`

## Result

passed

## Merge Gate

pending-human-review
