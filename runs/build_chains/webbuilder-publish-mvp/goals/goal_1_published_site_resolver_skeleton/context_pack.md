# Context Pack: goal_1_published_site_resolver_skeleton

## Goal Summary
- Lane: webbuilder
- Workflow: narrow_implementation
- Objective: Add domain_mapping plus site/site_version fixture and a host-based resolver for fake local subdomain tests.
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
- domain_mapping and site/site_version fixtures exist.
- Local tests use fake {site_slug}.hospio.ai host input.
- Host-based resolver maps host to persisted active site version.
- Guest-facing homepage renders from persisted version.
- No Webbuilder source edit occurs before Goal 0 receipt exists.

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
