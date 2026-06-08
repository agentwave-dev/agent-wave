# Context Pack: goal_5_generated_subdomain_publish

## Goal Summary
- Lane: webbuilder
- Workflow: narrow_implementation
- Objective: Make generated {site_slug}.hospio.ai hosts resolve to site_id and active_version_id, with no custom domains yet.
- Created at: 2026-06-08T02:50:22Z

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
- Publish assigns generated subdomain metadata.
- Generated host resolves to site_id.
- Generated host resolves to active_version_id.
- Custom domain code path remains absent.
- Tests cover generated subdomain routing.

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
- No service restart unless a runtime safety goal explicitly allows it.
- Dependency receipt has a blocker.
- Forbidden path or private data would be touched.
