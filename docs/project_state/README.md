# Project State Packs

Project state packs are durable, human-reviewable markdown files that keep repeated lane context out of chat prompts.

Agents should read the relevant state pack before work, then use a generated context pack for the current lane and skill. The state pack stores source-of-truth notes, current blockers, receipt pointers, and token/log limits. It must not store secrets, raw logs, private customer data, or full diffs.

## Files

- `current_build_state.md`: current public repo status, active primitives, and source-of-truth notes.
- `example_lane_state.md`: generic lane-level state that can be copied into a project.
- `token_efficiency_rules.md`: rules for bounded reading, bounded logging, and compact receipts.
- `codex_run_contract.md`: standard contract for Codex-style coding-agent runs.

## Why This Exists

Coding agents can burn large token budgets when every run repeats old project history, raw logs, diffs, and completion reports. State packs move repeated context into durable files. Context packs then select only the current lane, skill, goal, paths, blockers, and receipt requirements.

## Review Rules

- Keep state files concise enough to review in a normal pull request.
- Update state when blockers, receipt pointers, runtime roots, or lane goals change.
- Prefer artifact paths over inline evidence.
- Treat stale state as a bug.
