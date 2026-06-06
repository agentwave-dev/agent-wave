# Example Wave Task

LANE: demo-lane
EXPECTED_WORKTREE: /repo/fake-app
EXPECTED_BRANCH: feature/demo-lane

## Task

Run the fake-app baseline validation, write a completion receipt, link the receipt to a trace event, and leave the merge gate pending human review.

## Validation

- `python -m pytest examples/fake-app/tests`

## Safety

Use generic example data only. Do not include secrets, private paths, raw logs, or generated runtime artifacts.
