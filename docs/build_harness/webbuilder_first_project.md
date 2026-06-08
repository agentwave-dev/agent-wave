# Webbuilder First Project Chain

Webbuilder is the first real CodeLanes project because it has the right shape for the harness: a broad product objective, strict runtime safety boundaries, clear sequencing, and enough private-operational risk that token-efficient receipts matter more than a single large prompt.

The loaded chain is `webbuilder-publish-mvp` and lives under `runs/build_chains/webbuilder-publish-mvp`. It materializes the final Webbuilder manifesto into nine ordered child goals. This is planning and artifact setup only; the real Webbuilder source repo is not modified by loading the chain.

## Source Of Truth

The final Webbuilder manifesto supersedes legacy Webbuilder goals. Older goals should not be copied forward by default. They can be reintroduced only when a later receipt explicitly revalidates them against the current manifesto, Webbuilder lane guards, and the active child goal.

## Execution Model

The chain is sequential. Each child goal has its own compact `goal.json`, `context_pack.md`, `runner_manifest.json`, and `receipt.json`. Worker execution remains disabled unless an operator explicitly enables it later.

Token-efficient execution should follow these rules:

- Use the child context pack, not the full manifesto, as the worker prompt base.
- Keep each child goal to at most 10 acceptance criteria.
- Keep each context pack under 200 lines.
- Mark blockers in `receipt.json` instead of carrying long raw logs forward.
- Use `goal-chain-next` to select the next child from receipts.
- Do not launch subagents by default.
- Consider an optional reviewer only after the child goal has a receipt.

## Webbuilder Guards

Every child goal carries these operational guards:

- `expected_worktree: /home/joe/worktrees/wander-webbuilder`
- `runtime_data_root: /home/joe/apps`
- direct source edits happen only in the Webbuilder lane
- `/home/joe/apps` is read-only unless deploy or sync is explicitly approved
- no service restart unless a runtime safety goal explicitly allows it

The forbidden scope includes direct-booking checkout ownership, live reservation writes, raw secrets, production DNS mutation, and custom domain automation before generated subdomains work.

## Next Step

The next operator action is either to port the same CodeLanes primitives into `codex-builder` or to run a dry-run for Goal 0 and write the first real receipt.
