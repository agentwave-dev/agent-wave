# Healing Receipt

Lane: demo-lane
Goal: goal-demo-001
Trace: trace-fake-app-demo-001
Attempt: 1 of 2
Started: 2026-01-01T00:10:00Z
Completed: 2026-01-01T00:12:00Z

## Failure

Command: `python -m pytest examples/fake-app/tests`
Failure Class: test-failure

## Diagnosis

The example test expected a response string that did not match the fake-app function.

## Repair

- `examples/fake-app/tests/test_app.py`: aligned the expected response with the intended fake-app behavior.

## Validation

- `python -m pytest examples/fake-app/tests`

## Result

passed

## Merge Gate

pending-human-review
