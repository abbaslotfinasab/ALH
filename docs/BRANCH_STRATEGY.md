# Branch strategy and repository governance

This repository follows the three-branch promotion model used by EatHub, adapted for the Astro static site.

## Long-lived branches

| Branch | Purpose | Incoming changes |
| --- | --- | --- |
| `develop` | Integration and day-to-day development | Feature/fix/docs branches through pull requests; direct pushes are technically allowed by the matching EatHub-style ruleset |
| `main` | Reviewed, validated release candidate | Pull request from `develop` only |
| `production` | Production-ready snapshot / deployment source | Pull request promotion after `main`; deployments are not configured by this document |

## Recommended workflow

1. Create short-lived branches from `develop`: `feat/*`, `fix/*`, `docs/*`, `chore/*`.
2. Open a pull request into `develop`; wait for **Astro static site validation / Build and validate**.
3. When a release is ready, open a pull request from `develop` into `main`. The required source-policy check enforces this direction.
4. Promote the reviewed `main` snapshot into `production` with a pull request.
5. Do not push directly to `main` or `production`; do not force-push or delete either protected branch.

## Required GitHub rulesets

The GitHub connector available during setup can create branches and commit repository files, but cannot create or edit repository rulesets. Apply these rules in **Settings → Rules → Rulesets**.

### `develop` ruleset

- Enforcement: Active
- Target: `refs/heads/develop`
- Block deletions
- Block force pushes / non-fast-forward updates
- No required PR rule (matches EatHub)

### `main` ruleset

- Enforcement: Active
- Target: `refs/heads/main`
- Block deletions
- Block force pushes / non-fast-forward updates
- Require pull requests (0 approvals, matching EatHub)
- Require all review threads to be resolved
- Allowed merge methods: merge, squash, rebase
- Require strict status checks:
  - `Astro static site validation / Build and validate`
  - `Astro static site validation / Require develop as PR source`

### `production` ruleset

- Enforcement: Active
- Target: `refs/heads/production`
- Block deletions
- Block force pushes / non-fast-forward updates
- Require pull requests (0 approvals, matching EatHub)
- Dismiss stale approvals when new commits are pushed
- Allowed merge methods: merge, squash, rebase

For all three rulesets, bypass actors should be empty and bypass mode should be **Never**, matching EatHub.

## CI behavior

The Astro validation workflow runs on pushes to `develop`, `main`, and `production`, and on pull requests targeting each of those branches. It runs the Astro build, npm audit, generated-output validation, and static performance budgets.

The source-policy job fails a pull request targeting `main` unless its source branch is `develop`. It is skipped for other pull-request targets.

## Deployment boundary

No deployment workflow, hosting configuration, production secret, DNS setting, or production service was changed or created. The `production` branch is only a protected release branch until a separate deployment plan is explicitly approved.
