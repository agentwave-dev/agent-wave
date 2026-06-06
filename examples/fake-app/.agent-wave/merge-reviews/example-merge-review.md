# Merge Review

Lane: demo-lane
Goal: goal-demo-001
Trace: trace-fake-app-demo-001

## Summary

The fake-app baseline run has a completion receipt, trace event, and validation command.

## Validation Reviewed

- `python -m pytest examples/fake-app/tests`

## Safety Reviewed

- No secrets or private runtime artifacts are included.
- Example paths are generic.

## Risks

- Example trace validation is currently manual.

## Decision

pending-human-review
