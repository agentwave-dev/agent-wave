# Agent Wave Protocol

The Agent Wave protocol is a small operating contract for supervised multi-agent work.

1. A lane names the expected worktree, branch, status policy, and forbidden paths.
2. A state pack records current task, run ids, blockers, and the latest receipt.
3. A prompt starts from a lane template and names the exact objective.
4. A detached run writes logs outside the source tree or into a sanitized bridge.
5. A completion receipt records evidence, tests, blockers, and merge posture.
6. A milestone commit can happen only after verification gates pass.

The protocol is vendor-neutral. Codex CLI and Claude Code are examples of possible agent runners.

