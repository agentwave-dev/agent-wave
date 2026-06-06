# State Packs

State packs keep lane memory out of chat scrollback. A pack has two parts:

- `.agent-wave/lanes/<lane>.yaml`: expected worktree, branch, commands, forbidden paths, and receipt location.
- `.agent-wave/state/<lane>.json`: current task, run state, blockers, last receipt, and recent verification.

State packs should be small enough to review in a diff. They should never contain credentials or private runtime payloads.

