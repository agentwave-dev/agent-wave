# Wave Crew

Wave Crew is a supervised subagent pattern. The supervisor owns the plan and merge proposal. Subagents own bounded work products.

## Default Roles

- Planner: turns roadmap items into a wave plan.
- Implementer: makes scoped source changes.
- Tester: runs verification and reports failures.
- Docs: updates public documentation.
- Safety: checks forbidden paths and sensitive content.
- Merge Review: summarizes diffs, risks, and follow-up work.

## Subagent Contract

Each subagent gets:

- A bounded prompt
- A role-specific skill
- A state pack entry
- A detached run id
- A completion receipt
- A trace event

No subagent merges autonomously. The supervisor collects receipts, updates the trace graph, records useful lessons in the learning ledger, and prepares the merge gate for human review.

## Why This Matters

Without a crew contract, many agents working at once create branch drift, duplicated work, and noisy logs. With Wave Crew, each agent has a lane, a role, and a receipt trail.
