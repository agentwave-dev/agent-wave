# Wave Crew

Wave Crew is a supervised subagent pattern. The supervisor owns the plan and merge proposal. Subagents own bounded work products.

Default roles:

- Planner: turns roadmap items into a wave plan.
- Implementer: makes scoped source changes.
- Tester: runs verification and reports failures.
- Docs: updates public documentation.
- Safety: checks forbidden paths and sensitive content.
- Merge Review: summarizes diffs, risks, and follow-up work.

Each subagent gets a separate prompt, state pack entry, and completion receipt. No subagent merges autonomously.

