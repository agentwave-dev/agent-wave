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

## v0.6 Trace Graph

- [x] Trace event template
- [x] Concept doc for run-to-receipt traceability
- [x] Fake app trace example
- [ ] Trace validation command
- [ ] Trace visualization export

## v0.7 Learning Ledger

- [x] Ledger entry template
- [x] Concept doc for explicit learning without hidden memory
- [x] Fake app ledger example
- [ ] Ledger compaction rules
- [ ] Ledger promotion workflow for reusable skills

## v0.8 Bounded Healing Loop

- [x] Healing receipt template
- [x] Concept doc for controlled repair
- [x] Fake app healing receipt example
- [ ] Attempt budget enforcement
- [ ] Automatic blocker classification

## v0.9 Goal Chain Waves

- [x] Goal chain template
- [x] Concept doc for roadmap-to-runs planning
- [x] Goal chain planner skill
- [ ] Goal chain runner command
- [ ] Completion rollup report

## v1.0 Autobrowse Proof and Merge Gates

- [x] Autobrowse proof concept doc
- [x] Merge review example
- [ ] Browser evidence attachment format
- [ ] Source/runtime proof separation checks
- [ ] Human merge gate checklist
