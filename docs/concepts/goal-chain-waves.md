# Goal Chain Waves

Goal Chain Waves turn a large roadmap item into small bounded runs.

The goal chain runner should not ask one agent to solve a vague roadmap item in one pass. It should break the work into ordered goals, map each goal to a lane and skill, and require receipts before advancing.

## Goal Chain Fields

- `chain_id`
- `objective`
- `lane`
- `goals`
- `required_skills`
- `validation`
- `merge_gate`

## Advancement Rule

A goal can advance only when its receipt is present, validation has been recorded, blockers are empty or accepted, and the trace graph links the work to the parent chain.

See `templates/goal-chain.yaml`.
