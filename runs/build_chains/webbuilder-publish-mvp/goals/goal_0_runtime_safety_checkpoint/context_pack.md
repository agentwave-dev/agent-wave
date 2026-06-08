# Context Pack: goal_0_runtime_safety_checkpoint

## Goal Summary
- Lane: webbuilder
- Workflow: audit
- Objective: Prove hospio-site.service is stable and existing routes still work; do not expand Webbuilder product scope.
- Created at: 2026-06-08T02:50:21Z

## Lane Summary
- Source root: /home/joe/worktrees/wander-webbuilder
- Runtime data root: /home/joe/apps
- Expected branch: main
- Tmux session: codelanes-webbuilder

## Allowed Paths
- /home/joe/worktrees/wander-webbuilder
- runs/build_chains/webbuilder-publish-mvp
- reports/completions

## Forbidden Paths
- /stay routes
- checkout implementation owned by direct booking
- direct-booking Stripe code
- Hostaway live reservation writes
- private CRM mutation
- reports/direct_booking
- raw secrets or .env edits
- production DNS mutation
- custom domain automation before generated subdomains work

## Acceptance Criteria
- hospio-site.service stability evidence is captured without product expansion.
- Existing route checks are recorded with compact command results.
- No DNS, publish, or payment changes are made.
- No source edit occurs outside the Webbuilder lane.
- Runtime proof separates live status from source-build proof.

## Test Commands
- npm run build
- npm test

## Runtime Commands
- No runtime commands configured.

## Receipt Requirements
- context_pack.md
- receipt.json

## Stop Conditions
- expected_worktree: /home/joe/worktrees/wander-webbuilder
- runtime_data_root: /home/joe/apps
- Direct source edits should happen only in the webbuilder lane.
- /home/joe/apps is read-only unless deploy/sync is explicitly approved.
- Service restart is allowed only if this runtime safety goal explicitly documents operator approval.
- Wrong worktree or branch.
- Forbidden path or private data would be touched.
