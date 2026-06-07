# Wave Protocol Inside CodeLanes

Wave remains the protocol inside CodeLanes. It is a small operating contract for supervised multi-agent work across isolated lanes.

CodeLanes assumes the model is stateless and the lane is stateful. The protocol keeps durable state in files, not in chat scrollback.

## Protocol Chain

```text
lane -> state pack -> skill -> detached run -> receipt -> trace -> merge gate
```

1. A lane names the expected worktree, branch, status policy, and forbidden paths.
2. A state pack records current task, run ids, blockers, trace ids, and the latest receipt.
3. A skill defines the repeatable operating procedure for the task.
4. A detached run writes bounded logs outside source or through a sanitized bridge.
5. A completion receipt records evidence, tests, blockers, and merge posture.
6. A trace graph links the run to its goal, receipt, learning entry, healing attempt, and merge review.
7. A merge gate decides whether the work can enter the integration branch.

## Core Rule

Every agent run leaves a receipt. Every receipt belongs to a trace.

## Safety Rule

Self-healing means bounded repair with receipts and human merge gates, not uncontrolled autonomy.

## Vendor Neutrality

The protocol is vendor-neutral. Codex CLI, Claude Code, local scripts, and future agent runners can all participate when they honor the same lane, state, receipt, trace, and merge-gate contract.
