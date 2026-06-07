# Bounded Healing Loop

The Bounded Healing Loop is CodeLanes' repair model for failed runs.

Self-healing means bounded repair with receipts and human merge gates, not uncontrolled autonomy.

## Loop

```text
failure receipt -> classify blocker -> choose small repair -> run validation -> write healing receipt -> merge gate
```

## Rules

- Set an attempt budget before repair starts.
- Repair one failure class at a time.
- Keep source changes scoped to the failed objective.
- Record every attempt in a healing receipt.
- Stop when the budget is exhausted, the failure changes class, or validation passes.
- Never merge a healing change without a merge gate.

## Output

Each healing attempt should produce a receipt with the failed command, diagnosis, changed files, validation result, next action, and trace id.

See `templates/healing-receipt.md` and `examples/fake-app/.agent-wave/healing/example-healing-receipt.md`.
