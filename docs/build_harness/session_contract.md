# Session Contract

The session contract is the structured runner boundary for a future supervised CodeLanes worker. It records the lane, worktree, branch, mode, approval policy, tool boundary, context budget, artifact paths, and resume pointer before any worker is launched.

It differs from a prompt because it is not guidance for the model to interpret. It is an external contract that the launcher and operator can validate before the model receives context.

The MVP writes the contract inside `runner_manifest.json`. Worker launch remains disabled.

## Modes

- `plan`: read-only planning and goal shaping.
- `worker`: one bounded implementation pass inside lane-owned paths.
- `repair`: a bounded fix attempt against a failed receipt.
- `review`: read-only inspection of receipts, proofs, and changes.
- `integration`: patch-queue inspection only.
- `memory`: docs/state updates only.

Plan and review modes are read-only by contract. Worker and repair modes may include edit tools, but they remain constrained by lane and goal allowed paths. Integration mode is patch-queue only in the MVP.

## Why Boundaries Live Outside The Model

Approval policy and tool boundaries are launcher responsibilities. Keeping them outside the prompt makes the run auditable even if prompt text changes, and lets future launchers reject unsafe mode/tool/path combinations before execution.
