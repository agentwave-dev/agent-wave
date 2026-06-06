# Lane Prompt

LANE: demo-lane
EXPECTED_BRANCH: feature/demo-lane
EXPECTED_WORKTREE: /tmp/agent-wave-demo

TASK
Make a scoped change, run tests, write a completion receipt, and stop before merge.

RULES
- Verify lane, branch, worktree, and status before edits.
- Do not touch forbidden paths.
- Use fake data only.
- Run available tests.
- Write a completion receipt.

