# Example Lane State

Lane: `demo-lane`

Tooling root: `.`

Target source root: `examples/fake-app`

Runtime data root: `.agent-wave/runtime/demo-lane`

Branch: `main`

Status: `ready`

## Current Goal

Keep the fake app lane runnable while demonstrating token-efficient context packs and compact receipts.

## Allowed Paths

- `README.md`
- `docs/`
- `examples/fake-app/`
- `scripts/`
- `skills/`
- `templates/`
- `.agent-wave/lanes/demo-lane.yaml`
- `.agent-wave/context/`

## Forbidden Paths

- `.codex`
- `.codex-runtime`
- `.env`
- `.env.*`
- `secrets`
- `customer-data`
- `runtime`
- `artifacts/raw`
- `vendor/private`

## Read Before Work

- `docs/project_state/README.md`
- `docs/project_state/current_build_state.md`
- `docs/project_state/token_efficiency_rules.md`
- `docs/project_state/codex_run_contract.md`
- `skills/token-efficient-codex-run/SKILL.md`

## Last Receipts

- `reports/completions/latest_codex_completion.md`

## Known Blockers

- None.

## Completion Budget

Receipts: 120 lines. Context packs: 200 lines. Raw logs: referenced by path only.
