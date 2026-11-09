# Branch strategy and repository governance

This repository follows the three-branch promotion model used by EatHub, adapted for the Astro static site.

## Long-lived branches

| Branch | Purpose | Incoming changes |
| --- | --- | --- |
| `develop` | Integration and day-to-day development | Feature/fix/docs branches through pull requests; direct pushes are technically allowed by the matching EatHub-style ruleset |
| `main` | Reviewed, validated release candidate | Pull request from `develop` only |
| `production` | Production-ready snapshot / deployment source | Pull request promotion after `main`; every push to this branch triggers Cloudflare production deployment |

## Recommended workflow

1. Create short-lived branches from `develop`: `feat/*`, `fix/*`, `docs/*`, `chore/*`.
2. Open a pull request into `develop`; wait for **Build and validate**.
3. When a release is ready, open a pull request from `develop` into `main`. The required source-policy check enforces this direction.
4. Promote the reviewed `main` snapshot into `production` with a pull request. A successful merge pushes to `production` and starts the Cloudflare Worker Build automatically.
5. Do not push directly to `main` or `production`; do not force-push or delete either protected branch.

## Required GitHub rulesets

Apply and maintain these rules in **Settings → Rules → Rulesets**.

### `develop` ruleset

- Enforcement: Active
- Target: `refs/heads/develop`
- Block deletions
- Block force pushes / non-fast-forward updates
- No required PR rule (matches the current EatHub-style setup)

### `main` ruleset

- Enforcement: Active
- Target: `refs/heads/main`
- Block deletions
- Block force pushes / non-fast-forward updates
- Require pull requests (0 approvals)
- Require all review threads to be resolved
- Allowed merge methods: merge, squash, rebase
- Require strict status checks:
  - `Build and validate`
  - `Require develop as PR source`

### `production` ruleset

- Enforcement: Active
- Target: `refs/heads/production`
- Block deletions
- Block force pushes / non-fast-forward updates
- Require pull requests (0 approvals)
- Require all review threads to be resolved
- Dismiss stale approvals when new commits are pushed
- Require the strict `Build and validate` status check before merging
- Allowed merge methods: merge, squash, rebase

For all three rulesets, bypass actors should be empty and bypass mode should be **Never**.

## CI behavior

The GitHub Actions workflow runs on pushes to `develop`, `main`, and `production`, and on pull requests targeting each of those branches. It runs:

1. Dependency vulnerability audit (`npm audit`)
2. Astro type/content check and static build (`npm run build`)
3. Generated route and internal-reference validation (`npm run validate:output`)
4. Static performance budget validation (`npm run validate:performance`)

The source-policy job fails a pull request targeting `main` unless its source branch is `develop`. It is skipped for other pull-request targets.

## Production deployment

Cloudflare Worker Builds is connected to `abbaslotfinasab/ALH` and watches only the `production` branch.

- Worker: `alh`
- Build command: `npm audit && npm run build && npm run validate:output && npm run validate:performance`
- Deploy command: `npx wrangler deploy`
- Automatic builds: enabled
- Worker previews: enabled; preview builds use `npx wrangler preview`

A merge into `production` creates a push event. Cloudflare runs the production build command and deploys only if every command succeeds. A failed audit/build/validation stops deployment, leaving the previously deployed Worker version serving traffic.

GitHub Actions and Cloudflare both validate the release: GitHub checks pull requests and branch pushes; Cloudflare repeats the release-critical checks immediately before deploying. The GitHub `production` ruleset must require `Build and validate` to block a PR merge when the GitHub CI check fails. The Cloudflare build remains the final deployment gate even if GitHub checks are bypassed.

See [CI_CD.md](./CI_CD.md) for the end-to-end release procedure.
