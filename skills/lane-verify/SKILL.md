# lane-verify

Use this skill before lane work starts.

Steps:

1. Confirm `pwd` equals the lane expected worktree.
2. Confirm `git branch --show-current` equals the lane expected branch.
3. Run `git status --short --branch`.
4. Stop if the worktree or branch does not match.
5. Record the result in the lane state pack.

