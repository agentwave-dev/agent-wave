# Bounded Repair Loop

This is the repair-loop scaffold only. CodeLanes does not execute repair workers yet.

Planned flow:

1. A child goal receipt records a failed or blocked result.
2. The failure is classified from compact receipt fields and short excerpts only.
3. A repair goal is created in the same lane.
4. The repair context is bounded to the parent goal and failure evidence.
5. The repair receipt records commands, changed files, blockers, and next action.
6. The parent receipt is updated.
7. The chain is refreshed so `chain_status.json` and `chain_completion.md` reflect the repair state.

Repair attempts must be capped by `max_repair_attempts`. A repair stays in the same lane and same allowed paths unless an operator expands scope explicitly. Raw logs are not copied into repair artifacts; receipts should point to bounded artifacts or include failure excerpts only.

Parent receipts remain the source of truth for chain progress. After every repair receipt, run `goal-chain-refresh` before continuing the chain.
