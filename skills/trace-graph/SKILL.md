# trace-graph

Use this skill when a run, receipt, healing attempt, or merge review needs to be linked into the Trace Graph.

Steps:

1. Copy `templates/trace-event.json`.
2. Set `trace_id`, `event_id`, `event_type`, lane, goal id, and run id.
3. Link the completion or healing receipt.
4. Add sanitized artifact paths only.
5. Add parent event ids when this event depends on earlier work.
6. Record the current merge-gate status.
7. Update the lane state pack with the latest trace event id.
