# CodeLanes Roadmap

CodeLanes is organized around small public primitives that can be composed into larger multi-agent waves. Wave remains the protocol inside CodeLanes.

## v0.1 Lane Harness

- [x] Lane verification contract
- [x] Worktree, branch, and status checks
- [x] Forbidden-path audit
- [x] Detached run wrapper
- [x] Completion receipt template
- [x] Milestone commit gate

## v0.2 State Packs

- [x] `.agent-wave/lanes/<lane>.yaml` template
- [x] `.agent-wave/state/<lane>.json` model
- [x] Runtime bridge spec
- [x] Last receipt pointer
- [x] Blocker tracking

## v0.3 Skill Library

- [x] lane-verify skill
- [x] wave-smoke skill
- [x] wave-run-detached skill
- [x] completion-receipt skill
- [x] token-efficient-codex-run skill
- [x] completion-receipt-writer skill
- [x] log-hygiene skill
- [x] runtime-sync-check skill
- [x] forbidden-path-audit skill
- [x] state-pack-update skill
- [x] milestone-commit skill
- [x] merge-review skill

## v0.4 Wave Crew

- [x] Supervisor/subagent plan
- [x] Planner, implementer, tester, docs, safety, and merge-review agent roles
- [x] State pack per subagent
- [x] Receipt per subagent
- [x] No autonomous merge rule

## v0.5 Auto-Build Roadmap Runner

- [x] Roadmap item to wave plan
- [x] Wave plan to subagent prompts
- [x] Detached run orchestration
- [x] Test collection
- [x] Completion receipts
- [x] Merge proposal

## v0.6 Context Packs + Completion Receipts

- [x] Project state pack docs
- [x] Expanded lane YAML context schema
- [x] Context-pack generator command
- [x] Compact completion JSON template
- [x] Token-efficient markdown receipt template
- [x] Safe detached-run peek command
- [x] `/tmp/<task>_<timestamp>.run/.log/.done` marker pattern

## Builder Harness MVP

- [x] Lane registry
- [x] Lane guard
- [x] GoalSpec init
- [x] Context pack from goal file
- [x] Receipt init
- [x] Patch placeholder
- [x] Builder harness tests

## Goal Chain MVP

- [x] Sequential chain init command
- [x] Chain materialization into child GoalSpecs
- [x] Child context packs and receipt stubs
- [x] Chain status artifact
- [x] Chain completion artifact
- [x] Receipt update command for child progress
- [x] Chain refresh command for status and completion rollups
- [x] Chain next command for the next incomplete child goal
- [x] Session contract embedded in runner manifests
- [x] Structured CommandResult helper contract
- [x] Bounded repair loop docs scaffold
- [x] Supervised worker launcher dry-run plan/run/peek/collect
- [x] Two-part worker execution gate
- [ ] Parallel waves
- [ ] Repair loop integration

Progress flow:

```bash
scripts/codelanes goal-chain-init --lane demo --title "Demo chain" --objective "Make one small validated fake-app improvement"
scripts/codelanes goal-chain-materialize --chain-file runs/build_chains/demo-demo-chain/chain.json
scripts/codelanes goal-receipt-update --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state --status complete --tests-result passed --command "python -m pytest examples/fake-app/tests" --next-action "Proceed to next child goal"
scripts/codelanes goal-chain-refresh --chain-file runs/build_chains/demo-demo-chain
scripts/codelanes goal-chain-next --chain-file runs/build_chains/demo-demo-chain
scripts/codelanes worker-plan --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-run --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-peek --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
scripts/codelanes worker-collect --goal-dir runs/build_chains/demo-demo-chain/goals/audit_current_state
```

Current limitation: worker launch is single-goal and supervised. Dry-run is default, execution requires `--execute` plus `CODELANES_ENABLE_WORKER_EXEC=1`, and patch application, integration apply mode, repair execution, parallel workers, and swarms remain out of scope.

## v0.7 Trace Graph

- [x] Trace event template
- [x] Concept doc for run-to-receipt traceability
- [x] Fake app trace example
- [ ] Trace validation command
- [ ] Trace visualization export

## v0.8 Learning Ledger

- [x] Ledger entry template
- [x] Concept doc for explicit learning without hidden memory
- [x] Fake app ledger example
- [ ] Ledger compaction rules
- [ ] Ledger promotion workflow for reusable skills

## v0.9 Bounded Healing Loop

- [x] Healing receipt template
- [x] Concept doc for controlled repair
- [x] Fake app healing receipt example
- [ ] Attempt budget enforcement
- [ ] Automatic blocker classification

## v1.0 Goal Chain Waves

- [x] Goal chain template
- [x] Concept doc for roadmap-to-runs planning
- [x] Goal chain planner skill
- [ ] Goal chain runner command
- [ ] Completion rollup report

## v1.1 Autobrowse Proof and Merge Gates

- [x] Autobrowse proof concept doc
- [x] Merge review example
- [ ] Browser evidence attachment format
- [ ] Source/runtime proof separation checks
- [ ] Human merge gate checklist
