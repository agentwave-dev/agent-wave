# Trace Graph

The Trace Graph is the audit trail for Agent Wave.

Every agent run leaves a receipt. Every receipt belongs to a trace. A trace connects the goal, lane, skill, detached run, receipt, learning entry, healing attempt, browser proof, and merge review.

## Trace Event Fields

- `trace_id`: stable id for the wave or run family
- `event_id`: stable id for this event
- `event_type`: `goal_created`, `run_started`, `receipt_written`, `healing_attempted`, `merge_reviewed`, or another explicit event
- `lane`: lane that owns the event
- `goal_id`: roadmap or goal-chain item
- `run_id`: detached run id when applicable
- `receipt_path`: completion or healing receipt path
- `parent_event_ids`: prior events that this event depends on
- `artifact_paths`: sanitized proof files
- `merge_gate`: current merge posture

## Use

Trace events make multi-agent work inspectable after the chat is gone. They also make it possible to answer practical questions:

- Which run produced this diff?
- Which tests were run before this receipt?
- Did a healing loop change the source?
- Is the merge review based on source proof, runtime proof, or both?

See `templates/trace-event.json` and `examples/fake-app/.agent-wave/traces/example-wave-trace.json`.
