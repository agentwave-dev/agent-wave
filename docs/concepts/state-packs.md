# State Packs

State packs keep lane memory out of chat scrollback. They are the durable part of the system: the model is stateless, the lane is stateful.

## Files

- `.agent-wave/lanes/<lane>.yaml`: expected worktree, branch, commands, forbidden paths, merge policy, and receipt location.
- `.agent-wave/state/<lane>.json`: current task, run state, blockers, last receipt, trace pointer, learning ledger pointer, healing attempts, and recent verification.
- `docs/project_state/*.md`: durable project and lane state that agents read before generated prompts.
- `.agent-wave/context/latest_<lane>.md`: generated context pack for one lane, skill, and goal.

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
- Token and receipt budgets
- Read-before-work files

## What Does Not Belong In State

- Credentials
- Raw logs
- Private runtime payloads
- Local-only absolute paths unless they are generic examples
- Generated artifacts that cannot be reviewed safely
- Full diffs or full project history

## Context Pack Command

```bash
scripts/wave context-pack --lane demo-lane --skill token-efficient-codex-run --goal "run fake-app tests"
```

The generated context pack must stay under 200 lines and include lane state, selected skill, goal, allowed paths, forbidden paths, blockers, and completion requirements.

State packs should be small enough to review in a diff. A stale state pack is a bug because it makes the lane lie about what happened.
