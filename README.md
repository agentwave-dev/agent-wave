# Agent Wave

Agent Wave is a public multi-agent auto-build harness for running many AI coding agents across separate worktrees and tasks without losing state, mixing branches, or drowning in logs.

The project is intentionally generic. It does not assume a host product, a private runtime, or a specific vendor. The first public scaffold demonstrates v0.1 through v0.5:

- v0.1 Lane Harness: verify lanes, worktrees, branches, forbidden paths, detached runs, completion receipts, and milestone commits.
- v0.2 State Packs: keep durable lane state in `.agent-wave/lanes` and `.agent-wave/state`.
- v0.3 Skill Library: codify repeatable lane, audit, receipt, state, and merge-review workflows.
- v0.4 Wave Crew: split work across supervised subagents with isolated state and receipts.
- v0.5 Auto-Build Roadmap Runner: turn roadmap items into plans, prompts, detached runs, test summaries, receipts, and merge proposals.

## Wedge

Run many AI coding agents across separate worktrees and tasks simultaneously without losing state, mixing branches, or drowning in logs.

## Core Concepts

- Lanes: named execution tracks with expected worktree, branch, and guardrails.
- State packs: small files that preserve current lane status, blockers, receipt pointers, and runtime bridge metadata.
- Skills: local, versioned operating procedures for repeatable agent work.
- Detached runs: background agent or shell runs with durable logs and receipts.
- Runtime artifact bridge: a controlled path for summaries and normalized events instead of raw runtime sprawl.
- Completion receipts: explicit evidence that a lane reached a specific outcome.
- Forbidden-path gates: deny lists that keep private, generated, or sensitive paths out of public artifacts.
- Milestone commit gates: checks that must pass before a local milestone commit.
- Wave Crew: supervised subagents with separate prompts, state packs, receipts, and no autonomous merge.

## Quick Start

```bash
cd /path/to/agent-wave
scripts/wave smoke
scripts/wave audit
python -m pytest examples/fake-app/tests
```

See [Getting Started](docs/guides/getting-started.md) for a guided walkthrough.

