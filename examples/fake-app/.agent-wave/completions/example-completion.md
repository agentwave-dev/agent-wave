# Completion Receipt

Lane: demo-lane
Goal: goal-demo-001
Run: run-demo-001
Trace: trace-fake-app-demo-001
Worktree: /repo/fake-app
Branch: feature/demo-lane

## Outcome

Fake-app baseline validation completed.

## Files Changed

- examples/fake-app/src/app.py
- examples/fake-app/tests/test_app.py

## Validation

- `python -m pytest examples/fake-app/tests`

## Evidence

- Trace: `examples/fake-app/.agent-wave/traces/example-wave-trace.json`
- Log summary: `/tmp/example_wave.log`

## Blockers

None

## Merge Posture

pending-human-review
