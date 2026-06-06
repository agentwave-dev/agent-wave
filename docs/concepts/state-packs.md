# State Packs

State packs keep lane memory out of chat scrollback. They are the durable part of the system: the model is stateless, the lane is stateful.

## Files

- `.agent-wave/lanes/<lane>.yaml`: expected worktree, branch, commands, forbidden paths, merge policy, and receipt location.
- `.agent-wave/state/<lane>.json`: current task, run state, blockers, last receipt, trace pointer, learning ledger pointer, healing attempts, and recent verification.

## What Belongs In State

- Current objective and task id
- Expected branch and worktree
- Active detached run id
- Latest completion receipt path
- Latest trace event id
- Known blockers
- Validation commands and last outcomes
- Runtime artifact bridge metadata
- Merge-gate posture

## What Does Not Belong In State

- Credentials
- Raw logs
- Private runtime payloads
- Local-only absolute paths unless they are generic examples
- Generated artifacts that cannot be reviewed safely

State packs should be small enough to review in a diff. A stale state pack is a bug because it makes the lane lie about what happened.
