# Current Build State

Status: public scaffold with lane contracts, skills, state packs, detached runs, receipts, trace concepts, audits, and fake-app tests.

## Source Of Truth

- Repo entrypoint: `README.md`
- Roadmap: `docs/roadmap/goals.md`
- Generic demo lane: `.agent-wave/lanes/demo-lane.yaml`
- Token-efficiency rules: `docs/project_state/token_efficiency_rules.md`
- Codex run contract: `docs/project_state/codex_run_contract.md`

## Current Goal

Make Context Packs + Completion Receipts a reusable CodeLanes primitive so coding-agent runs can use durable memory, bounded prompts, safe log inspection, and compact completion evidence.

## Current Blockers

- None.

## Runtime Notes

Detached run logs belong in runtime paths or `/tmp` markers. Public docs and examples should reference raw logs by path only.
